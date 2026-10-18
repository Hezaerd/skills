# Changelog

## hstack 0.1.0

First release as a plugin for Claude Code and Codex.

- Skills: `bro`, `unslop`, `crawl-x`, `how`, `why`, `correct`, `swarm`.
- Agent: `comment-sicko` (Claude Code through the plugin, Codex through `plugins/hstack/codex/agents/comment-sicko.toml`).
- The repo is a marketplace for both tools: `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`.
- Skills are namespaced: `/hstack:<skill>` in Claude Code, `$hstack:<skill>` in Codex.
