# PREREGISTRATION v2.8

**Paper 2: the adversary effect and the RL Scientist**

Version 2.8 · written 2026-09-10 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.7`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
nine are read together. This version corrects the justification of a threshold, fixes
a word in a licenses box that contradicted a measurement two sections earlier, and
rules an admissibility question that was being used without authority. It changes no
statistic, no `alpha`, no `p0`, no coordinate, no item set and no `n`, and it does not
touch Arm A or Arm C.

**Data observed at the time of writing.** No Paper 2 model data of any kind. No new
read of Paper 1 output either: sections 2 and 3 use the `c5` sign proportions already
in `results/T5_inertness_ceiling.json` and reported in `v2.7` section 2.1. Section 1's
argument is about the null's variance and uses no data at all.

| # | decision | where |
|---|---|---|
| 1 | Quantity (a)'s floor is numerical, not statistical. Provisionally 7, revised upward to T7's `F0` disagreement count. | §1, **P2-D13** |
| 2 | `p0 = 0.5` retained; "chance" withdrawn; the Type II cost given per model. | §2, **P2-D14** |
| 3 | `sign(ΔA)` is admissible for the cross-family control under D111. | §3, **P2-D15** |

---

## 1. Quantity (a)'s floor is a numerical noise floor. **P2-D13**

### 1.1 The old justification does not survive P2-D9

`v2.7` section 2 derived the inertness floor by asking how many moving items the
cluster bootstrap needs before its lower bound clears zero, and answered 7. That
derivation assumes the null has sampling variation. **P2-D9 established that it does
not.**

Under P2-D9 the scorer is an argmax over teacher-forced log-probabilities with no
sampling anywhere. So if the framing truly moves nothing:

```
every item        ΔA_i = 0
every resample    mean = 0 exactly
the interval      [0, 0]
Type I error      exactly 0, not alpha
```

The instrument could not produce a false positive at any rate, which means it was also
not supplying the `alpha`-level protection the floor was described as buying. And in
the other direction, a **single** changed option establishes deductively that the
framing moved something: the item that moved is in the population, so the population
change rate is above zero, with nothing left to infer.

**The bootstrap floor is therefore withdrawn as a justification.** The value 7 is kept,
for the reason in 1.3, but it is no longer presented as a statistical threshold and
must not be described as one.

### 1.2 The bootstrap keeps its role in (b), and the asymmetry is real

This is not a general demotion of the instrument. The two quantities pose different
questions:

| | quantity (a) | quantity (b) |
|---|---|---|
| question | is the population change rate above 0 | do two population rates differ |
| null | a point at the **boundary**, `rate = 0` | a difference in the **interior** |
| what is estimated | nothing; a single mover settles it | both rates, from a finite item sample |
| right instrument | a count against a noise floor | an interval |

P2-D8's bootstrap, its 10,000 resamples and its seed 20260910 are retained **unchanged**
in (b).

### 1.3 The real hazard, and the measurement that sizes it

Floating-point nondeterminism across batch compositions can flip a near-tie argmax, and
T7 runs in a different session and on different hardware from the run that produced
Paper 1's frozen `cond4`. That noise is not zero and is not knowable in advance.

It is also **already being measured, for a purpose that predates this decision**. Under
P2-D1, `F0` is Paper 1's Format V `base` rendering, so `F0`'s prompt is the `cond4`
prompt. T7's `F0`-versus-`cond4` disagreement count is a null perturbation: identical
text, different run. `T7.md` step 2 computes it for the environment-equivalence check.

```
floor = max(7, F0-versus-cond4 disagreement items)
```

**The revision is upward-only by construction**, the rule being a maximum, not by an
instruction a later session could read past. A quiet environment cannot lower the bar.
That is what stops a low measured noise floor from being used to make the movement half
easier to clear after F1 has been seen.

**Why not lower the floor to one**, which is what the deductive argument alone gives.
Because the numerical hazard is real and unmeasured until T7 runs, and setting the
floor at its most permissive value on an untested assumption of noiseless reproduction
is the opposite of conservative. **The provisional 7 is a conservative convention with
no statistical derivation**, and it is labelled as one wherever it appears rather than
inheriting authority from the calculation that no longer supports it.

**The caveat, reported rather than corrected.** `F0` and `cond4` are identical text, so
the `F0` count measures noise under an identical prompt. F1 and F2 are longer prompts
with different batch shapes, so their numerical noise could exceed it. The `F0` rate is
a **lower bound** on the noise floor. It is used as the floor rather than scaled,
because a scaling factor would be invented here with no measurement behind it.

### 1.4 What this closes

`v2.6` section 1.1 argued the no-effect same-option rate of 1.0 from Paper 1's code
path and recorded that it could not be corroborated, because the frozen artifacts
contain no repeated rendering. **T7's `F0` run is that repeated rendering.** The
quantity `v2.6` could only argue, T7 measures, and the measurement is the same number
that sets the floor.

---

## 2. A null on (c) is not a null against chance. **P2-D14**

### 2.1 The contradiction being fixed

`v2.7` section 3.4 licensed a null on (c) as "the direction was not distinguishable
from chance". `v2.7` section 2.1, two sections earlier, measured the content-neutral
sign proportion at **0.2453 to 0.5000**, at or below 0.5 on all seven models and below
it at the corrected `alpha` on one. Calling 0.5 chance contradicts the document's own
diagnostic.

The difference is not cosmetic. It separates a null that means "nothing directional
happened" from one that means "nothing directional happened that was large enough to
cross a baseline measured in the wrong place".

### 2.2 The ruling

**`p0 = 0.5` is retained.** The reasoning in P2-D12's third rejected alternative
stands: recalibrating `p0` to the neutral baseline would recalibrate a preregistered
test against a different manipulation, on a coordinate Paper 1 never used, and would
make a positive F1 result easier to obtain. The conservative direction is kept.

**Its cost is stated with the verdict, not filed as a caveat.** `p0 = 0.5` is
conservative against Type I and costly in Type II. The size of the cost is the gap
between 0.5 and the model's measured neutral baseline:

| model | content-neutral proportion | gap to `p0` | `n_eff` on the `c5` contrast |
|---|---:|---:|---:|
| `CTRL` | 0.2453 | **0.2547** | 53 |
| `L3` | 0.2571 | **0.2429** | 35 |
| `L4` | 0.2909 | **0.2091** | 55 |
| `L1` | 0.4074 | 0.0926 | 27 |
| `L2` | 0.4688 | 0.0312 | 32 |
| `B4` | 0.4875 | 0.0125 | 80 |
| `B2` | 0.5000 | 0.0000 | 42 |

> **Amended licence.** A null on (c) licenses that among the items that moved, the sign
> proportion was not distinguishable from `p0 = 0.5` at the realized `n_eff`. It does
> **not** license "no directional effect", and it does **not** distinguish that from "a
> directional effect that did not clear the gap between 0.5 and the measured
> content-neutral baseline". The gap above is reported with every (c) verdict.

The cost is therefore **large on `CTRL`, `L3` and `L4`, and negligible on `B2`, `B4`
and `L2`**. It is not uniform across the ladder and must not be reported as a single
figure.

---

## 3. `sign(ΔA)` is admissible for the cross-family control. **P2-D15**

### 3.1 The question

`v2.7` section 2.1's diagnostic uses the cross-family control's `ΔA` sign proportion,
and the control is the one model significant at the corrected `alpha`. Paper 1's D111
restricts cross-family comparison to choice-based statistics and bans raw PMI
magnitudes. `ΔA` derives from a magnitude coordinate, so the diagnostic's strongest
single number sat on an unruled question.

### 3.2 D111's mechanism, which is what decides it

D111's stated reason is tokenizer non-identity:

> The L1 to L4 comparison was clean because `tokenizer_identical_across_ladder` held,
> so option strings tokenized identically and log-probability magnitudes were
> commensurable. The cross-family control breaks that by construction. Choice-based
> statistics are computed **within** a model and compared as rates, so they survive the
> change; magnitudes do not.

So the restriction is on quantities that read a model's **log-probabilities**, and the
operational test follows directly:

> **Does the statistic change if the tokenizer changes but the chosen options do not?**

### 3.3 Applying it

`A(o) = (marg_norm(o) - marg_norm(o*_0)) / ext_i`, with `ext_i > 0` a per-item
constant, so

```
sign(ΔA) = sign(marg_norm(o_5) - marg_norm(o_4))
```

an ordinal comparison of two options on frozen item geometry. `marg_norm` is computed
from the item, not from any model. The only model input is **which two options were
chosen**. No log-probability enters, the statistic is computed within a model, and it
is reported as a rate.

**Ruling: admissible.** The same argument is why Paper 1 itself computes `post_norm`
for the control, which is likewise a lookup into frozen geometry indexed by the chosen
option.

**"Derives from a magnitude coordinate" is the wrong test**, and it is what made this
look harder than it is. It applies D111 by the shape of the quantity rather than by its
mechanism, and it would equally forbid `post_norm` for the control.

**What stays inadmissible, named so the ruling cannot be read as a relaxation:**
`logp_sum_chosen`, `logp_neutral_chosen`, and any PMI value, compared across families.
The ruling extends to nothing that reads a model's scores rather than its choice.

### 3.4 The conclusion does not rest on the ruling

Reported both ways regardless. On the six ladder models alone, excluding the control,
the content-neutral sign proportion runs **0.2571 to 0.5000**, still at or below 0.5 on
every one. So a content-neutral insertion does not drift toward the salience pole, and
`p0 = 0.5` remains conservative, whether or not the control's 0.2453 is admitted.

---

## 4. What is not decided here

- **`p0`, `alpha`, the two families of 21, the three-quantity structure, the
  coordinate, the confirmatory item set, `n = 108`.** All unchanged. Section 1 changes
  a justification and a revision rule, not a value or a statistic.
- **P2-D9 through P2-D12.** All stand. Section 1 rests on P2-D9 and supersedes only
  P2-D12's derivation of the floor, not the floor itself or the three-quantity
  structure.
- **D111 generally.** Section 3 rules one statistic admissible on D111's own mechanism.
  It relaxes nothing and names what remains barred.
- **Any new item draw.** P2-D7 declined the one that was open. None is proposed.

## 5. Ordering, disclosed

Section 1 uses no data. Its argument is that a deterministic scorer gives the null zero
variance, which is a property of Paper 1's code established in P2-D9 and not a
measurement made here. The revision rule is fixed before the measurement that triggers
it exists, and it is a maximum, so the measurement can only tighten it.

Sections 2 and 3 use the `c5` sign proportions already computed and reported in `v2.7`
section 2.1. **No new read of Paper 1 output was made for this document.** Section 2
moves a number that was already on the record into the place where the claim it bears
on is made, and section 3 rules on whether one of those numbers may be cited. Both were
raised against `v2.7` rather than discovered in new data, and both are resolved in the
direction that constrains what T7 may claim rather than loosening it.
