---
name: record-demo
description: Records screenshots and a video of a web app flow with headless Chromium and Playwright, for PR demos and visual checks. Use when asked to record a demo, capture screenshots or a video of a UI change, show a change working in the browser, or add demo media to a PR, including when the T3 Code preview browser can't reach the dev server.
metadata:
  short-description: Record UI demos with headless Chromium
---

# Record a demo

Follow these steps in order. Each one ends with a check; don't move on until it passes. Script paths are in this skill's directory, which Claude Code substitutes for `${CLAUDE_SKILL_DIR}`.

1. **Try the T3 Code preview tool first, when it's available.** Open a tab and navigate to the app with `preview_navigate` and `{ kind: "environment-port", port }`. If that works, record with `preview_recording_start` and `preview_recording_stop`, take screenshots with `preview_snapshot` and `save: true`, and skip to step 6.
   - If the navigation fails, load a public URL such as `https://example.com`. If the public URL loads, the tab runs on the user's machine and can't reach this one. Test once more against a plain server (`python3 -m http.server 5173 --bind 127.0.0.1`) to rule out the app.
   - Then fall back to headless Chromium without asking, and say in your report that the preview browser couldn't reach this machine. Don't retry the preview tool in a loop, and don't open a public tunnel.
2. **Set up headless Chromium.** Run `${CLAUDE_SKILL_DIR}/scripts/setup-browser.sh`, then `source ~/.cache/record-demo/env.sh` in every shell that runs the browser. The script needs no root. It installs `playwright-core`, the headless shell and ffmpeg, unpacks missing system libraries and fonts from `.deb` files, and writes the env file. It exits non-zero and names any library it still can't find.
3. **Serve the app on 127.0.0.1.** Prefer the production build and preview over the dev server. HMR reloads the page when the server restarts, and a production build behaves like what ships. Bind to `0.0.0.0` or `127.0.0.1`, since some dev servers listen only on `::1`. Use `127.0.0.1` in URLs. Seed data and use the project's seeded accounts. Confirm with `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:<port>/`.
4. **Write the recording script.** Copy `${CLAUDE_SKILL_DIR}/scripts/demo-template.mjs` to a scratch directory and edit its sign-in and steps. The template signs in outside the recording, records a second context with the saved session, and takes screenshots after fonts load. Add `sleep` pauses between steps so viewers can follow, and assert each thing the demo claims. Run it with `BASE_URL=... OUT_DIR=... node demo.mjs`.
5. **Look at the output.** Open every screenshot with the Read tool before using it. A blank page or missing text means fonts or the server failed. Check the logged console errors. If the demo exposes a bug, fix the code first, then record again.
6. **Attach the media to the PR.** Follow the `github-pr` skill. Reference each file in the body with `![alt](./file.png)` or `![](./demo.webm)`, pass the same paths with `--attach`, then read the body back and confirm every reference became a `user-attachments` URL. Describe each step in the PR text, next to the media.
7. **Clean up.** Stop the servers you started with `${CLAUDE_SKILL_DIR}/scripts/kill-port.sh <port>`. Never `pkill -f` a pattern that also appears in your own command line; it kills the shell running it.

## Rules for the media

- Don't inject captions or overlays into the page. Reviewers read them as app UI. Put the narration in the PR text.
- Show the real flow. Don't stub responses or edit the DOM to fake a state the app can't reach on its own.
- Use one viewport for every capture, 1280×800 unless the change is about narrow screens.
- Start the video on the page that matters. Sign-in, seeding and builds happen before recording starts.
- When the demo needs a server change mid-flow, such as a new deploy, build every variant before recording and only swap and restart during it. Say in the PR what the pause in the video is.

## Files

- `scripts/setup-browser.sh [workdir]` installs the browser and writes `<workdir>/env.sh` (default `~/.cache/record-demo`).
- `scripts/demo-template.mjs` is the recording script to copy and edit. It has helpers for screenshots, waiting on a path, and detecting a full page reload.
- `scripts/kill-port.sh <port>` stops whatever listens on a port.
- [pitfalls.md](pitfalls.md) lists failures seen while recording and their fixes. Read it when a step fails or hangs.
