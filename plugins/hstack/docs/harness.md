# Harness

hstack runs in T3 Code on Claude Code or Codex. Skills use neutral names. This file maps them to each harness. `<hstack>` is the plugin root, two levels above any `skills/<name>/SKILL.md`.

## Tools

| Skill text | Claude Code | Codex |
| --- | --- | --- |
| Open a todolist | `TodoWrite` | `update_plan` |
| Ask the user | `AskUserQuestion`. In `-p` mode it is absent, so ask in plain text and end the turn. | `request_user_input` when the session offers it. Otherwise ask in plain text and end the turn. |
| Run another hstack skill ("the **name** skill") | `Read` `<hstack>/skills/<name>/SKILL.md` and follow it. The `Skill` tool refuses skills with `disable-model-invocation: true`. | Read `<hstack>/skills/<name>/SKILL.md` and follow it. |
| Tell the user to type a skill, written `/hstack:<name>` | `/hstack:<name>` | `$hstack:<name>` |
| The `hez-agent` or `comment-sicko` agent | `subagent_type: "hstack:hez-agent"`, `"hstack:comment-sicko"` | the `hez-agent` or `comment-sicko` custom agent, installed from `<hstack>/codex/agents/` into `~/.codex/agents/` |
| Spawn a subagent | per [delegation](delegation.md) | per [delegation](delegation.md) |
| Wake when a PR changes | `watch_pull_request`, then end the turn. `unwatch_pull_request` before handing back. | same |
| Wake on a timer | `schedule_task` with an `interval` schedule bound to this thread. `delete_scheduled_task` when done. | same |
| Ask for a secret | `request_secret`. Pass the returned `secretRef` once. | same |
| Open a PR | `gh pr create`, then `link_pull_request` with its URL | same |
| Drive a web, Electron, or browser UI | T3 Code's `preview_*` tools | same |
| Drive a simulator or device | T3 Code's `device_*` tools | same |
| Show a chart, table, or diagram | `html_preview`, then `html_render` | same |

## Paths

| What | Claude Code | Codex |
| --- | --- | --- |
| Model file | `~/.claude/rules/hstack-models.mdc` | `~/.agents/rules/hstack-models.mdc` |
| Project agent instructions | `AGENTS.md`, or `CLAUDE.md` when the repo has no `AGENTS.md` | `AGENTS.md` |
| Project skills | `.claude/skills/` | `.agents/skills/` |
| User skills | `~/.claude/skills/` | `~/.agents/skills/` |
| Installed plugins | `~/.claude/plugins/`, manifest `.claude-plugin/plugin.json` | `~/.codex/plugins/`, manifest `.codex-plugin/plugin.json` |
| Custom agents | the plugin's `agents/` | `~/.codex/agents/*.toml` |
| hstack state (orchestration stores, automation state, logs) | `~/.hstack/` | `~/.hstack/` |

A skill that writes a new skill writes `SKILL.md` and, for Codex, `agents/openai.yaml` beside it: `interface.display_name`, `interface.short_description`, and `policy.allow_implicit_invocation: false` when the skill has `disable-model-invocation: true`.

### Transcripts

Read T3 threads first:

- This conversation is this thread. Its id is `parentThreadId` from `orchestrator_capabilities`. Read it with `t3_thread_read`, `view: "activity"` for tool calls.
- Past sessions in this project come from `t3_thread_list` and `t3_thread_search`, then `t3_thread_read`.
- A delegated task's run is its `childThreadId`.

When a step needs exact tool calls or arguments the thread view summarizes, read the harness transcript:

- Claude Code: `~/.claude/projects/<slug>/<session>.jsonl`. The slug is the workspace path with each `/`, `\`, `:`, and `.` changed to `-`, so `C:\Users\you\proj` is `C--Users-you-proj`. The newest `.jsonl` directly in that folder is the current session. Its `<session>/subagents/` folder holds native subagent transcripts.
- Codex: `~/.codex/sessions/<yyyy>/<mm>/<dd>/rollout-*.jsonl`. Each file's first line records its `cwd`. Use only files whose `cwd` is this workspace.

Read only this project's threads and this workspace's transcripts.
