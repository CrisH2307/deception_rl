# PREREGISTRATION v2.21

**Paper 2: the adversary effect and the RL Scientist**

Version 2.21 · written 2026-09-22 · follows `v2.1` through `v2.20`.

New file per Paper 1's **D148**. This version records a **verification**, not a
decision. It adds no `P2-D` number, changes no statistic, no item set, no `n`, no
`beta_c` value of record, and applies no fix. It determines which of three verdicts,
stated in advance by the author, the evidence selects.

**The instruction this acted on**, per `v2.10` section 2.4's countermeasure. The author
instructed a verification of the 161 pool items on which the closed-form and bisected
`beta_c` disagree (`results/T1_beta_c_crosscheck.json`), stated three verdicts in advance,
and required: check the identity "`beta_c` finite iff `o*_0 != o*_infinity`" per method
and per tile; evaluate `V_beta` directly for `o*_0` and the competing option on the 29
items that change separating status and on the other disagreements; test the hypothesis
that both coefficients of the crossing equation are float noise on near-identical curves;
check whether bisection's search ceiling explains any of the 62; rule nothing about Arm
C; fix nothing; treat every number in the instruction as unverified. This document is
written by an agent session acting on that instruction, not by the author.

All figures below are emitted by `src/beta_c_disagreement.py` into
`results/T1_beta_c_disagreement.json`.

---

## 1. The verdict: closed form spurious, single-crossing intact

**Verdict 1 applies. Bisection stands, and the 2,748 and its "all" stand.**

- Separating items among divergent, under the value of record:
  `results/T1_beta_c_disagreement.json:separating_count_bisection`, all inside P1's span
  guard: `results/T1_beta_c_disagreement.json:all_separating_inside_span_guard_bisection`.
- The 29 that would enter under the closed form
  (`results/T1_beta_c_disagreement.json:separating_that_enter_under_closed_form`) are all
  in group A below: `results/T1_beta_c_disagreement.json:separating_that_enter_are_all_in_group_A`.
  Group A is spurious, so none of them enters.

## 2. The identity, per method

`results/T1_beta_c_disagreement.json:identity_beta_c_finite_iff_o0_ne_oinf`. The closed form
violates it on exactly the disagreeing items, by tile. Bisection shows zero violations,
**by construction and not as evidence**: `beta_critical_batch` returns infinity for any
item whose `beta -> infinity` selector returns `o*_0`, so it cannot violate the identity.
The identity therefore tests the closed form only.

## 3. Group A: closed form finite, bisection infinite. Spurious roots

`results/T1_beta_c_disagreement.json:group_A_closed_form_finite_bisection_inf`, 62 items,
the 29 among them.

- **Both crossing coefficients are rounding residue.** Every one of the 62 has
  `|num|` and `|den|` below `EPS_TIE = 1e-12` (`.n_both_coeffs_below_eps_tie`), with
  maxima `.max_abs_num` and `.max_abs_den` and relative size `.max_rel_num`,
  `.max_rel_den`, a few units in the last place of float64. Their ratio is therefore a
  random number, and it lands at `x >= 1` on these items. The author's hypothesis holds.
- **The competitor never overtakes.** Its largest lead over `o*_0` on a dense `beta` grid
  is `.max_lead_over_o0`, some four orders inside D51's band
  (`results/T1_beta_c_disagreement.json:d51_band`). The raw lead changes sign many times,
  and every change happens at this noise level: the two curves are numerically identical,
  not crossing.
- **The spec's predicate never leaves `o*_0`.** Tie-broken argmax: `o*_0` loses on
  `.n_o0_loses` items and regains on `.n_o0_regains`. None is live (`.n_live`).
- **The pairs are the tied-content pairs.** `.pairs`: overwhelmingly `size` options (4,5)
  and (0,1), the same pairs P2-D19 found carrying the `A` ties. Identical fit rows give
  identical `V_beta` curves.

The same mechanism fires *early* on both-finite items:
`results/T1_beta_c_disagreement.json:both_finite_closed_form_earlier`, 60 items, all
coefficient pairs below `1e-12`, competitor never above `.max_lead_over_o0`. These are
most of the large `beta` gaps.

## 4. Group B: bisection finite, closed form infinite. Tie-break flips

`results/T1_beta_c_disagreement.json:group_B_bisection_finite_closed_form_inf`, 99 items,
and the same mechanism on both-finite items where the closed form fires *later*,
`results/T1_beta_c_disagreement.json:both_finite_closed_form_later`, 37 items.

On every one: the margins of `o*_0` and the winner are equal to `1e-9`
(`.n_margins_equal_1e9`), so the two curves converge on each other asymptotically; the
winner enters D51's band at bisection's `beta_c` (`.n_winner_inside_d51_band`) and wins
on fit (`.n_winner_higher_fit`); it never leads `o*_0` by more than
`.max_winner_lead_over_o0`; and `o*_0` never regains (`.n_o0_regains`). This is the
tie-broken argmax spec section 6.2 defines, so bisection is correct. The closed form
solves exact equality, and two curves that only meet at infinity have no exact root.

## 5. The search ceiling

`results/T1_beta_c_disagreement.json:group_A_search_ceiling`. It explains none of the 62:
bisection never searches an item whose selector returns `o*_0` (`.n_live`), and the
closed-form roots reach only `.max_closed_form_beta`, far below the ceiling.

## 6. Single-crossing

Intact on every item examined. No competitor leads `o*_0` beyond the band anywhere on the
grid, in any group, and the tie-broken argmax never returns to `o*_0` once it leaves.
Every raw sign change of the lead occurs at float-noise magnitude on numerically
identical curves. Spec section 6.3 Consequence 2 is not contradicted.

---

## 7. The bug and its fix, recorded and NOT applied

**The bug.** `adversary._crossings` tests the parallel case with an exact `den != 0`.
Spec section 6.3 gives the crossing equation "at most one root (none, if the coefficient
of `x` is zero and the two curves are not identical; the whole line, in the degenerate
case they are identical, which is not a crossing)". In float64, two identical curves do
not produce exact zeros; they produce two coefficients of rounding size, whose ratio is
arbitrary. The exact test lets that ratio through as a root.

**The fix, stated and not applied.** The spec's degenerate case applied in floating
point: treat a pair as identical, and therefore as not crossing, when both coefficients
fall below a floating-point tolerance. **The tolerance is not fixed here.** On the
disagreeing pairs both coefficients sit at or below `1e-15`, but this session did not
measure the coefficient distribution on genuinely crossing pairs, so it cannot show that
any threshold sits in an empty interval the way P2-D19's did. That measurement comes
before the fix. The closed form is the cross-check, not the value of record, so no
figure in the paper moves while it waits.

**A second closed-form limitation, recorded and not treated as the same bug.** The closed
form solves exact equality, while the spec's argmax is tie-broken. It cannot see the 136
flips of section 4. Matching them would mean solving for entry into D51's band with the
fit tie-break's direction, which is a change of criterion, not a float tolerance.

## 8. Recorded for the author, not ruled

**On 136 pool items, `beta_c` is a property of D51's tolerance, not of the game.** Group
B's 99 and the later-firing 37 flip where a gap converging to zero crosses `1e-9 + 1e-12`,
at `beta` in `results/T1_beta_c_disagreement.json:group_B_bisection_finite_closed_form_inf.bisection_beta_c_range`.
The winner never strictly beats `o*_0`; the Scientist is indifferent between them to nine
places, and the argmax moves to the higher-fit option. That is correct under spec section
6.2 and is the value of record. It means 99 of the pool's divergent items are divergent
only by tie-break. Whether that bears on any pool figure is the author's to decide; this
document does not rule it. The frozen 1,000 carries none of these
(`results/T1_beta_c_crosscheck.json:bases.frozen_1000.all.n_robust_classification_disagree`);
T6 recorded the same effect there at about `1e-16` on robust items only.

**Hypothesis H2 was checked and is not the cause.** Spec 6.3 Consequence 1 assumes
`o*_0` weakly leads every rival at `beta = 0`. Under D51's relative band a rival can sit
above `o*_0` and lose on fit, and `_crossings` does not check which way a root crosses. In
group A the competitor starts above `o*_0` on some items, but only at noise magnitude, so
no crossing in either direction is real. The gap in the proof's premise is latent here and
produced none of these disagreements.

## 9. Corrections to the instruction

- The monotonicity proof is spec section **6.3, Consequence 2**. Section 7.1 is the
  `beta = 0` boundary fix.
- The spec has no section labelled "edge case 1". The parallel case is in section 6.3's
  claim, quoted in section 7 above.
- The selection band is D51's `TAU_MAIN = 1e-9` relative plus `1e-12` absolute, not
  `EPS_TIE = 1e-12`. `EPS_TIE` is the right comparison for the coefficient magnitudes.

## 10. What this version changes

| | |
|---|---|
| `beta_c` value of record | unchanged: bisection |
| the 2,748 separating items, all inside the span guard | **stand** |
| Arm C | not re-ruled |
| `adversary._crossings` | unchanged; the fix is recorded, not applied |
| 136 pool items with tolerance-set `beta_c` | recorded for the author, not ruled |
