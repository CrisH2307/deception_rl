# PREREGISTRATION v2.2

**Paper 2: the adversary effect and the RL Scientist**

Version 2.2 · written 2026-09-09 · amends `PREREGISTRATION_v2.md` (v2.0) and
follows `PREREGISTRATION_v2.1.md`.

Written as a separate file per Paper 1's **D148**: earlier versions are never edited
in place, and they are read together. This version **records the outcome of a
preregistered kill gate and applies its preregistered consequence.** It changes no
threshold, no hypothesis and no analysis rule. Sections 2 and 3 are descriptive or a
disclosed defect and neither overrides section 1. Section 4 hands an open
unit-of-analysis question to T5 without deciding it.

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

**Scope of the prohibition, fixed here so it is not over-applied.** It bites on a new
draw that reaches for finite `beta_c` deliberately. It does not bite on the frozen
set's existing enrichment, whose finite-`beta_c` rate is 0.4600 against the pool's
0.1823. That enrichment is **benign**, for two independent reasons, either sufficient:

1. **Provenance.** Nothing in the frozen set was chosen with any knowledge of
   `beta_c`, which did not exist as a quantity when the set was drawn. The gap is
   fully accounted for by P1's 50% conflict quota
   (`0.50 * 0.9040 + 0.50 * 0.0160 = 0.4600`), fixed for P1's own reasons in
   `final_items.py` Step 5.
2. **Estimand.** Selection on the dependent variable corrupts a **prevalence**
   estimate. Prevalence is Arm A's question and Arm A measures it on the 200,000
   candidate pool, not on the item set (section 7.1; T6 Step 1). Arm B measures
   **movement within** the divergence set, conditional on membership, where
   enrichment costs the estimate nothing and buys it power.

It follows that a larger draw under P1's own recipe is also outside the prohibition,
since that recipe references `beta_c` nowhere. This paragraph records the enrichment
as benign; it is **not** a defect and must not be carried as one.

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

## 4. Handoff to T5: the unit of analysis for Arm B. Not decided here.

**The question.** Is Arm B's primary analysis **per tile**, or **pooled across tiles
with tile as a stratum**? This is a unit-of-analysis question, it belongs in the
preregistration, and it is handed to T5 rather than settled by the session that
produced the counts that bear on it.

**The two live paths.**

1. **Reuse P1's frozen 1,000-item set with a pooled primary.** Available now, no new
   draw, no new artifact, and the Paper 1 comparison is exact rather than merely
   preserved. The frozen set carries 460 finite-`beta_c` items pooled, 108 on the
   `size` tile.
2. **A larger redraw under P1's own recipe** (`final_items.py` Step 5: 50/50
   conflict/non-conflict per tile, `fit_cost` deciles on the conflict half,
   `decision_margin` deciles on the non-conflict half). This path is
   **pre-authorized** by section 1.3's "a larger sample drawn without reference to
   `beta_c`": the recipe references `beta_c` nowhere. Projected cost, arithmetic in
   `reports/T2_frozen_set_counts.md` section 5: **3,487 items, roughly 871 per
   tile**, to put 400 finite-`beta_c` items on every tile. Every tile is feasible
   against P1's own selection gates; `manmade` is the binding one at 69% of its
   qualifying conflict items.

**The ordering, recorded verbatim so the choice is disclosed rather than finessed:**

> The argument that |O| is not the driver, and therefore that singling out the
> size tile is unmotivated, was established on 2026-09-09 from pool data
> (manmade 0.0387 vs moves 0.1790 at identical |O|=3) BEFORE the frozen-set
> counts were run. The counts subsequently showed pooled finite-beta_c = 460
> (clears the 400 target) and size-tile = 108 (cannot clear it from a
> 250-item tile at any selection rule). Both facts are on the record. A
> pooled primary is therefore chosen with knowledge that it passes, and that
> is disclosed rather than finessed.

**Neither path is adopted here.** Section 8.2's 400 remains provisional in either
case: it rests on a `sigma` nothing has measured, and section 8.2's own commitment to
report realized power once `sigma` is estimable from `F0` is unchanged by anything in
this document.

---

## 5. What this amendment does not do

- It does not change K1, K2, K3, any threshold, any hypothesis, or any exclusion rule.
- It does not override the fired gate, in any form, on any subset statistic.
- It does not adopt a fallback sample, and it does not choose between section 4's
  two paths. Section 1.1 records only that the redraw does not happen and that the
  pre-specified fallback is the frozen set; the fallback's own design, and Arm B's
  unit of analysis, are T5's decisions.
- It does not record the frozen set's finite-`beta_c` enrichment as a defect. Section
  1.3 records it as benign, with both reasons.
- It does not relieve T6 of running K1 and emitting the gate record.
