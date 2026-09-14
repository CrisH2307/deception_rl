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

**Status:** adopted.
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

**Why it needed deciding.** `A` is near-trichotomous: 470 option-cells at exactly 0,
439 at exactly 1, and 841 off-pole at median `-3.329`, unbounded below because `A`
divides by `ext_i`. Off-pole is the common case, not a tail. Over the 6,048 admissible
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
> coordinate Paper 1 never used. The empirical gloss is restated per model rather
> than universally: `p0 = 0.5` is conservative on six models, and on `B2` it is not
> established either way, since 0.5556 on `n_eff` 36 carries `p = 0.6177` and a 95%
> exact interval of [0.3810, 0.7206]. Two clauses that reverse on `B2` are withdrawn
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
