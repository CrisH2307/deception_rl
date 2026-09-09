---
name: p2-task
description: Load and execute a single Paper 2 task brief by ID (T0 through T9). Use when the user invokes /p2-task with a task ID, or asks to start, run, or work on a specific P2 task such as "start T1" or "run the oracle task".
---

# P2 Task Runner

Loads one task brief from the Paper 2 plan and executes it under the project
invariants. One task per session.

## Procedure

1. **Identify the task ID** from the user's invocation (T0 through T9). If no ID was
   given, list the available tasks from `docs/P2/tasks/` with their titles and ask
   which one. Do not pick one.

2. **Read `docs/P2/tasks/<ID>.md` in full** before doing anything else.

3. **Check preconditions.** Each brief states its own. In addition, these apply
   globally:
   - Every task except T0 requires `docs/spec/adversary-game-v1.md` to exist. If it
     does not, stop and tell the user T0 must run first.
   - T6, T7, T8 and T9 require the preregistration from T5 to exist.
   - T7 and T8 require T6 to have reported a passing kill gate. Look for the recorded
     gate result. If you cannot find an explicit pass with a number attached, stop.
     Do not infer a pass from the absence of a recorded failure.

   If a precondition is unmet, report which one and stop. Do not begin partial work.

4. **Read `CLAUDE.md`** and treat its invariants as binding. If the task brief and
   `CLAUDE.md` conflict, stop and report the conflict rather than resolving it.

5. **Plan before executing.** For any task that writes code or produces analysis,
   state your plan and the files you intend to touch, then proceed. For T4 and T5,
   which produce prose, outline first.

6. **Execute the brief.** Honour its anti-requirements as strictly as its
   requirements. The anti-requirements exist because the failure modes they describe
   are the likely ones.

7. **Report at the end**, in this order:
   - What the brief asked for, and whether each deliverable exists
   - Any number the brief asked you to report, stated explicitly
   - Anything you could not do, and why
   - Any assumption you had to make, flagged for author review

## Scope discipline

Do exactly one task. Do not start the next one because it looks ready. The waves are
gated deliberately and the author decides when a gate opens.

If you finish early, do not expand scope. Report completion and stop.

## When a task reveals a spec problem

If executing a brief shows that an assumption in `docs/spec/adversary-game-v1.md` is
wrong or underspecified, stop immediately and report it. Do not patch around it
locally. A spec change is cheap; reconciling three divergent implementations that each
patched around the same gap is not.
