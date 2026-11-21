# Changelog

## Unreleased

hstack now mirrors pstack 0.15.46 ([cursor/plugins@0b46ec3](https://github.com/cursor/plugins/commit/0b46ec3)), rewritten for T3 Code on Claude Code and Codex.

### hstack only

- The Babysit playbook has a `merge` mode. "Babysit this PR and merge when green" now merges on the watcher's `READY` verdict, pinned to that head, and reads the PR back to confirm. Before, Babysit said it never authorizes merging, so agents stopped at green and wrote a report. `drive` still stops at merge-ready.

### Since pstack 0.15.36

- Skill texts are much shorter. `hez-mode` drops from 151 lines to 111: its trigger list is eleven short lines, Writing the reply is one paragraph, and the Comments section is gone. 14 `principle-*` skills, `unslop` and `technical-writing` keep each rule in a shorter body, and `unslop` keeps its rule numbers.
- `how`, `why`, `reflect` and `architect` are each one short file. `how` starts one read-only subagent. `why` answers from the commits and PR discussions behind the code. `reflect` reads the thread itself, with no reviewers, and waits for approval before any edit. `architect` sketches two shapes and picks one, and sends a large or contested design to `arena`. Their `references/` folders are deleted, 21 files in all. `recall` starts its own investigator for each source.
- `hez-mode` no longer runs `how`. The playbooks tell the agent to trace the code itself.
- The Orchestrate playbook is deleted, which leaves twenty-two. Program-scale work goes to `figure-it-out`.
- The Opening a PR, Babysit and Multi-phase plan playbooks are cut to a few rules each. `check-plan.mjs` and its test are deleted.
- New `hez-mode/worker.md` holds the operator's rules for every started agent. The first line of each subagent brief points at it.
- Model roles follow the cuts. `hardest tasks`, `how explorer`, `how explainer`, `why investigators`, `why synthesizer`, `reflect tooling`, `reflect judgment, divergent, synthesizer` and `architect runners` are retired, and `setup-hstack` drops their lines on its next run. No role runs above `xhigh`, so the `unlimited` budget is gone and an old `unlimited` file becomes `large`. Trivial mechanical edits read `swarm workers`.
- A code role moves to the `judgment and prose` model only when the user names it or after two runs of the same brief on the role's own model fail their check. This is hstack's form of pstack's Fable 5.2 exception, and it replaces `hardest tasks`.
- hstack keeps its own defaults: Codex for code, Opus 5.5 for prose and judgment, and an Opus 5.5 and Codex panel. pstack's move to Opus-first routing, its Fable 5.2 exception and its Gemini 4 Neon panel seat are not ported.
- `statechart` now takes pstack's own native Windows support, so hstack's Windows patches to `run.ts` and `statechart.ts` are gone and the scripts match pstack's. It also reports the spec's line and column when SANY cannot read it, and draws an arrow into a parent state to the parent's border. All 33 corpus specs give the committed chart and report on Windows with TLC 1.7.4. The CLI tests still need a POSIX system.
- `sharpen`'s rewritten prompt asks the agent to prototype any choice an experiment can settle.

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
