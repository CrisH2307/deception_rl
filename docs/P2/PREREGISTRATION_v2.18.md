# PREREGISTRATION v2.18

**Paper 2: the adversary effect and the RL Scientist**

Version 2.18 · written 2026-09-15 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.17`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
nineteen are read together. This version records **the author's ruling on P2-D5's
blocker**, which every entry from P2-D21 onward has carried as open and which P2-D24 was
deliberately built not to depend on.

It changes no statistic, no `alpha`, no `p0`, no coordinate, no item set and no `n`. It
computes nothing. It closes the last open entry in the scope registry.

| # | decision | where |
|---|---|---|
| 1 | P2-D5's blocker is discharged as permanently blocking, on a structural ground, not pending measurement. | §2, **P2-D26** |
| 2 | The confirmatory confound is 108 of 108, never 452 of 460. | §4, **P2-D26** |
| 3 | Factual correction to P2-D24's premise 1: the marginal null has now been computed. Substance untouched. | §5 |

**Provenance.** This ruling was made **by the author**, in writing. This session recorded
it and did not make it. The author's words are quoted in full in P2-D26 in
`docs/P2/DECISIONS.md` and the decision text is drawn from them. That distinction is the
one P2-D16's provenance correction exists to keep visible: an entry written by a session
from an author instruction and an entry the author wrote are different objects, and only
the second may be recorded as the author's ruling without qualification.

---

## 1. The measurement it rests on

Emitted by `src/t7_control.py` under P2-D25, and reproduced independently from
`df["o_fit"]` and `t6_arm_a.arm_a_columns`, the path that produced
`results/T6_F0_headroom.json`'s `n_o_star_inf_equals_o_fit`:

| tile | divergent items | `o*_infinity == o_fit` | separating |
|---|---:|---:|---:|
| `hold` | 116 | 116 | 0 |
| `manmade` | 114 | 111 | **3** |
| `moves` | 122 | 117 | **5** |
| **`size`** | **108** | **108** | **0** |
| pooled | 460 | 452 | 8 |

**All 8 separating items are on `manmade` and `moves`. None is on `size`.** So on the
confirmatory set the adversary-aware optimum and the salience pole are the same option,
on every item, and `v2.0` section 3.3's four references collapse to three there.

---

## 2. The ruling. **P2-D26**

> P2-D5's blocker is DISCHARGED as permanently blocking, on a structural ground, and
> not pending further measurement. On the `size` confirmatory set `o*_infinity` equals
> `o_fit` on all 108 items: of the 8 divergent items where the two differ, 3 are on
> `manmade` and 5 on `moves`, and none is on `size`. The adversary-aware optimum and
> the salience pole are therefore the SAME OPTION throughout the confirmatory set, and
> `v2.0` section 3.3's four references collapse to three there. **No Arm B quantity
> computed on that set can support a claim about adversary tracking**, because the
> coordinate cannot distinguish adversary-aware behaviour from salience-driven
> behaviour when the two targets are one point, and no successor measure on `size` can
> either. This is not a caveat to attach to a result. It is why the direction question
> was never answerable on this set, and it explains P2-D24 from the other side: P2-D24
> found that the design licenses nothing about direction, and this says why. The tile
> is not revisitable: Paper 1's D49 and D108 fixed `size` on measured grounds before
> any of this was known, and the 8 separating items sit on tiles those decisions
> excluded. The confirmatory confound is stated as **108 of 108** and never as 452 of
> 460, which is a divergence-set figure and understates the confirmatory case.

---

## 3. Discharged, not satisfied, and not still pending

Three different states, and the log has used all three, so the difference is worth stating.

- **Satisfied** would mean an Arm B quantity is an excess over the marginal null. None is,
  and P2-D25 confirmed none may be made into one.
- **Pending** would mean a further measurement could meet it. None could, because the
  obstacle is not in the measure.
- **Discharged** means **the claim the conjunct gated is unavailable for a reason that
  precedes the conjunct.** A rule about how to support a claim stops governing when the
  claim cannot be made at all.

### 3.1 Why no successor measure on `size` helps

This is the part that makes the discharge permanent rather than provisional.

The confound is **not a property of `A`**. `A` pins `o*_0` at 0 and `o*_infinity` at 1, and
on this set `o*_infinity` IS `o_fit`, so a model at `A = 1` is at the salience pole and at
the adversary-aware optimum with one choice. Any measure built on the confirmatory item set
inherits that, because the two targets are the same option there and **no function of a
chosen option can separate two labels attached to the same option**.

The separation is absent from the item set, not from the coordinate. That is why "design a
better measure" is not an available move.

### 3.2 Why the tile is not revisitable

Three independent grounds. D49 selected `size` on `fit_cost` coverage, because it spans the
full range on its own where tile-balanced selection would confound tile with `fit_cost`.
D108 confirmed the primary curve rests on `size` alone, because `moves` sits below its
marginal null at all four rungs and `hold` carries approximately nothing. Both predate this
measurement. And the 8 separating items sit on `manmade` and `moves`, which are the tiles
D108 found carry approximately nothing, so admitting them would import the separation
together with the tiles the design excluded for measured reasons. It would also be a
frozen-artifact change, which `CLAUDE.md` forbids.

---

## 4. The confirmatory figure is 108 of 108

`452 of 460` is a **divergence-set** figure. On the confirmatory set the confound is not
overwhelming but **total**, and citing the divergence-set number where the confirmatory set
governs understates it.

P2-D5's own text is unchanged and its `452 of 460` is correct about the set it describes;
a forward note beside that entry says which figure governs Arm B. Two live sites that cited
the divergence figure where the confirmatory set governs are corrected:
`src/inertness_ceiling.py`'s diagnostic docstring and `DECISIONS.md`'s direction-finding
note. Sites that describe the divergence set, in `src/t6_f0_headroom.py`,
`reports/T2_frozen_set_counts.md` and `reports/T6_arm_a.md`, are correct and unchanged.
`bind_adversary_tracking_claim` refuses a caller that cites 452 for the confirmatory set.

---

## 5. Factual correction to P2-D24, recorded as a correction

P2-D24's premise 1 said `A_null` and `ΔA_null` "have never been computed". That was true
when it was written and became false when `src/t7_control.py` computed both under P2-D25.

**This is a factual correction, not a ruling.** Premise 1's substance is that no
confirmatory quantity is an excess over the marginal null and that using either to license
a direction claim on (c) would be post-hoc. That is untouched, and P2-D25 authorized the
computation precisely as preregistered work, so the fact changing is the entry **working**
rather than failing. `P2D24_MARGINAL_NULL_COMPUTED` moves from `False` to `True` and gains
`P2D24_MARGINAL_NULL_COMPUTED_BY`. P2-D24's decision text is not edited; it never contained
the stale phrase.

The tripwire that caught this fired correctly: a test said "if a run computes it, re-read
the entry", a run computed it, and the entry was re-read. Two other tests that asserted the
registry stay open also fired, and both were inverted rather than deleted, so the record
shows the state changing rather than the assertion disappearing.

---

## 6. What survives, and it is not nothing

P2-D9's exact zero makes the movement claim strong. Quantity (a) clears P2-D13's floor on
all 14 cells, 30 to 77 items of 108, against a no-effect rate of exactly 1.0.

> **The framings changed the chosen option.**

That claim reads chosen options only, needs no direction, and is untouched by this entry.
What Arm B cannot say **on this set** is what the movement was toward.

P2-D24 and P2-D26 say the same thing from two sides. P2-D24 ruled, from three inputs, that
the design licenses nothing about direction. P2-D26 gives the reason: the direction question
was never answerable on this set. Neither supersedes the other, and P2-D24 is not weakened
by being explained; its three premises were each independently sufficient and each remains
true.

---

## 7. The scope registry is empty

`scope_audit()` and `undefended()` both return empty for the first time since the registry
was created. The entry carrying `v2.0` section 4.4's cap, section 4's movement criterion and
P2-D5's conjunct is now `ruled_by` P2-D25 and P2-D26.

**The `defends_against` hypothesis is discharged with it, and the reason matters**: not
because the defence was restored, but because the claim it protected is unavailable. The
generic-shift hypothesis mattered only because an adversary-tracking claim had to rule it
out. There is no such claim left to protect on this set.

An empty registry is not a guarantee that no scope has expired. It is maintained, no parser
can tell a scope from a mention, and the registry could not catch the cap until it was
written, which `DECISIONS.md` records as the limit of the countermeasure.

---

## 8. What this version changes

| | |
|---|---|
| P2-D5's blocker | **discharged**, structurally, not pending measurement |
| adversary-tracking claims on the confirmatory set | **unavailable**, and no successor measure on `size` changes that |
| the tile | not revisitable; D49 and D108 stand |
| the confirmatory confound figure | **108 of 108**, never 452 of 460 |
| P2-D24 | unchanged in substance; one stale fact corrected and recorded as a correction |
| the scope registry | empty for the first time |
| statistics, `alpha`, `p0`, coordinates, item set, `n` | unchanged |
| the movement claim | untouched and strong, on P2-D9's exact zero |
