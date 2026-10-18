---
name: automate-me
description: "Use for \"automate me\", \"create/update/refresh my -mode skill\", \"turn/capture my preferences or working style into a skill\", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill via skill-creator + unslop, optionally pulling fresh evidence from recent T3 threads. Run it with /hstack:automate-me in Claude Code or $hstack:automate-me in Codex."
disable-model-invocation: true
metadata:
  short-description: Turn your working style into a mode skill
---

# Automate me

A guided flow for turning the user's working conventions into a skill agents will follow. The output is one `-mode` skill tailored to them (e.g. `jay-mode`, `priya-mode`).

This skill orchestrates three others: an inline mining pass (see step 1), the `skill-creator` skill (authoring), and the **unslop** skill (prose discipline). It sequences them. It doesn't replace them.

## Flow

### 0. Check for an existing skill

Look recursively for `*-mode/SKILL.md` matching the user's handle in every project and user skills folder [harness](../../docs/harness.md#paths) lists. Mode skills can live in a personal category directory (`<handle>/` inside a skills folder), not only at the top level. If one exists, confirm intent by asking the user (unless they already said "update my skill" or similar):

- Update the existing skill (default for repeat runs)
- Start fresh (rare, ask why before doing it)

Update mode changes the rest of the flow:
- Step 1 mines only history since the skill was last edited (`git log -1 --format=%cI <path>`, or the file's modification time outside a repo).
- Step 2 asks what's changed or missing, not what to capture from zero.
- Step 4 edits the existing file in place. Preserve sections the user hasn't contradicted. Revise ones with new evidence. Add new sections only for genuinely new rules.

### 1. Mine their history

Locate the active workspace's history before fanning out. Past sessions in this project are T3 threads. List them with `t3_thread_list`, narrow them with `t3_thread_search`, and read each with `t3_thread_read`. Use only this project's threads. Don't search other projects' threads or glob across other projects' transcript folders. That crosses workspace boundaries and reads private chats from unrelated projects. When a signal hinges on exact tool calls or arguments that the thread view summarizes, read the harness transcript at the path [harness](../../docs/harness.md#paths) gives, inside this workspace's transcript folder only.

Survey recent agent conversations within that scope for recurring patterns. Run multiple parallel subagents across slices of history (e.g. last 2-4 weeks, split into 3 slices so each has enough material). Each miner is a read-only general-purpose subagent in the shared checkout that needs the `t3-code` tools. Its brief says do not edit files, commit, or change external state. Spawn them per [delegation](../../docs/delegation.md). Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **hez-mode** skill. Each slice mining subagent reads the threads the parent lists for its slice, looks for the signals below, and returns a short structured list of patterns it saw with evidence pointers. Default signals worth hunting:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (subagents, models, specialized workflows, parallelism)
- Verification posture (what "done" means, unit tests vs live repro, reviewers)
- Code and prose discipline (style, principles cited, lint/format tools)
- Process conventions (worktrees, commits, PRs, review/merge tooling)
- Meta preferences (fixing skills mid-task, proposing new ones)

Cross-check across slices before elevating a signal. Patterns seen in 2+ slices are high-confidence. Lone signals are weak and usually get dropped.

### 2. Ask the user directly

Mining misses intent that hasn't come up yet. Ask the user with structured multi-choice questions ([harness](../../docs/harness.md#tools) maps the tool) rather than asking the user to type from scratch.

Shape: one or two questions with 4-6 options each, with multiple answers allowed for category questions. Start broad ("Which areas matter most?"), then follow up on selected areas with specific options. After the structured rounds, one free-form chat question catches anything the options missed.

Don't dump 20 questions.

### 3. Cluster findings

Group the combined signals into sections. Common ones (use only what applies):

- **Response style**: length, tone, format.
- **Autonomy**: how much to do without asking, MCP tool use.
- **Understand first**: which skills to reach for when scoping or investigating a change.
- **Subagents**: default, parallelism, model-to-task, specialized workflows.
- **Prose / code discipline**: principles, lint tools, style guides.
- **Review and verify**: repro posture, verification skills, live-testing tools.
- **Process**: git worktrees, commits, PRs, review/merge tooling.
- **Skills**: skill-authoring habits, fix-the-skill-first, proposing new skills.

The **hez-mode** skill shows the shape. Read it for granularity. Don't copy its content. The user's rules are not the same as hez-mode's.

### 4. Draft the skill

Use the `skill-creator` skill to author the skill. Placement:

- Path: preserve an existing mode skill's location and category. For a new mode, default to `<handle>-mode/SKILL.md` in the user skills folder ([harness](../../docs/harness.md#paths)), or `<handle>/<handle>-mode/SKILL.md` when that folder has an established personal category for that handle. Use the project skills folder instead only if the user wants the mode in the repo.
- Codex metadata: write `agents/openai.yaml` next to the new `SKILL.md`, in the shape [harness](../../docs/harness.md#paths) gives.
- Handle: the user's first name or chosen identifier.
- Routing: the mode skill runs on top of hstack. It tells the agent to run the `hstack:hez-mode` skill for the work and states only where the user's rules differ. It names other hstack skills as `hstack:<name>`.
- Frontmatter `description`: trigger on their name + `/<handle>-mode` (`$<handle>-mode` in Codex) + "work in their style", not on generic keywords like "write code" or "review PR".
- Frontmatter formatting: follow `skill-creator`'s YAML rules. Keep `description` as one YAML scalar. Quote it or use `description: >-` with indented continuation lines when punctuation or wrapping requires it.
- Frontmatter `disable-model-invocation: true` by default. Opt out only if the user explicitly wants their mode to apply on every turn.

### 5. Iterate on prose

Apply the **unslop** skill and `skill-creator`'s writing guidelines to every line.

Show the draft to the user and take feedback. Expect multiple iterations. Cut ruthlessly. A mode skill is not a manual.

### 6. Land it

If the skill lives in a git repo, work in a worktree off main. Commit and open a PR. Don't push to main directly. Otherwise write it in place.

## Guardrails

- **Don't overfit to one conversation.** A preference stated once and contradicted another time is noise. Require multiple instances before codifying it.
- **Don't be clever.** Restating other skills' contents, inventing metaphors, or writing "poetic" prose for an agent reader is cost without benefit. Keep it operational.
- **Reference, don't inline.** Other skills the user relies on should appear as path references, not pasted excerpts. Same for any principle docs they maintain elsewhere.
- **Keep sections minimal.** Only add a section if the user has a specific, non-default rule there. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." is.
- **Name conventions generic.** Use "the user" or "the human" in imperatives, not the author's first name.
- **Don't force symmetry.** If a user has no process rules worth writing down, skip the Process section entirely.

## Evaluation

A `-mode` skill is subjective output. A `skill-creator`-style test/iterate benchmark loop isn't useful here. Vibe-check with the user: does it read like them? Did it miss anything? Then ship.

Run a description-optimization loop only if the skill's trigger accuracy turns out to be a problem in practice.

## When not to use

- User wants a task-specific skill (not working conventions): `skill-creator` alone, no mining required.
- User wants to capture one narrow workflow (e.g. "how I write commit messages"). That's a regular skill, not a mode skill.
