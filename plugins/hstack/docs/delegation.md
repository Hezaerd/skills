# Delegation

How hstack skills start workers. The skill decides what each worker does, whether it may write, and which model class it needs. This file decides how to start it. Read it once per session, before the first spawn.

## Detect T3 Code

T3 Code is present when the session has tools from the `t3-code` MCP server. Their names may carry a prefix such as `mcp__t3-code__`. In Claude Code, search deferred tools with `ToolSearch` for `t3-code` before you decide it is absent. In Codex, make one direct call to `orchestrator_capabilities` before you decide.

Without T3 Code, use only native subagents and inline work:

- run every worker on the parent provider, and say so when the user asked for another provider's model;
- give a writing worker its own worktree when the native tool supports it (Claude Code: `isolation: "worktree"` on `Agent`); otherwise run writing workers one after another in the shared checkout;
- skip the T3-only steps below (`task_status`, pending requests, `task_cancel`).

## Pick the models

Each spawn has a role from the table below. Resolve its model in this order, taking the first that applies:

1. a model the user names for this run, including one from another provider;
2. the role's line in `~/.hstack/models.md`;
3. the line for the role's class (`fast` or `strongest`) in that file;
4. the default: the parent model, at `medium` effort for `fast` and `high` for `strongest`.

Read `~/.hstack/models.md` fresh before each fan-out, so edits apply without a new session. If it doesn't exist, use the defaults. `/hstack:setup-hstack` writes it.

| Role | Class |
| --- | --- |
| `how explorers` | fast |
| `how explainer` | strongest |
| `why investigators` | fast |
| `why synthesizer` | strongest |
| `swarm workers` | per slice: fast for mechanical slices, strongest for judgment-heavy ones |
| `swarm race arms` | strongest; a list, one arm per entry |

A role without its own line takes its class line. `swarm workers` has no class line: without its own line, swarm picks the class per slice.

### Values

Each value is one of:

- `<providerInstanceId>/<model> <option>=<value> ...`, such as `codex/gpt-6-luna reasoningEffort=medium serviceTier=priority` or `claudeAgent/claude-opus-5-5 effort=high`. The ids and option values are the ones `orchestrator_capabilities` lists.
- `inherit-parent`, optionally followed by `effort=<level>`: the parent model, with `<level>` set on the parent provider's reasoning option.
- `fast` or `strongest`: whatever that class line resolves to.
- For `swarm race arms`, a comma-separated list of the above.

### Turning a value into a spawn

- With T3 Code: call `orchestrator_capabilities` and check the value against it. Use only providers with `canRunChildTask: true`. If the model or an option value is missing, use the closest listed model of the same family, or the closest listed value, and say so. A model on another provider, or one the native tool can't select, goes through `delegate_task` with `target` set to the provider, model, and options.
- A model on the parent's provider can run as a native subagent. Claude Code's `Agent` takes `model` (`opus`, `sonnet`, `haiku`, `fable`: the family in the model id) and `effort` (the `effort` option). Codex spawns on the session model; when the value names a different Codex model, use `delegate_task` if T3 Code is present, otherwise the session model.
- Without T3 Code, a value on another provider runs on the parent model at the same effort level instead. Say so in your reply.

## Pick the transport

Use the lightest transport that can run the worker.

- **Native subagent.** Same provider as the parent, a model the native tool accepts, and no write collision with a sibling.
  - Claude Code: `Agent` with `subagent_type: "general-purpose"`. Agents run in the background and wake you when they finish. For read-only search with no MCP needs, `"Explore"` is cheaper. It still has `Bash`, so the brief says "do not edit files". `Explore` drops MCP servers, so a worker that needs them uses `"general-purpose"`.
  - Codex: spawn a subagent and put any read-only rule in its brief.
- **T3 delegated task.** Call `delegate_task` with `mode: "async"`, a `title` naming the worker, a `role` (`research`, `review`, `test`, `implementation`, or `general`), and a `target` of `providerInstanceId`, `model`, and `options` from the model step. Use it when any of these hold:
  - the worker runs on another provider (Claude parent with Codex workers, or the reverse), or on a model the native tool can't select;
  - the worker writes code that could collide with a sibling, so it needs `isolation: "worktree"`;
  - the run is long and the user should be able to watch or steer each worker as its own child thread in T3.

  Give every call a distinct `clientRequestId` that stays the same across retries, such as `<skill>-<slug>-<worker>-r1`, so a retry doesn't spawn a duplicate. Leave `runtimeMode` unset unless the user asks for supervised workers; a narrower mode stalls the child on approvals nobody can give. State limits such as "read-only" in the brief. A child runs with its own provider's MCP configuration, so a worker that needs a specific MCP server goes to a provider that has it, or stays native.
- **Inline.** If you can't spawn workers (you are already a subagent, or no tool is available), do each worker's job yourself in order and say the work ran serially.

Never use `t3_thread_launch` or `create_threads` for workers. Those create top-level conversations, not children of this thread. Use them only when the user asks for separate threads.

Every brief stands alone. Neither native agents nor delegated tasks see this conversation, so each brief carries the goal, repo path, base SHA, scope, permissions, and what to report. A worktree starts from the parent's local `HEAD` commit, without uncommitted edits.

## Drain

Spawn independent workers in one message so they start together, then end the turn. Native background agents and async delegated tasks both wake this thread when they finish. Don't poll and don't start watchers. Call `task_status` only when you need a delegated result mid-turn.

- When a wake-up or `task_status` shows `hasPendingQuestion`, read it with `t3_pending_request_list` and `t3_pending_request_read`, passing the worker's `childThreadId` as `threadId`. Answer with `t3_pending_request_respond` when the brief already settles it; otherwise ask the user.
- If a worker fails, hangs, or drops out, `task_cancel` it if it is still running, and say so in the result.
- To redo a worker, start a new spawn or `delegate_task` call whose brief repeats the original and adds what changed, under a new `clientRequestId` (`-r2`). Never continue a worker by sending to its `childThreadId`.

Read a delegated task's result from its `summary`, and a native agent's from its final message.
