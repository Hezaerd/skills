---
name: setup-hstack
description: "Configure which models hstack uses per role and at what reasoning budget. Detects the models T3 Code can run and writes the hstack model file that overrides the skill defaults. Use for /hstack:setup-hstack, \"configure hstack models\", \"hstack budget\", or changing hstack's model choices."
metadata:
  short-description: Choose which models hstack uses per role
---

# Setup hstack

Write the hstack model file, which sets hstack's model per role. Write the same content to both paths so either harness finds it: `~/.claude/rules/hstack-models.mdc` for Claude Code and `~/.agents/rules/hstack-models.mdc` for Codex. [Delegation](../../docs/delegation.md#pick-the-models) defines the value format and reads the file before every fan-out.

## Steps

### 1. Detect available models

Call `orchestrator_capabilities`. Keep only providers with `canRunChildTask: true`. For each model, note its id and its options with their values. The effort option is `effort` on Claude models and `reasoningEffort` on Codex models. The speed option is `serviceTier` on Codex models (`priority` is fast) and `fastMode` on Claude models that list it. Never write a model, option, or value you have not detected. The alias `inherit-parent` is always valid.

### 2. Load current state

The default role-to-model mapping is the file shape shown in step 5 below. If the model file exists at either path, read it and treat its `# budget` line and its role values as the current choices. When both exist and differ, use the one for the harness you are running in. Otherwise start from those defaults. A line whose role is not in step 5, such as `how critics`, is from a retired role. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Ask the user with these four options and these exact labels, and name the current budget when the file records one. With no file, say that `large` matches the skill defaults.

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Build the working table from the skill defaults, and on a re-run keep any role you changed by model, list, or alias (`inherit-parent`). `unlimited`, `large`, `medium`, and `small` set the effort option of every real value, panel entries included, to `max`, `xhigh`, `high`, or `medium`, on the ladder `max` > `xhigh` > `high` > `medium` > `low`. If the model does not list that level, use its highest listed level below the target, else mark the role as needing a choice. Never set `ultra`, `ultracode`, or `ultrathink` through the budget. They do more than deepen reasoning, so set them only when the user names them. Leave speed options as they are. `inherit-parent` does not change. So `unlimited` turns `claudeAgent/claude-opus-5-5 effort=xhigh` into `claudeAgent/claude-opus-5-5 effort=max`. `large` keeps both defaults. `small` turns them into `claudeAgent/claude-opus-5-5 effort=medium` and `codex/gpt-6.1-sol reasoningEffort=medium serviceTier=priority`.

**(c) Show the roles and confirm.** Show every role with its value, marking any value not in the detected set as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` (this role runs on the parent thread's model) as the options. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose provider differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm. Warn that `why investigators` need MCP servers, and a delegated child has only its own provider's MCP setup, so that provider needs the user's evidence sources configured too.

### 4. Validate

Every real value written must use a detected provider, model, option id, and option value. `inherit-parent` always passes. If a chosen value is not available, stop and ask again.

### 5. Write the file

Create `~/.claude/rules/` and `~/.agents/rules/` if needed. Write the same content to both files, with a `# budget` line holding the chosen label and its target effort, and one line per role, using the same labels the skills use. Overwrite each whole file so re-runs stay idempotent. Shape:

```
# hstack model configuration. One line per role. Delete a line to fall back to the skill default.
# Values: <providerInstanceId>/<model> <option>=<value> ... or inherit-parent (the parent thread's model). Alias entries in a panel list still count toward its fan-out.
# budget: large (xhigh)
feature, refactoring: codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
bug-fix: codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
perf-issue: codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
hillclimb: codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
judgment and prose: claudeAgent/claude-opus-5-5 effort=xhigh
hardest tasks: claudeAgent/claude-opus-5-5 effort=xhigh
how explorer: codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
how explainer: claudeAgent/claude-opus-5-5 effort=xhigh
why investigators: codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
why synthesizer: claudeAgent/claude-opus-5-5 effort=xhigh
reflect tooling: codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
reflect judgment, divergent, synthesizer: claudeAgent/claude-opus-5-5 effort=xhigh
arena runners: claudeAgent/claude-opus-5-5 effort=xhigh, codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
arena cross-judge pool: claudeAgent/claude-opus-5-5 effort=xhigh, codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
swarm workers: codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
architect runners: claudeAgent/claude-opus-5-5 effort=xhigh, codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
interrogate reviewers: claudeAgent/claude-opus-5-5 effort=xhigh, codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority
```

### 6. Confirm

Tell the user where both files are and that they apply from the next fan-out, with no new session needed. Re-running this skill updates them.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /hstack:create-verification-skill." On yes, run the **create-verification-skill** skill. On no, move on without pushing.
