# PREREGISTRATION v2.15

**Status.** New file per D148. `v2.0` through `v2.14` are not edited. This version rules
one question: what Arm B may conclude from quantity (c)'s five resolving cells, given
P2-D5's unruled blocker, the measured neutral baseline, and the switch concentration, all
three at once.

**Decided by an agent session acting on an author instruction**, per the countermeasure in
`v2.10` section 2.4. The session is not the author. It wrote this document and P2-D24 from
the instruction quoted in section 1, and every number below is recomputed from the
artifacts rather than carried from the instruction.

**Scope of the ruling.** It rules what may be concluded. It does NOT rule P2-D5's blocker,
which stays open and stays the author's: section 6 shows the ruling holds under all three
readings of that blocker, which is why it can be made without pre-empting it. It does not
move `p0`. It does not reopen P2-D6, P2-D12, P2-D14, P2-D19, P2-D20 or P2-D21. It computes
no new statistic.

---

## 1. The instruction

Quoted in the parts that bear on the ruling.

> Quantity (a) clears P2-D13's floor on all 14 cells, 30 to 77 items of 108. Five cells
> resolve on (c) at the corrected alpha, all downward, meaning away from `o*_infinity`.
> Three inputs stand against reading those five as a result, and **none can be ruled
> alone**:
>
> 1. **P2-D5's blocker.** No adversary-relevant claim rests on `A` under a single framing.
>    (a) and (b) read chosen options only; (c)'s baseline is the same-option distribution,
>    not `A_null(m,F) = sum_o p_{m,F}(o) A_i(o)`. Treating a framing contrast against a
>    same-option baseline as an excess is a substantive ruling, since `A_null` is a
>    marginal over canonical option ids and a same-option baseline is not that object.
> 2. **The neutral baseline.** `c5` also departs downward where it resolves (CTRL 0.1951,
>    L3 0.2424 at the item unit), so downward departure may be a property of inserted text
>    rather than of adversary content. Reading F1/F2 against those figures is the
>    recalibration P2-D12 and P2-D14 declined and P2-D21 retained `p0` through, performed
>    in the reporting rather than in the null.
> 3. **The concentration.** The 0.0519 per-pair bound is not a bound: the tied-switch
>    ratio runs 0.00 to 5.10 across models, pooled 0.0726, and CTRL/F2 loses 14 of 50
>    switches to `A`-invisibility. Two of the five resolving cells (CTRL/F1, L3 both arms)
>    sit in the concentrated group, so their `n_eff` is formed after the coordinate
>    discards switches it cannot see, at 2 to 5 times the anticipated rate. This is
>    selection, not measurement error: nothing establishes the discarded switches carry
>    the direction of the retained ones.
>
> **What does the design license concluding from the five downward departures, given all
> three at once?** Ruling any one alone licenses a reading the other two forbid, which is
> why they come together.

Three readings were offered **to evaluate, not to adopt**:

> - H-B's null half is refuted by (a) and (c) says nothing interpretable, so the paper
>   reports movement without direction.
> - The departures are interpretable against the neutral baseline and the concentration is
>   a stated limitation on two cells.
> - Nothing about direction is licensed and (c) is reported as computed, with all three
>   limits attached.

The constraints: compute no new statistic; treat every number in the instruction as
unverified; do not move `p0`; do not reopen P2-D6, P2-D12, P2-D14, P2-D19, P2-D20 or
P2-D21; name any quantity a reading needs that was never computed and say whether computing
it now would be preregistered or post-hoc; and if the design licenses nothing about
direction, say so. All were followed.

---

## 2. Every number in the instruction, recomputed

Per `v2.10` section 3.6, which records three figures that reached a session through an
author instruction and did not reproduce. Nothing here is transcribed.

| carried | recomputed | source | verdict |
|---|---|---|---|
| (a) clears the floor on all 14 cells | all 14 `clears_the_floor` true | `results/T7_armb_quantities.json` | **reproduces** |
| 30 to 77 items of 108 | min 30 (`L1`/F1), max 77 (`B4`/F2) | same | **reproduces** |
| five cells resolve on (c) | `CTRL`/F1, `L3`/F1, `L4`/F1, `L3`/F2, `L4`/F2 | same, `significant_at_corrected_alpha_item` | **reproduces** |
| all five downward | 0.1667, 0.1915, 0.2174, 0.2456, 0.2131, every one below 0.5 | same | **reproduces** |
| `c5` departs downward where it resolves, `CTRL` 0.1951 **and `L3` 0.2424** | `CTRL` 0.1951 at `p` = 0.000112 resolves; **`L3` 0.2424 at `p` = 0.004551 does NOT resolve** at `alpha` = 0.002381 | `results/T5_inertness_ceiling.json`, `significant_at_corrected_alpha_item` | **FAILS on `L3`** |
| per-pair bound 0.0519 | 84 / 1,620 = 0.05185 | `results/T7_switch_concentration.json` | reproduces |
| ratio runs 0.00 to 5.10, pooled 0.0726 | 0.00 to 5.10; 62 / 854 = 0.0726 | same | reproduces |
| `CTRL`/F2 loses **14 of 50 switches** | 14 of 50 **items**: `CTRL`/F2 has 54 switches, 17 on tied pairs, and 14 of its 50 moved items carry `ΔA` = 0 | same | **unit is wrong**, the counts are right |
| **two** of the five resolving cells are concentrated | **three**: `CTRL`/F1, `L3`/F1, `L3`/F2. The parenthetical names all three and calls them two | same | **FAILS as a count** |
| at **2 to 5** times the anticipated rate | **1.81 to 4.09** on those three cells (4.09, 2.50, 1.81). 1.81 to 5.10 is the range over all six concentrated cells, and 5.10 is `CTRL`/F2, which does not resolve | same | **FAILS as a range** |

### 2.1 The `L3` failure is the one that matters

P2-D21's adopted decision text says "only `CTRL` resolves at the corrected `alpha` and it
resolves downward". The artifact agrees: `L3`'s `c5` item-unit `p` is 0.004551 against
`alpha` = 0.002381, and `significant_at_corrected_alpha_item` is false. The same error is
in `docs/P2/DECISIONS.md`'s open-question note, written 2026-09-14, which is where the
instruction's wording came from. It is corrected there with a dated line pointing here.

It cuts both ways and both are recorded.

- It **weakens** the empirical case that inserted text departs downward: the evidence is
  one model of seven, not two.
- It **weakens reading 2 further**, and this is the larger effect. Reading 2 needs a
  neutral figure to read an F1/F2 proportion against. On four of the five resolving cells
  the model is `L3` or `L4`, and neither model's neutral figure resolves at the corrected
  `alpha`. Reading a resolved departure against an unresolved point estimate is precisely
  what P2-D22 forbade in the tally case: it hands the reader an exception they cannot
  resolve.

### 2.2 Two other wordings that do not survive verification

**"The framings move choices substantially"** (`DECISIONS.md`, open-question note).
"Substantially" is a magnitude word, and magnitude is quantity (b), which P2-D12 makes
descriptive and which resolves on 3 of the 14 cells. The framing-minus-`c5` difference runs
-0.1620 to +0.0648 with half-widths 0.0787 to 0.1275, and the three intervals that exclude
zero are `L3`/F1 at -0.1065, `B2`/F2 at -0.1481 and `L3`/F2 at -0.1620, all negative, which
is the framing changing the chosen option on MORE pairs than `c5` does. So a magnitude
statement is licensed, and it is narrower and more specific than the adjective: on three
cells of fourteen the framing moves choices more than a known-effective content insertion in
the same slot does, and on the other eleven the comparison does not resolve. The bare word
"substantially" reports the resolved three and the unresolved eleven as one thing.

**"(c)'s baseline is the same-option distribution"** (instruction, input 1). (a) and (b)
use same-option rates. (c)'s baseline is `p0 = 0.5` on the sign of the within-item mean
`ΔA` among items with `|mean ΔA| > EPS`. The instruction's substantive point survives the
correction and is adopted: neither a same-option rate nor `p0 = 0.5` is `A_null`. But the
ruling turns on which object is being compared to which, so the object is named correctly.

---

## 3. The three inputs are three views of one hole

The instruction says none can be ruled alone. That is right, and the reason is stronger
than "they interact": all three are the same gap seen from three sides. The gap is that
**the design's preregistered defence against "the movement is a generic inserted-text
shift in option preference" is a quantity quantity (c) does not carry.**

`v2.0` section 4.4 states that defence in full. Take the option-frequency shift measured on
the `beta_c = infinity` control set, where the optimal signal does not change and there is
nothing adversary-relevant to move toward, apply it as a reweighting on the confirmatory
set, and compute the displacement it predicts:

```
ΔA_null(m, F) = sum_o ( p_{m,F}^{ctrl}(o) - p_{m,F0}^{ctrl}(o) ) * mean_i A_i(o)
```

`v2.0` section 4.4 then required a confirmatory tracking claim to clear it: "Movement that
a generic prompt-induced shift in option preference already explains is reported as prompt
sensitivity and named as such." P2-D6 replaced the mean with a sign test and P2-D12 fixed
three quantities, and no successor to that cap was written.

Read against that:

- **Input 1 is the gap stated as a rule.** P2-D5 makes the excess conjunct binding on every
  adversary-relevant claim, and the confirmatory family contains no excess quantity.
- **Input 2 is the gap with a measurement in it.** A content-neutral insert in the same
  slot produces a downward departure on the model where its diagnostic resolves. That is an
  observed instance of exactly the generic shift the cap existed to subtract.
- **Input 3 is the gap in the geometry.** The switches the coordinate discards are 54 of 62
  on one option-index pair, (4,5), at the end of the option order, which is the signature a
  generic option-position shift would have. On three of the five resolving cells the
  discarded share runs 1.81 to 4.09 times the per-pair bound.

They point the same way because they are the same absence. That is why ruling one alone
licenses a reading the other two forbid, and section 5 works each case.

---

## 4. What the missing quantity is, where it is specified, and its status

**`A_null(m, F) = sum_o p_{m,F}(o) * A_i(o)`.** Specified in `v2.0` section 3.3 as the
fourth member of the reference set, restated in `v2.3` section 1.2, and named by P2-D5's
decision text. `v2.0` section 3.3 defines **excess** as `A_observed - A_null`.

**`ΔA_null(m, F)`.** Specified in `v2.0` section 4.4 as the attribution cap, computed from
the control set as above.

**Neither has ever been computed for Paper 2.** No module emits either: the only quantity
in the Arm B results with "marginal" in its name is `tv_option_marginal`, the total
variation distance between two option marginals, which `src/c5_effect.py` forms and which
is neither object. `docs/P2/tasks/T7.md` step 4 (the `beta_c = infinity` control) and step
5 (place every model against the marginal null) both require them, and neither step has
been run.

**Status if computed now. The two halves separate and the distinction is the crux of
reading 2.**

1. **Computing `A_null` and `ΔA_null` as `v2.0` specifies them is PREREGISTERED.** Both
   formulas were fixed before any Paper 2 data existed, both are named in T7's own brief as
   required steps, and neither has a free parameter. Running them is unrun preregistered
   work, not a new quantity.
2. **Using either to license a direction claim on quantity (c) would be POST-HOC.** No
   preregistered rule maps a level excess, in `A` units, onto a sign-test proportion.
   P2-D5's conjunct and `v2.0` section 4's criterion were both written against mean `ΔA`,
   which P2-D6 demoted. The mapping would be written now, with the five resolving cells and
   their directions on the table, which is the ordering hazard P2-D21 reason 2 names and
   P2-D12 named before it.

This version authorizes neither. Running T7 steps 4 and 5 is T7's business and is not
blocked by P2-D24; what P2-D24 blocks is a direction claim, and a post-hoc bridge from a
level excess to a sign proportion would not unblock it. Whether P2-D5's conjunct travels to
the new quantities at all remains the open question `DECISIONS.md` records, and it is the
author's.

---

## 5. The three readings, evaluated

### 5.1 Reading 1: refuted null half, movement without direction. Partly adopted

Its second and third clauses are the ruling. Its first clause is declined on two grounds
and neither is a quibble.

**"Refuted" is a verdict on H-B, and verdicts on H-B are what the blocker blocks.** H-B is a
conjunction: little or no movement, and any movement uncorrelated with the correct
direction. Quantity (a) resolves the first half and the design currently says nothing about
the second, so the conjunction is not refuted; one half of it is. Reporting "H-B's null half
is refuted" invites the reader to complete the conjunction, which is the sentence nothing
licenses.

**"(c) says nothing interpretable" is too strong in the other direction.** (c) is computed,
exact, reproducible from a committed seed, and reported in full with its `n_eff`, its
realized power, its signed Type II gap and its attrition. What is unlicensed is one
interpretation of its sign, not the statistic. `CLAUDE.md` is explicit that numbers are not
withheld; P2-D12's emission requirement is unchanged.

**What of (a) is adopted.** Quantity (a) reads chosen options only, makes no claim about
adversary-relevant content, and is therefore outside P2-D5's reach entirely. Under P2-D9
the no-effect rate is exactly 1.0 and not estimated, so a changed option is deductive
evidence that the framing moved something. All 14 cells clear P2-D13's floor of 7 at 30 to
77 items of 108. That is the strongest single result Arm B currently has and it is stated
as movement, not as a verdict.

### 5.2 Reading 2: interpret against the neutral baseline, limit the concentration. Rejected

Four grounds, in order of weight.

1. **The neutral baseline resolves on one model of seven, and on none of the four `L3` or
   `L4` resolving cells.** Section 2.1. Reading a resolved departure against an unresolved
   point estimate produces a comparison with no error rate, on four of the five cells the
   reading exists to interpret.
2. **It is the recalibration three decisions declined, moved to a place with no test.**
   P2-D12 alternative 3, P2-D14 alternative 1 and P2-D21 alternative 1 all refused to move
   `p0` to the measured neutral proportion, on the structural ground that it recalibrates a
   preregistered test against a different manipulation on a coordinate Paper 1 never used.
   Performing the same recalibration in the reporting is worse, not better: moving `p0`
   would at least be a stated null tested at a stated `alpha`, while a reporting-level
   comparison has neither. It also inherits the ordering hazard in full, because it would be
   adopted with the five resolving cells on screen.
3. **It miscounts the concentration and mislabels it.** Three of the five resolving cells
   are concentrated, not two, and the report it rests on says the concentration is selection
   rather than measurement error: "nothing in the current design establishes that the
   discarded switches carry the same direction as the retained ones." A limitation is what
   attaches to an estimate one still believes. A selection whose direction is unknown is a
   reason not to have the estimate.
4. **It leaves input 1 unanswered.** Even granted a neutral comparison, the object compared
   is a sign proportion and `A_null` is a level. Reading 2 does not supply the missing
   quantity; it substitutes a different one and does not say why the substitution is valid.

### 5.3 Reading 3: nothing about direction is licensed. Adopted

It is the only reading that survives all three inputs at once, and section 6 shows it does
not depend on how the blocker is later ruled.

**One thing it must not be read as.** "Nothing about direction is licensed" is not "the
measurement failed". Quantity (c) measured what it was designed to measure, at the unit
P2-D20 fixed, at the tolerance P2-D19 fixed, against the null P2-D6 fixed. What is missing
is the second conjunct the design always required and never operationalised after P2-D6
changed the statistic. This is a finding about the design, and `CLAUDE.md` treats reporting
one as a successful outcome.

### 5.4 A fourth reading, not offered, rejected anyway

**Withhold (c)'s numbers until the blocker is ruled.** Rejected. The numbers are not what is
blocked, and `reports/T7_armb_quantities.md` section 6 already says so. Withholding a
reproducible statistic because its interpretation is unsettled makes the record depend on a
later ruling, which is the opposite of what a preregistration is for.

---

## 6. Why the ruling does not pre-empt P2-D5's blocker

Three readings of the blocker are in circulation (`DECISIONS.md`, "What the registry
surfaced on its first run"). The direction claim fails under each.

| reading of the blocker | what it would license | why the direction claim still fails |
|---|---|---|
| the conjunct travels to the new quantities and needs an operational form | nothing until that form exists | the form does not exist, and section 4 shows writing it now would be post-hoc |
| it expired with the mean, the way the `ext_i` floor's scope did | the framing contrast alone | P2-D5's first clause survives regardless, and inputs 2 and 3 are unaffected by the blocker: a content-neutral insert departs downward on the model where it resolves, and the retained subset is selected on three of the five cells |
| (a), (b) and (c) already satisfy it, because a contrast against a same-option baseline is an excess | the direction claim | the premise is false as stated: `A_null` is a marginal over canonical option ids weighted by `A`, and a same-option rate is a rate of unchanged choices. They are different objects. Inputs 2 and 3 are again unaffected |

So the blocker stays open and stays the author's, and P2-D24 is well formed without it.

---

## 7. The ruling, and the words

### 7.1 What Arm B may now claim

**Movement, at quantity (a), stated with its counts and its floor.**

> Both framings changed the chosen option on every model. Per cell the count of items
> carrying a changed rendering runs from 30 to 77 of 108, every cell clears the
> preregistered noise floor of 7, and every cluster-bootstrap interval excludes zero at the
> corrected `alpha`. Under Paper 1's deterministic scorer the no-effect rate is exactly 1.0
> and not estimated, so this is a statement about the framing rather than about measurement
> noise.

**Magnitude, per cell, as descriptive context that gates nothing.**

> On `L3`/F1, `B2`/F2 and `L3`/F2 the framing changes the chosen option on more pairs than
> Paper 1's `c5` insert does, with the interval excluding zero at the corrected `alpha` at
> -0.1065, -0.1481 and -0.1620. On the other eleven cells the comparison does not resolve:
> the difference runs -0.1620 to +0.0648 against half-widths of 0.0787 to 0.1275. Quantity
> (b) is descriptive under P2-D12, gates nothing, and spends no `alpha`.

**Direction, as an arithmetic description of the statistic and nothing more.**

> On five of the fourteen cells the within-item sign proportion departs from `p0 = 0.5` at
> the corrected `alpha`, and all five departures are below 0.5.

### 7.2 What it may not claim

- That the five departures are movement away from `o*_infinity`, away from the
  adversary-aware optimum, or away from anything. The arithmetic statement stands; the
  reading of the `A` axis does not.
- That any model does or does not track the adversary, carry adversary-relevant content,
  or fail to. That was blocked before this version and stays blocked.
- That the framings move choices "substantially", or by any magnitude word that pools the
  three cells where quantity (b) resolves with the eleven where it does not. Section 2.2.
- That a content-neutral insert drifts downward as a general property. It resolves on
  `CTRL` and only `CTRL`.
- That the concentration is a limitation on two cells. It affects three of the five
  resolving cells and it is selection, not a limitation.

### 7.3 The human-behaviour gap claim is untouched

`docs/P2/tasks/T4.md` fixes its wording and `CLAUDE.md` forbids broadening it. Nothing here
touches it: it is a claim about what the prior literature does not ask, and it is
independent of what Arm B measures. It is named here only so that a reader of this version
does not take a narrowed Arm B claim as a reason to widen a different one.

---

## 8. Consequences

- `docs/P2/DECISIONS.md` gains **P2-D24**, and the open-question note added 2026-09-14
  gains a dated correction line for the `L3` error and the word "substantially".
- `src/p2_decisions.py` gains `P2D24_TEXT`, `P2D24_REJECTED`, the constants the ruling
  needs, and `bind_direction_claim`, called by `src/t7_armb.py`. The binding asserts the
  three premises a direction claim would need, each with the reason it exists, per the
  binding-form note in `DECISIONS.md`. It does not assert a range any number occupies.
- `src/t7_armb.py` emits a `direction_reading_P2D24` block into
  `results/T7_armb_quantities.json` and a section into `reports/T7_armb_quantities.md`.
  **Every pre-existing key and value in that artifact is byte-identical**; the block is
  additive and was verified key by key.
- `reports/T7_switch_concentration.md` has "2 to 5 times" replaced by the range its own
  table carries, 1.81 to 4.09 on the resolving cells, and its cell-versus-model counting
  made explicit.
- `tests/test_p2d24_direction.py` fails if the ruling drifts: if a resolving cell enters or
  leaves, if a departure turns upward, if the neutral diagnostic resolves on a second model,
  if the concentrated subset of resolving cells changes, or if a caller reports a direction
  claim.
- Nothing is recomputed and no statistic is introduced. `p0` is 0.5. P2-D6, P2-D12, P2-D14,
  P2-D19, P2-D20 and P2-D21 are untouched. P2-D5's blocker is still open.
