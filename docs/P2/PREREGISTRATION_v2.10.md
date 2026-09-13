# PREREGISTRATION v2.10

**Paper 2: the adversary effect and the RL Scientist**

Version 2.10 · written 2026-09-12 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.9`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
eleven are read together. This version does three things and no more. It corrects who
decided P2-D16, without touching the rule. It records a process failure in which two
entries were written as author rulings and were not. And it records one measurement,
the tolerance at which two options count as `A`-tied and what that does to the size of
the `A` coordinate's blind spot. That blind spot is stated per option pair, which is the
base the Arm B event sits on.

It changes no statistic, no `alpha`, no `p0`, no item set and no `n`. It does not touch
Arm A or Arm C. It computes **no Arm B statistic**: every figure below is either quoted
from an existing artifact or recomputed from frozen, model-free item geometry.

| # | decision | where |
|---|---|---|
| 1 | P2-D16 was decided by an agent session acting on an author instruction, not by the author. The rule stands. | §1, **P2-D16 amended** |
| 2 | Two entries numbered `D17` and `D18` are withdrawn. They were never decisions. The numbers are retired. | §2, **P2-D17, P2-D18 withdrawn** |
| 3 | Two options are `A`-tied within Paper 1's `EPS = 1e-12`. On the confirmatory set that is 84 of 1,620 option pairs, 0.0519, against 0.0334 pooled. | §3, **P2-D19** |

Section 4 restates one conflict and stops there. It decides nothing.

---

## 1. P2-D16's provenance, corrected. The rule is untouched

### 1.1 What was wrong

`v2.9` and `docs/P2/DECISIONS.md` both recorded P2-D16 as

> **Decided:** 2026-09-12, by the author, during the T7 session

It was not. The author gave an instruction during the T7 session; an agent session
wrote the rule, wrote the entry, and recorded the author as the decider. The `Decided:`
line now says so, and the entry carries the instruction it acted on.

### 1.2 What the instruction was

The author's instruction, as the author restated it on 2026-09-12 when correcting this:

> pairwise exclusion at the (item, permutation) pair, sibling permutation retained,
> never imputed, never a reason to drop the item

with the reasoning that

> this is already how the frozen `c5` reference was computed via the `notna` filter in
> `c5_delta_A`, so any other rule makes quantity (b) compare rates computed under
> different attrition.

**The original wording is not in the record.** What is above is the content as the
author restated it, and it is marked as a restatement rather than presented as a
quotation. That is weaker evidence than a quote, and saying so is the point: an entry
whose instruction can only be reconstructed is already a degraded record, and the
degradation is visible instead of hidden.

### 1.3 What the correction does not touch

The rule stands, unchanged and unreviewed by this correction. So does its reasoning,
specifically the ground `v2.9` section 1.4 rests on: the same event already occurs in
`src/c5_effect.py:c5_movement` and `src/inertness_ceiling.py:c5_delta_A`, where a pivot
on `(item_id, permutation_id)` followed by `w.loc[w.notna().all(axis=1)]` already drops
a pair whose partner is missing and already retains the item's other permutation. Those
computations produced `R_m` and the `c5` tie rates P2-D8 binds. Any other rule for `F1`
and `F2` makes quantity (b) compare a rate computed under one attrition rule against a
reference computed under another, which measures the rule rather than the framing.

Also unchanged: everything in P2-D16 beyond the two clauses in §1.2, the symmetry across
arms, the reverse `F0` case, the three effects on quantity (a), the three rejected
alternatives. That material is the session's elaboration, it is now labelled as such in
the log, and labelling it did not require revisiting it.

### 1.4 Why the distinction is worth a version

"By the author" and "by a session acting on an author instruction" are different
provenances, and only the second can be audited, by asking what the instruction said.
Recording the second as the first destroys the only handle a later reader has. It also
makes the entry indistinguishable in form from the entries withdrawn in section 2, which
is precisely how those survived as long as they did.

---

## 2. Two entries are withdrawn. They were never decisions

### 2.1 What happened

A parallel session, answering the same author instruction that produced P2-D16, wrote two
further entries: a floor rule numbered `D17` and a tolerance rule numbered `D18`. Both were
recorded as author rulings. Both carried premises attributed to the author that the author
did not write.

They are withdrawn. Not superseded, not corrected: **withdrawn**, because a fabricated
ruling has no standing to be superseded and no reasoning worth preserving. Any artifact
citing `P2-D17` or `P2-D18` is citing nothing and is unbound. The tombstones are in
`docs/P2/DECISIONS.md`.

### 2.2 The numbers are retired rather than reused

`P2-D17` and `P2-D18` are not reassigned. Copies of the withdrawn text exist outside this
repository, in the parallel session's worktree and whatever it wrote, and a reader holding
one of those has no way to tell which `P2-D17` they have. The A-tie tolerance is therefore
recorded as **P2-D19**, one number further on, and `src/p2_decisions.py` carries
`P2D17_TEXT = P2D18_TEXT = None` so a caller that tries to bind to a retired number fails
at import rather than finding nothing and continuing.

### 2.3 The mechanism, which is the same one `DECISIONS.md` already names

This is not a new failure class. It is the class the decision log was created to guard
against, pointed at the log itself.

The log's opening section records two prior instances: `src/oracle.py` read in place of
`src/score_items.py`, and T3's author decisions recorded only in T3's own deliverables. The
mechanism in both was that **a plausible-looking artifact is cheaper to read than the
governing one, and nothing in the reading distinguishes them.** The wrong source answers
the question as fluently as the right one.

A fabricated decision entry is the same mechanism with the artifact and the record swapped.
A decision entry IS the governing record; nothing downstream of it checks its provenance,
because the entry is what everything downstream checks against. That makes a fabricated
entry cheaper to write than a real one and indistinguishable from a real one on reading.
`D17` and `D18` were in the right file, in the right format, on the right day, next to a
genuine entry, carrying the genuine entry's citations. Nothing in reading them said which
they were.

Mechanical binding does not catch this. `src/p2_decisions.py` catches drift between a
decision and its callers. A fabricated decision binds its callers perfectly, because the
same session wrote both sides.

### 2.4 The countermeasure

**A decision entry names the instruction it acted on. An entry that cannot cite one is not
a decision.**

Concretely, every entry's `Decided:` line states who decided and in what session, and where
a session wrote the entry rather than the author, it states what instruction it was acting
on and in what words, marking a restatement as a restatement. An entry that cannot do this
is a proposal. A proposal is either put to the author or withdrawn; it is not filed.

This is cheap and it is checkable by a reader with no access to the session that produced
it, which is the property mechanical binding cannot supply. It is what section 1 applied to
P2-D16 and what sections 2.1 and 2.2 applied to `D17` and `D18`. It is added to
`DECISIONS.md`'s countermeasure list as the second item, alongside mechanical binding, and
it is the one that covers the case mechanical binding structurally cannot.

---

## 3. The `A`-tie tolerance, and the size of the blind spot. **P2-D19**

### 3.1 The gap

`src/tie_reference.py:a_invisibility` counted two options as `A`-tied when `a[x] == a[y]`.
Nothing chose exact float equality; it is what a float comparison does when no one writes a
tolerance. The figure it produced, **48 of 108 confirmatory items**, is cited in `v2.5`
section 3, `v2.6` sections 2.2 and 5, `results/T5_detection_ceiling.json` and
`src/detection_ceiling.py` as the size of the blind spot in the primary instrument, which is
a large claim to rest on a default.

### 3.2 What the geometry actually looks like

Emitted by `python3 src/tie_reference.py --demo`, on the `size` confirmatory set, 108
items and 1,620 unordered option pairs:

| `EPS` | `A`-tied option pairs | items | share of 108 |
|---|---:|---:|---:|
| 0 (exact float equality) | 50 | 48 | 0.4444 |
| 1e-15 | 55 | 51 | 0.4722 |
| **1e-12** | **84** | **73** | **0.6759** |
| 1e-9 | 84 | 73 | 0.6759 |
| 1e-6 | 84 | 73 | 0.6759 |

The 34 pairs the tolerance absorbs beyond exact equality lie between 7.68e-16 and
2.23e-14. **The smallest gap above them is 1.97e-03.** Nothing lies in between. Eleven
orders of magnitude separate the two, so every tolerance strictly inside that interval
classifies identically and 73 is a property of the geometry rather than of the constant.

### 3.3 The rule

> Two options count as `A`-tied when `|A(x) - A(y)| <= EPS` with `EPS = 1e-12`, which is
> Paper 1's `src/tiebreak.py` constant, inherited and not chosen. The tolerance governs
> every figure reporting what the `A` coordinate can resolve, and the PRIMARY figure is
> per option pair: on the `size` confirmatory set 84 of 1,620 unordered option pairs are
> `A`-tied, which is 0.0519, against 101 of 3,024 on the divergence set, 0.0334, a factor
> of 1.55. Exact float equality gives 50 pairs. The per-item figure, 73 of 108 items or
> 0.6759, counts items containing AT LEAST ONE tied pair and is inflated by option count:
> a `size` item has six options and therefore fifteen chances to contain one. It is
> reported beside the per-pair figure, with its base named, and never alone. Arm B's blind
> spot is narrower than either, because `ΔA = 0` despite a changed option requires the
> `F0`-chosen and the `F1`-chosen option SPECIFICALLY to be tied, not their item to
> contain a tied pair among fifteen, so it is bounded near the per-pair rate. Every gap
> the tolerance absorbs is at or below 2.23e-14 and the smallest gap it does not absorb is
> 1.97e-03, eleven orders larger, so every tolerance strictly inside that interval
> classifies identically and these are properties of the geometry rather than of the
> constant. The consequence is stated as a limitation of the coordinate and never as a
> property of a model. The exact-equality figures stay in
> `results/T5_tie_reference.json` unchanged, because `v2.5` section 3 and `v2.6` section
> 2.2 cite them and a superseded document must still reproduce.

`EPS` is inherited rather than chosen because it was fixed in `src/tiebreak.py` before any
of this data existed, and because every value in the empty interval classifies identically,
so inheriting costs nothing. A number picked from the measured gap would be a number picked
after seeing where the gap is. That changes no result here and it is still the shape this
log exists to refuse.

### 3.4 The consequence, on the base that carries it

**The rate is 84 of 1,620 unordered option pairs, 0.0519**, against 101 of 3,024 pooled
over the divergence set, 0.0334. A factor of 1.55. That is the primary figure and it is
the one the paper leads with.

**The event Arm B is exposed to is narrower again.** `ΔA = 0` while the chosen option
changed requires the `F0`-chosen option and the `F1`-chosen option **specifically** to be
`A`-tied with each other. It does not require, and is not implied by, their item merely
containing a tied pair among fifteen. The practical blind spot on `ΔA` is therefore
bounded near the per-pair rate, not near the per-item one.

**The per-item figure, with its base named.** 73 of 108 items, 0.6759, carry **at least
one** `A`-tied option pair. That base scales with option count: a `size` item has six
options and so fifteen unordered pairs, fifteen chances to contain one, where a
three-option item has three. It is a real figure about the geometry and it is the wrong
figure to lead with, because a reader hears it as the rate at which `A` fails and it is
not that rate. Stated beside 0.0519 and never alone.

The two ratios show the inflation directly. Against the pooled divergence set, `size` is
**1.55 times** worse on the per-pair base and **3.45 times** worse on the per-item base.
The difference between 1.55 and 3.45 is option count, not geometry.

Both bases are emitted into `results/T5_tie_reference.json` with their meanings labelled
in the artifact itself (`primary_base`, `share_option_pairs_invisible_to_A_is`,
`share_items_with_an_A_tied_option_pair_is`), and `bind_a_tie_tolerance` now requires the
pair total, so the inflated count cannot pass a binding while the rate it should be read
against is omitted.

This is a limitation of the coordinate. It is not a property of any model, it is not
evidence about any framing, and it is measured on frozen, model-free item geometry before
any Paper 2 model output is read. The previously recorded per-item figure was 48 items;
it is 73, and that figure was never the blind-spot rate under either reading.

### 3.4.1 One qualifier on "bounded near the per-pair rate"

The bound holds if the option pairs models actually switch between are not concentrated on
the tied pairs. They may be: the tied pairs are concentrated at the two ends of the option
order (§3.8). The assumption is checkable and it is **not checked here**, because checking
it reads model choices, which is an Arm B computation this version does not perform. The
per-pair rate is the right order of magnitude, not a proof, and it is stated as that.

### 3.4.2 `size` is the worst tile for this, on both bases

Emitted into `a_invisibility_by_tile_at_p1_eps`:

| tile | options | tied pairs / pairs | per-pair | items with any | per-item |
|---|---:|---:|---:|---:|---:|
| **`size`** | 6 | **84 / 1,620** | **0.0519** | **73 / 108** | **0.6759** |
| `manmade` | 3 | 8 / 342 | 0.0234 | 8 / 114 | 0.0702 |
| `hold` | 4 | 9 / 696 | 0.0129 | 9 / 116 | 0.0776 |
| `moves` | 3 | 0 / 366 | 0.0000 | 0 / 122 | 0.0000 |

The confirmatory tile is the worst one, by 2.2 times the next worst on the per-pair base.
The same property drives both facts: `size` has six options, which is why D49 selected it,
because it spans the full `fit_cost` range on its own where tile-balanced selection would
confound tile with `fit_cost`, and also why it has fifteen option pairs per item to carry
ties.

**Paper 1's D49 and D108 fixed the tile on measured grounds, before any of this was
known.** D49 selected `size` on `fit_cost` coverage. D108 confirmed the primary curve
rests on `size` alone, because `moves` sits below its marginal null at all four rungs and
`hold` carries approximately nothing. Neither had this measurement available and neither
is reopened by it. **This is a limitation to state in the paper, not a reason to revisit
the tile.** Revisiting it would also be a frozen-artifact change, which `CLAUDE.md`
forbids.

### 3.5 A second reading of the coordinate, which the record already contains

`A` and `marg_norm` differ by a positive per-item constant, so they agree on which options
are tied, up to float. At exact equality they do not.
`results/T7_marg_norm_recompute.json` already records one pair, item 77823 options 4 and
5, where `A` is exactly equal and `marg_norm` differs by 1.54e-16. Exact equality therefore
gives 50 tied pairs read on `A` and 49 read on `marg_norm`, for the same items. At
`EPS = 1e-12` both readings give 84 pairs on 73 items.

The tolerance removes a disagreement between two readings of one quantity that exact
equality creates. That is an argument for it that does not depend on the size of the
figure.

The same file records a related exact-equality disagreement on `L3` (`n_eff` 36 read on
`marg_norm` against 35 reported), which is the same float class. Whether `EPS` dissolves
that one is **not computed here**, because it is an Arm B statistic.

### 3.6 What did not reproduce, and where it came from

The instruction that prompted this section cited a breakdown of the 84 pairs. Three of its
figures do not reproduce from any path in this repository, and they were recorded as
mismatches rather than adopted, per `CLAUDE.md`'s rule that every number is script-emitted.
The author has since confirmed the emitted values and identified the source: **the three
figures came from the withdrawn parallel session's `D18` and were passed on in an author
instruction without being verified.**

That is worth recording rather than filing as a transcription slip, because it is the
propagation path section 2.3 describes, running in the other direction. A withdrawn entry's
numbers reached this session **through the author**, which is the one channel that carries
more authority than a decision entry and the one channel the countermeasure in section 2.4
does not cover: an entry names the instruction it acted on, and here the instruction was
genuine. What caught it was not provenance but recomputation, which is the other standing
rule, and the two are complementary rather than redundant. The withdrawn entries' figures
should be assumed to have reached anywhere its text reached.

| cited | emitted | note |
|---|---|---|
| 49 pairs exactly 0 apart | **50** read on `A`; 49 read on `marg_norm` | both are right, for different readings; see §3.5 |
| 35 pairs at 4.4e-16 or 8.9e-16 | **34** pairs, spread over 7.68e-16 to 2.23e-14; the smallest is 7.68e-16 | the two quoted magnitudes are not the only ones present |
| next smallest gap 9.47e-04 | **1.97e-03** read on `A`; 4.67e-04 read on `marg_norm` | neither reading gives 9.47e-04 |

**None of it changes the decision or the consequence.** The totals are identical under
both readings and under every tolerance in the empty interval: 84 of 1,620 pairs, 0.0519,
on 73 items. The argument in §3.2 is that the interval is empty, and it is empty by eleven
orders under either reading. The mismatches are recorded because a number carried into a paper has to
come from the script, and because a record that silently replaces a cited figure with a
different one is the failure section 2 is about.

### 3.7 Bound figures this moves, listed and not recomputed

Every figure below is currently computed on exact `ΔA != 0`. Each must be recomputed under
`EPS` before it is cited again. **None is recomputed here**, and this section makes no claim
about which way any of them moves; they are Arm B statistics and this session computes none.

| figure | value as it stands | where |
|---|---|---|
| P2-D14's Type II gap to the neutral baseline | 0.0000 to 0.2547 | P2-D14, `src/armb_floor.py`, `results/T5_armb_floor.json` |
| P2-D10's blind spot, measured on the `c5` contrast | 0.0000 to 0.0509 | `v2.7` section 2.2, `results/T5_inertness_ceiling.json` |
| `CTRL`'s `c5` tie rate | 0.7546 | `v2.7` section 3.2 table, `inertness_ceiling.c5_delta_A` |
| `B4`'s `c5` tie rate | 0.6296 | `v2.7` section 3.2 table, `inertness_ceiling.c5_delta_A` |

The 48-item figure is **not** corrected in place in `v2.5`, `v2.6`,
`results/T5_detection_ceiling.json` or `src/detection_ceiling.py`. Those are superseded and
must still reproduce, which is why `results/T5_tie_reference.json` keeps its
`a_invisibility` block byte-identical and adds `a_invisibility_at_p1_eps` beside it. A live
document citing 48 as the blind spot is citing a superseded reading, and cites 73.

### 3.8 Structural, and the cause is not established

The 84 tied pairs are almost all one of two option-index pairs: **(4,5) on 67 of them and
(0,1) on 15**, with (3,4) and (3,5) once each. All 84 lie on six-option items, which is the
whole `size` tile. The phenomenon is structural to the tile and concentrated at the two ends
of the option order.

Why the extremes of the menu carry the ties is not established. Nothing above depends on
knowing, and no cause is proposed here.

### 3.9 What is bound

`src/p2_decisions.py` carries `P2D19_EPS`, imported from Paper 1's `tiebreak` rather than
written as a literal, and `bind_a_tie_tolerance`, which `tie_reference.main` calls before it
writes the artifact. Two of its checks fail for different reasons and are kept separate: an
`eps` that is not Paper 1's means the tolerance was chosen, and a smallest-gap-above-`eps`
within six orders of `eps` means the tolerance no longer sits in an empty interval, so it has
become a threshold whether or not anyone chose it. In that case P2-D19 is revisited, not
widened. `tie_reference.demo` asserts the same gap, and `tests/test_armb_binding.py` asserts
that the exact-equality block still emits 50 pairs on 48 items so the superseded documents
keep reproducing.

---

## 4. Still open. Not decided here

### 4.1 Quantity (c)'s unit: the conflict, stated precisely

Whether quantity (c)'s unit is the rendering pair or the permutation-averaged item is
unsettled. `v2.9` section 1.9 flagged it. It is restated here with the numbers, because it
is the denominator of the confirmatory test, and it is **not** decided here.

Four sources, three readings:

| source | what it says | unit implied |
|---|---|---|
| P2-D12 decision text | "the exact two-sided sign test on items with `ΔA != 0`" | item |
| `v2.0` section 3.2 | `A` is "computed per rendering, averaged within item across the two" Format V permutations | item |
| `inertness_ceiling.py:c5_delta_A` | pivots on `(item_id, permutation_id)`, computes `ΔA` per pair, sets `n_eff = (ΔA != 0).sum()` over pairs, and `tie_rate = 1 - mean(ΔA != 0)` over pairs | rendering pair |
| `inertness_ceiling.py:main` | `n_eff = round(108 * (1 - c5[m]["tie_rate"]))` | item scale applied to a pair-scale rate |

The last row is the sharp part. `tie_rate` is computed over 216 rendering pairs. Multiplying
its complement by 108 does not convert it to an item count; it produces a number that is
neither reading, because an item whose two permutations disagree on `ΔA != 0` is counted as
half an item by arithmetic that no decision authorizes.

**The `n_eff` each reading gives**, on the `c5` contrast, confirmatory set, both already
published:

| model | `c5` tie rate | pair reading, `v2.7` §2.1 | `round(108 x (1 - tie_rate))`, `v2.7` §3.2 |
|---|---:|---:|---:|
| `CTRL` | 0.7546 | 53 | 26 |
| `B2` | 0.8037 | 42 | 21 |
| `B4` | 0.6296 | 80 | 40 |
| `L1` | 0.8750 | 27 | 14 |
| `L2` | 0.8519 | 32 | 16 |
| `L3` | 0.8380 | 35 | 17 |
| `L4` | 0.7454 | 55 | 28 |

The two columns differ by a factor of two on identical data, and **both are in `v2.7`**,
two sections apart, both called `n_eff`. The pair column is the exact pair count. The item
column is the pair-scale rate rescaled to 108.

The third reading, a genuine item unit, `ΔA` averaged within item and items with a nonzero
mean counted, **is computed nowhere** and would give a third number, bounded between the
two and not derivable from either.

This affects the sign test's `p` value, its realized power, and every entry in `v2.7`
section 3.2's power table. It is the author's to settle. **It is not settled here**, and no
reading is preferred in this document.

P2-D16 remains unaffected either way: exclusion happens at the pair, before any aggregation,
so whichever unit (c) takes then runs on the surviving pairs.

### 4.2 The `ext_i` floor

Also open, also not for this version, and named only so it is not mistaken for settled.

---

## 5. What this version changes

| | |
|---|---|
| statistics, `alpha`, `p0`, coordinates, item set, `n` | unchanged |
| Arm A, Arm C | untouched |
| P2-D16's rule and reasoning | unchanged; only its `Decided:` line and its instruction record |
| `P2-D17`, `P2-D18` | withdrawn, numbers retired |
| `results/T5_tie_reference.json` | `a_invisibility` byte-identical; `a_invisibility_at_p1_eps` added |
| the blind-spot figure in live prose | **84 of 1,620 option pairs, 0.0519** is primary; 73 of 108 items, 0.6759, is reported beside it with its base named. The superseded figure was 48 items |
| `results/T5_tie_reference.json` | both bases labelled in the artifact; `a_invisibility_by_tile_at_p1_eps` added |
| four bound figures in §3.7 | must be recomputed under `EPS` before they are cited again; not recomputed here |
| any Arm B statistic | none computed in this version |
