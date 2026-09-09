# Project memory

## What this repo is

A research program on signal selection under a constrained channel, using a
forced-choice signalling task abstracted from the board game Deception: Murder in
Hong Kong.

**Paper 1 is finished and published** (arXiv:2609.00576, "Consistency Without
Alignment: Item-Sensitive Language Models Indistinguishable From Random"). Its
finding: models are item-sensitive but sit outside the salience-Bayes interval on the
far side of salience. Item-sensitivity is necessary but not sufficient evidence of
task competence.

**Paper 2 is in progress.** It adds an informed adversary who shares the audience and
asks three questions: does the optimal signal change (Arm A), do language models
track that change (Arm B), can a learned policy recover it (Arm C).

Plan: `docs/P2/prompt-plan.md`. Literature and formal core: `docs/P2/foundation.md`.
Individual task briefs: `docs/P2/tasks/T0.md` through `T9.md`.

## Frozen artifacts, never modify

These are shared with the published Paper 1. Changing any of them silently
invalidates the Paper 1 comparison, which is the point of Paper 2.

- The concept vocabulary and similarity space
- The `fit` function (min-aggregation exponential decay, no free parameters)
- The candidate pool and its construction code
- The Format V rendering
- Paper 1's item set, prompt templates, and reported results

If a task appears to require changing one of these, that is a design problem. Stop and
report it. Do not work around it.

## Hard rules

**The spec is authoritative.** `docs/spec/adversary-game-v1.md` is the single source
of truth for the adversary game. If it is ambiguous, stop and ask. Do not resolve
ambiguity by choosing, because parallel sessions will choose differently and diverge.

**Stop rather than guess.** Every task brief lists preconditions. If one is unmet,
report it and stop. Producing plausible output from an unmet precondition is worse
than producing nothing, because it looks like progress.

**No tuning toward a desired result.** Do not adjust parameters, thresholds, reward
shaping, or exclusion rules to make an outcome look better. If something must be
tuned, it is preregistered before it is tuned.

**No silent clipping, clamping, or regularization.** If a value is degenerate,
surface it. Numerical convenience that changes results is a bug.

**Failures are data.** Parse failures, non-convergence, and null results get reported
as numbers, not retried away. A model indistinguishable from the marginal null is a
finding; say so plainly.

**Beating the oracle is a bug.** If any policy outperforms the analytically computed
optimum, the oracle or the environment is misspecified. Find the bug. Do not report it
as a result.

**Every number in the paper is script-emitted.** No number is read off a plot or
typed from a draft. `verify_paper.py` recomputes all of them from frozen artifacts and
committed seeds.

**No invented citations.** Cite nothing you have not verified against arXiv or a
publisher record. One fewer reference beats one invented reference. Verified reference
list is in `docs/P2/foundation.md` section 10.

## Kill gates

Paper 2 has preregistered stop conditions. They are not advisory.

1. **Divergence set gate (T6, Step 1).** If the divergence set is below the
   preregistered fraction at the largest plausible beta, the adversary effect does not
   exist in this signal space. Arms B and C do not run. Report the number and stop.
2. **fit_cost correlation gate (T2).** If `beta_c` correlates with `fit_cost` above
   the preregistered threshold, the redraw rationale collapses and the design needs
   revisiting.

An agent working a task list will treat "stop" as a failure state and look for a
reason to continue. Do not. Reporting a failed gate is a successful task outcome.

## Reproducibility

- Seeds are committed and results reproduce exactly from them.
- Item files carry a manifest recording seed, pool hash, bin edges, per-cell counts,
  and spec version.
- Raw model outputs are never overwritten.
- Chain of custody: item hash matches manifest, manifest cites spec version, spec
  version matches the implementation.

## Writing conventions

- Do not use em dashes. Use commas, colons, or separate sentences.
- Direct and concise. No hedging, filler, or unnecessary disclaimers.
- Explain the reasoning behind a choice, not just the choice.
- Do not use bracketed placeholder markers in paper prose. Research notes may use
  `[unconfirmed: ...]`; paper prose may not.
- Do not overstate novelty. Paper 2's human-behaviour gap claim is narrow and is
  stated precisely in `docs/P2/tasks/T4.md`. Use that wording, not a broader version.

## Working style

- Read the relevant task brief in full before acting.
- Prefer editing existing code over reimplementing. If you find yourself copying a
  frozen function, that is a duplication bug that will silently diverge.
- Vectorize where the pipeline runs over the 200k candidate pool.
- Log space throughout for probability math.
- Tests are real test files, not notebook assertions.

## Session hygiene

- One task per session. Use `/clear` between tasks.
- Wave 1 tasks run in separate git worktrees, not concurrently in one directory.
- `/p2-task T1` loads a task brief. See `.claude/skills/p2-task/SKILL.md`.


## Addition
- Before citing a P1 behaviour, trace the code path that produced the frozen
artifact, not the module that looks like it should have. src/oracle.py is a
Task-11 diagnostic; src/score_items.py -> grid_stats -> src/tiebreak.py is what
produced items_final.parquet. Reading the plausible module instead of the actual
one produced the v2 posterior error and its wrong explanation.