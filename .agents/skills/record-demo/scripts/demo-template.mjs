// Records a demo video and screenshots of a web app with headless Chromium.
// Copy this file, edit the sections marked EDIT, then run:
//   source "$RECORD_DEMO_DIR/env.sh" && BASE_URL=http://127.0.0.1:5173 node demo.mjs
import { createRequire } from "node:module"
import { mkdirSync, renameSync } from "node:fs"

const { chromium } = createRequire(`${process.env.RECORD_DEMO_DIR}/`)("playwright-core")

const base = process.env.BASE_URL ?? "http://127.0.0.1:5173"
const out = process.env.OUT_DIR ?? "/tmp/demo-media"
const viewport = { width: 1280, height: 800 }

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

mkdirSync(out, { recursive: true })

const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH,
  args: ["--no-sandbox"],
})

// EDIT: sign in outside the recording, so the video starts on the page that matters.
// Delete this block and `storageState` below when the flow needs no account.
const setup = await browser.newContext({ viewport })
const login = await setup.newPage()
await login.goto(`${base}/sign-in`)
await login.locator("input").first().waitFor()
await sleep(2000) // let the page hydrate, or the form submits natively
await login.fill('input[name="email"]', "dev@example.test")
await login.fill('input[name="password"]', "password123")
await login.click('button[type="submit"]')
await login.waitForFunction(() => location.pathname.startsWith("/dashboard"), null, {
  timeout: 30_000,
})
const storageState = await setup.storageState()
await setup.close()

const context = await browser.newContext({
  viewport,
  storageState,
  recordVideo: { dir: `${out}/raw`, size: viewport },
})
const page = await context.newPage()

page.on("console", (message) => {
  if (message.type() === "error") console.log("console error:", message.text().slice(0, 200))
})
page.on("pageerror", (error) => console.log("page error:", error.message))

async function screenshot(name) {
  await page.evaluate(() => document.fonts.ready)
  await page.screenshot({ path: `${out}/${name}.png` })
  console.log("screenshot", `${out}/${name}.png`)
}

// Client-side navigation never fires `load`, so wait on the path instead of waitForURL.
async function waitForPath(pathname, timeout = 15_000) {
  await page.waitForFunction((path) => location.pathname === path, pathname, { timeout })
}

// Marks the current document. `isSameDocument()` turns false once the page fully reloads.
const markDocument = () => page.evaluate(() => (window.__demoDocument = true))
const isSameDocument = () => page.evaluate(() => window.__demoDocument === true)

// EDIT: the steps. Pause between them so viewers can follow, and assert what the
// demo claims, so a broken flow fails here instead of in the PR.
await page.goto(`${base}/dashboard`)
await page.getByRole("heading").first().waitFor()
await markDocument()
await sleep(1500)
await screenshot("01-start")

await page.getByRole("link", { name: "Settings" }).click()
await waitForPath("/dashboard/settings")
await sleep(1500)
await screenshot("02-after")
console.log("same document after navigation:", await isSameDocument())

// Closing the context finishes writing the video.
const video = page.video()
await context.close()
renameSync(await video.path(), `${out}/demo.webm`)
await browser.close()
console.log("video", `${out}/demo.webm`)
