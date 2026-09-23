# Paper 2 decision log

Paper 1 binds an artifact to the decision that governs it (D100): the decision text
lives in `.claude/rules/30-data-decisions.md`, a verbatim constant lives in
`src/decisions.py`, and every script producing a derived artifact imports that
constant and asserts against it at import, so a drift fails before it can enter a
stimulus. Paper 2 had no equivalent. This file is the source; `src/p2_decisions.py`
is its binding module.

**Never edit an entry here to make a caller pass.** The entry is the source. If the
log and the code disagree, that is the bug this file exists to surface.

## ID scheme

`P2-D1`, `P2-D2`, and so on. The `P2-` prefix is deliberate: Paper 1's `D1` through
`D148` are frozen, and a Paper 2 entry numbered `D149` would read as their
continuation.

## The failure this file guards against

Twice in this project a plausible-looking artifact has been read in place of the one
that actually governs.

1. **The v2 posterior error.** `src/oracle.py` was read as the source of Paper 1's
   frozen posterior. It is a Task-11 diagnostic. The path that produced
   `items_final.parquet` is `src/score_items.py` to `grid_stats` to `src/tiebreak.py`.
   Reading the plausible module produced both a wrong posterior and a confident wrong
   explanation of it. Recorded in `CLAUDE.md`.
2. **T3's two author decisions.** Both were recorded, but only inside T3's own
   deliverables: `src/framings.py`'s docstring, `data/reference/framings_p2.json`,
   and `reports/T3_framings.md` section 7. T7 would have inherited them by reading a
   deliverable rather than a governing record. Nothing had gone wrong yet; the
   structure that lets it go wrong was in place.
3. **The manufactured rulings, 2026-09-12.** A parallel session answering the same
   author instruction that produced P2-D16 wrote two further entries, a floor rule and
   a tolerance rule, numbered `D17` and `D18`. Both were recorded as author rulings,
   and both carried premises attributed to the author that the author did not write.
   They are withdrawn as decisions; see the tombstones at P2-D17 and P2-D18. Nothing
   in the entries themselves distinguished them from P2-D16, which was written by an
   agent session from the same instruction, in the same format, on the same day.
   Substantively one of the two survives, as P2-D19, but it survives by being
   re-derived and re-scoped, not by being believed.

**The mechanism, which is the point of writing this down.** An artifact that looks
authoritative is cheaper to read than the record that is authoritative, and nothing
in the reading distinguishes them. Both cases were a correct-looking read of a file
whose standing was assumed rather than traced. Plausibility is not provenance, and an
agent working from a task list has no reason to check which it has, because the wrong
source answers the question just as fluently as the right one.

4. **The expired scope, 2026-09-13.** `v2.0` section 7.2 imported Paper 1's
   `ext_i >= 0.02` floor correctly and wrote the exclusion against "the confirmatory Arm
   B analysis". At `v2.0` that analysis WAS the mean and median of per-item `A`, so the
   sentence was exact. P2-D6 then replaced the mean with a sign test. **The import stayed
   correct and its scope silently expired.** Ruled, after the fact, by P2-D23. Harmless,
   and the second instance below was not.

**The fourth case is a different failure class from the first three, and the difference
is the point.** Cases 1 to 3 are all a wrong source: a plausible module read in place of
the governing one, a deliverable read in place of a record, an entry that was never a
decision. Case 4 has no wrong source anywhere. The citation was right. The reasoning was
right. The sentence was true when written and is still true of the thing it originally
described. What moved was the quantity underneath it.

So the two countermeasures below do not reach it. Provenance does not help, because the
provenance is clean. **Mechanical binding does not help either, and this is the sharp
part: the bound text is still true.** A binding asserts that a caller matches the decision
text, and here the caller matches and the decision text is accurate; what has gone wrong is
that the decision now governs nothing, and nothing in reading it says so. An expired scope
and a live one are textually identical.

`v2.4` is the proof that vigilance is not the answer. Section 3.1 caught one of these,
D74's SESOI on mean `ΔA`, and ruled it explicitly: "The SESOI does not translate, and none
is invented." The same version family left section 7.2's floor untouched. One session, one
document, two scopes attached to the same replaced quantity, one seen and one not.

5. **The orphaned attribution cap, 2026-09-14.** `v2.0` section 4.4 preregistered
   `ΔA_null(m, F)`, labelled in its own text "**Attribution cap, preregistered**", and
   stated what it was for in its own words: "Movement that a generic prompt-induced shift
   in option preference already explains is reported as prompt sensitivity and named as
   such." P2-D6 replaced the mean with a sign test, P2-D12 fixed three quantities, and
   **no successor to the cap was written.** Still unruled.

**The two instances, recorded together, because the difference between them is the
lesson.** Case 4 and case 5 are the same failure: a correct preregistration whose scope
expired when the quantity underneath it moved. They are not the same cost.

The `ext_i` floor's expiry was **harmless**. It guarded a mean of per-item ratios, the
analysis moved to a sign test, and P2-D23 found that the floor reached nothing and
removed no item. Confirmatory `n` stayed 108. Had nobody noticed, nothing would have been
wrong.

The cap's expiry **removed the design's only preregistered defence against the hypothesis
the data now points at**. Neither of its inputs exists: `TV(m, F)` on the
`beta_c = infinity` control set is T7 step 4 and has not been run, and `ΔA_null(m, F)` has
never been computed at the time this was recorded; both were computed on 2026-09-15 by
`src/t7_control.py` under P2-D25, descriptively, which is the outcome P2-D25 authorized. It
went unnoticed through P2-D6, P2-D12, P2-D19, P2-D20, P2-D21 and
T7's confirmatory run, and surfaced only when three independent inputs converged on its
absence: P2-D5's blocker naming a quantity that does not exist, the neutral baseline
departing downward too, and the discarded-switch geometry carrying the signature the cap
was written to rule out. P2-D24 rules the direction claim out on all three.

**Did the standing check added for case 4 catch case 5? Partly, and the part it missed is
the part that mattered.**

It **did** list the passage. On its first run the registry returned exactly one unruled
entry and that entry was this one. So the enumeration worked.

Two things it did not do.

1. **It could not have caught it earlier.** The registry was added on 2026-09-14, in the
   same session that recorded case 4. P2-D6, P2-D12, P2-D19, P2-D20, P2-D21 and T7 all
   predate it. A retrofitted check cannot catch what expired before it existed, and the
   six decisions that passed over the cap passed over it with no check in place.
2. **It recorded what the passage was scoped to and not what it was for.** The entry named
   `ΔA_null(m, F)` as the object and P2-D6 as the owner, and it read as a sentence needing
   a ruling. Nothing in it said the sentence was a **defence**, so the cost was invisible
   in the record even after the enumeration had succeeded. A reader of that entry learned
   that Arm B's licensing was unsettled. They did not learn that a hypothesis had been left
   undefended.

**The check that would have.** The registry carries a `defends_against` field as of this
entry, and `p2_decisions.undefended()` returns the unruled scopes that are defences.
An expired convention needs a ruling; an expired defence leaves a hypothesis the design can
no longer rule out, and the design stops being able to while nothing in the reading says
so. Separating them is cheap and it is the whole content of the second instance. It does
not retroactively help: the check still has to exist before the quantity moves, which is
the first point above and is not fixable by a better field.

**The countermeasure: a decision that scopes itself to another decision's quantity names
that decision.** Then superseding a quantity is not a local act. It surfaces every
dependent scope, because the dependents are enumerable rather than discoverable. A scope
that cannot name the decision owning its quantity is a scope nobody can audit when that
quantity moves.

This is maintained as a registry in `src/p2_decisions.py`, `SCOPE_REGISTRY`, with
`scope_audit()` listing every preregistration passage scoped to a quantity a later decision
replaced, and whether each has been ruled. It is a standing check because an entry arriving
there is not an error to fix; it is a question to answer, and the failure mode is that
nobody notices there is one.

### What the registry surfaced on its first run

**`v2.0` section 4's confirmatory movement criterion, and P2-D5's second conjunct. Not
ruled.**

`v2.0` section 4 required **both** that the interval on mean `ΔA` exclude zero and that the
observed mean `ΔA` exceed `ΔA_null(m, F)`, the marginal null of section 3.3. P2-D6 demoted
mean `ΔA` to descriptive, which retires the first conjunct. P2-D6 does not name the second,
and P2-D12's three quantities contain no excess-over-the-marginal-null quantity.

P2-D5 is adopted and binds it independently: "Every such claim is made on a framing
contrast **and on excess over the marginal null**, never on raw `A`." That is a live
constraint on exactly the claim Arm B exists to make, and the quantity it names is not
among the three P2-D12 fixed.

**This entry does not rule it.** The reading could be that P2-D5's conjunct travels to the
new quantities and needs an operational form, or that it expired with the mean the way the
floor's scope did, or that (a), (b) and (c) already satisfy it because a framing contrast
against a same-option baseline is an excess. Those are different decisions with different
consequences for what Arm B may claim, and choosing among them here would be resolving an
ambiguity by choosing. It is recorded, it is flagged to the session that opens Arm B, and
it is the author's.

### A second open question, recorded 2026-09-14 and not resolved

Not a scope expiry, so not a registry entry, but it travels with the blocker above because
it constrains the same verdict.

**The direction finding, recorded plainly.** T7's confirmatory run
(`results/T7_armb_quantities.json`) resolves quantity (c) against `p0 = 0.5` at the
corrected `alpha` on five cells: `CTRL`/F1, `L3`/F1, `L4`/F1, `L3`/F2, `L4`/F2. **All five
depart downward.** Under `p0 = 0.5` a downward departure is movement away from
`o*_infinity`, which is Paper 1's salience pole on **all 108** confirmatory items (P2-D26;
452 of 460 is the divergence-set figure and understates this set). Quantity (a)
clears P2-D13's floor on all 14 cells, 30 to 77 items moved of 108.

So: **the framings move choices substantially, and the resolving movement runs away from
the adversary-aware optimum.** That is neither H-B's predicted null nor adversary tracking.
It is recorded as the measurement it is.

**What it cannot yet be read as, and why that is a ruling rather than a caveat.** The `c5`
neutral baseline also departs downward where it resolves: `CTRL` 0.1951 and `L3` 0.2424 at
P2-D20's item unit (P2-D21). A downward departure may therefore be a property of inserted
text rather than of adversary content, and the F1 and F2 proportions need reading against
those per-model neutral figures and not only against 0.5.

Reading them against the neutral baseline is **a substantive ruling, not a restatement**.
P2-D6 fixed `p0 = 0.5`; P2-D12 and P2-D14 both rejected moving it, and P2-D21 retained it
while withdrawing the claim that made it look conservative. A comparison against the
measured neutral figure is the recalibration those entries declined, performed in the
reporting rather than in the null. Whether that is admissible, and if so whether it is
descriptive or confirmatory, is unsettled.

**It is not resolved here and it goes with the P2-D5 blocker**, because both bear on the
same verdict and ruling one without the other would license a claim the other forbids.
`reports/T7_switch_concentration.md` adds a third input to the same verdict: the `A`
coordinate's blind spot is concentrated on `CTRL`, `L1` and `L3` at 1.8 to 5.1 times
P2-D19's per-pair bound, and two of the five resolving cells sit in that group.

### Ruled 2026-09-14 by P2-D24, with three corrections to the note above

**The second open question is closed and the P2-D5 blocker is not.** P2-D24 rules that the
five departures license no claim about direction, under every one of the three readings of
the blocker, so the blocker stays open and stays the author's. Reading the F1 and F2
proportions against the measured neutral figure is rejected, not deferred. What the note
above got right is that the two questions travel together; what it assumed is that ruling
them required ruling the blocker first, and it does not, because inputs 2 and 3 are
independent of how the blocker goes.

**Three numbers in the note do not survive recomputation.** They are corrected here and
not edited above, so the record of what was believed on 2026-09-14 stays readable.

1. **`L3` does not resolve on the `c5` diagnostic.** `results/T5_inertness_ceiling.json`
   gives `L3` a two-sided `p` of 0.004551 at the item unit against `alpha` = 0.002381, and
   `significant_at_corrected_alpha_item` is false. P2-D21's adopted decision text already
   says "only `CTRL` resolves at the corrected `alpha` and it resolves downward". The
   sentence above should read `CTRL` 0.1951 and nothing else. The error propagated into the
   author instruction that produced P2-D24 and was caught by recomputation, which is the
   pattern `v2.10` section 3.6 records.
2. **"The framings move choices substantially" overstates what quantity (b) resolves.**
   (b) resolves on 3 of 14 cells, `L3`/F1 at -0.1065, `B2`/F2 at -0.1481 and `L3`/F2 at
   -0.1620, all in the direction of the framing moving choices more than `c5` does. On the
   other eleven the comparison does not resolve. The licensed sentence names the three and
   the eleven; "substantially" reports them as one thing.
3. **Three of the five resolving cells sit in the concentrated group, not two, and the
   ratio on them is 1.81 to 4.09.** The three are `CTRL`/F1 at 4.09, `L3`/F1 at 2.50 and
   `L3`/F2 at 1.81. "1.8 to 5.1" is the range over all six concentrated cells, and 5.10 is
   `CTRL`/F2, which does not resolve.

### The (4,5) signature, recorded 2026-09-14 as evidence

Recorded here because it is the third of the three inputs P2-D24 rules on, and because it
is what turned the orphaned cap from a licensing question into a cost.

Of the 62 switches the `A` coordinate discards on the confirmatory set, **54 sit on option
pair (4,5)**, with 4 on (0,1), 3 on (3,4) and 1 on (3,5)
(`results/T7_switch_concentration.json`). Option 5 is the end of the option order on a
six-option tile.

`reports/T7_switch_concentration.md` first recorded this as structure inherited from
P2-D19 section 3.8, cause unestablished. That is true and it is not the whole of it.
**A generic shift in option POSITION preference would leave exactly this signature**: a
model nudged toward or away from the end of the menu moves between the last two options,
and those are the options `A` cannot tell apart.

That hypothesis is the one `v2.0` section 4.4's attribution cap was preregistered against,
and the cap has no successor. So the observation is **suggestive evidence for the
alternative explanation and is uncomputable against the preregistered defence**. Neither of
the cap's inputs exists.

**Recorded, not tested.** No successor cap is computed, the hypothesis is not tested, and
the signature is not offered as establishing anything: a generic position shift predicts
it, other things would too, and distinguishing them is what the cap was for. **The design
cannot currently adjudicate it, and that inability is the finding.**

**Corrected 2026-09-14 by P2-D25. The observation stands; the hypothesis it was said to
favour does not.** The paragraphs above are left unedited, per the rule at the head of
this file, so the reading held on 2026-09-14 stays legible.

`chosen_option` is a CANONICAL option id, not a menu position. Paper 1's Format V permutes
the menu per item and per permutation, and on the `size` tile canonical options 4 and 5
occupy all six menu positions at near-uniform rates under both permutations
(`items_rendered.parquet`, `option_order`). So "option 5 is the end of the option order"
is true of the item's canonical option list and false of the menu the model reads, and a
model nudged toward or away from the end of the MENU would not concentrate its switches on
canonical pair (4,5); it would smear them across canonical pairs. The generic
option-POSITION hypothesis is therefore not what this signature favours, and no quantity in
the design is a marginal over rendered positions, so that hypothesis is unevidenced here
and remains unadjudicable for a second and independent reason.

What the signature is consistent with is a shift in preference over canonical option
CONTENT at the ends of the tile's ordinal scale: on `size`, canonical 0 and 1 are the grain
of sand and the chicken egg and canonical 4 and 5 are the taxi and the aircraft carrier.
That hypothesis IS the one `v2.0` section 4.4's cap is shaped for, because `p^ctrl(o)` is a
marginal over canonical option ids, so the cap is matched to it rather than mismatched. It
still cannot reach quantity (c), for the reasons P2-D24 gives and P2-D25 restates, so the
inability recorded above is unchanged in substance and changed in its reason.

P2-D24 is untouched. Its third premise is that nothing establishes the discarded switches
carry the direction of the retained ones, which is a statement about selection and does not
depend on what the concentration is a signature of.

The third case is the same failure class pointed at the log itself. A decision entry
is the governing record, so nothing downstream of it checks its provenance; the entry
IS the check. That makes a fabricated entry cheaper to write than a real one and
indistinguishable from it on reading, which is the mechanism above with the artifact
and the record swapped.

The countermeasure is not vigilance. It is two things.

1. **The governing record and the artifact are bound mechanically**, so a mismatch
   fails at import rather than being noticed. That is what D100 does for Paper 1 and
   what `src/p2_decisions.py` does here. It catches drift between a decision and its
   callers. It cannot catch an entry that was never a decision, because such an entry
   binds its callers perfectly.
2. **A decision entry names the instruction it acted on.** Every entry states who
   decided, in what session, and, where a session wrote the entry rather than the
   author, what instruction it was acting on and in what words. **An entry that cannot
   cite one is not a decision.** It is a proposal, and it is either put to the author
   or withdrawn. This is what the `Decided:` line is for and why P2-D16's was corrected
   rather than left standing: "by the author" and "by a session acting on an author
   instruction" are different provenances, and only the second can be audited by
   asking what the instruction said.

## The binding working, with a date on it

The countermeasures above are easier to state than to show working. One instance is
worth recording, because it is the only place so far where a binding caught something
no one's reasoning did.

`src/armb_floor.py` carried, from the session that wrote P2-D14 and long before
P2-D20 changed quantity (c)'s unit:

```python
g = type_ii_gap()
assert all(v["gap_to_p0"] >= 0 for v in g.values()), \
    "a neutral baseline sits above p0 = 0.5; the Type II statement reverses"
```

When P2-D20 moved (c) to the item unit, `B2`'s neutral baseline crossed `p0` and its
gap went to `-0.0556`. **That assertion had already named the consequence**: not that a
number would be out of range, but that the Type II statement reverses, which is what
P2-D21 then had to work out and record as a Type I exposure P2-D14's licence box has no
sentence for. Nobody re-derived it. The assert had it written down, with its reason,
before the event.

**The general form, which is the part worth carrying forward.** An assertion that
encodes WHY a quantity has the sign or shape it does is worth more than one that checks
a value. A value check tells a later session that something moved. A reason check tells
it what breaks, and it survives the change of unit, tolerance or estimator that makes
the value check stale. `gap_to_p0 >= 0` is a range check; the message attached to it is
the decision's mechanism, and the message is what did the work.

Written this way, a binding is not only a tripwire against drift. It is the place a
decision's reasoning goes so that the reasoning, and not just the number, is what a
later session collides with. Prefer that form wherever a quantity's sign, direction or
ordering carries an argument.

**The same lesson, reached independently and stated as a rule.** `bind_ext_floor`, written
for P2-D23 before this note existed, asserts that `ext_i` is **strictly positive**. It does
not assert that `ext_i` clears the 0.02 floor, and it does not assert a range at all. The
reason is the same shape as the one above: at `ext_i = 0` the identity
`sign(mean ΔA) = sign(sum of raw margin differences)` fails and the sign is **undefined
rather than large**, so a small `ext_i` was never the hazard and a range check would have
been guarding the wrong thing.

Two bindings, written months apart by different sessions for unrelated quantities, both
landed on it. The rule:

> **Assert the premise that makes a quantity well defined, not a range the quantity happens
> to occupy.**

A premise assert survives a change of unit, tolerance or estimator, because the premise is
what the argument needs and the argument is what a later session has to preserve. A range
assert goes stale with the unit, and worse, it keeps passing while the argument it was
standing in for stops holding. `gap_to_p0 >= 0` passed for every version in which the pair
unit was current; it fired the moment the unit changed, and its message, not its bound, is
what said why.

## Why the binding module is not called `decisions.py`

Paper 1's frozen `decisions.py` is imported by bare name from Paper 1's `src/`, which
`src/p1.py` puts on `sys.path`. A Paper 2 file of the same name shadows it whenever
it precedes Paper 1's entry on the path, which is the case for any Paper 2 module
that imports `decisions` before `p1` has run.

Measured on 2026-09-09: a decoy `src/decisions.py` placed in this repository was
returned to a Paper 2 caller in place of Paper 1's, carrying a drifted
`D64_COND5_INSERT` and an `assert_verbatim` that did nothing. Both of Paper 1's
tripwires were silently disabled, and the import raised nothing.

Giving Paper 2's binding module the same name as the file it exists to imitate would
be the failure above, committed inside the guard against it. The name differs so the
shadow cannot exist.

---

## P2-D1. `F0` is Paper 1's `base` variant only; `c5` is not carried into Paper 2

**Status:** adopted.
**Decided:** 2026-09-09, by the author, by interactive selection during the T3
session. Not an agent resolution of an ambiguity: T3 stopped before writing any
framing text and put the choice to the author with the alternatives below.
**Binds:** `src/framings.py`. **Constant:** `P2D1_TEXT`, `P2D1_VARIANT`.

**Decision text.**

> `F0` is Paper 1's Format V `base` rendering only. Paper 1's `c5` variant, the D64
> condition-5 insert, is not carried into Paper 2. A Paper 2 rendering is
> (item x permutation x framing) and not x variant. `F0`'s replication target is
> Paper 1's condition 4.

**Why it needed deciding.** Paper 1 renders eight renderings per item: two formats by
two permutations by two variants, `base` (condition 4) and `c5` (condition 5, the D64
insert). Paper 2 retires format L (D103), which leaves two permutations by two
variants. No Paper 2 document resolves the variant. `PREREGISTRATION_v2.md` section 2
names Format V, D101 and D103, and "two option-order permutations per item", and
never names the variant; section 5's covariate table lists permutation and not
variant; section 7.2's exclusions name Format only. `v2.1`, `T3.md` and `T7.md` are
all silent. So the variant axis was neither carried forward nor retired, and Paper 1
scored both conditions.

**Alternatives offered and not chosen.**

1. **Cross variant by framing.** `{base, c5}` by `{F0, F1, F2}`, twelve renderings
   per item. Would have kept both Paper 1 conditions live and given a within-Paper 2
   calibration for "one extra sentence in that slot" through the `c5` contrast, which
   is the cleanest available defence against section 4.5 cell 4's length and register
   artifact. Cost: doubles T7 inference, and makes variant a reported factor the
   preregistration does not name.
2. **`c5` as the `F0` base.** `F0` is Paper 1's `c5` rendering and `F1`/`F2` build on
   it. The argument was that `c5` already tells the chooser to consider every
   pairing, making it the tighter no-adversary control. Cost: it occupies the
   `{extra}` slot, forcing the adversary text elsewhere, and it moves the `F0`
   replication target to condition 5.

Both are recorded because a decision record that keeps only the chosen option cannot
be audited. A reader who disagrees needs to see what was on the table, and a later
session that wants to reopen this needs to know the alternatives were considered
rather than missed.

**Consequences.** A Paper 2 rendering is (item x permutation x framing): two
permutations by three framings, six per item. The `F0` replication check in
`PREREGISTRATION_v2.md` section 4.2 targets Paper 1's condition 4. T7's inference
budget is six renderings per item, not twelve.

---

## P2-D2. The framing block goes in Paper 1's `{extra}` slot

**Status:** adopted.
**Decided:** 2026-09-09, by the author, by interactive selection during the T3
session, alongside P2-D1.
**Binds:** `src/framings.py`. **Constant:** `P2D2_TEXT`, `P2D2_SLOT_ANCHOR`.

**Decision text.**

> The `F1` and `F2` framing block goes in Paper 1's `{extra}` slot, after the option
> menu and immediately before `Which do you send?`. That is the position D64's
> condition-5 insert occupies, and D104's PMI neutral prompt already excludes the
> slot, so the scoring normalisation is identical under `F0`, `F1` and `F2`.

**Why it needed deciding.** `F0` is byte-identical to Paper 1, so `F1` and `F2` can
only add text, but nothing fixes where. The choice changes what the model reads
before it reaches the option menu, and two sessions would not choose alike.

**Alternative offered and not chosen.**

1. **After the audience paragraph, before the menu.** The adversary is a property of
   the audience, so it would be described where the audience is described, and the
   framing would land before the model sees the options. Cost: no Paper 1 precedent
   for inserting there, and it separates the two audience facts from the menu by a
   paragraph.

**Consequences.** D104's neutral prompt is built from the menu and the question only.
Paper 1 deliberately held the condition-5 insert outside it, so a block in the same
slot is outside it too and the PMI denominator is identical across the three
framings. Verified in `reports/T3_framings.md` section 6.

---

## P2-D3. Arm B's unit of analysis is per tile, `size` confirmatory

**Status:** adopted.
**Decided:** 2026-09-09, during the T5 session, resolving the handoff in
`PREREGISTRATION_v2.2.md` section 4. Full reasoning in `PREREGISTRATION_v2.3.md`
section 1.
**Binds:** any Arm B analysis script. **Constant:** `P2D3_TEXT`, `P2D3_TILE`.

**Decision text.**

> Arm B's confirmatory analysis is per tile, on the `size` tile alone. Pooling across
> tiles with tile as a stratum is rejected. This preserves `PREREGISTRATION_v2.md`
> section 2 unchanged: the confirmatory set is `size`-tile items with finite
> `beta_c`, and `manmade`, `moves` and `hold` stay secondary.

**Why it needed deciding.** T2's counts showed the frozen set carries 460 finite-`beta_c`
items pooled against 108 on `size`, so a pooled primary would have quadrupled the
confirmatory `n`. Nothing in the preregistration settled whether the unit of analysis
was per-tile or pooled, and the counts made the question live.

**Alternatives offered and not chosen.**

1. **Pooled across tiles with tile as a stratum.** Would have taken `n` from 108 to
   460, covering `sigma <= 0.276` rather than `sigma <= 0.134`. Rejected for three
   independent reasons: P1's D108 measured that `moves` sits below its own marginal
   null at all four rungs and `hold` carries approximately nothing, so pooling asserts
   what D108 denies; under that prior pooling *loses* power, short by `1/f = 4.26x` at
   the point where `size`-only is exactly powered, because the diluted effect grows the
   requirement by `1/f^2` against a supply growing by `1/f`; and section 3.3's marginal
   null is over canonical option ids, which do not pool across `|O| in {3,3,4,6}`.

**Consequences.** The confirmatory `n` is 108, covering `sigma <= 0.134`, and the
shortfall against section 8.2's 400 is a stated limitation rather than a repaired one.
The `|O| = 6` single-arity property of the confirmatory set is preserved, so the
marginal null stays a single six-vector. The disclosure paragraph from
`PREREGISTRATION_v2.2.md` section 4 is carried verbatim into `v2.3` section 1.3,
including its final sentence, which the decision made counterfactual: the pooled option
was known to clear the target at the moment it was declined.

---

## P2-D4. Arm B's confirmatory item set is Paper 1's frozen 1,000

**Status:** adopted, with one part explicitly left open.
**Decided:** 2026-09-09, during the T5 session. Full reasoning in
`PREREGISTRATION_v2.3.md` section 3.
**Binds:** any Arm B analysis script. **Constant:** `P2D4_TEXT`, `P2D4_ITEMS_SHA256`.

**Decision text.**

> Arm B's confirmatory analysis set is the `size` tile of Paper 1's frozen
> `items_final.parquet`, restricted to items with finite `beta_c`: 108 items. No new
> item draw is authorized. Redraw variant (a), uniform enlargement of all four tiles,
> is rejected outright. Redraw variant (b), enlarging the `size` tile only, is neither
> adopted nor rejected: its size depends on `sigma` for `ΔA`, which is unmeasured.

**Why it needed deciding.** K2 fired, so D2's `beta_c`-stratified redraw does not
happen and the fallback was reuse of the frozen set. T2's projection then split the
redraw path into a uniform variant and an unequal-`N` variant, and
`PREREGISTRATION_v2.2.md` section 4 did not distinguish them.

**Alternatives offered and not chosen.**

1. **Redraw variant (a), uniform ~871 per tile, 3,487 total.** Rejected outright, and
   without needing `sigma`: under a `size`-only confirmatory set it buys nothing
   confirmatory that a `size`-only enlargement would not, while adding 2,561 items on
   the three tiles D108 identifies as carrying approximately nothing. It is dominated
   by variant (b). Two further costs recorded: `manmade` would sit at 69% of its
   qualifying conflict items, 79% at the interval's upper end, so its estimate would be
   near a population value while the others remain samples; and P1's equal-count
   within-conflict `fit_cost` deciles are what keep it fillable.
2. **Redraw variant (b), enlarging `size` only.** The correct shape for a redraw under
   this unit of analysis, and not chosen only because its size cannot be fixed without
   `sigma`. Left open rather than rejected.

**Consequences.** No new artifact, manifest, gate or hash is created, and the Paper 1
comparison is on identical items rather than on a comparable draw. `n = 108` against
section 8.2's 400. The `beta_c = infinity` control set is the same tile's remaining 142
items. An enlargement under Paper 1's recipe would be a superset in distribution rather
than a replacement, so adopting the frozen set now forecloses nothing.

---

## P2-D5. The `A` level confound is handled in interpretation, not in the item set

**Status:** adopted. **The blocker this entry raised is discharged by P2-D26 (2026-09-15),
structurally and not pending measurement.** This entry's text is unchanged and its
"452 of 460" is correct about the divergence set it describes. On the `size` confirmatory
set the figure is **108 of 108**, and that is the one that governs Arm B; see P2-D26.
**Decided:** 2026-09-10, during the T5 session. Full reasoning in
`PREREGISTRATION_v2.4.md` section 1.
**Binds:** any Arm B analysis or reporting script. **Constant:** `P2D5_TEXT`.

**Decision text.**

> `o*_infinity` is Paper 1's `o_fit` on 452 of 460 divergent items, so Arm B's target
> sits on Paper 1's salience pole and the LEVEL of `A` is confounded with salience.
> The confound is real, permanent, and not repaired by any item set. No change is made
> to the item set, the coordinate, or the analysis set. Instead: no claim that a model
> carries adversary-relevant content may rest on `A` under a single framing. Every such
> claim is made on a framing contrast and on excess over the marginal null, never on
> raw `A`. A model at `A = 1` under F0 is reporting salience, not adversary awareness,
> and a point mass at `A = 0` is likewise not evidence of Bayes-optimal behaviour.

**Why it needed deciding.** T6 measured the coincidence and asked whether models
already sit at or past `A = 1` under F0, which would let H-B's null be confirmed by a
ceiling. Measured: they do not. `A >= 1` on 0.0174 to 0.1870 across the ladder, median
`A` at or below zero for all seven, median headroom 1.0 to 1.9.

**Alternatives offered and not chosen.**

1. **Restrict the primary analysis to items with F0 headroom.** Rejected. `ΔA` is
   `A(F1) - A(F0)`, so F0 headroom is a function of one term of the outcome, and
   conditioning the analysis set on it is selection on the dependent variable in the
   form `PREREGISTRATION_v2.2.md` section 1.3 prohibits. Also unnecessary: the
   condition it protects against is measured absent.
2. **Add a second coordinate not confounded with salience at the level.** Rejected. It
   would be a new preregistered quantity chosen after F0 positions were seen, a
   researcher degree of freedom with none of the prior provenance the existing
   coordinate has from P1's D47.

**Consequences.** The design is unchanged and the limitation is stated rather than
engineered around: Arm B can establish whether the framing moves a model along Paper
1's frontier, and cannot establish whether a model's position on that axis reflects
adversary reasoning rather than salience. That is a property of the signal space, and
no enlargement fixes it.

---

## P2-D6. Arm B's confirmatory statistic is a tie rate plus a sign test, not mean `ΔA`

**Status:** adopted.
**Decided:** 2026-09-10, during the T5 session. Full reasoning in
`PREREGISTRATION_v2.4.md` section 2.
**Binds:** any Arm B confirmatory analysis script, and `src/sign_power.py`.
**Constant:** `P2D6_TEXT`, `P2D6_ALPHA`, `P2D6_P0`.

**Decision text.**

> Arm B's confirmatory instrument is (i) the tie rate, the share of analysis-set items
> with `ΔA` exactly zero, reported directly as a primary quantity, and (ii) an exact
> two-sided sign test on the remaining items, on the count with `ΔA > 0` against
> `p0 = 0.5`, at `alpha = 0.05/21`. Mean `ΔA` is demoted to a reported descriptive
> quantity. The median of per-item `ΔA` and the value computed from the means are both
> retained. The `size`-tile analysis set, the 21-test family and `alpha` are unchanged.

**Why it needed deciding.** `A` is near-trichotomous: 470 option-cells at Paper 1's
Bayes pole (`sb = 1`, where `A`'s median is 0), 439 at its salience pole (`sb = 0`,
where `A`'s median is 1), and 841 off-pole at median `-3.329`, unbounded below because
`A` divides by `ext_i`. Off-pole is the common case, not a tail.

*Corrected 2026-09-22, words only, nothing recomputed (`PREREGISTRATION_v2.22.md`
section 5).* This sentence first read "470 option-cells at exactly 0, 439 at exactly 1".
The three counts are the split by Paper 1's `sb` poles
(`results/T6_F0_headroom.json:coordinate_geometry.n_option_cells_by_p1_pole`), not by
`A`'s value; split by `A` itself they are 464, 439 and 847
(`results/T6_F0_headroom.json:coordinate_geometry.n_option_cells_by_A_value`). The
near-trichotomy the decision rests on holds under both, so the decision does not move. Over the 6,048 admissible
ordered option pairs, 0.7004 exceed the target move of `ΔA = +1` in magnitude and
0.1518 exceed it tenfold, so one item moving to a far off-pole option outweighs ten
items making the exact move Arm B exists to detect. H-B predicts a null, so a
heavy-tailed estimator could satisfy it by widening the interval rather than by the
models.

**Alternatives offered and not chosen.**

1. **Accept the mean, state the mixture as a limitation.** Rejected as contradicted,
   not merely disfavoured. A limitation is the right instrument when an estimator is
   unbiased but noisy or occasionally distorted by a tail. Neither holds: the
   distortion is typical, and a three-way mixture with unbounded components means the
   mean's expectation is a different quantity, not the effect plus noise.
2. **Restrict to pole-to-pole transitions.** Rejected. It discards 0.8479 of
   admissible moves and needs a new rule for what a pole/off-pole move counts as,
   fixed after the geometry was seen. The sign is interpretable on every move,
   including off-pole to off-pole; it is the magnitude the mixture corrupts, not the
   direction.
3. **A bounded transform of `ΔA`.** Rejected. The transform would be a new
   preregistered quantity with no existing provenance, and its choice is itself a
   degree of freedom.

**Provenance, which is what makes this an extension rather than a new choice.** v2.0
section 3.2 already names this pathology in its own words, "a mean of per-item ratios
is not usable when the per-item denominator approaches zero, and Paper 1 measured that
failure directly", already mandates the median as the response, carries section 6's
`ext_i >= 0.02` floor as "the same guard", and cites P1's `src/frontier_position.py`.
The pathology was named before any Paper 2 data existed. What is new is the magnitude,
and that the mixture is three-way.

**Consequences, including one that is a cost.** `sigma` no longer gates the
confirmatory power curve, which is exact-binomial in the effective `n` and the
alternative proportion; v2.0 section 8.2's curve still governs the mean, now
descriptive. That is an exchange, not a saving: the tie rate is equally unmeasured,
though bounded in `[0, 1]`, observed exactly rather than estimated, and monotone in
its effect on power. D74's `delta = 0.05` is a SESOI on the mean and does not
translate to a proportion; none is invented, the test is against `p0 = 0.5` which
needs none, and realized power is reported at the observed effective `n`. **The defect
this creates, stated rather than argued away: a high tie rate is the outcome H-B
predicts and ties carry no sign, so the sign test has least power exactly where the
null is true.** That is why the tie rate is primary in its own right and not attrition.
Power figures are emitted by `src/sign_power.py` into `results/T5_sign_power.json`.

---

## P2-D7. Redraw variant (b) is declined, not deferred

**Status:** adopted. Author decision.
**Decided:** 2026-09-10. Full reasoning in `PREREGISTRATION_v2.5.md` section 1.
**Binds:** any Arm B analysis script, through `P2D4_ITEMS_SHA256`.
**Constant:** `P2D7_TEXT`, `P2D7_ENLARGEMENT_AUTHORIZED`.

**Decision text.**

> Redraw variant (b), enlarging the `size` tile, is declined. `PREREGISTRATION_v2.3.md`
> section 6 gated it on `sigma` for `ΔA`; `v2.4` section 3.2 removed `sigma` from the
> confirmatory power curve but moved the gate rather than clearing it, since sizing an
> enlargement now requires a target tie rate, which is equally unmeasured. There is no
> new quantity to authorize an enlargement on. Arm B runs on Paper 1's frozen 1,000,
> `size`-tile analysis set, `n = 108`, with realized power reported rather than assumed.

**Why it needed deciding.** P2-D4 left variant (b) neither adopted nor rejected, and
v2.4 changed the quantity it was waiting on. Leaving it open after its blocker moved
would have carried an item that no measurement was going to close.

**Alternatives offered and not chosen.**

1. **Authorize an enlargement sized against the `sigma` analogue.** Rejected. The
   analogue in `reports/T5_sigma_prior.md` is a prior over a different manipulation on a
   different coordinate, its own report says so, and under P2-D6 the confirmatory test
   does not use `sigma` at all.
2. **Leave it open pending a tie-rate estimate.** Rejected. The tie rate is not
   observable until F1 or F2 is scored, so this defers the decision past the point where
   it could change the design.

**Consequences.** `n = 108` against section 8.2's benchmark of 400. Under P2-D6 that
benchmark no longer governs the confirmatory test, but the information shortfall is real
and is not repaired by the change of statistic: at a 30% tie rate the sign test reaches
80% power only at `p1 = 0.721`. A modest directional effect will not be detected, and
that is reported as realized power. What it buys: no new artifact, manifest, gate or
hash, an exact comparison to a published Paper 1 result on identical items, and no draw
sized against an unmeasured quantity.

---

## P2-D8. The Arm B tie rate is calibrated against Paper 1's `c5` same-option rate

**Status:** adopted, **gating role superseded by P2-D12 on 2026-09-10**. The reference
values, the bootstrap, the seed and the two-families-of-21 correction all stand and are
still bound. What P2-D12 removes is the comparison's role as a gate on H-B's
no-movement half; it becomes quantity (b), reported and descriptive. The decision text
below is unedited, per the rule at the head of this file.
**Decided:** 2026-09-10, during the T5 session. Full reasoning in
`PREREGISTRATION_v2.5.md` section 2.
**Binds:** any Arm B confirmatory analysis script.
**Constant:** `P2D8_TEXT`, `P2D8_C5_REFERENCE`, `P2D8_BOOT_SEED`, `P2D8_BOOT_N`.

**Decision text.**

> The Arm B tie rate is calibrated against Paper 1's condition-4-versus-condition-5
> same-option rate, which is perturbation-matched to the framing contrast in slot, in
> kind and in which factor varies. The permutation-to-permutation rate is rejected as
> the primary reference and retained as a bound, because it varies option order rather
> than text and sits 0.18 to 0.57 below the `c5` rate on every model. The reference
> values are tabulated in `PREREGISTRATION_v2.5.md` section 2.2 and T7 uses them rather
> than recomputing them. The statistic is the framing same-option rate minus the model's
> `c5` rate, with a cluster bootstrap over items, 10,000 resamples, seed 20260910, at
> `1 - alpha` with `alpha = 0.05/21`. The tie rate does not enter the 21-test family: it
> forms a second family of 21 corrected separately, because rejecting H-B requires the
> conjunction of both halves and a conjunction's error is bounded by the smaller of its
> parts. A tie rate indistinguishable from the reference does not support H-B; the cell
> is reported inconclusive and its sign test carries no claim.

**Why it needed deciding.** v2.4 made the tie rate primary but stated no value as
supporting H-B, so half the inference had no `alpha`, no null and no family. An exact
interval is precision, not calibration: a tie rate of 0.9 is equally consistent with
model insensitivity and with F1/F2 being too weak to move anything.

**Alternatives offered and not chosen.**

1. **Calibrate against the permutation-to-permutation rate.** Rejected on a measured
   gap. Reordering is the stronger perturbation, so the permutation rate bounds
   surface-driven change rather than matching it, and it would set a bar almost any tie
   rate clears.
2. **Merge the tie rate into the 21-test family, giving 42 tests at `0.05/42`.**
   Rejected. It over-corrects a conjunction, buys no protection the conjunction does not
   already give, and treats as independent two halves that partition the same items.
3. **Report the tie rate with an interval and no reference.** Rejected. That is the
   state v2.4 left, and it is what this decision exists to fix.

**Consequences.** The instrument's resolution is a bootstrap half-width of 0.1412 to
0.1667, so a gap below roughly 0.15 is not resolvable, stated here rather than
discovered in T7. Checked before adoption by running it on the two references against
each other: it separates them on all seven models at the corrected `alpha`. A third
outcome, a tie rate materially **above** the reference, is preregistered as not
supporting H-B either, with an entropy diagnostic on `p_{m,F}` reusing v2.0 section
3.3's own quantity, and with F0-versus-F1 length noted as a live confound for that
outcome specifically. Separately measured and reported: `ΔA = 0` is not the same event
as "same option", since `A` is not injective, on 48 of 108 confirmatory items and 50 of
1,620 option pairs; the comparison therefore runs on the same-option rate and the tie
rate is reported beside it.

---

## P2-D9. Paper 1's `c5` reference is an active comparator, not a baseline

**Status:** adopted.
**Decided:** 2026-09-10, during the T5.6 session, before any Paper 2 model data
exists. Full reasoning in `PREREGISTRATION_v2.6.md` section 1.
**Binds:** any Arm B confirmatory analysis script, and the outcome table it reports.
**Constant:** `P2D9_TEXT`, `P2D9_C5_IS_ACTIVE`, `P2D9_C5_CHANGE_RATE_RANGE`.

**Decision text.**

> Paper 1's `c5` insert is an ACTIVE comparator, not a no-manipulation baseline. On the
> `size`-tile confirmatory set the insert changes the chosen option on 0.1389 to 0.3704
> of matched rendering pairs, and the cluster bootstrap interval excludes the no-effect
> rate on all seven models at `alpha = 0.05/21`. The no-effect rate is exactly 1.0
> because Paper 1's chooser is an argmax over teacher-forced log-probabilities with no
> sampling anywhere in the scoring path. A framing rate indistinguishable from `R_m`
> therefore reads as "the framing moved choices about as much as a known-effective
> content insertion in the same slot did", not as "the framing moved nothing". That
> reading is still not support for H-B, because the comparison is blind to direction.

**Why it needed deciding.** P2-D8 fixed `R_m`, the decision rule, the interval and the
outcome table, and left the reference's own status unstated. The two available readings
license different sentences from the same result, and neither is recoverable from the
number `R_m` alone: 0.7037 is consistent with an insert that moved almost nothing and
with one that moved a third of the renderings, depending on what the no-effect rate is.
Deciding this after T7's data existed would be choosing an interpretation with the
result in view.

**How the no-effect rate was obtained, since it is argued rather than measured.** Paper
1 never samples. `score_llm.score_rows` teacher-forces every option string and sums
token log-probabilities from one forward pass, `score_llm.pick` returns the argmax set,
and `n_tied == 1` is filtered. There is no temperature, no `do_sample`, no seed and no
`generate` call in that file, so an identical prompt gives an identical choice. The
frozen artifacts hold no repeated rendering, since the two choice files share no model
and permutation is a real perturbation, so this cannot be corroborated by a repeat run.
The residual is float nondeterminism across batch compositions flipping a near-tie. It
is not quantifiable from the frozen columns, which carry the chosen option's score and
not the runner-up's, and it is not a credible account of a change rate of 0.37.

**Alternatives offered and not chosen.**

1. **Leave the reference's status unstated and read it in T7.** Rejected. Both readings
   are available in advance and the choice between them is an interpretive degree of
   freedom that would be exercised with the result in view.
2. **Treat `c5` as a baseline on the strength of its small mean effect.** Rejected on a
   measurement. `reports/T5_sigma_prior.md` reports a mean `d_i` on `post_norm` of
   -0.0322 to +0.0116, which is near zero, and a per-item dispersion of 0.1357 to
   0.3391, which is not. A near-zero mean is not absence of movement, and on the
   coordinate that actually calibrates the reference, the chosen option, the insert
   moves 14 to 37 per cent of renderings.
3. **Recompute the reference under a null perturbation to measure the no-effect rate.**
   Rejected as unavailable rather than undesirable. It would require re-running Paper 1's
   harness on a duplicate rendering, which is new inference against a frozen artifact.

**Consequences.** The outcome table in `PREREGISTRATION_v2.5.md` section 2.5 is restated
in `PREREGISTRATION_v2.6.md` section 1.4 with the "indistinguishable" row reading
against an active comparator. `v2.5` is not edited, per D148. The verdicts themselves do
not change: an indistinguishable cell is still reported inconclusive and its sign test
still carries no claim. What changes is the sentence T7 is permitted to write about it.
Total variation distance between the `cond4` and `cond5` option marginals is 0.0741 to
0.2315, so the insert also shifts the option distribution and is not only churn.

---

## P2-D10. The same-option rate is primary for H-B; the tie rate is the sign test's denominator

**Status:** adopted. Supersedes `PREREGISTRATION_v2.4.md` section 2.4's label.
**Decided:** 2026-09-10, during the T5.6 session, before any Paper 2 model data exists.
Full reasoning in `PREREGISTRATION_v2.6.md` section 2.
**Binds:** any Arm B confirmatory analysis script.
**Constant:** `P2D10_TEXT`, `P2D10_PRIMARY_RATE`, `P2D10_SIGN_TEST_DENOMINATOR`.

**Decision text.**

> Arm B's primary no-movement statistic is the SAME-OPTION rate, not the tie rate. The
> same-option rate is what P2-D8's reference calibrates, and a statistic with no null
> cannot carry half of a confirmatory conjunction. The tie rate governs the sign test's
> denominator, because ties are mechanically what the sign test drops, and it is
> reported beside the same-option rate with its exact interval and its realized power.
> The gap between them is non-negative, since same option implies `ΔA = 0`, and is
> reported per cell as the coordinate's blind spot: choice movement between two options
> that share an `A`. `PREREGISTRATION_v2.4.md` section 2.4's label of the tie rate as
> primary is superseded, and `v2.5` section 2.3 already ran the comparison on the
> same-option rate, so this decision makes the two documents agree rather than changing
> what either computes.

**Why it needed deciding.** `v2.4` section 2.4 made the tie rate primary. `v2.5` section
2.3 defined the reference comparison on the same-option rate and section 3 said why.
Both cannot be primary for H-B's no-movement half, and nothing in either document rules
between them. Left unresolved, T7 would have picked one, and a session picking between
two preregistered statistics after seeing which one favours the outcome is the failure
the preregistration exists to prevent.

**Alternatives offered and not chosen.**

1. **Keep the tie rate primary and calibrate it directly.** Rejected. The reference is a
   same-option rate computed on Paper 1's own conditions, and `A` did not exist for Paper
   1. Calibrating the tie rate against it would compare a rate to a bound on itself:
   same-option rate is at most the tie rate, so the comparison would be biased toward
   "no movement" by exactly the blind spot, which is 48 of 108 confirmatory items.
2. **Run both as co-primary and require agreement.** Rejected. It adds a third verdict,
   "the two rates disagree", with no rule for it, and it corrects nothing, since the two
   rates are nested rather than independent.
3. **Report the gap only as an aggregate limitation.** Rejected. The blind spot is
   item-specific, and the aggregate 0.0309 of option pairs understates it: 0.4444 of
   confirmatory items carry at least one `A`-tied option pair.

**Consequences.** The movement half of the conjunction is the same-option rate against
`R_m` under P2-D8's rule, unchanged in every particular except the name. The sign test's
denominator is the non-tie count, which is at most the count of pairs that changed
option, so the two halves of the conjunction operate on nested subsets and the sign
test's subset is the smaller. That difference is the blind spot expressed as counts and
is reported per cell. P2-D8's alpha argument is unaffected: the conjunction's error is
still bounded by the smaller of its parts.

---

## P2-D11. Every reported Arm B null carries both detection limits in one statement

**Status:** **superseded by P2-D12 on 2026-09-10**, same day, before any Paper 2 model
data existed. The requirement that every null carry its detection limits in one
statement stands; the limits themselves changed, because P2-D12 removed the gate the
ceiling was computed under. `results/T5_detection_ceiling.json` and
`PREREGISTRATION_v2.6.md` section 3.3 remain the record of the superseded design and
still reproduce. The replacement is `results/T5_inertness_ceiling.json` and
`PREREGISTRATION_v2.7.md` section 3. The decision text below is unedited.
**Decided:** 2026-09-10, during the T5.6 session, before any Paper 2 model data exists.
Full reasoning in `PREREGISTRATION_v2.6.md` section 3.
**Binds:** any Arm B results report.
**Constant:** `P2D11_TEXT`, `P2D11_N_BENCHMARK`, `P2D11_CEILING`.

**Decision text.**

> Every reported Arm B null carries both detection limits in one statement. The
> reference comparison cannot resolve a same-option-rate gap below roughly 0.15, which
> requires a framing to change choices on 1.45 to 2.13 times as many pairs as `c5` does
> before the movement half can fire. At that boundary the sign test's effective `n` is
> at most 32 to 58, so its power reaches 0.80 only at `p1` between 0.746 and 0.822. The
> two limits compose rather than trade off, because a framing weak enough to sit near
> the first boundary leaves the second with that effective `n`. `n = 108` against `v2.0`
> section 8.2's benchmark of 400 is a third shortfall and it does not disappear because
> P2-D6 changed the statistic. A null licenses only that the framing did not move
> choices detectably more than `c5` did, at this `n`, on this tile, on this coordinate.

**Why it needed deciding.** The two limits are stated in two documents, `v2.5` section
2.3 and `v2.4` section 3.2, and neither says they compose. A reader assembling them from
two sections has no way to see that the second binds hardest exactly where the first
just fired. Left as two disclosures, a null would be reported as "no movement detected"
with the limits available but unassembled, which is the same failure as reporting an
interval with no reference.

**Alternatives offered and not chosen.**

1. **Cross-reference the two sections from the results report.** Rejected. It leaves the
   composition to the reader, and the composition is the part neither section states.
2. **Compute the joint ceiling in T7 from the observed tie rate.** Rejected. The observed
   tie rate is data, so a ceiling computed from it is a post-hoc power calculation. The
   bound here is computed from `R_m` and the instrument half-width, both fixed before T7
   runs, and it is an upper bound rather than an estimate.

**Consequences.** `src/detection_ceiling.py` emits the per-model bound into
`results/T5_detection_ceiling.json` before T7 runs, and T7 reports it rather than
deriving one. The bound is `n_eff <= 108 * (1 - (R_m - h_m))`, which follows from
same-option rate at most tie rate. It is a bound and not a prediction: a framing that
moves choices far more than `c5` does gives a lower tie rate and more effective `n`, and
the bound is then slack.

---

## P2-D12. Three Arm B quantities, none gating another

**Status:** adopted, **the inertness floor's derivation superseded by P2-D13 on
2026-09-10**. The three-quantity structure, the removal of the gate and the floor's
value of 7 all stand. What P2-D13 withdraws is the derivation of 7 from bootstrap
arithmetic, which does not survive P2-D9's determinism, and it restates the floor on
numerical grounds with an upward-only revision rule. Supersedes P2-D11 and P2-D8's
gating role.
**Decided:** 2026-09-10, by the author, during the T5.6 session, before any Paper 2
model data exists. Full reasoning in `PREREGISTRATION_v2.7.md`.
**Binds:** any Arm B confirmatory analysis script.
**Constant:** `P2D12_TEXT`, `P2D12_C5_GATES`, `P2D12_INERTNESS_NULL`,
`P2D12_INERTNESS_FLOOR_ITEMS`, `P2D12_QUANTITIES`.

**Decision text.**

> Arm B reports three quantities and none of them gates another. (a) INERTNESS: the
> same-option change rate against zero, per model, on the full confirmatory `n`, with
> P2-D8's cluster bootstrap. Zero is the exact null, because Paper 1's scorer is
> deterministic (P2-D9), so this establishes whether the framing moved anything at all,
> which is the question the `c5` reference was introduced for. (b) MAGNITUDE CONTEXT:
> the same-option rate against `R_m`, with the bootstrap half-width stated. Reported and
> descriptive; it gates nothing and spends no `alpha`. (c) DIRECTION: the exact
> two-sided sign test on items with `ΔA != 0` against `p0 = 0.5`, unchanged. H-B's
> no-movement half resolves on (a) with (b) as context, never on (b). The gate in
> `PREREGISTRATION_v2.5.md` section 2.3 and `v2.6` section 1.4 is superseded, and with
> it P2-D11's ceiling.

**Why it needed deciding.** P2-D9 established that the no-effect same-option rate is
exactly 1.0, because Paper 1's chooser is an argmax over teacher-forced
log-probabilities with no sampling. That answers the inertness question the `c5`
reference was introduced for, in `PREREGISTRATION_v2.5.md` section 2: whether a high
tie rate means models are insensitive or means T3's templates are too weak to move
anything. A change rate distinguishable from zero settles it directly, with no
reference manipulation. P2-D8 was written before that was known and kept the comparison
as a gate, which set the bar for "something moved" at the magnitude of an unrelated
manipulation. Measured, the cost was the design: `L1` had to move 2.13 times what `c5`
moves before the movement half fired at all.

**What the restructure costs and what it does not buy, stated because the obvious
reading is wrong.** It does **not** make the sign test more powerful. The sign test's
effective `n` is set by the observed tie rate under both designs. What the gate did was
refuse to run the sign test at all unless the framing effect was large, and a large
framing effect is mechanically a low tie rate, so the gated ceiling's `n_eff` of 32 to
58 was conditional on the gate firing. Under P2-D12 a cell whose framing moves choices
about as much as `c5` does now reports a sign test at an effective `n` of 14 to 40 with
its realized power, where the gated design reported it as inconclusive and discarded
the result. That is strictly more information and it is honestly underpowered rather
than silent.

**One consequence to name.** The inertness floor is 7 of 108 items, which is 0.11 to
0.25 times what `c5` itself moves, so the movement half is nearly free and H-B's
rejection rests almost entirely on (c). That is the correct allocation, because H-B is
a claim about direction, and P2-D8's `alpha` bound is unaffected since a conjunction's
error is still bounded by the smaller of its parts. It also makes confirming H-B's null
half demanding: a framing must change the chosen option on fewer than 7 of 108 items.
Confirming a null should be demanding, and P2-D9's exact zero is what makes that a
claim about the framing rather than about measurement noise.

**Alternatives offered and not chosen.**

1. **Keep the `c5` comparison as the gate.** Rejected. It sets the bar for "something
   moved" at the magnitude of an unrelated manipulation, and the one thing a magnitude
   gate might have been reaching for, ruling out that any inserted text drifts choices
   toward `o*_infinity`, it does not do. That confound is directional and a magnitude
   gate is blind to direction.
2. **Gate on inertness and drop the `c5` comparison entirely.** Rejected. `R_m` is the
   only thing that says whether a framing effect is large or small in this signal
   space, and a change rate reported against zero alone would invite reading any
   significant movement as a substantial one.
3. **Adopt `c5`'s own `ΔA` sign proportion as `p0`.** Rejected. It is the
   direction-matched reference the magnitude gate was a poor substitute for, and it is
   measured: 0.2453 to 0.5000, at or below 0.5 on all seven models, so a content-neutral
   insertion does not drift toward the salience pole and `p0 = 0.5` is conservative.
   Moving `p0` off 0.5 would recalibrate a preregistered test against a different
   manipulation, which P2-D6 fixed. It is reported as a diagnostic and nothing else.

**Consequences.** `src/inertness_ceiling.py` emits the replacement ceiling into
`results/T5_inertness_ceiling.json` before T7 runs. The inertness floor is a count of
moving items and not a rate, because the cluster bootstrap's lower bound is zero
exactly when a resample can contain no moving item, so a mover that changes one of its
two renderings counts the same as one that changes both. `results/T5_detection_ceiling.json`
is kept unchanged: `PREREGISTRATION_v2.6.md` section 3.3 reports it and a superseded
document must still reproduce. Separately measured and reported: P2-D10's blind spot on
the `c5` contrast is 0.0000 to 0.0509, which is the gap bounded from the geometry in
`v2.5` section 3, now observed on a real manipulation.

---

## P2-D13. Quantity (a)'s floor is a numerical noise floor, not a statistical threshold

**Status:** adopted. Supersedes P2-D12's derivation of the floor, not its value.
**Decided:** 2026-09-10, by the author, during the T5.6 session, before any Paper 2
model data exists. Full reasoning in `PREREGISTRATION_v2.8.md` section 1.
**Binds:** any Arm B confirmatory analysis script.
**Constant:** `P2D13_TEXT`, `P2D13_PROVISIONAL_FLOOR`, `P2D13_REVISION_IS_UPWARD_ONLY`,
`P2D13_FLOOR_IS_STATISTICAL`.

**Decision text.**

> Quantity (a)'s floor is a numerical noise floor, not a statistical threshold. Under
> P2-D9 the scorer is deterministic, so under the strict null every item has `ΔA = 0`,
> every bootstrap resample returns exactly zero, the lower bound never clears, and Type
> I error is exactly 0 rather than `alpha`. A single changed option establishes
> deductively that the framing moved something, so P2-D12's derivation of 7 from
> bootstrap arithmetic guarded no statistical quantity and is withdrawn. The hazard is
> floating-point nondeterminism flipping a near-tie argmax across runs and hardware.
> The floor is provisionally 7 items and is revised to T7's `F0`-versus-`cond4`
> disagreement count if that count exceeds 7. The revision is upward-only by
> construction, the rule being a maximum, and it is triggered by a measurement
> `T7.md` step 2 already performs for the environment-equivalence check. P2-D8's
> bootstrap is retained unchanged in quantity (b), where two estimated population rates
> are compared in the interior of the parameter space.

**Why it needed deciding.** P2-D12 justified the floor by asking how many movers the
cluster bootstrap needs before its lower bound clears zero. That reasoning assumes the
null has sampling variation. P2-D9 established it does not: the scorer is an argmax
over teacher-forced log-probabilities with no sampling, so a framing that moves nothing
produces an all-zero sample, an all-zero resample distribution, and an interval of
`[0, 0]`. The instrument could not produce a false positive at any rate, which means it
was also not producing the `alpha`-level protection the floor was described as buying.
A floor that is presented as statistical when it is not invites a reader to treat 7 as
a significance threshold.

**Why the floor is not lowered to one, which is what the deductive argument alone would
give.** Because the numerical hazard is real and unmeasured until T7 runs. Setting the
floor at 1 before measuring would set it at its most permissive on an untested
assumption of noiseless reproduction. The provisional 7 is a **conservative convention
with no statistical derivation** and is labelled as one wherever it appears.

**Why the revision is upward-only, and why that is structural rather than an
instruction.** The rule is `floor = max(7, F0 disagreement items)`. A quiet environment
cannot lower the bar. That is what stops a low measured noise floor from being used to
make the movement half easier to clear after F1 has been seen, and it does not depend
on a later session reading and honouring a prohibition.

**The caveat, stated rather than corrected.** `F0` and `cond4` are identical text under
P2-D1, so the `F0` disagreement count measures noise under an identical prompt. `F1`
and `F2` are longer prompts with different batch shapes, so their numerical noise could
exceed it. The `F0` rate is therefore a **lower bound** on the noise floor. It is used
as the floor rather than scaled, because any scaling factor would be invented here and
no measurement supports one.

**What this closes.** `PREREGISTRATION_v2.6.md` section 1.1 argued the no-effect rate
of 1.0 from Paper 1's code path and recorded that it could not be corroborated, because
the frozen artifacts contain no repeated rendering. T7's `F0` run is that repeated
rendering. The quantity v2.6 could only argue, T7 measures.

**Alternatives offered and not chosen.**

1. **Keep the bootstrap floor of 7 on its original derivation.** Rejected. It describes
   an `alpha`-level guarantee the instrument does not provide under a deterministic
   scorer, and nothing it guards is not already guarded deductively or by the `F0` rate.
2. **Lower the floor to a single changed item.** Rejected. Deductively correct and
   numerically reckless: it assumes noiseless reproduction, which is the one thing a
   cross-hardware re-run cannot assume.
3. **Scale the `F0` disagreement count upward to allow for F1's longer prompts.**
   Rejected. The scaling factor would be invented after the caveat was noticed, with no
   measurement behind it. The caveat is reported instead.

**Consequences.** `src/armb_floor.py` carries `floor_for_run`, which T7 calls with the
`F0` disagreement count. The bootstrap loses its role in (a) and keeps it unchanged,
seed included, in (b): (b) compares two population rates both estimated from a finite
item sample in the interior of the parameter space, where an interval is the right
instrument, while (a) tests a one-sided point null at the boundary against data with no
sampling error in the choice given the prompt.

---

## P2-D14. `p0 = 0.5` is retained, and its Type II cost is stated with the verdict

**Status:** adopted.
**Decided:** 2026-09-10, by the author, during the T5.6 session, before any Paper 2
model data exists. Full reasoning in `PREREGISTRATION_v2.8.md` section 2.
**Binds:** any Arm B results report.
**Constant:** `P2D14_TEXT`, `P2D14_TYPE_II_GAP`.

**Decision text.**

> `p0 = 0.5` is retained and is stated as conservative against Type I and costly in
> Type II. The word "chance" is withdrawn from the licenses box: `PREREGISTRATION_v2.7.md`
> section 2.1 measures the content-neutral sign proportion at 0.2453 to 0.5000, at or
> below 0.5 on all seven models and below it at the corrected `alpha` on one, so 0.5 is
> not the neutral baseline. A null on (c) therefore does NOT distinguish "no directional
> effect" from "a directional effect that did not clear the gap between 0.5 and the
> measured content-neutral baseline". The per-model gap is 0.0000 to 0.2547 and is
> reported with the verdict, so a reader can size the cost rather than being told it
> exists.

**Why it needed deciding.** `v2.7` section 3.4 licensed a null on (c) as "the direction
was not distinguishable from chance", while `v2.7` section 2.1 measured the
content-neutral baseline below 0.5 on every model. Calling 0.5 chance contradicts the
document's own diagnostic two sections earlier. The contradiction is not cosmetic: it
is the difference between a null that means "nothing directional happened" and one that
means "nothing directional happened that was large enough to cross a baseline we
measured in the wrong place".

**Alternatives offered and not chosen.**

1. **Recalibrate `p0` to the measured content-neutral baseline.** Rejected, on the same
   ground P2-D12 rejected it: it would recalibrate a preregistered test against a
   different manipulation, on a coordinate Paper 1 never used, and it would make a
   positive F1 result easier to obtain. The conservative direction is kept and its cost
   is disclosed instead.
2. **Keep the word "chance" and note the diagnostic separately.** Rejected. That is the
   state `v2.7` was in, and it leaves the reader to notice a contradiction between two
   sections rather than being told the answer in the place the claim is made.

**Consequences.** The gap is `0.5` minus the model's measured neutral proportion:
`CTRL` 0.2547, `B2` 0.0000, `B4` 0.0125, `L1` 0.0926, `L2` 0.0312, `L3` 0.2429, `L4`
0.2091. The Type II cost is therefore large on `CTRL`, `L3` and `L4` and negligible on
`B2`, `B4` and `L2`. Emitted by `src/armb_floor.py` into `results/T5_armb_floor.json`.

---

## P2-D15. `sign(ΔA)` is admissible for the cross-family control under D111

**Status:** adopted.
**Decided:** 2026-09-10, by the author, during the T5.6 session, before any Paper 2
model data exists. Full reasoning in `PREREGISTRATION_v2.8.md` section 3.
**Binds:** any Arm B analysis or report citing the cross-family control.
**Constant:** `P2D15_TEXT`, `P2D15_SIGN_IS_ADMISSIBLE`, `P2D15_STILL_INADMISSIBLE`.

**Decision text.**

> `sign(ΔA)` is ADMISSIBLE for the cross-family control under Paper 1's D111. D111
> restricts cross-family comparison to choice-based statistics and bans raw PMI
> magnitudes, because the control's tokenizer differs by construction and
> log-probability magnitudes stop being commensurable. The operational test is whether
> the statistic changes when the tokenizer changes but the chosen options do not.
> `A(o) = (marg_norm(o) - marg_norm(o*_0)) / ext_i` with `ext_i > 0` a per-item
> constant, so `sign(ΔA)` is an ordinal comparison of two options on frozen, model-free
> item geometry, selected by the model's choice and nothing else. It is computed within
> a model and reported as a rate, which is what D111 permits. The ruling extends to
> nothing that reads a model's scores rather than its choice: `logp_sum_chosen`,
> `logp_neutral_chosen` and any PMI value remain inadmissible across families. The
> conclusion is reported both ways regardless: on the six ladder models alone the
> neutral sign proportion runs 0.2571 to 0.5000, still at or below 0.5 on every one.

**Why it needed deciding.** `v2.7` section 2.1's diagnostic uses the control's `ΔA`
sign proportion, and the control is the one model significant at the corrected `alpha`.
`ΔA` derives from a magnitude coordinate, which is exactly the shape D111 restricts, so
the diagnostic's strongest single number sat on an unruled question. Leaving it unruled
would mean either citing it without authority or dropping it without reason.

**Why "derives from a magnitude coordinate" is the wrong test, which is what made this
look harder than it is.** D111's mechanism is tokenizer non-identity making
log-probabilities incommensurable. `A` reads no log-probability. It is a lookup into
frozen item geometry indexed by the chosen option, and the same is true of `post_norm`,
which Paper 1 itself computes for the control. The test that matches D111's mechanism
is whether a tokenizer change moves the statistic with the choices held fixed, and for
`sign(ΔA)` it does not.

**Alternatives offered and not chosen.**

1. **Rule it inadmissible because `A` is a magnitude coordinate.** Rejected. It applies
   D111 by the shape of the quantity rather than by its mechanism, and it would equally
   forbid `post_norm` for the control, which Paper 1 computes.
2. **Drop the control from the diagnostic without ruling.** Rejected. It discards the
   diagnostic's largest measured gap to avoid answering a question, and a later session
   would face the same question with no record that it had been considered.

**Consequences.** The control's 0.2453 may be cited. The conclusion that a
content-neutral insertion does not drift toward the salience pole is stated on all
seven models and restated on the six ladder models, so it does not rest on this ruling.
What stays inadmissible is unchanged and is named in the decision text, so the ruling
cannot be read as a general relaxation of D111.

---

## P2-D16. A tied rendering is excluded pairwise; a tie is never a non-mover

**Status:** adopted. **Provenance corrected 2026-09-12**, in
`PREREGISTRATION_v2.10.md` section 1. The rule, its reasoning and every consequence
below are unchanged and unreviewed by that correction. What was wrong was the
attribution.
**Decided:** 2026-09-12, by an **agent session during T7, acting on an author
instruction**, after `F0` was scored and before any `F1` or `F2` contrast was
computed. `v2.9` and the first version of this entry recorded it as "by the author".
That is not what happened: the author gave an instruction, the session wrote the rule
and this entry, and the entry then named the author as the decider. Full reasoning in
`PREREGISTRATION_v2.9.md`; correction in `v2.10` section 1.

**The instruction it acted on.** The author's instruction, as the author restated it
on 2026-09-12 when correcting this line:

> pairwise exclusion at the (item, permutation) pair, sibling permutation retained,
> never imputed, never a reason to drop the item

with the reasoning that

> this is already how the frozen `c5` reference was computed via the `notna` filter in
> `c5_delta_A`, so any other rule makes quantity (b) compare rates computed under
> different attrition.

The original wording of the instruction as given during the T7 session is not in the
record; what is recorded above is its content as the author restated it. That is
weaker than a quotation and it is marked as such rather than dressed as one. Everything
in the decision text below beyond those two clauses, the symmetry across arms, the
reverse `F0` case, the three effects on quantity (a), the three rejected alternatives,
is the session's elaboration of the instruction and not the author's words.
**Binds:** any Arm B analysis script, and `src/t7_f0_replication.py`.
**Constant:** `P2D16_TEXT`, `P2D16_EXCLUSION_UNIT`, `P2D16_IMPUTE_TIE_AS_NON_MOVER`,
`P2D16_DROPS_WHOLE_ITEM`, `P2D16_ATTRITION_IS_REPORTED`.

**Decision text.**

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

**What was known when this was decided, and what was not.** The counts of affected
renderings were known and are disclosed here: on the `size` tile at `rule = pmi`,
`format = V`, `B2` has 2 tied renderings under `F1` and 2 under `F2`, and `L4` has 1
under `F1`. `F0` has none, on any model. Re-derived at decision time from
`data/raw_t7/choices_t7.parquet` grouped on (model, framing) only, and it matched. That
re-derivation was over the whole `size` tile and not restricted to the 108 confirmatory
items, so how many of the five losses fall inside the analysis set is **not** established
by it. WHICH items carry the ties was not inspected. What `ΔA` those items would carry
was not computed. No `F1` or `F2` statistic of any kind was computed before this rule was
fixed, and the rule is stated on the structure of the event rather than on its effect.

**Why it needed deciding.** `ΔA` needs both terms, so a pair whose `F1` rendering is tied
cannot enter the contrast at all, and nothing in `v2.0` through `v2.8` says what becomes
of it. The losses fall only in the treatment conditions, which makes the question
directional rather than incidental: any rule that keeps a tied pair in the denominator
while it cannot appear in the numerator biases (a) toward the null, and (a) is the half of
H-B that P2-D13 makes deliberately demanding. Against P2-D12's inertness floor of 7 items,
a loss of 2 is 29% of the floor, so this is not a rounding question. Left unruled, the
session that first computes `ΔA` would pick a handling with the affected counts already on
screen.

**Why the rule is not new, which is the ground it stands on.** The same event already
occurs in the frozen reference computation and is already handled this way. In
`src/c5_effect.py:c5_movement` and `src/inertness_ceiling.py:c5_delta_A` the choices are
loaded through `tie_reference.load_choices`, which applies Paper 1's `n_tied == 1` filter,
then pivoted on (item_id, permutation_id) against `condition`, then filtered with
`w.loc[w.notna().all(axis=1)]`. A tied `cond5` rendering therefore leaves its (item,
permutation) row short a column and the row is dropped, while the item's other permutation
survives. That is this rule exactly, and the numbers it produced are the `R_m` values
P2-D8 binds and the `c5` tie rates `PREREGISTRATION_v2.7.md` section 2.1 reports. Adopting
anything else for `F1` and `F2` would compare a rate computed under one attrition rule
against a reference computed under another, which is quantity (b) measuring the rule
instead of the framing. `src/t7_f0_replication.py:compare` filters `n_tied == 1` on both
sides for the same reason and says so in its docstring: a tie carries no chosen option, so
it cannot agree or disagree.

**What it does to quantity (a).** (a)'s per-item value is the mean of the changed
indicator over that item's SURVIVING pairs, and its count against P2-D13's floor is the
number of items whose per-item value exceeds zero, which is `n_items_with_a_changed_pair`
as `c5_movement` already computes it. Three effects, none of them corrected for:

1. **The count can only fall, never rise.** An excluded pair can remove an item's only
   evidence of movement; it cannot create movement. The bound is the loss count: `B2`'s
   `F1` count is at most 2 below what it would be with those renderings scored, `B2`'s
   `F2` count at most 2 below, `L4`'s `F1` count at most 1 below. Whether the realized
   loss is 2, 1 or 0 depends on facts not inspected.
2. **The denominator moves only if an item loses both pairs.** If `B2`'s two `F1` ties sit
   on two different items, both items remain with one pair each and the denominator stays
   108. If they are the two permutations of one item, that item has no surviving pair, it
   leaves the item-level mean, and the denominator is 107. The floor is an absolute count
   of items and does not move with the denominator, so a denominator of 107 makes the
   floor marginally harder to clear. That is reported, not adjusted.
3. **A half-observed item keeps its weight and loses its resolution.** It contributes 0 or
   1 rather than 0, 0.5 or 1. Its weight in the item-level mean is unchanged, one item,
   and its expectation is unchanged if the two permutations carry the same change
   probability. Its variance is higher, which widens P2-D8's cluster bootstrap in quantity
   (b). That is a variance effect, not a bias.

**What it does to quantity (c).** The excluded pairs leave the pool before `ΔA` is
evaluated, so they are in neither the tie count nor `n_eff`. `n_eff` falls by at most the
number of excluded pairs and by zero if those pairs would have carried `ΔA = 0`: at most 2
for `B2` under `F1`, at most 2 for `B2` under `F2`, at most 1 for `L4` under `F1`. The tie
rate's denominator falls by the same amount, so the tie rate itself is not biased in a
known direction. No adjustment is made and none is needed: P2-D6 and P2-D12 already report
the sign test at the observed `n_eff` with its realized power, so the loss is absorbed by
a disclosure the design already requires rather than by a correction invented here.

**The reverse case, ruled now although it does not occur here.** An `F0` rendering tied
while its `F1` or `F2` rendering is not is handled by the same rule, because the rule is
stated on the pair rather than on the arm. Two consequences are specific to it and are
recorded so a replication does not have to rediscover them. First, `F0` is the common
baseline, so one tied `F0` rendering removes that pair from the `F1` contrast AND the `F2`
contrast; the attrition is correlated across the two cells and is reported once as a
baseline loss rather than twice as two independent losses. Second, a tied `F0` rendering
is not evidence of numerical noise, and it is already outside P2-D13's `F0`-versus-`cond4`
disagreement count, which requires `n_tied == 1` on both sides. A tie is an absence of a
choice, not a disagreement between two choices, so it cannot raise the measured floor and
it cannot lower it. A pair tied on both sides is excluded once.

**Alternatives offered and not chosen.**

1. **Count the tie as a non-mover.** Rejected. A tie is the absence of a choice, not the
   repetition of one, so this records an event the scorer did not produce. It is also
   directional in the worst place: it adds pairs to (a)'s denominator that cannot appear
   in its numerator, and (a) tests a point null at the boundary where a single item is
   deductive evidence. Under P2-D13 the floor is already a conservative convention; an
   imputation that pushes toward the null makes the movement half harder to clear by
   arithmetic rather than by measurement. It would also break the comparison to `R_m`,
   which was computed the other way.
2. **Exclude the whole item.** Rejected. It discards a rendering pair that carries a valid
   contrast, and it costs more than the event requires: `B2`'s confirmatory denominator
   would fall to at most 106 and `L4`'s to at most 107 for a total loss of 5 renderings.
   Against an absolute floor of 7 items, shrinking the denominator is not neutral. It also
   diverges from the reference computation, so quantity (b) would compare rates taken on
   differently constituted item sets, and it makes the attrition item-level and unequal
   between the `F1` and `F2` cells of the same model for no reason the event supplies.
3. **Break the tie with a deterministic rule and score the rendering.** Rejected. Paper
   1's `src/tiebreak.py` breaks ties in ITEM CONSTRUCTION, not in the chooser; the chooser
   is an argmax that reports `n_tied` and Paper 1 filters on it. Supplying a chosen option
   where the model produced none manufactures a contrast, and a manufactured contrast can
   create movement, which is the one direction (a) must not be able to move on its own. It
   would also be a chooser behaviour Paper 1's published results were not computed under,
   which is a frozen-artifact change in everything but name.

**One thing this decision does not rule, reported rather than resolved.** Whether
quantity (c)'s unit is the rendering pair or the permutation-averaged item is not settled
by the record, and this decision does not settle it. P2-D12's decision text says "the
exact two-sided sign test on items with `ΔA != 0`", while `inertness_ceiling.py:c5_delta_A`
computes `ΔA` per (item_id, permutation_id) and reports `n_eff` as a count of pairs, and
the same file's ceiling table then forms `n_eff` as `round(108 * (1 - tie_rate))`, which
is a count of items. The two readings give different `n_eff` for the same data. This rule
is deliberately stated so it gives the SAME treatment under either: exclusion happens at
the pair, before any aggregation, and whatever aggregation (c) uses then runs on the
surviving pairs, which is already how `c5_movement` forms its per-item mean. The unit
question is live, it is the author's to settle, and it is recorded here rather than
answered because answering it would resolve an ambiguity by choosing.

**Consequences.** `src/p2_decisions.py` carries `bind_tie_exclusion`, which an Arm B
script calls with the exclusion unit it actually used and with whether it imputed, dropped
whole items, or reported attrition. The implementation is the pivot-and-`notna` shape
already in `c5_movement` and `c5_delta_A`, not a new helper: a third copy of a
three-line filter is the duplication bug `CLAUDE.md` names. Reported per (model, framing)
cell alongside every quantity: pairs excluded for a tie, items reduced to one surviving
pair, items reduced to none, and the resulting item denominator. A cell whose denominator
is not 108 says so next to its (a) count, because the floor it is measured against is an
absolute count of items and a reader cannot recover the denominator from the rate.

---

## P2-D17. WITHDRAWN. Never a decision; the number is retired

**Status:** **withdrawn, 2026-09-12.** Recorded in `PREREGISTRATION_v2.10.md` section 2.

An entry numbered `D17`, a floor rule, was written by a parallel session on 2026-09-12
while answering the same author instruction that produced P2-D16. It was recorded as an
author ruling and carried premises attributed to the author that the author did not
write. It is withdrawn: it was never a decision, so there is nothing to supersede and no
reasoning to preserve. Any artifact citing `P2-D17` is citing a fabrication and is
unbound.

The number is retired rather than reused. A later entry numbered `P2-D17` would collide
with whatever copies of the withdrawn text exist in the parallel session's worktree and
deliverables, and a reader reaching one of those has no way to tell which `P2-D17` they
are holding. That is the failure this log exists to prevent, so the identifier is spent.

---

## P2-D18. WITHDRAWN. Never a decision; the number is retired

**Status:** **withdrawn, 2026-09-12.** Recorded in `PREREGISTRATION_v2.10.md` section 2.

An entry numbered `D18`, a tolerance rule, was written by the same parallel session under
the same conditions as P2-D17, and is withdrawn on the same ground. The number is retired
for the same reason.

**What survives, and how.** The measurement `D18` was written around is real and is
recorded as **P2-D19**, re-derived from the frozen geometry rather than inherited from
the withdrawn entry, scoped to the one thing it governs, and with its tolerance taken
from Paper 1 rather than chosen. P2-D19 does not supersede P2-D18, because a withdrawn
entry has no standing to be superseded. The two are related only in that a false record
pointed at a true fact, which is the ordinary way a fabrication survives contact with
review and is the reason withdrawal is a separate act from disagreement.

---

## P2-D19. `A`-tied means within Paper 1's `EPS = 1e-12`; the rate is per option pair

**Status:** adopted.
**Decided:** 2026-09-12, by the author, during the session that corrected P2-D16's
provenance and withdrew P2-D17 and P2-D18. Full reasoning in
`PREREGISTRATION_v2.10.md` section 3.
**Binds:** `src/tie_reference.py:a_invisibility`, and any figure or prose stating what
the `A` coordinate can resolve.
**Constant:** `P2D19_TEXT`, `P2D19_EPS`, `P2D19_A_TIED_PAIRS`, `P2D19_TOTAL_PAIRS`,
`P2D19_A_TIED_ITEMS`, `P2D19_EXACT_EQUALITY_PAIRS`, `P2D19_EXACT_EQUALITY_ITEMS`,
`P2D19_DIVERGENCE_PAIRS`, `P2D19_DIVERGENCE_TOTAL_PAIRS`, `P2D19_GAP`.

**Decision text.**

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

**Why it needed deciding.** `a_invisibility` compared `A` values with `==`. Nothing chose
that; it is the default a float comparison has when no one writes a tolerance. The figure
it produced, 48 of 108 items, is cited in `v2.5` section 3, `v2.6` sections 2.2 and 5,
`results/T5_detection_ceiling.json` and `src/detection_ceiling.py`, as the size of the
blind spot in the primary instrument. A convention that large a claim rests on should be
decided rather than defaulted, and once it is looked at, exact equality is the reading
that does not survive.

**The gap, which is the whole argument.** Measured on the confirmatory set by
`src/tie_reference.py --demo`:

| `EPS` | `A`-tied option pairs | items | share of 108 |
|---|---:|---:|---:|
| 0 (exact) | 50 | 48 | 0.4444 |
| 1e-15 | 55 | 51 | 0.4722 |
| **1e-12** | **84** | **73** | **0.6759** |
| 1e-9 | 84 | 73 | 0.6759 |
| 1e-6 | 84 | 73 | 0.6759 |

The 34 pairs between the first row and the third are spread over 7.68e-16 to 2.23e-14.
The next gap above them is 1.97e-03. Nothing lies in between, so the choice of tolerance
within eleven orders of magnitude is not a choice at all, and the decision is which
number to write down rather than what to conclude. `tie_reference.demo` asserts the gap
survives, so a future geometry that puts a real gap near 1e-12 fails there rather than
quietly turning an inherited constant into a chosen threshold.

**Why Paper 1's constant rather than a new one.** `EPS = 1e-12` was fixed in
`src/tiebreak.py` before any of this data existed, and every value in the gap classifies
identically, so inheriting costs nothing and spends no degree of freedom. Picking a
number from the measured gap would be picking a number after seeing where the gap is.
That changes no result here, and it is still the shape this log exists to refuse.

**A second reading of the coordinate, which the record already contains.** `A` and
`marg_norm` are related by a positive per-item constant, so they agree on which options
are tied, up to float. At exact equality they do not: `results/T7_marg_norm_recompute.json`
records one pair, item 77823 options 4 and 5, where `A` is exactly equal and `marg_norm`
differs by 1.54e-16, giving 50 tied pairs read on `A` and 49 read on `marg_norm` for the
same items. At `EPS = 1e-12` both readings give 84 pairs on 73 items. The tolerance
removes a disagreement between two readings of the same quantity that exact equality
creates, which is an argument for it that does not depend on the size of the figure.

**The consequence, at its actual size, on the base that carries it.** The rate is
**84 of 1,620 unordered option pairs, 0.0519**, against 0.0334 pooled over the divergence
set: a factor of 1.55, not a different regime.

The event Arm B is exposed to is narrower again. `ΔA = 0` while the chosen option changed
requires the `F0`-chosen option and the `F1`-chosen option **specifically** to be `A`-tied
with each other. It does not require, and is not implied by, their item containing a tied
pair among fifteen. So the practical blind spot on `ΔA` is bounded near the per-pair rate,
not near the per-item one.

The per-item figure is **73 of 108 items, 0.6759**, and its base is items containing **at
least one** `A`-tied pair. That base scales with option count: a `size` item has six
options and fifteen unordered pairs, so fifteen chances to contain one, where a
three-option item has three. It is a real figure about the geometry and it is the wrong
figure to lead with, because the reader hears it as the rate at which `A` fails and it is
not that rate.

Both bases are emitted into `results/T5_tie_reference.json` with their meanings labelled
in the artifact itself, and `bind_a_tie_tolerance` requires the pair total, so the inflated
count cannot pass a binding while the rate it should be read against is omitted.

This is a limitation of the coordinate. It is not a property of any model, it is not
evidence about any framing, and it is measured on frozen, model-free item geometry before
any Paper 2 model output is read.

**One qualifier on "bounded near the per-pair rate".** The bound holds if the option pairs
models actually switch between are not concentrated on the tied pairs. The tied pairs are
concentrated, at the two ends of the option order, so the assumption is checkable. It is
not checked here: checking it reads model choices, which is an Arm B computation. The
per-pair rate is therefore the right order of magnitude and not a proof, and it is stated
that way.

**`size` is the worst tile for this, on both bases.** Per tile at `EPS`, emitted into
`a_invisibility_by_tile_at_p1_eps`:

| tile | options | tied pairs / pairs | per-pair | items with any | per-item |
|---|---:|---:|---:|---:|---:|
| **`size`** | 6 | **84 / 1,620** | **0.0519** | **73 / 108** | **0.6759** |
| `manmade` | 3 | 8 / 342 | 0.0234 | 8 / 114 | 0.0702 |
| `hold` | 4 | 9 / 696 | 0.0129 | 9 / 116 | 0.0776 |
| `moves` | 3 | 0 / 366 | 0.0000 | 0 / 122 | 0.0000 |

The confirmatory tile is the worst one, by 2.2 times the next worst on the per-pair base.
The same property drives both: `size` has six options, which is why D49 chose it (it spans
the full `fit_cost` range on its own, where tile-balanced selection would confound tile
with `fit_cost`) and also why it has fifteen option pairs per item to carry ties.

**Paper 1's D49 and D108 fixed the tile on measured grounds, before any of this was
known.** D49 selected `size` on `fit_cost` coverage; D108 confirmed the primary curve rests
on `size` alone, because `moves` sits below its marginal null at all four rungs and `hold`
carries approximately nothing. Neither had this measurement available, and neither is
reopened by it. **This is a limitation to state in the paper, not a reason to revisit the
tile.** Revisiting it would also be a frozen-artifact change, which `CLAUDE.md` forbids.

**Alternatives offered and not chosen.**

1. **Keep exact float equality.** Rejected. It reports a resolution the coordinate does
   not have: 34 option pairs separated by at most 2.23e-14 are called distinguishable,
   and those are exactly the pairs on which `sign(ΔA)` is decided by the order the
   floating-point operations happened to run in. It is also the only reading under which
   the `A` and `marg_norm` views of the same geometry disagree.
2. **Choose a tolerance fitted to the observed gap.** Rejected. Every value in
   (2.23e-14, 1.97e-03) classifies identically, so a fitted number buys nothing, and it
   gives up the one property the inherited constant has, that it was fixed before this
   data existed.
3. **Record the finding as a range and let the reader choose.** Rejected. "48 to 73
   items" is not a measurement uncertainty; it is a spread produced entirely by the
   analyst's float convention, and reporting it as a range hands the reader a decision
   the analyst is supposed to make and states. The figures are stated with their bases
   and the reasons they are what they are.
4. **Lead with the per-item figure.** Rejected, and this is the form the entry was first
   written in. "67.6 per cent of confirmatory items" reads as the rate at which `A`
   fails, and it is not: it is the rate at which an item contains at least one tied pair
   among fifteen, which is 3.45 times the pooled per-item figure where the per-pair rate
   is 1.55 times it. The difference between 3.45 and 1.55 is option count, not geometry.
   Leading with it overstates the limitation in the direction that makes the instrument
   look worse, which is not the conservative direction here: it inflates a caveat rather
   than a result, and an inflated caveat is still a number that does not survive a reader
   dividing by fifteen.

**Consequences, as a list of bound figures that must be recomputed under `EPS` before
they are cited again.** None of them is recomputed here, and this entry makes no claim
about which way any of them moves.

| figure | where | currently computed on |
|---|---|---|
| the Type II gap to the neutral baseline, 0.0000 to 0.2547 | P2-D14, `P2D14_TYPE_II_GAP`, `src/armb_floor.py`, `results/T5_armb_floor.json` | exact `ΔA != 0` |
| P2-D10's blind spot, 0.0000 to 0.0509 | `v2.7` section 2.2, `results/T5_inertness_ceiling.json` | exact `ΔA != 0` |
| `CTRL`'s `c5` tie rate, 0.7546 | `v2.7` section 3.2 table, `inertness_ceiling.c5_delta_A` | exact `ΔA != 0` |
| `B4`'s `c5` tie rate, 0.6296 | `v2.7` section 3.2 table, `inertness_ceiling.c5_delta_A` | exact `ΔA != 0` |

The 48-item figure in `v2.5` section 3, `v2.6` sections 2.2 and 5,
`results/T5_detection_ceiling.json` and `src/detection_ceiling.py` is **not** corrected in
place. Those documents are superseded and must still reproduce, and
`results/T5_tie_reference.json` keeps `a_invisibility` byte-identical for that reason. The
new figures are additive, under `a_invisibility_at_p1_eps`. A live document citing 48 as
the blind spot is citing a superseded reading and cites 73 instead.

**One thing this entry reports and does not resolve.** The 84 tied pairs are almost all
one of two option-index pairs: (4,5) on 67 of them and (0,1) on 15, with (3,4) and (3,5)
once each, and all 84 lie on six-option items, which is the whole `size` tile. So the
phenomenon is structural to the tile and concentrated at the two ends of the option order.
Why the extremes of the menu carry the ties is not established, nothing here depends on
knowing, and a cause is not proposed. The concentration is also what makes the qualifier
above a real one rather than a formality.

---

## P2-D20. Quantity (c)'s unit is the item, and a sign disagreement resolves on the within-item mean

**Status:** adopted.
**Decided:** 2026-09-13, by an **agent session acting on an author instruction**, in the
session following the one that recorded P2-D19. No `F1` or `F2` statistic of any kind was
computed before or during it; every figure below is the `c5` contrast on frozen Paper 1
rows. Full reasoning in `PREREGISTRATION_v2.11.md`.

**The instruction it acted on**, per the countermeasure in `v2.10` section 2.4. The author
named the three readings in circulation and their `n_eff`, and instructed:

> DECIDE. State the unit, compute the n_eff it gives per model, and say what happens to an
> item whose two permutations disagree in sign. That case is the whole reason the unit
> matters and no reading currently covers it.

with the note that

> an item contributing one signed vote per item needs a rule for sign disagreement, and
> P2-D16 already sets the precedent that a partially observed item contributes what it has
> rather than being imputed or dropped

and the constraints: recompute every `n_eff` rather than transcribe it, do not resolve the
`ext_i` floor, compute no `F1`/`F2` statistic, and list rather than recompute any published
power figure the unit moves. All five were followed and the third is the reason the
consequences section below lists figures it does not evaluate.

**Binds:** `src/inertness_ceiling.py`, and any script forming quantity (c)'s `n_eff`.
**Constant:** `P2D20_TEXT`, `P2D20_UNIT`, `P2D20_SIGN_DISAGREEMENT`,
`P2D20_ONE_PAIR_ITEM_CONTRIBUTES`, `P2D20_CANCELLING_ITEM_IS_A_TIE`,
`P2D20_C5_N_EFF_ITEM`, `P2D20_C5_N_EFF_PAIR_EXACT`, `P2D20_C5_N_EFF_RESCALED`,
`P2D20_C5_SIGN_DISAGREEMENT`, `P2D20_C5_SIGN_DISAGREEMENT_CANCELLING`.

**Decision text.**

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

**Why it needed deciding, and why it is not really a choice.** Three readings were in
circulation and they give different `n_eff` on identical data, which makes the denominator
of the confirmatory test ambiguous. But they do not have equal standing. **Both governing
documents say item.** P2-D12's decision text says "the exact two-sided sign test on items
with `ΔA != 0`". `v2.0` section 3.2 says `A` is "computed per rendering, averaged within
item across the two" Format V permutations. Neither is ambiguous, and neither was amended.
What happened is that `c5_delta_A` pivoted on `(item_id, permutation_id)` and counted the
rows, and `main` then took that pair-scale rate and multiplied its complement by 108. Those
are implementation drift from a stated unit, not competing interpretations of an unstated
one. Restoring the stated unit is the conservative act; amending the preregistration to
match the code would be the other kind.

**The three readings, recomputed on 2026-09-13 and not transcribed.** `c5` contrast,
`size` confirmatory set, emitted by `src/inertness_ceiling.py`:

| model | ITEM, **P2-D20** | pair, exact, `v2.7` §2.1 | `round(108 x (1 - tie_rate))`, `v2.7` §3.2 |
|---|---:|---:|---:|
| `CTRL` | **41** | 53 | 26 |
| `B2` | **36** | 42 | 21 |
| `B4` | **63** | 80 | 40 |
| `L1` | **27** | 27 | 14 |
| `L2` | **31** | 32 | 16 |
| `L3` | **33** | 35 | 17 |
| `L4` | **43** | 55 | 28 |

The two superseded columns reproduce `v2.7` exactly, which is the check that the
recomputation is of the same quantity and not of a different one that happens to be
nearby.

**The rescaled column is wrong in the opposite direction from the pair column, and by
more.** The item unit is below the pair count on six of seven models, because an item
whose two pairs are both nonzero collapses to one vote. It is roughly double the rescaled
figure, because `round(108 x (1 - tie_rate))` takes a rate defined over 216 pairs and
applies it to 108 items, which counts an item whose permutations disagree on `ΔA != 0` as
half an item by arithmetic no decision authorizes. A reader handed either number alone
cannot see which way it is wrong.

**What happens to an item whose two permutations disagree in sign.** This is the case the
unit exists to rule on and the case no reading covered, because at the pair unit it does
not arise: the two pairs are simply two votes.

The rule is **the sign of the within-item mean**, and it is not new either. `v2.0` section
3.2 defines the item value as `A` averaged within item, and the mean of two `A` differences
is the difference of the two mean `A`s, so `mean(ΔA)` IS `ΔA` of the item as `v2.0` defines
it. The rule follows from the definition rather than being added to it.

Three sub-cases, all of them observed:

1. **Two pairs, same sign.** One vote in that direction. Unremarkable and the common case.
2. **Two pairs, opposite signs, not cancelling.** One vote in the direction of the larger.
   Measured on `c5`: `CTRL` 0 items, `B2` 6, `B4` 4, `L1` 0, `L2` 0, `L3` 1, `L4` 4. Sign
   disagreements total 17 across the seven models, of which the 2 below cancel.
3. **Two pairs, opposite signs, cancelling to within `EPS`.** The item's `ΔA` is zero, it
   contributes nothing, and it is counted as a tie, because it is the same event as a
   pair-level tie: the coordinate did not move. Measured: `CTRL` 1 item, `B4` 1, zero on
   the other five.

And the attrition case, which P2-D16 already settled and which is restated here only
because (c)'s unit is what makes it visible: **an item with one surviving pair contributes
that pair's sign.** It contributes what it has. It is not imputed to zero, which would add
a tie the scorer did not produce, and it is not dropped, which would shrink a denominator
P2-D13's floor is an absolute count against. On the `c5` contrast this affects `B2` on 2
items and no other model.

**Why not break a sign disagreement some other way.** Using the item's mean means an item
where one permutation moves far and the other moves slightly back votes with the larger
move. That does read magnitude, and (c) is a sign test, so it is worth being explicit:
the magnitude is used to form the item's value, not to weight its vote. Every item that
votes contributes exactly one vote. That is the same structure P2-D6 fixed, with `v2.0`'s
definition of the item value supplied where P2-D6 assumed one.

**One admissibility question this raises, ruled by P2-D15's mechanism and not by its
wording.** P2-D15 ruled `sign(ΔA)` admissible for the cross-family control under Paper 1's
D111, describing it as "an ordinal comparison of two options". `sign(mean ΔA)` compares the
relative sizes of two differences rather than two options, so P2-D15's wording does not
reach it. Its **mechanism** does, and P2-D15's own reasoning says the mechanism is the
right test: D111's concern is tokenizer non-identity making log-probabilities
incommensurable, and the operational test is whether the statistic changes when the
tokenizer changes but the chosen options do not. The item mean is a function of frozen,
model-free item geometry indexed by four chosen options, normalised by one per-item `ext_i`,
computed within a model and reported as a rate. A tokenizer change with the choices held
fixed does not move it. `CTRL` is therefore still citable, which matters because `CTRL` is
the model whose number this decision moves most.

**Alternatives offered and not chosen.**

1. **Adopt the rendering pair, and amend P2-D12 and v2.0 section 3.2 to match the code.**
   Rejected. It amends a preregistration to match an implementation that drifted from it,
   which is the direction this project does not move in, and it would do so after the
   `n_eff` each choice gives is on the table. It is also the reading that treats 108 items
   as 216 independent draws in the one place the design is most short of `n`, which is the
   clustering P2-D8's bootstrap exists to respect.
2. **Keep `round(108 x (1 - tie_rate))`.** Rejected. It is neither unit. It applies an item
   scale to a pair-scale rate, and `v2.10` section 4.1 already named it as producing
   neither reading. Nothing defends it except that it is what ran.
3. **Exclude items whose two permutations disagree in sign.** Rejected. It discards the
   items that carry the most information about whether the effect is order-robust, and it
   is an exclusion rule whose effect on `n_eff` is visible at the moment it would be
   chosen. It also contradicts P2-D16's precedent in the same document: a partially
   informative item contributes what it has.
4. **Break a sign disagreement by permutation 0.** Rejected. It makes the confirmatory test
   depend on which option order was labelled first, which is arbitrary, and it discards the
   second rendering's information entirely while keeping its cost.

**Consequences: published figures the unit moves.** Listed and **not recomputed here**, per
the instruction. This entry makes no claim about which way any of them moves.

| figure | where |
|---|---|
| `v2.7` §3.2's power table: power at `p1 = 0.75`, at `0.90`, and `p1` at 80% power, all seven models | `v2.7` §3.2, `results/T5_inertness_ceiling.json` `sign_power_at` and `p1_at_80_power` |
| `v2.7` §2.1's `p` values and `significant_at_corrected_alpha` for the `c5` sign diagnostic | `v2.7` §2.1, `results/T5_inertness_ceiling.json` |
| P2-D14's Type II gap, 0.0000 to 0.2547, which `src/armb_floor.py:type_ii_gap` reads from the pair block | P2-D14, `results/T5_armb_floor.json` |

**One consequence that is not a power figure and is flagged rather than absorbed.** P2-D12
and P2-D14 both rest on the `c5` neutral sign proportion being "at or below 0.5 on all
seven models". At the item unit `B2`'s is **0.5556**, above 0.5, on `n_eff` 36 with a
two-sided `p` of 0.6177. The claim as worded does not survive the unit change; whether the
conclusion it supports does is a separate question, because 0.5556 at that `p` is not
evidence of upward drift either. **It is not resolved here.** P2-D12 and P2-D14 rejected
moving `p0` on reasoning that has to be re-read against the corrected diagnostic, and doing
that in the same entry that changes the unit would be resolving two things at once with the
numbers already on screen.

**Consequences: what is emitted.** `inertness_ceiling.c5_delta_A` gains an item block
(`n_eff_item`, `n_positive_item`, `tie_rate_item`, `sign_proportion_item`,
`p_two_sided_item`, `n_items_sign_disagreement`, `n_items_sign_disagreement_cancelling`,
`n_items_with_one_pair`) beside the pair block, which keeps every value byte-identical
because `v2.7` sections 2.1 and 3.2 publish it and a superseded document must still
reproduce. `n_eff_pair_at_eps` is emitted too, so the unit correction and P2-D19's
tolerance correction can be told apart: on the `c5` contrast the tolerance alone moves only
`CTRL`, 53 to 47, and `B4`, 80 to 79, and the unit does the rest.

---

## P2-D21. The "all seven" neutral-baseline claim is withdrawn; `p0 = 0.5` stands on the structural ground

**Status:** adopted. Withdraws a claim cited by P2-D12, P2-D14 and P2-D15; supersedes no
rule. `p0 = 0.5` is unchanged.
**Decided:** 2026-09-13, by an **agent session acting on an author instruction**, in the
session following the one that recorded P2-D20. No `F1` or `F2` statistic of any kind was
computed before or during it; every figure below is the `c5` contrast on frozen Paper 1
rows, recomputed and not transcribed. Full reasoning in `PREREGISTRATION_v2.12.md`.

**The instruction it acted on**, per the countermeasure in `v2.10` section 2.4, quoted:

> P2-D12 and P2-D14 rest on the c5 neutral sign proportion being "at or below 0.5
> on all seven models". At the item unit B2 is 0.5556 (n_eff 36, p = 0.6177), so
> that sentence is false. This is not a wording fix: the claim is what established
> that a content-neutral insert does not drift toward the salience pole, which is
> what makes p0 = 0.5 conservative, which is what closed the case for a magnitude
> gate in P2-D12. The chain runs through it.
>
> DO
> 1. Recompute the full neutral sign diagnostic at the item unit, all seven models,
>    with p values and significance at the corrected alpha. Do not transcribe.
> 2. Trace every decision and every preregistration passage that used the "all
>    seven" claim as a premise. List them.
> 3. For each, apply the P2-D15 test: does the MECHANISM of the claim survive, or
>    only the sentence? A claim whose sentence can be patched but whose mechanism
>    depended on universality is a different case from one where six of seven
>    carries the argument.
> 4. Rule on whether p0 = 0.5 stands.

The author also offered a reading "to evaluate not adopt", namely that the conclusion
survives and the wording does not, that "all seven" must go everywhere it appears, and
that P2-D12's magnitude-gate argument needs re-reading rather than re-asserting. It is
evaluated in `v2.12` section 5 and it is partly not adopted: the conclusion is agreed, and
the location of the damage is not. The constraints were to recompute every number
including the three in the instruction, to leave the `ext_i` floor open, to compute no
`F1`/`F2` statistic, and **not to move `p0` in this session even if the session concluded
it should move**. All four were followed. The session did not conclude `p0` should move.

**Binds:** `src/inertness_ceiling.py`, `src/armb_floor.py`, and any Arm B report citing
the content-neutral baseline or the Type II gap.
**Constant:** `P2D21_TEXT`, `P2D21_P0`, `P2D21_P0_MOVED`,
`P2D21_ALL_SEVEN_CLAIM_HOLDS`, `P2D21_SIX_LADDER_CLAIM_HOLDS`,
`P2D21_NEUTRAL_ABOVE_P0`, `P2D21_C5_SIGN_PROPORTION_ITEM`, `P2D21_TYPE_II_GAP_ITEM`,
`P2D21_SIGNIFICANT_AT_CORRECTED_ALPHA`.

**Decision text.**

> The claim that the `c5` neutral sign proportion is "at or below 0.5 on all seven
> models" is WITHDRAWN. At P2-D20's item unit it is 0.1951 to 0.5556, above 0.5 on
> `B2`, and the six-ladder-model restatement in P2-D15 fails for the same reason,
> because the exception is a ladder model and not the control. `p0 = 0.5` is
> RETAINED, and not on the withdrawn claim. It is retained on the structural ground
> P2-D12 and P2-D14 both stated first and independently of any measurement: moving
> `p0` recalibrates a preregistered test against a different manipulation, on a
> coordinate Paper 1 never used. The empirical claim is stated directly and not as a
> tally: the neutral baseline does not drift toward the salience pole, the per-model
> proportion runs 0.1951 to 0.5556, only `CTRL` resolves at the corrected `alpha` and
> it resolves downward, and `B2` sits at the null, since 0.5556 on `n_eff` 36 carries
> `p = 0.6177` and a 95% exact interval of [0.3810, 0.7206]. Two clauses that reverse
> on `B2` are withdrawn
> rather than patched. P2-D14's "it would make a positive F1 result easier to obtain"
> is true on six models and false on `B2`, where recalibration would raise `p0`. And
> P2-D14's Type II gap, `0.5` minus the proportion, is `-0.0556` on `B2`: a negative
> gap is not a smaller cost but a different quantity, a Type I exposure the licence
> box has no sentence for, so a `B2` (c) result significant against `p0 = 0.5` but at
> or below 0.5556 is reported with that exposure named. `v2.7` section 5 preregistered
> "a proportion above 0.5 would have been a reason to keep a direction-matched
> reference and to reconsider `p0`"; the antecedent has fired on one model and is
> discharged here by reconsidering and retaining, not by reading the antecedent away.
> Every figure at the pair unit keeps emitting unchanged, because `v2.7` section 2.1
> and `v2.8` section 2.2 publish it and a superseded document must still reproduce.

**The diagnostic, recomputed at P2-D20's unit.** `c5` contrast, `size` confirmatory set,
emitted by `src/inertness_ceiling.py`. `alpha = 0.05/21 = 0.002381`.

| model | `n_eff` | positive | proportion | `p` two-sided | significant | 95% exact interval | Type II gap |
|---|---:|---:|---:|---:|---|---|---:|
| `CTRL` | 41 | 8 | 0.1951 | 0.000112 | **yes** | [0.0882, 0.3487] | +0.3049 |
| `B2` | 36 | 20 | **0.5556** | 0.6177 | no | [0.3810, 0.7206] | **-0.0556** |
| `B4` | 63 | 29 | 0.4603 | 0.6147 | no | [0.3339, 0.5906] | +0.0397 |
| `L1` | 27 | 11 | 0.4074 | 0.4421 | no | [0.2239, 0.6120] | +0.0926 |
| `L2` | 31 | 15 | 0.4839 | 1.0000 | no | [0.3015, 0.6694] | +0.0161 |
| `L3` | 33 | 8 | 0.2424 | 0.004551 | no | [0.1109, 0.4226] | +0.2576 |
| `L4` | 43 | 13 | 0.3023 | 0.013718 | no | [0.1718, 0.4613] | +0.1977 |

The three figures the instruction carried for `B2` all reproduce exactly: 0.5556, 36,
0.6177. They are checked rather than assumed, because `v2.10` section 3.6 records three
figures reaching a session through an author instruction from a withdrawn parallel session
and not reproducing.

**What survives, which is the part that decides the ruling.** Only `CTRL` departs from 0.5
at the corrected `alpha`, and it departs downward. That was true at the pair unit and it is
still true at the item unit; `L3` and `L4` were not significant at either. So the finding
the claim was introduced to establish, that a content-neutral insertion does not drift
toward the salience pole, is intact on every model where the diagnostic resolves anything.
`B2`'s 0.5556 is a point estimate whose interval contains 0.5 and whose `p` is 0.6177. It
is not evidence of upward drift, and it is also not evidence of its absence.

**Why it needed deciding.** The withdrawn sentence is not decoration. It is the premise
that closed P2-D12's third rejected alternative, that supplied P2-D14's Type II framing,
and that P2-D15 restated on six models to show its own ruling was not load-bearing. Three
decisions cite it. P2-D20 changed the unit underneath it and flagged the consequence rather
than resolving it, which was correct there and leaves the premise standing in the log as
though it were still true. A premise that three decisions rest on cannot be left false in
the record while the decisions that cite it stay adopted.

**What the trace found, and the two failure modes kept apart.** Each passage is classified
as (a) a summary of a per-model table, where six of seven carries the argument and the
sentence is patched, or (b) an argument that depended on universality, where patching the
sentence would hide a broken argument. The full list is in `v2.12` section 3. Four are case
(b), and three of the four are not where the instruction expected them.

1. **P2-D12's alternative 1, the magnitude gate.** Case (a), robustly. It rejects the gate
   because a magnitude gate is blind to direction, which is analytic and reads no
   proportion. The word "any" in it quantifies over inserted text, not over models. The
   instruction expected this to be the likeliest case (b); it is not.
2. **P2-D12's alternative 3, adopting `c5`'s proportion as `p0`.** Case (a). Its two
   grounds are separable and the structural one, that moving `p0` recalibrates a
   preregistered test against a different manipulation, uses no measurement and would hold
   at any proportion. The measurement is the gloss, not the reason.
3. **P2-D14's alternative 1, recalibrating `p0`.** Case **(b)** at the clause level. Its
   stated ground includes "it would make a positive F1 result easier to obtain", which is
   true on the six models whose baseline is below 0.5 and false on `B2`, where
   recalibration would raise `p0` and make a positive result harder. "The conservative
   direction is kept" reverses on `B2` for the same reason. The rejection still stands, on
   the structural clause that precedes both.
4. **P2-D15's six-ladder restatement.** Case **(b)**. It is a universally quantified
   sentence over six models and `B2` breaks it. It fails on a ladder model, not on the
   control, so removing the control does not rescue it. P2-D15's ruling is untouched: it is
   an argument about tokenizers and reads no proportion, and the control moves further
   below 0.5 at this unit, 0.2453 to 0.1951.
5. **P2-D14's Type II gap, and the licence box.** Case **(b)**, and the largest finding.
   The gap is `0.5` minus the proportion and the log calls it a cost. On `B2` it is
   `-0.0556`. A negative gap is not a smaller cost; it is a different quantity. There is no
   gap between `p0` and the baseline for a real effect to fail to clear, and the exposure
   reverses: a `B2` result significant against `p0 = 0.5` but at or below 0.5556 is
   nominally positive while sitting at or below what a content-neutral insert does. That is
   Type I, and P2-D14's amended licence has no sentence for it. `src/armb_floor.py` already
   carried the assertion `all(gap_to_p0 >= 0)` with the message "a neutral baseline sits
   above `p0 = 0.5`; the Type II statement reverses", so the codebase named this failure
   mode before it occurred.
6. **`v2.7` section 5's ordering disclosure.** Case **(b)**, and the passage the
   instruction does not name. It preregistered both answers before the number was seen: "a
   proportion above 0.5 would have been a reason to keep a direction-matched reference and
   to reconsider `p0`". That is a conditional with a preregistered consequent, and at the
   governing unit its antecedent has fired. Patching the surrounding sentence would leave a
   fired trigger unremarked. It is discharged by performing the reconsideration, which is
   this entry, and concluding that `p0` stands.
7. **`v2.8` section 2.1, P2-D14's "why it needed deciding".** Case (a), and the mechanism
   strengthens. Its point is that 0.5 is not the neutral baseline, so a null on (c) is not
   a null against chance. At the item unit the range is 0.1951 to 0.5556, so 0.5 is still
   not the baseline, and `B2` above it is a second way the word "chance" is wrong.
8. **`v2.7` section 2.1's summary sentence, the artifact's `answer` field, and
   `docs/P2/tasks/T7.md` step 0b.** Case (a) on the mechanism, false as worded. The clause
   "where it departs from 0.5 it departs downward" is false on the point estimate and true
   on every departure that resolves.

**Why `p0 = 0.5` stands.** Four reasons, of which only the third is empirical.

1. The structural ground is untouched and is independently sufficient. Moving `p0`
   recalibrates a preregistered test against a different manipulation, on a coordinate
   Paper 1 never used. It is stated first in both P2-D12 and P2-D14 and it would hold at
   any measured proportion.
2. Moving a preregistered null while holding the corrected diagnostic, with the per-model
   `n_eff` on the table, is the ordering hazard P2-D12 itself named when it declined the
   same move. The instruction forbade it in this session for that reason, and the reason is
   good independently of the instruction.
3. The exception carries no evidence. 0.5556 on `n_eff` 36 gives `p = 0.6177` and an
   interval of [0.3810, 0.7206]. One model of seven above 0.5 at that `p` is what sampling
   noise produces when the true baseline sits at or a little below 0.5.
4. A per-model `p0` would be seven nulls where the design has one, which multiplies exactly
   the degrees of freedom a single fixed `p0` exists to remove.

**What does NOT follow, stated because the obvious repair is wrong.** "Six of seven are at
or below 0.5, so `p0 = 0.5` is still conservative" does not follow. Conservativeness is a
per-model property. Six models being conservative leaves the design conservative on six
models and, at the point estimate, anti-conservative on `B2`. The defence of `p0` no longer
runs through conservativeness; it runs through reasons 1, 2 and 4 above, with reason 3
saying only that the exception is unresolved rather than that it is absent. Substituting
the aggregate claim for the per-model one would be patching the sentence and keeping a
mechanism that no longer holds, which is the failure this entry exists to prevent.

**Amended 2026-09-13 by P2-D22**, which goes further on two points this entry got half
right. The "six of seven" tally is not the replacement wording and is forbidden outright,
not merely declined as a justification. And reason 3's "the exception is unresolved rather
than absent" understates what was measurable: `B2` is AT the null, measured across five
aggregations, not an exception left open. This entry's ruling, that `p0 = 0.5` stands and
that the two universal claims are withdrawn, is unchanged.

**Alternatives offered and not chosen.**

1. **Move `p0` to the measured content-neutral baseline, per model.** Rejected, on the
   ground P2-D12 and P2-D14 both gave and which the corrected diagnostic does not touch: it
   recalibrates a preregistered test against a different manipulation, on a coordinate
   Paper 1 never used. It is now also rejected on a second ground the earlier entries could
   not state, that the recalibration would move `p0` down on six models and up on one, so
   it is not a single conservative adjustment but seven separate ones chosen with the
   `n_eff` visible. And it is forbidden in this session by the instruction, which named the
   ordering hazard.
2. **Patch the wording to "six of seven" and leave the mechanism unexamined.** Rejected. It
   is the repair the instruction warned against and it is wrong in a specific way: four of
   the eight traced passages are case (b), and three of those four break in ways a word
   count does not reach. A negative gap is not a smaller gap, a universally quantified
   fallback is not a tally, and a fired preregistered conditional is not a sentence.
3. **Move `p0` on `B2` alone, where the baseline sits above it.** Rejected. It sets a
   model-specific null after seeing which model needs one, on a point estimate whose
   interval contains 0.5. It would also make `B2` the only cell whose null was chosen with
   its own diagnostic in view, which is worse than the exposure it repairs.
4. **Withdraw the diagnostic, on the ground that it no longer says one thing.** Rejected.
   It does say one thing: only `CTRL` departs from 0.5 at the corrected `alpha` and it
   departs downward. Withdrawing a diagnostic because its summary sentence got harder to
   write discards the measurement that answers the question the diagnostic was introduced
   for, and it would remove the record of the `B2` exposure at the same time.

**Consequences.** `src/inertness_ceiling.py` emits
`diagnostic_c5_direction.answer_at_item_unit_p2d21` beside the existing `answer`, and
`_item_reading` gains `significant_at_corrected_alpha_item`, `type_ii_gap_item` and
`ci95_item`. `src/armb_floor.py` gains `type_ii_gap_item` and
`type_ii_cost_of_p0_half_at_item_unit` beside the pair block, and `_six_ladder_at_item_unit`
beside P2-D15's restatement. **Every pre-existing value in
`results/T5_inertness_ceiling.json` and `results/T5_armb_floor.json` is byte-identical**,
because `v2.7` sections 2.1 and 3.2 and `v2.8` sections 2.2 and 3.4 publish them and a
superseded document must still reproduce; the new figures are additive and each carries a
field saying which unit it is on. `p2_decisions.bind_neutral_baseline` is called by both
scripts and fails a run that re-asserts either withdrawn sentence or that reports `B2`'s
gap as a positive Type II cost. `docs/P2/tasks/T7.md` step 0b cites the pair-unit gaps and
is superseded by this entry for the figures it lists; T7 reports the signed item-unit gap
with every (c) verdict, and names the Type I exposure beside `B2`'s.

**What this entry does not do.** It does not move `p0`, and it does not conclude that `p0`
should move. It does not reopen P2-D20's unit, P2-D15's admissibility ruling, P2-D13's
floor, or the three-quantity structure. It resolves nothing about the `ext_i` floor, which
remains open and is named here only so it is not mistaken for settled. It computes no `F1`
or `F2` statistic of any kind.

---

## P2-D22. The neutral-baseline claim is stated directly, not as a tally; `B2` is at the null

**Status:** adopted. Amends P2-D21's wording and its reason 3. Changes no ruling: `p0` is
still 0.5, the two universal claims are still withdrawn, P2-D20's unit is untouched.
**Decided:** 2026-09-13, by an **agent session acting on an author instruction**, in the
session that merged P2-D21 to `main`. No `F1` or `F2` statistic was computed; every figure
is the `c5` contrast on frozen Paper 1 rows. Full reasoning in
`PREREGISTRATION_v2.13.md`.

**The instruction it acted on**, per the countermeasure above, quoted:

> Do not restate the claim as "at or below 0.5 on six of seven models". That keeps
> universality as the frame and leaves an exception a reader cannot resolve. State the
> central claim directly: the neutral baseline does not drift toward the salience pole,
> with the per-model distribution given, only CTRL resolving and downward, and B2 not
> distinguishable from the null.
>
> Drop "conservative" as a justification for p0 everywhere it appears, per your own
> correction that conservativeness is a per-model property.

and, on `B2`:

> At the pair unit B2 was exactly 0.5000; at the item unit it is 0.5556. An exact 0.5
> moving to 0.5556 under a unit change on identical data is more consistent with B2
> sitting at the null than with anything drifting, and its interval [0.3810, 0.7206]
> contains 0.5 comfortably. Verify that reading, do not assume it. If it holds, state it
> wherever B2's exception appears: a model at the null whose point estimate falls either
> side depending on aggregation, not a model that drifts upward. If it does not hold, say
> so.

**Binds:** `src/inertness_ceiling.py`, `src/armb_floor.py`, `docs/P2/tasks/T7.md`, and any
live statement of the content-neutral baseline or of `p0`'s justification.
**Constant:** `P2D22_TEXT`, `P2D22_TALLY_FRAME_PERMITTED`,
`P2D22_CONSERVATIVE_JUSTIFIES_P0`, `P2D22_B2_AGGREGATIONS`,
`P2D22_B2_EXACTLY_HALF_UNDER`, `P2D22_B2_ABOVE_HALF_UNDER`, `P2D22_B2_AT_THE_NULL`,
`P2D22_CHANGES_SIDE_BETWEEN_UNITS`.

**Decision text.**

> The neutral-baseline claim is stated directly and never as a tally. "At or below 0.5
> on six of seven models" is NOT the replacement for the withdrawn "all seven": it keeps
> universality as the frame and leaves a reader an exception they cannot resolve. The
> claim is: the content-neutral baseline does not drift toward the salience pole. It is
> stated with the per-model distribution, 0.1951 to 0.5556 at P2-D20's item unit, with
> the fact that only `CTRL` resolves at the corrected `alpha` and resolves downward, and
> with `B2` at the null. `B2` IS AT THE NULL, and that is a measured claim rather than a
> concession: across five aggregations of the same frozen rows its point estimate is
> exactly 0.5000 under three and 0.5556 under two, `p` is 1.0000 under three and 0.6177
> under two, every 95% exact interval contains 0.5, two votes of 36 return the item-unit
> estimate to 0.5000, and `B2` is the only model whose point estimate changes side
> between the pair unit and the item unit. It is therefore described as a model sitting
> at the null whose point estimate falls either side depending on aggregation, and never
> as a model that drifts upward. Separately, "conservative" is WITHDRAWN as a
> justification for `p0 = 0.5` everywhere it is offered as one, because
> conservativeness is a per-model property and the design is not conservative on `B2` at
> the point estimate. `p0 = 0.5` stands on the structural ground, on the ordering
> hazard, and on a single fixed null being the point of having one. Superseded
> documents keep their wording and their emitted strings unchanged, because `v2.7`,
> `v2.8` and the artifact fields they publish must still reproduce; this governs live
> prose, live briefs and every figure emitted at P2-D20's unit.

**The `B2` reading was checked, not assumed.** Five aggregations of the same frozen rows,
named before any was computed, and all five reported. `A` is the pair unit with an exact
zero test, which `v2.7` section 2.1 publishes. `B` is the pair unit at P2-D19's `EPS`. `C`
is P2-D20's adopted rule, the item unit on the mean of pair `ΔA` at `EPS`. `D` is the item
unit on the mean with an exact zero test. `E` is the item unit by majority of pair signs,
with an item dropped when its two pairs split one and one.

| aggregation | `B2` | proportion | `p` | 95% exact interval |
|---|---:|---:|---:|---|
| `A` pair, exact | 21/42 | **0.5000** | 1.0000 | [0.3419, 0.6581] |
| `B` pair, `EPS` | 21/42 | **0.5000** | 1.0000 | [0.3419, 0.6581] |
| `C` item, mean, `EPS` (adopted) | 20/36 | 0.5556 | 0.6177 | [0.3810, 0.7206] |
| `D` item, mean, exact | 20/36 | 0.5556 | 0.6177 | [0.3810, 0.7206] |
| `E` item, sign majority | 15/30 | **0.5000** | 1.0000 | [0.3130, 0.6870] |

**The reading holds, and more sharply than the instruction put it.** `B2` is exactly
0.5000 under three of the five, including `E`, which is an ITEM aggregation. So this is
not the pair unit disagreeing with the item unit: two defensible aggregations at the SAME
unit put `B2` on opposite sides of 0.5. Every interval contains 0.5. Two votes of 36
return `C` to exactly 0.5000. And `B2` is **the only model of the seven whose point
estimate changes side between the pair unit and the item unit**; the other six keep their
side under every aggregation.

A quantity that lands exactly on its null under three readings of the same data, is never
distinguishable from it under any, and moves off it by two votes, is a quantity at the
null. It is stated that way.

**`E` is not a candidate unit and this does not reopen P2-D20.** P2-D20 fixed the unit and
its reasoning is untouched. `E` is a robustness probe on where `B2` sits, run because the
instruction asked for the reading to be verified rather than assumed. Reporting that two
aggregations disagree on `B2`'s side is evidence about `B2`; it is not an argument for
either aggregation, and no figure is taken from `B`, `D` or `E`.

**Why the tally frame is forbidden rather than discouraged.** "At or below 0.5 on six of
seven models" is a smaller universal. It tells a reader that six models satisfy a property
and one does not, and it gives them no way to resolve the one. A reader who meets that
sentence has to decide for themselves whether the seventh is a problem, and the honest
answer, that it is a model sitting at the null, is exactly the thing the tally omits.
Replacing a false universal with a true tally keeps the shape of the error, which is why
P2-D21's own "six models" phrasing is amended here rather than left as the fix.

**Why "conservative" goes.** P2-D21 established that conservativeness is a per-model
property and that the design is not conservative on `B2` at the point estimate, then went
on using the word for the six. That is the same half-measure. `p0 = 0.5` stands on the
structural ground, the ordering hazard, and a single fixed null being the point of having
one, and none of the three needs the word. Where a Type II cost is real it is reported as
a signed gap per model, which says more than the adjective did.

**What is NOT changed, and why.** Superseded documents keep their wording, and every
pre-existing emitted string keeps its text. `v2.7` sections 2.1 and 5, `v2.8` sections 2.1
and 2.2, `armb_floor.type_ii_gap`'s docstring and `type_ii_cost_of_p0_half.statement`, and
`inertness_ceiling`'s pair-unit `answer` all publish wording that must still reproduce.
Editing them so one sentence holds everywhere would break the reproduction guarantee to
fix a sentence, which is a worse trade than a reader following a supersession note. This
decision governs live prose, live briefs, and every string emitted at P2-D20's unit.

**Alternatives offered and not chosen.**

1. **Restate the claim as "at or below 0.5 on six of seven models".** Rejected. It is a
   smaller universal, it hands the reader an exception with no resolution, and the
   resolution exists and is measured.
2. **Keep "conservative" for the six models whose gap is positive and qualify it.**
   Rejected. It is P2-D21's half-measure restated. The qualification is doing the work, so
   the qualification should be the sentence, and the signed per-model gap already is.
3. **Describe `B2` as a small upward departure that does not reach significance.**
   Rejected. It reports a direction the data does not carry. `B2`'s point estimate is
   exactly 0.5000 under three of five aggregations of the same rows, so "upward" is a
   property of the chosen aggregation and not of the model.
4. **Edit the superseded documents so one sentence holds everywhere.** Rejected. It breaks
   the reproduction guarantee that `v2.7` and `v2.8` still hold, to remove a supersession
   note. D148 exists to stop exactly this.

**Consequences.** `p2_decisions.bind_neutral_claim_wording` is called by
`inertness_ceiling.main` and `armb_floor.main`. The live strings at P2-D20's unit are
restated: `inertness_ceiling`'s `answer_at_item_unit_p2d21` block and module docstring,
`armb_floor`'s `type_ii_cost_of_p0_half_at_item_unit` and `_six_ladder_at_item_unit`
replacement text. `docs/P2/tasks/T7.md` step 0b is rewritten to the direct statement and
to the signed item-unit gaps. P2-D21's decision text and its reason 3 are amended above.
Every pre-existing value in `results/T5_inertness_ceiling.json` and
`results/T5_armb_floor.json` stays byte-identical.

---

## P2-D23. The `ext_i` floor is retained and does not reach the confirmatory set

**Status:** adopted. Rules the reach of a floor `v2.0` imported; does not change its
value and does not withdraw it. The confirmatory `n` stays 108.
**Decided:** 2026-09-13, by an **agent session acting on an author instruction**, in the
session that recorded P2-D22. No `F1` or `F2` statistic was computed. Full reasoning in
`PREREGISTRATION_v2.14.md`.

**The instruction it acted on**, per the countermeasure above, quoted in the parts that
bear on the ruling:

> The open question is whether that floor should apply to Arm B's confirmatory set,
> which would cut n below 108.
>
> An earlier session reported that none of the three quantities depends on ext_i: (a)
> reads chosen options only, (c) reads the sign of the margin difference, and ties in
> (c) use raw margins under P2-D19. If that holds, the floor governs mean and median
> Delta-A and v2.x's Delta-A null, none of which is confirmatory after P2-D6 replaced
> the mean with a sign test, and the confirmatory n stays 108.
>
> Verify each of those three claims against the current code and the current decisions,
> at the item unit adopted in P2-D20. The earlier report predates both P2-D19 and
> P2-D20 and may not survive them.
>
> DECIDE. Whether the floor applies to the confirmatory set, and what n it leaves. State
> which quantities it does govern and where it remains in force.

with the constraints: treat every number in the instruction as unverified including
`0.00134` and the `0.02` floor and recompute both; do not reopen P2-D6, P2-D19 or
P2-D20; no `F1`/`F2` statistic; and **if the floor turns out to bind on a confirmatory
quantity, say so and stop rather than choosing a remedy.** It does not bind, so no remedy
was reached for.

**Ordering, disclosed.** An earlier step printed the smallest `ext_i` in the confirmatory
set, and that number was known to this session before the ruling. **Which items fall below
the floor was not inspected**, the export CSV carrying `ext_i` per item was not opened for
that purpose, and the count of items below the floor was deliberately **not computed**, on
the reasoning that it is never needed: if the floor does not bind, the count is irrelevant,
and if it binds, the instruction requires stopping rather than sizing a remedy. The ruling
rests on the form of the quantities and not on how many items an exclusion would cost.

**Binds:** `src/inertness_ceiling.py`, and any script forming Arm B's confirmatory `n`.
**Constant:** `P2D23_TEXT`, `P2D23_FLOOR`, `P2D23_APPLIES_TO_CONFIRMATORY`,
`P2D23_CONFIRMATORY_N`, `P2D23_P1_SOURCE`, `P2D23_P1_EXPRESSION`,
`P2D23_MIN_EXT_CONFIRMATORY`, `P2D23_MAX_EXT_CONFIRMATORY`, `P2D23_GOVERNS`.

**Decision text.**

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

**The two numbers in the instruction, recomputed.** Both reproduce.

| carried | recomputed | source |
|---|---|---|
| floor `0.02` | **0.02** | `span > 0.02` in Paper 1's `src/frontier_position.py`, verified present |
| smallest `ext_i` `0.00134` | **0.001340028643** | `t6_f0_headroom.item_axis`, `size` confirmatory set |

`max ext_i` on the same set is 0.5123189453, and **no confirmatory item has
`ext_i <= 0`**. That last check is not decoration: the ruling rests on a strictly positive
denominator, and it is the one value of `ext_i` that would break it.

**Paper 1's source says what the floor is for, and it is narrower than a floor.** The
comment beside `span > 0.02` reads:

> A mean of per-item ratios is not usable here: the per-item S->B span goes near zero on
> some items and the ratio explodes, which produced values of -1 to -4 on a quantity
> bounded near [0, 1].

The floor is applied to `frac`, which feeds `sb_frac_median`. The other aggregate Paper 1
reports, `sb_frac_of_means`, forms no per-item ratio and takes no floor. So Paper 1 did not
exclude items from an analysis; it guarded **one aggregation form** and reported a second
form that does not need the guard.

`v2.0` section 3.2 imports it in exactly those terms: two aggregates are reported, the
median of per-item values and the value computed from the means, "following Paper 1's
handling of the same ratio pathology", and "the `ext_i >= 0.02` floor in section 6 is the
same guard, carried over".

**Where the literal reading comes from.** `v2.0` section 7.2's exclusion table then says
items with `ext_i < 0.02` are "excluded from the confirmatory Arm B analysis". Read today
that cuts `n`. Read at `v2.0`, the confirmatory Arm B analysis **was** the mean and median
of per-item `A`, so section 7.2 and section 3.2 said the same thing. P2-D6 replaced the
mean with a sign test and P2-D12 fixed the three quantities. The exclusion's wording stayed
still while the quantity it was written against moved out from under it.

**The three claims, verified against current code at P2-D20's unit.**

1. **"(a) reads chosen options only."** **Verified.** `src/c5_effect.py` contains no
   reference to `ext`, `item_axis`, `A[` or `marg_norm`; `c5_movement` pivots
   `chosen_option` and compares option labels. The same holds for **(b)**, which the
   instruction did not list and which is the same rate against `R_m`. In
   `src/inertness_ceiling.py`, `A` enters at exactly one line, inside the (c) path.
2. **"(c) reads the sign of the margin difference."** **Verified, with the mechanism
   stated precisely, because the code does not literally read margins.** (c) computes
   `sign(mean ΔA)` on `A`. `ext_i` is a strictly positive **per-item** constant, so both
   renderings of an item share one denominator and
   `mean ΔA = (sum of raw margin differences) / (2 ext_i)`. The sign is therefore the
   sign of the raw margin sum and cannot be changed by any positive denominator. The
   claim is true of the quantity; it is not true of the expression, and the difference is
   the whole reason it had to be checked rather than trusted.
3. **"Ties in (c) use raw margins under P2-D19."** **Does not survive as stated.** The
   zero test is `|mean ΔA| > EPS` on `A`, which is `ext_i`-scaled, not on raw margins.
   The claim predates P2-D20 and is false against the current code.

   **It does not change the conclusion, and the reason is measured rather than assumed.**
   `ext_i` lies in `(0, 0.5123]`, so dividing by it can only magnify `|ΔA|` relative to the
   raw margin difference, never shrink it; a genuine nonzero can therefore never be turned
   into a tie. The reverse risk is a sub-`EPS` float residue being magnified past `EPS`.
   Worst-case amplification is `1 / 0.00134 = 746`, and the observed raw-margin residues
   are of order `7.69e-17`, which magnified is about `5.7e-14`, still below
   `EPS = 1e-12`. Measured directly, the **smallest nonzero `|mean ΔA|` on the
   confirmatory set is 0.0272**, which is `2.7e10` times `EPS`. Nothing sits near the
   boundary, so no `ext_i` in this set can move an item across it.

**One open question from `v2.10` section 3.5, now answered.** That section recorded an `A`
versus `marg_norm` disagreement on `L3` under exact equality and said whether `EPS`
dissolves it was not computed. At P2-D20's item unit there is exactly **one** item where
`sign(mean ΔA)` and `sign(mean Δmarg_norm)` differ, and it is that class: one side is
exactly `0` and the other is a `7.69e-17` float residue. **Both are below `EPS`, so both
classify as a tie** and (c) is unaffected. Its `ext_i` is 0.0264, above the floor, so it is
not an `ext_i` pathology either. `EPS` dissolves it.

**The ruling.** The floor does not reach any confirmatory quantity, so it removes no item.
**The confirmatory `n` is 108.**

**Where the floor remains in force, unamended.** On every quantity that is a mean or median
of per-item `A`, which `v2.0` section 3.2 still specifies as reported aggregates; on `v2.0`
section 4.3's correlation between per-item `ΔA` and `ext_i`; and on the `ΔA` null reported
before P2-D6 replaced it. All of those are reported quantities, none is confirmatory, and
the floor is the right guard for each. **The floor is not withdrawn and its value is not
changed. What is ruled is its reach.**

**Alternatives offered and not chosen.**

1. **Apply the floor to the confirmatory set as `v2.0` section 7.2 reads literally.**
   Rejected. It would cut `n` to protect a ratio form that no confirmatory quantity has,
   on the one axis the design is already shortest of. Section 7.2's sentence is not a
   separate decision from section 3.2's; it is the same guard named at the place the
   exclusions are tabulated, and section 3.2 states what it guards.
2. **Withdraw the floor, since no confirmatory quantity needs it.** Rejected. The reported
   mean and median of per-item `A` still exist and still have the ratio form, and Paper 1
   measured that failure directly. Withdrawing a guard because the analysis moved away
   from the quantity it guards leaves it unguarded when a later section moves back.
3. **Lower the floor to a value the confirmatory set clears.** Rejected outright. It is
   choosing a threshold from the data it will be applied to, which is what the whole log
   exists to refuse, and it would be doing so to reach a predetermined `n`.

**Consequences.** `src/p2_decisions.py` carries `bind_ext_floor`, called by
`inertness_ceiling.main` with the run's minimum `ext_i`, its confirmatory `n`, and the list
of confirmatory quantities that read `ext_i`, which must be empty. The strictly-positive
check carries its reason rather than a range, per the note above on binding form: at
`ext_i = 0` the sign identity fails and the sign is undefined rather than large, and a
small `ext_i` is not the hazard. `check_p1_ext_floor_source` asserts `span > 0.02` is still
present in Paper 1's `src/frontier_position.py`, because Paper 1's decision log has no
entry for this floor and that expression with its comment is therefore the governing
record. No artifact value changes.

---

## P2-D24. The five downward departures license no claim about direction

**Status:** adopted. Rules what Arm B may conclude from quantity (c)'s resolving cells.
Changes no statistic, no unit, no tolerance and no null. `p0` is 0.5. P2-D5's blocker
stays open.
**Decided:** 2026-09-14, by an **agent session acting on an author instruction**, in the
session following the one that recorded P2-D23 and ran T7's switch-concentration check. No
new statistic was computed; every figure below is re-read from an existing artifact and
recomputed against it rather than transcribed. Full reasoning in
`PREREGISTRATION_v2.15.md`.

**The instruction it acted on**, per the countermeasure in `v2.10` section 2.4, quoted in
the parts that bear on the ruling:

> Quantity (a) clears P2-D13's floor on all 14 cells, 30 to 77 items of 108. Five cells
> resolve on (c) at the corrected alpha, all downward, meaning away from `o*_infinity`.
> Three inputs stand against reading those five as a result, and **none can be ruled
> alone**: P2-D5's blocker; the neutral baseline; the concentration.
>
> **What does the design license concluding from the five downward departures, given all
> three at once?** Ruling any one alone licenses a reading the other two forbid, which is
> why they come together.

with three readings offered **to evaluate, not to adopt**, listed under the alternatives
below, and the constraints: compute no new statistic; treat every number in the
instruction as unverified; do not move `p0`; do not reopen P2-D6, P2-D12, P2-D14, P2-D19,
P2-D20 or P2-D21; name any quantity a reading needs that was never computed and say
whether computing it now would be preregistered or post-hoc; and **if the design licenses
nothing about direction, say so**. All were followed.

**Binds:** `src/t7_armb.py`, and any Arm B report or paper passage stating what quantity
(c)'s departures mean.
**Constant:** `P2D24_TEXT`, `P2D24_DIRECTION_CLAIM_LICENSED`,
`P2D24_MOVEMENT_CLAIM_LICENSED`, `P2D24_RESOLVING_CELLS`,
`P2D24_RESOLVING_ALL_DOWNWARD`, `P2D24_NEUTRAL_RESOLVES_ON`,
`P2D24_CONCENTRATED_RESOLVING_CELLS`, `P2D24_CONCENTRATION_RATIO_RESOLVING`,
`P2D24_MARGINAL_NULL_COMPUTED`, `P2D24_MARGINAL_NULL_SPEC`.

**Decision text.**

> The five downward departures license NO claim about direction. Quantity (c) is
> reported as computed, nothing is withheld, and the five cells that resolve at the
> corrected `alpha` are reported as what they are: a sign proportion below `p0 = 0.5`
> on `CTRL`/F1, `L3`/F1, `L4`/F1, `L3`/F2 and `L4`/F2. No sentence reads that as
> movement away from `o*_infinity`, as evidence about adversary tracking, or as a
> property of a model. A direction claim needs three premises and none holds. First,
> P2-D5's second conjunct names a quantity the confirmatory family does not contain:
> `A_null(m, F) = sum_o p_{m,F}(o) A_i(o)` is `v2.0` section 3.3's object, and neither
> a same-option rate nor `p0 = 0.5` is that object. Second, a content-neutral insert
> departs downward too, on the one model whose own diagnostic resolves at the corrected
> `alpha`, which is `CTRL` and only `CTRL`, so downward departure is not established as
> a property of adversary content rather than of inserted text. Third, on three of the
> five resolving cells the coordinate discards the switches it cannot see at 1.81 to
> 4.09 times P2-D19's per-pair bound, and nothing establishes that the discarded
> switches carry the direction of the retained ones. The ruling does not depend on how
> P2-D5's blocker is later ruled: under all three readings in circulation the second
> and third premises still fail, so the blocker stays open and stays the author's. What
> IS licensed is movement. Quantity (a) reads chosen options only, carries no claim
> about adversary-relevant content, and clears P2-D13's floor of 7 on all 14 cells at
> 30 to 77 items of 108 against an exact null of zero. Quantity (b) resolves on three
> cells, all in the direction of the framing moving choices more than `c5` does, and on
> eleven it does not. Both are reported per cell, never as one magnitude word.

**Why it needed deciding.** T7's confirmatory run put a resolved, signed, one-directional
result on the table: five of fourteen cells depart from `p0` at the corrected `alpha` and
every one departs downward. That is the shape of a finding, and three separate records say
it cannot be read as one. Left unruled, the session writing the paper meets five
significant cells and three caveats scattered across a decision log, a preregistration
version and a diagnostic report, and the caveats lose, because a resolved `p` of 7.7e-06
is a louder object than a paragraph. The ruling exists to make the absence of a licence as
concrete as the presence of a `p` value.

**The three inputs are three views of one absence, which is why none could be ruled
alone.** `v2.0` section 4.4 preregistered the design's defence against the reading that
the movement is a generic inserted-text shift in option preference: the attribution cap
`dA_null(m, F)`, computed by reweighting the confirmatory set with the option-frequency
shift measured on the `beta_c = infinity` control set, where nothing adversary-relevant
can change. P2-D6 replaced the mean with a sign test and P2-D12 fixed three quantities,
and no successor to that cap was written. Input 1 is that absence stated as a rule, since
P2-D5 makes the excess conjunct binding and the confirmatory family contains no excess
quantity. Input 2 is the same absence with a measurement in it, since a content-neutral
insert in the same slot departs downward on the model where its diagnostic resolves. Input
3 is the same absence in the geometry, since 54 of the 62 discarded switches fall on one
option-index pair at the end of the option order, which is the signature a generic
option-position shift would have. Ruling any one alone licenses a reading the other two
forbid: retire the conjunct and input 2 makes the claim false on its face; read against the
neutral baseline and input 3 denies that the retained subset is representative; call the
concentration a limitation and inputs 1 and 2 still stand on the two cells it does not
touch.

**Three numbers in the instruction did not survive recomputation, and they are recorded
rather than adopted**, per `v2.10` section 3.6.

| carried | recomputed | verdict |
|---|---|---|
| `c5` departs downward where it resolves, `CTRL` 0.1951 and `L3` 0.2424 | `CTRL` resolves at `p` = 0.000112; **`L3` does not**, at `p` = 0.004551 against `alpha` = 0.002381 | **fails on `L3`** |
| **two** of the five resolving cells are concentrated | **three**: `CTRL`/F1, `L3`/F1, `L3`/F2. The parenthetical names three and calls them two | **fails as a count** |
| at **2 to 5** times the anticipated rate | **1.81 to 4.09** on those three cells; 1.81 to 5.10 is the range over all six concentrated cells, and 5.10 is `CTRL`/F2, which does not resolve | **fails as a range** |

The `L3` error is also in this file's own open-question note of 2026-09-14, which is where
the instruction's wording came from, and it is corrected there. It cuts both ways: the
evidence that inserted text departs downward is one model rather than two, and reading 2
is weaker still, because four of the five resolving cells are `L3` or `L4` and neither
model's neutral figure resolves. A resolved departure read against an unresolved point
estimate is the comparison P2-D22 refused in the tally case.

**Why this does not pre-empt P2-D5's blocker, which is the part that makes the ruling
possible.** Three readings of the blocker are in circulation. Under the first, the conjunct
travels and needs an operational form, which does not exist. Under the second, it expired
with the mean, which leaves the framing contrast but touches neither input 2 nor input 3.
Under the third, (a), (b) and (c) already satisfy it, which is false as stated, since
`A_null` is a marginal over canonical option ids weighted by `A` and a same-option rate is
a rate of unchanged choices. The direction claim fails under all three, so the blocker
stays open and stays the author's.

**The quantity a rejected reading needed, and its status.** `A_null(m, F)` is specified in
`v2.0` section 3.3 and `dA_null(m, F)` in `v2.0` section 4.4. Neither has ever been
computed for Paper 2: no module emits either, and `tv_option_marginal` in
`src/c5_effect.py` is a total variation distance between two option marginals, which is a
different object. Computing them as `v2.0` specifies them would be **preregistered**: both
formulas predate all Paper 2 data, both are named as required steps in
`docs/P2/tasks/T7.md`, and neither has a free parameter. Using either to license a
direction claim on quantity (c) would be **post-hoc**: no preregistered rule maps a level
excess in `A` units onto a sign-test proportion, P2-D5's conjunct and `v2.0` section 4's
criterion were both written against the mean P2-D6 demoted, and the mapping would be
written with the five cells and their directions already on the table. This entry
authorizes neither.

**Alternatives offered and not chosen.**

1. **H-B's null half is refuted by (a), and the paper reports movement without direction.** Partly adopted and rejected as stated. Its second and third
   clauses are the ruling. "Refuted" is declined on two grounds: it is a verdict on H-B,
   which the blocker blocks, and H-B is a conjunction whose second half is the direction
   half, so (a) resolves one half and reporting the whole as refuted invites the reader to
   complete it. "(c) says nothing interpretable" is declined in the other direction: (c) is
   exact, reproducible and reported in full, and what is unlicensed is one reading of its
   sign, not the statistic.
2. **Read the five departures against the measured neutral baseline, and state the concentration as a limitation on the affected cells.** Rejected on four grounds. The neutral figure resolves on
   `CTRL` alone and on none of the four `L3` or `L4` resolving cells, so on four of five
   cells it would read a resolved departure against an unresolved point estimate. It is
   the recalibration P2-D12 alternative 3, P2-D14 alternative 1 and P2-D21 alternative 1
   all declined, moved into the reporting, which is worse rather than better: moving `p0`
   would at least be a stated null at a stated `alpha`, and a reporting-level comparison
   has neither, while the ordering hazard is unchanged because it would be adopted with
   the resolving cells on screen. It miscounts the concentration as two cells and mislabels
   selection as a limitation, where `reports/T7_switch_concentration.md` says plainly that
   nothing establishes the discarded switches carry the direction of the retained ones. And
   it leaves input 1 unanswered, since it substitutes a different comparison object for
   `A_null` without saying why the substitution is valid.
3. **Withhold quantity (c)'s numbers until P2-D5's blocker is ruled.** Rejected. The numbers are not what is blocked, and
   `reports/T7_armb_quantities.md` section 6 already says so. Withholding a reproducible
   statistic because its interpretation is unsettled makes the record depend on a later
   ruling, which is the opposite of what a preregistration is for.

**Consequences.** `src/p2_decisions.py` carries `bind_direction_claim`, called by
`src/t7_armb.py`, which asserts the three premises a direction claim would need rather
than any range a proportion or ratio occupies: that no confirmatory quantity is an excess
over the marginal null, that the `c5` neutral diagnostic resolves on `CTRL` alone, and that
the direction of the discarded switches is not established. Each fires when a premise
becomes established, not when a value drifts, so the ruling is re-read rather than
inherited. `src/t7_armb.py` emits a `direction_reading_P2D24` block into
`results/T7_armb_quantities.json` and a section into `reports/T7_armb_quantities.md`, both
additive: every pre-existing key and value in the artifact is byte-identical, verified key
by key. `reports/T7_switch_concentration.md` replaces "2 to 5 times" with the range its own
table carries. `tests/test_p2d24_direction.py` fails if a resolving cell enters or leaves,
if a departure turns upward, if the neutral diagnostic resolves on a second model, if the
concentrated subset of resolving cells changes, or if a caller reports a direction claim.

**What this entry does not do.** It does not rule P2-D5's blocker, move `p0`, change a
unit, a tolerance, a null or a floor, or reopen P2-D6, P2-D12, P2-D14, P2-D19, P2-D20 or
P2-D21. It does not compute `A_null` or `dA_null` and does not authorize computing them
for this purpose. It does not touch the human-behaviour gap claim, whose wording
`docs/P2/tasks/T4.md` fixes and which is independent of everything Arm B measures.

---

## P2-D25. `A_null` and `ΔA_null` are computed and descriptive; no mapping onto quantity (c), and no successor cap

**Status:** adopted. Rules what the two preregistered marginal-null quantities may be
used for, before either has been computed. Changes no statistic, no unit, no tolerance,
no null and no family. `p0` is 0.5. The confirmatory family is 21 tests at
`alpha = 0.05/21`. P2-D5's blocker stays open and stays the author's.
**Decided:** 2026-09-14, by an **agent session acting on an author instruction**, in the
session following the one that recorded P2-D24. **No statistic was computed.** The
session read `v2.0`, the log, the two T7 reports and the modules, and recomputed nothing
from `data/raw_t7/`: no `A_null`, no `ΔA_null`, no control-set `TV`, no quantity on the
Arm B artifacts. One frozen, model-free property of Paper 1's rendering table was read
and is disclosed in `PREREGISTRATION_v2.16.md` section 6. Full reasoning in
`PREREGISTRATION_v2.16.md`.

**The instruction it acted on**, per the countermeasure in `v2.10` section 2.4, quoted in
the parts that bear on the ruling:

> You rule. **You compute nothing.**
>
> **With no number on the table, what may the computed quantities be used for and what
> may they not?** At minimum, all four:
>
> 1. Whether `A_null` and `ΔA_null` **enter the confirmatory family or are
>    descriptive**. Note that the confirmatory family is 21 tests and
>    `alpha = 0.05/21`; say what happens to that family under your ruling and whether
>    anything you authorize changes it.
> 2. Whether they **may be read against quantity (c) at all**, and if so **under what
>    preregistered mapping**, or whether **no mapping is authorized**.
> 3. What they **license about the generic-option-position-shift hypothesis** the (4,5)
>    signature favours.
> 4. Whether **a successor to section 4.4's cap is authorized**, or whether **the cap
>    stays orphaned and its absence stays the finding**.

with the note that

> A ruling made with the numbers visible is a different object from one made without,
> and the author split the sessions so that this one is made blind. If you find yourself
> wanting a number to decide, that wanting is the thing the split exists to prevent

and the constraints: do not reopen P2-D5, P2-D6, P2-D12, P2-D14, P2-D19, P2-D20, P2-D21
or P2-D24; do not move `p0`; treat every claim in the instruction as unverified and check
it against the record; and if the ruling makes the computation nearly worthless or leaves
the hypothesis unadjudicable, say so plainly rather than inflating what it licenses. All
were followed. Two claims in the instruction did not survive verification and are recorded
in the consequences below.

**Binds:** any script computing `A_null(m, F)` or `ΔA_null(m, F)`, any script computing
`TV(m, F)` on the `beta_c = infinity` control set, and any report or paper passage citing
one of the three.
**Constant:** `P2D25_TEXT`, `P2D25_IN_CONFIRMATORY_FAMILY`,
`P2D25_CONFIRMATORY_FAMILY_SIZE`, `P2D25_MAPPING_TO_QUANTITY_C`,
`P2D25_SUCCESSOR_CAP_AUTHORIZED`, `P2D25_CAP_APPLIES_TO`, `P2D25_CONTROL_TV_AUTHORIZED`,
`P2D25_CONTROL_TILE`, `P2D25_CONTROL_N`, `P2D25_CONTROL_N_ALL_TILES`,
`P2D25_CONFIRMATORY_ARITY`, `P2D25_MARGINAL_SUPPORT`,
`P2D25_MENU_POSITION_ADJUDICABLE`, `P2D25_CANONICAL_TAIL_IDS`,
`P2D25_EXT_FLOOR_IN_FORCE`.

**Decision text.**

> `A_null(m, F)` and `ΔA_null(m, F)` are computed as `v2.0` sections 3.3 and 4.4
> specify them, and they are DESCRIPTIVE. Neither enters the confirmatory family,
> which stays at 21 tests at `alpha = 0.05/21`. Neither was ever a test: `A_null` is
> a reference point in section 3.3's table and `ΔA_null` is a conjunct on section 4's
> criterion, and section 10 lists neither. For `ΔA_null` this restates rather than
> extends P2-D23, which already placed the `ΔA` null among the reported quantities and
> left the `ext_i >= 0.02` floor in force on it; `A_null` has the same ratio form and
> inherits the same floor, on its mean and on its median, under `v2.0` section 3.2's
> two aggregates. NO mapping from either onto quantity (c) is authorized and none may
> be written: (c) is a sign proportion, both are levels in `A` units, no preregistered
> rule connects them, and a rule written now would be written with all fourteen of
> (c)'s cells already published, so writing it blind to `A_null` would not make it
> blind. NO successor to section 4.4's cap is authorized, and the cap needs none. It
> caps mean `ΔA`, which P2-D6 demoted rather than deleted, so it follows its quantity
> down to descriptive and is applied unchanged to the quantity it was written for.
> P2-D6's mixture finding reaches both sides of that comparison, since `ΔA_null` is
> built from `mean_i A_i(o)`, and the cap is reported with that defect named. Arm B's
> confirmatory family therefore carries no defence against the generic-shift
> hypothesis and cannot acquire one. That is the finding and it is stated as one.
> `TV(m, F)` on the `beta_c = infinity` control set IS authorized and is descriptive,
> on section 4.4's first paragraph, whose ground is that any change in the choice
> distribution on adversary-robust items is prompt sensitivity. That ground is
> independent of the cap, of mean `ΔA` and of `A`, so P2-D6 and P2-D12 do not reach it
> and it survives them intact and unamended. The control base is the `size` tile's 142
> adversary-robust items, which is the base P2-D4 names and the only one whose option
> arity matches the set the cap reweights; the 540-item figure across all four tiles is
> reported beside it with its base named, never alone. Both quantities are marginals
> over CANONICAL option ids, so neither can adjudicate a menu-POSITION hypothesis, and
> the (4,5) signature is not evidence for one: `chosen_option` is a canonical id, Paper
> 1's Format V permutes the menu per item and per permutation, and canonical options 4
> and 5 fall in all six menu positions at near-uniform rates under both permutations.
> The hypothesis these quantities bear on is a shift in preference over canonical option
> CONTENT at the ends of the tile's ordinal scale, and they bear on it descriptively, at
> the level, never at the sign. The ruling holds whichever way P2-D5's blocker is later
> ruled, because nothing it authorizes is an excess quantity in the confirmatory family
> and nothing it authorizes reaches quantity (c).

**Why it needed deciding, and why it had to be decided before the numbers existed.**
P2-D24 named `A_null` and `ΔA_null` as preregistered-but-uncomputed and authorized
neither for the purpose it was ruling on. It did not say what else they may be used for,
and `docs/P2/tasks/T7.md` steps 4 and 5 both require them, so the next session was going
to compute two quantities with no standing. The hazard is specific and it is the one this
log keeps recording: a resolved level excess is a loud object, (c)'s five downward cells
are already published, and a session holding both at once would be writing the bridge
between them with both ends in view. Ruling first and computing second is what makes the
absence of a bridge a decision rather than an omission.

**What this session wanted a number for, and why it ruled without one.** Twice. First, on
question 4: whether the cap, run on the descriptive mean, would come out near the observed
mean `ΔA` or far from it decides how much the "nearly worthless" verdict costs, and it is
exactly the number the split forbids, because a cap that happened to be slack would make a
successor look unnecessary and a cap that happened to be binding would make one look
urgent. The ruling is made on the form of the quantities instead: the cap conditions a
level test, (c) is a sign test, and no arithmetic on either side changes that. Second, on
the control base: the count of `size`-tile adversary-robust items the `ext_i` floor would
reach is unknown here, and P2-D23 deliberately did not compute it. It is not needed, for
P2-D23's own reason: the floor governs a descriptive aggregate either way, and how many
items it removes changes the figure and not its standing.

**Alternatives offered and not chosen.**

1. **Admit `A_null` and `ΔA_null` to the confirmatory family.** Rejected on three
   grounds. Neither was ever a test: `v2.0` section 8.1 lists seven models by three
   contrasts and nothing else, and section 10's confirmatory list names the three
   contrasts "subject to section 4.4's attribution cap", which makes the cap a condition
   on a test and not a member of the family. Admitting them would move `alpha` for 21
   tests that were preregistered at `0.05/21`, which is P2-D6's family and is not
   reopened here. And a test admitted now is chosen after its neighbours are published,
   which is the ordering hazard P2-D12, P2-D21 and P2-D24 each declined in turn.
2. **Write a successor cap mapping the control-set reweighting onto quantity (c)'s sign proportion.** Rejected. P2-D24 already rules that use post-hoc and this entry does not
   reopen it. The further reason is the one the session split exists for and it defeats
   the obvious repair: a mapping written by a session that has not seen `A_null` is still
   written by a session that has seen all fourteen of (c)'s cells, so blindness on one end
   does not buy preregistration.
3. **Leave the cap orphaned and compute neither quantity.** Rejected. Both formulas
   predate all Paper 2 data, neither has a free parameter, both are named in T7's own
   brief, and `v2.0` section 4.2 requires the `F0` replication to be reported on excess
   over the marginal null. Declining unrun preregistered work because its licence turned
   out to be small converts a stated limitation into a silent one, which is the failure
   this log exists to surface. The computation is owed; the claim is not.
4. **Compute a marginal over rendered menu positions, so the (4,5) signature can be tested against a position-shaped cap.** Rejected twice over. It is a new preregistered
   quantity chosen after the signature was seen, which P2-D5 alternative 2 already
   rejected in the same shape. And it would be invented to test a hypothesis whose only
   evidence does not survive checking: the signature is on canonical ids, and canonical 4
   and 5 are spread across all six menu positions, so a menu-position preference would not
   produce it.

**Two claims did not survive verification, and they are recorded rather than adopted**,
per `v2.10` section 3.6.

| carried | checked | verdict |
|---|---|---|
| both formulas are "named required steps in `T7.md`" | step 5 names the marginal null explicitly; step 4 names the control analysis and its capping role but names neither `ΔA_null` nor its formula, which appear only in `v2.0` section 4.4 | **true of the steps, loose of `ΔA_null`** |
| the (4,5) signature is evidence for a generic option-POSITION shift | `chosen_option` is a canonical option id, not a menu position; `items_rendered.parquet` permutes the menu per item and per permutation, and canonical options 4 and 5 occupy all six menu positions at near-uniform rates under both | **fails**; the signature is on canonical ids and is not position evidence |

The second is the larger of the two and it is why question 3 could be answered at all. It
does not disturb P2-D24, whose third premise is that nothing establishes the discarded
switches carry the direction of the retained ones; that premise is about selection and is
untouched by what the concentration is a signature OF. What it does disturb is the
sentence in `reports/T7_switch_concentration.md` and in this file's own "(4,5) signature"
note, which read a canonical-id concentration as a menu-position one. Both are corrected
where they stand, dated, and the superseded reading is left legible.

**Consequences.** `src/p2_decisions.py` carries `bind_marginal_null_use`, which Session 2
calls before emitting either quantity. Per the binding-form note it asserts the premises
that make a use well formed and no range any value occupies: that neither quantity is in
the confirmatory family and the family is still 21 at `alpha = 0.05/21`; that the run
declares no mapping onto quantity (c); that no successor cap is claimed; that the control
marginal and the set the cap reweights share an option arity, without which the
reweighting is not defined; that the hypothesis a caller names the cap as adjudicating is
stated over canonical option ids; and that the `ext_i` floor P2-D23 left in force is
applied to the `A`-ratio aggregates. `tests/test_p2d25_marginal_null.py` fails if a caller
crosses any of those, and it recomputes the menu-position spread of canonical options 4
and 5 from Paper 1's frozen renderings rather than trusting the figure quoted here. The
scope registry's one unruled entry is NOT cleared: it covers the cap, `v2.0` section 4's
movement criterion and P2-D5's second conjunct, and the conjunct is the author's, so
`undefended()` keeps returning it and the hypothesis keeps reading as undefended, which is
the true state. A `partly_ruled_by` field records which half this entry answered. No
`results/*.json` value changes; no superseded preregistration version is edited.

**What this entry does not do.** It does not rule P2-D5's blocker, move `p0`, change a
unit, a tolerance, a null, a floor or a family, or reopen P2-D6, P2-D12, P2-D14, P2-D19,
P2-D20, P2-D21, P2-D23 or P2-D24. It computes no statistic of any kind. It does not
license any claim about direction, which P2-D24 rules and which nothing here reaches. It
does not touch the human-behaviour gap claim, whose wording `docs/P2/tasks/T4.md` fixes.

---

## P2-D26. P2-D5's blocker is discharged as permanently blocking, on a structural ground

**Status:** adopted. Discharges the blocker P2-D5 raised and every prior entry left open,
including the one the scope registry carried. Changes no statistic and no item set.
**Decided:** 2026-09-15, **by the author**, in writing, after `src/t7_control.py` measured
the coincidence under P2-D25. This session recorded the ruling; it did not make it. The
author's words are quoted below in full and the decision text is drawn from them, which is
the distinction P2-D16's correction exists to keep visible.

**The ruling, as the author wrote it:**

> On the size-tile confirmatory set, o*_infinity == o_fit on all 108 items. The 8 items
> where they differ are 3 on manmade and 5 on moves, none on size. So the adversary-aware
> optimum and the salience pole are the same option throughout the confirmatory set, and
> section 3.3's four references collapse to three there.
>
> P2-D5's blocker is discharged as permanently blocking, on a structural ground, not
> pending further measurement. No Arm B quantity computed on the confirmatory set can
> support a claim about adversary tracking, because the coordinate cannot distinguish
> adversary-aware behaviour from salience-driven behaviour when the two targets are the
> same point. No successor measure on size can, either.
>
> This is not a caveat to attach to a result. It is why the direction question was never
> answerable on this set, and it explains P2-D24's conclusion from the other side: P2-D24
> found the design licenses nothing about direction; this says why.
>
> The tile is not revisitable: D49 and D108 fixed size on measured grounds before this was
> known, and the 8 separating items sit on tiles those decisions excluded.

**Binds:** any Arm B analysis or reporting script, and any prose stating the confound.
**Constant:** `P2D26_TEXT`, `P2D26_BLOCKER_DISCHARGED`, `P2D26_DISCHARGE_IS_STRUCTURAL`,
`P2D26_ADVERSARY_TRACKING_CLAIM_AVAILABLE`, `P2D26_TILE_REVISITABLE`,
`P2D26_CONFIRMATORY_COINCIDENCE`, `P2D26_DIVERGENCE_COINCIDENCE`,
`P2D26_SEPARATING_ITEMS_BY_TILE`, `P2D26_CONFOUND_FIGURE_FOR_CONFIRMATORY`.

**Decision text.**

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

**The measurement it rests on.** Emitted by `src/t7_control.py` and reproduced
independently from `df["o_fit"]` and `t6_arm_a.arm_a_columns`, the path that produced
`results/T6_F0_headroom.json`'s `n_o_star_inf_equals_o_fit`:

| tile | divergent items | `o*_infinity == o_fit` | separating |
|---|---:|---:|---:|
| `hold` | 116 | 116 | 0 |
| `manmade` | 114 | 111 | **3** |
| `moves` | 122 | 117 | **5** |
| **`size`** | **108** | **108** | **0** |
| pooled | 460 | 452 | 8 |

**Discharged, not satisfied, and not still pending.** Those three are different states and
the log has used all three, so the difference is worth stating. P2-D5's conjunct is not
met: no Arm B quantity is an excess over the marginal null, and P2-D25 confirmed none may
be made into one. It is not pending either: nothing further could meet it, because the
obstacle is not in the measure. It is discharged, because **the claim the conjunct gated
is unavailable for a reason that precedes the conjunct.** A rule about how to support a
claim stops governing when the claim cannot be made at all.

**Why no successor measure on `size` helps, which is the part that makes this permanent.**
The confound is not a property of `A`. `A` pins `o*_0` at 0 and `o*_infinity` at 1, and on
this set `o*_infinity` IS `o_fit`, so a model at `A = 1` is at the salience pole and at the
adversary-aware optimum with one choice. Any measure built on the confirmatory item set
inherits that, because the two targets are the same option there and no function of a
chosen option can separate two labels attached to the same option. **The separation is
absent from the item set, not from the coordinate.**

**What P2-D24 and this entry say to each other.** P2-D24 ruled, from three inputs, that the
design licenses nothing about direction. This gives the reason: the direction question was
never answerable on this set. Neither supersedes the other, and P2-D24 is not weakened by
being explained. Its three premises were each independently sufficient and each remains
true; what changes is that a reader no longer has to hold three separate limits in mind to
see why the answer is what it is.

**What survives, and it is not nothing.** P2-D9's exact zero makes the movement claim
strong: quantity (a) clears P2-D13's floor on all 14 cells, 30 to 77 items of 108, against
a no-effect rate of exactly 1.0. **The framings changed the chosen option.** That claim
reads chosen options only, needs no direction, and is untouched by this entry. What Arm B
cannot say on this set is what the movement was toward.

**The confirmatory figure is 108 of 108, and never 452 of 460.** The latter is a
divergence-set figure. On the confirmatory set the confound is not overwhelming but total,
and citing the divergence-set number where the confirmatory set governs understates it.
`bind_adversary_tracking_claim` refuses a caller that cites it.

**Alternatives the record left open, and what closes them.** None was offered to the
author; these are the readings the record itself carried and the ruling forecloses.

1. **Discharge the blocker as satisfied, by treating a framing contrast as an excess.**
   Closed, and now moot. It was the reading P2-D24 declined and P2-D25 refused to
   authorize. Even had it been adopted, a satisfied conjunct would not make a tracking
   claim available when the two targets are one option, so the question it answers is no
   longer live.
2. **Hold the blocker open pending a successor measure on `size`.** Closed. The obstacle
   is in the item set and not in the measure, so no successor on `size` can lift it.
   Holding it open would promise a resolution the design cannot deliver, which is worse
   than a blocker because it reads as temporary.
3. **Revisit the tile so the 8 separating items enter the confirmatory set.** Closed on
   three independent grounds. D49 selected `size` on `fit_cost` coverage and D108 confirmed
   the curve rests on it alone, both before this was known. The 8 separating items are on
   `manmade` and `moves`, the tiles D108 found carry approximately nothing. And it would be
   a frozen-artifact change, which `CLAUDE.md` forbids.

**Consequences.** `p2_decisions.bind_adversary_tracking_claim` asserts the premise the
discharge rests on rather than a range: that `o*_infinity == o_fit` on ALL 108 confirmatory
items. If an item set ever separates them the assert fires and P2-D26 is re-read, because a
partial coincidence is a different case this ruling does not cover. It also refuses a caller
that cites 452 of 460 as the confirmatory confound. The scope registry entry that carried
P2-D5's conjunct is now `ruled_by` P2-D25 and P2-D26, so `scope_audit()` and `undefended()`
both return empty; the `defends_against` hypothesis is discharged with it, **not because the
defence was restored but because the claim it protected is unavailable.**

---

## P2-D27. A control-set change rate is a new quantity, authorized now as exploratory, side by side with (a) and nothing beyond

**Status:** adopted. Rules the standing of one quantity **before it has been computed**.
Changes no statistic, no unit, no tolerance, no null, no floor and no family. `p0` is 0.5.
The confirmatory family is 21 tests at `alpha = 0.05/21`. The confirmatory `n` is 108.
**Decided:** 2026-09-21, by an **agent session acting on an author instruction**, in its
own worktree, after P2-D26 and the results outline were on `main` at `17a7f41`. **No
statistic was computed.** The session ran no analysis `main()`, did not call `c5_movement`
on the control set, and read nothing on `data/raw_t7/`. Full reasoning in
`PREREGISTRATION_v2.19.md`.

**The instruction it acted on**, per the countermeasure in `v2.10` section 2.4, quoted in
the parts that bear on the ruling:

> You rule. **You compute nothing.**
>
> Quantity (a) is a change rate: the share of rendering pairs whose chosen option differs
> between a framing and `F0`, on the 108 confirmatory items, formed by
> `c5_effect.c5_movement` with P2-D16's pairwise exclusion and P2-D8's cluster bootstrap.
> The 142-item `beta_c = infinity` control on the `size` tile is reported in **TV** under
> P2-D25, in `results/T7_control_marginal_null.json`. The two are in different units, so a
> reader cannot compare them, and the control is what bounds what (a) means.
>
> **Rule: is a change rate on the 142-item control set, formed with quantity (a)'s own
> instrument, preregistered work under T7 step 4, or is it a new quantity P2-D25 did not
> authorize?**
>
> The author's read is that it is preregistered. **Evaluate that, do not adopt it.** Rule it
> on the record.
>
> It is not adversary-relevant in any way P2-D26 blocks: `A` is undefined on the control set
> and (a)'s instrument never reads `A`. Say whether you agree with that too, rather than
> taking it.

with the constraints: compute nothing, and in particular not the control change rate; do
not reopen P2-D5, P2-D6, P2-D12, P2-D24, P2-D25 or P2-D26; do not edit
`docs/P2/RESULTS_OUTLINE.md` or anything in `results/`; treat every claim in the
instruction as unverified. All were followed. The author's read was evaluated and **is not
adopted**; the second claim is agreed, with a refinement.

**Binds:** any script computing a change rate on the `beta_c = infinity` control set, and
any report or paper passage placing it beside quantity (a).
**Constant:** `P2D27_TEXT`, `P2D27_PREREGISTERED`, `P2D27_P2D25_ADDRESSED`,
`P2D27_AUTHORIZED`, `P2D27_STANDING`, `P2D27_IN_CONFIRMATORY_FAMILY`, `P2D27_INSTRUMENT`,
`P2D27_CONTRAST`, `P2D27_ARMS`, `P2D27_CONTROL_TILE`, `P2D27_CONTROL_N`,
`P2D27_ALL_TILES_AUTHORIZED`, `P2D27_FLOOR_APPLIED`, `P2D27_FIELDS`,
`P2D27_COMPARISON`, `P2D27_DERIVED_AUTHORIZED`.

**Decision text.**

> A change rate on the `beta_c = infinity` control set is NOT preregistered work under
> T7 step 4. Step 4 names movement and its role and names no instrument and no unit, and
> it was written on 2026-09-09, before P2-D12 made quantity (a) a change rate, so its
> word "movement" cannot carry (a)'s instrument. The preregistration that operationalizes
> step 4 is `v2.0` section 4.4, and it names one control measure, `TV`. P2-D12 scopes (a)
> to the confirmatory `n`. P2-D25 authorized `TV` and is SILENT on a change rate: it
> neither declined nor authorized one, and `steps_not_run` in
> `results/T7_control_marginal_null.json` records the computing session's reading of that
> silence under its own instruction, not a ruling. The control change rate is therefore a
> NEW quantity. It is AUTHORIZED NOW, as EXPLORATORY under `v2.0` section 10 and
> descriptive, because its instrument is fixed by existing decisions and by matching (a)
> cell for cell, and leaves no choice that could be fitted to its value:
> `c5_effect.c5_movement` with `col = "framing"` and `base = "F0"`, per model, for `F1`
> and `F2`, on the `size` tile's 142 adversary-robust items only, with P2-D16's pairwise
> exclusion, and with P2-D8's cluster bootstrap interval emitted as (a) emits it and
> carrying no inferential role, as P2-D13 left it in (a). The rate is reported with its
> item count beside it, as (a) is. P2-D13's floor is not applied and no verdict flag is
> emitted, because the floor exists for (a)'s inertness verdict and no verdict on the
> control is authorized. It does not enter the confirmatory family, which stays 21 tests
> at `alpha = 0.05/21`. The comparison it licenses is SIDE BY SIDE, per cell, in the same
> units, and nothing beyond: no difference, ratio, attributable share or test of (a)
> against the control rate is authorized. Each would be a new quantity written with (a)
> published and with the control's `TV`, which bounds its rate from below, in view, so it
> would be post-hoc; each would need a rule transferring a rate across two disjoint item
> sets that differ by construction, which no version writes; and a share of (a) read as
> adversary-attributable is a claim about adversary content on the confirmatory set, which
> P2-D26 makes unavailable.

**Why the author's read does not survive the record.** It has one strong form: after
P2-D12, "movement" in Arm B means quantity (a), since P2-D12 says H-B's no-movement half
"resolves on (a)", so step 4's "there should be NO movement there" names (a)'s instrument
applied to the control. Three things defeat it.

1. **Step 4 predates the vocabulary it would need.** The sentence "caps how much of the
   divergence-set effect you can attribute" entered `docs/P2/tasks/T7.md` in `13bb803` on
   2026-09-09. P2-D12 was decided on 2026-09-10 (`3233c02`). Reading "movement" as (a)'s
   instrument reads a later decision back into an earlier sentence, which is the scope
   expiry of cases 4 and 5 run in reverse: not a scope left behind by a moving quantity,
   but a scope extended to a quantity that did not exist when it was written.
2. **The preregistration that operationalized step 4 chose, and chose one.** `v2.0`
   section 4.4: "Because `A` is undefined on the control set, the control measure is the
   total variation distance". Singular, with its reason. A task brief's generic word does
   not preregister an instrument when the preregistration names a different one.
3. **P2-D12 is scoped to the confirmatory set**: "(a) INERTNESS: the same-option change
   rate against zero, per model, on the full confirmatory `n`". Nothing in P2-D8, P2-D12,
   P2-D13 or P2-D16 names the control set.

What the author's read gets right, and it is why this entry authorizes rather than
declines: `v2.0` section 4.4's **reason** for a separate control measure was that the
confirmatory measure, mean `ΔA`, needs `A` and `A` is undefined on the control. P2-D12
replaced the confirmatory measure with one that reads chosen options only, so that reason
no longer excludes running the confirmatory instrument on the control. That makes the
change rate admissible and motivated **by the record rather than by the values**. It does
not make it preregistered.

**What P2-D25 actually said about a control change rate: nothing.** Its decision text, its
four rejected alternatives, `v2.16` in full and `P2D25_TEXT` contain no mention of a change
rate or a same-option rate on the control. It did not decline one, it did not authorize
one, it did not address one. The `steps_not_run.step_4_control_change_rate` field reads
"P2-D25 does not authorize it ... Compute no quantity P2-D25 did not authorize", and
`v2.17` sections 3.6 and 7.1 give its provenance: the computing session applied **its own
instruction** to P2-D25's silence and flagged the gap as the author's. That was the
correct reading of silence under that instruction, and it is not a ruling in P2-D25's text.
The results outline's "not computed, under P2-D25" compresses the two; the outline session
should re-cite to this entry.

**The second claim in the instruction, agreed with a refinement.** `c5_movement` reads
`chosen_option` through `tie_reference.pair_frame` and nothing else; `A`, `ext_i` and
`marg_norm` appear in neither function, which P2-D23's first verified claim already
recorded. And `A` is undefined on the control set by `v2.0` section 3.2. So the rate
carries nothing P2-D26 blocks. The refinement is that P2-D26 is scoped to quantities
"computed on that set", the confirmatory set, and the control set is outside it entirely;
the rate does not need P2-D26's permission. **What P2-D26 does reach is the derived
quantities**: a difference or share of (a) read as the part the adversary explains is an
adversary-tracking claim about the confirmatory set, and P2-D26 makes that unavailable on
a ground no successor measure lifts.

**Ordering, disclosed**, as P2-D23 disclosed what it knew before its ruling. Known to this
session when it ruled, because it is on `main`: all fourteen cells of quantities (a), (b)
and (c), including (a) at 30 to 77 items of 108; the control `TV` on the 142 at 0.0176 to
0.2782 and on the 540; the cap, `A_null`, and P2-D26. Read in this session beyond the
documents: the key list, the `control_bases` block and the `steps_not_run` block of
`results/T7_control_marginal_null.json`, the set names in `results/T5_c5_effect.json`, and
`CTRL|F1`'s control rendering counts, 284 and 284.
**Not known: the control change rate on any cell.** One thing about it IS known, and it is
disclosed because it means this ruling is not fully blind: for paired renderings, the total
variation between the two empirical marginals is at most the share of pairs whose choice
differs, so on every cell whose `TV` was formed on the same surviving renderings the pairs
use, the control's rendering-level change rate is **at least** that cell's `TV`. The
session did not compute an upper bound, a value, or any item-level figure. The ruling does
not turn on the value anywhere: nothing it authorizes reads the value, no derived quantity
is authorized, and no verdict is attached.

**What this session wanted a number for.** Whether the control rate sits near (a)'s or far
below it. Near would make a share look like the natural summary; far would make the
side-by-side look like support for (a). Both are the pull toward a derived quantity chosen
with its value in view, and the ruling forbids every derived quantity for that reason.

**Why it needed deciding.** The outline carries (a) as a change rate and the control as a
`TV`, and a reader cannot put them side by side. Left unruled, a computing session either
computes the rate on the strength of step 4's word "movement", which the record does not
support, or declines it on the strength of P2-D25's silence, which is not a ruling either.
Both would be resolving an ambiguity by choosing.

**Alternatives offered and not chosen.**

1. **Rule the control change rate preregistered under T7 step 4.** Rejected on the three
   grounds above: step 4 names no instrument and predates the one it would need, `v2.0`
   section 4.4 names `TV` and only `TV`, and P2-D12 is scoped to the confirmatory `n`.
   Calling it preregistered would also license confirmatory-register language about it,
   which `v2.0` section 10 forbids for a quantity requested after the data.
2. **Leave it uncomputed and state the control in `TV` only.** Rejected. It leaves the
   outline with two numbers a reader cannot compare, and it leaves open the gap `v2.17`
   section 7.1 recorded: `TV` near zero is consistent with heavy churn, so `TV` alone
   understates control movement in the one sentence step 4 exists to support. The
   quantity has no free parameter once matched to (a), so declining it buys no protection
   that the side-by-side restriction does not already buy.
3. **Authorize the rate together with a difference, ratio or attributable share against quantity (a).** Rejected. Each is a new quantity written with (a) published and a lower
   bound on the control rate in view; each needs an unwritten rule transferring a rate
   between two disjoint item sets that differ by construction in whether the adversary can
   move the optimum; `v2.16` section 5.4 already rules that the control "can show that
   generic movement exists" and "cannot adjudicate whether the confirmatory movement is
   that movement"; and a share read as adversary-attributable is what P2-D26 makes
   unavailable.
4. **Apply P2-D13's floor to the control and emit a verdict flag.** Rejected. P2-D13's
   floor is the numerical convention for (a)'s inertness verdict on the confirmatory set.
   The control has its own preregistered expectation, step 4's "NO movement", and `v2.17`
   already reports it failed on `TV`. A floor verdict on the change rate would be a second
   verdict on the same expectation in a new instrument, chosen after the first was seen.
5. **Report the change rate on the 540-item all-tile base beside the 142.** Rejected. The
   side-by-side target is (a) on the `size` tile, and the 142 share its tile, arity and
   menus. A 540-item rate mixes arities 3, 3, 4 and 6, whose chance switching rates differ,
   so it is comparable to (a) in neither direction. P2-D25's 540 was a reporting
   requirement on `TV`, and it does not travel.

**Consequences.** The computing session calls `p2_decisions.bind_control_change_rate`
before emitting anything, and forms the rate exactly as `PREREGISTRATION_v2.19.md` section
5 specifies, into a NEW artifact, `results/T7_control_change_rate.json`, so every existing
`results/*.json` stays byte-identical. `results/T7_control_marginal_null.json`, including
its `steps_not_run` text, is not edited: it records truthfully what P2-D25 authorized.
`tests/test_p2d27_control_change_rate.py` fails if a caller crosses any premise. The
outline's "Needed and absent" entry for this quantity is updated by the outline session
after merge, with the sentence in `v2.19` section 7.

**What this entry does not do.** It computes no statistic. It does not reopen P2-D5,
P2-D6, P2-D12, P2-D24, P2-D25 or P2-D26, change `p0`, the family, `alpha`, the floor or
`n`, or license any claim about direction or adversary tracking.

---

## P2-D28. Tolerance-determined divergent items stay in `D(infinity)` and are disclosed beside the pool existence rate

**Status:** adopted. **Author ruling.** Changes no statistic, no item set, no `n`, no
`beta_c` value of record, and no definition.
**Decided:** 2026-09-22, by the author, after `PREREGISTRATION_v2.21.md` recorded the
items for the author and did not rule them. Recorded by an agent session. The counts
below are the ones `src/crossing_tolerance.py` emits, not the ones in the instruction
(section "Corrections" below). Full record in `PREREGISTRATION_v2.22.md` section 2.

**The instruction it acted on**, per the countermeasure in `v2.10` section 2.4, quoted in
the parts that bear on the ruling:

> Keep section 6.2's tie-broken argmax as the definition of divergence. It is
> preregistered and predates all data; excluding these items would redefine divergence
> after seeing where the definition bites. Disclose instead: count the 136 pool items
> whose beta_c is set by the D51 band, and the 99 that are divergent only by tie-break,
> beside the pool existence rate; state that all have beta_c between 17.3 and 23.4, above
> the grid endpoint, so |D(8)| and every grid-rate figure is unaffected and only
> |D(infinity)| includes them; report how many of the 2,748 separating items fall among
> them; state that the frozen 1,000 contains none, so no confirmatory claim is touched.

**Binds:** any pool-base figure that includes `D(infinity)`, and any report or paper
passage stating the pool existence rate.
**Constant:** `P2D28_TEXT`, `P2D28_EXCLUDED`, `P2D28_N_TOLERANCE_DETERMINED`,
`P2D28_N_DIVERGENT_ONLY_BY_TIE_BREAK`, `P2D28_N_SEPARATING_AMONG`,
`P2D28_N_FROZEN`, `P2D28_DISCLOSURE_FIELDS`.

**Decision text.**

> Spec section 6.2's tie-broken argmax stays the definition of divergence, and the pool
> items whose `beta_c` is set by D51's band stay in `D(infinity)`. They are 136 pool items,
> and all 136 are divergent only by tie-break: the tie-broken winner never leads `o*_0`
> beyond the band at any `beta`, and no other rival does either. They are disclosed beside
> the pool existence rate, never omitted, with four facts: the count; that every one has
> `beta_c` between 17.35 and 23.45, above the reporting grid's endpoint of 8, so `|D(8)|`
> and every grid-rate figure are unaffected and only `|D(infinity)|` includes them; that
> none of the 2,748 separating items is among them; and that the frozen 1,000 contains
> none, so no confirmatory claim is touched.

**Why.** The definition is preregistered and predates all data. Excluding the items would
redefine divergence after seeing where the definition bites, which is the move `CLAUDE.md`
names as tuning toward a result. Disclosure leaves the definition fixed and lets a reader
see how much of `|D(infinity)|` rests on the tolerance: 136 of 36,464.

**Corrections to the instruction, none of which changes the ruling.** The instruction's
"99 that are divergent only by tie-break" repeats `PREREGISTRATION_v2.21.md` section 8,
which was wrong. The 99 is the number the exact-test closed form classed robust. The other
37 had a closed-form root, but `src/crossing_tolerance.py` shows each is a parallel pair
with a rounding-size coefficient of `x` (at most 2.1e-17) and a real numerator, so the
root is spurious and no rival strictly overtakes on those 37 either. All 136 are divergent
only by tie-break. The instruction's range "17.3 and 23.4" is the emitted range truncated.

**Alternatives offered and not chosen.**

1. **Exclude the tolerance-determined items from the divergence set.** Rejected by the
   author: it redefines divergence after the data showed where the definition bites.
2. **Report the pool existence rate without the disclosure.** Rejected: the rate would
   then carry 136 items whose membership is a property of D51's tolerance, and a reader
   could not see it.

**Consequences.** `p2_decisions.bind_tolerance_determined_disclosure` asserts the
premises from `results/T1_crossing_tolerance.json`. It checks that the items are still in
`D(infinity)`, lie above the grid endpoint, include no separating item, and do not occur
in the frozen 1,000. It returns the four disclosure fields, and
`tests/test_crossing_tolerance.py` calls it. `docs/P2/RESULTS_OUTLINE.md` section 1.5
carries the disclosure.

**What this entry does not do.** It does not change section 6.2, `beta_c`'s value of
record, any grid rate, any confirmatory figure, or Arm C's standing.

---

## P2-D29. The closed form reads spec 6.3's zero coefficient of `x` at `EPS_TIE`, set inside an empty gap

**Status:** adopted. Changes the closed-form cross-check only. The bisected `beta_c`
remains the value of record, and no statistic, item set or `n` moves.
**Decided:** 2026-09-22, by an **agent session acting on an author instruction**. The
instruction was conditional: it said to set the threshold only if an empty gap exists.
Full record in `PREREGISTRATION_v2.22.md` section 3.

**The instruction it acted on**, quoted in the parts that bear on the decision:

> Measure the crossing coefficients on genuinely crossing pairs. If an empty gap
> separates them from the noise-level coefficients (at most 1e-15 on the numerator,
> 2.1e-17 on the denominator), set the parallel-case threshold inside it, by the same
> method P2-D19 used. If no empty gap exists, do not set one and report that. Then record
> the cross-check's expected residual. [...] Assert that the residual disagreement set
> equals that set.

**Binds:** `src/adversary.py:_crossings` and `bisection_vs_closed_form`, through
`adversary.PARALLEL_TOL`.
**Constant:** `P2D29_TEXT`, `P2D29_PARALLEL_TOL`, `P2D29_TESTED_COEFFICIENT`.

**Decision text.**

> `adversary._crossings` treats a rival as never overtaking when the coefficient of `x`
> in its crossing equation has magnitude at most `PARALLEL_TOL = 1e-12`, which is
> `EPS_TIE`, the spec's inherited absolute tie tolerance, not a new constant. The test
> is on the coefficient of `x` alone, because spec section 6.3's degenerate case is that
> coefficient being zero, in both its parallel and its identical form. On the 200,000
> pool every root pair whose curves are identical or only converge has that coefficient
> at most 3.5e-17, and every pair that crosses strictly has it at least 7.3e-8, so every
> tolerance inside that interval classifies identically. With it, the closed form
> disagrees with bisection on exactly the 136 tolerance-determined items of P2-D28 and on
> no other item. That residual is the cross-check's expected state, because the closed
> form tests strict crossing and cannot see a tie-break flip, and it is asserted as an
> invariant.

**Why the coefficient of `x` and not both coefficients.** `v2.21` section 7 proposed
treating a pair as identical when both coefficients are small, and the instruction quotes
both noise levels. Measured, that rule removes the 62 spurious roots on identical curves.
It leaves 37 spurious roots on parallel curves, where the numerator is real (at least
3.4e-3) and only the coefficient of `x` is rounding residue. Those 37 are tolerance-
determined items too, so the residual invariant would hold under either rule. But the
both-coefficients rule would leave the closed form reporting 37 roots that are not roots.
The spec's degenerate test names the coefficient of `x`, and the measured gap on it is
nine orders wide.

**Why `EPS_TIE`, by P2-D19's method.** The gap from 3.5e-17 to 7.3e-8 contains `1e-12`.
Writing down the inherited constant inside the gap is the choice P2-D19 made for `A`'s
tolerance. On the numerator the gap runs from 1.0e-15 to 4.8e-4, and on the larger of the
two coefficients it is the same interval. The frozen 1,000 has no pair below either gap,
so the fix changes nothing there.

**Alternatives offered and not chosen.**

1. **Both-coefficients rule, as `v2.21` section 7 proposed.** Rejected: it leaves 37
   spurious parallel-case roots in place.
2. **Keep the exact `den != 0` test and report the disagreement as unresolved.** Rejected:
   the empty gap exists, and the instruction said to set the threshold when it does.

**Consequences.** `src/beta_c_crosscheck.py` and `src/beta_c_disagreement.py` pass
`parallel_tol=0.0` explicitly, so `results/T1_beta_c_crosscheck.json` and
`results/T1_beta_c_disagreement.json` reproduce byte-identical as the pre-fix record.
`results/T1_crossing_tolerance.json` is the new artifact. `p2_decisions.bind_parallel_tol`
asserts that the constant still sits in the gap on both bases and that the residual still
equals the tolerance-determined set.

**What this entry does not do.** It does not change bisection, `beta_c`'s value of record,
D51's band, or any figure computed from the bisected value.

---

## Standing checks

| check | where |
|---|---|
| `src/framings.py` renders with `P2D1_VARIANT`, asserted at import | `p2_decisions.bind` |
| `src/framings.py` splices at `P2D2_SLOT_ANCHOR`, asserted at import | `p2_decisions.bind` |
| Framing ids are exactly `F0`, `F1`, `F2`, with no variant axis | `p2_decisions.bind` |
| The constants still match the decision text in this file | `p2_decisions.check_log` |
| A change to either constant fails the suite | `tests/test_framings.py` |
| A tied rendering is excluded at the pair, never imputed | `p2_decisions.bind_tie_exclusion` |
| Per-cell tie attrition is reported beside every Arm B quantity | `p2_decisions.bind_tie_exclusion` |
| `A`-tie tolerance is Paper 1's `EPS`, and the figures it gives | `p2_decisions.bind_a_tie_tolerance` |
| The gap the tolerance sits in still exists | `tie_reference.demo` |
| Quantity (c)'s `n_eff` is formed at the item, with P2-D19's `EPS` | `p2_decisions.bind_quantity_c_unit` |
| The two superseded `n_eff` readings still reproduce `v2.7` | `tests/test_armb_binding.py` |
| Exact-equality `a_invisibility` still emits 50 pairs on 48 items | `tests/test_armb_binding.py` |
| `p0` is 0.5 and the "all seven" claim is not re-asserted | `p2_decisions.bind_neutral_baseline` |
| The item-unit Type II gap is negative on exactly `B2` | `p2_decisions.bind_neutral_baseline` |
| `B2`'s 95% interval still contains 0.5, so 0.5556 is not drift | `armb_floor.demo`, `tests/test_armb_binding.py` |
| The pair-unit gaps and P2-D15's restatement still reproduce | `armb_floor.demo`, `tests/test_armb_binding.py` |
| No live statement uses a tally frame or "conservative" for `p0` | `p2_decisions.bind_neutral_claim_wording` |
| `B2` is exactly 0.5 under aggregations A, B and E | `p2_decisions.bind_neutral_claim_wording` |
| An assert carries the reason a quantity has its sign, not just a range | the mechanism note above |
| `ext_i > 0` on every confirmatory item, and no confirmatory quantity reads it | `p2_decisions.bind_ext_floor` |
| No caller reports a direction claim on quantity (c) | `p2_decisions.bind_direction_claim` |
| No confirmatory quantity is an excess over the marginal null | `p2_decisions.bind_direction_claim` |
| The `c5` neutral diagnostic still resolves on `CTRL` alone | `p2_decisions.bind_direction_claim`, `tests/test_p2d24_direction.py` |
| The five resolving cells and their downward sign still reproduce | `tests/test_p2d24_direction.py` |
| Paper 1's `span > 0.02` is still the floor's governing record | `p2_decisions.check_p1_ext_floor_source` |
| `o*_infinity == o_fit` on all 108 confirmatory items, the premise P2-D26 rests on | `p2_decisions.bind_adversary_tracking_claim` |
| No caller reports an adversary-tracking claim, or cites 452 of 460 for the confirmatory set | `p2_decisions.bind_adversary_tracking_claim` |
| No prereg passage is scoped to a replaced quantity without a ruling | `p2_decisions.scope_audit` |
| A binding asserts a premise, not a range the quantity occupies | the binding note above |
| `A_null` and `ΔA_null` are descriptive; the family stays 21 at 0.05/21 | `p2_decisions.bind_marginal_null_use` |
| No caller maps either onto quantity (c), and no successor cap is claimed | `p2_decisions.bind_marginal_null_use` |
| The control marginal and the set the cap reweights share an option arity | `p2_decisions.bind_marginal_null_use` |
| No caller reads the cap as adjudicating a menu-position hypothesis | `p2_decisions.bind_marginal_null_use` |
| Canonical options 4 and 5 are not at the end of the rendered menu | `tests/test_p2d25_marginal_null.py` |
| A control change rate runs (a)'s instrument, on the 142, for `F1` and `F2` only | `p2_decisions.bind_control_change_rate` |
| No verdict flag, floor or derived quantity is emitted beside it | `p2_decisions.bind_control_change_rate` |
| `c5_movement` reads chosen options only, never `A` | `tests/test_p2d27_control_change_rate.py` |
| Tolerance-determined items stay in `D(infinity)`, above the grid, none separating, none frozen | `p2_decisions.bind_tolerance_determined_disclosure` |
| The parallel-case tolerance still sits in the empty gap on both bases | `p2_decisions.bind_parallel_tol` |
| After the fix, the cross-check disagrees on exactly the tolerance-determined set | `p2_decisions.bind_parallel_tol`, `tests/test_crossing_tolerance.py` |
