# PREREGISTRATION v2.17

**Status.** New file per Paper 1's **D148**. `v2.0` through `v2.16` are not edited. This
version **records what was computed** under P2-D25. It rules nothing, decides nothing, and
takes no new `P2-D` number.

**Written by an agent session acting on an author instruction**, per the countermeasure in
`v2.10` section 2.4. The session is not the author. The instruction it acted on is quoted
in section 1.

**This session computed.** It is the other half of the split P2-D25 was made under: the
ruling session saw no value, and this session saw every value and revisited no ruling.
Where this session believes P2-D25 got something wrong or left something unresolved, it
says so in section 7 and **stops on that point**; it resolves none of them.

**What is unchanged.** `p0` is 0.5. The confirmatory family is 21 tests at
`alpha = 0.05/21`. The confirmatory `n` for Arm B's three quantities is 108. No statistic,
unit, tolerance, null or family moves. P2-D5's blocker stays open and stays the author's.
No `results/*.json` value that existed before this session changed, verified by hashing
every file before and after and by walking the old key set against the new.

---

## 1. The instruction

Quoted in the parts that bear on what was computed.

> You are running one task in your own git worktree on the deception_RL Paper 2 repo:
> **T7 step 4, and steps 5 and onward only so far as P2-D25 permits**. You compute. **You
> rule nothing.**
>
> A prior session (P2-D25, `PREREGISTRATION_v2.16.md`, committed `d73c7a0`) ruled, **with
> no number on the table**, what these quantities may and may not be used for. The
> sessions were split so that the ruling was made blind to the values. **You are the other
> half of that split.** You compute under that ruling and you do not revisit it, extend it,
> or reinterpret it. If you believe the ruling is wrong or incomplete, say so in your
> report and **stop on that point**; do not resolve it.
>
> **Compute no quantity P2-D25 did not authorize.** If something you want is unauthorized,
> that is the split working.
>
> **T7 step 4 is the primary deliverable.** The `beta_c = infinity` control has a
> preregistered purpose independent of the cap: `o*_0 = o*_infinity` there, so the optimal
> option does not change and there is nothing for an adversary-aware model to move toward.
> Movement there is prompt sensitivity, not adversary tracking, and it caps attribution.
> P2-D25 ruled that purpose survives, intact and descriptive.
>
> Run step 4. Then run steps 5 and onward **only so far as P2-D25 permits**, and say
> explicitly for each step whether you ran it, ran it partially, or did not, and under
> which clause.

with the constraints: treat every number in the instruction and in `T7.md` as unverified
and recompute or re-derive it; beating the oracle is a bug; do not reopen P2-D5, P2-D6,
P2-D12, P2-D14, P2-D19, P2-D20, P2-D21, P2-D24 or P2-D25; artifact edits are additive only
for every pre-existing `results/*.json`, verified mechanically; no superseded
preregistration version edited in place; all tests pass and real tests are added for what
is computed. All were followed.

The instruction also summarised what P2-D25 authorizes and said, of its own summary, that
the record governs and any discrepancy is to be reported. Section 2 checks it.

---

## 2. Every claim carried into this session, checked

`CLAUDE.md`'s rule, and `v2.12` section 3.6's and `v2.15`'s two recorded cases of a figure
reaching a session through an author instruction without surviving recomputation.

| carried | checked against | verdict |
|---|---|---|
| local `main` at `d73c7a0` | `git log --oneline -1 main`; `HEAD` equals it and is an ancestor | **holds** |
| `bind_marginal_null_use` takes nine arguments | `src/p2_decisions.py:1169` | **holds**; the nine are those the instruction names, in that order |
| the control base is the `size` tile's **142** `beta_c = infinity` items | `tie_reference.item_sets`, `~isfinite(beta_c)` on `tile == "size"` | **holds**, 142 |
| the all-tile figure is on **540** non-divergent items | same, all four tiles: `hold` 134, `manmade` 136, `moves` 128, `size` 142 | **holds**, 540 |
| the confirmatory set is 108 six-option items | same; `|O| = 6` on every `size` item | **holds** |
| `alpha = 0.05/21` and the family is 21 | `P2D6_ALPHA`, `P2D25_CONFIRMATORY_FAMILY_SIZE` | **holds** |
| `v2.16` section 5.2: `F0` and Paper 1's `cond4` disagree on zero of 3,500 size-tile renderings | `results/T7_f0_replication.json`, summed over the seven models | **holds**, 0 of 3,500 |
| `v2.16` section 5.3: canonical (4,5) are the two largest on the `size` ordinal scale and the tile's `A`-tied pairs concentrate there | `reports/T7_switch_concentration.md`, P2-D19 section 3.8 | **holds**, and is not re-derived here |
| `T7.md` SCOPE: "step 4's `beta_c = infinity` control runs on the 540 non-divergent items" | the two bases above | **holds, and is a different base from the cap's.** P2-D25 says so; both are reported, with their bases named |
| `T7.md` step 4: "there should be NO movement there" | measured | **fails as a prediction.** `TV` is nonzero in all fourteen cells, 0.0176 to 0.2782 on the 142. The sentence is a hypothesis about models, not a property of the design, and the measurement is the answer to it |

Nothing else carried a number into this session.

---

## 3. What was computed, and under which clause of P2-D25

Emitted by `src/t7_control.py` into `results/T7_control_marginal_null.json` and
`reports/T7_control_marginal_null.md`. Every figure below is script-emitted. The script
calls `p2_decisions.bind_marginal_null_use` with the nine arguments P2-D25 requires before
it emits anything, and `tests/test_t7_control.py` fails if a caller crosses any of the six
premises behind them.

### 3.1 Step 4, the `beta_c = infinity` control. RUN IN FULL

`v2.0` section 4.4's first paragraph, which P2-D25 rules survives P2-D6 and P2-D12 intact
and unamended, and which was descriptive at `v2.0` and is descriptive now.

`TV(m, F) = 0.5 * sum_o |p^ctrl_{m,F}(o) - p^ctrl_{m,F0}(o)|`, on the `size` tile's 142
adversary-robust items, `|O| = 6`, 284 renderings per cell. The all-tile figure on 540
items is reported beside it with its base named, never alone, as the item-weighted mean of
the four **within-tile** distances: arity is constant inside a tile, so no marginal is
pooled across `|O| in {3,3,4,6}`, which P2-D3 rejected and which the binding's arity
premise asserts against.

| model | `TV` `F1`, n=142 | `TV` `F2`, n=142 | `TV` `F1`, n=540 | `TV` `F2`, n=540 |
|---|---:|---:|---:|---:|
| `CTRL` | 0.1725 | 0.0458 | 0.0806 | 0.0519 |
| `B2` | 0.0556 | 0.0704 | 0.0970 | 0.1537 |
| `B4` | 0.1585 | 0.1162 | 0.1620 | 0.2343 |
| `L1` | 0.0810 | 0.1021 | 0.1676 | 0.1657 |
| `L2` | 0.0423 | 0.0176 | 0.0546 | 0.0250 |
| `L3` | 0.1866 | 0.1866 | 0.1509 | 0.1685 |
| `L4` | 0.2148 | 0.2782 | 0.3241 | 0.3000 |

**The control moves in every cell.** On the 142, `TV` runs 0.0176 to 0.2782; on the 540,
0.0250 to 0.3241. The preregistered reading of that is fixed and is not chosen here: on
these items `o*_0 = o*_infinity`, so there is nothing adversary-relevant to move toward,
and any change in the choice distribution is **prompt sensitivity**. It caps how much of
the divergence-set effect can be attributed, which is T7 step 4's own sentence.

What `TV` cannot say, per P2-D25: it cannot size how much of the confirmatory movement it
explains. Sizing that is the reweighting, the reweighting lands in `A` units at the level,
and `A` is undefined on the control set by `v2.0` section 3.2. **The control set can show
that generic movement exists. It cannot adjudicate whether the confirmatory movement is
that movement.**

The per-tile table is in the report. `L4` on `manmade` carries the largest single-tile
value, 0.6544 under `F1` and 0.4890 under `F2`, and `CTRL` on `manmade` is exactly 0 under
both. Neither is on the cap's base and neither is read alone.

### 3.2 The attribution cap against the descriptive mean `ΔA`. RUN IN FULL

`ΔA_null(m, F) = sum_o (p^ctrl_{m,F}(o) - p^ctrl_{m,F0}(o)) * mean_i A_i(o)`, the control
shift on the 142 applied as a reweighting on the confirmatory set. P2-D6 demoted mean `ΔA`
rather than deleting it, so the cap follows its quantity down and is applied to it
unchanged at descriptive standing. No successor is authorized and none is claimed.

SLACK means the observed mean exceeds `ΔA_null`; BINDING means it does not.

| model | `ΔA_null` `F1` | mean `ΔA` `F1` | cap | `ΔA_null` `F2` | mean `ΔA` `F2` | cap |
|---|---:|---:|---|---:|---:|---|
| `CTRL` | -0.3194 | -0.5656 | BINDING | 0.0145 | -0.3525 | BINDING |
| `B2` | -0.0369 | -0.0936 | BINDING | -0.2027 | -0.5852 | BINDING |
| `B4` | 0.0676 | -0.1241 | BINDING | 0.1265 | -0.0694 | BINDING |
| `L1` | -0.2816 | -0.3993 | BINDING | -0.4162 | -0.4414 | BINDING |
| `L2` | -0.1332 | **0.1165** | **SLACK** | -0.0162 | **-0.0024** | **SLACK** |
| `L3` | -0.5960 | -1.2238 | BINDING | -0.4727 | -1.1540 | BINDING |
| `L4` | -0.7925 | -1.1786 | BINDING | -1.0479 | -1.7392 | BINDING |

**Binding on 12 of 14 cells, slack on `L2`'s two.** `n = 101` on both sides after the
`ext_i` floor. The observed median `ΔA` is exactly 0 in every cell, because most items do
not change their chosen option and an unchanged choice has `ΔA = 0` identically; the
median is reported beside the mean, never substituted for it, because the cap was written
against the mean.

**This is a descriptive comparison of two means and nothing else.** `v2.0` section 4.4's
criterion had two conjuncts and the first, a positive-direction interval on mean `ΔA`, was
retired when P2-D6 demoted the mean. Every observed mean here is negative except `L2`'s
`F1`, so the retired conjunct would have failed on 13 of 14 cells independently of the
cap. The comparison licenses nothing about quantity (c), nothing about direction, and
nothing about H-B.

**P2-D6's mixture defect, named and not repaired.** Both sides of every row are means over
the geometry P2-D6 measured: 470 option-cells at exactly 0, 439 at exactly 1, 841 off-pole
at median -3.329, unbounded below. `ΔA_null` is built from `mean_i A_i(o)`, whose value on
the floored confirmatory set is `o=0` -6.1230, `o=1` -4.0132, `o=2` -0.2366, `o=3`
-1.9996, `o=4` -6.0525, `o=5` -6.9515. A shift of a few percent of mass between option 2
and any other option therefore moves `ΔA_null` by order 0.1 to 0.2 in `A` units. The
comparison is weak on both ends and it is reported at that strength. Substituting a
median, a bounded transform or a trimmed mean would be inventing the successor P2-D25
declines, and each was rejected on its own grounds in P2-D6.

**The consequence P2-D25 states, restated with the numbers now in it.** Arm B's
confirmatory family carries no defence against the hypothesis that the movement is a
generic prompt-induced shift in option preference, and it cannot acquire one, because
acquiring one means writing a level-to-sign mapping with all fourteen of quantity (c)'s
cells published. That inability is the finding and it is a property of the design.

### 3.3 Step 5, reference-set placement. RUN AS FAR AS P2-D25 PERMITS

`A_null(m, F) = sum_o p_{m,F}(o) * A_i(o)` on the floored confirmatory set, with `v2.0`
section 3.2's two aggregates, both emitted so neither reading of the formula is foreclosed.
The marginal `p_{m,F}` is the empirical option marginal over the cell's surviving
renderings, which is uniform across items up to P2-D16's tie attrition; the rendering count
is emitted per cell.

**A finding about the reference set itself, measured on frozen model-free geometry.**
`results/T6_F0_headroom.json` records 8 items on the divergence set where
`o*_infinity != o_fit`, and **zero of them are on the `size` tile**. So on the confirmatory
set `A_i(o_fit) = 1` on all 101 floored items: **the salience reference and the adversary
oracle are the same point**, and `v2.0` section 3.3's four-reference set collapses to
three. That is P2-D5's level confound at its sharpest, and it is why section 3.3 puts every
content claim on excess over the marginal null rather than on raw `A`.

| model | framing | `A_null` median | `A_null` from means | `A` obs median | `A` obs from means |
|---|---|---:|---:|---:|---:|
| `CTRL` | `F0` | -3.6271 | -5.7209 | -3.2766 | -5.0865 |
| `CTRL` | `F1` | -3.9115 | -6.1591 | -3.6321 | -5.6522 |
| `CTRL` | `F2` | -3.7874 | -5.7875 | -3.6030 | -5.4390 |
| `B2` | `F0` | -1.5715 | -2.6983 | -1.4371 | -2.8690 |
| `B2` | `F1` | -1.6165 | -2.6567 | -1.3489 | -2.9626 |
| `B2` | `F2` | -1.8752 | -3.0816 | -1.5423 | -3.3840 |
| `B4` | `F0` | -2.4616 | -3.9728 | -1.8638 | -3.7622 |
| `B4` | `F1` | -2.3971 | -3.9826 | -1.9905 | -3.8863 |
| `B4` | `F2` | -2.3435 | -3.8466 | -2.2148 | -3.8315 |
| `L1` | `F0` | -2.8549 | -4.5013 | -2.1647 | -4.1491 |
| `L1` | `F1` | -3.2901 | -5.0135 | -2.7839 | -4.5484 |
| `L1` | `F2` | -3.2636 | -4.9512 | -3.1018 | -4.5905 |
| `L2` | `F0` | -2.4789 | -3.9637 | -1.2633 | -3.2630 |
| `L2` | `F1` | -2.5008 | -3.9723 | -1.1997 | -3.1465 |
| `L2` | `F2` | -2.4287 | -3.8982 | -1.4286 | -3.2654 |
| `L3` | `F0` | -2.7124 | -4.2472 | -1.6861 | -3.3388 |
| `L3` | `F1` | -3.3241 | -4.8980 | -2.7704 | -4.5626 |
| `L3` | `F2` | -3.3842 | -4.9282 | -2.6891 | -4.4928 |
| `L4` | `F0` | -2.6967 | -4.5722 | -0.9505 | -2.9004 |
| `L4` | `F1` | -2.9952 | -5.1546 | -1.7258 | -4.0880 |
| `L4` | `F2` | -3.2144 | -5.5453 | -2.4552 | -4.6396 |

The excess `A_observed - A_null` is emitted per cell in the artifact and is **descriptive
and licenses nothing**. `v2.0` section 3.3 defines it; P2-D5's second conjunct, which would
make it load-bearing, is UNRULED and stays the author's. Under all three readings of that
conjunct the excess stays descriptive, which is `v2.16` section 5.5's point and is not
re-argued here. The permitted sentence is the flat one: model `m` under framing `F` sits at
or away from what its own option marginal would produce on this item geometry. It is not a
statement about movement and not a claim that a model carries adversary-relevant content.

**`F0` replication on excess over the marginal null** (`v2.0` section 4.2, a gate on
artifact reuse and not a test). `F0` and Paper 1's `cond4` disagree on **0 of 3,500**
size-tile renderings, so every function of chosen options agrees identically there,
`A_null` and the excess included. The gate is satisfied **by construction** on this tile
and `A_null` adds no information to it. Recorded so it is never later presented as a check
that passed on its own strength, which is `v2.16` section 5.2's instruction and holds on
recomputation.

### 3.4 The `ext_i` floor, applied, and the count P2-D23 and `v2.16` both declined

P2-D23 leaves the `ext_i >= 0.02` floor in force on every mean or median of per-item `A`
and on the `ΔA` null; P2-D25 requires it applied and the removed count reported.

**7 of the 108 confirmatory items fall below the floor, leaving 101** for every `A`-ratio
aggregate here: `A_null`'s two aggregates, the observed `A` aggregates, `mean_i A_i(o)`
inside `ΔA_null`, and mean `ΔA`. The removed item ids are in the artifact. `min ext_i` on
the confirmatory set is 0.001340028643 and `max` is 0.5123189453, reproducing P2-D23.

**The confirmatory `n` is untouched and stays 108.** P2-D23 rules the floor out of the
confirmatory set and nothing here reopens that; what the floor reaches is the descriptive
figures, which is exactly what P2-D23 said it reaches.

The floor does **not** reach the control marginals or `TV`, which read chosen options only
and form no ratio. It could not: `ext_i = 0` is the defining property of the control set, so
a floor applied there would delete the control set itself.

`v2.16` section 7 records the ruling session as wanting this count and declining to compute
it, and P2-D23 declined before it, both on the reasoning that it changes a descriptive
figure and not its standing. The count is 7 and that reasoning holds: nothing above turns
on it.

### 3.5 Steps run, partially run, and not run

| step | status | clause |
|---|---|---|
| 1, run the ladder | already done before this session | `data/raw_t7/choices_t7.parquet`, unmodified here |
| 2, `F0` sanity check | already done before this session | `results/T7_f0_replication.json`; re-read, not re-run, and its size-tile figure verified |
| 3, primary analysis | already done before this session | `results/T7_armb_quantities.json`, unmodified here |
| **4, the `beta_c = infinity` control** | **RUN IN FULL** | P2-D25: `TV` on the control set is authorized and is descriptive, on `v2.0` section 4.4's first paragraph, whose ground is independent of the cap |
| **the attribution cap** | **RUN IN FULL** | P2-D25: the cap applies unchanged to mean `ΔA` at descriptive standing; no successor authorized, none claimed |
| **5, reference-set placement** | **RUN, AS FAR AS PERMITTED** | P2-D25: `A_null` per `v2.0` section 3.3 with section 3.2's two aggregates under the `ext_i` floor. The placement is emitted; no reading of it as content is issued, which P2-D5's unruled conjunct blocks and P2-D24 blocks for direction |
| 6, size-ladder analysis | **NOT RUN** | Step 6 asks whether adversary sensitivity appears at any scale. That is a statement that a model does or does not track the adversary, which is what P2-D5's second conjunct blocks and what P2-D25 explicitly does not rule. P2-D25 authorizes no quantity for it. Every table here is ordered by the ladder, so the descriptive substrate exists the moment the blocker is ruled |

### 3.6 What was deliberately not computed

| quantity | why not |
|---|---|
| a control-set same-option or change rate | The natural companion to quantity (a), and P2-D25 does not authorize it. `v2.0` section 4.4's control measure is `TV`. The instruction's rule applies: compute no quantity P2-D25 did not authorize, and an unauthorized quantity one wants is the split working. Flagged in section 7 as a gap the author may want to close |
| a marginal over rendered menu positions | P2-D25 alternative 4, rejected twice over: a new preregistered quantity chosen after the (4,5) signature was seen, and the signature is on canonical ids, which Format V permutes per item and per permutation |
| any mapping from a level onto quantity (c) | P2-D25, and P2-D24 before it. None is authorized and none may be written |
| any successor cap | P2-D25. The cap's object still exists at descriptive standing |
| any verdict on H-B, or any direction claim | P2-D5's conjunct is unruled; P2-D24 rules the direction claim |
| the unfloored `A` aggregates | P2-D25 forbids reporting these aggregates without the `ext_i` floor. Only the floored figures are emitted, with the removed count beside them |

---

## 4. The oracle check

`A <= 1` identically, because `marg_norm <= 1` and `marg_norm(o*_infinity) = 1`, so
`A(o*_infinity) = 1` is the adversary oracle and nothing can exceed it.

**4,532 confirmatory renderings checked, 0 chosen options above `A = 1`, maximum `A` over
chosen options exactly 1.000000.** 4,536 renderings are expected (108 items, two
permutations, three framings, seven models) and 4 are absent to P2-D16's tie exclusion.

`A_null` is a convex combination of per-option `A`, so it carries the same bound, and the
bound is asserted on every per-item `A_null` in every cell rather than on the aggregate
alone. Nothing in this run implies a chooser above the analytically computed optimum.

The `ΔA_null` and mean `ΔA` columns are displacements rather than positions and are not
bounded by 1; no value of either is a claim that anything beat the oracle, and none is read
as one.

---

## 5. What is bound

No new constant and no new binding. `src/t7_control.py` calls the bindings that already
exist:

| call | what it asserts here |
|---|---|
| `bind_marginal_null_use` | P2-D25's six premises, with the nine arguments the ruling names. Called before anything is emitted |
| `bind_ext_floor` | `min ext_i > 0` on the confirmatory set, and that no confirmatory quantity in this run reads `ext_i` |
| `bind_armb` | the tile and the frozen item hash |
| `check_p1_ext_floor_source` | Paper 1's `span > 0.02` is still the floor's governing record |

`tests/test_t7_control.py` adds 21 tests. Each names the premise it protects rather than
pinning a value: that crossing any one of P2-D25's six premises fails the binding; that the
two control bases are the sets P2-D25 names; that the all-tile figure is an item-weighted
mean of within-tile distances and never a pooled marginal; that neither figure is emitted
without its base; that the floor is applied and its cost reported; that `A` is defined on
every item the aggregates use and undefined on every control item; that `TV` agrees with
`c5_effect.tv`, the frozen implementation; that nothing sits above the adversary oracle;
that the cap's label is a function of the two emitted numbers and nothing else; and that
the `pair_delta_A` refactor leaves `v2.7`'s published `c5` `n_eff` counts untouched.

**One refactor.** `inertness_ceiling.pair_delta_A` was factored out of `c5_delta_A` so
`t7_control` could reuse the per-pair `ΔA` instead of copying it, which `CLAUDE.md` treats
as a duplication bug. `c5_delta_A` calls it and computes exactly what it computed before;
the test asserts the frozen `n_eff` counts and the stored sign proportions still reproduce.

---

## 6. Ordering, disclosed

**What this session knew when it computed.** Everything in `DECISIONS.md` through P2-D25,
`v2.0` and `v2.4` through `v2.16`, `T7.md`, both T7 reports including all fourteen cells of
quantities (a), (b) and (c), and the modules. It read the ruling before it read any value,
which is the order the split requires.

**What it did with that.** It computed the quantities P2-D25 authorizes and no others. It
revisited no ruling. Where a quantity it wanted was unauthorized, it recorded the absence
rather than computing it, and section 3.6 lists those.

**The number the ruling session wanted and could not have, now on the table.** `v2.16`
section 7 names it: whether the cap comes out slack or binding against the descriptive
mean. It comes out **binding on 12 of 14 cells and slack on `L2`'s two**. That is recorded
here as an outcome and **not** as an argument for or against a successor cap, because
P2-D25 ruled that question on the form of the quantities and stated in advance that a
binding result would make a successor look urgent and a slack one would make it look
unnecessary. The ruling is not re-read in the light of the number. Anyone reopening it is
reopening it with the number visible, and this paragraph is the record that they are.

---

## 7. Four things this session flags and does not act on

Per the instruction: state what P2-D25 may have got wrong or left unresolved, and stop on
it. Each of the four is the author's. None is resolved, worked around, or treated as
licensing anything.

**7.1 The control set has no authorized inertness measure, and `TV` alone understates the
movement.** P2-D25 authorizes `TV` and P2-D12's quantity (a) on the confirmatory set is a
change RATE, not a distance. The two are different objects: `c5_effect`'s own docstring
records that a high change rate with `TV` near zero is churn, movement that shifts
individual renderings without shifting the distribution. So a control cell with `TV` near
zero is consistent with a model changing a large share of its control choices, and this
run cannot tell the two apart because it computed no control change rate. The gap matters
for exactly the sentence step 4 exists to support: `L2`'s `TV` of 0.0176 under `F2` is the
smallest in the table, and nothing here says whether that cell moved few choices or many
choices symmetrically. **Flagged, not computed.**

**7.2 `ΔA_null` inherits a defect that P2-D25 names and that the numbers make larger than
the naming suggests.** The weight vector `mean_i A_i(o)` spans -0.2366 to -6.9515 across
the six canonical options, a range of 6.7 `A` units, because option 2 sits near the
`o*_0` pole on this tile and the others do not. `ΔA_null` is that vector dotted with a
mass shift, so a two-percent movement of mass between option 2 and option 5 changes it by
about 0.13, which is the same order as most of the observed means it is compared against.
P2-D25 names the mixture defect and declines to repair it, and that is followed. What this
session flags is that the defect is not symmetric noise: it makes `ΔA_null` a function
mostly of how much mass moves on or off one option. Whether that leaves the cap worth
reporting at all is the author's.

**7.3 P2-D25 does not say how the marginal `p_{m,F}` is aggregated, and this run had to
read it one way.** `v2.16` section 4 resolves the aggregation over items by emitting both
of `v2.0` section 3.2's aggregates, so neither reading is foreclosed. It does not raise the
adjacent question on the other index: whether `p_{m,F}(o)` is the marginal over the cell's
renderings or the mean of per-item marginals. This run uses the marginal over surviving
renderings, which is `v2.0` section 3.3's phrase "computed within model and within framing
over the confirmatory analysis set" read directly, and it emits the rendering count per
cell so the weighting is visible. The two readings coincide except for P2-D16's tie
attrition, which is 4 renderings out of 4,536 on this run, so nothing here turns on it.
**Recorded because it is an ambiguity a later session on a noisier cell could resolve
differently, and `CLAUDE.md` forbids resolving an ambiguity by choosing.** It is not
resolved here; it is stated, with the reading used and the size of what it could cost.

**7.4 A trigger in P2-D24 has fired, and this session did not act on it.**
`P2D24_MARGINAL_NULL_COMPUTED` is `False`, and
`tests/test_p2d24_direction.py::test_the_marginal_null_is_still_uncomputed` carries the
docstring "P2-D24's status call depends on it. If a run computes it, re-read the entry."
This run computed it. The test still passes, because it asserts the constant's value and
asserts that no `A_null` quantity has entered `results/T7_armb_quantities.json`'s
confirmatory cells, and both remain true: the new quantities live in a separate artifact
and the confirmatory family is untouched. What is now false is the sentence in P2-D24's
premise 1, "`A_null` and `v2.0` section 4.4's attribution cap `ΔA_null` have never been
computed for Paper 2."

The half of premise 1 that the ruling rests on is untouched: no rule maps a level excess
onto a sign proportion, so using either to license a direction claim on quantity (c) is
still post-hoc, and P2-D25 restates that and forbids writing such a rule. Only the
record-of-fact half is stale.

**The constant is not changed and P2-D24 is not edited.** Changing it means editing a
decision entry's text, which this session is forbidden to do and which would be ruling.
The trigger is recorded here so that a later reader finds the fired trigger rather than a
silently-still-`False` constant. Re-reading P2-D24 is the author's.

---

## 8. What this version changes

- `src/t7_control.py` is added: T7 step 4, the attribution cap, and step 5's placement.
- `src/inertness_ceiling.py` gains `pair_delta_A`, factored out of `c5_delta_A`, which
  computes what it computed before.
- `results/T7_control_marginal_null.json` and `reports/T7_control_marginal_null.md` are
  added.
- `tests/test_t7_control.py` is added.
- **No `results/*.json` value that existed before this session changed**, verified by
  hashing every file before and after and by walking the old key set against the new: 13
  pre-existing JSON files, 0 lost keys, 0 changed values. No superseded preregistration
  version is edited. No new `P2-D` number is taken and no decision is recorded.
- `p0` is 0.5. The confirmatory family is 21 tests at `alpha = 0.05/21`. The confirmatory
  `n` is 108. P2-D5's blocker stays open and stays the author's.
