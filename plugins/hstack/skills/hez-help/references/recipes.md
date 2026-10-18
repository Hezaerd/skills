# Prompts worth copying

Swap in the real paths, skills, and done checks. Informal wording works.

## Understand

- `/hstack:hez-mode read <thread>. restate the underlying issue in your own words, in plain english.`
- `/hstack:in-your-own-words <long or messy ask>`
- `/hstack:sharpen <your task>`
- `/hstack:hez-mode investigate why <symptom>. give me what we know, what data you used, and your best hypotheses. don't change any code yet.`
- `use /hstack:how to understand <subsystem>. then use /hstack:why to find out why it broke recently.`
- `/hstack:recall my work on <topic> from last week, then read <issue>.`
- `/hstack:teach me why you implemented it this way and not <other way>. what did you trade off?`
- `/hstack:hez-mode take over this branch. read the decision log, find what's done, and continue. don't redo finished work.`

## Build

- Bug: `/hstack:hez-mode <symptom>. repro first, then fix and verify.`
- Bug in an app: `/hstack:hez-mode repro this with /verify-<app>. if it repros on main, fix it and show me a video as proof.`
- Bug with a cheap test: `/hstack:hez-mode repro <bug> first. if there's a cheap test path, /hstack:tdd it. then fix and rerun.`
- Feature: `/hstack:hez-mode add <behavior>. <current output> stays byte-identical. verify both.`
- Refactor: `/hstack:hez-mode move <code> into one module, zero behavior change. record the current output first and prove it's unchanged after.`
- Perf: `/hstack:hez-mode <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.`

## Design and plan

- `/hstack:hez-mode prototype a few options for <feature>. take screenshots or videos for me to compare.`
- `/hstack:hez-mode we need <feature>. /hstack:architect it first, and answer open questions with prototypes. let me review before proceeding.`
- `/hstack:hez-mode write a tutorial for how i would use <new package> first. then /hstack:teach me why it beats the current one.`
- `ask /hstack:arena for a second opinion on this thread and our approach.`
- `/hstack:hez-mode turn this design into a plan. small verifiable PRs, each with its own verification steps.`
- `/hstack:hez-mode plan the migration of <library> to <target>. small verifiable PRs. the result must match the original exactly, bugs included.`

## Review and ship

- `/hstack:interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's a real bug or regression.` Read the dismissals too.
- `/hstack:swarm check every package under <dir> against its check script. one worker per package. one report.`
- `/hstack:hez-mode open the pr. small ordered commits, evidence in the description.`
- `/hstack:hez-mode babysit this pr. get it green.` For status only: `/hstack:hez-mode check on pr <number>. anything outstanding?`
- `/hstack:hez-mode land the stack.`

## Away and back

- `/hstack:hez-mode im going to bed. <goal> in a fresh worktree off <base>. done means <checks>. keep a decision log. don't ask me before committing. keep going until done. if you're truly stuck after a few hours, stop and write up why.`
- `/hstack:show-me-your-work catch me up on what you did last night.` Read its Attention section first.
- `/hstack:hez-mode full autopilot on this queue. each item is independent.`
- `/hstack:hez-mode autopilot these changes but stack them, don't ship. i'll land the stack.`
- `/hstack:reflect capture what we learned so the next run doesn't repeat it.` Approve only edits that change a future decision.
- `/hstack:bro` restates the last reply in plain words.
