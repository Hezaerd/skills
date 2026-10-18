# Changelog

## Unreleased

- `sharpen`: new skill from pstack ([cursor/plugins@79afd75](https://github.com/cursor/plugins/commit/79afd75)). Before starting a task, it asks how a top expert would approach it, what the user is really after, and whether the task is over- or underspecified, then does the work without handing back a rewritten prompt. Runs only when you call it.
- `setup-hstack`: new skill that picks the provider, model and reasoning effort for each worker role (`how explorers`, `why synthesizer`, `swarm race arms`, ...) from the models T3 Code lists, under a budget, and writes them to `~/.hstack/models.md`.
- `docs/delegation.md` resolves each spawn's model from that file: the role's line, then its `fast` or `strongest` class line, then the parent model. Models on another provider go through T3 Code delegated tasks.
- `unslop`: synced with pstack ([cursor/plugins@bc697d0](https://github.com/cursor/plugins/commit/bc697d0)). It no longer runs on its own (`disable-model-invocation: true`), and "Must always apply." is gone from the description. The process steps are now one sentence, and several rules use tighter wording. No rules were added or removed.
- `docs/delegation.md` holds the shared rules for spawning workers: detect T3 Code, pick models, pick native, T3 delegated or inline transport, and drain. `swarm`, `how` and `why` read it.
- `swarm` falls back to native subagents when T3 Code is absent instead of calling `orchestrator_capabilities` unconditionally.
- `how` and `why` can run workers on other providers through T3 Code delegated tasks.

## hstack 0.1.0

First release as a plugin for Claude Code and Codex.

- Skills: `bro`, `unslop`, `crawl-x`, `how`, `why`, `correct`, `swarm`.
- Agent: `comment-sicko` (Claude Code through the plugin, Codex through `plugins/hstack/codex/agents/comment-sicko.toml`).
- The repo is a marketplace for both tools: `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`.
- Skills are namespaced: `/hstack:<skill>` in Claude Code, `$hstack:<skill>` in Codex.
