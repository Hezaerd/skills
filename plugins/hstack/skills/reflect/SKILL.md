---
name: reflect
description: "Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect. Run it with /hstack:reflect in Claude Code or $hstack:reflect in Codex."
disable-model-invocation: true
metadata:
  short-description: Route session learnings into skill edits
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "/hstack:reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Before fanning out, find this conversation's transcript. This conversation is this T3 thread, whose id is `parentThreadId` from `orchestrator_capabilities`. Read its opening user prompt with `t3_thread_read`. Reviewers need the exact tool calls and arguments the thread view summarizes, so also find the harness transcript in this workspace's transcript folder, at the path [harness](../../docs/harness.md#transcripts) gives. Do not read other projects' threads or transcript folders. That crosses workspace boundaries and reads private chats from unrelated projects.

List the ten newest `.jsonl` files in that folder. For each candidate, read its first user message. Take the file whose first user message contains the conversation's opening user prompt. If none matches, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

One message, three general-purpose subagents in the shared checkout, spawned per [delegation](../../docs/delegation.md). Reviewers need MCP access to look up the tickets, chat threads, and observability traces the transcript references, and `Explore` drops MCP servers, so don't use it.

Each reviewer and the synthesizer name a role line in the [model file](../../docs/delegation.md#pick-the-models) and a default. Read those lines from the model file before the first spawn. A missing line uses its default. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **hez-mode** skill.

| Lens | Role line | Default model | Prompt template |
|---|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `claudeAgent/claude-opus-5-5 effort=xhigh` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `claudeAgent/claude-opus-5-5 effort=xhigh` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings as their result.

## 3. Synthesize

One general-purpose subagent in the shared checkout, on the `reflect judgment, divergent, synthesizer` line (default `claudeAgent/claude-opus-5-5 effort=xhigh`). It spot-verifies citations through MCP, and `Explore` drops MCP servers, so don't use it. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

File each Backlog item to your team's devex or backlog tracker without waiting. Only the Accepted list waits for approval.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the `skill-creator` skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `skill-creator` and run its description-optimization loop.
- `new skill via skill-creator: <kebab-name>`: hand creation to `skill-creator`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
