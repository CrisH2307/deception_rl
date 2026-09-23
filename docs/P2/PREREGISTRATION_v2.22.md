# PREREGISTRATION v2.22

**Paper 2: the adversary effect and the RL Scientist**

Version 2.22 · written 2026-09-22 · follows `v2.1` through `v2.21`.

New file per Paper 1's **D148**. This version records one author ruling (**P2-D28**), one
decision taken on an author's conditional instruction (**P2-D29**), and three bookkeeping
corrections. It changes no statistic, no item set, no `n`, and no `beta_c` value of
record. It does not touch Arm C.

**The instruction this acted on**, per `v2.10` section 2.4's countermeasure. The author
accepted `v2.21`'s Verdict 1 and its corrections. The author asked that bisection's zero
identity violations be recorded as by construction and not as evidence, with the direct
`V_beta` evaluation on 258 items as the evidence. Then five items, in one session, with
no drafting: (1) record the ruling on the tolerance-divergent items; (2) measure the
crossing coefficients on genuinely crossing pairs, set the parallel-case threshold inside
an empty gap if one exists by P2-D19's method, and assert the cross-check's residual
equals the tolerance-determined set; (3) add to the outline that no sentence may imply
quantity (a)'s movement is caused by adversary content; (4) if 470 and 439 were the
`sb`-pole split, correct the prose in P2-D6's reasoning and `T7.md` with a dated note,
words only; (5) replace the outline's stale section 1.4 pool bullet with the verified
result. Treat every number in the instruction as unverified. This document is written by
an agent session acting on that instruction, not by the author.

New figures are emitted by `src/crossing_tolerance.py` into
`results/T1_crossing_tolerance.json`.

---

## 1. What the evidence for bisection is

Recorded as the author directed. Bisection's zero violations of the identity "`beta_c`
finite iff `o*_0 != o*_infinity`"
(`results/T1_beta_c_disagreement.json:identity_beta_c_finite_iff_o0_ne_oinf.all.bisection_violations`)
are **by construction and are not evidence**. `beta_critical_batch` returns infinity
exactly when the `beta -> infinity` selector returns `o*_0`, so it cannot violate the
identity. The evidence is the direct `V_beta` evaluation in `v2.21` sections 3 and 4.
It covered the 62 items plus the 60 where the closed form fires early, and the 99 plus
the 37 where it fires late or not at all: 258 items. On every one, no rival leads `o*_0`
beyond D51's band at a point where bisection says it does not, and `o*_0` never regains.

## 2. P2-D28: the tolerance-determined items stay, disclosed

Decision text in `docs/P2/DECISIONS.md` P2-D28. The emitted facts, pool base:

| | key |
|---|---|
| tolerance-determined items | `results/T1_crossing_tolerance.json:bases.pool_200000.n_tolerance_determined` |
| divergent only by tie-break | `results/T1_crossing_tolerance.json:bases.pool_200000.n_divergent_only_by_tie_break` |
| `beta_c` range | `results/T1_crossing_tolerance.json:bases.pool_200000.tolerance_determined_beta_c_range` |
| all above the grid endpoint | `results/T1_crossing_tolerance.json:bases.pool_200000.tolerance_determined_all_above_grid_endpoint` |
| separating items among them | `results/T1_crossing_tolerance.json:bases.pool_200000.n_separating_tolerance_determined` |
| frozen 1,000 | `results/T1_crossing_tolerance.json:bases.frozen_1000.n_tolerance_determined` |

**Definitions, from `V_beta` and never from the closed form.** An item is
**tolerance-determined** when its bisected `beta_c` is finite and the tie-broken winner
just past it never leads `o*_0` beyond the band at any `beta`. For a linear-fractional
`V_beta` the ratio of two options' values is monotone in `x`, so "never" is checked at
`beta = infinity`, where the ratio is the margin difference. An item is **divergent only
by tie-break** when no rival at all ever leads `o*_0` beyond the band.

**Correction to `v2.21` section 8, which was wrong.** It said 99 of the pool's divergent
items are divergent only by tie-break. All 136 are. The 99 is the number the exact-test
closed form classed robust. The other 37 had closed-form roots, and section 3 below shows
those roots are spurious in their own way. `v2.21` is not edited, per D148; this section
supersedes its sentence.

## 3. P2-D29: the closed form's parallel case, measured then set

**The measurement.** Every (item, rival) pair with a closed-form root `x >= 1` under the
exact test, on both bases, is classed by `V_beta` alone:

- **identical**: the rival's lead over `o*_0` is inside the band at `beta = 0` and at
  `beta = infinity`, hence everywhere. `results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.n_root_pairs_indistinguishable`
  pairs, all numerators at most
  `results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.indistinguishable_max_abs_num`,
  all denominators at most
  `results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.indistinguishable_max_abs_den`.
- **converging**: outside the band at `beta = 0`, inside it at `beta = infinity`. Any
  crossing is below the band's resolution.
  `results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.n_root_pairs_converging`
  pairs. Their numerators are real, at least
  `results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.converging_min_abs_num`.
  Their denominators, the coefficient of `x`, are rounding residue, at most
  `results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.converging_max_abs_den`.
- **strict**: outside the band at `beta = infinity`.
  `results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.n_root_pairs_strict`
  pairs, denominators at least
  `results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.strict_min_abs_den`,
  numerators at least
  `results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.strict_min_abs_num`.

**The gap exists.** On the coefficient of `x`, every identical or converging pair sits
at or below the lower end of
`results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.den_gap` and every
strict pair at or above its upper end: 3.5e-17 to 7.3e-8, nothing in between. The frozen
1,000 has no identical or converging root pair at all
(`results/T1_crossing_tolerance.json:bases.frozen_1000.coefficients.n_root_pairs_indistinguishable`,
`results/T1_crossing_tolerance.json:bases.frozen_1000.coefficients.n_root_pairs_converging`).
Its strict denominators start at
`results/T1_crossing_tolerance.json:bases.frozen_1000.coefficients.strict_min_abs_den`.

**The threshold, by P2-D19's method.** `EPS_TIE = 1e-12`, the spec's inherited absolute
tolerance, lies inside the gap
(`results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.parallel_tol_inside_den_gap`).
It is written down as `adversary.PARALLEL_TOL`, and `_crossings` treats `|den| <=
PARALLEL_TOL` as spec 6.3's degenerate case. Every tolerance inside the gap classifies
identically, so this is a property of the geometry and not of the constant.

**Where this departs from the instruction's framing, and why.** The instruction quoted
both noise levels and `v2.21` section 7 proposed a both-coefficients rule. The measurement
shows the converging pairs, which `v2.21` did not separate. There the numerator is real
and only the coefficient of `x` is residue, so the both-coefficients rule would leave 37
spurious roots
(`results/T1_crossing_tolerance.json:bases.pool_200000.cross_check_both_below_not_adopted`).
The spec's degenerate case is the coefficient of `x` being zero, in both its parallel and
its identical form, so the threshold is set on that coefficient. The numerator also has
an empty gap, from 1.0e-15 to 4.8e-4
(`results/T1_crossing_tolerance.json:bases.pool_200000.coefficients.empty_gap`), and it
is reported, but it is not the test.

**What was not changed.** Bisection, D51's band and `beta_c`'s value of record.
`src/beta_c_crosscheck.py` and `src/beta_c_disagreement.py` now pass `parallel_tol=0.0`
explicitly. Both regenerate byte-identical artifacts, verified in this session, so
`v2.21` still reproduces.

## 4. The cross-check's expected residual, now an invariant

The closed form tests strict crossing, and a tie-break flip has no strict crossing, so it
cannot see one by design. After P2-D29, on the pool:

- classification disagreements
  `results/T1_crossing_tolerance.json:bases.pool_200000.cross_check_adopted_parallel_tol.n_classification_disagree`,
  every one bisection-finite and closed-form-infinite
  (`results/T1_crossing_tolerance.json:bases.pool_200000.cross_check_adopted_parallel_tol.n_bisection_finite_closed_form_inf`);
- the disagreement set **equals** the tolerance-determined set of section 2,
  `results/T1_crossing_tolerance.json:bases.pool_200000.cross_check_adopted_parallel_tol.residual_equals_tol_set`;
- no both-finite item disagrees: the largest gap outside that set is
  `results/T1_crossing_tolerance.json:bases.pool_200000.cross_check_adopted_parallel_tol.max_abs_gap_both_finite_outside_tol_set`,
  below the reported edge `results/T1_crossing_tolerance.json:gap_edge`.

On the frozen 1,000 the residual is empty and the set is empty. `tests/test_crossing_tolerance.py`
and `p2_decisions.bind_parallel_tol` assert it. A future disagreement off the
tolerance-determined set fails there as a bug and is not absorbed as residual.

The edge `1e-3` is needed only for the exact-test comparison, where noise roots give gaps
up to 4.66. After the fix, both-finite gaps reach 1.9e-4. That is larger than the frozen
base's 2.2e-6 and is reported as a number, not thresholded, as the cross-check has always
reported its gap.

## 5. The mixture wording, corrected in words only

The 470, 439 and 841 option-cells are the split by Paper 1's `sb` poles:
`results/T6_F0_headroom.json:coordinate_geometry.n_option_cells_by_p1_pole`. Split by
`A`'s own value the counts are 464, 439 and 847:
`results/T6_F0_headroom.json:coordinate_geometry.n_option_cells_by_A_value`. P2-D6's
reasoning in `docs/P2/DECISIONS.md` and section 2 of `docs/P2/tasks/T7.md` called them
cells "at exactly 0" and "exactly 1" of `A`. Both are corrected in place with a dated note
beside each. Nothing was recomputed, and P2-D6's quoted decision text is untouched.

The same words also appear in these places, which are **not edited** because they are
superseded versions or emitted artifacts that must stay byte-identical:
`PREREGISTRATION_v2.4.md`, `v2.16.md` and `v2.17.md`; `src/t7_control.py`'s emitted
note string; and `reports/T7_control_marginal_null.md`. The outline's section 6 names
which partition a drafter must cite.

## 6. The outline

- Section 1's pool cross-check bullet, "NOT clean, reported and not resolved", is replaced
  with the verified result and P2-D29's invariant.
- Section 1.5 carries P2-D28's disclosure beside the pool existence rate.
- Section 3.3 notes that the 2,748 is verified against both methods and that none of them
  is tolerance-determined.
- Section 4 carries a new may-not-say rule: no sentence may imply that quantity (a)'s
  movement is caused by adversary content. The grounds are P2-D26
  (`p2_decisions.P2D26_ADVERSARY_TRACKING_CLAIM_AVAILABLE`) and quantity (b)'s 11 of 14
  unresolved cells, counted from
  `results/T7_armb_quantities.json:cells.*.b_magnitude_context.resolves` (three true).
- Section 6's mixture paragraph now records the correction.

## 7. Corrections to the instruction

- "the 99 that are divergent only by tie-break": 136 (section 2). The error was `v2.21`'s,
  repeated in the instruction.
- "beta_c between 17.3 and 23.4": emitted as 17.345 to 23.446, which the instruction
  truncates.
- "at most 1e-15 on the numerator, 2.1e-17 on the denominator": the pool-wide measurement
  over every identical root pair gives 1.0e-15 and 3.5e-17. `v2.21`'s 2.1e-17 was the
  binding competitor only. It does not change the gap.
- "set the parallel-case threshold inside it": set on the coefficient of `x` alone, for
  the reason in section 3.

## 8. What this version changes

| | |
|---|---|
| `beta_c` value of record | unchanged: bisection |
| the 2,748, all inside the span guard | stand; none tolerance-determined |
| `adversary._crossings` | parallel case read at `PARALLEL_TOL = EPS_TIE` (P2-D29) |
| `results/T1_beta_c_crosscheck.json`, `T1_beta_c_disagreement.json` | byte-identical, pinned to the exact test |
| the 136 tolerance-determined pool items | kept in `D(infinity)`, disclosed (P2-D28) |
| `v2.21` section 8's "99" | superseded: 136 |
| P2-D6 reasoning, `T7.md` section 2 | words corrected, dated note |
| Arm C | not touched |
