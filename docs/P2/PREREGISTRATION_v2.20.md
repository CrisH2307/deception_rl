# PREREGISTRATION v2.20

**Paper 2: the adversary effect and the RL Scientist**

Version 2.20 · written 2026-09-21 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.19`.

**Status.** New file per Paper 1's **D148**. `v2.0` through `v2.19` are not edited. This
version **records what was computed** under P2-D27. It rules nothing, decides nothing, and
takes no new `P2-D` number.

**Written by an agent session acting on an author instruction**, per the countermeasure in
`v2.10` section 2.4. The session is not the author. The instruction it acted on is quoted
in section 1.

**This session computed.** It is the other half of the split P2-D27 was made under: the
ruling session did not know the control change rate, and this session computed it exactly
as `v2.19` section 5 fixes it, choosing nothing.

**What is unchanged.** `p0` is 0.5. The confirmatory family is 21 tests at
`alpha = 0.05/21`. The confirmatory `n` is 108. No statistic, unit, tolerance, null, floor
or family moves. No decision is reopened.

---

## 1. The instruction

Quoted in the parts that bear on what was computed.

> You are running one task in your own git worktree on the deception_RL Paper 2 repo:
> **compute the control change rate exactly as P2-D27 specifies, and report it beside
> quantity (a)**. You compute. **You rule nothing.**
>
> P2-D27 ... ruled, before the value existed, that a change rate on the 142-item control
> set is a **new quantity, authorized as exploratory and descriptive**, and **fixed every
> choice in it by matching quantity (a) cell for cell**. **v2.19 section 5 is your
> specification and it leaves you no choices.** If you find a choice it did not fix, stop
> on that point and report it; do not make it.
>
> Compute no quantity P2-D27 did not authorize. In particular, **no difference, ratio,
> attributable share, or test of (a) against the control rate** ... Side by side, per
> cell, in the same units, and nothing else.
>
> **Check the one bound the ruling disclosed.** For paired renderings, TV between the two
> marginals cannot exceed the share of pairs whose choice changed. ... say on which cells
> that premise holds and on which it does not. A cell where the change rate is below that
> TV on identical renderings is a bug, not a result: stop and find it.
>
> **Put the rate beside (a) in the outline.** ... using the comparability sentence v2.19
> section 7 gives. ... Do not add a difference, ratio or share anywhere in the outline.

with the constraints: every pre-existing `results/*.json` byte-identical; no superseded
preregistration edited; this file records the computation; no new P2-D number; commit on
the worktree branch, do not merge or push.

---

## 2. What was computed, and how it matches `v2.19` section 5

`python3 src/t7_control.py --change-rate` writes `results/T7_control_change_rate.json` and
`reports/T7_control_change_rate.md`. `main()` is untouched in what it emits.

| `v2.19` section 5 element | as run |
|---|---|
| instrument | `c5_effect.c5_movement`, unmodified, called directly |
| contrast, arms, models | `("framing", "F0")`, `P2D27_ARMS`, `tie_reference.LADDER`: 14 cells |
| item set | `t7_control.geometry()["robust_by_tile"]["size"]`, 142 items, arity 6; 540 base not computed |
| choice rows | `t7_armb.load_t7()`'s `kept` |
| pair unit, exclusion, attrition | `pair_frame` inside `c5_movement`; `t7_armb.attrition` per cell as `attrition_P2D16` |
| interval | as `c5_movement` emits it: 10,000 resamples, seed 20260910, `alpha = 0.05/21`, no inferential role |
| floor, verdict flags, second TV, derived quantities | none emitted |
| per-cell fields | exactly `P2D27_FIELDS`, checked by `bind_control_change_rate` against the emitted names |
| bindings | `bind_control_change_rate` with `v2.19` section 5's arguments, and `bind_tie_exclusion` as `t7_armb` calls it, both before anything is emitted |
| (a)'s values | not copied; each cell carries the key path of (a)'s same cell |

The artifact carries `standing`, `comparison_licensed` and `comparison_sentence` (the
`v2.19` section 7 sentence) as fields. The report places (a)'s values beside the control's,
read from `results/T7_armb_quantities.json` at report time.

**Choices `v2.19` section 5 left unfixed.** None found that bears on a value. Two
presentational points were settled by the record rather than chosen: the report's table
format, and the item arity in `control_base`, which is read from the frozen geometry.

---

## 3. The TV bound, checked

P2-D27 disclosed that on any cell whose `TV` was formed on the same renderings the pairs
use, the rendering-level change rate is at least that `TV`. The premise is tested as: the
`TV` of record in `results/T7_control_marginal_null.json` was formed on as many `F0` and arm
renderings as there are surviving pairs, both from the same `kept` and the same choices
file (hash asserted). Pair renderings are a subset of the `TV` renderings, so equal counts
mean identical renderings.

The cells on which the premise holds and fails are emitted at
`results/T7_control_change_rate.json:tv_bound_check`. The premise fails on one cell, where
one arm rendering is tied: `TV` was formed on the base's full set of renderings and the pair
drops its partner. On every cell where the premise holds the bound holds; a violation stops
the run as a bug and none occurred. `tests/test_p2d27_control_change_rate.py` re-derives the
check from both artifacts.

---

## 4. Byte identity

Every `results/*.json` and `results/*` file present before this session was hashed with
`shasum -a 256` before and after. All are byte-identical. The only new artifact is
`results/T7_control_change_rate.json`.

---

## 5. What this version changes

- `src/t7_control.py` gains `change_rate`, `change_rate_report`, `change_rate_main`,
  `tv_bound_premise` and a `--change-rate` flag. `main()` and `compute()` are unchanged.
- `results/T7_control_change_rate.json` and `reports/T7_control_change_rate.md` are added.
- `tests/test_p2d27_control_change_rate.py` gains four tests on the computed artifact.
- `docs/P2/RESULTS_OUTLINE.md` section 4.6 places the control rate beside (a), per cell, in
  the same units, by file and key, with the `v2.19` section 7 sentence; its needed-and-absent
  entry is re-cited to P2-D27.
- No decision, no new P2-D number, no superseded preregistration edited, no difference,
  ratio, share or test of (a) against the control rate anywhere.
