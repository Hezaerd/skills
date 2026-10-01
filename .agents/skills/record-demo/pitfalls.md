# Pitfalls

Failures seen while recording demos, with what fixed each one.

## Browser setup

- **`error while loading shared libraries: libatk-1.0.so.0`** (or another `.so`). The headless shell needs system libraries the machine lacks. `setup-browser.sh` unpacks them from `.deb` files with `apt-get download` and `dpkg-deb -x`, which need no root. It then needs `LD_LIBRARY_PATH` from `env.sh`. When a library is still missing, find the package that ships it (on Debian, search packages.debian.org for the file name), add the package to the list in the script, and run it again.
- **Screenshots with no text at all**, not even the logo's text. Fontconfig has no fonts. Source `env.sh`, which sets `FONTCONFIG_FILE` to the unpacked `fonts-liberation`. Web fonts load once fontconfig works.
- **`playwright install --with-deps` asks for sudo.** Don't use it. The script installs only the headless shell and ffmpeg, and unpacks the libraries itself.
- **`Cannot find package 'playwright-core'`.** ESM ignores `NODE_PATH`. The template loads Playwright with `createRequire` from `$RECORD_DEMO_DIR`, so source `env.sh` before running it.

## Reaching the app

- **The preview tool's `environment-port` navigation fails.** The tab runs in the T3 Code client the thread is viewed from, often the user's laptop, and its port forwarding to this machine doesn't work. The tools can't choose another machine. Fall back to headless Chromium and tell the user.
- **`ERR_CONNECTION_REFUSED` on 127.0.0.1** while `curl localhost` works. The server listens only on `::1`. Start it with `--host 0.0.0.0` or `--host 127.0.0.1`.
- **A server restart kills your shell** (exit code 144). `pkill -f "vp preview --port 4317"` matched the shell whose command line contained that same text. Stop servers by port with `kill-port.sh`.

## Waiting

- **`waitForURL` times out after a link click** in a single-page app. Client-side navigation changes the URL without a `load` event. Wait with `page.waitForFunction(() => location.pathname === "/path")` (the template's `waitForPath`).
- **`waitForLoadState("networkidle")` never resolves.** Captcha widgets, WebSockets and polling keep the network busy. Wait for a selector or a heading instead.
- **Sign-in does nothing.** The form submitted before React hydrated. Wait a moment after the inputs appear (the template waits 2 s), then fill and submit.
- **A hover changes the outcome.** Playwright's `click()` hovers first, and routers that preload on intent (TanStack Router's `defaultPreload: "intent"`, Next.js `Link`) fetch data on hover. If the demo is about what the first request does, show the hover as its own step with `locator.hover()`.

## Verifying behavior

- **Did the page fully reload?** Set a marker on `window` before the step (`markDocument()`), and check it after (`isSameDocument()`). A full load clears it.
- **Which build or version served a request?** Log response headers with `page.on("response", ...)`, and filter on the URL (for example `_serverFn` for TanStack Start server functions).
- **Old and new builds.** Build each variant once and copy its output aside (`cp -r dist /tmp/dist-v1`). During the recording, stop the server by port, swap the copied output into place, and restart it. This keeps the dead time to the server's restart.

## Video

- **The video file is empty or missing.** Playwright writes it when the context closes. Call `context.close()` before reading `page.video().path()`.
- **Format.** Playwright records WebM, and GitHub plays `.webm`, `.mp4` and `.mov` attachments, so no conversion is needed.
