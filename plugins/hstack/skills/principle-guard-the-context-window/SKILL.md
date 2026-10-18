---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads. Run it with /hstack:principle-guard-the-context-window in Claude Code or $hstack:principle-guard-the-context-window in Codex."
disable-model-invocation: true
metadata:
  short-description: Keep bulk output out of the main context
---

# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
