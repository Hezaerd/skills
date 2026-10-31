---
name: hez-help
description: "Guides users through hstack setup, /hstack:hez-mode, and picking the skill, playbook, or principle for a task. Run it with /hstack:hez-help in Claude Code or $hstack:hez-help in Codex."
disable-model-invocation: true
metadata:
  short-description: Find the right hstack skill or playbook
---

# Hez help

Answer the user's question about hstack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and an hstack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use hstack to fix this bug", is not a help question. Read [`hez-mode`](../hez-mode/SKILL.md) and do the work under it.

This file maps questions to the skills that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. The links here point into the installed plugin, which the user may not be able to open, so give the user the file's public copy: `https://github.com/Hezaerd/skills/blob/master/plugins/hstack/` followed by its path.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `/hstack:hez-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make hstack my own

Check the state that changes the answer, and mention it only when it does:

- No hstack model file at the path [harness](../../docs/harness.md#paths) gives means `/hstack:setup-hstack` hasn't run for this user, so every role uses its default model.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `/hstack:create-verification-skill` when the question is about proving a change works.
- No formal verification skill in the project means no property is checked past what tests reach. Mention `/hstack:create-formal-verification-skill` when the question is about a race, an invariant, or another case tests rarely hit. When one exists and the code it covers changed after the commit it records as last in sync, mention `/hstack:maintain-formal-verification-skill` if the question touches that code.

When the model file is missing and it matters, ask whether the user wants to pick a model for each role and a reasoning budget now. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask at most once per chat. If the need is also unclear, ask both questions together. Offer two choices:

- Now: give them `/hstack:setup-hstack` to type, and answer their question too.
- Later: answer their question, and add one line saying every role keeps its default model until they run `/hstack:setup-hstack`.

## Get set up

1. Install from the `hezaerd/skills` marketplace with `claude plugin install hstack@hezaerd` for Claude Code or `codex plugin add hstack@hezaerd` for Codex. T3 Code runs whatever each CLI has installed.
2. Run [`/hstack:setup-hstack`](../setup-hstack/SKILL.md). It asks for a reasoning budget, maps a model to each role, and writes the hstack model file. Skills read it before each fan-out. Then it offers once each to generate a verification skill and a formal verification skill for the project, unless the project already has one.
3. Start a real task with `/hstack:hez-mode`, a goal, and a check that can pass or fail.

Installing changes nothing until the user invokes a skill. Only skills without `disable-model-invocation: true`, such as `/hstack:setup-hstack`, load from the user's words. Offer to word their first prompt with them, per [`references/prompting.md`](references/prompting.md).

If cost is the worry, say where the tokens go and how to spend fewer. hstack spends extra tokens on subagents and review panels. Rerun `/hstack:setup-hstack` and pick a smaller budget or cheaper models. A role set to `inherit-parent` runs on the thread's model, which saves tokens when the thread runs on a cheaper model. A shorter panel list runs fewer subagents, one for each entry. Save `/hstack:hez-mode` for work that needs rigor.

hstack is built for T3 Code running Claude Code or Codex. Its skills use the Agent Skills format, so other tools can read them. But most workflow skills, including `/hstack:hez-mode`, `/hstack:how`, `/hstack:why`, and `/hstack:teach`, spawn workers through T3 Code with per-role models, so those parts may not work there.

## Start a task with `/hstack:hez-mode`

`/hstack:hez-mode` matches the task to a playbook, copies the playbook's steps into the todo list, and runs the other skills as the steps need them. A step it skips stays in the list as `skip: <reason>`. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one.

`/hstack:hez-mode` attaches the skill to one message. It fades as the chat moves on, so start each new task with `/hstack:hez-mode`.

Mid-chat, "new task" makes the mode match a fresh playbook. `/hstack:hez-mode` already uses `hez-agent` for the subagents its playbook steps spawn. To get the same style from a subagent of your own, spawn a `hez-agent` subagent.

## Pick a skill

The default answer is `/hstack:hez-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`/hstack:hez-mode`](../hez-mode/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`/hstack:in-your-own-words`](../in-your-own-words/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before sending it: what a top professional would add, their raw material and methods, and an outside check. It returns the prompt and doesn't do the task | [`/hstack:sharpen`](../sharpen/SKILL.md) |
| Know how code works now, or where new code should live | [`/hstack:how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`/hstack:why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`/hstack:teach`](../teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`/hstack:recall`](../recall/SKILL.md) |
| Catch up on what changed in this chat since their last message, in plain words and small visuals, with every item waiting on them listed and decidable from the reply alone | [`/hstack:ketchup`](../ketchup/SKILL.md) |
| Catch up like `/hstack:ketchup`, in a short subtitled video of slides, with the waiting calls as text under it | [`/hstack:ketchup-video`](../ketchup-video/SKILL.md) |
| Know what a small diff could break outside itself | [`/hstack:blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`/hstack:architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`/hstack:arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers, in separate worktrees | [`/hstack:swarm`](../swarm/SKILL.md) |
| Have different models review a diff and try to break it | [`/hstack:interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`/hstack:tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`/hstack:typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Apply Luau rules to Roblox `.luau` work | [`/hstack:luau-best-practices`](../luau-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`/hstack:no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`/hstack:unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`/hstack:technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`/hstack:bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`/hstack:create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`/hstack:maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`/hstack:create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| Bring a formal verification back in line after the code it covers changed, and learn whether a failure is drift or a bug | [`/hstack:maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| Show a PM or designer what the user sees as a chart checked by a TLA+ model, with the shortest path to each state that breaks a rule | [`/hstack:statechart`](../statechart/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`/hstack:benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`/hstack:figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`/hstack:show-me-your-work`](../show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`/hstack:setup-hstack`](../setup-hstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`/hstack:automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`/hstack:reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`/hstack:correct`](../correct/SKILL.md) |
| Find their way around hstack | `/hstack:hez-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `/hstack:how` explains what the code does. `/hstack:why` explains the reasons. `/hstack:teach` runs one or both and explains the result plainly.
- `/hstack:arena` gives every worker the same brief and merges the best parts. `/hstack:swarm` splits work into slices or a race and returns one report.
- `/hstack:architect` implements right after it settles the design. Add "with checkpoint" to review the design before it writes code.
- `/hstack:interrogate` reviews the diff. `/hstack:blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `/hstack:recall` rebuilds context across recent chats. `/hstack:ketchup` covers only this chat since the user's last message. Resuming one specific chat or branch is the Session pickup playbook.
- `/hstack:figure-it-out` designs one rigorous run. The Orchestrate playbook runs a program that spans days and many PRs. The Autonomous run playbook drives one task to a finish condition.

Not in hstack:

- pstack's code-cleanup and app-control skills from Cursor's team kit don't ship. Skills drive UIs with T3 Code's preview and device tools, and CLIs in a terminal. The [README](https://github.com/Hezaerd/skills#not-shipped-here) lists them.
- `skill-creator` comes with the harness, not with hstack.
- hstack has no `/hstack:orchestrate` skill. Orchestrate is a `/hstack:hez-mode` playbook. If the slash menu shows `/orchestrate`, another plugin provides it.

## Playbooks and principles

Playbooks are step lists inside `/hstack:hez-mode`, not skills, so they have no slash command. Inside `/hstack:hez-mode`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "autopilot, don't merge" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

The Playbooks section of [`hez-mode`](../hez-mode/SKILL.md) lists every playbook and when it applies.

hstack has no planning skill. T3 Code's plan mode works alongside it. For work that spans phases or stacked PRs, asking `/hstack:hez-mode` for a plan runs the [Multi-phase plan playbook](../hez-mode/playbooks/multi-phase-plan.md), which writes the plan and doesn't implement it. For a design question, the Prototype playbook or `/hstack:architect` settles it in code first.

Principles are one-rule skills that `/hstack:hez-mode` reads and cites in its replies. The user rarely invokes one. They steer with the names instead, as in "apply prove it works. show me the real output." Typing `/hstack:principle-<name>` still loads one on demand. The Principles section of [`hez-mode`](../hez-mode/SKILL.md) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying after a few turns | It was attached to one message and faded. Start each task with `/hstack:hez-mode`. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | Skills read the hstack model file before each fan-out. Check the file at this harness's path ([harness](../../docs/harness.md#paths)), and check that T3 Code lists the model. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | Only skills without `disable-model-invocation: true` load from the user's words. The others load when the user types them or when `/hstack:hez-mode` runs them, and it doesn't run every skill. |
| Parallel agents overwrote each other | Give each writing agent its own worktree. |
| An overnight run moved but finished nothing | Its timed rechecks need a check that can pass or fail, not a duration. |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers.

## Make hstack my own

- [`/hstack:automate-me`](../automate-me/SKILL.md) drafts a personal mode skill from the user's own history, which runs `/hstack:hez-mode` underneath.
- [`/hstack:reflect`](../reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `/hstack:hez-mode write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
