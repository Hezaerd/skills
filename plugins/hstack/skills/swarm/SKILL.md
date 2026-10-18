---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for 'swarm this' or parallel coverage, races, gauntlets, and exploration. Runs workers as native subagents or T3 Code delegated tasks, across providers and in isolated worktrees when needed. Run it with /hstack:swarm in Claude Code or $hstack:swarm in Codex."
disable-model-invocation: true
metadata:
  short-description: Fan out parallel workers and merge one report
---

# Swarm

Read [delegation](../../docs/delegation.md) once per session before you follow this skill. It covers detecting T3 Code, picking models, picking a transport, and draining workers. If the file is missing, use native subagents on the parent provider.

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
4. Pick the models per [delegation](../../docs/delegation.md#pick-the-models). Use the fast class at low or medium effort for mechanical slices and the strongest class for judgment-heavy ones. Save fast or priority service tiers for races where wall-clock matters. For a model race, name each arm's provider, model, and options up front, and prefer arms from different providers. Without T3 Code, a cross-provider race can't run; say so and race models of the parent provider instead.
5. Give each worker its own writable output when it writes: a distinct file, directory, or worktree. Workers that edit overlapping files each get `isolation: "worktree"`. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.
6. Worktrees start from the parent's local `HEAD` commit. Uncommitted edits are not copied. If workers need uncommitted changes, ask the user before committing them; otherwise name the base SHA in each brief.

## Transport

Pick each worker's transport per [delegation](../../docs/delegation.md#pick-the-transport). Name delegated tasks after the slice or arm, with `clientRequestId` values like `swarm-<slug>-<slice>-r1`.

## Phase B: Fan out

Spawn all N workers in one message so they start together. Build every brief from `references/worker-brief.md`. Every brief stands alone. Include the goal, repo path, base SHA, scope, exact slice or race arm, writable output, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first. A worktree worker that writes code commits in its worktree and reports the branch and SHA.

Then end the turn and drain per [delegation](../../docs/delegation.md#drain). Also:

- For a `first pass` race, `task_cancel` the remaining arms once one passes and you have confirmed it.
- When a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. Respawn per [delegation](../../docs/delegation.md#drain), naming what was missing. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front: first pass, rank all, or best-of. Check a winning worktree result yourself (diff, tests) before you name it. Do not paste raw worker dumps.

Don't merge worktree branches into the user's branch unless the done predicate says to. Report the winning branch and SHA so the user can pick it up.

## Phase D: Report

Return one consolidated in-chat report:

- a table with one row per worker: slice or arm, provider and model, transport, status (`PASS`, `ISSUES`, `BLOCKED`, gap, or dropout), and the evidence or branch@SHA;
- one-liners for each issue, deduplicated across workers;
- gaps and dropouts with their reason;
- the race rule and the winner, when used.

When the table is wide or the results compare better visually, also publish it with `html_render`.
