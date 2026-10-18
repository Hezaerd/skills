---
name: principle-encode-lessons-in-structure
description: "Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text. Run it with /hstack:principle-encode-lessons-in-structure in Claude Code or $hstack:principle-encode-lessons-in-structure in Codex."
disable-model-invocation: true
metadata:
  short-description: Encode repeated lessons as structure, not text
---

# Encode Lessons in Structure

If the lesson needs judgment and cannot be encoded, make the instruction more prominent and add an example of the failure mode.

**Corollary:** If the fix is structural, only use the structural fix. The instruction is the symptom.
