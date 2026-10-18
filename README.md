# skills

`hstack`: personal agent skills and subagents for Claude Code and Codex, built to run inside T3 Code. The repo is a plugin marketplace for both tools.

| Skill | What it does |
| --- | --- |
| `bro` | Restates the last message in plain language, with no jargon. |
| `unslop` | Cuts AI tells from any writing. |
| `crawl-x` | Reads Tweets, threads and profiles on X as Markdown. |
| `how` | Explains how a part of the codebase works, with parallel explorers on big questions. |
| `why` | Digs through git, PRs and connected MCPs for the reasons behind code, with cited confidence levels. |
| `correct` | Finds mistakes agents keep repeating in a repo and blocks them with architecture, types, lints or tests. Runs only when you call it. |
| `swarm` | Fans out parallel workers (slices, races or both) and merges their results into one report. Uses T3 Code delegated tasks for cross-provider workers and isolated worktrees. Runs only when you call it. |

| Agent | What it does |
| --- | --- |
| `comment-sicko` | Deletes comments that don't earn their place and flags the code they excuse as `MUST KILL`. Uses the `how` and `why` skills. |

## Install

Claude Code:

```bash
claude plugin marketplace add hezaerd/skills
claude plugin install hstack@hezaerd
```

Codex:

```bash
codex plugin marketplace add hezaerd/skills
codex plugin add hstack@hezaerd
```

Pin a release in Codex with `--ref hstack--v<version>`. T3 Code runs both CLIs, so it picks up whatever they have installed.

Skills are namespaced by the plugin: call `/hstack:swarm` in Claude Code and `$hstack:swarm` in Codex. Claude Code names the agent `hstack:comment-sicko`.

### Update

```bash
claude plugin marketplace update hezaerd && claude plugin update hstack@hezaerd
codex plugin marketplace upgrade hezaerd && codex plugin add hstack@hezaerd
```

### Codex agents

Codex plugins don't ship subagents yet, so `comment-sicko` needs the sync script. It writes a TOML version to `~/.codex/agents/` (or `$CODEX_HOME/agents/`):

```bash
python scripts/sync-agents.py
```

Run it again after updating. Pass `--codex-dir` to install into a project, or `--dry-run` to see the output. Then "spawn the comment-sicko agent on this diff" in Codex.

### Other agents

Agents that read `SKILL.md` but not plugins can take the skills alone, without the `hstack:` prefix:

```bash
npx skills add hezaerd/skills -g
```

## Layout

```
.claude-plugin/marketplace.json     Claude Code marketplace
.agents/plugins/marketplace.json    Codex marketplace
plugins/hstack/
  .claude-plugin/plugin.json        Claude Code manifest
  .codex-plugin/plugin.json         Codex manifest
  skills/<name>/SKILL.md            shared by both tools
  skills/<name>/agents/openai.yaml  Codex-only skill metadata
  agents/*.md                       subagents in Claude Code's format
scripts/                            sync, version check, release helpers
```

## Develop

Clone to `~/dev/skills`, then load the plugin from the clone so edits apply without reinstalling.

Claude Code loads any plugin folder in `~/.claude/skills/` as `<name>@skills-dir`. Link it there instead of installing from the marketplace:

```powershell
# Windows
New-Item -ItemType Junction -Path "$HOME\.claude\skills\hstack" -Target "$HOME\dev\skills\plugins\hstack"
```

```bash
# macOS / Linux
ln -sfn ~/dev/skills/plugins/hstack ~/.claude/skills/hstack
```

Codex copies plugins into its cache, so add the clone as a local marketplace and reinstall after edits:

```bash
codex plugin marketplace add ~/dev/skills
codex plugin add hstack@hezaerd        # rerun after each edit to refresh the cache
```

Don't also install the skills another way (`npx skills`, links in `~/.agents/skills`), or each skill loads twice.

Before opening a PR:

```bash
claude plugin validate .
python scripts/check-versions.py
```

CI runs both on every PR.

## Release

1. Bump `version` in `plugins/hstack/.claude-plugin/plugin.json`, `plugins/hstack/.codex-plugin/plugin.json` and the `hstack` entry in `.claude-plugin/marketplace.json`. Add a `CHANGELOG.md` entry.
2. Merge to `master`.
3. Tag it from `master`: `claude plugin tag plugins/hstack --push`. This creates `hstack--v<version>` and fails if the manifests disagree.

## Credits

Thanks to [Lauren Tan](https://github.com/poteto) for [pstack](https://github.com/cursor/plugins/tree/main/pstack), an amazing tool for working with agents.

## License

[MIT](LICENSE).
