---
name: crawl-x
description: Read Tweets, threads and profiles on X. Use whenever the user shares an x.com or twitter.com link or asks you to look at a Tweet or account.
metadata:
  short-description: Read X posts as Markdown
---

# Crawl X

x.com cannot be fetched directly. Fetch the same URL through `x.pcstyle.dev`, which returns Markdown.

## Fetch

1. Replace the hostname `x.com` (or `twitter.com`) with `x.pcstyle.dev`. Keep the path and query string unchanged.
2. Fetch the new URL with your web fetch tool, or `curl -sS <url>`.

| Original | Fetch |
| --- | --- |
| `https://x.com/jack/status/20` | `https://x.pcstyle.dev/jack/status/20` |
| `https://x.com/jack` | `https://x.pcstyle.dev/jack` |

## What comes back

- **Status URL:** the post first, then its replies, each numbered ("Post 1/11", "Reply 2/11") with author, text and a `Source:` link.
- **Profile URL:** the bio and a list of the latest posts, each with a `[Source]` link.
- Images appear as `pbs.twimg.com` links. Open them to see the image.

## Navigate

- `Source:` links point at `x.com`. Rewrite the hostname again before following one.
- To read a reply's own thread, fetch its `Source:` URL through `x.pcstyle.dev`.
- To see more of an account, take a status link from its profile page.
- `x.com/i/article/...` links are long-form articles. Fetch them the same way.

## Limits

- The service allows about 600 requests per minute per IP. Fetch only what the question needs.
- If a fetch fails, say so. Do not guess at what a Tweet says.
