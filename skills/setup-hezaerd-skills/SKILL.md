---
name: setup-hezaerd-skills
description: >-
  Configure this repo for Hezaerd skills. Run once after installing from
  Hezaerd/skills — currently offers to add a conventional-commits instruction
  block to AGENTS.md or CLAUDE.md.
disable-model-invocation: true
---

# Setup Hezaerd Skills

Prompt-driven per-repo setup for skills from [Hezaerd/skills](https://github.com/Hezaerd/skills).
Explore, present what you found, confirm with the user, then write.

This is not a silent scaffold. Ask before editing.

## Process

### 1. Explore

Read the current repo; don't assume:

- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist?
- Is there already an `## Agent skills` section in either?
- Is there already a `### Conventional commits` (or equivalent) subsection?
- Is the `conventional-commits` skill installed? (a `conventional-commits`
  skill folder alongside this one, or listed in available skills.)

### 2. Present findings and ask

Summarise what's present and what's missing in one short paragraph.

Then ask **one** question (for now):

> Do you want to add a **Conventional commits** section to your agent
> instructions file (`AGENTS.md` or `CLAUDE.md`) so the agent always uses the
> `conventional-commits` skill when committing? (recommended: **yes**)

Lead with the recommendation so they can accept in a word.

- On **no** — stop. Tell them setup is skipped; they can re-run this skill later.
- On **yes** — continue to confirm and write.

### 3. Confirm

Show a draft of the block that will be written (see below). Let them edit
before you write.

**Pick the file:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask which one to create — don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) —
always edit the one that's already there.

If an `## Agent skills` block already exists, update it in-place (add or
refresh the Conventional commits subsection). Do not append a duplicate
`## Agent skills` heading. Don't overwrite unrelated sections.

### 4. Write

Use this block shape:

```markdown
## Agent skills

### Conventional commits

When the user asks to commit, create a git commit, or write/fix a commit
message: read and follow the `conventional-commits` skill first. Prefer
commitlint-compatible Conventional Commits (`type: subject`, lowercase
subject, no trailing period).
```

If `## Agent skills` already exists, only add or replace the
`### Conventional commits` subsection under it.

### 5. Done

Tell the user:

- Which file was updated (or that nothing changed if they declined)
- That commit / commit-message requests should now load `conventional-commits`
- They can edit the section by hand later; re-run this skill only to re-apply
  or start over

Do not install skills yourself in this flow — assume they already ran
`npx skills add Hezaerd/skills` (or equivalent). If `conventional-commits`
appears missing, mention they should install it, then continue with the
AGENTS/CLAUDE question if they still want it.
