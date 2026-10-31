# Changelog

## Unreleased

hstack now mirrors pstack 0.15.36 ([cursor/plugins@c742dd6](https://github.com/cursor/plugins/commit/c742dd6)), rewritten for T3 Code on Claude Code and Codex.

### Since pstack 0.15.26

- New `statechart` skill. It checks a TLA+ model with TLC and draws it as a Mermaid statechart in the reader's words, marks each state that breaks a rule, and gives the shortest path to each one. The compiler, its tests and its corpus are pstack's, with two hstack changes so it runs on Windows from Git Bash. Process trees are killed with `taskkill` instead of a `/bin/sh` process-group kill, TLC's CRLF output is read line by line like LF, and the check's worker gets `TEMP` and `TMP` as well as `TMPDIR`, so a killed run leaves no temporary folder. All 33 corpus specs give the committed chart and report on Windows. The test suite itself still needs a POSIX system, because it runs fake binaries through shebangs and sends signals. Rendered SVGs are shown with `html_preview` and `html_render`.
- New `maintain-formal-verification-skill`. It brings a formal verification back in line with the code after merges and refactors, and says whether each failure is drift in the verification or a bug in the code.
- New `ketchup-video`. It gives the `/hstack:ketchup` catch-up as a short subtitled video of slides.
- Orchestrate is agentic. The coordinator spawns workers per `docs/delegation.md`, keeps the program's state in one notes file at `~/.hstack/orchestrate/<slug>/notes.md`, watches PRs with `watch_pull_request`, and keeps one long `schedule_task` heartbeat. The `scripts/orch` CLI and its store are deleted.
- `interrogate` now keeps only findings an adversary proves with a run, and reuses arena's runner fan-out. Its four reference files are deleted.
- Autopilot-stack is Autopilot-full without the merge. A PR stacks only on a PR it builds on. Autopilot-full rebases when a concurrent change lands and pushes each finished unit before the next.
- `sharpen` hands back a deeper rewritten prompt and does not do the task.
- `create-formal-verification-skill` defaults to TLA+ for bad orderings, records each check's coverage and sync commit, and points at `statechart` and `maintain-formal-verification-skill`. `setup-hstack` offers a formal verification skill.
- `reflect` never edits a skill inside an installed plugin. It copies the skill to the project or user skills folder first.
- `arena` drops panel seats whose provider can't run a child task and never puts the cross-judge on the parent's provider. Smaller fixes land in `swarm`, `principle-explain-the-number`, `hez-mode`, `hez-help` and the PR watcher.

### pstack 0.15.26 port

- Every pstack skill except `make-bot-ui` is ported. `poteto-mode`, `poteto-agent` and `poteto-help` are now `hez-mode`, `hez-agent` and `hez-help`. `hez-mode` brings all 23 playbooks, the Bugbot triage reference, and its bun scripts (the PR watcher, plan checker and worktree audit). The other new skills are the 24 `principle-*` skills plus `architect`, `arena`, `automate-me`, `benchmark-checklist`, `blast-radius`, `create-formal-verification-skill`, `create-verification-skill`, `figure-it-out`, `in-your-own-words`, `interrogate`, `ketchup`, `maintain-verification-skill`, `no-comments`, `recall`, `reflect`, `sharpen`, `show-me-your-work`, `tdd`, `teach`, `technical-writing` and `typescript-best-practices`.
- New `luau-best-practices` skill, hstack's own, next to `typescript-best-practices`. It covers `--!strict` with the new type solver, a typed composition root instead of a folder-scanning module loader, typed metatable classes (`typeof(setmetatable({} :: Data, X))` with an explicit `self`), tagged unions with `never` exhaustiveness, parsing remote arguments from `unknown` on the server, cleanup ownership, and the `task` library. Every example in `references/patterns.md` type-checks under luau-lsp's new solver.
- `bro`, `unslop`, `how`, `why`, `swarm`, `correct` and `comment-sicko` are re-synced with pstack. As in pstack, every skill except `setup-hstack` (and hstack's own `crawl-x`) runs only when you call it. That now includes `how`, `why` and `bro`.
- `setup-hstack` mirrors `setup-pstack`. It detects models through `orchestrator_capabilities`, applies a reasoning budget, and writes the same per-role model file to `~/.claude/rules/hstack-models.mdc` (Claude Code) and `~/.agents/rules/hstack-models.mdc` (Codex). It replaces `~/.hstack/models.md` and its `fast` and `strongest` classes. Roles and defaults follow pstack: code roles default to `codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority`, and judgment and prose to `claudeAgent/claude-opus-5-5 effort=xhigh`.
- hstack assumes T3 Code. `docs/delegation.md` drops every fallback for running without it and holds the one set of spawn rules: read the model file, pick a native subagent or a `delegate_task` child, then drain. The new `docs/harness.md` maps skill text to Claude Code and Codex tools, paths and transcripts.
- Cursor-only features map to T3 Code:
  - cloud agents become delegated tasks in worktrees;
  - Automations become `schedule_task`;
  - `/loop` and the babysit watcher become `watch_pull_request`;
  - agent transcripts become T3 threads;
  - `control-ui` becomes the preview and device tools.

  Origin, `deslop` and Cursor's built-in skills are dropped.
- New `hez-agent` Codex agent at `plugins/hstack/codex/agents/hez-agent.toml`, next to `comment-sicko.toml`.
- pstack's guide (`docs/guide/`) and benny automation pack are not ported.
- New `scripts/check-skills.py`, run in CI. It fails when a skill's `agents/openai.yaml` drifts from its frontmatter, and when pstack or Cursor leftovers (`poteto`, Cursor paths, `Task`-tool fields, Cursor model slugs, no-T3 fallbacks) appear in the plugin. `--write` regenerates the YAML files.

## hstack 0.1.0

First release as a plugin for Claude Code and Codex.

- Skills: `bro`, `unslop`, `crawl-x`, `how`, `why`, `correct`, `swarm`.
- Agent: `comment-sicko` (Claude Code through the plugin, Codex through `plugins/hstack/codex/agents/comment-sicko.toml`).
- The repo is a marketplace for both tools: `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`.
- Skills are namespaced: `/hstack:<skill>` in Claude Code, `$hstack:<skill>` in Codex.
