# PREREGISTRATION v2.12

**Paper 2: the adversary effect and the RL Scientist**

Version 2.12 · written 2026-09-13 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.11`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
thirteen are read together. This version handles the consequence `v2.11` section 5.1
flagged and declined to resolve: **P2-D12, P2-D14 and P2-D15 all rest on the `c5` neutral
sign proportion being "at or below 0.5 on all seven models", and at P2-D20's item unit
that sentence is false.**

It **does not move `p0`**. It withdraws two universally quantified claims, records what
survives them, and retains `p0 = 0.5` on a ground that uses no measurement. It computes
**no `F1` or `F2` statistic**: every figure is the `c5` contrast on frozen Paper 1 rows,
recomputed here and not transcribed. The `ext_i` floor is untouched and stays open.

| # | decision | where |
|---|---|---|
| 1 | "At or below 0.5 on all seven models" is withdrawn. So is P2-D15's six-ladder restatement of it. | §2, **P2-D21** |
| 2 | `p0 = 0.5` is retained, on the structural ground and not on the withdrawn claim. | §4, **P2-D21** |

**The instruction this acted on**, per `v2.10` section 2.4's countermeasure. The author
stated the problem, named the chain ("the claim is what established that a content-neutral
insert does not drift toward the salience pole, which is what makes p0 = 0.5 conservative,
which is what closed the case for a magnitude gate in P2-D12"), gave four numbered
instructions (recompute the diagnostic at the item unit; trace every passage using the
claim as a premise; apply the P2-D15 mechanism-versus-sentence test to each; rule on
`p0 = 0.5`), offered a reading explicitly "to evaluate not adopt", and constrained the
session: recompute rather than transcribe, leave the `ext_i` floor open, compute no
`F1`/`F2` statistic, and **do not move `p0` even if the session concludes it should**, on
the ordering hazard P2-D12 itself named. The full text is quoted in P2-D21 in
`docs/P2/DECISIONS.md`. This document is written by an agent session acting on that
instruction, not by the author.

---

## 1. The diagnostic, recomputed at P2-D20's unit

`c5` contrast, `size` confirmatory set, 108 items, `alpha = 0.05/21 = 0.002381`. Emitted by
`python3 src/inertness_ceiling.py`.

| model | `n_eff` | positive | proportion | `p` two-sided | significant at corrected `alpha` | 95% exact interval | Type II gap |
|---|---:|---:|---:|---:|---|---|---:|
| `CTRL` | 41 | 8 | 0.1951 | 0.000112 | **yes, downward** | [0.0882, 0.3487] | +0.3049 |
| `B2` | 36 | 20 | **0.5556** | 0.6177 | no | [0.3810, 0.7206] | **-0.0556** |
| `B4` | 63 | 29 | 0.4603 | 0.6147 | no | [0.3339, 0.5906] | +0.0397 |
| `L1` | 27 | 11 | 0.4074 | 0.4421 | no | [0.2239, 0.6120] | +0.0926 |
| `L2` | 31 | 15 | 0.4839 | 1.0000 | no | [0.3015, 0.6694] | +0.0161 |
| `L3` | 33 | 8 | 0.2424 | 0.004551 | no | [0.1109, 0.4226] | +0.2576 |
| `L4` | 43 | 13 | 0.3023 | 0.013718 | no | [0.1718, 0.4613] | +0.1977 |

### 1.1 The three figures in the instruction were checked, not assumed

`B2` at 0.5556, `n_eff` 36, `p` = 0.6177. All three reproduce exactly. They were
recomputed rather than carried across because `v2.10` section 3.6 records three figures
reaching a session through an author instruction, originating in a withdrawn parallel
session, and failing recomputation. An author instruction is a genuine channel that
carries no guarantee about the numbers inside it.

### 1.2 What survives, which is what decides the ruling

**Only `CTRL` departs from 0.5 at the corrected `alpha`, and it departs downward.** That
was true at the pair unit and it is still true at the item unit. `L3` at `p` = 0.004551 and
`L4` at `p` = 0.013718 were not significant at either unit; the corrected `alpha` is
0.002381.

So the finding the claim was introduced to establish, that a content-neutral insertion does
not drift toward the salience pole, **is intact on every model where the diagnostic
resolves anything**. `B2`'s 0.5556 is a point estimate whose exact interval contains 0.5
and whose `p` is 0.6177. It is not evidence of upward drift. It is also not evidence of its
absence.

---

## 2. What is withdrawn. **P2-D21**

> The claim that the `c5` neutral sign proportion is "at or below 0.5 on all seven
> models" is WITHDRAWN. At P2-D20's item unit it is 0.1951 to 0.5556, above 0.5 on
> `B2`, and the six-ladder-model restatement in P2-D15 fails for the same reason,
> because the exception is a ladder model and not the control. `p0 = 0.5` is
> RETAINED, and not on the withdrawn claim. It is retained on the structural ground
> P2-D12 and P2-D14 both stated first and independently of any measurement: moving
> `p0` recalibrates a preregistered test against a different manipulation, on a
> coordinate Paper 1 never used. The empirical gloss is restated per model rather
> than universally: `p0 = 0.5` is conservative on six models, and on `B2` it is not
> established either way, since 0.5556 on `n_eff` 36 carries `p = 0.6177` and a 95%
> exact interval of [0.3810, 0.7206]. Two clauses that reverse on `B2` are withdrawn
> rather than patched. P2-D14's "it would make a positive F1 result easier to obtain"
> is true on six models and false on `B2`, where recalibration would raise `p0`. And
> P2-D14's Type II gap, `0.5` minus the proportion, is `-0.0556` on `B2`: a negative
> gap is not a smaller cost but a different quantity, a Type I exposure the licence
> box has no sentence for, so a `B2` (c) result significant against `p0 = 0.5` but at
> or below 0.5556 is reported with that exposure named. `v2.7` section 5 preregistered
> "a proportion above 0.5 would have been a reason to keep a direction-matched
> reference and to reconsider `p0`"; the antecedent has fired on one model and is
> discharged here by reconsidering and retaining, not by reading the antecedent away.
> Every figure at the pair unit keeps emitting unchanged, because `v2.7` section 2.1
> and `v2.8` section 2.2 publish it and a superseded document must still reproduce.

---

## 3. The trace, with the two failure modes kept apart

Each passage that used the claim as a premise is classified as:

- **case (a)**, a summary of a per-model table, where six of seven carries the argument,
  the sentence is patched and the mechanism is intact; or
- **case (b)**, an argument that depended on universality, where patching the sentence
  would hide a broken argument.

Eight passages. **Four are case (b), and three of those four are not where the instruction
expected them.**

| # | passage | case |
|---|---|---|
| 1 | P2-D12 alternative 1, the magnitude gate | (a) |
| 2 | P2-D12 alternative 3, adopting `c5`'s proportion as `p0` | (a) |
| 3 | P2-D14 alternative 1, recalibrating `p0` | **(b)** |
| 4 | P2-D15's six-ladder restatement | **(b)** |
| 5 | P2-D14's Type II gap and the licence box | **(b)** |
| 6 | `v2.7` section 5's ordering disclosure | **(b)** |
| 7 | `v2.8` section 2.1, P2-D14's "why it needed deciding" | (a) |
| 8 | `v2.7` section 2.1's summary, the artifact's `answer` field, `T7.md` step 0b | (a) |

### 3.1 P2-D12 alternative 1, the magnitude gate. Case (a)

The instruction expected this to be the likeliest case (b). **It is not, and robustly so.**
It rejects the gate because a magnitude gate is blind to direction, which is analytic and
reads no proportion at all. The word "any" in "if any inserted text drifted choices toward
salience" quantifies over inserted text, not over models. The diagnostic is what the gate
was a poor proxy FOR; it is not a premise of the argument that the proxy is poor.

### 3.2 P2-D12 alternative 3, adopting `c5`'s proportion as `p0`. Case (a)

Two grounds, and they are separable. The structural one, that moving `p0` recalibrates a
preregistered test against a different manipulation on a coordinate Paper 1 never used,
uses no measurement and holds at any proportion. The measured range is the gloss, not the
reason. The rejection stands unchanged.

### 3.3 P2-D14 alternative 1, recalibrating `p0`. Case (b) at the clause level

Its stated ground includes "it would make a positive F1 result easier to obtain". That is
true on the six models whose baseline sits below 0.5 and **false on `B2`**, where
recalibration would raise `p0` and make a positive result harder. "The conservative
direction is kept" reverses on `B2` for the same reason.

The rejection still stands, on the structural clause that precedes both. The two clauses
that reverse are withdrawn rather than patched.

### 3.4 P2-D15's six-ladder restatement. Case (b)

P2-D15 restates the conclusion on the six ladder models with the control removed, in order
to show that its own D111 admissibility ruling is not load-bearing. That restatement is a
universally quantified sentence over six models, and `B2` breaks it.

**It fails on a ladder model, not on the control**, so removing the control does not rescue
it. This is the sharp part: the fallback breaks in the one place its purpose does not
reach.

**P2-D15's ruling itself is untouched.** It is an argument about tokenizers and reads no
proportion, and the control moves further below 0.5 at this unit, 0.2453 to 0.1951. So the
ruling is still not load-bearing for the direction P2-D15 was about. What fails is a
sentence, and the fix is the per-model statement in section 1.2 rather than a smaller
universal.

### 3.5 P2-D14's Type II gap and the licence box. Case (b), and the largest finding

The gap is `0.5` minus the proportion and P2-D14 calls it a Type II cost. **On `B2` it is
-0.0556.**

A negative gap is not a smaller cost. It is a different quantity. There is no gap between
`p0` and the baseline for a real effect to fail to clear. The exposure reverses: a `B2`
result significant against `p0 = 0.5` but at or below 0.5556 is nominally positive while
sitting at or below what a content-neutral insert does. **That is Type I, and P2-D14's
amended licence box has no sentence for it.**

`src/armb_floor.py` already carried, before this session, the assertion
`all(v["gap_to_p0"] >= 0 for v in g.values())` with the message "a neutral baseline sits
above p0 = 0.5; the Type II statement reverses". **The codebase named this failure mode
before it occurred.** The assertion is retained unchanged as a guard on the published
pair-unit figures, and `type_ii_gap_item` is added beside it with the sign carried
explicitly.

### 3.6 `v2.7` section 5's ordering disclosure. Case (b), and the passage the instruction does not name

`v2.7` section 5 preregistered both answers before the number was seen:

> a proportion above 0.5 would have been a reason to keep a direction-matched reference and
> to reconsider `p0`, and a proportion at or below 0.5 makes `p0 = 0.5` conservative. It
> came out the second way and `p0` was left alone

**That is a conditional with a preregistered consequent, and at the governing unit its
antecedent has fired on one model.** Patching the surrounding sentence would leave a fired
trigger unremarked, which is worse than the wording error, because the trigger was written
precisely so that this case could not be absorbed silently.

It is discharged by performing the reconsideration, which is section 4, and concluding that
`p0` stands. It is not discharged by reading the antecedent away, and it is not discharged
by observing that the firing model is not significant: the conditional's antecedent is
stated on the proportion, not on significance.

### 3.7 `v2.8` section 2.1, P2-D14's "why it needed deciding". Case (a), mechanism strengthens

Its point is that 0.5 is not the neutral baseline, so a null on (c) is not a null against
chance. At the item unit the range is 0.1951 to 0.5556, so 0.5 is still not the baseline,
and `B2` sitting above it is a second, independent way the word "chance" is wrong. The
argument is stronger than it was.

### 3.8 The summary sentences. Case (a) on the mechanism, false as worded

`v2.7` section 2.1, the `answer` field in `results/T5_inertness_ceiling.json`, and
`docs/P2/tasks/T7.md` step 0b. `v2.7` section 2.1's clause "where it departs from 0.5 it
departs downward" is **false on the point estimate** and **true on every departure that
resolves**. T7 step 0b additionally lists the pair-unit per-model gaps as a set of
non-negative numbers and is superseded for those figures.

---

## 4. The ruling: `p0 = 0.5` stands

Four reasons, of which **only the third is empirical**.

1. **The structural ground is untouched and independently sufficient.** Moving `p0`
   recalibrates a preregistered test against a different manipulation, on a coordinate
   Paper 1 never used. Both P2-D12 and P2-D14 state it first, and it holds at any measured
   proportion.
2. **Ordering.** Moving a preregistered null while holding the corrected diagnostic, with
   the per-model `n_eff` on the table, is the hazard P2-D12 named when it declined the same
   move. The instruction forbade it in this session for that reason, and the reason is good
   independently of the instruction.
3. **The exception carries no evidence.** 0.5556 on `n_eff` 36 gives `p` = 0.6177 and an
   interval of [0.3810, 0.7206]. One model of seven above 0.5 at that `p` is what sampling
   noise produces when the true baseline sits at or a little below 0.5.
4. **A per-model `p0` would be seven nulls where the design has one**, which multiplies
   exactly the degrees of freedom a single fixed `p0` exists to remove.

### 4.1 What does NOT follow, stated because the obvious repair is wrong

**"Six of seven are at or below 0.5, so `p0 = 0.5` is still conservative" does not follow.**

Conservativeness is a per-model property. Six models being conservative leaves the design
conservative on six models and, at the point estimate, anti-conservative on `B2`. The
defence of `p0` no longer runs through conservativeness. It runs through reasons 1, 2 and
4, with reason 3 saying only that the exception is unresolved rather than that it is
absent.

Substituting the aggregate claim for the per-model one would be patching the sentence and
keeping a mechanism that no longer holds, which is the failure this version exists to
prevent.

### 4.2 The session did not conclude `p0` should move

Stated explicitly because the instruction required the session to stop if it had. It did
not. `p0 = 0.5` is retained on the reasoning above, not deferred.

---

## 5. The author's read, evaluated

The author offered a reading marked "to evaluate not adopt":

> The conclusion survives and the wording does not. 0.5556 at p = 0.6177 is not evidence of
> upward drift, and six of seven remain at or below 0.5, so p0 = 0.5 stays defensible as
> conservative. But "all seven" must go everywhere it appears, and the magnitude-gate
> argument in P2-D12 needs re-reading rather than re-asserting.

**Agreed:** the conclusion survives and the wording does not. `p0 = 0.5` stands. "All
seven" goes everywhere it appears.

**Not adopted, on two points.**

1. **"`p0 = 0.5` stays defensible as conservative" is the one clause that does not carry
   over.** Conservativeness is per model, and on `B2`'s point estimate the design is
   anti-conservative. `p0` is defensible, and section 4 defends it, but not on that ground.
   This is the distinction between patching a sentence and re-deriving an argument that the
   author's own step 3 asks for, applied to the author's own summary.
2. **The magnitude-gate argument is where the damage is not.** The instruction expected
   P2-D12's alternative 1 to be the most exposed passage. It is case (a) and robustly so:
   it is analytic and reads no proportion. The four case (b) passages are P2-D14's
   recalibration clauses, P2-D15's six-ladder restatement, P2-D14's Type II gap, and
   `v2.7` section 5's fired conditional. **Three of the four are passages the instruction
   does not name**, and the fourth, the gap, was named only as a possibility.

The evaluation is recorded rather than silently absorbed because the instruction asked for
it and because a session that agrees with an author's read without checking where it is
wrong is not doing the step the instruction set.

---

## 6. What is bound and what is emitted

`inertness_ceiling._item_reading` gains `significant_at_corrected_alpha_item`,
`type_ii_gap_item` (SIGNED) and `ci95_item`. `inertness_ceiling.main` emits
`diagnostic_c5_direction.answer_at_item_unit_p2d21` beside the existing `answer`.
`armb_floor` gains `type_ii_gap_item`, `type_ii_cost_of_p0_half_at_item_unit` and
`_six_ladder_at_item_unit` beside the pair-unit blocks.

**Every pre-existing value in `results/T5_inertness_ceiling.json` and
`results/T5_armb_floor.json` is byte-identical**, verified by walking the old artifact
against the new for lost keys and changed values. `v2.7` sections 2.1 and 3.2 and `v2.8`
sections 2.2 and 3.4 publish those figures and a superseded document must still reproduce.
Each new figure carries a field naming the unit it is on.

`p2_decisions.bind_neutral_baseline` is called by both scripts. It fails a run that
re-asserts either withdrawn sentence, and it checks the **sign** of each item-unit gap
against the recorded set of models whose baseline sits above `p0`, because the sign decides
whether the number describes a Type II cost or a Type I exposure.

`armb_floor.demo` keeps the pair-unit assertions as reproduction guards and adds the live
item-unit ones. `tests/test_armb_binding.py` asserts the recomputed table, that `B2`'s
interval still contains 0.5, and that both withdrawn sentences stay withdrawn.

---

## 7. What this version changes

| | |
|---|---|
| `p0` | **0.5, unchanged.** Not moved, not deferred |
| "at or below 0.5 on all seven models" | **withdrawn**, recorded as False rather than deleted |
| P2-D15's six-ladder restatement | **withdrawn**; the ruling under it is untouched |
| P2-D14's "makes a positive F1 result easier to obtain" and "the conservative direction is kept" | withdrawn as stated; the rejection they supported stands on its structural clause |
| P2-D14's Type II gap | now SIGNED. Negative on `B2`, where the exposure is Type I and the licence box has no sentence |
| P2-D12 alternatives 1 and 3 | unchanged, mechanisms intact |
| P2-D15's admissibility ruling, P2-D20's unit, P2-D13's floor, the three quantities | untouched |
| `v2.7` §5's preregistered conditional | antecedent fired; discharged by reconsidering and retaining |
| `T7.md` step 0b | superseded for the per-model gap figures it lists |
| the `ext_i` floor | untouched, still open |
| any `F1` or `F2` statistic | none computed in this version |
