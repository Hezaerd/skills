# Delegation

How hstack skills start workers in T3 Code. A skill names each worker's role, its job, whether it writes, and whether it needs its own worktree. This file turns that into a model and a spawn. Read it once per session, before the first spawn. The **hez-mode** skill's Subagents section sets the policy: which agent, fresh or continued, and how to tune effort and speed for the job.

## Pick the models

Read the hstack model file fresh before each fan-out, so edits apply without a new session: `~/.claude/rules/hstack-models.mdc` in Claude Code, `~/.agents/rules/hstack-models.mdc` in Codex. `/hstack:setup-hstack` writes both. Neither harness loads the file on its own.

Each line is `<role>: <value>`. Resolve a role's model in this order, taking the first that applies:

1. a model the user names for this run;
2. the role's line in the model file;
3. the default the skill names for the role.

A value is one of:

- `<providerInstanceId>/<model> <option>=<value> ...`, such as `codex/gpt-6.1-sol reasoningEffort=xhigh` or `claudeAgent/claude-opus-5-5 effort=xhigh`. The ids and option values are the ones `orchestrator_capabilities` lists.
- `inherit-parent`: the parent thread's model (`inheritedProviderInstanceId` and `inheritedModel`).
- For a panel role (`arena runners`, `arena cross-judge pool`, `architect runners`, `interrogate reviewers`), a comma-separated list of the above. One worker runs per entry, `inherit-parent` entries included, so the list length sets the count.

The effort option is `effort` on Claude models and `reasoningEffort` on Codex models, on the ladder `low` < `medium` < `high` < `xhigh` < `max`. Fast speed is `serviceTier=priority` on Codex models and `fastMode=true` on Claude models that list it. Standard speed drops that option. A provider is a model family: a panel stays diverse when its entries span providers.

Call `orchestrator_capabilities` once per session and check each value against it. Use only providers with `canRunChildTask: true`. If the model or an option value isn't listed, use the closest listed model of the same provider or the closest listed value, and say so.

## Pick the transport

Use the lightest transport that can run the worker.

- **Native subagent.** The value is on the parent's provider, the native tool can set every option, the worker spawns no workers of its own, and it can't collide with a sibling's writes.
  - Claude Code: `Agent` takes `model` (`opus`, `sonnet`, `haiku`, `fable`: the family in the model id) and `effort` (ladder values only). A value with `fastMode` or an effort off the ladder goes through `delegate_task`. Use `subagent_type: "general-purpose"` by default, `"hstack:hez-agent"` or `"hstack:comment-sicko"` when the skill names that agent, and `"Explore"` for a read-only search that needs no MCP server. `Explore` keeps `Bash`, so the brief still says "do not edit files".
  - Codex: native subagents run on the session model. A value naming another Codex model goes through `delegate_task`. Name the `hez-agent` or `comment-sicko` custom agent when the skill names one.
- **Delegated task.** Everything else: another provider, a model or option the native tool can't set, a writer that needs its own checkout, a worker that spawns its own workers (native subagents can't), or a long run the user should watch as its own child thread. Call `delegate_task` with:
  - `mode: "async"`, a `title` naming the worker, and a `role` (`implementation`, `research`, `review`, `design`, `test`, or `general`);
  - `target` with `providerInstanceId`, `model`, and `options` from the value;
  - `isolation: "worktree"` for a writer that could collide with a sibling, omitted for the shared checkout;
  - a `clientRequestId` that stays the same across retries of that spawn, such as `<skill>-<slug>-<worker>-r1`.

  Leave `runtimeMode` unset; a narrower mode stalls the child on approvals nobody can give. State read-only limits in the brief. A child runs with its own provider's MCP configuration, so a worker that needs an MCP server only the parent's provider has stays on the parent's provider. A delegated task has no agent type: for a `hez-agent` worker, the brief's first line tells it to read the hez-mode `SKILL.md` at its absolute path in full before any work.

Never use `t3_thread_launch` or `create_threads` for workers. Those make top-level threads, not children of this one. Use them only when the user asks for separate threads.

Every brief stands alone. Neither native subagents nor delegated tasks see this conversation, so each brief carries the goal, repo path, base branch and SHA, scope, permissions, and what to report. A worktree starts from the parent's local `HEAD` commit without uncommitted edits. Name the base SHA, and ask the user before committing their uncommitted changes for a worker. A worker that must start from another branch checks it out in its worktree as its first step.

## Drain

Spawn independent workers in one message so they start together, then end the turn. Native subagents and async delegated tasks both wake this thread when they finish. Don't poll and don't start watchers. Call `task_status` only when you need a delegated result mid-turn.

- When a wake-up or `task_status` shows `hasPendingQuestion`, read it with `t3_pending_request_list` and `t3_pending_request_read`, passing the worker's `childThreadId` as `threadId`. Answer with `t3_pending_request_respond` when the brief already settles it. Otherwise ask the user.
- If a worker fails, hangs, or drops out, `task_cancel` it if it is still running, and say so in the result.
- New work goes to a fresh spawn whose brief carries the original brief, every later directive, and the prior worker's report and branch, under a new `clientRequestId` (`-r2`). Never continue a delegated task by sending to its `childThreadId`. Continue a native subagent (`SendMessage` in Claude Code) only in the cases hez-mode's Subagents section allows.

Read a delegated task's result from its `summary`, and a native subagent's from its final message.
