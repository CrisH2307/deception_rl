# PREREGISTRATION v2.11

**Paper 2: the adversary effect and the RL Scientist**

Version 2.11 · written 2026-09-13 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.10`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all twelve
are read together. This version settles one thing: **quantity (c)'s unit**, which `v2.9`
section 1.9 flagged and `v2.10` section 4.1 restated with the numbers and declined to
answer. It is the denominator of the confirmatory test.

It changes no statistic, no `alpha`, no `p0`, no coordinate, no item set and no item count.
It does not touch Arm A or Arm C. It computes **no `F1` or `F2` statistic**: every figure
below is the `c5` contrast on frozen Paper 1 rows, recomputed on 2026-09-13 and not
transcribed. The `ext_i` floor is untouched and stays open.

| # | decision | where |
|---|---|---|
| 1 | Quantity (c)'s unit is the ITEM. An item's value is the mean of its surviving pair `ΔA`s. | §2, **P2-D20** |
| 2 | A sign disagreement between an item's two permutations resolves on the sign of their mean. Cancellation to within `EPS` is a tie. | §3, **P2-D20** |

**The instruction this acted on**, per `v2.10` section 2.4's countermeasure: the author
named the three readings and their `n_eff`, instructed "DECIDE. State the unit, compute the
n_eff it gives per model, and say what happens to an item whose two permutations disagree
in sign", noted that "P2-D16 already sets the precedent that a partially observed item
contributes what it has rather than being imputed or dropped", and constrained the session
to recompute rather than transcribe, to leave the `ext_i` floor alone, to compute no
`F1`/`F2` statistic, and to list rather than recompute any published power figure the unit
moves. This section is written by an agent session acting on that instruction, not by the
author.

---

## 1. Three readings, one of which the documents already fix

### 1.1 What was in circulation

| source | unit implied |
|---|---|
| P2-D12 decision text: "the exact two-sided sign test on items with `ΔA != 0`" | item |
| `v2.0` section 3.2: `A` is "computed per rendering, averaged within item across the two" Format V permutations | item |
| `inertness_ceiling.py:c5_delta_A`: pivots on `(item_id, permutation_id)`, `n_eff` counts those rows | rendering pair |
| `inertness_ceiling.py:main`: `n_eff = round(108 * (1 - tie_rate))` | neither |

### 1.2 They do not have equal standing

**Both governing documents say item.** Neither is ambiguous and neither was amended. What
`c5_delta_A` and `main` do is implementation drift from a stated unit, not competing
readings of an unstated one.

That changes what kind of act this is. Restoring a preregistered unit is conservative.
Amending a preregistration to match an implementation that drifted from it, after the
`n_eff` each choice gives is on the table, is the other kind, and it is the kind this
project does not perform.

### 1.3 The three readings, recomputed

`c5` contrast, `size` confirmatory set, 108 items, emitted by
`python3 src/inertness_ceiling.py`:

| model | ITEM, **P2-D20** | pair, exact, `v2.7` §2.1 | `round(108 x (1 - tie_rate))`, `v2.7` §3.2 |
|---|---:|---:|---:|
| `CTRL` | **41** | 53 | 26 |
| `B2` | **36** | 42 | 21 |
| `B4` | **63** | 80 | 40 |
| `L1` | **27** | 27 | 14 |
| `L2` | **31** | 32 | 16 |
| `L3` | **33** | 35 | 17 |
| `L4` | **43** | 55 | 28 |

The two superseded columns reproduce `v2.7` exactly. That is the check that this is a
recomputation of the same quantity at a different unit rather than a different measurement
that lands nearby, and it is why they are reported rather than dropped.

### 1.4 The rescaled column is wrong in the opposite direction, and by more

The item figure sits **below** the pair count on six of seven models, because an item whose
two pairs are both nonzero collapses to one vote. It sits at roughly **double** the rescaled
figure, because `round(108 x (1 - tie_rate))` takes a rate defined over 216 pairs and
applies it to 108 items. That counts an item whose permutations disagree on `ΔA != 0` as
half an item, by arithmetic no decision authorizes.

A reader handed either superseded number alone cannot see which way it is wrong. That is
the practical case for fixing the unit rather than continuing to report whichever ran.

### 1.5 Two corrections, separated

`v2.10`'s P2-D19 moved the zero test from exact float equality to `EPS = 1e-12`. This
version moves the unit. They are different corrections and they are emitted separately as
`n_eff_pair_at_eps` so they can be told apart:

| model | pair, exact | pair, at `EPS` | item, at `EPS` |
|---|---:|---:|---:|
| `CTRL` | 53 | 47 | 41 |
| `B2` | 42 | 42 | 36 |
| `B4` | 80 | 79 | 63 |
| `L1` | 27 | 27 | 27 |
| `L2` | 32 | 32 | 31 |
| `L3` | 35 | 35 | 33 |
| `L4` | 55 | 55 | 43 |

**The tolerance alone moves only `CTRL` and `B4`**, which is what `v2.10` section 3.7
predicted when it listed those two tie rates and no others. The unit does the rest. Neither
correction is large on `L1`, and both are large on `CTRL` and `L4`.

---

## 2. The unit. **P2-D20**

> Quantity (c)'s unit is the ITEM. This is not a choice between three readings in
> circulation; it is the unit both governing documents already state, restored. P2-D12's
> decision text says "the exact two-sided sign test on items with `ΔA != 0`" and `v2.0`
> section 3.2 says `A` is computed per rendering and "averaged within item across the
> two" Format V permutations. An item's value is therefore the mean of its SURVIVING
> pair `ΔA`s, which equals the difference of its within-item mean `A`s, and the item
> enters the sign test when `|mean ΔA| > EPS` under P2-D19's tolerance. Three
> consequences are fixed here because no reading covered them. An item with one
> surviving pair contributes that pair's sign, per P2-D16: it contributes what it has,
> and is neither imputed nor dropped. An item whose two pairs DISAGREE in sign
> contributes the sign of their mean. An item whose two pairs cancel to within `EPS`
> contributes nothing and is counted as a tie, which is the same event as a pair-level
> tie and is reported as one. `inertness_ceiling.c5_delta_A`'s pair count and
> `inertness_ceiling.main`'s `round(108 x (1 - tie_rate))` are both superseded for (c):
> the first counts the wrong unit, the second applies an item scale to a 216-pair rate
> and yields neither unit. Both keep emitting unchanged, because `v2.7` sections 2.1 and
> 3.2 publish them and a superseded document must still reproduce.

An item's value is the mean of its **surviving** pair `ΔA`s, which is the same number as
the difference of its within-item mean `A`s, because the mean of two differences is the
difference of two means. So `mean(ΔA)` IS the item's `ΔA` as `v2.0` section 3.2 defines it.
The rule follows from the existing definition; it is not added to it.

The item enters the sign test when `|mean ΔA| > EPS`, under P2-D19's tolerance. P2-D19's
text already governs "every figure reporting what the `A` coordinate can resolve", and an
item-level zero test is one, so this is scope already granted rather than scope taken here.

---

## 3. What happens to an item whose two permutations disagree in sign

This is the case the unit exists to rule on and the case no reading covered, because at the
pair unit it does not arise: two pairs are simply two votes and a disagreement is invisible.

### 3.1 The rule

**The sign of the within-item mean.** Four cases, all observed on the `c5` contrast:

| case | contributes | `CTRL` | `B2` | `B4` | `L1` | `L2` | `L3` | `L4` |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| two pairs, same sign | one vote, that direction | the common case; the balance of each model's 108 | | | | | | |
| two pairs, opposite signs, not cancelling | one vote, direction of the larger | 0 | 6 | 4 | 0 | 0 | 1 | 4 |
| two pairs, opposite signs, cancelling within `EPS` | nothing; counted as a tie | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| one surviving pair (P2-D16 attrition) | one vote, that pair's sign | 0 | 2 | 0 | 0 | 0 | 0 | 0 |

Sign-disagreeing items total 17 across the seven models, of which 2 cancel.

### 3.2 Why the one-pair case is not a new rule

**P2-D16 already settled it**, and the author's instruction named it as the precedent: a
partially observed item contributes what it has rather than being imputed or dropped. It is
restated here only because (c)'s unit is what makes the case visible. Imputing such an item
to zero would add a tie the scorer did not produce. Dropping it would shrink a denominator
that P2-D13's floor is an absolute count against.

### 3.3 Why cancellation is a tie and not something else

An item whose two pairs cancel has an item-level `ΔA` of zero. That is the same event as a
pair-level tie: **the coordinate did not move.** It is counted as a tie and reported as one,
which keeps one definition of "tie" in the design rather than two.

### 3.4 The magnitude objection, stated rather than deflected

Resolving a disagreement by the mean means an item where one permutation moves far and the
other moves slightly back votes with the larger move. That reads magnitude, and (c) is a
sign test, so the objection is real and is worth being explicit about.

The answer is that the magnitude forms the item's **value**; it does not weight the item's
**vote**. Every voting item contributes exactly one vote. That is the structure P2-D6 fixed,
with `v2.0` section 3.2's definition of the item value supplied where P2-D6 assumed one
without stating it.

### 3.5 An admissibility question, ruled by P2-D15's mechanism and not its wording

P2-D15 ruled `sign(ΔA)` admissible for the cross-family control under Paper 1's D111,
describing it as "an ordinal comparison of two options". `sign(mean ΔA)` compares the
relative sizes of two differences rather than two options, so **P2-D15's wording does not
reach it.**

Its mechanism does, and P2-D15's own reasoning says the mechanism is the right test. D111's
concern is tokenizer non-identity making log-probabilities incommensurable, and the
operational test it gives is whether the statistic changes when the tokenizer changes but
the chosen options do not. The item mean is a function of frozen, model-free item geometry
indexed by four chosen options and normalised by one per-item `ext_i`, computed within a
model and reported as a rate. A tokenizer change with the choices held fixed does not move
it.

`CTRL` remains citable. That matters, because `CTRL` is the model this decision moves most,
53 to 41.

This is flagged rather than folded in silently, because it extends a ruling past its stated
words, and a later session is entitled to see that that happened and disagree.

---

## 4. Alternatives offered and not chosen

1. **Adopt the rendering pair, and amend P2-D12 and `v2.0` section 3.2 to match the code.**
   Rejected. It amends a preregistration to match an implementation that drifted from it,
   after the numbers are visible. It is also the reading that treats 108 items as 216
   independent draws, in the one place the design is most short of `n`, which is the
   clustering P2-D8's bootstrap exists to respect.
2. **Keep `round(108 x (1 - tie_rate))`.** Rejected. It is neither unit, `v2.10` section 4.1
   already said so, and nothing defends it except that it is what ran.
3. **Exclude items whose two permutations disagree in sign.** Rejected. It discards exactly
   the items carrying the most information about whether an effect is order-robust, it is an
   exclusion rule whose effect on `n_eff` is visible at the moment it would be chosen, and it
   contradicts P2-D16's precedent in the same document.
4. **Break a sign disagreement by permutation 0.** Rejected. It makes the confirmatory test
   depend on which option order was labelled first, and it discards the second rendering's
   information while keeping its cost.

---

## 5. Published figures the unit moves. Listed, not recomputed

Per the instruction, these are named and **not** recomputed here. This version makes no
claim about which way any of them moves.

| figure | where |
|---|---|
| `v2.7` §3.2's power table: power at `p1 = 0.75`, at `0.90`, and `p1` at 80% power, all seven models | `v2.7` §3.2; `sign_power_at` and `p1_at_80_power` in `results/T5_inertness_ceiling.json` |
| `v2.7` §2.1's `p` values and `significant_at_corrected_alpha` for the `c5` sign diagnostic | `v2.7` §2.1; same artifact |
| P2-D14's Type II gap, 0.0000 to 0.2547 | P2-D14; `src/armb_floor.py:type_ii_gap` reads the pair block, `results/T5_armb_floor.json` |

`results/T5_detection_ceiling.json` is untouched. It computes its own `n_eff_max` from
`N * (1 - t_star)` for the superseded P2-D11 ceiling and does not read (c)'s unit.

### 5.1 One consequence that is not a power figure, flagged rather than absorbed

P2-D12 and P2-D14 both rest on the `c5` neutral sign proportion being **"at or below 0.5 on
all seven models"**. At the item unit, `B2`'s is **0.5556**, above 0.5, on `n_eff` 36 with a
two-sided `p` of 0.6177.

**The claim as worded does not survive the unit change.** Whether the conclusion it supports
survives is a different question, because 0.5556 at that `p` is not evidence of upward drift
either, and the conclusion was that a content-neutral insertion does not drift toward the
salience pole.

**It is not resolved here.** P2-D12 and P2-D14 rejected moving `p0` on reasoning that now
has to be re-read against a corrected diagnostic, and doing that inside the entry that
changes the unit would be settling two things at once with the numbers already on screen.
It is recorded so the next session finds it rather than rediscovers it.

---

## 6. What is emitted and what is bound

`inertness_ceiling.c5_delta_A` gains an item block beside the pair block: `n_eff_item`,
`n_positive_item`, `tie_rate_item`, `sign_proportion_item`, `p_two_sided_item`,
`n_items_sign_disagreement`, `n_items_sign_disagreement_cancelling`,
`n_items_with_one_pair`, `n_items_with_both_pairs`, and `n_eff_pair_at_eps`.

**The pair block keeps every value byte-identical**, and `main`'s
`n_eff_at_a_c5_like_tie_rate` keeps emitting its rescaled figure, because `v2.7` sections
2.1 and 3.2 publish both and a superseded document must still reproduce. Both now carry a
field saying what they are and what supersedes them, so neither can be lifted out of the
artifact without that.

`src/p2_decisions.py` carries `bind_quantity_c_unit`, which `inertness_ceiling.main` calls.
It checks the unit, the sign-disagreement rule, the one-pair and cancelling conventions, and
the zero test's `EPS`. The last is checked because the unit and the tolerance move `n_eff`
separately, and a run that fixes one and not the other is still not reporting P2-D20's
quantity.

---

## 7. What this version changes

| | |
|---|---|
| statistics, `alpha`, `p0`, coordinates, item set, item count | unchanged |
| Arm A, Arm C | untouched |
| quantity (c)'s unit | **item**, restored from P2-D12 and `v2.0` §3.2 |
| sign disagreement between an item's two permutations | sign of the within-item mean; cancellation within `EPS` is a tie |
| an item with one surviving pair | contributes that pair, per P2-D16. Not a new rule |
| `c5` `n_eff` for (c) | `CTRL` 41, `B2` 36, `B4` 63, `L1` 27, `L2` 31, `L3` 33, `L4` 43 |
| `results/T5_inertness_ceiling.json` | item block added; pair block and rescaled figure byte-identical, both now labelled |
| three published figure sets in §5 | must be recomputed under the item unit; not recomputed here |
| the `ext_i` floor | untouched, still open |
| any `F1` or `F2` statistic | none computed in this version |
