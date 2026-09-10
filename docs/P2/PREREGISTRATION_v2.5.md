# PREREGISTRATION v2.5

**Paper 2: the adversary effect and the RL Scientist**

Version 2.5 · written 2026-09-10 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1`, `v2.2`, `v2.3` and `v2.4`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
six are read together. This version closes the redraw question with an author
decision, and gives the tie rate the decision rule and reference it lacked. It does
not reopen K1 or K2, does not change `alpha` or the confirmatory item set, and does
not touch Arm A or Arm C.

**Data observed at the time of writing.** No Paper 2 model data of any kind. Section
2 adds one new body of evidence, and it is a read of frozen Paper 1 output: the
same-option rates between Paper 1's own conditions and permutations, computed by
`src/tie_reference.py` into `results/T5_tie_reference.json`. Those numbers are
written into this document as fixed reference values **before T7 runs**, so T7 does
not compute its own comparator.

| # | decision | where |
|---|---|---|
| 1 | Redraw variant (b) is **declined**, not deferred. Arm B runs on `n = 108`. | §1, **P2-D7** |
| 2 | The tie rate gets a reference, a threshold, and an outcome table. | §2, **P2-D8** |
| 3 | `ΔA = 0` is not the same event as "same option", and the gap is measured. | §3 |

---

## 1. Redraw variant (b) is declined. **P2-D7**

**Author decision, taken 2026-09-10. Not a deferral and not a stop on a missing
quantity.**

v2.3 section 6 left variant (b), enlarging the `size` tile, gated on `sigma` for
`ΔA`. v2.4 section 3.2 removed `sigma` from the confirmatory power curve by making
the instrument a sign test, whose power is exact-binomial in the effective `n` and
the alternative proportion. That did not clear the gate, it **moved** it: sizing an
enlargement now requires a target tie rate, which is equally unmeasured.

**Decision.** There is no new quantity to authorize an enlargement on, so it is
declined rather than left open. Arm B runs on Paper 1's frozen 1,000, `size`-tile
analysis set, `n = 108`, with **realized power reported rather than assumed**.

The `sigma` analogue in `reports/T5_sigma_prior.md` does not change this and is not
treated as if it did: it is a prior over a different manipulation (D64's `c5`
insert) on a different coordinate (`post_norm`), and its own report says so. It is
not a measurement of `sigma` for `ΔA`, and under P2-D6 the confirmatory test does
not use `sigma` at all.

**What this costs, stated rather than absorbed.** `n = 108` against section 8.2's
benchmark of 400. Under P2-D6 that benchmark no longer governs the confirmatory
test, but the shortfall in *information* is real and does not disappear because the
statistic changed: at a 30% tie rate the sign test reaches 80% power only at
`p1 = 0.721` (`results/T5_sign_power.json`). A modest directional effect will not be
detected, and that is reported as realized power, not repaired after the fact.

**What it buys.** No new artifact, manifest, gate or hash; an exact rather than
approximate comparison to a published Paper 1 result on identical items; and no
draw sized against an unmeasured quantity, which is what v2.3 section 6 declined to
do and what this decision declines permanently.

---

## 2. The tie rate: reference, threshold, and what each outcome licenses. **P2-D8**

v2.4 section 2.4 made the tie rate primary and said H-B resolves on both halves
together, but stated **no tie-rate value as supporting H-B**. The sign test has an
`alpha`, a null and a family; the tie rate had none and carries half the inference.
Section 3.3's exact interval is precision, not calibration: a tie rate of 0.9 with a
tight interval is equally consistent with models being insensitive to adversary
structure and with F1/F2 being too weak to move anything, and the second is a fact
about T3's templates rather than about models. This section fixes that.

### 2.1 The reference, and why it is not the permutation rate

`ΔA_i = 0` is, near enough, "the model chose the same option under both framings"
(section 3 measures how near). So the tie rate is a same-option rate, and Paper 1
already contains same-option rates on the same coordinate, items, models and
renderer. Two candidates:

- **`c5`.** Paper 1's condition 4 against condition 5: one sentence inserted into
  the **same `{extra}` slot** P2-D2 puts the framing block in, with option order
  held fixed. Matched to the framing contrast in slot, in kind, and in which factor
  varies. It differs in **content** only: D64's `c5` asks the chooser to consider
  every Means-by-Clue pairing; P2's block describes an adversary.
- **Permutation.** Format V permutation 0 against permutation 1 within one
  condition: option **order** varies and text is held fixed. This is the *opposite*
  perturbation.

**The permutation rate is rejected as the primary reference**, and the reason is
measured rather than argued. On the confirmatory set the two references are far
apart, with the permutation rate below the `c5` rate on every model by 0.18 to 0.57.
Reordering is the stronger perturbation, so the permutation rate is an **upper bound
on surface-driven change** rather than a matched null, and using it would set a bar
that almost any tie rate clears. `c5` is the primary reference. The permutation rate
is retained and reported as the bound it is.

### 2.2 The reference values, fixed here

`size`-tile confirmatory set, `n = 108` items, `pmi` / `template`, from
`results/T5_tie_reference.json`. **T7 uses these numbers; it does not recompute
them.**

| model | `c5` same-option rate `R_m` | pairs | permutation rate (bound) |
|---|---:|---:|---:|
| `CTRL` | **0.7037** | 216 | 0.4722 |
| `B2` | **0.8037** | 214 | 0.4259 |
| `B4` | **0.6296** | 216 | 0.4537 |
| `L1` | **0.8611** | 216 | 0.2870 |
| `L2` | **0.8519** | 216 | 0.3426 |
| `L3` | **0.8102** | 216 | 0.2778 |
| `L4` | **0.7407** | 216 | 0.5093 |

### 2.3 The decision rule, fixed here

For model `m` and framing contrast `c`, let `T_{m,c}` be the **same-option rate**
between F0 and the contrast framing, over matched rendering pairs (item x
permutation), on the confirmatory set.

```
statistic   T_{m,c} - R_m
interval    cluster bootstrap over ITEMS, 10,000 resamples, seed 20260910,
            at 1 - alpha with alpha = 0.05/21
verdict     "materially below"  if the interval lies entirely below 0
            "materially above"  if it lies entirely above 0
            "indistinguishable" otherwise
```

Items are the resampling unit because each contributes two renderings; a binomial
interval on 216 pairs would treat 108 items as 216 independent draws.

**The instrument was checked before it was adopted**, by running it on the two
references against each other on the same set. It separates the permutation rate
from the `c5` rate on all seven models at the corrected `alpha`. Its resolution is
a half-width of **0.1412 to 0.1667**, so it can detect a gap of roughly 0.15 and
cannot resolve smaller. That is the honest limit and it is stated rather than
discovered in T7.

### 2.4 Whether the tie rate enters the 21-test family: it does not, and why

**Decision. Two families of 21, corrected separately at `alpha = 0.05/21` each, not
one family of 42.**

The reason is the conjunction. Rejecting H-B for a cell requires **both** halves:
the tie rate materially below `R_m` (something moved) **and** the sign test above
`p0 = 0.5` (it moved toward the adversary optimum). For a false rejection both must
fire when nothing moved, so

```
P(false rejection of H-B for a cell) <= min(P(tie fires), P(sign fires)) <= 0.05/21
```

Correcting a conjunction at `0.05/42` would over-correct: it would buy no protection
the conjunction does not already give, and would cost real power in a design that
section 1 has just declined to enlarge. The two halves are also not independent,
since they partition the same items, so treating them as 42 independent tests would
be wrong in its own right.

**What this does not license.** The tie rate on its own does not carry a
confirmatory claim in either direction, and no cell's H-B verdict rests on it alone.

### 2.5 What each outcome licenses

| `T_{m,c} - R_m` | reading | licenses |
|---|---|---|
| **indistinguishable** | The framing moved choices no more than a content-neutral sentence in the same slot does. | **Not support for H-B.** H-B is a claim about models; this outcome is consistent with F1/F2 being too weak to move anything, which is a fact about T3's templates. The cell is reported **inconclusive**, and its sign test carries no claim in either direction. |
| **materially below** | Something moved, beyond the matched perturbation. | The sign test on the movers carries the direction, and H-B resolves for that cell on the conjunction. |
| **materially above** | The framing moved choices **less** than a content-neutral sentence does. | See below. |

**The third outcome, stated now because it is representable and was previously
unaddressed.** A framing tie rate materially above `R_m` means the adversary block
makes the model *more* stable than a neutral insert does. That is an effect of the
manipulation, not an absence of one, so **it does not support H-B either.** Two
readings are available in advance and the design does not separate them: the block
anchors attention and makes the choice more deterministic, or it pushes toward a
canonical answer and collapses the option marginal. The block is also longer than
`c5`, and F0-versus-F1 is not length-matched by construction (T3's length parity is
between F1 and F2), so length is a live confound for this outcome specifically.

**Preregistered diagnostic for it**, reusing a quantity v2.0 section 3.3 already
defines rather than inventing one: compare the entropy of the model's marginal over
canonical option ids, `p_{m,F}`, between F0 and the contrast framing. A drop
indicates collapse onto fewer options. **This is a diagnostic, not a test**: it is
reported with the cell and spends no alpha. If this outcome occurs it is reported as
an unexplained positive that the design does not resolve, and not as evidence for or
against adversary tracking.

---

## 3. `ΔA = 0` is not the same event as "same option", and the gap is measured

Stated because the reference in section 2 calibrates a same-option rate while
P2-D6's tie rate is `ΔA = 0`, and the two are not identical.

`A` is a deterministic function of the chosen option, so **same option implies
`ΔA = 0`**. The converse fails: `A` is not injective over an option set, and two
distinct options can share an `A`. So

```
same-option rate  <=  tie rate
```

Measured on the confirmatory set (`results/T5_tie_reference.json`): **48 of 108
items** carry at least one pair of distinct options with identical `A`, which is
**50 of 1,620** unordered option pairs, or 0.0309.

Two consequences, both reported rather than corrected:

1. **The tie rate is an upper bound on same-option behaviour**, so a tie rate at or
   above the reference is weaker evidence of stability than the same rate would be
   if `A` were injective. The comparison in section 2.3 is therefore run on the
   same-option rate, which is matched to the reference, and the tie rate is reported
   beside it.
2. **`A` cannot see some real choice movement.** On an item with an `A`-tied option
   pair, a genuine switch between those two options registers as no movement. This
   is a sensitivity limit of the coordinate, not of the sample, and no item set
   fixes it. It is stated as a limitation on what a high tie rate can mean.

---

## 4. What is not decided here

- **K1 and K2.** Settled. Neither is referenced as live.
- **Arm A and Arm C.** Untouched.
- **`alpha`, the 21-test family, the confirmatory item set, D74's SESOI on the
  mean.** Unchanged. Section 2.4 adds a second family of the same size rather than
  enlarging the first.
- **Any new item draw.** P2-D7 declines the one that was open; no other is proposed.

## 5. Ordering, disclosed

The reference values in section 2.2 are model output. They are **Paper 1's**, under
Paper 1's own conditions, and no Paper 2 framing has been rendered or scored. They
were computed to give the tie rate a comparator, and the choice between the two
candidate comparators was made on a structural argument (matched slot, matched kind
of perturbation) that holds independently of the values, then confirmed by the
measured gap. The threshold, the interval, the bootstrap seed, the resolution and
the outcome table are all fixed in this document before T7 runs, and T7 is
instructed to use the tabulated `R_m` rather than recompute them.
