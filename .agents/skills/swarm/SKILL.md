---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration. Runs workers as native subagents or T3 Code delegated tasks, across providers and in isolated worktrees when needed. Run it with /swarm in Claude Code or $swarm in Codex."
disable-model-invocation: true
metadata:
  short-description: Fan out parallel workers and merge one report
---

# Swarm

## Start

Open a todolist with one entry per phase before launching anything. Add one entry per worker when you spawn it, holding its id (`taskId` or agent id).

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning. Keep N at 8 or fewer unless the user asks for more.
3. Pick the transport per worker. See [Transport](#transport).
4. Pick the models. Call `orchestrator_capabilities` from the `t3-code` MCP server (the name may carry a prefix such as `mcp__t3-code__`). Use only providers with `canRunChildTask: true`, and copy model ids and option values exactly as listed. Models the user names win. Otherwise run workers on the parent provider and model, at low or medium effort for mechanical slices and high for judgment-heavy ones. Save fast or priority tiers for races where wall-clock matters. For a model race, name each arm's provider, model, and options up front, and prefer arms from different providers. If a requested model is missing, use the closest listed model of the same family and say so.
5. Give each worker its own writable output when it writes: a distinct file, directory, or worktree. Workers that edit overlapping files each get `isolation: "worktree"`. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.
6. Worktrees start from the parent's local `HEAD` commit. Uncommitted edits are not copied. If workers need uncommitted changes, ask the user before committing them; otherwise name the base SHA in each brief.

## Transport

Pick the lightest transport that can run the worker.

- **Native subagent.** For same-provider workers on a model the native tool accepts, sharing the parent checkout. In Claude Code, use the `Agent` tool with `subagent_type: "general-purpose"` and `run_in_background: true`, or `"Explore"` for read-only search slices. In Codex, spawn a subagent.
- **T3 delegated task.** Call `delegate_task` with `mode: "async"`, a `title` naming the slice or arm, a `role` (`research`, `review`, `test`, `implementation`, or `general`), and a `target` of `providerInstanceId`, `model`, and `options` from step 4. Use it when any of these hold:
  - the worker runs on another provider (Claude parent with Codex workers, or the reverse), or on a model the native tool can't select;
  - the worker writes code that could collide with a sibling, so it needs `isolation: "worktree"`;
  - the run is long and the user should be able to watch or steer each worker as its own child thread in T3.

  Give every call a distinct, stable `clientRequestId` such as `swarm-<slug>-<slice>-r1` so a retry doesn't spawn a duplicate. Leave `runtimeMode` unset unless the user asks for supervised workers; a narrower mode stalls the child on approvals nobody in this thread can give. To limit what a worker may do, say so in the brief.
- **Inline.** If you can't spawn workers (for example, you are already a subagent, or no tool is available), run each slice yourself in sequence and say the swarm ran serially.

Never use `t3_thread_launch` or `create_threads` for workers. Those create top-level conversations, while the swarm owns its workers as children. Use them only when the user asks for separate threads.

## Phase B: Fan out

Spawn all N workers in one message so they start together. Build every brief from `references/worker-brief.md`. Every brief stands alone: delegated tasks don't see this conversation. Include the goal, repo path, base SHA, scope, exact slice or race arm, writable output, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first. A worktree worker that writes code commits in its worktree and reports the branch and SHA.

Then end the turn. Native background agents and async delegated tasks both wake this thread when they finish. Don't poll and don't start watchers. Call `task_status` only when you need a result mid-turn.

While draining:

- When a wake-up or `task_status` shows `hasPendingQuestion`, read it with `t3_pending_request_list` and `t3_pending_request_read`, passing the worker's `childThreadId` as `threadId`. Answer with `t3_pending_request_respond` when the brief already settles it; otherwise ask the user.
- For a `first pass` race, `task_cancel` the remaining arms once one passes and you have confirmed it.
- If a worker fails, hangs, or drops out, `task_cancel` it if it is still running, proceed with N-1, and note it.

## Phase C: Aggregate

Read the terminal results: the delegated task's `summary`, or the native agent's final message. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. The respawn is a new `delegate_task` call (or native spawn) whose brief repeats the original and names what was missing, under a new `clientRequestId` ending `-r2`. Never continue a worker by sending to its `childThreadId`. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front: first pass, rank all, or best-of. Check a winning worktree result yourself (diff, tests) before you name it. Do not paste raw worker dumps.

Don't merge worktree branches into the user's branch unless the done predicate says to. Report the winning branch and SHA so the user can pick it up.

## Phase D: Report

Return one consolidated in-chat report:

- a table with one row per worker: slice or arm, provider and model, transport, status (`PASS`, `ISSUES`, `BLOCKED`, gap, or dropout), and the evidence or branch@SHA;
- one-liners for each issue, deduplicated across workers;
- gaps and dropouts with their reason;
- the race rule and the winner, when used.

When the table is wide or the results compare better visually, also publish it with `html_render`.
