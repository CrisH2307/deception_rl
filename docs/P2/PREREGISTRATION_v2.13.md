# PREREGISTRATION v2.13

**Paper 2: the adversary effect and the RL Scientist**

Version 2.13 · written 2026-09-13 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.12`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
fourteen are read together. This version fixes **how** the corrected neutral-baseline
claim is stated, and records a measurement `v2.12` left as an open exception.

It changes **no ruling**. `p0` is still 0.5. The two universal claims `v2.12` withdrew
stay withdrawn. P2-D20's unit, P2-D15's admissibility ruling, P2-D13's floor and the
three-quantity structure are untouched. It computes **no `F1` or `F2` statistic**. The
`ext_i` floor stays open.

| # | decision | where |
|---|---|---|
| 1 | The claim is stated directly, never as a tally. "Six of seven" is forbidden, not preferred against. | §2, **P2-D22** |
| 2 | `B2` is AT the null. Measured across five aggregations, not conceded. | §3, **P2-D22** |
| 3 | "Conservative" is withdrawn as a justification for `p0 = 0.5` everywhere it is offered as one. | §4, **P2-D22** |

**The instruction this acted on**, per `v2.10` section 2.4's countermeasure. The author
instructed that the claim not be restated as "at or below 0.5 on six of seven models",
because "that keeps universality as the frame and leaves an exception a reader cannot
resolve"; that the central claim be stated directly, with the per-model distribution,
only `CTRL` resolving and downward, and `B2` not distinguishable from the null; and that
"conservative" be dropped as a justification for `p0` everywhere it appears, "per your own
correction that conservativeness is a per-model property". On `B2` the author offered a
reading and required it be verified rather than assumed: "If it holds, state it wherever
B2's exception appears: a model at the null whose point estimate falls either side
depending on aggregation, not a model that drifts upward. If it does not hold, say so." The
full text is quoted in P2-D22 in `docs/P2/DECISIONS.md`. This document is written by an
agent session acting on that instruction, not by the author.

---

## 1. What `v2.12` got half right

`v2.12` withdrew "at or below 0.5 on all seven models" and established that
conservativeness is a per-model property that does not hold on `B2`. Then, in its own
prose, it went on saying "six models" and "conservative on six models".

Both are the same half-measure. A false universal was replaced with a true tally, and a
word that had just been shown not to apply was kept for the models it still applied to.
Neither is wrong as arithmetic. Both keep the shape of the error.

---

## 2. The claim is stated directly. **P2-D22**

> The neutral-baseline claim is stated directly and never as a tally. "At or below 0.5
> on six of seven models" is NOT the replacement for the withdrawn "all seven": it keeps
> universality as the frame and leaves a reader an exception they cannot resolve. The
> claim is: the content-neutral baseline does not drift toward the salience pole. It is
> stated with the per-model distribution, 0.1951 to 0.5556 at P2-D20's item unit, with
> the fact that only `CTRL` resolves at the corrected `alpha` and resolves downward, and
> with `B2` at the null. `B2` IS AT THE NULL, and that is a measured claim rather than a
> concession: across five aggregations of the same frozen rows its point estimate is
> exactly 0.5000 under three and 0.5556 under two, `p` is 1.0000 under three and 0.6177
> under two, every 95% exact interval contains 0.5, two votes of 36 return the item-unit
> estimate to 0.5000, and `B2` is the only model whose point estimate changes side
> between the pair unit and the item unit. It is therefore described as a model sitting
> at the null whose point estimate falls either side depending on aggregation, and never
> as a model that drifts upward. Separately, "conservative" is WITHDRAWN as a
> justification for `p0 = 0.5` everywhere it is offered as one, because
> conservativeness is a per-model property and the design is not conservative on `B2` at
> the point estimate. `p0 = 0.5` stands on the structural ground, on the ordering
> hazard, and on a single fixed null being the point of having one. Superseded
> documents keep their wording and their emitted strings unchanged, because `v2.7`,
> `v2.8` and the artifact fields they publish must still reproduce; this governs live
> prose, live briefs and every figure emitted at P2-D20's unit.

### 2.1 Why the tally frame is forbidden and not merely discouraged

"At or below 0.5 on six of seven models" is a **smaller universal**. It tells a reader
that six models satisfy a property and one does not, and gives them no way to resolve the
one. A reader meeting that sentence has to decide for themselves whether the seventh is a
problem.

The honest answer, that the seventh is a model sitting at the null, is exactly what the
tally omits. So the tally is not a weaker version of the truth; it withholds the part that
resolves the reader's question while appearing to be complete.

### 2.2 The statement that replaces it

> The content-neutral baseline does not drift toward the salience pole. At P2-D20's item
> unit the per-model proportion runs 0.1951 to 0.5556. Only `CTRL` resolves at the
> corrected `alpha`, and it resolves downward. `B2` sits at the null.

Three facts and no quantifier over models. Every model's number is given, so there is
nothing for a reader to take on trust and no exception left dangling.

---

## 3. `B2` is at the null, and this was checked

The instruction asked for the reading to be verified, not assumed. Five aggregations of
the same frozen `c5` rows, **named before any was computed**, and all five reported
whatever they gave.

`A` is the pair unit with an exact zero test, which `v2.7` section 2.1 publishes. `B` is
the pair unit at P2-D19's `EPS`. `C` is P2-D20's adopted rule, the item unit on the mean of
pair `ΔA` at `EPS`. `D` is the item unit on the mean with an exact zero test. `E` is the
item unit by majority of pair signs, with an item dropped when its two pairs split one and
one.

| aggregation | `B2` | proportion | `p` | 95% exact interval |
|---|---:|---:|---:|---|
| `A` pair, exact | 21/42 | **0.5000** | 1.0000 | [0.3419, 0.6581] |
| `B` pair, `EPS` | 21/42 | **0.5000** | 1.0000 | [0.3419, 0.6581] |
| `C` item, mean, `EPS` (adopted) | 20/36 | 0.5556 | 0.6177 | [0.3810, 0.7206] |
| `D` item, mean, exact | 20/36 | 0.5556 | 0.6177 | [0.3810, 0.7206] |
| `E` item, sign majority | 15/30 | **0.5000** | 1.0000 | [0.3130, 0.6870] |

### 3.1 The reading holds, and more sharply than it was put

**`B2` is exactly 0.5000 under three of the five**, including `E`, which is an **item**
aggregation. So this is not the pair unit disagreeing with the item unit. Two defensible
aggregations at the **same** unit put `B2` on opposite sides of 0.5.

Every interval contains 0.5. Two votes of 36 return `C` to exactly 0.5000. And `B2` is
**the only model of the seven whose point estimate changes side between the pair unit and
the item unit**; the other six keep their side under every aggregation.

A quantity that lands exactly on its null under three readings of the same data, is never
distinguishable from it under any, and moves off it by two votes, is a quantity at the
null. It is stated that way, and "a small upward departure that does not reach
significance" is rejected as a description because it reports a direction the data does not
carry.

### 3.2 `E` is not a candidate unit and P2-D20 is not reopened

P2-D20 fixed the unit and its reasoning is untouched. `E` is a robustness probe on where
`B2` sits, run because the instruction required verification. **No figure is taken from
`B`, `D` or `E`.** Reporting that two aggregations disagree on `B2`'s side is evidence
about `B2`; it is not an argument for either aggregation, and it would be a misuse of this
section to read it as one.

---

## 4. "Conservative" is withdrawn as a justification for `p0`

`v2.12` established that conservativeness is a per-model property and that the design is
not conservative on `B2` at the point estimate, then kept using the word for the six. The
word goes.

**`p0 = 0.5` stands on three grounds, none of which needs it:**

1. **Structural.** Moving `p0` recalibrates a preregistered test against a different
   manipulation, on a coordinate Paper 1 never used. Independently sufficient, and it
   holds at any measured proportion.
2. **Ordering.** Moving a preregistered null while holding the corrected diagnostic is the
   hazard P2-D12 named when it declined the same move.
3. **One null.** A per-model `p0` would be seven nulls where the design has one, which
   multiplies exactly the degrees of freedom a single fixed null exists to remove.

Where a Type II cost is real it is reported as a **signed per-model gap**, which says more
than the adjective did: `CTRL` +0.3049, `L3` +0.2576, `L4` +0.1977, `L1` +0.0926, `B4`
+0.0397, `L2` +0.0161, `B2` **-0.0556**. A reader can size the cost per model instead of
being told a word that holds on six of them.

---

## 5. What is changed and what is not

### 5.1 Changed: live prose, live briefs, and strings emitted at P2-D20's unit

| site | what changed |
|---|---|
| `inertness_ceiling` module docstring | the direct statement replaces "survives on six models" |
| `answer_at_item_unit_p2d21.what_survives` | direct statement plus `B2`'s five-aggregation position |
| `answer_at_item_unit_p2d21.p0_is_retained_on` | "conservative" withdrawn, signed gap named instead |
| `armb_floor` `type_ii_cost_of_p0_half_at_item_unit.statement` | "conservative on the six" replaced by the per-model signed gap |
| `_six_ladder_at_item_unit.replacement` | tally replaced by the direct statement |
| `docs/P2/tasks/T7.md` step 0b | rewritten: direct statement, signed item-unit gaps, `B2`'s Type I exposure named, "do not justify `p0` by calling it conservative" |
| P2-D21's decision text and its reason 3 | amended in `DECISIONS.md`; the ruling is unchanged |

### 5.2 Not changed: everything a superseded document publishes

`v2.7` sections 2.1 and 5, `v2.8` sections 2.1 and 2.2, `armb_floor.type_ii_gap`'s
docstring and `type_ii_cost_of_p0_half.statement`, `d111_verdict`'s pair-unit block, and
`inertness_ceiling`'s pair-unit `answer` all keep their wording exactly. Editing them so
one sentence holds everywhere would break the reproduction guarantee in order to remove a
supersession note, which is the trade D148 exists to refuse.

**Verified mechanically against the previous commit:** no key lost, **no numeric value
changed**, in either `results/T5_inertness_ceiling.json` or `results/T5_armb_floor.json`.
Exactly four prose fields were restated, all four added at P2-D20's unit by P2-D21, and no
preregistration quotes any of them.

---

## 6. What is bound

`p2_decisions.bind_neutral_claim_wording(tally_frame_used, conservative_justifies_p0,
b2_described_as_drifting)` is called by `inertness_ceiling.main` and `armb_floor.main`.
Three separate failures, because they mean different things: a tally frame keeps
universality and hands the reader an unresolved exception; "conservative" as `p0`'s
justification asserts a per-model property of the design that does not hold on `B2`; and
describing `B2` as an upward departure reports a direction the data does not carry.

It also re-derives, from `P2D22_B2_AGGREGATIONS`, which aggregations put `B2` exactly at
0.5, and fails if that set is not `A`, `B`, `E`. The at-the-null reading rests on that set,
so it is bound rather than described.

---

## 7. A note on bindings, recorded in `DECISIONS.md` rather than here

`src/armb_floor.py` carried, from the session that wrote P2-D14 and long before P2-D20
changed quantity (c)'s unit, the assertion `all(v["gap_to_p0"] >= 0 for v in g.values())`
with the message "a neutral baseline sits above p0 = 0.5; the Type II statement reverses".

When the unit changed and `B2`'s gap went negative, that assertion **had already named the
consequence**: not that a number would be out of range, but that the Type II statement
reverses, which is what P2-D21 then had to work out from scratch. Nobody re-derived it; the
assert had it written down, with its reason, before the event.

The general form is now recorded in `DECISIONS.md` beside the mechanism note: **an
assertion that encodes WHY a quantity has the sign or shape it does is worth more than one
that checks a value.** A value check tells a later session that something moved. A reason
check tells it what breaks, and it survives the change of unit, tolerance or estimator that
makes the value check stale.

---

## 8. What this version changes

| | |
|---|---|
| `p0` | **0.5, unchanged.** Not moved, not deferred |
| the withdrawn universal claims | still withdrawn; the replacement is a direct statement, not a tally |
| "six of seven" as a restatement | **forbidden** |
| "conservative" as `p0`'s justification | **withdrawn** everywhere it is offered as one |
| `B2` | **at the null**, measured across five aggregations, not an open exception |
| Type II cost | reported as a signed per-model gap |
| P2-D20's unit, P2-D15's ruling, P2-D13's floor, the three quantities | untouched |
| superseded documents and every figure they publish | unchanged and still reproducing |
| the `ext_i` floor | untouched, still open |
| any `F1` or `F2` statistic | none computed in this version |
