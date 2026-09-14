# PREREGISTRATION v2.16

**Status.** New file per D148. `v2.0` through `v2.15` are not edited. This version rules
one question: what `A_null(m, F)` and `ΔA_null(m, F)` may be used for, ruled **before
either has been computed**.

**Decided by an agent session acting on an author instruction**, per the countermeasure in
`v2.10` section 2.4. The session is not the author. It wrote this document and **P2-D25**
from the instruction quoted in section 1.

**This session computed no statistic.** No `A_null`, no `ΔA_null`, no control-set `TV`, no
quantity on `data/raw_t7/`, no analysis script's `main()`. Section 6 discloses the one
thing it did read that was not already in a report, and why reading it was not computing a
statistic.

**Scope of the ruling.** It rules what the two quantities may be used for. It does NOT rule
P2-D5's blocker, which stays open and stays the author's, and section 5.5 shows the ruling
holds under all three readings of it. It does not move `p0`. It does not reopen P2-D6,
P2-D12, P2-D14, P2-D19, P2-D20, P2-D21, P2-D23 or P2-D24.

---

## 1. The instruction

Quoted in the parts that bear on the ruling.

> You rule. **You compute nothing.**
>
> You may and must **verify the record**: read `v2.0`'s formulas, confirm what each
> decision says, check whether a module exists, grep for whether a quantity was ever
> emitted. That is reading, and every claim in this prompt must be checked that way rather
> than trusted.
>
> **With no number on the table, what may the computed quantities be used for and what may
> they not?** At minimum, all four:
>
> 1. Whether `A_null` and `ΔA_null` **enter the confirmatory family or are descriptive**.
>    Note that the confirmatory family is 21 tests and `alpha = 0.05/21`; say what happens
>    to that family under your ruling and whether anything you authorize changes it.
> 2. Whether they **may be read against quantity (c) at all**, and if so **under what
>    preregistered mapping**, or whether **no mapping is authorized**.
> 3. What they **license about the generic-option-position-shift hypothesis** the (4,5)
>    signature favours. Be precise about what would and would not count as adjudicating
>    it, and about whether the control set can adjudicate it at all given that `A` is
>    undefined there.
> 4. Whether **a successor to section 4.4's cap is authorized**, or whether **the cap stays
>    orphaned and its absence stays the finding**.
>
> Consider explicitly, and rule on, the space between "confirmatory" and "useless": the
> control set has a preregistered purpose in `v2.0` section 4.4 that is independent of the
> cap, namely that movement on `beta_c = infinity` items is prompt sensitivity rather than
> adversary tracking. Whether that purpose survives P2-D6 and P2-D12 is part of what you
> rule.

and, on why the session ordering exists:

> A ruling made with the numbers visible is a different object from one made without, and
> the author split the sessions so that this one is made blind. If you find yourself
> wanting a number to decide, that wanting is the thing the split exists to prevent: rule
> on the structure, and say explicitly what you would have wanted and why you ruled without
> it.

**Constraints, all followed.** Do not reopen P2-D5, which is the author's and stays open,
and the ruling must work whichever way it is later ruled and say so explicitly. Do not move
`p0`. Do not reopen P2-D6, P2-D12, P2-D14, P2-D19, P2-D20, P2-D21 or P2-D24. Do not
overstate: if the ruling makes the computation nearly worthless, say that plainly; if it
leaves the hypothesis unadjudicable, say that. Treat every claim in the instruction as
unverified.

---

## 2. Every claim in the instruction, checked against the record

The instruction's own rule. Two of its claims do not survive, and the second is the reason
question 3 can be answered at all.

| carried | checked against | verdict |
|---|---|---|
| `v2.0` sections 3.3 and 4.4 specify `A_null(m, F)` and `ΔA_null(m, F)` | `v2.0` section 3.3's reference table, fourth row; section 4.4's "Attribution cap, preregistered" block | **holds**, verbatim |
| both formulas predate all Paper 2 data and neither has a free parameter | `v2.0` is the first Paper 2 preregistration; both formulas are closed forms over `p_{m,F}`, `p^ctrl` and frozen `A_i(o)` | **holds** |
| both are named required steps in `T7.md` | step 5 names "salience, marginal null, Bayes" explicitly; step 4 names the `beta_c = infinity` control and says it "caps how much of the divergence-set effect you can attribute", but names neither `ΔA_null` nor its formula | **holds of the steps; loose of `ΔA_null`**, whose formula lives only in `v2.0` section 4.4 |
| P2-D24 established that using either to license a direction claim on (c) would be post-hoc | P2-D24 decision text and `v2.15` section 4 | **holds**, verbatim |
| the cap is the second recorded instance of the scope-expiry failure | `DECISIONS.md`, the two instances recorded together | **holds** |
| neither of the cap's inputs has ever been computed | grep across `src/` and `results/`: the only "marginal" quantity is `c5_effect.tv_option_marginal`, a total variation between two option marginals; `t7_armb` emits it per cell on the **confirmatory** set; no module forms a control-set marginal, an `A_null` or a `ΔA_null`. `inertness_ceiling`'s and `detection_ceiling`'s `a_null_licenses` fields are about what a NULL RESULT licenses and are not `A_null` | **holds** |
| the (4,5) signature is recorded as suggestive evidence for a generic option-position-shift hypothesis | `reports/T7_switch_concentration.md`, "The (4,5) signature"; `DECISIONS.md`, same heading; P2-D24's "why it needed deciding" | **recorded as claimed** |
| ...and that hypothesis is what the signature favours | `chosen_option` is a canonical option id; `items_rendered.parquet` carries `option_order`, a per-item per-permutation permutation of canonical ids; canonical 4 and 5 occupy all six menu positions at near-uniform rates under both permutations | **fails**. See section 5.3 |
| local `main` should be at `e6620ff` | `git log --oneline -1 main` | **holds**; `HEAD` equals it and is an ancestor |

One further thing the record settles that the instruction did not raise. **`ΔA_null`'s
status is not an open question: P2-D23 already answered half of it.** P2-D23's decision
text puts the `ext_i >= 0.02` floor in force on "the `ΔA` null `v2.x` reported before
P2-D6" and adds "all of those are reported rather than confirmatory". `v2.14` section 5
lists the same three items under "Where the floor remains in force, unamended". There is
only one `ΔA` null in the record, so the referent is unambiguous. P2-D25 restates that
rather than deciding it fresh, and extends it to `A_null`, which P2-D23 does not name.

The tense in P2-D23's phrase, "reported before P2-D6 replaced it", is loose: the `ΔA` null
was never reported, because it was never computed. The referent survives the slip. P2-D23
is not edited.

---

## 3. What the two quantities are, structurally

Restated from `v2.0` without amendment, because the ruling turns on their form and not on
their values.

```
A_null(m, F)  = sum_o p_{m,F}(o) * A_i(o)                         v2.0 section 3.3
ΔA_null(m, F) = sum_o ( p_{m,F}^{ctrl}(o) - p_{m,F0}^{ctrl}(o) ) * mean_i A_i(o)
                                                                  v2.0 section 4.4
TV(m, F)      = 0.5 * sum_o | p_{m,F}^{ctrl}(o) - p_{m,F0}^{ctrl}(o) |
                                                                  v2.0 section 4.4
```

Four structural facts, each of which does work below.

1. **`p_{m,F}(o)` and `p^ctrl(o)` are marginals over CANONICAL option ids.** `v2.0` section
   3.3 says so in those words. They are not marginals over rendered menu positions, and no
   passage in any version specifies one.
2. **`A_null` and `ΔA_null` are LEVELS, in `A` units.** Quantity (c) is a sign proportion.
   Nothing in any version maps one onto the other.
3. **Both divide by `ext_i`,** through `A_i(o)`, so both carry the ratio form P2-D23's
   floor guards and P2-D6's mixture finding describes. `ΔA_null` carries it explicitly, in
   the `mean_i A_i(o)` its own formula names.
4. **`A` is undefined on the control set**, by `v2.0` section 3.2: `ext_i > 0` exactly on
   the divergence set. So the control set can carry a distributional quantity and cannot
   carry a displacement.

---

## 4. Question 1: confirmatory or descriptive

**Descriptive. The confirmatory family stays at 21 tests and `alpha = 0.05/21` is
unchanged. Nothing this version authorizes touches either.**

**Neither quantity was ever a test.** `v2.0` section 8.1 defines the family as seven models
by three framing contrasts and enumerates what is outside it. `A_null` appears in section
3.3's table of four REFERENCES, beside the Bayes oracle, the adversary oracle and salience,
none of which is a test. `ΔA_null` appears in section 4.4 as a second CONJUNCT on a
criterion: "requires **both** that the interval on mean `ΔA` excludes zero ... **and** that
the observed mean `ΔA` exceeds `ΔA_null(m, F)`". Section 10 lists the three contrasts
"subject to section 4.4's attribution cap", which is the grammar of a condition on a test,
not of a test. A conjunct spends no `alpha`; that is why `v2.0` could carry it with 21
tests and no correction for it.

**So there is no promotion available to decline and no demotion to perform.** The test the
cap conditioned was mean `ΔA`, and P2-D6 demoted that to descriptive. A condition on a
descriptive quantity is descriptive. That is the whole of the answer for `ΔA_null`, and
P2-D23 had already reached it: the `ΔA` null is on P2-D23's list of quantities the `ext_i`
floor still governs, and P2-D23 says of that list "all of those are reported rather than
confirmatory."

**`A_null` inherits the same status by the same route**, and it is worth saying why it is
not different. It is a reference point, references are not tests, and its only live
non-reference role is `v2.0` section 4.2's `F0` replication on "`post_norm` and on excess
over the marginal null", which section 8.1 explicitly excludes from the family: "The `F0`
replication check. A gate on artifact reuse (section 4.2), not a test."

**What admitting them would cost, which is why alternative 1 is rejected rather than merely
not preferred.** It would move `alpha` for 21 tests preregistered at `0.05/21`. That is
P2-D6's family and P2-D8's second family is corrected separately for exactly the reason
that a conjunction's error is bounded by the smaller of its parts. Re-correcting now would
change the threshold every published (c) cell was resolved against, after those cells are
published. No version authorizes that, and this one does not either.

**The `ext_i` floor rides along, and Session 2 must apply it.** P2-D23 leaves the
`ext_i >= 0.02` floor in force on every mean or median of per-item `A`. `A_null`'s two
aggregates under `v2.0` section 3.2 are exactly that, and `ΔA_null` is built from
`mean_i A_i(o)`. The floor applies to those aggregates, it removes items from the
descriptive figure, and the count it removes is reported. It does not touch the
confirmatory `n`, which stays 108 by P2-D23.

**One aggregation question, answered by a stated rule rather than by choosing.** `v2.0`
section 3.3's formula for `A_null` mixes an item-indexed `A_i(o)` with a model-level
`p_{m,F}(o)` and does not say where the aggregation over `i` happens. Section 3.2 does say,
for `A` generally: computed per rendering, averaged within item across the two
permutations, then aggregated across items, with **two** aggregates reported for every
cell, the median of per-item values and the value computed from the means. `A_null` is a
value on the `A` axis by section 3.3's own table header, so section 3.2's rule reaches it.
Both aggregates are emitted, so both readings of the formula are recoverable from the
artifact and neither is foreclosed here.

---

## 5. Question 2 and question 3: what may be read against what

### 5.1 No mapping onto quantity (c) is authorized, and none may be written

P2-D24 already rules the use post-hoc and this version does not reopen it. What this
version adds is the rule that follows from it and the reason a blind session cannot repair
it.

**The structural reason.** `A_null` and `ΔA_null` are levels in `A` units. Quantity (c) is
the proportion of items with `mean ΔA > 0` against `p0 = 0.5`. No passage in `v2.0` through
`v2.15` maps a level excess onto a proportion, and `v2.0` section 4's criterion did not
need one, because the quantity it conditioned was also a level.

**The reason the session split does not fix it, which is the part worth writing down.** The
obvious repair is that a session which has not seen `A_null` can write the mapping blind
and preregister it. It cannot. All fourteen of quantity (c)'s cells, their proportions,
their `p` values and their directions are published in
`reports/T7_armb_quantities.md` and were read by this session under instruction. A mapping
from a level to a sign proportion has two ends, and blindness on one end is not
preregistration. Any mapping written from here is written with (c) in view, whoever writes
it.

**What this costs, stated plainly.** For the direction question the computation is worth
close to nothing. `A_null` and `ΔA_null` will be emitted and will license no sentence about
any cell of (c). That is not an argument for withholding them, for the reasons in section
5.6, but it is what they buy there and it is not more.

### 5.2 What the two quantities do license

Three uses, all descriptive, none of which needs a mapping.

1. **Reference-set placement (`T7.md` step 5, `v2.0` section 3.3).** Where each model sits
   on the `A` axis relative to the Bayes oracle at 0, the adversary oracle at 1, salience,
   and `A_null`. T7's brief makes this the headline: "The point is where models sit on the
   interval, not whether they beat a baseline", and its anti-requirements say "If a model's
   behaviour is indistinguishable from the marginal null, say so plainly." That is a
   statement about POSITION under a framing. It is not a statement about movement, it is
   not a claim that a model carries adversary-relevant content, and P2-D5's first sentence
   already forbids reading raw `A` under a single framing as content. The permitted
   sentence is the flat one: model `m` under framing `F` sits at or away from what its own
   option marginal would produce on this item geometry.
2. **The `F0` replication gate (`v2.0` section 4.2).** Reported and not a test. Note what
   it will find: `results/T7_f0_replication.json` records zero disagreeing renderings
   between `F0` and Paper 1's `cond4` on all 3,500 confirmatory-tile renderings, so every
   function of chosen options agrees identically, `A_null` included. The gate is satisfied
   by construction on that tile and `A_null` adds no information to it. Recorded here so
   that it is not later presented as a check that passed on its own strength.
3. **Prompt sensitivity on the control set (`v2.0` section 4.4, first paragraph), via
   `TV(m, F)`.** Section 5.4.

### 5.3 The (4,5) signature is not evidence for a generic option-POSITION shift

This is the instruction's claim that fails verification, and it changes what question 3 can
be answered with.

**The observation is unchanged.** 54 of the 62 discarded switches fall on option-index pair
(4,5), 4 on (0,1), 3 on (3,4), 1 on (3,5).

**The index is canonical, not positional.** `t7_switch_concentration.cell` reads
`w[BASE]` and `w[arm]` from `tie_reference.pair_frame`, whose values are the
`chosen_option` column, and it uses them to index `A[i]`, the item's frozen per-option
geometry. So the pair (4,5) is a pair of canonical option ids.

**Canonical ids are not menu positions.** Paper 1's `items_rendered.parquet` carries
`option_order`, a permutation of canonical ids, different per item and per
`permutation_id`; `t7_render` renders the menu through it. On the `size` tile's 250 items,
canonical option 5 falls in menu positions 0 to 5 on counts of 41, 40, 40, 36, 45, 48 under
permutation 0 and 45, 48, 37, 43, 32, 45 under permutation 1; canonical option 4 gives 35,
49, 42, 47, 39, 38 and 41, 38, 41, 40, 49, 41. Both are spread across the whole menu, and
`option_order` on permutation 1 is not the reverse of permutation 0 on a single item.

**Therefore the inference does not follow.** A model nudged toward or away from the end of
the MENU moves between whatever canonical ids happen to sit in the last two menu slots, and
those differ item by item and permutation by permutation. Such a model would smear its
switches across canonical pairs. It would not concentrate 54 of 62 on canonical (4,5).

**What the signature is consistent with.** A shift in preference over canonical option
CONTENT at the ends of the tile's ordinal scale. On `size` the canonical list is grain of
sand, chicken egg, football, washing machine, taxi, aircraft carrier, so canonical (4,5) is
the two largest and (0,1) the two smallest. It is also, as
`reports/T7_switch_concentration.md` first recorded and P2-D19 section 3.8 measured, where
the `A`-tied pairs themselves sit, 67 of 84 on (4,5) and 15 on (0,1), which is a property
of the frozen geometry carrying no model in it. Both readings remain available and this
version distinguishes neither; what it rules out is the positional one.

**The consequence for the cap, which runs the opposite way from the record's expectation.**
`p^ctrl(o)` is a marginal over canonical option ids, so `ΔA_null` is shaped for exactly the
canonical-content hypothesis and is **matched** to it, not mismatched. What it cannot do is
reach quantity (c), and that is section 5.1's problem rather than a mismatch of object.

**And a menu-position hypothesis is unadjudicable for a second, independent reason.** No
preregistered quantity is a marginal over rendered positions. Building one now would be a
new preregistered quantity chosen after the signature was seen, which P2-D5 alternative 2
rejected in the same shape. It is declined. So that hypothesis is both unevidenced by the
signature and untestable by the design, and both halves are stated rather than one.

**What would and would not count as adjudicating the canonical-content hypothesis.** Would:
a preregistered rule that attributes a portion of the confirmatory movement to the
control-set option-frequency shift, applied to a quantity the confirmatory family contains.
The design has the first half and not the second. Would not: a large `TV(m, F)`, which shows
generic movement exists without sizing its share of the confirmatory movement; a large
`ΔA_null` read against a sign proportion, which is section 5.1; or the (4,5) concentration
itself, which predicts the same shape under a tie-geometry account that carries no model in
it.

### 5.4 The control set's independent purpose survives, intact and unamended

`v2.0` section 4.4's first paragraph states a purpose that is not the cap: the
adversary-robust items are the built-in control, `o*_0 = o*_infinity` there, nothing for an
adversary-aware model to move toward, and "Any change in the choice distribution on those
items is prompt sensitivity."

**It survives P2-D6 and P2-D12, and the reason is that neither reaches it.** P2-D6 replaced
mean `ΔA` with a sign test; `TV` is not a function of `ΔA`, of `A` or of `ext_i`. P2-D12
fixed three quantities on the confirmatory set; `TV` is on the control set and is not one of
them. The purpose was never scoped to a quantity either decision moved; it is scoped to the
control SET, whose defining property is `beta_c = infinity` on frozen item geometry, and no
Paper 2 decision has moved that. It was descriptive at `v2.0` and it is descriptive now,
because nothing promoted it and nothing demoted it. This is the one passage in the
neighbourhood whose scope did not expire, and saying so is part of the ruling: the second
recorded scope-expiry instance is the cap, and it is not the control set.

**What `TV(m, F)` can and cannot say.** It can establish that the framings move choices
where there is nothing adversary-relevant to move toward, which is prompt sensitivity
measured directly. It cannot size how much of the confirmatory movement that explains,
because sizing that is the reweighting step and the reweighting lands in `A` units at the
level. And `A` is undefined on the control set by `v2.0` section 3.2, so the control set
carries no displacement of its own to compare. **The control set can show that generic
movement exists. It cannot adjudicate whether the confirmatory movement is that movement.**

**The base.** The control set for `ΔA_null`'s reweighting is the `size` tile's 142
adversary-robust items. That is the base P2-D4's consequences name, and it is the only one
whose option arity matches the set being reweighted: the reweighting multiplies
`p^ctrl(o)` by `mean_i A_i(o)` over the 108 six-option confirmatory items, so the control
marginal must live on the same six-option support. P2-D3 rejected pooling for the adjacent
reason, that section 3.3's marginal null is over canonical option ids which do not pool
across `|O| in {3,3,4,6}`. `T7.md`'s SCOPE sentence names 540 non-divergent items; that
sentence is about how much inference to buy, not about the cap's base, and the two numbers
are both correct about different sets. The 540-item figure is reported beside the 142 with
its base named, never alone, which is P2-D19's discipline applied to a second pair of
bases.

### 5.5 The ruling holds whichever way P2-D5's blocker goes

P2-D5's second conjunct, "every such claim is made on a framing contrast and on excess over
the marginal null", is unruled and is the author's. Three readings are in circulation and
this version reaches none of them.

- **The conjunct travels and needs an operational form.** Then an excess quantity would
  have to enter the confirmatory family, and nothing here puts one there: `A_null` and
  `ΔA_null` are descriptive under section 4, and the excess `A_observed - A_null` they
  would form is descriptive with them.
- **It expired with the mean.** Then there is no conjunct to satisfy, and nothing here
  claims one is satisfied.
- **(a), (b) and (c) already satisfy it.** Then the conjunct is discharged by quantities
  this version does not touch, and nothing here is offered as discharging it.

Under all three, the two quantities stay descriptive, no mapping onto (c) exists, and no
successor cap is authorized. The blocker stays open and stays the author's.

### 5.6 The space between confirmatory and useless

Three things are true at once and none cancels the others.

1. For the direction question the computation is worth close to nothing. Said plainly in
   section 5.1.
2. The computation is still owed. Both formulas predate all Paper 2 data, neither has a
   free parameter, T7's brief names both steps, and section 4.2 requires the replication to
   be reported on excess over the marginal null. Declining unrun preregistered work because
   its licence turned out small converts a stated limitation into a silent one.
3. What it buys is reference-set placement, a prompt-sensitivity measurement on the control
   set, and a descriptive cap on a descriptive mean. Those are real and they are small, and
   the paper reports them at that size.

---

## 6. Question 4: no successor cap, and what that costs

**No successor is authorized, and the cap does not need one.**

**The framing that makes this simple.** The cap is often described as orphaned in the sense
that the object it capped no longer exists. That is not what happened. `v2.0` section 4.4's
cap conditions mean `ΔA`. P2-D6 **demoted** mean `ΔA` and did not delete it: its decision
text says "Mean `ΔA` is demoted to a reported descriptive quantity", and `v2.0` section
3.2's two aggregates are still required for every cell. So the cap's object still exists,
at descriptive standing, and the cap applies to it unchanged. **The cap followed its
quantity down. It did not lose it.**

What genuinely does not exist is a defence for quantity (c), and section 5.1 is why none can
be written now.

**The defect that must be reported with the cap rather than repaired.** `ΔA_null` is built
from `mean_i A_i(o)`, and P2-D6 measured what a mean of per-item `A` is: a three-way
mixture, 470 option-cells at exactly 0, 439 at exactly 1, 841 off-pole at median `-3.329`,
unbounded below. Both sides of the cap comparison are means over that geometry, so P2-D6's
finding reaches both and the comparison is weak on both ends. **It is not repaired here.**
Substituting a median, a bounded transform or a trimmed mean would be inventing the
successor this version declines, and each was rejected on its own grounds in P2-D6. The cap
is computed as specified, reported as descriptive, and reported with that defect named
beside it.

**The cost, stated rather than softened.** Arm B's confirmatory family carries no defence
against the hypothesis that the movement is a generic prompt-induced shift in option
preference. It cannot acquire one, because acquiring one means writing a level-to-sign
mapping with (c) published. So the design cannot adjudicate between that hypothesis and
adversary tracking on any confirmatory quantity, and **that inability is the finding**, in
the same words `reports/T7_switch_concentration.md` already uses. It is reported as a
property of the design and not as a caveat on a result.

**What is NOT lost, and the record should not overstate the loss either.** The cap is
computable, on the quantity it was written for, at that quantity's current standing. The
control-set purpose in section 4.4's first paragraph survives whole. The three confirmatory
quantities are unaffected. What is lost is a confirmatory conjunct that P2-D6 had already
removed the other half of.

---

## 7. Ordering, disclosed

**What this session knew when it ruled.** All fourteen cells of quantities (a), (b) and (c),
their intervals, `p` values and directions; the five resolving cells and their downward
sign; the switch-concentration table; the neutral-baseline diagnostic; P2-D24 and every
entry before it. All of that is in the documents the instruction required it to read in
full, and none of it is `A_null`, `ΔA_null` or a control-set `TV`.

**What it did not know, and the ruling therefore could not be fitted to.** Any value of
`A_null`, any value of `ΔA_null`, any control-set `TV`, and the size of any excess. The
ruling turns on the FORM of the quantities in every place it turns on anything: a reference
is not a test, a conjunct is not a test, a level is not a proportion, a canonical-id
marginal is not a position marginal, and a demoted quantity still has its conditions.

**The one thing read that was not already in a report, disclosed because it is load-bearing
on section 5.3.** The session read Paper 1's frozen `data/processed/items_rendered.parquet`
and `data/reference/tiles.json` to establish that `option_order` permutes the menu per item
and per permutation and that canonical options 4 and 5 are spread across all six menu
positions, and it counted that spread. That is a property of frozen, model-free item
geometry, computed before any Paper 2 model output is read, which is the same class as
P2-D19's tied-pair counts and P2-D23's `ext_i` range. It reads no model choice, no framing
contrast and no Arm B quantity. It is not one of the quantities the instruction forbids and
it is not on `data/raw_t7/`. It is disclosed anyway, because a session instructed to compute
nothing should say what it did compute and why that was not the thing.

**What this session wanted a number for.** Two places, both recorded in P2-D25. Whether the
cap comes out slack or binding against the descriptive mean, which would have made a
successor look unnecessary or urgent and is precisely the number the split forbids. And how
many `size`-tile adversary-robust items the `ext_i` floor reaches, which P2-D23 also
declined to compute and which changes a descriptive figure rather than its standing.

---

## 8. What is bound

`src/p2_decisions.py` gains `P2D25_TEXT`, `P2D25_REJECTED`, the constants the ruling needs,
and `bind_marginal_null_use`, which **Session 2 calls** before emitting either quantity.

Per the binding-form note in `DECISIONS.md`, it asserts the premises that make a use well
formed, not a range any value occupies. Every value below may move on a re-run without
touching the ruling; what the ruling rests on is six premises, and each assert fires when
one of them changes rather than when a number drifts.

| premise | assert | why, in the assert's own message |
|---|---|---|
| neither quantity is confirmatory | `in_confirmatory_family` is false and the family is 21 at `P2D6_ALPHA` | a conjunct and a reference are not tests; admitting one moves `alpha` for 21 published tests |
| no level-to-sign bridge | `mapping_to_quantity_c` is None | (c) is a proportion, both are levels, and any bridge is written with (c)'s cells published |
| no successor cap | `successor_cap` is None | the cap's object still exists at descriptive standing; a successor is a new quantity |
| the reweighting is defined | control arity equals confirmatory arity | `p^ctrl(o)` and `mean_i A_i(o)` must share an option-id support or the sum is not a sum over one index set |
| the hypothesis matches the support | `hypothesis_support` is `canonical_option_id` | a marginal over canonical ids cannot express a menu-position preference |
| the floor P2-D23 left in force is applied | `ext_floor_applied` is true | both quantities have the ratio form P2-D23 governs |

`tests/test_p2d25_marginal_null.py` fails if a caller crosses any of the six, and it
recomputes the menu-position spread of canonical options 4 and 5 from Paper 1's frozen
renderings rather than trusting the figures in section 5.3.

The scope registry's one unruled entry is **not cleared**. It covers the cap, `v2.0`
section 4's movement criterion and P2-D5's second conjunct; the conjunct is the author's, so
`scope_audit()` and `undefended()` keep returning it and the hypothesis keeps reading as
undefended, which is the true state. A `partly_ruled_by` field records which half P2-D25
answered.

---

## 9. What this version changes

- `docs/P2/DECISIONS.md` gains **P2-D25**, a dated correction to the "(4,5) signature" note
  that leaves the superseded reading legible, and five standing-check rows.
- `reports/T7_switch_concentration.md` gains a dated correction section on the same point.
  Its tables and every number in them are unchanged.
- `src/p2_decisions.py` gains the P2-D25 block and `bind_marginal_null_use`, and
  `check_log` covers P2-D25 in both loops.
- `tests/test_p2d25_marginal_null.py` is added.
- **No `results/*.json` value changes**, verified by hashing every file before and after.
  No superseded preregistration version is edited. No statistic is computed. `p0` is 0.5.
  The confirmatory family is 21 tests at `alpha = 0.05/21`.
