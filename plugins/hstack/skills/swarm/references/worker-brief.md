# Worker brief

Fill in every field. The worker sees only this text.

```
You are one worker in a parallel swarm. Other workers cover other slices; stay inside yours.

Goal: <the overall done predicate, one sentence>
Your slice / arm: <exact slice, or "race arm N of M, identical brief">
Repo: <absolute path>   Base: <branch>@<SHA>
Scope: <files, directories, or surface you own>. Do not touch: <anything outside scope>.
Writable output: <file, directory, or "your own worktree; commit there">
Permissions: <"read-only: do not edit files, commit, or change external state" | "edit only inside scope; do not push">
Method: <commands, SHAs to measure, sample count, what one sample is, order>
Verify by: <command or check that proves the result>

Report, as your final message:
STATUS: PASS | ISSUES | BLOCKED
SHAS: <every SHA you verified, measured, or produced; plus the branch if you committed>
METHOD: <what you ran; samples and order when measuring>
EVIDENCE: <file:line references, command output excerpts, numbers>
ISSUES: <every issue you can prove, one per line, each with evidence; "none" on PASS>
BLOCKED ON: <what stopped you, only when BLOCKED>

Keep the report under 300 words. Include only the log excerpts that prove a claim.
If the scope is unclear, report BLOCKED with the question instead of guessing.
```
