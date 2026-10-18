---
name: setup-hstack
description: "Choose which provider, model, and reasoning effort each hstack worker role runs on, and write them to ~/.hstack/models.md. Detects available models through T3 Code. Use for /hstack:setup-hstack, \"configure hstack models\", \"hstack budget\", or changing which models how, why, or swarm spawn. Run it with /hstack:setup-hstack in Claude Code or $hstack:setup-hstack in Codex."
disable-model-invocation: true
metadata:
  short-description: Choose which models hstack workers run on
---

# Setup hstack

Write `~/.hstack/models.md`, the per-role model choices that [delegation](../../docs/delegation.md#pick-the-models) reads before every fan-out. Read that section first: it defines the roles, their classes, the value format, and how a value becomes a spawn.

## 1. Detect models

Call `orchestrator_capabilities` from the `t3-code` MCP server (the name may carry a prefix such as `mcp__t3-code__`). In Claude Code, search deferred tools with `ToolSearch` for `t3-code` before you decide it is absent.

Keep only providers with `canRunChildTask: true`. For each model, note its id and its options with their values. The reasoning option is the one labeled "Reasoning" (`effort` for Claude, `reasoningEffort` for Codex). Record the parent provider from `inheritedProviderInstanceId`.

Never write a model, option, or value you didn't detect. `inherit-parent` is always valid.

Without T3 Code, you can't detect models on any provider. Say so, and offer only `inherit-parent` values in step 3. The budget still applies to them.

## 2. Load current state

If `~/.hstack/models.md` exists, read it. Its `# budget` line and role lines are the current choices. Keep the `fast` and `strongest` class lines. Drop any other line whose role isn't in the delegation table, and keep the dropped lines to show in step 3.

With no file, start from:

```
fast: inherit-parent effort=medium
strongest: inherit-parent effort=high
```

## 3. Budget, map, confirm

**(a) Ask for a budget.** Use `AskUserQuestion` in Claude Code; otherwise ask in plain text. Offer these labels, and name the current budget when the file records one. With no file, say that `medium` matches the defaults.

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** The ladder is `low` < `medium` < `high` < `xhigh` < `max`. The budget's level is the target. Set the reasoning option of each line:

- `strongest`, its roles, every `swarm race arms` entry, and a `swarm workers` own line get the target.
- `fast` and its roles get one step below the target. So `medium` puts fast at `medium` and strongest at `high`, the same as the defaults.

If a model doesn't list the level, use its highest listed level below it. Never write `ultra`, `ultracode`, or `ultrathink` through the budget: they do more than deepen reasoning. Set them only when the user asks for them by name. Leave other options, such as `serviceTier` or `fastMode`, as they are.

**(c) Show and confirm.** Show a table with every role from the delegation table, its value, and where the value comes from (own line or class line). List the lines step 2 dropped. Ask whether to accept or change specific roles. Offer the detected models, `inherit-parent`, and a class name as choices.

- Suggest a cross-provider `swarm race arms` list when more than one provider can run child tasks: the top model of each, at the target.
- A role set to its class name, or left unset, follows the class line. Write an own line only when it differs. Unset `swarm workers` follows `fast` or `strongest` per slice; an own line puts every slice on that value.
- Warn when a `why investigators` value is on another provider: those investigators need MCP servers, and a delegated child only has its own provider's MCP setup.

## 4. Validate

Check every written value against step 1's catalog: provider, model, option ids, and option values. `inherit-parent` with `effort=<level>` on the ladder always passes. If a value fails, show why and ask again.

## 5. Write the file

Create `~/.hstack/` if needed. Overwrite `~/.hstack/models.md` completely so re-runs give the same result. Shape:

```
# hstack model routing, read by docs/delegation.md before every fan-out.
# One line per role. Delete a line to fall back to its class, then to the parent model.
# Values: <providerInstanceId>/<model> <option>=<value> ... | inherit-parent [effort=<level>] | fast | strongest
# budget: medium (high)
fast: codex/gpt-6-luna reasoningEffort=medium
strongest: claudeAgent/claude-opus-5-5 effort=high
how explainer: claudeAgent/claude-fable-5-1 effort=high
swarm race arms: claudeAgent/claude-opus-5-5 effort=high, codex/gpt-6.1-sol reasoningEffort=high
```

The model ids above are examples. Write the ones step 1 detected.

## 6. Confirm

Tell the user where the file is and that it applies from the next fan-out, with no new session needed. Re-running this skill updates it, and they can also edit the file by hand.
