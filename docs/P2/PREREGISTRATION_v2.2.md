# PREREGISTRATION v2.2

**Paper 2: the adversary effect and the RL Scientist**

Version 2.2 · written 2026-09-09 · amends `PREREGISTRATION_v2.md` (v2.0) and
follows `PREREGISTRATION_v2.1.md`.

Written as a separate file per Paper 1's **D148**: earlier versions are never edited
in place, and they are read together. This version **records the outcome of a
preregistered kill gate and applies its preregistered consequence.** It changes no
threshold, no hypothesis and no analysis rule. Everything below in sections 2 and 3
is descriptive or a disclosed defect; neither overrides section 1.

---

## 1. K2 fired. The `beta_c`-stratified redraw does not happen.

T2 Step 1, run on 2026-09-09 over the full 200,000-candidate pool, before any
stratification was designed.

```
K2 statistic  rho_Spearman(beta_c, fit_cost) = -0.9036
threshold     |rho| >= 0.80   (v2.0 section 7.1, fixed before any data)
item base     full candidate pool, N = 200,000, beta_c = infinity ranked at the
              maximum, tied at the top
outcome       FIRES
```

Emitted by `src/k2_gate.py`; full report in `reports/T2_k2_gate.md`. Deterministic,
no seed enters either variable.

### 1.1 The consequence applied

v2.0 section 7.1: "If K2 fires, the finding is reported prominently and Wave 2 stops
for an author decision. It is not resolved by re-picking the stratification variable
inside the same session."

**Applied, narrowly: D2's `beta_c`-stratified redraw does not happen.** The T2
session that produced the number designed no bins, set no quotas, drew no sample and
wrote no item file. The pre-specified fallback is reuse of Paper 1's frozen
1,000-item set, `items_final.parquet`.

### 1.2 Ordering, which is what gives the number its standing

K2's threshold (`0.80`) and its operationalization (Spearman over the full pool with
infinity ranked at the top) were both fixed in v2.0, before any P2 measurement of
either variable existed. The T2 brief was amended on 2026-09-09, **before the
statistic was computed**, to move K2 to the front of the task and require it be
reported before any stratification design existed. That reordering was explicitly
not a threshold change. The number arrived into a rule that was already written.

### 1.3 Ruled out before the fallback counts were measured

Fixed here, in advance of the counts in `reports/T2_frozen_set_counts.md`:

> **No fallback sample may select items because they have finite `beta_c`.**

That is selection on the dependent variable: Arm B's confirmatory analysis set is
defined by finite `beta_c` (v2.0 section 3.2), so enriching a draw for it would
manufacture the contrast the test is supposed to measure. If a count falls short of
section 8.2's provisional target, the admissible responses are a larger sample drawn
without reference to `beta_c`, or a stated power limitation. Never a
`beta_c`-enriched set.

Reuse of the frozen set is not selection on `beta_c`: nothing in that set was chosen
with any knowledge of the quantity, which did not exist when the set was drawn. Its
finite-`beta_c` rate of 0.4600 against the pool's 0.1823 is fully accounted for by
P1's 50% conflict quota (`0.50 * 0.9040 + 0.50 * 0.0160 = 0.4600`), a quota fixed for
P1's own reasons in `final_items.py` Step 5.

---

## 2. Diagnosis of the coefficient. Descriptive, and explicitly not grounds to override.

Recorded so a reader can see what the number is made of. **None of this changes the
outcome in section 1, and none of it is offered as a reason to revisit it.**

The pooled coefficient is driven by two coinciding tie blocks:

| block | N | share of pool |
|---|---:|---:|
| `beta_c = infinity`, tied at the rank maximum | 163,536 | 81.77% |
| `fit_cost = 0`, one midrank block at the bottom | 162,694 | 81.35% |
| both at once | 159,912 | 79.96% |

Related statistics, none of them the gate:

| statistic | value |
|---|---:|
| pooled Spearman (**the gate**) | **-0.9036** |
| Pearson on the finite-`beta_c` subset (v2.0 section 7.1's named secondary) | -0.3441 |
| Spearman on conflict items only (`fit_cost > 0`) | -0.4784 |
| per-tile Spearman, range across the four tiles | -0.8697 to -0.9257 |

A gate specified on the pooled statistic fires on the pooled statistic. That the
subset numbers are smaller is a fact about tie structure, not a competing reading:
adopting a subset statistic now, after seeing that it is smaller, would be choosing
the gate rule after seeing the number, which v2.1 section 1.1 already declined to do
once for K1 and declines again here.

---

## 3. Specification defect in K2 as written. Disclosed, not acted on.

**The defect.** K2 is specified over the pooled full pool. P1 never stratified on
that base: `final_items.py` Step 5 cuts `fit_cost` deciles over **conflict items
only** and stratifies the non-conflict half on `decision_margin` instead. So the base
K2 measures and the base P1's draw actually used are different sets, and K2's premise
that "stratifying on one is stratifying on the other" is evaluated on a base where
`fit_cost` is identically zero for 81.35% of items and therefore stratifies nothing.

**Found after the number.** This was noticed by the T2 session while reporting the
fired gate, not before. That ordering is why it is recorded rather than applied.

**Not acted on, and the outcome stands.** Three reasons, each sufficient. The
preregistered rule names the pooled statistic and the pooled statistic fired.
Amending a gate's base after seeing that the amendment would reverse the outcome is
the precise move `CLAUDE.md` forbids. And the outcome K2 protects against is not
obviously wrong on the conflict base either: at -0.4784 the two variables are still
substantially related, so a redraw stratified on `beta_c` would still be partly a
redraw stratified on `fit_cost`.

**What a future document may do with this.** Nothing in this study. If a later paper
re-specifies a K2-like gate, it should name its base explicitly and match it to the
base the comparison design actually uses. That is a note for a future
preregistration, written before its data, not a repair to this one.

---

## 4. What this amendment does not do

- It does not change K1, K2, K3, any threshold, any hypothesis, or any exclusion rule.
- It does not override the fired gate, in any form, on any subset statistic.
- It does not adopt a fallback sample. Section 1.1 records only that the redraw does
  not happen and that the pre-specified fallback is the frozen set; the fallback's
  own design is a separate decision, taken outside the session that produced the
  counts.
- It does not relieve T6 of running K1 and emitting the gate record.
