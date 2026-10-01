#!/usr/bin/env bash
# Installs Playwright's headless Chromium without root and writes an env file to source.
# Usage: setup-browser.sh [workdir]   (default: ~/.cache/record-demo)
# Then:  source <workdir>/env.sh
set -euo pipefail

work="${1:-${RECORD_DEMO_DIR:-$HOME/.cache/record-demo}}"
mkdir -p "$work"
cd "$work"

# 1. playwright-core, the headless shell, and ffmpeg (needed for video).
[ -f package.json ] || echo '{ "private": true, "type": "module" }' > package.json
[ -d node_modules/playwright-core ] || npm install --silent --no-audit --no-fund playwright-core
node node_modules/playwright-core/cli.js install --only-shell chromium ffmpeg >/dev/null

shell=$(ls -d "${PLAYWRIGHT_BROWSERS_PATH:-$HOME/.cache/ms-playwright}"/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | sort -V | tail -1)
[ -x "$shell" ] || { echo "headless shell not found after install" >&2; exit 1; }

# 2. System libraries the shell needs, unpacked from .deb files instead of installed.
#    fonts-liberation plus libfontconfig1 are what make text render at all.
libs="$work/libs"
lib_dir="$libs/root/usr/lib/x86_64-linux-gnu"
missing() { LD_LIBRARY_PATH="$lib_dir" ldd "$shell" | awk '/not found/ { print $1 }'; }

if [ -n "$(missing)" ] || [ ! -d "$libs/root/usr/share/fonts" ]; then
  command -v apt-get >/dev/null || { echo "missing libraries and no apt-get:" >&2; missing >&2; exit 1; }
  mkdir -p "$libs/debs" "$libs/root"
  packages="fonts-liberation libfontconfig1 libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64
    libatspi2.0-0t64 libavahi-client3 libavahi-common3 libcairo2 libcups2t64 libdatrie1 libdrm2
    libfribidi0 libgbm1 libgraphite2-3 libharfbuzz0b libpango-1.0-0 libpixman-1-0 libthai0 libx11-6
    libxau6 libxcb-render0 libxcb-shm0 libxcb1 libxcomposite1 libxdamage1 libxdmcp6 libxext6
    libxfixes3 libxi6 libxkbcommon0 libxrandr2 libxrender1"
  # One package at a time, so a name this distribution lacks doesn't stop the rest.
  (cd "$libs/debs" && for p in $packages; do apt-get download -qq "$p" 2>/dev/null || echo "skipped $p" >&2; done)
  for deb in "$libs"/debs/*.deb; do dpkg-deb -x "$deb" "$libs/root"; done
fi

if [ -n "$(missing)" ]; then
  echo "still missing (find the package that ships each and add it above):" >&2
  missing >&2
  exit 1
fi

# 3. A fontconfig file pointing at the unpacked fonts.
cat > "$work/fonts.conf" <<CONF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>$libs/root/usr/share/fonts</dir>
  <cachedir>$work/fontcache</cachedir>
</fontconfig>
CONF

cat > "$work/env.sh" <<ENV
export RECORD_DEMO_DIR="$work"
export CHROME_PATH="$shell"
export LD_LIBRARY_PATH="$lib_dir\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"
export FONTCONFIG_FILE="$work/fonts.conf"
ENV

echo "ready: source $work/env.sh"
