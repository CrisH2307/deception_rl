# PREREGISTRATION v2.4

**Paper 2: the adversary effect and the RL Scientist**

Version 2.4 · written 2026-09-10 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1`, `v2.2` and `v2.3`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
five are read together. This version rules on the **two open Arm B questions** T6
routed here, and on nothing else. It does not reopen K1 or K2, does not authorize
any item draw, and does not touch Arm A or Arm C.

**Data observed at the time of writing.** No Paper 2 model data of any kind. Two
new bodies of evidence are in view, both of them reads of frozen Paper 1 artifacts:

1. **F0 positions on the `A` axis**, from P1's frozen `cond4`
   (`reports/T6_F0_headroom.md`). This is model output, but it is Paper 1's, under
   the condition F0 replicates, and no Paper 2 framing has been rendered or scored.
2. **The geometry of the `A` coordinate**, computed from the frozen item set with
   no model choice of any kind.

`sigma` for `ΔA` remains unmeasured. Section 3 changes what that costs.

| # | decision | where |
|---|---|---|
| 1 | The `A` level confound is real, unfixable, and already handled by the contrast. Design unchanged; an interpretive prohibition is added. | §1, **P2-D5** |
| 2 | Mean `ΔA` is **not** the confirmatory statistic. Tie rate plus a sign test replaces it. | §2, **P2-D6** |
| 3 | What P2-D6 costs, what it does not buy, and the one thing it makes worse. | §3 |
| 4 | What is still open, and what is deliberately not decided here. | §4 |

---

## 1. The `A` level confound: design unchanged, one prohibition added

**Decision. No change to the item set, the coordinate, or the analysis set. Raw `A`
under a single framing is prohibited as evidence of adversary tracking, and that
prohibition is written into the interpretation rules rather than left to judgement.**

### 1.1 What was measured

T6 measured that `o*_infinity` is Paper 1's `o_fit` on 452 of 460 divergent items in
the frozen set and 92.5% of the pool. Arm B's target therefore sits on Paper 1's
salience pole. Two consequences follow, and only one was ever a threat:

- **The level is confounded.** A model sitting at `o*_infinity` is not thereby
  tracking the adversary; it is doing the salience-driven thing Paper 1 documented.
- **The contrast is not.** Salience-driven behaviour is constant across framings and
  cancels in `F1 - F0` and `F2 - F0`. v2.0 section 4 already makes the primary
  measure a contrast.

The residual risk was **power**: if models sat at or past `A = 1` under F0 there
would be no headroom, and H-B's "little or no movement" would be confirmed by a
ceiling. A prediction confirmed by a ceiling carries no evidence.

**Measured, and the ceiling is absent** (`reports/T6_F0_headroom.md`). On the
460-item divergence set, `pmi`/`template`: `A >= 1` on 0.0174 to 0.1870 across the
seven-model ladder, median `A` at or below zero for all seven, median headroom 1.0
to 1.9. There is no saturation, so a null cannot be produced by one.

### 1.2 Why the two remedies are rejected

**Restricting the primary analysis to items with F0 headroom is rejected.** `ΔA` is
`A(F1) - A(F0)`, so F0 headroom is a function of one term of the outcome.
Conditioning the analysis set on it is selection on the dependent variable in the
form `v2.2` section 1.3 prohibits, and the prohibition does not weaken because the
selection is on a component rather than the whole. It is also unnecessary: the
condition it would protect against is measured absent.

**Adding a second, non-salience-confounded coordinate is rejected.** It would be a
new preregistered quantity chosen after F0 positions were seen. Its selection is a
researcher degree of freedom with no prior provenance, which is exactly what the
existing coordinate has (v2.0 section 3.1, P1's D47) and a new one would not.

### 1.3 What is added instead

The confound is real and permanent, so it is handled where it bites, in
interpretation:

> **No claim that a model carries adversary-relevant content may rest on `A` under a
> single framing.** Every such claim is made on a framing contrast, and on **excess
> over the marginal null** (v2.0 section 3.3), never on raw `A`. A model at `A = 1`
> under F0 is reporting salience, not adversary awareness.

This restates a commitment v2.0 section 3.3 already makes ("any claim that a model
carries adversary-relevant content is made on excess, never on raw `A`") and makes
it binding on the level specifically, which is the form the confound takes. The
supporting evidence is on the record: under F0 the share of renderings landing on
`o*_0` runs 0.2739 to 0.4228 against a chance rate of 0.2732, so **a point mass at
`A = 0` is likewise not evidence of Bayes-optimal behaviour.**

### 1.4 The limitation, stated as it will appear

`A`'s zero and one are the Bayes and salience poles of Paper 1's own frontier. Arm B
therefore measures movement along an axis whose endpoints Paper 1 has already shown
language models do not respect at the level. What Arm B can establish is whether the
**framing** moves a model along it. What it cannot establish, on any item set, is
whether a model's position on that axis reflects adversary reasoning rather than
salience. That is a property of the signal space, not of the sample, and no
enlargement fixes it.

---

## 2. Mean `ΔA` is not the confirmatory statistic. **P2-D6**

**Decision. Arm B's confirmatory instrument is (i) the tie rate, the share of
analysis-set items with `ΔA` exactly zero, reported directly, and (ii) an exact
two-sided sign test on the remaining items against `p0 = 0.5`. Mean `ΔA` is demoted
to a reported descriptive quantity. The median of per-item `ΔA` is retained, as v2.0
section 3.2 already requires.**

### 2.1 The strongest ground first: this extends a commitment already made

v2.0 section 3.2 does not treat `A`'s aggregation as open. It requires two
aggregates for every cell, "the **median of per-item values**, and the value
computed **from the means**", and gives its own reason:

> A mean of per-item ratios is not usable when the per-item denominator approaches
> zero, and Paper 1 measured that failure directly.

with the `ext_i >= 0.02` floor of section 6 carried over as "the same guard", and
provenance traced to P1's `src/frontier_position.py`, which handles the identical
pathology.

**So the pathology was named before any Paper 2 data existed, the median was already
mandated as the response to it, and P2-D6 extends that response rather than
introducing one.** What is new is only the magnitude, and that the mixture is
three-way rather than a single heavy tail.

### 2.2 What is new: the mean estimates something other than the effect

Measured from the frozen item geometry over every admissible option pair, with no
observed choice of any kind (`results/T6_F0_headroom.json`, `delta_A_leverage`).
`A` is near-trichotomous on the divergence set:

| region | option-cells | `A` |
|---|---:|---|
| `o*_0`, the Bayes pole | 470 | exactly 0 |
| `o*_infinity`, the salience pole | 439 | exactly 1 |
| everything else | 841 | median **-3.329**, unbounded below |

Off-pole cells (841) nearly match pole cells (909), so off-pole is the common case,
not a tail. Over the 6,048 ordered option pairs the coordinate admits:

| move kind | share | median `\|ΔA\|` | p90 | max |
|---|---:|---:|---:|---:|
| pole to pole | 0.1521 | 1.000 | 1.0 | 1.0 |
| mixed | 0.5952 | 3.763 | 16.2 | 4,777.9 |
| off to off | 0.2526 | 2.467 | 12.8 | 2,515.6 |

The target move `o*_0 -> o*_infinity` is `ΔA = +1` exactly, on all 460 divergent
items. **0.7004** of admissible moves exceed it in magnitude; **0.1518** exceed it
tenfold. A move of magnitude `|ΔA|` carries the weight of `|ΔA|` target moves in a
mean, so one item moving to a far off-pole option outweighs ten items making the
exact move Arm B exists to detect.

**Accepting the mean with the mixture as a stated limitation is therefore rejected,
and rejected as contradicted rather than disfavoured.** A limitation statement is
the right instrument when an estimator is unbiased but noisy, or when a tail
occasionally distorts it. Neither holds. The distortion is the typical case, not a
tail; and a three-way mixture with unbounded components means the mean's expectation
is a different quantity, not the effect plus noise. A limitation cannot repair an
estimator that is not estimating the effect.

**This matters most because H-B predicts a null.** A heavy-tailed estimator widens
the interval, which makes a null easier to obtain. Under the original design, "the
interval on mean `ΔA` contains zero" could have been satisfied by the estimator
rather than by the models, which is the same failure mode as the ceiling in section
1 and is not repaired by disclosing it.

### 2.3 Why the sign, and not the pole-to-pole restriction

Restricting to pole-to-pole transitions measures exactly the event of interest at
`ΔA in {0, +1, -1}` and shares P2-D6's provenance. It was not chosen for two
reasons:

1. It discards 0.8479 of admissible moves, and it requires a **new rule** for what a
   pole/off-pole move counts as. That rule has no prior provenance and would be
   fixed after the geometry was seen, which is the objection this document raises
   against a new coordinate in section 1.2.
2. The sign is interpretable on **every** move, including off-pole to off-pole:
   `ΔA > 0` means the model moved up on normalized margin, toward `o*_infinity`.
   It is the **magnitude** that the mixture corrupts, not the direction. Discarding
   items to recover an uncorrupted magnitude gives up coverage to fix a quantity the
   sign does not need.

### 2.4 The instrument, stated precisely

For each analysis-set item `i` and framing contrast, with `ΔA_i` per v2.0 section 4:

```
tie          ΔA_i == 0 exactly
tie rate     |{ i : ΔA_i == 0 }| / n            REPORTED, primary
sign test    among { i : ΔA_i != 0 }, exact two-sided binomial on
             |{ i : ΔA_i > 0 }| against p0 = 0.5, at alpha = 0.05/21
```

`alpha`, the 21-test family and the `size`-tile analysis set are unchanged (v2.0
section 8.1, v2.3 section 3). Mean `ΔA`, the value from the means, and the median
are all still reported for every cell, so this document's change is auditable
against the original design rather than replacing it silently.

**H-B resolves on both parts together.** No movement appears as a high tie rate.
Movement that is not adversary-directed appears as a tie rate below 1 with the sign
proportion near 0.5. Adversary tracking appears as a sign proportion above 0.5. The
three are distinguishable, which mean `ΔA` did not make them.

---

## 3. What P2-D6 costs, and the one thing it makes worse

Recorded so none of it has to be rediscovered, and because two of the three are
costs rather than gains.

### 3.1 The SESOI does not translate, and none is invented

D74's `delta = 0.05` is a SESOI on **mean `ΔA`**. It does not carry to a proportion
without a distributional assumption, and no substitute is invented here. The
confirmatory test is against `p0 = 0.5`, which is well posed with no SESOI; a SESOI
would enter only for power, and **realized power at the observed effective `n` is
reported instead**. D74 is Paper 1's and is neither relaxed nor reinterpreted.

### 3.2 `sigma` no longer gates the confirmatory test, and one unknown is exchanged for another

Power for a sign test is exact-binomial in the effective `n` and the alternative
proportion. **`sigma` enters nowhere.** v2.0 section 8.2's
`n = 15.05 * sigma^2 / delta^2` sizes a mean and no longer governs the primary
analysis; it still governs the mean, which is now descriptive.

This is **not** a free saving. It exchanges `sigma` for the **tie rate**, which is
also unmeasured. The exchange is recorded honestly:

| | `sigma` | tie rate |
|---|---|---|
| range | unbounded above | bounded in `[0, 1]` |
| how obtained | estimated, with error | observed exactly once F1 or F2 is scored |
| effect on power | through `n = C sigma^2` | monotone, exactly computable |

Emitted by `src/sign_power.py` into `results/T5_sign_power.json`, at
`alpha = 0.002381` two-sided and `n = 108` (v2.3 section 3):

| tie rate | effective `n` | power at `p1 = 0.65` | at `0.70` | at `0.75` | `p1` at 80% power |
|---:|---:|---:|---:|---:|---:|
| 0% | 108 | 0.480 | 0.858 | 0.988 | 0.691 |
| 15% | 92 | 0.443 | 0.813 | 0.977 | 0.698 |
| 30% | 76 | 0.310 | 0.670 | 0.925 | 0.721 |
| 50% | 54 | 0.166 | 0.425 | 0.740 | 0.762 |
| 70% | 32 | 0.082 | 0.212 | 0.432 | 0.822 |

### 3.3 The thing this makes worse, stated plainly

**A high tie rate is the outcome H-B predicts, and ties carry no sign. So the sign
test has least power exactly in the state of the world where the null is true.**

That is a real defect and it is not argued away. It is handled by making the tie
rate a **primary reported quantity in its own right** rather than treating it as
attrition: "no movement" is answered by the tie rate directly, as a rate with an
exact interval, and the sign test answers only the narrower question "among the
items that moved, did they move toward the adversary optimum". A design that
reported only the sign test would be able to confirm H-B by running out of data,
which is the failure this document rejects in sections 1 and 2.

Note also the coherence with section 1: under the level confound, a purely
salience-driven item produces `ΔA = 0` and lands in the tie rate, where it is
counted and visible, rather than contributing a spurious signed magnitude.

---

## 4. What is not decided here

- **Redraw variant (b), enlarging the `size` tile.** **DECLINED by author decision
  on 2026-09-10, P2-D7, `PREREGISTRATION_v2.5.md` section 1.** It is no longer open.
  When this section was written it was still an open author decision, for the reason
  recorded here: v2.3 section 6 gated it on `sigma`, and section 3.2 above removes
  `sigma` from the confirmatory power curve, so the stated blocker moved rather than
  cleared, since sizing an enlargement now requires a target tie rate that is equally
  unmeasured. P2-D7 closes it on exactly that ground: there is no new quantity to
  authorize an enlargement on. Arm B runs at `n = 108` with realized power reported.
- **K1 and K2.** Settled. Neither is referenced as live.
- **Arm A and Arm C.** Untouched.
- **The 21-test family, `alpha`, and D74's SESOI on the mean.** Unchanged.
- **The CTRL residual finding** (`reports/T6_F0_headroom.md`): one of fourteen
  comparisons survives Bonferroni, on the cross-family control, worth about four
  renderings of 878, with a named alternative explanation that this design cannot
  distinguish from an adversary residual. It is a reported F0 observation and it
  changes no rule here.

## 5. Ordering, disclosed

Both questions were measured before any remedy was proposed, and no remedy was
proposed in the session that measured them. No Paper 2 model data of any kind
exists. The `A` geometry in section 2.2 admits every option pair rather than any
observed choice, so nothing in it could have been selected to favour an outcome.
Section 3.2's leverage figures and section 2.1's `post_norm` commitment both predate
this document: the first is a property of the frozen item set, the second is v2.0's
own text.

The F0 positions in section 1.1 **are** model output. They are Paper 1's, under the
condition F0 replicates, and they were read to answer whether a ceiling existed, not
to choose a statistic. P2-D6 rests on the item geometry, which is model-free; the F0
positions bear only on section 1, where they **removed** a reason to change the
design rather than supplying one.
