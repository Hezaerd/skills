# skills

Agent skills installable via [skills.sh](https://skills.sh). Works with Claude Code, Codex, Cursor, OpenCode, and other agents the CLI supports.

[![skills.sh](https://skills.sh/b/Hezaerd/skills)](https://skills.sh/Hezaerd/skills)

## Quickstart

1. Install from this repo:

```bash
npx skills@latest add Hezaerd/skills
```

2. Pick the skills you want and which agents to install them for. **Include `/setup-hezaerd-skills`.**

3. In your coding agent, run:

```text
/setup-hezaerd-skills
```

It will ask whether to add a Conventional commits section to `AGENTS.md` or `CLAUDE.md` so the agent uses that skill on commit.

## Available skills

| Skill | Description |
| ----- | ----------- |
| [`setup-hezaerd-skills`](./skills/setup-hezaerd-skills/) | Per-repo setup flow. Run once after install. |
| [`conventional-commits`](./skills/conventional-commits/) | Draft and validate Conventional Commit messages (commitlint-compatible). |

## Install options

```bash
# List skills
npx skills add Hezaerd/skills --list

# Install specific skills
npx skills add Hezaerd/skills --skill setup-hezaerd-skills --skill conventional-commits

# Global install for one agent (example: claude-code)
npx skills add Hezaerd/skills --skill '*' -g -a claude-code -y

# All skills, all supported agents
npx skills add Hezaerd/skills --all
```

Direct path:

```bash
npx skills add https://github.com/Hezaerd/skills/tree/main/skills/conventional-commits
```

Browse: [skills.sh/Hezaerd/skills](https://skills.sh/Hezaerd/skills)

## Repo layout

```text
skills/
  setup-hezaerd-skills/
    SKILL.md
  conventional-commits/
    SKILL.md
```

Each skill is a directory with a `SKILL.md` ([Agent Skills](https://agentskills.io/) format). The CLI discovers any `**/SKILL.md` in the repo.

## Agent invocation

- `setup-hezaerd-skills` sets `disable-model-invocation: true` — run it explicitly (`/setup-hezaerd-skills`).
- `conventional-commits` is agent-invokable: strong description triggers on commit / commit-message requests. The setup skill can also pin that habit in `AGENTS.md` / `CLAUDE.md`.
