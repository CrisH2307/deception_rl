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

**Two of the three concentrated models are resolving cells.** `CTRL`/F1, `L3`/F1 and
`L3`/F2 all depart from `p0 = 0.5` at the corrected `alpha`, and all three sit in the
concentrated group. Their `n_eff` is formed after the coordinate has discarded the
switches it cannot see, and on those cells that discard is 2 to 5 times what P2-D19's
bound anticipated.

This does not say the departures are artifacts. It says the sign test on those cells runs
on a subset of the movement selected by a property of the item geometry rather than at
random, and nothing in the current design establishes that the discarded switches carry
the same direction as the retained ones.

**No statistic is adjusted in response, and none should be without a ruling.** Reweighting,
reselecting or excluding on this would be choosing a remedy with the affected counts on
screen, which is the ordering hazard the log names repeatedly.

## Structure, consistent with P2-D19

The 62 tied-pair switches fall almost entirely on one option-index pair: **(4,5) on 54**,
(0,1) on 4, (3,4) on 3, (3,5) on 1. P2-D19 section 3.8 recorded the tied pairs themselves
as 67 on (4,5) and 15 on (0,1), structural to the six-option tile and concentrated at the
ends of the option order, with the cause not established. The switches inherit that shape.
The cause is still not established and none is proposed here.
