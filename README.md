# hstack

hstack is a port of [pstack](https://github.com/cursor/plugins/tree/main/pstack), the cursor plugin by [Lauren Tan](https://github.com/poteto), for t3 code. it runs the same skills, playbooks, and principles on claude code or codex inside t3 code. this repo is a plugin marketplace for both.

there's a growing sense that ai writes too much slop code. i agree. i don't want to ship like a team of twenty slop artists. throughput without quality is not a goal i aspire to. if you want to go fast, go deep first.

**pstack is Lauren's answer, and hstack brings it to t3 code.** these are the skills she uses every day to ship high quality code at Cursor, rewired for claude code and codex. this turns your agent into a real engineering team. the goal is not to maximize loc, in fact it's the opposite. hstack helps you write less, but higher quality code.

**hstack gives you fearless parallelism.** when you can go deep on one agent and trust it to write good, verifiable code, you can truly parallelize with confidence. start multiple agents up with `hez-mode` and trust that they'll apply rigorous engineering principles to their work.

**t3 code gives you the best of all worlds.** every frontier model has its strengths and weaknesses. t3 code runs claude and codex models side by side, and many hstack skills use multi-model workflows to take advantage of each model's unique strengths.

fork it. improve it. make it yours. PRs are welcome!

## install

hstack runs inside t3 code. t3 code runs the claude code and codex CLIs, so it picks up whatever they have installed.

claude code:

```bash
claude plugin marketplace add hezaerd/skills
claude plugin install hstack@hezaerd
```

codex:

```bash
codex plugin marketplace add hezaerd/skills
codex plugin add hstack@hezaerd
```

pin a release in codex with `--ref hstack--v<version>`.

skills are namespaced by the plugin. call `/hstack:hez-mode` in claude code and `$hstack:hez-mode` in codex. this readme writes the claude code form. claude code names the agents `hstack:hez-agent` and `hstack:comment-sicko`.

[`/hstack:setup-hstack`](./plugins/hstack/skills/setup-hstack/SKILL.md) writes your model choices to the hstack model file, `~/.claude/rules/hstack-models.mdc` for claude code and `~/.agents/rules/hstack-models.mdc` for codex. neither harness loads the file on its own. skills read it fresh before each fan-out. [`docs/harness.md`](./plugins/hstack/docs/harness.md) maps every other name to each harness, and [`docs/delegation.md`](./plugins/hstack/docs/delegation.md) covers how skills pick models and spawn workers.

### update

```bash
claude plugin marketplace update hezaerd && claude plugin update hstack@hezaerd
codex plugin marketplace upgrade hezaerd && codex plugin add hstack@hezaerd
```

### codex agents

codex plugins don't ship subagents yet, so copy `hez-agent` and `comment-sicko` into `~/.codex/agents/` (or `$CODEX_HOME/agents/`, or `.codex/agents/` in a project):

```bash
mkdir -p ~/.codex/agents
curl -fsSL https://raw.githubusercontent.com/Hezaerd/skills/master/plugins/hstack/codex/agents/hez-agent.toml -o ~/.codex/agents/hez-agent.toml
curl -fsSL https://raw.githubusercontent.com/Hezaerd/skills/master/plugins/hstack/codex/agents/comment-sicko.toml -o ~/.codex/agents/comment-sicko.toml
```

copy them again after updating. then "spawn the comment-sicko agent on this diff" in codex.

## get started

two steps:

1. run [`/hstack:setup-hstack`](./plugins/hstack/skills/setup-hstack/SKILL.md), pick a reasoning budget, and choose which models you want.
2. use [`/hstack:hez-mode`](./plugins/hstack/skills/hez-mode/SKILL.md) whenever you're doing anything that requires rigor.

new here, stuck, or unsure which skill fits? ask [`/hstack:hez-help`](./plugins/hstack/skills/hez-help/SKILL.md).

that's it. the other skills are situational, and the mode skill uses them for you as needed. out of the box the mode splits work by model strength. code delegates (feature, refactoring, bug fix, perf, hillclimb) go to `codex/gpt-6.1-sol reasoningEffort=xhigh serviceTier=priority`, while the hardest changes, prose, and judgment go to `claudeAgent/claude-opus-5-5 effort=xhigh`. the default panel is opus 5.5 / gpt-6.1-sol. [`/hstack:setup-hstack`](./plugins/hstack/skills/setup-hstack/SKILL.md) changes any of it.

## usage

use [`/hstack:hez-mode`](./plugins/hstack/skills/hez-mode/SKILL.md) at the start of a task. it reads your request, picks from a set of playbooks, and runs the other skills as the steps need them.

type `/hstack:hez-mode` at the start of the message, before your task, so the harness loads the skill with it.

### just use [`/hstack:hez-mode`](./plugins/hstack/skills/hez-mode/SKILL.md)

this skill is the main shortcut. i use it whenever i need the agent to do rigorous engineering work. it comes with twenty-three playbooks:

```
/hstack:hez-mode this pr has a subtle bug where the scroll drifts every 750ms even when idle.
repro first, then fix and verify.
```

```
/hstack:hez-mode i'm going to bed. land the stack even if ci flakes. i want everything merged
by morning.
```

<details>
<summary>the twenty-three playbooks</summary>

| playbook | for |
|---|---|
| [investigation](./plugins/hstack/skills/hez-mode/playbooks/investigation.md) | a read-only question. how does x work, why was y built this way, are we sure. |
| [bug fix](./plugins/hstack/skills/hez-mode/playbooks/bug-fix.md) | reproduce a defect, root-cause it, and fix with runtime evidence. |
| [perf](./plugins/hstack/skills/hez-mode/playbooks/perf-issue.md) | trace a measured slowness and improve it against a baseline. |
| [hillclimb](./plugins/hstack/skills/hez-mode/playbooks/hillclimb.md) | sustained, scientific improvement of one metric against a target, looping hypotheses with before/after measurement and one commit per accepted win. |
| [runtime forensics](./plugins/hstack/skills/hez-mode/playbooks/runtime-forensics.md) | diagnose a live symptom (leak, idle-cpu spin, glitch) from instrumentation. |
| [trace forensics](./plugins/hstack/skills/hez-mode/playbooks/trace-forensics.md) | diagnose a captured profiling artifact (cpuprofile, trace, spindump, heap snapshot). |
| [feature](./plugins/hstack/skills/hez-mode/playbooks/feature.md) | new or changed behavior, built from a named data shape. |
| [refactoring](./plugins/hstack/skills/hez-mode/playbooks/refactoring.md) | a behavior-preserving change to structure or shape. |
| [prototype](./plugins/hstack/skills/hez-mode/playbooks/prototype.md) | a throwaway sketch to make a design or behavioral decision cheaply, or to settle an empirical fork by observing it. |
| [visual parity](./plugins/hstack/skills/hez-mode/playbooks/visual-parity.md) | pixel-exact ui equivalence between two implementations. |
| [authoring a skill](./plugins/hstack/skills/hez-mode/playbooks/authoring-a-skill.md) | writing or editing a SKILL.md. |
| [eval](./plugins/hstack/skills/hez-mode/playbooks/eval.md) | test how a skill or prompt change affects agent behavior, blinded. |
| [babysit](./plugins/hstack/skills/hez-mode/playbooks/babysit.md) | drive a pr or a stack to merge-ready: conflicts, review threads, ci. |
| [shipping](./plugins/hstack/skills/hez-mode/playbooks/shipping.md) | independently verify a green stack, then land the contiguous verified run bottom-up through github. |
| [autonomous run](./plugins/hstack/skills/hez-mode/playbooks/autonomous-run.md) | drive a long task to completion without stopping. |
| [orchestrate](./plugins/hstack/skills/hez-mode/playbooks/orchestrate.md) | a standing project handed to one coordinator chat: multi-day, many stacked prs, fleets of subagents. |
| [autopilot-full](./plugins/hstack/skills/hez-mode/playbooks/autopilot-full.md) | run independent prs to merged with one owner per pr. a swarm verifies each code-ready head, and every later change to the patch gets a fresh check. |
| [autopilot-stack](./plugins/hstack/skills/hez-mode/playbooks/autopilot-stack.md) | build and verify one linear base-branch stack for the operator to review and land. |
| [session pickup](./plugins/hstack/skills/hez-mode/playbooks/session-pickup.md) | resume or take over a prior agent's in-flight work. |
| [pause safely](./plugins/hstack/skills/hez-mode/playbooks/pause-safely.md) | suspend in-flight work cleanly so it can be resumed later. |
| [multi-phase plan](./plugins/hstack/skills/hez-mode/playbooks/multi-phase-plan.md) | work that spans phases or stacked PRs. |
| [worktree cleanup](./plugins/hstack/skills/hez-mode/playbooks/worktree-cleanup.md) | reclaim disk by pruning merged or abandoned worktrees and stale ios simulators, safety-gated. |
| [opening a pr](./plugins/hstack/skills/hez-mode/playbooks/opening-a-pr.md) | open a ready pr from small ordered commits with a conventional commits title and a briefing-style body. invoked at the end of every other playbook. |

</details>



when invoked it:

1. matches your task to a [playbook](./plugins/hstack/skills/hez-mode/playbooks/) and opens a todo list whose first items are its steps, copied in verbatim.
2. routes to the other skills as the steps fire.
3. writes unslopped replies framed for the consumer and the maintainer.

the full rules and playbooks live in [`skills/hez-mode/SKILL.md`](./plugins/hstack/skills/hez-mode/SKILL.md).

the skill loads with the message you type it in and stays in the chat's context, but it fades as the chat moves on. t3 code has no custom modes, so type `/hstack:hez-mode` again at the start of each new task.

[`/hstack:hez-mode`](./plugins/hstack/skills/hez-mode/SKILL.md) works extremely well with t3 code's scheduler and pr watcher. it wakes itself with `schedule_task` and `watch_pull_request`, so you can make it work for many hours without sacrificing rigor.

## skills

[`/hstack:hez-mode`](./plugins/hstack/skills/hez-mode/SKILL.md) runs most of these for you when a step needs them (`how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, `unslop`, `no-comments`, `technical-writing`, `tdd`, and the principles). every skill except `setup-hstack` and `crawl-x` runs only when you call it. the table below is for when you want one directly:

```
/hstack:how do we cancel runs? do we have an n+1 when we look up every run to cancel?
```

```
/hstack:interrogate review this pr.
```

<details>
<summary>all skills</summary>

| skill | use it when |
|---|---|
| [`/hstack:hez-mode`](./plugins/hstack/skills/hez-mode/SKILL.md) | default entry point for any non-trivial task. |
| [`/hstack:hez-help`](./plugins/hstack/skills/hez-help/SKILL.md) | you're new to hstack, or unsure which skill, playbook, or principle fits. finds out what you're trying to do, answers that part, and hands you a prompt to type. runs only when you type `/hstack:hez-help`. |
| [`/hstack:in-your-own-words`](./plugins/hstack/skills/in-your-own-words/SKILL.md) | you want the agent to play back your goal and the problem before it starts. runs only when you type `/hstack:in-your-own-words`. |
| [`/hstack:sharpen`](./plugins/hstack/skills/sharpen/SKILL.md) | you want a task approached the way a top expert would, aimed at what you're really after, without overspecifying it or deciding your choices for you. |
| [`/hstack:how`](./plugins/hstack/skills/how/SKILL.md) | you want a walkthrough of how a subsystem works. |
| [`/hstack:why`](./plugins/hstack/skills/why/SKILL.md) | you want to know why something was built this way. discovers available MCPs at run time and queries each evidence category in parallel (source control, issue tracker, long-form docs, real-time chat, infra observability, error tracking, analytics warehouse). |
| [`/hstack:recall`](./plugins/hstack/skills/recall/SKILL.md) | you're starting or resuming work and want your recent context on a topic rebuilt from your own t3 code threads and the shared record, handed back as a tight current-state brief. |
| [`/hstack:ketchup`](./plugins/hstack/skills/ketchup/SKILL.md) | you want what changed in this chat since your last message, in plain words and small visuals, with every item waiting on you listed and decidable from the reply alone, even when that makes the reply long. |
| [`/hstack:blast-radius`](./plugins/hstack/skills/blast-radius/SKILL.md) | you have a small-looking change and want to know what else it could break, with the one fact it's safe because of proven by running code, not asserted. |
| [`/hstack:architect`](./plugins/hstack/skills/architect/SKILL.md) | you're about to write code that crosses a function boundary and want the caller's usage, types, and module shape settled first. |
| [`/hstack:arena`](./plugins/hstack/skills/arena/SKILL.md) | you want N parallel attempts at the same thing, then to grab the best parts of each. |
| [`/hstack:swarm`](./plugins/hstack/skills/swarm/SKILL.md) | you want N parallel workers across different slices or races, then one aggregated report. |
| [`/hstack:interrogate`](./plugins/hstack/skills/interrogate/SKILL.md) | you have a diff and want different models to try to break it, including a strict code-quality lens. |
| [`/hstack:automate-me`](./plugins/hstack/skills/automate-me/SKILL.md) | you want your own `-mode` skill, drafted from how you've actually worked. |
| [`/hstack:setup-hstack`](./plugins/hstack/skills/setup-hstack/SKILL.md) | you want to pick which models hstack uses per role. detects the models t3 code can run and writes the hstack model file. |
| [`/hstack:reflect`](./plugins/hstack/skills/reflect/SKILL.md) | a long task landed and you want the recipe captured as a skill edit. |
| [`/hstack:correct`](./plugins/hstack/skills/correct/SKILL.md) | you keep correcting agents for the same mistakes. mines history for mistake classes, fixes each at the highest level that works (architecture, then types, lint, and ci, then tests, with docs last), and keeps a table pairing each rule with what enforces it. |
| [`/hstack:teach`](./plugins/hstack/skills/teach/SKILL.md) | you want to actually understand a change or subsystem, not just have it summarized. runs how + why and weaves one plain explanation, built up diagram by diagram. |
| [`/hstack:tdd`](./plugins/hstack/skills/tdd/SKILL.md) | you're fixing a bug and there's a cheap local test path. write the failing test first, then the fix. |
| [`/hstack:benchmark-checklist`](./plugins/hstack/skills/benchmark-checklist/SKILL.md) | you ran a benchmark or measured a speedup or regression. vets the number (limiter, tuning, errors, repeat runs, end-to-end relevance) before you report or act on it. |
| [`/hstack:no-comments`](./plugins/hstack/skills/no-comments/SKILL.md) | strip comments before review; spawns Comment Sicko, fixes accepted findings, offers encodings for claimed constraints. |
| [`/hstack:typescript-best-practices`](./plugins/hstack/skills/typescript-best-practices/SKILL.md) | you're reading or editing typescript. grounds the type-system-discipline principle in syntax. |
| [`/hstack:luau-best-practices`](./plugins/hstack/skills/luau-best-practices/SKILL.md) | you're reading or editing roblox luau. `--!strict` with the new solver, a typed composition root instead of a scanning module loader, typed metatable classes, and server-side parsing of every remote. hstack's own skill, not from pstack. |
| [`/hstack:figure-it-out`](./plugins/hstack/skills/figure-it-out/SKILL.md) | no bundled playbook fits. designs a rigorous, auditable playbook for the task. |
| [`/hstack:show-me-your-work`](./plugins/hstack/skills/show-me-your-work/SKILL.md) | you want a reviewable decision trail. logs decisions to a tsv you can commit. |
| [`/hstack:create-verification-skill`](./plugins/hstack/skills/create-verification-skill/SKILL.md) | your project has no scripted way to prove app behavior. generates a project-local verify skill with a feature map, for any language or platform. |
| [`/hstack:maintain-verification-skill`](./plugins/hstack/skills/maintain-verification-skill/SKILL.md) | your verify skill's feature map has drifted from the app. source wave + one live pass, at most one PR of proven corrections. |
| [`/hstack:create-formal-verification-skill`](./plugins/hstack/skills/create-formal-verification-skill/SKILL.md) | tests can't reach the case that breaks a race, retry, state machine, parser, or unsafe code. verifies one property with the tool that fits and generates a project-local skill to recheck it on every change. |
| [`/hstack:unslop`](./plugins/hstack/skills/unslop/SKILL.md) | you're cleaning up writing. removes AI tells. |
| [`/hstack:bro`](./plugins/hstack/skills/bro/SKILL.md) | you want the last message restated in plain human language, no jargon. |
| [`/hstack:crawl-x`](./plugins/hstack/skills/crawl-x/SKILL.md) | you share an x.com or twitter.com link, or want a Tweet, thread, or profile on X read as Markdown. hstack's own skill, not from pstack. loads on its own when you share a link. |
| [`/hstack:technical-writing`](./plugins/hstack/skills/technical-writing/SKILL.md) | layered doc standard (Diátaxis + Google developer style + STE + Global English) for docs, RFCs, readmes, PR descriptions, commit messages. |

</details>



### examples

mostly i type [`/hstack:hez-mode`](./plugins/hstack/skills/hez-mode/SKILL.md) at the start of a task and let it route to a playbook. the other skills fire as the steps need them. a few i reach for directly.


<details>
<summary>all the examples</summary>

```
bug fix:           /hstack:hez-mode this pr has a subtle bug where the scroll drifts every 750ms
                   even when idle. repro first, then fix and verify.
perf:              /hstack:hez-mode a big list takes a second or two to load even though we
                   virtualize. run a cpu trace and tell me why.
feature:           /hstack:hez-mode build a small feature behind a feature flag. verify it really
                   works.
prototype:         /hstack:hez-mode build two prototypes of the markdown renderer so we can
                   compare. spawn an agent for each.
multi-phase:       /hstack:hez-mode open source these skills as a plugin. nothing internal leaks,
                   work in a temp dir, show me the dependency graph first.
overnight run:     /hstack:hez-mode i'm going to bed. land the stack even if ci flakes. i want
                   everything merged by morning.
babysit:           /hstack:hez-mode check on pr 123. anything outstanding?
visual parity:     /hstack:hez-mode the row spacing is too tall when this flag is on. the second
                   image is correct. repro and fix until it matches.
figure it out:     /hstack:hez-mode i'm stepping away. migrate every caller from the synchronous
                   store to the new async one, keeping behavior identical. i want to trust it was
                   done right when i'm back.
how:               /hstack:how do we cancel runs? do we have an n+1 when we look up every run to
                   cancel?
why:               /hstack:why is this feature flag not on yet?
architect:         design this instrumentation to be high signal with no false positives.
                   /hstack:architect this first.
arena:             /hstack:arena take my prompt to the arena verbatim. i want to compare their
                   proposals with yours.
swarm:             /hstack:swarm check every package under packages/ against its check.sh. one
                   worker per package. one report.
interrogate:       /hstack:interrogate review this pr.
tdd:               /hstack:tdd implement
unslop:            can we unslop and tighten the new changes?
reflect:           /hstack:reflect that took too long. capture what we learned so the next run
                   doesn't repeat it.
correct:           /hstack:correct
show-me-your-work: /hstack:show-me-your-work keep a decision trail i can review when i'm back.
automate-me:       /hstack:automate-me
crawl-x:           what's this thread saying? https://x.com/<user>/status/<id>
help:              /hstack:hez-help which skill should i use to review this branch?
```

</details>

## the `hez-agent` and Comment Sicko subagents

[`/hstack:hez-mode`](./plugins/hstack/skills/hez-mode/SKILL.md) runs in the chat that receives it. that chat owns the playbook, the todo list, and every subagent spawn.

hstack also ships [`hez-agent`](./plugins/hstack/agents/hez-agent.md) as the wrapper for delegates spawned during a run. it reads `hez-mode` in full, including its inline principles index, before doing any work. substituting a general-purpose subagent skips that read and drifts. do not spawn `hez-agent` to run the playbook itself. claude code names it `hstack:hez-agent`. codex needs the copy from [codex agents](#codex-agents). a delegated t3 code task has no agent type, so its brief tells it to read `hez-mode` first, per [delegation](./plugins/hstack/docs/delegation.md).

[`/hstack:hez-mode`](./plugins/hstack/skills/hez-mode/SKILL.md) and [`hez-agent`](./plugins/hstack/agents/hez-agent.md) route through the same wrapper.

hstack also ships [Comment Sicko](./plugins/hstack/agents/comment-sicko.md), a read-only comment reviewer available as the `comment-sicko` agent (`hstack:comment-sicko` in claude code). usually invoke it through [`/hstack:no-comments`](./plugins/hstack/skills/no-comments/SKILL.md), not directly.

## principles

twenty-four short skills, one principle each. `hez-mode` indexes them inline and reads that index at task start. the standalone files are there so other skills can reference a principle by name, and so the index can point at the full rule for each.

<details>
<summary>all twenty-four principles</summary>

| principle | group | rule |
|---|---|---|
| [laziness-protocol](./plugins/hstack/skills/principle-laziness-protocol/SKILL.md) | core | Bias toward deletion and the smallest change that solves the problem. |
| [foundational-thinking](./plugins/hstack/skills/principle-foundational-thinking/SKILL.md) | core | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious. |
| [redesign-from-first-principles](./plugins/hstack/skills/principle-redesign-from-first-principles/SKILL.md) | core | Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on. |
| [attack-the-premise](./plugins/hstack/skills/principle-attack-the-premise/SKILL.md) | core | Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it. |
| [subtract-before-you-add](./plugins/hstack/skills/principle-subtract-before-you-add/SKILL.md) | core | Remove dead weight, redundant validators, and stub references first, then build on the simpler base. |
| [minimize-reader-load](./plugins/hstack/skills/principle-minimize-reader-load/SKILL.md) | core | Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope. |
| [outcome-oriented-execution](./plugins/hstack/skills/principle-outcome-oriented-execution/SKILL.md) | core | Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code. |
| [experience-first](./plugins/hstack/skills/principle-experience-first/SKILL.md) | core | Choose user delight over implementation convenience; ship fewer polished features over more rough ones. |
| [exhaust-the-design-space](./plugins/hstack/skills/principle-exhaust-the-design-space/SKILL.md) | core | Build 2-3 competing prototypes and compare side by side before committing. |
| [build-the-lever](./plugins/hstack/skills/principle-build-the-lever/SKILL.md) | core | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the artifact a reviewer can rerun. |
| [model-the-domain](./plugins/hstack/skills/principle-model-the-domain/SKILL.md) | architecture | Encode the domain in a structure instead of scattered conditionals. |
| [boundary-discipline](./plugins/hstack/skills/principle-boundary-discipline/SKILL.md) | architecture | Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions. |
| [type-system-discipline](./plugins/hstack/skills/principle-type-system-discipline/SKILL.md) | architecture | Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants, derive from authoritative schemas. |
| [make-operations-idempotent](./plugins/hstack/skills/principle-make-operations-idempotent/SKILL.md) | architecture | Converge to the same end state regardless of partial prior runs. |
| [migrate-callers-then-delete-legacy-apis](./plugins/hstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | architecture | Migrate callers and delete the old API in the same wave instead of preserving compatibility layers. |
| [separate-before-serializing-shared-state](./plugins/hstack/skills/principle-separate-before-serializing-shared-state/SKILL.md) | architecture | Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant. |
| [prove-it-works](./plugins/hstack/skills/principle-prove-it-works/SKILL.md) | verification | Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'. |
| [fix-root-causes](./plugins/hstack/skills/principle-fix-root-causes/SKILL.md) | verification | Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate. |
| [sequence-verifiable-units](./plugins/hstack/skills/principle-sequence-verifiable-units/SKILL.md) | verification | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer. |
| [test-behavior-not-implementation](./plugins/hstack/skills/principle-test-behavior-not-implementation/SKILL.md) | verification | Apply when you write, change, or keep a test. Assert what the code's users can observe, so the test fails when that behavior breaks and keeps passing when only the internals change. |
| [explain-the-number](./plugins/hstack/skills/principle-explain-the-number/SKILL.md) | verification | Apply before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something other than the work you think. |
| [guard-the-context-window](./plugins/hstack/skills/principle-guard-the-context-window/SKILL.md) | delegation | Route bulk to subagents; keep summaries in the main thread, not raw payloads. |
| [never-block-on-the-human](./plugins/hstack/skills/principle-never-block-on-the-human/SKILL.md) | delegation | Proceed, present the result, let the human course-correct after the fact; reserve confirmation for irreversible actions. |
| [encode-lessons-in-structure](./plugins/hstack/skills/principle-encode-lessons-in-structure/SKILL.md) | meta | Encode the rule as a lint, metadata flag, runtime check, or script instead of more text. |

</details>

## not shipped here

a few things pstack bundles or references that hstack doesn't ship:

- `/deslop` and the `deslop` skill ship in cursor's `cursor-team-kit` plugin. hstack's playbooks drop that step, so ask for the code cleanup in plain words when you want it.
- `control-cli` (for CLIs and TUIs) and `control-ui` (for browser, Electron, web) ship in `cursor-team-kit` too. hstack drives apps with t3 code's preview and device tools instead, and runs CLIs and TUIs in a terminal, with tmux for an interactive TUI.
- `/create-skill` is a cursor built-in. hstack's [authoring playbook](./plugins/hstack/skills/hez-mode/playbooks/authoring-a-skill.md) uses a `skill-creator` skill instead, which hstack doesn't ship.

## why are there no planning skills?

t3 code already has a great plan mode which works great with hstack. but personally, i don't believe in planning. the best spec is code. if you do want to make a plan, [`/hstack:hez-mode`](./plugins/hstack/skills/hez-mode/SKILL.md) covers it, but it's not a default.

## make it yours

`hez-mode` is my style. you may not want exactly that.

type [`/hstack:automate-me`](./plugins/hstack/skills/automate-me/SKILL.md). it mines your recent t3 code threads in the project, drafts a `<your-name>-mode` skill from how you've actually worked, and routes through hstack underneath. you keep hstack as the base and end up with your own routing skill alongside `hez-mode`.

models are configurable too. type [`/hstack:setup-hstack`](./plugins/hstack/skills/setup-hstack/SKILL.md). it detects the models t3 code can run and writes the hstack model file, mapping each role (code, judgment, the review panels) to a model. every skill reads it fresh before each fan-out and falls back to sensible defaults when a role has no line, so you override only what you want.

when a default changes, a file written before the change still pins the old default. delete those role lines, or delete the file, then run `/hstack:setup-hstack` again. a rerun keeps any role whose model differs from the default.

## layout

```
.claude-plugin/marketplace.json     Claude Code marketplace
.agents/plugins/marketplace.json    Codex marketplace
plugins/hstack/
  .claude-plugin/plugin.json        Claude Code manifest
  .codex-plugin/plugin.json         Codex manifest
  skills/<name>/SKILL.md            shared by both tools
  skills/<name>/agents/openai.yaml  Codex-only skill metadata
  skills/hez-mode/playbooks/        the playbooks hez-mode routes to
  skills/hez-mode/scripts/          the PR watcher, plan checker, orchestration store, and worktree audit the playbooks run
  docs/delegation.md                how skills pick models and spawn workers in T3 Code
  docs/harness.md                   how skill text maps to Claude Code and Codex: tools, paths, transcripts
  agents/*.md                       subagents in Claude Code's format
  codex/agents/*.toml               the same subagents for Codex
scripts/                            version, agent, and skill checks
```

## develop

clone to `~/dev/skills`, then load the plugin from the clone so edits apply without reinstalling.

claude code loads any plugin folder in `~/.claude/skills/` as `<name>@skills-dir`. link it there instead of installing from the marketplace:

```powershell
# Windows
New-Item -ItemType Junction -Path "$HOME\.claude\skills\hstack" -Target "$HOME\dev\skills\plugins\hstack"
```

```bash
# macOS / Linux
ln -sfn ~/dev/skills/plugins/hstack ~/.claude/skills/hstack
```

codex copies plugins into its cache, so add the clone as a local marketplace and reinstall after edits:

```bash
codex plugin marketplace add ~/dev/skills
codex plugin add hstack@hezaerd        # rerun after each edit to refresh the cache
```

don't also install the skills another way (`npx skills`, links in `~/.agents/skills`), or each skill loads twice.

before opening a PR:

```bash
claude plugin validate .
python scripts/check-versions.py
python scripts/check-agents.py
python scripts/check-skills.py
```

ci runs all four on every PR.

## release

1. bump `version` in `plugins/hstack/.claude-plugin/plugin.json`, `plugins/hstack/.codex-plugin/plugin.json` and the `hstack` entry in `.claude-plugin/marketplace.json`. add a `CHANGELOG.md` entry.
2. merge to `master`.
3. tag it from `master`: `claude plugin tag plugins/hstack --push`. this creates `hstack--v<version>` and fails if the manifests disagree.

## license

[MIT](./LICENSE), like pstack.
