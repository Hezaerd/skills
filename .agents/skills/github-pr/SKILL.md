---
name: github-pr
description: Create or update a GitHub pull request or issue with the gh CLI, including image and video attachments. Use when asked to open, edit or comment on a PR or issue, or to add screenshots or recordings to one.
metadata:
  short-description: Open PRs with gh, with media
---

# GitHub pull requests

Use the `gh` CLI for everything on GitHub. Run `gh auth status` first if a command fails with an auth error.

## Open a PR

1. Check the branch: `git status`, `git log --oneline <base>..HEAD`. Push it with `git push -u origin HEAD`.
2. Write the body to a file and create the PR:

   ```bash
   gh pr create --base <base> --title "<title>" --body-file body.md
   ```

   Add `--draft` when the work is not ready for review.
3. Print the PR URL back to the user.

A good body says what changed and why, how it was tested, and anything a reviewer should look at first. Match the repo's commit and PR title style.

## Inspect and update

```bash
gh pr view [<number>]                # description, status, checks
gh pr checks [<number>]               # CI status
gh pr diff [<number>]
gh pr edit [<number>] --title "..." --body-file body.md
gh pr comment [<number>] --body-file comment.md
gh pr ready [<number>]                # mark a draft ready
```

When editing a body, read the current one first with `gh pr view --json body -q .body` and keep its existing content.

## Attachments

`--attach` works on `gh issue create`, `gh issue edit`, `gh issue comment`, `gh pr create`, `gh pr edit` and `gh pr comment`.

- Pass a local file path with each `--attach`. Repeat the flag for different files, never for the same file twice.
- Alt text goes after `#`: `--attach './login.png#The login error state'`. Video has no alt text.
- For inline placement, use `--body-file` with local Markdown references and attach the same paths.
  - Image: `![descriptive alt text](PATH/TO/IMAGE)`
  - Video player: `![](PATH/TO/VIDEO)` alone in its paragraph
- The CLI replaces these references with uploaded URLs. Attachments not referenced in the body are appended to it.

Example:

```bash
gh pr create --base master --title "Fix login error state" \
  --body-file body.md --attach ./before.png --attach ./after.png
```

### Check the result

- Uploads need push access to the repo and a supported image or video format.
- After posting, read the body back and confirm it contains uploaded URLs, not local paths. Check rendering in a browser when one is available.
- If some uploads fail, the PR is still created and the command exits non-zero with the URL printed. Report which files failed.
- If `gh` lacks `--attach`, access is insufficient, or the format is unsupported, report that specific blocker. Do not say media was embedded when it was not.
