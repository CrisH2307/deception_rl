# PREREGISTRATION v2.14

**Paper 2: the adversary effect and the RL Scientist**

Version 2.14 · written 2026-09-13 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.13`.

New file per Paper 1's **D148**: earlier versions are never edited in place and all
fifteen are read together. This version settles the last item the recent versions kept
naming as open: **whether `v2.0` section 7.2's `ext_i >= 0.02` floor applies to Arm B's
confirmatory set**, which would cut `n` below 108.

**It does not.** The confirmatory `n` is 108. The floor is retained, unamended, on the
quantities it was written for. It computes **no `F1` or `F2` statistic**, and it reopens
neither P2-D6, P2-D19 nor P2-D20.

| # | decision | where |
|---|---|---|
| 1 | The `ext_i >= 0.02` floor does not reach any confirmatory quantity. `n` stays 108. | §3, **P2-D23** |
| 2 | It remains in force, unamended, on the mean and median of per-item `A` and on the `ΔA`-against-`ext_i` correlation. | §5, **P2-D23** |

**The instruction this acted on**, per `v2.10` section 2.4's countermeasure: the author
stated the open question, reported an earlier session's three claims and required each be
verified rather than trusted "at the item unit adopted in P2-D20", since "the earlier
report predates both P2-D19 and P2-D20 and may not survive them"; required both `0.02` and
`0.00134` be treated as unverified and recomputed; forbade reopening P2-D6, P2-D19 and
P2-D20; and required that **if the floor turns out to bind on a confirmatory quantity, the
session say so and stop rather than choose a remedy**. Quoted in full in P2-D23 in
`docs/P2/DECISIONS.md`. Written by an agent session acting on that instruction, not by the
author.

**Ordering, disclosed.** The smallest `ext_i` in the confirmatory set was known to this
session before the ruling, because an earlier step printed it. **Which items fall below the
floor was not inspected**, the per-item `ext_i` export was not opened for that purpose, and
**the count of items below the floor was deliberately not computed.** That count is never
needed: if the floor does not bind it is irrelevant, and if it binds the instruction
requires stopping rather than sizing a remedy. The ruling rests on the form of the
quantities, not on what an exclusion would cost.

---

## 1. Both numbers recomputed

| carried in the instruction | recomputed | source |
|---|---|---|
| floor `0.02` | **0.02** | `span > 0.02` in Paper 1's `src/frontier_position.py`, verified present |
| smallest `ext_i` `0.00134` | **0.001340028643** | `t6_f0_headroom.item_axis`, `size` confirmatory set |

Also measured: `max ext_i` is 0.5123189453, and **no confirmatory item has `ext_i <= 0`**.
The last is not decoration. The ruling rests on a strictly positive denominator, and zero
is the one value that breaks it.

---

## 2. What Paper 1's floor is actually for

Paper 1's decision log has no entry for this floor. The governing record is the comment
beside the expression, which is why `p2_decisions.check_p1_ext_floor_source` asserts that
expression is still there.

> A mean of per-item ratios is not usable here: the per-item S->B span goes near zero on
> some items and the ratio explodes, which produced values of -1 to -4 on a quantity
> bounded near [0, 1].

The floor is applied to `frac`, which feeds `sb_frac_median`. The other aggregate Paper 1
reports, `sb_frac_of_means`, forms no per-item ratio and takes no floor.

**So Paper 1 did not exclude items from an analysis. It guarded one aggregation form, and
reported a second form that does not need the guard.**

`v2.0` section 3.2 imports it in exactly those terms: two aggregates are reported, the
median of per-item values and the value computed from the means, "following Paper 1's
handling of the same ratio pathology", and "the `ext_i >= 0.02` floor in section 6 is the
same guard, carried over".

### 2.1 Where the literal reading comes from

`v2.0` section 7.2's exclusion table says items with `ext_i < 0.02` are "excluded from the
confirmatory Arm B analysis". Read today that cuts `n`.

Read at `v2.0`, **the confirmatory Arm B analysis was the mean and median of per-item
`A`**, so section 7.2 and section 3.2 said the same thing. P2-D6 replaced the mean with a
sign test and P2-D12 fixed the three quantities. Section 7.2's wording stayed still while
the quantity it was written against moved out from under it.

---

## 3. The three claims, verified at P2-D20's unit

### 3.1 "(a) reads chosen options only." Verified

`src/c5_effect.py` contains no reference to `ext`, `item_axis`, `A[` or `marg_norm`.
`c5_movement` pivots `chosen_option` and compares option labels. **The same holds for
(b)**, which the instruction did not list and which is the same rate against `R_m`. In
`src/inertness_ceiling.py`, `A` enters at exactly one line, inside the (c) path. A test
asserts the absence, because a later edit could add an `A` term silently.

### 3.2 "(c) reads the sign of the margin difference." Verified, with the mechanism stated

The code does not literally read margins. (c) computes `sign(mean ΔA)` on `A`.

What makes the claim true of the **quantity** is that `ext_i` is a strictly positive
**per-item** constant. Both renderings of an item share one denominator, so

```
mean ΔA = (sum of that item's raw margin differences) / (2 * ext_i)
```

and the sign is the sign of the raw margin sum, which no positive denominator can change.

**The claim is true of the quantity and false of the expression**, and that difference is
the whole reason it had to be checked rather than trusted. Had `ext_i` been per rendering
rather than per item, the identity would fail at the item unit P2-D20 adopted, and the
earlier session's report was written before that unit existed.

### 3.3 "Ties in (c) use raw margins under P2-D19." Does not survive as stated

The zero test is `|mean ΔA| > EPS` on `A`, which is `ext_i`-scaled, not on raw margins.
The claim predates P2-D20 and is **false against the current code**.

**It does not change the conclusion, and the reason is measured rather than assumed.**

- `ext_i` lies in `(0, 0.5123]`, so dividing by it can only **magnify** `|ΔA|` relative to
  the raw margin difference, never shrink it. A genuine nonzero can therefore never be
  turned into a tie.
- The reverse risk is a sub-`EPS` float residue magnified past `EPS`. Worst-case
  amplification is `1 / 0.00134 = 746`. Observed raw-margin residues are of order
  `7.69e-17`, which magnified is about `5.7e-14`, still below `EPS = 1e-12`.
- Measured directly: the **smallest nonzero `|mean ΔA|` on the confirmatory set is
  0.0272**, which is `2.7e10` times `EPS`. Nothing sits near the boundary, so no `ext_i`
  in this set can move an item across it.

### 3.4 An open question from `v2.10` section 3.5, now answered

That section recorded an `A` versus `marg_norm` disagreement on `L3` under exact equality
and said whether `EPS` dissolves it was not computed.

At P2-D20's item unit there is **exactly one** item where `sign(mean ΔA)` and
`sign(mean Δmarg_norm)` differ, and it is that class: one side is exactly `0`, the other a
`7.69e-17` float residue. **Both are below `EPS`, so both classify as a tie** and (c) is
unaffected. Its `ext_i` is 0.0264, above the floor, so it is not an `ext_i` pathology
either. `EPS` dissolves it.

---

## 4. The ruling. **P2-D23**

> The `ext_i >= 0.02` floor is RETAINED and does NOT apply to Arm B's confirmatory
> set. The confirmatory `n` stays 108. The floor is Paper 1's, carried into `v2.0`
> section 3.2 as the guard on a MEAN OF PER-ITEM RATIOS: Paper 1's governing source is
> the comment beside `span > 0.02` in `src/frontier_position.py`, which scopes the
> pathology to exactly that form, and `v2.0` section 3.2 imports it in exactly those
> words. `v2.0` section 7.2 then wrote the exclusion against "the confirmatory Arm B
> analysis", which at `v2.0` WAS the mean and median of per-item `A`. P2-D6 replaced
> the mean with a sign test and P2-D12 fixed the three quantities, and none of the
> three has the ratio form the floor guards. (a) and (b) read chosen options only and
> never touch `A` or `ext_i`. (c) is a sign test, and `ext_i` is a strictly positive
> PER-ITEM constant, so both renderings of an item share it and
> `sign(mean ΔA) = sign(sum of raw margin differences)`, which no denominator can
> change. The floor therefore removes no item from the confirmatory set. It REMAINS IN
> FORCE, unamended, on every quantity that is a mean or median of per-item `A`, on
> `v2.0` section 4.3's `ΔA`-against-`ext_i` correlation, and on the `ΔA` null `v2.x`
> reported before P2-D6; all of those are reported rather than confirmatory. The floor
> is not withdrawn and its value is not changed: what is ruled is its reach.

**The floor does not reach any confirmatory quantity, so it removes no item. The
confirmatory `n` is 108.**

The instruction's stop condition did not fire: the floor does not bind on a confirmatory
quantity, so no remedy was reached for and none is proposed.

---

## 5. Where the floor remains in force, unamended

- Every quantity that is a **mean or median of per-item `A`**, which `v2.0` section 3.2
  still specifies as reported aggregates.
- `v2.0` section 4.3's **correlation between per-item `ΔA` and `ext_i`**.
- The **`ΔA` null** reported before P2-D6 replaced it.

All three are reported quantities. None is confirmatory. The floor is the right guard for
each, and Paper 1 measured the failure it guards against directly.

**The floor is not withdrawn and its value is not changed. What is ruled is its reach.**

---

## 6. Alternatives offered and not chosen

1. **Apply the floor to the confirmatory set as section 7.2 reads literally.** Rejected. It
   cuts `n` to protect a ratio form no confirmatory quantity has, on the axis the design is
   already shortest of. Section 7.2's sentence is not a separate decision from section
   3.2's; it is the same guard named where exclusions are tabulated, and 3.2 states what it
   guards.
2. **Withdraw the floor, since no confirmatory quantity needs it.** Rejected. The reported
   mean and median of per-item `A` still exist and still have the ratio form. Withdrawing a
   guard because the analysis moved away from the quantity it guards leaves it unguarded
   when a later section moves back.
3. **Lower the floor to a value the confirmatory set clears.** Rejected outright. It is
   choosing a threshold from the data it will be applied to, to reach a predetermined `n`.

---

## 7. What is bound

`p2_decisions.bind_ext_floor(min_ext_confirmatory, n_confirmatory,
quantities_reading_ext)` is called by `inertness_ceiling.main`.

Following the binding form recorded in `DECISIONS.md`, the check carries its reason rather
than a range. It does not assert that `ext_i` is large enough. It asserts that `ext_i` is
**strictly positive**, because that is the property the sign identity needs: at `ext_i = 0`
the sign is undefined rather than large, and the floor would reach (c) after all. **A small
`ext_i` is not the hazard; a zero one is.**

`quantities_reading_ext` must be empty. A run that adds an `A`-magnitude quantity to the
confirmatory family has changed what the floor reaches, and that surfaces there rather than
in a quietly reduced `n`.

`check_p1_ext_floor_source` asserts `span > 0.02` is still present in Paper 1's
`src/frontier_position.py`. Paper 1's decision log has no entry for this floor, so that
expression with its comment **is** the governing record, and this is the chain of custody
to it.

No artifact value changes in this version.

---

## 8. What this version changes

| | |
|---|---|
| the `ext_i >= 0.02` floor | **retained, unamended.** Its reach is ruled, not its value |
| Arm B's confirmatory `n` | **108**, unchanged |
| `v2.0` section 7.2's exclusion | superseded in its reach: it names the guard section 3.2 defines, and that guard is on a mean of per-item ratios |
| quantities the floor governs | mean and median of per-item `A`, section 4.3's correlation, the pre-P2-D6 `ΔA` null. All reported, none confirmatory |
| `v2.10` section 3.5's open `L3` question | answered: `EPS` dissolves it, both sides are below the tolerance |
| P2-D6, P2-D19, P2-D20 | untouched, not reopened |
| any `F1` or `F2` statistic | none computed in this version |
