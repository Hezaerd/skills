---
name: conventional-commits
description: >-
  Draft and validate Conventional Commit messages (commitlint-compatible).
  Use whenever the user asks to commit, create a git commit, write or fix a
  commit message, amend a commit message, or when commitlint rejects a message.
  Always read this skill before drafting the message.
---

# Conventional Commits

Generate short, correct Conventional Commit messages. Prefer validating with
commitlint when the project has it configured.

## Output (mandatory)

When the user asks for a commit message only, your **entire reply** is the
message itself — nothing else.

- No preamble ("Here's your commit message", "Suggested message:", etc.)
- No explanations, rationale, or validation notes
- No markdown formatting (no code fences, no bold, no bullets)
- No follow-up questions unless you cannot draft a message without missing context

If a body is needed, include it with a blank line after the header. Otherwise
output a single line.

Example reply (this is the full response):

```
feat: add username
```

## Workflow (silent)

Do this internally; do not describe these steps to the user.

1. Inspect changes: `git status`, `git diff`, and `git diff --staged`. Read
   recent style with `git log --oneline -10`.
2. Draft one message (or header + optional body) matching repo style.
3. Validate when commitlint is available (see below). Fix until it passes.
4. Prefer a single-line header. Add a body only when the why is not obvious.
5. If the user only asked for a message: reply with only the validated message.
6. If the user asked to commit: create the commit with HEREDOC (below). Do not
   echo the message in chat unless they also asked for it.

## Format

```
<type>[optional scope]: <subject>

[optional body]
```

### Rules (`@commitlint/config-conventional`)

| Rule                   | Requirement                                                                                          |
| ---------------------- | ---------------------------------------------------------------------------------------------------- |
| `type-enum`            | One of: `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test` |
| `type-case`            | Lowercase (`feat`, not `Feat`)                                                                       |
| `subject-case`         | Lowercase start; no Sentence/Start/Pascal/UPPER case                                                 |
| `subject-full-stop`    | No trailing period                                                                                   |
| `header-max-length`    | Header ≤ 100 characters                                                                              |
| `body-max-line-length` | Body lines ≤ 100 characters                                                                          |

Also keep a blank line before body and before footer when those sections exist.

### Style defaults

- **Keep it simple**: one line is the default.
- **Imperative mood**: `add`, `fix`, `remove`, `refactor` — not `added`, `fixes`, `removing`.
- **Lowercase subject**: `feat: add username` not `feat: Add username`.
- **Scope only when useful**: omit by default; add when it clarifies area (`fix(auth): …`).
- **Match the repo**: mirror `git log` for scope usage, length, and tone.
- **Accurate type**: user-visible behavior → `feat`/`fix`; internal restructure → `refactor`; tooling/deps → `chore`/`build`/`ci`; docs only → `docs`.
- **No period** at the end of the subject.
- Focus on **why**, not a file list.

## Type picker

| Type       | Use when                                |
| ---------- | --------------------------------------- |
| `feat`     | New user-facing capability              |
| `fix`      | Bug fix                                 |
| `refactor` | Code change, no new feature or bug fix  |
| `perf`     | Performance improvement                 |
| `test`     | Tests only                              |
| `docs`     | README, comments, docs                  |
| `style`    | Formatting, whitespace; no logic change |
| `chore`    | Maintenance, lint, config, deps         |
| `build`    | Build system or bundler                 |
| `ci`       | CI/CD pipelines                         |
| `revert`   | Revert a prior commit                   |

## Examples

```
feat: add username
fix: resolve version drift detection
refactor: simplify auth helpers
chore: add husky and commitlint
```

### Anti-patterns

```
refact: simplify auth helpers    # invalid type (use refactor)
feat: Add username.             # wrong case + trailing period
fix(auth): Fix login bug        # scope OK, but subject must be lowercase
```

## Validate with commitlint (when available)

Detect in order; skip validation if none work:

1. Project binary: `bunx commitlint` / `npx commitlint` / `pnpm exec commitlint` / `yarn commitlint`
2. Config present: `commitlint.config.*`, `.commitlintrc*`, or `commitlint` key in `package.json`

Single-line:

```bash
echo "type: subject" | bunx commitlint
```

Multi-line:

```bash
printf '%s\n' "refactor: extract email sender module" "" "Move delivery behind a shared helper." | bunx commitlint
```

If commitlint is not installed, still follow the format rules above.

## Multi-line (only when needed)

Use when explaining non-obvious motivation or breaking changes:

```
refactor: extract email sender module

Move delivery behind a shared helper so auth and server
functions can reuse the same async API.
```

## Commit integration

When the user asks to commit (not just for a message), draft from staged
changes, validate when possible, then pass the final message via HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
feat: add username

EOF
)"
```

Follow the user's git safety protocol (status/diff/log, no force pushes, commit
only when asked, etc.). This skill only governs the message format and
validation.
