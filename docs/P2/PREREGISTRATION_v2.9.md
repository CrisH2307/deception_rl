# PREREGISTRATION v2.9

**Paper 2: the adversary effect and the RL Scientist**

Version 2.9 · written 2026-09-12 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.8`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all ten
are read together. This version rules one case that `v2.0` through `v2.8` do not cover:
what becomes of a rendering whose argmax is tied. It changes no statistic, no `alpha`,
no `p0`, no coordinate, no item set and no `n`, it supersedes nothing, and it does not
touch Arm A or Arm C.

**Data observed at the time of writing.** `F0` has been scored and checked against Paper
1's frozen `cond4` (`results/T7_f0_replication.json`). Of the `F1` and `F2` output, one
aggregate and nothing else: the number of tied renderings per (model, framing) on the
`size` tile, disclosed in full in section 1.2. No `ΔA`, no same-option rate, no tie rate,
no sign test, no item identity. The rule below is fixed on the structure of the event and
on a precedent already in the frozen reference path, not on what the affected items would
contribute.

| # | decision | where |
|---|---|---|
| 1 | A tied rendering is excluded pairwise, at the (item, permutation) pair. Never imputed as a non-mover, never taken as a reason to drop the item. | §1, **P2-D16** |

---

## 1. A tied rendering is excluded pairwise. **P2-D16**

### 1.1 The gap

`ΔA` is `A(F1) - A(F0)` on a rendering pair, so it needs both terms. A rendering whose
argmax is tied carries no chosen option: Paper 1's scorer reports `n_tied` and Paper 1
filters on `n_tied == 1` everywhere a choice is read. A tied `F1` rendering therefore
cannot enter the contrast, and its `F0` partner has nothing to be contrasted against.

Nothing in `v2.0` through `v2.8` says what happens to that pair. The item set is fixed
(P2-D4), the statistics are fixed (P2-D6, P2-D10, P2-D12), the floor is fixed (P2-D13),
and the attrition rule is absent from all of them.

### 1.2 The counts, disclosed, and what was deliberately not looked at

On the `size` tile at `rule = pmi`, `format = V`, in `data/raw_t7/choices_t7.parquet`:

| model | framing | tied renderings |
|---|---|---|
| `B2` | `F1` | 2 |
| `B2` | `F2` | 2 |
| `L4` | `F1` | 1 |

Every other (model, framing) cell has none, `F0` included, on all seven models. These
counts were re-derived at decision time by grouping on (model, framing) alone and they
matched. The re-derivation ran on the whole `size` tile rather than on the 108
confirmatory items, so **how many of the five losses fall inside the analysis set is not
established by it**, and the rule is written to hold either way.

Not inspected, and not computed, before the rule was fixed:

- which items carry the tied renderings,
- what `ΔA` those items would carry,
- any `F1` or `F2` same-option rate, tie rate, sign count or `n_eff`.

**Why the ordering is stated rather than assumed.** A rule for handling attrition that is
chosen after the attrition's effect is visible is a researcher degree of freedom with the
same shape as an exclusion criterion fixed after seeing the outcome. The counts had to be
known for the question to be asked at all; the identities did not, so they were not
looked at.

### 1.3 The losses are one-sided, which is what makes this material

The ties fall only in the treatment conditions. That turns a handling question into a
directional one: any rule that keeps a tied pair in a denominator it cannot appear in the
numerator of pushes quantity (a) toward the null, and (a) is the half of H-B that P2-D13
deliberately makes demanding to confirm.

Against P2-D12's inertness floor of 7 items, a 2-item loss is 29% of the floor. This is
not a rounding question, and it is not one a later session should settle with the affected
counts already on screen.

### 1.4 The rule, and why it is not a new choice

> A rendering whose argmax is tied carries no chosen option, so it carries neither a
> same-option verdict nor an `A` value, and it is excluded. The exclusion is PAIRWISE and
> at the level of the rendering pair, the (item, permutation) unit at which a framing
> contrast is formed: the pair leaves both the numerator and the denominator of every
> quantity whenever either of its two renderings is tied, and the item's other permutation
> is retained. A tied rendering is never imputed as a non-mover, and the item is never
> dropped whole. The rule is symmetric across the arms: it applies whether the tie falls
> on `F0`, `F1` or `F2`, so a tied `F0` rendering leaves both the `F1` and the `F2`
> contrast while a tied `F1` rendering leaves only the `F1` contrast. A tied `F0`
> rendering is also outside the `F0`-versus-`cond4` disagreement count that sets P2-D13's
> floor, which is already Paper 1's `n_tied == 1` filter on both sides, so it neither
> raises nor lowers the floor. This is Paper 1's `n_tied == 1` filter applied at the
> contrast rather than at the rendering, and it is what `src/c5_effect.py` and
> `src/inertness_ceiling.py` already do to produce P2-D8's reference values. Every cell
> reports its attrition: rendering pairs excluded for a tie, and items left with one
> surviving pair or with none.

The last clause is the ground the decision stands on. The same event already occurs in the
computation that produced the frozen reference, and it is already handled this way:

```
tie_reference.load_choices     applies Paper 1's n_tied == 1 filter
c5_movement / c5_delta_A       pivot on (item_id, permutation_id) x condition
                               w.loc[w.notna().all(axis=1)]
```

A tied `cond5` rendering leaves its (item, permutation) row short a column, the row is
dropped, and the item's other permutation survives. That is the rule above, applied to the
`c5` contrast, and the numbers it produced are the `R_m` values P2-D8 binds and the `c5`
tie rates `v2.7` section 2.1 reports. Handling `F1` and `F2` any other way would make
quantity (b) a comparison between a rate computed under one attrition rule and a reference
computed under another, which measures the rule rather than the framing.

`src/t7_f0_replication.py:compare` already filters `n_tied == 1` on both sides and its
docstring already gives the reason: a tie carries no chosen option, so it cannot agree or
disagree.

### 1.5 What it does to quantity (a)

(a)'s per-item value is the mean of the changed indicator over that item's **surviving**
pairs, and its count against P2-D13's floor is the number of items whose per-item value
exceeds zero, which is `n_items_with_a_changed_pair` as `c5_movement` already computes it.

| effect | direction | bound here |
|---|---|---|
| the count of moving items | can only fall | `B2` `F1` at most -2, `B2` `F2` at most -2, `L4` `F1` at most -1 |
| the item denominator | falls only if an item loses both pairs | 108, or 107 per item that loses both |
| a half-observed item's contribution | 0 or 1 instead of 0, 0.5 or 1 | weight unchanged, variance higher |

An excluded pair can remove an item's only evidence of movement. It cannot create
movement, so the count is biased downward or not at all, which is toward the null on the
half where the null is harder to confirm. Whether the realized loss is 2, 1 or 0 depends
on facts not inspected.

If `B2`'s two `F1` ties sit on two different items, both items remain with one pair each
and the denominator stays 108. If they are the two permutations of one item, that item has
no surviving pair, it leaves the item-level mean and the denominator is 107. **The floor is
an absolute count of items and does not scale with the denominator**, so 107 makes the
floor marginally harder to clear. That is reported beside the count, not adjusted for.

The third row is a variance effect and not a bias: a half-observed item still counts as
one item and its expectation is unchanged if its two permutations carry the same change
probability, but its value is a single Bernoulli draw rather than a mean of two, which
widens P2-D8's cluster bootstrap in quantity (b).

### 1.6 What it does to quantity (c)

Excluded pairs leave the pool before `ΔA` is evaluated, so they are in neither the tie
count nor `n_eff`. `n_eff` falls by at most the number of excluded pairs, and by zero if
those pairs would have carried `ΔA = 0`: at most 2 for `B2` under `F1`, at most 2 for `B2`
under `F2`, at most 1 for `L4` under `F1`. The tie rate's denominator falls by the same
amount, so the tie rate itself is not biased in a known direction.

No adjustment is made and none is needed. P2-D6 and P2-D12 already report the sign test at
the observed `n_eff` with its realized power, so this loss is absorbed by a disclosure the
design already requires. At the `c5`-analogue `n_eff` of 14 to 40 reported in `v2.7`
section 2.2, a loss of 2 is within the range those figures already span, and the realized
figure replaces the analogue in the results table regardless.

### 1.7 The reverse case, ruled now although it does not occur here

An `F0` rendering tied while its `F1` or `F2` rendering is not is covered by the same rule,
which is stated on the pair and not on the arm. Two consequences are specific to it and are
recorded so a replication does not rediscover them.

1. **`F0` is the common baseline.** One tied `F0` rendering removes that pair from the `F1`
   contrast AND the `F2` contrast. The attrition is correlated across the two cells and is
   reported once as a baseline loss, not twice as two independent losses.
2. **A tied `F0` rendering is not evidence of numerical noise.** It is already outside
   P2-D13's `F0`-versus-`cond4` disagreement count, which requires `n_tied == 1` on both
   sides. A tie is an absence of a choice, not a disagreement between two choices, so it
   can neither raise the measured floor nor lower it. P2-D13's upward-only rule is
   untouched.

A pair tied on both sides is excluded once.

### 1.8 Alternatives offered and not chosen

1. **Count the tie as a non-mover.** Rejected. A tie is the absence of a choice, not the
   repetition of one, so this records an event the scorer did not produce. It is
   directional in the worst place: it adds pairs to (a)'s denominator that cannot appear in
   its numerator, on a point null at the boundary where a single item is deductive
   evidence. Under P2-D13 the floor is already a conservative convention with no
   statistical derivation; an imputation toward the null makes the movement half harder to
   clear by arithmetic rather than by measurement. It also breaks the comparison to `R_m`,
   which was computed the other way.
2. **Exclude the whole item.** Rejected. It discards a rendering pair carrying a valid
   contrast and costs more than the event requires: `B2`'s confirmatory denominator would
   fall to at most 106 and `L4`'s to at most 107, for five renderings lost. Against an
   absolute floor of 7 items, shrinking the denominator is not neutral. It diverges from
   the reference computation, so quantity (b) would compare rates taken on differently
   constituted item sets, and it makes attrition item-level and unequal between the `F1`
   and `F2` cells of one model for no reason the event supplies.
3. **Break the tie with a deterministic rule and score the rendering.** Rejected. Paper 1's
   `src/tiebreak.py` breaks ties in ITEM CONSTRUCTION, not in the chooser; the chooser is an
   argmax that reports `n_tied`, and Paper 1 filters on it. Supplying a chosen option where
   the model produced none manufactures a contrast, and a manufactured contrast can create
   movement, which is the one direction (a) must not be able to move on its own. It would
   also be a chooser behaviour Paper 1's published results were not computed under, which is
   a frozen-artifact change in everything but name.

### 1.9 One thing this decision does not rule

Whether quantity (c)'s unit is the rendering pair or the permutation-averaged item is not
settled by the record, and this decision does not settle it.

| source | unit it implies |
|---|---|
| P2-D12 decision text: "the exact two-sided sign test on items with `ΔA != 0`" | item |
| `v2.0` section 3.2: `A` "averaged within item across the two Format V permutations" | item |
| `inertness_ceiling.py:c5_delta_A`: `ΔA` per `(item_id, permutation_id)`, `n_eff` a count of those | rendering pair |
| `inertness_ceiling.py:main`: `n_eff = round(108 * (1 - tie_rate))` | item |

The two readings give different `n_eff` for the same data. **This rule is written so it
gives the same treatment under either**: exclusion happens at the pair, before any
aggregation, and whatever aggregation (c) uses then runs on the surviving pairs, which is
already how `c5_movement` forms its per-item mean. So the unit question does not block
T7, and it is not answered here, because answering it would resolve an ambiguity by
choosing. It is the author's to settle, and it is flagged rather than carried silently.

### 1.10 What T7 reports because of this

Per (model, framing) cell, beside the three quantities:

```
pairs excluded for a tie
items reduced to one surviving pair
items reduced to no surviving pair
the resulting item denominator
```

A cell whose denominator is not 108 states that next to its (a) count, because the floor
it is measured against is an absolute count of items and a reader cannot recover the
denominator from the rate.

`src/p2_decisions.py` carries `bind_tie_exclusion`, which an Arm B script calls with the
exclusion unit it actually used and with whether it imputed, dropped whole items, or
reported attrition. The filter itself is the pivot-and-`notna` shape already in
`c5_movement` and `c5_delta_A`; a third copy of a three-line filter would be the
duplication bug `CLAUDE.md` names.
