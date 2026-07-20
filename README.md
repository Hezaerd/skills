# skills

Agent skills for [Cursor](https://cursor.com) and other coding agents, installable via [skills.sh](https://skills.sh).

[![skills.sh](https://skills.sh/b/Hezaerd/skills)](https://skills.sh/Hezaerd/skills)

## Install with skills.sh

```bash
# List skills in this repo
npx skills add Hezaerd/skills --list

# Install one skill globally for Cursor
npx skills add Hezaerd/skills --skill conventional-commits -g -a cursor -y

# Install everything in this repo for Cursor
npx skills add Hezaerd/skills --skill '*' -g -a cursor -y

# Install for every supported agent
npx skills add Hezaerd/skills --all
```

Direct path (also works):

```bash
npx skills add https://github.com/Hezaerd/skills/tree/main/skills/conventional-commits
```

Browse: [skills.sh/Hezaerd/skills](https://skills.sh/Hezaerd/skills)

## Available skills

| Skill | Description |
| ----- | ----------- |
| [`conventional-commits`](./skills/conventional-commits/) | Draft and validate Conventional Commit messages (commitlint-compatible). Agent-invoked on commit requests. |

## Repo layout

Skills follow the [Agent Skills](https://agentskills.io/) / [skills.sh](https://skills.sh) convention:

```text
skills/
  conventional-commits/
    SKILL.md
```

Each skill is a directory with a `SKILL.md` (YAML frontmatter + instructions). The CLI discovers any `**/SKILL.md` in the repo.

## Cursor-only install (without skills CLI)

```bash
git clone https://github.com/Hezaerd/skills.git ~/Developer/skills
mkdir -p ~/.cursor/skills
ln -s ~/Developer/skills/skills/conventional-commits ~/.cursor/skills/conventional-commits
```

## Force auto-use on commit (Cursor User Rule)

Skills are discovered from their `description`. To make commits reliably load
`conventional-commits`, add a **User Rule** in Cursor Settings:

> Whenever I ask to commit, create a git commit, or write/fix a commit message:
> read and follow the `conventional-commits` skill first, then run the normal
> git commit safety protocol.

## Agent invocation

These skills omit `disable-model-invocation`, so agents can load them from
context (not only via `/skill-name`). Keep descriptions specific: include both
**what** the skill does and **when** to use it.
