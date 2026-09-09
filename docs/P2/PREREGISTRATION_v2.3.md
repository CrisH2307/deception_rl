# PREREGISTRATION v2.3

**Paper 2: the adversary effect and the RL Scientist**

Version 2.3 · written 2026-09-09 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` and `v2.2`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
four are read together. This version settles the unit-of-analysis question `v2.2`
section 4 handed to T5, fixes the confirmatory item set, and re-examines section 8.2's
sample-size target. It does not reopen K1 or K2; both are settled and neither is
touched here.

**Data observed at the time of writing.** No Paper 2 model data of any kind. The
quantities in view are Arm A computations over frozen Paper 1 artifacts (`beta_c` and
its counts, `reports/T2_k2_gate.md` and `reports/T2_frozen_set_counts.md`) and Paper
1's own published decisions. `sigma` for `ΔA` remains unmeasured; see section 5.

| # | decision | where |
|---|---|---|
| 1 | Arm B's unit of analysis is **per tile**, `size` confirmatory. Pooling rejected. | §1, **P2-D3** |
| 2 | Not pooled, so no tile term. What reopening it would require is stated. | §2 |
| 3 | Confirmatory item set is **Paper 1's frozen 1,000**, `size` tile. Redraw variant (a) rejected outright; variant (b) undecided. | §3, **P2-D4** |
| 4 | Target re-examined. Its stated basis was wrong; its real basis survives, and the number does not move. | §4 |
| 5 | `sigma` still unmeasured. The target stays provisional and says so. | §5 |
| 6 | One decision needs a number that does not exist. Named, and stopped on. | §6 |

---

## 1. Arm B's unit of analysis: per tile, `size` confirmatory

**Decision. Arm B's confirmatory analysis is per tile, on the `size` tile alone.
Pooling across tiles with tile as a stratum is rejected.** This preserves v2.0 section
2 unchanged; the question was whether the counts justified departing from it, and they
do not.

### 1.1 Correcting the premise the question was put on

The handoff arrived with the reasoning that section 8.2's target "was set per-tile on
the `size` tile because `|O| = 6` made `size` the tile where the effect should be
strongest," and that the discrediting of `|O|` as a driver therefore undermines it.

**No governing record says that.** Traced to the source rather than to the document
that summarises it:

- **D49**, `.claude/rules/30-data-decisions.md` in the Paper 1 repository: "The top
  `fit_cost` decile is 90.9% `size`, so tile-balanced selection confounds tile with
  `fit_cost`: the low end of the curve would be `manmade`/`moves`/`hold` and the high
  end `size`. `size` spans the full range on its own." The basis is **`fit_cost` range
  coverage**.
- **D108**, same file: "`moves` is below its marginal null at all four rungs, residual
  position sensitivity, not content, and `hold` carries approximately nothing. **The
  primary curve rests on `size` alone.**" The basis is a **measured model-side
  result**.
- v2.0 section 2 cites exactly these two. Its only mention of `|O| = 6` is a stated
  *consequence* ("every item in the confirmatory set has `|O| = 6`, so the model's
  marginal over canonical option ids is a single six-vector"), not a motivation.
  Appendix A.1 gives the 400's basis as "Derived from the power curve at
  `sigma = 0.25`."

**What the `|O|` correction does reach.** Spec section 7.2's per-tile gate protocol,
which ordered tiles by `|O|` on the assumption that option count is the binding
structural constraint. That was corrected in `v2.1` section 2.2 and spec `v3.1`
section 7.2, and the correction is real. It does not reach v2.0 section 2 or section
8.2, which never rested on `|O|`.

The frozen set's near-flat finite-`beta_c` counts (114 / 122 / 116 / 108) are likewise
a fact about **availability of divergent items**, not about which tile carries model
signal. Availability was never the argument for `size`.

### 1.2 Why pooling is rejected

Three independent reasons; the first alone is sufficient.

1. **D108 is a measured negative result, and pooling would override it with nothing.**
   Paper 1 measured that `moves` sits below its own marginal null at all four rungs
   and `hold` carries approximately nothing. Pooling Arm B across tiles asserts those
   tiles carry the effect. Nothing measures that, and the one thing that does measure
   the adjacent question says the opposite. v2.0 section 2 states Paper 2 inherits
   D108; this document does not un-inherit it on a count of item availability.

2. **Pooling loses power rather than gaining it, under exactly the prior D108
   supplies.** The apparent gain is `n` from 108 to 460. But if only `size` carries
   the effect, the pooled mean `ΔA` is diluted to `f * delta_size` with
   `f = 108/460 = 0.235`, while `n` grows only by `1/f`. Required `n` scales as
   `1/delta^2`, so the requirement grows by `1/f^2` against a supply that grows by
   `1/f`:

   ```
   at the point where size-only is exactly powered, pooled is short by
   1/f = 4.26x
   ```

   This is generous to pooling: it assumes equal `sigma` on all four tiles, and D108
   attributes `moves`'s behaviour to residual position sensitivity, which is variance
   without signal.

3. **The marginal null does not pool across arities.** Section 3.3's null is
   `A_null(m,F) = sum_o p_{m,F}(o) * A_i(o)`, with `p_{m,F}` the model's own marginal
   over **canonical option ids**. With `|O| in {3,3,4,6}` there is no common option-id
   space: id 5 exists only on `size`. The null would have to be computed per tile and
   the excess would be a per-tile quantity, so the pooled test would be a stratified
   combination of per-tile estimates rather than a pooled estimate. v2.0 section 2
   already flagged this as a reason the confirmatory set is single-arity.

### 1.3 The ordering, carried verbatim

`v2.2` section 4 recorded this disclosure and required it travel with the decision
rather than stay behind:

> The argument that |O| is not the driver, and therefore that singling out the
> size tile is unmotivated, was established on 2026-09-09 from pool data
> (manmade 0.0387 vs moves 0.1790 at identical |O|=3) BEFORE the frozen-set
> counts were run. The counts subsequently showed pooled finite-beta_c = 460
> (clears the 400 target) and size-tile = 108 (cannot clear it from a
> 250-item tile at any selection rule). Both facts are on the record. A
> pooled primary is therefore chosen with knowledge that it passes, and that
> is disclosed rather than finessed.

**Its final sentence is now counterfactual, and that is worth stating plainly rather
than editing the paragraph.** The paragraph was written to disclose a hazard: choosing
a unit of analysis because it is the one that clears the target. The decision went the
other way. `size`-only was chosen at `n = 108`, which does **not** clear 400, over a
pooled primary at `n = 460`, which does. The hazard the disclosure guards against did
not materialise, in the direction that would have been self-serving. The paragraph is
carried unchanged because a disclosure edited after the fact to match the outcome is
worth nothing, and because a future reader is entitled to see that the pooled option
was known to pass at the moment it was declined.

---

## 2. How tile would enter, if pooling were ever reopened

Not applicable to this design: there is no pooled model and therefore no tile term.
Recorded so a later session reopening the question starts from the requirements rather
than from scratch. Reopening would need all four:

1. **A measurement that displaces D108 on Arm B's coordinate.** D108 is on Paper 1's
   consistency coordinate. Whether `manmade`, `moves` and `hold` carry signal on `ΔA`
   is unmeasured. That measurement is available from Arm B's own secondary tiles once
   F0/F1/F2 are scored, and it is **exploratory** (v2.0 section 10), so it can inform
   a future paper's design but cannot be used to re-choose this paper's confirmatory
   set after seeing it.
2. **A stratified estimator, not a pooled mean.** Tile enters as a fixed stratum with
   per-tile marginal nulls and per-tile excess, combined with weights fixed in
   advance. Item-level random effects across tiles are not admissible while the null
   is per-tile.
3. **A statement of how the four tiles' differing finite-`beta_c` rates are handled.**
   The rates (0.4560 / 0.4880 / 0.4640 / 0.4320 on the frozen set) are close enough
   that weighting by them is nearly uniform; the real inequality is in effect size,
   not availability, and weights set from availability would be the wrong axis.
4. **A recomputed family.** The 21-test family in section 8.1 is per model and framing
   contrast, not per tile, so pooling does not change the family. Adding the three
   secondary tiles as separate confirmatory tests would take the family to 84 and
   `alpha` to `0.05/84`, which is a different design.

---

## 3. Confirmatory item set: Paper 1's frozen 1,000

**Decision. Arm B's confirmatory analysis set is the `size` tile of Paper 1's frozen
`items_final.parquet`, restricted to items with finite `beta_c`: 108 items.** No new
draw is authorized by this document.

### 3.1 Redraw variant (a), uniform ~871 per tile, is rejected outright

This needs no unmeasured quantity to decide. Under a `size`-only confirmatory set,
variant (a) buys **nothing confirmatory** that a `size`-only enlargement would not,
and costs 2,561 additional items on the three tiles D108 identifies as carrying
approximately nothing. It is dominated by variant (b) on its own terms.

Its two further costs are recorded because they would otherwise have to be
rediscovered. `manmade` would sit at 69% of its qualifying conflict items at the point
estimate and 79% at the interval's upper end, against 7% or less on the other three
(`reports/T2_frozen_set_counts.md` section 5), so that tile's estimate would be close
to a population value while the other three remain samples. That is not a defect but
it would have to be stated in every sentence comparing them. And P1's equal-count
within-conflict `fit_cost` deciles are what keep it fillable at all.

### 3.2 Variant (b), enlarging `size` only, is not decided here

Variant (b) is the correct **shape** for a redraw under a `size`-only confirmatory set:
enlarge the tile the confirmatory analysis uses, leave the others at Paper 1's 250 for
secondary reporting. Its **size** cannot be fixed, because the quantity that would fix
it does not exist. See section 6.

Note for whoever takes it up: the deviation from Paper 1's recipe that variant (b)
involves is unequal per-tile `N`, not any reference to `beta_c`. Both variants size
`N` from the measured finite-`beta_c` rates, which is an ordinary power calculation
over the outcome's prevalence and is not selection on the dependent variable
(`v2.2` section 1.3). Equal per-tile `N` is what Paper 1's `final_items.py` fixes, and
that is what (b) breaks.

### 3.3 What adopting the frozen set costs

Stated rather than buried, since this is the option that was chosen:

- **`n = 108`, which covers `sigma <= 0.134`** on section 8.2's own curve
  (`n = 6020 * sigma^2` at `delta = 0.05`, `alpha = 0.05/21`, 80% power). That sits at
  the optimistic end of the range section 8.2 itself tabulates, 0.10 to 0.40. **If
  `sigma` exceeds 0.134 the confirmatory test is underpowered against its own SESOI**,
  and that is reported as realized power, not repaired after the fact.
- The `beta_c = infinity` control set (section 4.4) is the same tile's 142 remaining
  items, so control and analysis sets stay comparable on `|O|` as section 8.2 requires.

What it buys: no new artifact, no new manifest, gates or hashes, and an exact rather
than approximate comparison to a published Paper 1 result on the identical items. It
also commits nothing that a later enlargement would invalidate, since an enlarged
`size` tile drawn under Paper 1's recipe is a superset in distribution, not a
replacement.

---

## 4. Section 8.2's target, re-examined

**Outcome: the number does not move. Its stated motivation was wrong, its actual basis
is untouched, and re-deriving it for the chosen unit of analysis returns the same
value.**

The target was examined rather than carried forward, as directed. What it rests on:

```
n = (z_{alpha/2} + z_{0.20})^2 * sigma^2 / delta^2  =  15.05 * sigma^2 / delta^2
  = 6020 * sigma^2                                     at delta = 0.05
sigma = 0.25  ->  n = 376.25  ->  377, stated in section 8.2's table, rounded to 400
```

Every input is unchanged by anything in this document or in `v2.1` and `v2.2`:
`alpha = 0.05/21` follows from seven models by three framing contrasts (section 8.1),
neither of which moved; `delta = 0.05` is D74's SESOI, carried on the argument that `A`
and `post_norm` share a scale and a pinned-pole construction; `sigma = 0.25` is an
assumption, not a measurement. **`|O|` appears nowhere in the derivation**, so the
`|O|` correction cannot move it.

The unit of analysis is unchanged at `size`-tile-per-tile, so the target is also
unchanged in **kind**: it remains a per-tile count on `size`, not a pooled count. Had
pooling been adopted, the target would have had to be re-derived against the diluted
effect size of section 1.2, giving roughly `1/f^2` times the size-only requirement
rather than the naive `n = 460` supply, which is a further reason pooling was not the
cheap win it appeared to be.

**What does change is the target's role.** With no redraw authorized, 400 is no longer
a delivery requirement on T2. It becomes the benchmark against which the adopted set is
reported: 108 of 400, covering `sigma <= 0.134` rather than `sigma <= 0.25`. The
shortfall is carried as a stated limitation under section 11, not absorbed by moving
the SESOI, which is D74's and is not Paper 2's to relax.

---

## 5. `sigma` for `ΔA` is still unmeasured

**Confirmed. It is unmeasured, and the target is provisional and says so.**

No Paper 2 model data exists. `ΔA` is a new coordinate: it is a difference between
framings on a normalized margin axis, and no framing has been scored. Section 8.2's
table is a curve over an assumption, and every count in this document that depends on
it inherits that status.

Section 8.2's commitment is unchanged and is restated here so it is not lost across
four files: `sigma` becomes estimable from the **F0 condition alone**, which spends no
confirmatory alpha because no contrast in section 4.1 involves F0 alone, and realized
power is reported at that point.

---

## 6. The number that does not exist, and what stops on it

**Missing: `sigma`, the per-item standard deviation of `ΔA`.**

It gates exactly one open decision: **whether a `size`-tile enlargement (variant (b))
is needed, and if so how large.** That decision is **not made here**, and no
enlargement is designed, sized, or scheduled. Sizing a draw against an assumed `sigma`
is designing around a missing quantity.

Everything else in this document was decidable without it, and was decided: the unit of
analysis (section 1) turns on D108 and on arity, not on `sigma`; variant (a)'s
rejection (section 3.1) is a dominance argument that holds at every `sigma`; the
target's derivation (section 4) is unchanged at every `sigma`.

**The admissible route to the number, for the author, not taken here.** Paper 1 scored
two conditions differing by a single inserted sentence in the same `{extra}` slot that
P2-D2 puts the framing block in: condition 4 (`base`) and condition 5 (D64's `c5`
insert). The per-item difference in `post_norm` between those two conditions is the
closest available empirical analogue to `sigma` for `ΔA`, on the same coordinate family
and the same prompt perturbation geometry. It is a **prior, not a measurement**: it is
Paper 1's coordinate, not `A`, and its perturbation is not an adversary framing.

It is named and not computed. Computing it inside the session that would use it to size
a draw is how a prior becomes a target, and the instruction to stop rather than design
around a missing quantity is the reason to leave it to an explicit author decision.

---

## 7. What this amendment does not do

- It does not reopen K1 or K2. Both are settled and neither is referenced as live.
- It does not authorize any new item draw, of any size or shape.
- It does not relax D74's SESOI, change `alpha`, or change the 21-test family.
- It does not un-inherit D49, D105 or D108, and it does not promote any secondary tile
  to confirmatory.
- It does not edit `v2.0`, `v2.1` or `v2.2` in place, and it does not amend the
  ordering paragraph in section 1.3 to match the decision that followed it.
