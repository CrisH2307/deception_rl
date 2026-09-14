# T7: do switches concentrate on the `A`-tied option pairs?

Emitted by `src/t7_switch_concentration.py` into
`results/T7_switch_concentration.json`. Run on frozen `data/raw_t7/choices_t7.parquet`,
`size` confirmatory set, `n` = 108, `rule = pmi`, Format V, at P2-D19's `EPS = 1e-12` and
P2-D20's item unit.

**This file adjusts nothing.** P2-D19's tolerance, P2-D20's unit and P2-D12's three
quantities are untouched. No H-B verdict is issued here or anywhere else in T7.

## Why it had to run

P2-D19 bounds the `A` coordinate's blind spot at the **per-pair** rate, 84 of 1,620
unordered option pairs, **0.0519**. `v2.13` section 3.4.1 records the assumption that
bound rests on, and records that it was not checked:

> The bound holds if the option pairs models actually switch between are not concentrated
> on the tied pairs. They may be: the tied pairs are concentrated at the two ends of the
> option order. The assumption is checkable and it is **not checked here**, because
> checking it reads model choices, which is an Arm B computation this version does not
> perform.

T7's confirmatory run did not check it either. It emitted P2-D10's blind-spot gap and
bound P2-D19's tolerance figures, and it computed no concentration quantity.

## Result

`blind` is items that changed option but carry `ΔA = 0` at the item unit, which is
quantity (a)'s moving-item count minus quantity (c)'s `n_eff`. `obs` is the share of
switches landing on an `A`-tied option pair; `exp` is the share a switch uniform over that
item's own 15 pairs would give; `ratio` is `obs / exp`. **Above 1 the per-pair bound
understates the realized blind spot.**

| cell | (a) moved | (c) `n_eff` | blind | switches | on tied | obs | exp | ratio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `CTRL`/F1 | 43 | 36 | **7** | 50 | 12 | 0.2400 | 0.0587 | **4.09** |
| `B2`/F1 | 51 | 50 | 1 | 57 | 1 | 0.0175 | 0.0561 | 0.31 |
| `B4`/F1 | 66 | 65 | 1 | 85 | 0 | 0.0000 | 0.0525 | 0.00 |
| `L1`/F1 | 30 | 24 | **6** | 35 | 8 | 0.2286 | 0.0629 | **3.64** |
| `L2`/F1 | 42 | 42 | 0 | 45 | 0 | 0.0000 | 0.0563 | 0.00 |
| `L3`/F1 | 53 | 47 | **6** | 64 | 8 | 0.1250 | 0.0500 | **2.50** |
| `L4`/F1 | 48 | 46 | 2 | 56 | 1 | 0.0179 | 0.0595 | 0.30 |
| `CTRL`/F2 | 50 | 36 | **14** | 54 | 17 | 0.3148 | 0.0617 | **5.10** |
| `B2`/F2 | 64 | 62 | 2 | 75 | 0 | 0.0000 | 0.0507 | 0.00 |
| `B4`/F2 | 77 | 74 | 3 | 102 | 2 | 0.0196 | 0.0529 | 0.37 |
| `L1`/F2 | 32 | 28 | **4** | 37 | 5 | 0.1351 | 0.0649 | **2.08** |
| `L2`/F2 | 40 | 40 | 0 | 41 | 0 | 0.0000 | 0.0488 | 0.00 |
| `L3`/F2 | 63 | 57 | **6** | 76 | 7 | 0.0921 | 0.0509 | **1.81** |
| `L4`/F2 | 62 | 61 | 1 | 77 | 1 | 0.0130 | 0.0606 | 0.21 |

Pooled over all 14 cells: **62 of 854 switches land on a tied pair, 0.0726**, against the
0.0519 bound. 53 items in total changed option and carry `ΔA = 0`.

## The answer is model-split, and that is the finding

**The assumption fails on three models and holds on four.**

- **Concentrated, bound understates:** `CTRL` (4.09, 5.10), `L1` (3.64, 2.08), `L3`
  (2.50, 1.81). On `CTRL` under F2 nearly a third of all switches are invisible to `A`.
- **Not concentrated, bound overstates:** `B2`, `B4`, `L2`, `L4`, all at or below 0.37,
  four of the eight cells at exactly zero.

So the per-pair bound is not a bound. It is an average over a quantity that varies by a
factor of 5 across models, and on the models where it fails it fails in the direction that
matters: (c) is measuring less of the movement than (a) sees.

The blind-spot counts track the ratio exactly, as they must: every cell with a ratio above
1 loses 4 or more items between (a) and (c), and every cell at or below 1 loses 3 or
fewer.

## What this bears on, stated and not resolved

**Three of the five resolving cells sit in the concentrated group.** `CTRL`/F1, `L3`/F1
and `L3`/F2 all depart from `p0 = 0.5` at the corrected `alpha` and all three are
concentrated, at ratios of 4.09, 2.50 and 1.81. The other two resolving cells, `L4`/F1 and
`L4`/F2, are not concentrated, at 0.30 and 0.21. Counted by model rather than by cell, two
of the three concentrated models carry a resolving cell. On the three affected cells the
`n_eff` is formed after the coordinate has discarded the switches it cannot see, and that
discard is **1.81 to 4.09** times what P2-D19's bound anticipated. The wider 1.81 to 5.10
is the range over all six concentrated cells, and its top end is `CTRL`/F2, which does not
resolve.

This does not say the departures are artifacts. It says the sign test on those cells runs
on a subset of the movement selected by a property of the item geometry rather than at
random, and nothing in the current design establishes that the discarded switches carry
the same direction as the retained ones.

**No statistic is adjusted in response, and none should be without a ruling.** Reweighting,
reselecting or excluding on this would be choosing a remedy with the affected counts on
screen, which is the ordering hazard the log names repeatedly.

**Ruled 2026-09-14 by P2-D24, and no statistic is adjusted there either.** The concentration
is one of the three premises a direction claim on quantity (c) would need, and it is the
premise that the discarded switches carry the direction of the retained ones. Nothing
establishes it, so no direction claim is licensed on any cell. The ruling changes no number
in this file.

## The (4,5) signature, restated 2026-09-14 as evidence rather than as structure

The 62 discarded switches fall almost entirely on one option-index pair: **(4,5) on 54**,
(0,1) on 4, (3,4) on 3, (3,5) on 1. This file first recorded that as structure inherited
from P2-D19 section 3.8, which measured the tied pairs themselves at 67 on (4,5) and 15 on
(0,1), and left the cause unestablished. That framing understates what the observation is.

**Option 5 is the end of the option order on a six-option tile, and 54 of 62 discarded
switches land on the pair {4, 5}.** That is the signature a generic shift in option
POSITION preference would leave: a model whose inserted text nudges it toward or away from
the end of the menu moves between the last two options, and those are exactly the options
the `A` coordinate cannot tell apart.

**The hypothesis this favours is the one the design can no longer rule out.** `v2.0`
section 4.4 preregistered the attribution cap `ΔA_null(m, F)` against precisely it, in its
own words: "Movement that a generic prompt-induced shift in option preference already
explains is reported as prompt sensitivity and named as such." P2-D6 replaced the mean with
a sign test, P2-D12 fixed three quantities, and no successor to the cap was written.
`DECISIONS.md` records that as the second instance of the scope-expiry failure.

So this is **suggestive evidence for the alternative explanation, and it is uncomputable
against the preregistered defence, because the defence has no successor.** Neither of the
cap's inputs exists: `TV(m, F)` on the `beta_c = infinity` control set is T7 step 4 and has
not been run, and `ΔA_null(m, F)` has never been computed.

**What is and is not claimed here.** The observation is recorded. The hypothesis it favours
is named. **The design cannot currently adjudicate between it and adversary tracking**, and
that inability is the finding. No successor cap is computed here, the hypothesis is not
tested, and the concentration on (4,5) is not offered as establishing anything: a generic
position shift predicts this signature, and so would other things, and distinguishing them
is what the cap was for.

The cause of the underlying tie structure is still not established, and none is proposed.
