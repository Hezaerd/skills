# skills

Personal agent skills for Claude Code, Codex and other agents that read `SKILL.md`.

| Skill | What it does |
| --- | --- |
| `bro` | Restates the last message in plain language, with no jargon. |
| `unslop` | Cuts AI tells from any writing. |
| `crawl-x` | Reads Tweets, threads and profiles on X as Markdown. |
| `github-pr` | Opens and updates PRs with `gh`, including image and video attachments. |
| `record-demo` | Records screenshots and video of a web app flow with headless Chromium, for PR demos. |
| `how` | Explains how a part of the codebase works, with parallel explorers on big questions. |
| `why` | Digs through git, PRs and connected MCPs for the reasons behind code, with cited confidence levels. |

## Install

With the [skills CLI](https://www.skills.sh/):

```bash
npx skills add hezaerd/skills -g
```

Or clone and symlink into each agent:

```bash
git clone https://github.com/hezaerd/skills ~/skills
for s in ~/skills/.agents/skills/*/; do
  n=$(basename "$s")
  ln -sfn "$s" ~/.claude/skills/$n
  ln -sfn "$s" ~/.agents/skills/$n
done
```

## Agents

Subagents live in `agents/*.md` in Claude Code's format. The sync script copies them to `~/.claude/agents/` and writes a TOML version to `~/.codex/agents/` (or `$CODEX_HOME/agents/`):

```bash
python scripts/sync-agents.py
```

Run it again after pulling changes. Pass `--claude-dir` and `--codex-dir` to install into a project instead, or `--dry-run` to see the output.

| Agent | What it does |
| --- | --- |
| `comment-sicko` | Deletes comments that don't earn their place and flags the code they excuse as `MUST KILL`. Uses the `how` and `why` skills. |

Call it by name: "use the comment-sicko agent on this diff" in Claude Code, or "spawn the comment-sicko agent on this diff" in Codex.

## Credits

`how`, `why` and `comment-sicko` are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, under the MIT license in [`LICENSE-pstack`](LICENSE-pstack). The changes swap Cursor-specific tools and model rules for Claude Code and Codex equivalents.
