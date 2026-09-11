# PREREGISTRATION v2.7

**Paper 2: the adversary effect and the RL Scientist**

Version 2.7 · written 2026-09-10 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.6`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
eight are read together. This version restructures Arm B's confirmatory logic into
three quantities, none gating another, and replaces the detection ceiling `v2.6`
section 3.3 computed under the superseded gate. It does not reopen K1 or K2, does not
change `alpha`, `p0`, the coordinate, the confirmatory item set or `n`, and does not
touch Arm A or Arm C. It authorizes no item draw.

**Data observed at the time of writing.** No Paper 2 model data of any kind. Two new
reads of frozen Paper 1 output, both on the `cond4` / `cond5` rows `v2.5` section 2.2
and `v2.6` section 1.2 already read: `c5`'s own `ΔA` sign proportion, and `c5`'s tie
rate against its same-option rate. Both by `src/inertness_ceiling.py` into
`results/T5_inertness_ceiling.json`. Section 3's floor uses no observed choice at all.

| # | decision | where |
|---|---|---|
| 1 | Three quantities, none gating another. The `c5` comparison stops being a gate. | §1, §2, **P2-D12** |
| 2 | The replacement detection ceiling, and what the restructure does **not** buy. | §3 |

**Note on section numbering.** The instruction that prompted this version named
`v2.6` section 3.4's table. Section 3.4 has no table; the ceiling table is in `v2.6`
section 3.3, and that is what section 3 below replaces.

---

## 1. Why the gate has to go

`v2.5` section 2 introduced the `c5` reference to answer one question, stated there
in its own words: a tie rate of 0.9 with a tight interval is equally consistent with
models being insensitive to adversary structure and with F1 and F2 being too weak to
move anything, and the second is a fact about T3's templates rather than about models.
Call that the **inertness question**. The reference was the instrument for it.

`v2.6` section 1.1 then established something `v2.5` did not have: **the no-effect
same-option rate is exactly 1.0**, because Paper 1's chooser is an argmax over
teacher-forced option log-probabilities with no sampling anywhere in the scoring path.
That is a point null with no variance. It answers the inertness question directly: a
change rate distinguishable from zero establishes that the manipulation moved
something, and no reference manipulation is needed to say so.

The reference's original purpose is therefore already served, and `v2.5` section 2.3's
construction now does something else instead. It requires the framing's same-option
rate to sit more than a bootstrap half-width **below** `R_m` before the movement half
fires, which sets the bar for "something moved" at the magnitude of an unrelated
manipulation. `v2.6` section 3.3 measured the cost: `L1` had to change the chosen
option on 2.13 times as many pairs as `c5` does, and the sign test's effective `n` was
capped at 32 to 58.

That is a bar the design never intended to set. It is removed.

## 2. The three quantities. **P2-D12**

**Arm B reports three quantities and none of them gates another.**

### (a) Inertness. Where H-B's no-movement half resolves

```
statistic   the same-option CHANGE rate, per model, on the full confirmatory n
null        0, exactly. Not estimated, not a reference. P1's scorer is deterministic.
interval    P2-D8's cluster bootstrap over ITEMS, 10,000 resamples, seed 20260910,
            at 1 - alpha with alpha = 0.05/21
verdict     "moved"  if the interval lies entirely above 0
            "inert"  otherwise
```

The instrument and its seed are P2-D8's, unchanged. What changes is the comparand:
zero rather than `R_m`.

**The floor is a count of items, not a rate.** The item-level mean of a bootstrap
resample is zero exactly when the resample contains no moving item, so the lower bound
clears zero as soon as `((n - k) / n)^n < alpha / 2`. At `n = 108` and
`alpha = 0.05/21` that gives **`k = 7`**, checked against the bootstrap itself: six
movers give a lower bound of 0.000000, seven give 0.009259. An item that changes one
of its two renderings counts the same as one that changes both, which is confirmed
separately.

### (b) Magnitude context. Reported, never a gate

```
statistic   the framing same-option rate minus R_m, with the bootstrap half-width
role        DESCRIPTIVE. Spends no alpha. Gates nothing.
```

`R_m` is the only thing that says whether a framing effect is large or small in this
signal space, so it is kept. Its resolution limit is unchanged and still binding on
what the context can say: a gap below roughly 0.15 is not resolvable, so a framing
that moves choices materially less than `c5` does is not distinguishable from one that
moves them as much. Under P2-D12 that limits the **sentence**, not whether the
movement half fires.

### (c) Direction. Unchanged

```
statistic   exact two-sided sign test on { i : ΔA_i != 0 } against p0 = 0.5
alpha       0.05/21, two-sided
```

Nothing about P2-D6's instrument changes. What changes is that it now runs on every
cell rather than only on cells that cleared a magnitude gate.

**H-B's no-movement half resolves on (a), with (b) as context, never on (b).** The
conjunction for rejecting H-B is (a) AND (c). P2-D8's `alpha` argument carries
unchanged, since a conjunction's error is still bounded by the smaller of its parts,
and (b) spends no `alpha` to bound.

### 2.1 What the magnitude gate might have been reaching for, and why it did not reach it

The one defensible case for gating on magnitude is a confound: `o*_infinity` is Paper
1's `o_fit` on 452 of 460 divergent items (`v2.4` section 1.1), so it is the salience
pole. If **any** inserted text drifted choices toward salience, a positive F1 sign test
would be explicable without adversary tracking, and requiring F1 to move more than a
neutral insert would look like protection against that.

It is not. The confound is **directional** and a magnitude gate is blind to direction.
A framing that moves twice as much as `c5` can still be moving by salience drift.

The quantity that does address it is `c5`'s own `ΔA` sign proportion, which is
computable from the same frozen rows. Measured on the confirmatory set:

| model | ties | `n_eff` | positive | sign proportion | `p` |
|---|---:|---:|---:|---:|---:|
| `CTRL` | 0.7546 | 53 | 13 | **0.2453** | 0.0003 |
| `B2` | 0.8037 | 42 | 21 | 0.5000 | 1.0000 |
| `B4` | 0.6296 | 80 | 39 | 0.4875 | 0.9111 |
| `L1` | 0.8750 | 27 | 11 | 0.4074 | 0.4421 |
| `L2` | 0.8519 | 32 | 15 | 0.4688 | 0.8601 |
| `L3` | 0.8380 | 35 | 9 | 0.2571 | 0.0060 |
| `L4` | 0.7454 | 55 | 16 | 0.2909 | 0.0027 |

**A content-neutral insertion does not drift toward the salience pole.** The
proportion is at or below 0.5 on all seven models, and where it departs from 0.5 it
departs downward, one model significantly at the corrected `alpha`. So `p0 = 0.5` is
**conservative** for detecting movement toward `o*_infinity`, and the confound the
magnitude gate was a poor proxy for is measured absent.

**This is reported and it is not adopted as a null.** P2-D6 fixes `p0 = 0.5`. Moving
`p0` to `c5`'s proportion would recalibrate a preregistered test against a different
manipulation, on a coordinate Paper 1 never used, and it would make a positive F1
result easier to obtain. It stays a diagnostic.

### 2.2 P2-D10's blind spot, now measured rather than bounded

`v2.5` section 3 bounded the tie-rate-minus-same-option-rate gap from the frozen
geometry. The `c5` contrast gives it observed on a real manipulation: **0.0000 to
0.0509**, zero on `B2`, `B4` and `L2`, largest on `CTRL`. The decision in P2-D10 does
not depend on the size of this gap, only on its sign, but a reported number is better
than a bound and it is now on the record.

### 2.3 One consequence to name rather than discover

The inertness floor of 7 items is **0.11 to 0.25 times** what `c5` itself moves, so
the movement half is nearly free and H-B's rejection rests almost entirely on (c).
That is the correct allocation: H-B is a claim about direction. The other side of it
is that **confirming** H-B's null half is now demanding, since a framing must change
the chosen option on fewer than 7 of 108 items. Confirming a null should be demanding,
and P2-D9's exact zero is what makes it a claim about the framing rather than about
measurement noise.

---

## 3. The replacement detection ceiling

This replaces `v2.6` section 3.3's table. `v2.6` is not edited, and
`results/T5_detection_ceiling.json` is kept unchanged, because a superseded document
must still reproduce.

### 3.1 What the restructure does **not** buy

**It does not make the sign test more powerful.** The sign test's effective `n` is
`108 * (1 - tie rate)` under both designs, and the tie rate is a property of the
framing, not of the decision rule. What the gate did was refuse to run the sign test
at all unless the framing effect was large, and a large framing effect is mechanically
a low tie rate. So the gated ceiling's `n_eff` of 32 to 58 was **conditional on the
gate firing**, not a floor the restructure gives up.

The honest comparison is between what each design reports for the same cell. Take a
cell whose framing moves choices about as much as `c5` does:

- **Under the gate:** the movement half does not fire, the cell is reported
  inconclusive, and the sign test result is discarded.
- **Under P2-D12:** the movement half fires, the sign test runs at the effective `n`
  the tie rate gives, and its realized power is reported alongside it.

That is strictly more information, and it is honestly underpowered rather than silent.

### 3.2 The table

`c5`'s tie rate is used as the analogue for F1's, with the caveat
`reports/T5_sigma_prior.md` section 0 attaches to its own analogue: a structurally
matched manipulation, not a measurement of the quantity. It sizes nothing.

| model | `c5` items moved / 108 | floor / `c5` | `c5` tie rate | `n_eff` | power at `p1 = 0.75` | at `0.90` | `p1` at 80% power |
|---|---:|---:|---:|---:|---:|---:|---:|
| `CTRL` | 54 | 0.13 | 0.7546 | 26 | 0.184 | 0.888 | 0.879 |
| `B2` | 36 | 0.19 | 0.8037 | 21 | 0.192 | 0.848 | 0.889 |
| `B4` | 65 | 0.11 | 0.6296 | 40 | 0.584 | 0.999 | 0.791 |
| `L1` | 28 | 0.25 | 0.8750 | 14 | 0.101 | 0.585 | 0.941 |
| `L2` | 31 | 0.23 | 0.8519 | 16 | 0.063 | 0.515 | 0.949 |
| `L3` | 38 | 0.18 | 0.8380 | 17 | 0.164 | 0.762 | 0.909 |
| `L4` | 44 | 0.16 | 0.7454 | 28 | 0.264 | 0.945 | 0.858 |

Read it as the bad news it is. If F1's tie rate resembles `c5`'s, the sign test on
`L2` has 16 signed items and reaches 80 per cent power only at `p1 = 0.949`. The
movement half will fire on every one of these cells, and the direction half will be
able to say almost nothing unless the effect is very large. **The restructure makes
that visible instead of converting it into seven inconclusive cells.**

### 3.3 The `n` shortfall, unchanged and restated here

`n = 108` against `v2.0` section 8.2's benchmark of 400. P2-D6 replaced the mean with
a sign test and P2-D12 replaced the gate; neither changes how much information 108
items carry. `v2.5` section 1 and `v2.6` section 3.4 record the same point, and it is
repeated here because this is the section a reader consults when a null is reported.

### 3.4 What a null licenses, and what it does not

> **A null on (a) licenses:** that the framing changed the chosen option on fewer than
> 7 of 108 items, which at this `n` is indistinguishable from a manipulation that
> changes nothing. Because the no-effect rate is exactly 1.0 and not estimated, this is
> a statement about the framing, not about measurement noise. It is the strongest form
> of "no movement" this design can produce.
>
> **A null on (c) licenses:** that among the items that moved, the direction was not
> distinguishable from chance at the realized `n_eff`, which is reported with the
> verdict.
>
> **Neither licenses:** that models are insensitive to adversary structure. A framing
> can move choices without moving them toward `o*_infinity`, which is what (c)
> separates and what (a) cannot. Nothing licenses a claim about magnitude: (b)'s
> resolution is roughly 0.15 on the same-option rate, so a framing that moves choices
> materially less than `c5` does is not distinguishable from one that moves them as
> much. The `A` coordinate additionally cannot see a switch between two `A`-tied
> options, measured at 0.0000 to 0.0509 on the `c5` contrast. P2-D5 stands: no claim
> about adversary-relevant content rests on `A` under a single framing.

Every reported Arm B null carries this statement, which is P2-D11's requirement
retained after its ceiling was superseded.

---

## 4. What is not decided here

- **`p0`, `alpha`, the two families of 21, the coordinate, the confirmatory item set,
  `n = 108`, D74's SESOI on the mean.** All unchanged. Section 2 changes which
  quantity carries H-B's no-movement half; it introduces no new statistic and no new
  coordinate.
- **P2-D9 and P2-D10.** Unchanged and load-bearing. P2-D12 rests on P2-D9's exact
  zero, and uses P2-D10's same-option rate for both (a) and (b).
- **K1 and K2, Arm A, Arm C.** Untouched.
- **Any new item draw.** P2-D7 declined the one that was open. Section 3.2 is a
  statement of limits, not a case for enlargement, and an enlargement sized against it
  would be sized against a quantity computed after the limits were seen.

## 5. Ordering, disclosed

Section 2's floor uses no observed choice: it follows from `n`, `alpha` and the
bootstrap's own arithmetic. The decision to remove the gate follows from P2-D9's
determinism result, which is a property of Paper 1's code and not of any measurement
made here.

Sections 2.1 and 2.2 **are** model output. They are Paper 1's, on conditions 4 and 5,
on the same rows `v2.5` section 2.2 read, and no Paper 2 framing has been rendered or
scored. Section 2.1's diagnostic was computed to answer a question raised against the
restructure, namely what a magnitude gate might buy, with both answers written down
before the number was seen: a proportion above 0.5 would have been a reason to keep a
direction-matched reference and to reconsider `p0`, and a proportion at or below 0.5
makes `p0 = 0.5` conservative. It came out the second way and `p0` was left alone,
which is the direction that makes a positive F1 result harder rather than easier.

Section 3.2's table uses `c5`'s tie rate, which is model output, as an analogue for a
quantity that cannot be observed before T7 runs. It sizes nothing, authorizes nothing,
and is labelled an analogue in the same terms `reports/T5_sigma_prior.md` labels its
own.
