---
name: principle-laziness-protocol
description: "Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem. Run it with /hstack:principle-laziness-protocol in Claude Code or $hstack:principle-laziness-protocol in Codex."
disable-model-invocation: true
metadata:
  short-description: Bias toward deletion and the smallest change
---

# Laziness Protocol

- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.
