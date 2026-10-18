---
name: sharpen
description: "Sharpen a task before starting: the expert approach, what the user is really after, and the right level of specification. Run it with /hstack:sharpen in Claude Code or $hstack:sharpen in Codex."
disable-model-invocation: true
metadata:
  short-description: Sharpen a task before starting it
---

Before starting, ask how a top expert would approach this task (their raw sources, their real methods, an outside check that the result is right), what the user is really after, and whether the task is over- or underspecified. Loosen constraints that don't serve the goal as readily as you add ones that do, and leave choices that are the user's to make open instead of deciding them. Fold in only what makes the work better, not bigger, but always keep one outside check that the result is right, without narrating the framing, then do the work. Don't hand back a rewritten prompt.
