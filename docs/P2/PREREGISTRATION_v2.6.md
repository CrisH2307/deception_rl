# PREREGISTRATION v2.6

**Paper 2: the adversary effect and the RL Scientist**

Version 2.6 · written 2026-09-10 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.5`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
seven are read together. This version settles three things Arm B needs before T7
runs and nothing else. It does not reopen K1 or K2, does not change `alpha`, the
confirmatory item set or `n`, and does not touch Arm A or Arm C. It authorizes no
item draw and no new coordinate.

**Data observed at the time of writing.** No Paper 2 model data of any kind. One new
body of evidence, and it is a read of frozen Paper 1 output on the same conditions
`v2.5` already read: whether Paper 1's `c5` insert moved the chosen option, computed
by `src/c5_effect.py` into `results/T5_c5_effect.json`. Section 3's ceiling is a
combination of quantities already fixed, computed by `src/detection_ceiling.py` into
`results/T5_detection_ceiling.json`, and uses no observed choice at all.

| # | decision | where |
|---|---|---|
| 1 | The `c5` reference is an **active comparator**, not a no-manipulation baseline. The outcome table's "indistinguishable" row is restated accordingly. | §1, **P2-D9** |
| 2 | The **same-option rate** is primary for H-B's no-movement half. The tie rate is the sign test's denominator. | §2, **P2-D10** |
| 3 | Both detection limits, and the `n` shortfall, stated in one place with what a null does and does not license. | §3, **P2-D11** |

---

## 1. The `c5` reference is an active comparator. **P2-D9**

`v2.5` section 2 fixed `R_m`, the decision rule, the interval, the resolution and the
outcome table, and left one thing unstated: whether `c5` itself moved anything. That
is not a detail. It changes what a null licenses, and the two readings were both
available in advance:

- **`c5` had little or no effect.** `R_m` is a no-manipulation baseline, and "F1
  indistinguishable from `R_m`" means F1 moved nothing.
- **`c5` moved choices.** `R_m` is an active comparator, and the same result means
  "F1 moved choices about as much as a known-effective content insertion in the same
  slot did", which is a different and stronger sentence.

Deciding this after T7's data existed would be choosing an interpretation with the
result in view, so it is decided here.

### 1.1 The no-effect rate is exactly 1.0, and it is argued from the code path

The question "did `c5` move choices" needs a comparator for `R_m`, and the comparator
is the same-option rate a no-op perturbation would give.

Paper 1 never samples. `score_llm.score_rows` teacher-forces every option string and
sums token log-probabilities from a single forward pass, `score_llm.pick` returns the
argmax set, and the analysis keeps `n_tied == 1`. There is no temperature, no
`do_sample`, no seed and no `generate` call in that file. An identical prompt
therefore returns an identical `chosen_option`, and the no-effect same-option rate is
**1.0 exactly**.

**This is argued, not measured, and the reason is stated rather than glossed.** The
frozen artifacts contain no repeated rendering: the two choice files share no model,
and permutation is a real perturbation rather than a repeat. So there is no
within-artifact null pair to measure against. The residual is float nondeterminism
across batch compositions flipping a near-tie. It is not quantifiable from the frozen
columns, which carry the chosen option's score and not the runner-up's, and it is not
a credible account of a change rate of 0.37.

### 1.2 The measurement

`size`-tile confirmatory set, `n = 108` items, `pmi` / `template`, cluster bootstrap
over items at `1 - alpha` with `alpha = 0.05/21`, seed 20260910, the same instrument
`v2.5` section 2.3 fixed. `results/T5_c5_effect.json`.

| model | `R_m` | change rate | changed / pairs | interval on the change rate | items with a changed pair | TV on the option marginal |
|---|---:|---:|---:|---:|---:|---:|
| `CTRL` | 0.7037 | **0.2963** | 64 / 216 | [+0.2037, +0.3981] | 0.5000 | 0.2315 |
| `B2` | 0.8037 | **0.1963** | 42 / 214 | [+0.1111, +0.2917] | 0.3333 | 0.0794 |
| `B4` | 0.6296 | **0.3704** | 80 / 216 | [+0.2731, +0.4722] | 0.6019 | 0.2130 |
| `L1` | 0.8611 | **0.1389** | 30 / 216 | [+0.0741, +0.2130] | 0.2593 | 0.0880 |
| `L2` | 0.8519 | **0.1481** | 32 / 216 | [+0.0829, +0.2176] | 0.2870 | 0.0741 |
| `L3` | 0.8102 | **0.1898** | 41 / 216 | [+0.1157, +0.2731] | 0.3519 | 0.0926 |
| `L4` | 0.7407 | **0.2593** | 56 / 216 | [+0.1667, +0.3657] | 0.4074 | 0.1898 |

**Verdict: active comparator, on all seven models.** The change rate runs 0.1389 to
0.3704 and every interval excludes the no-effect rate at the corrected `alpha`. On
the 460-item divergence set the same measurement gives 0.0761 to 0.4120, also
excluding zero on all seven.

Two things the table says that the change rate alone does not:

1. **It is not only churn.** Total variation distance between the `cond4` and `cond5`
   option marginals is 0.0741 to 0.2315, so the insert shifts the distribution over
   options and does not merely reshuffle which rendering lands where.
2. **A near-zero mean is not absence of movement.** `reports/T5_sigma_prior.md`
   reports a mean `d_i` on `post_norm` of -0.0322 to +0.0116 with a per-item
   dispersion of 0.1357 to 0.3391. Reading that mean as "the insert did nothing"
   would have been wrong, and on the coordinate that actually calibrates the
   reference, the chosen option, it moves 14 to 37 per cent of renderings.

### 1.3 What this does not change

The verdicts are unchanged. An indistinguishable cell is still reported inconclusive
and its sign test still carries no claim, because this comparison is blind to
direction and H-B is a claim about direction. What changes is the sentence T7 is
permitted to write about that cell.

### 1.4 The outcome table, restated

`v2.5` section 2.5 is not edited, per D148. This is its replacement, with the reading
column written against an active comparator and the licences unchanged.

| `T_{m,c} - R_m` | reading, against an active comparator | licenses |
|---|---|---|
| **indistinguishable** | The framing moved choices about as much as `c5` did, and `c5` moved them on 0.1389 to 0.3704 of pairs. This is a statement of **relative magnitude**, not of absence. | **Not support for H-B.** The comparison is blind to direction, and the cell is consistent with the framing being adversary-irrelevant, with T3's F1/F2 being too weak, and with a real effect below section 3's limits. The cell is reported **inconclusive** and its sign test carries no claim in either direction. |
| **materially below** | The framing moved choices more than a known-effective content insertion in the same slot did. | The sign test on the movers carries the direction, and H-B resolves for that cell on the conjunction. |
| **materially above** | The framing moved choices **less** than a known-effective content insertion did, so the block is stabilizing relative to a manipulation that demonstrably moves this scorer. | Unchanged from `v2.5` section 2.5: not support for H-B either, reported as an unexplained positive, with the `p_{m,F}` entropy diagnostic and the length confound noted. |

---

## 2. The same-option rate is primary. **P2-D10**

`v2.4` section 2.4 made the tie rate primary. `v2.5` section 2.3 ran the reference
comparison on the same-option rate, and `v2.5` section 3 said why. Both cannot be
primary for H-B's no-movement half. Nothing in either document rules between them, so
T7 would have picked, and a session picking between two preregistered statistics
after seeing which favours the outcome is the failure a preregistration exists to
prevent.

### 2.1 The ruling

**The same-option rate is primary. The tie rate is the sign test's denominator.**

Three grounds, in order of weight:

1. **It is what the reference calibrates.** `R_m` is a same-option rate computed on
   Paper 1's own conditions. `A` did not exist for Paper 1 and no tie rate can be
   computed from its artifacts. A statistic with no null cannot carry half of a
   confirmatory conjunction, and `v2.5` section 2 exists because `v2.4` left the tie
   rate in exactly that state.
2. **Calibrating the tie rate against `R_m` would compare a rate to a bound on
   itself.** Same option implies `ΔA = 0`, so same-option rate is at most the tie
   rate. Testing the tie rate against a same-option reference is biased toward "no
   movement" by exactly the size of the gap, and the gap is not small: 48 of 108
   confirmatory items carry at least one `A`-tied option pair.
3. **It is not blind to switches between `A`-tied options.** The tie rate is. A model
   that switches between two options sharing an `A` has moved, and the same-option
   rate records it.

**The tie rate is not demoted to nothing.** It is mechanically what the sign test
operates on: ties carry no sign and are dropped, so the tie rate sets the effective
`n` and the realized power. It is reported for every cell with its exact interval,
beside the same-option rate.

### 2.2 The gap is the coordinate's blind spot, and it is reported per cell

```
same-option rate  <=  tie rate
gap  =  tie rate - same-option rate  >=  0
```

The gap is choice movement `A` cannot see: a switch between two options with
identical `A`. Measured on the frozen geometry (`results/T5_tie_reference.json`), the
confirmatory set carries 50 `A`-tied option pairs among 1,620, which is 0.0309, on 48
of 108 items. The aggregate understates the exposure, which is why the per-cell gap is
reported rather than the aggregate share.

One consequence to state plainly, because it is the price of the ruling. The two
halves of the conjunction now operate on **nested** subsets: the movement half counts
pairs that changed option, the sign test runs on pairs with `ΔA != 0`, and the second
set is contained in the first. The difference is the blind spot expressed as counts,
and it is reported as such. P2-D8's `alpha` argument is unaffected, since a
conjunction's error is still bounded by the smaller of its parts.

### 2.3 What is superseded, and what is not

`v2.4` section 2.4's **label** is superseded. Nothing it computes is. The tie rate is
still reported directly, the sign test is still exact and two-sided against
`p0 = 0.5` at `alpha = 0.05/21`, mean `ΔA` is still not confirmatory, and the median
and the value from the means are still reported. `v2.5` section 2.3's statistic was
already the same-option rate, so this decision makes the two documents agree rather
than changing what either does.

---

## 3. What Arm B can detect, in one statement. **P2-D11**

The two limits are stated in two documents and neither says they compose. They do,
and unfavourably. A reader assembling them from `v2.5` section 2.3 and `v2.4` section
3.2 has no way to see that the second binds hardest exactly where the first has just
fired. This section is where they sit together.

### 3.1 Limit 1, the reference comparison

P2-D8's cluster bootstrap has a half-width of **0.1412 to 0.1667** on the
confirmatory set, measured on its own adoption check. A framing whose same-option
rate sits within roughly 0.15 of `R_m` is "indistinguishable", which section 1.4
rules is not support for H-B. So the movement half fires only at a framing
same-option rate at or below `T*_m = R_m - h_m`.

### 3.2 Limit 2, the sign test

Ties carry no sign, so the effective `n` is `108 * (1 - tie rate)`. From
`results/T5_sign_power.json`, at a 30 per cent tie rate the test reaches 80 per cent
power only at `p1 = 0.721`, and at a 50 per cent tie rate only at `p1 = 0.762`.

### 3.3 How they compose

Rejecting H-B for a cell needs both halves. Since same-option rate is at most the tie
rate (section 2.2), at limit 1's boundary the tie rate is at least `T*_m`, so the sign
test's effective `n` there is **at most** `108 * (1 - T*_m)`. That is an upper bound
on the sign test's power at the weakest framing effect limit 1 can resolve.
`results/T5_detection_ceiling.json`:

| model | `R_m` | `h_m` | framing change rate needed | x `c5` | `n_eff` at most | sign power at `p1 = 0.70` | `p1` at 80% power |
|---|---:|---:|---:|---:|---:|---:|---:|
| `CTRL` | 0.7037 | 0.1551 | 0.4514 | 1.52 | 48 | 0.396 | 0.770 |
| `B2` | 0.8037 | 0.1412 | 0.3375 | 1.72 | 36 | 0.204 | 0.818 |
| `B4` | 0.6296 | 0.1667 | 0.5370 | 1.45 | 58 | 0.519 | 0.746 |
| `L1` | 0.8611 | 0.1574 | 0.2963 | 2.13 | 32 | 0.212 | 0.822 |
| `L2` | 0.8519 | 0.1481 | 0.2963 | 2.00 | 32 | 0.212 | 0.822 |
| `L3` | 0.8102 | 0.1417 | 0.3315 | 1.75 | 35 | 0.234 | 0.812 |
| `L4` | 0.7407 | 0.1667 | 0.4259 | 1.64 | 46 | 0.345 | 0.780 |

Read across one row. For `L1` the framing must change the chosen option on 29.6 per
cent of pairs, **2.13 times** what `c5` changes, before the movement half fires at
all. At that boundary the sign test has at most 32 signed items, and 80 per cent power
arrives only at `p1 = 0.822`, meaning more than four in five movers must move toward
the adversary optimum.

**The limits do not trade off.** The intuition that a framing weak enough to strain
limit 1 at least leaves the sign test plenty of movers is wrong on the models where
`R_m` is high, because a high `R_m` sets a high `T*_m`, and a high `T*_m` bounds the
tie rate from below. The bound is slack only for a framing that moves choices far more
than `c5` does, which is the case where neither limit is binding anyway.

### 3.4 Limit 3, the `n` shortfall, which is not repaired by the change of statistic

`n = 108` against `v2.0` section 8.2's benchmark of 400. P2-D6 replaced the mean with
a sign test, so section 8.2's curve no longer governs the confirmatory test. **The
shortfall in information is unchanged by that.** A statistic that needs less of an
unmeasured `sigma` does not thereby need fewer items. `v2.5` section 1 records the
same point on the redraw decision, and it is repeated here because this is the section
a reader will consult when a null is reported.

### 3.5 What a null licenses, and what it does not

> **A null licenses:** that the framing did not move choices detectably more than
> Paper 1's `c5` insert moved them, at `n = 108`, on the `size` tile, on the `A`
> coordinate, with a resolution of roughly 0.15 on the same-option rate. Because `c5`
> is an active comparator (section 1) and not a no-manipulation baseline, this is a
> statement about **relative magnitude**, not about absence of movement.
>
> **A null does not license:** that models are insensitive to adversary structure.
> Three readings produce the same null and this design does not separate them. The
> models are insensitive; T3's F1 and F2 are too weak to move anything, which is a
> fact about the templates rather than about models; or the effect is real and
> smaller than the limits in 3.1 to 3.4. To these add the coordinate's blind spot
> (section 2.2), which hides a switch between two `A`-tied options on 48 of 108
> confirmatory items, and P2-D5's standing prohibition, under which no claim about
> adversary-relevant content rests on `A` under a single framing.

Every reported Arm B null carries this statement. It is not a footnote to be
assembled by the reader from two other documents, which is the state this section
ends.

---

## 4. What is not decided here

- **K1 and K2.** Settled. Neither is referenced as live.
- **Arm A and Arm C.** Untouched.
- **`alpha`, the two families of 21, the confirmatory item set, `n = 108`, D74's
  SESOI on the mean, the `A` coordinate.** All unchanged. Section 2 renames which of
  two already-preregistered rates carries the no-movement half; it introduces no
  statistic.
- **Any new item draw.** P2-D7 declined the one that was open. None is proposed, and
  section 3 is a statement of limits rather than a case for enlargement. An
  enlargement sized against section 3's ceiling would be sizing against a quantity
  computed after the ceiling was seen, which is the objection `v2.4` section 1.2
  raises against a new coordinate.

## 5. Ordering, disclosed

Section 3 uses no observed choice of any kind. Its inputs are `R_m`, fixed in `v2.5`
section 2.2, the instrument half-widths from P2-D8's own adoption check, and the
exact binomial power function, so nothing in it could have been selected to favour an
outcome.

Section 1 **is** model output. It is Paper 1's, under Paper 1's own conditions 4 and
5, on the same rows `v2.5` section 2.2 already read, and no Paper 2 framing has been
rendered or scored. It was computed to answer whether the reference has a status, a
question raised before the number was seen, and both answers were written down in
advance with the sentence each would license. The measurement selected between them;
it did not generate them.

Section 2 rests on an inequality that holds on the frozen geometry with no model
choice at all, and on the fact that Paper 1's artifacts cannot produce a tie rate.
Neither depends on any value measured here.
