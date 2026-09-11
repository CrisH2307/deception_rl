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

**The mechanism, which is the point of writing this down.** An artifact that looks
authoritative is cheaper to read than the record that is authoritative, and nothing
in the reading distinguishes them. Both cases were a correct-looking read of a file
whose standing was assumed rather than traced. Plausibility is not provenance, and an
agent working from a task list has no reason to check which it has, because the wrong
source answers the question just as fluently as the right one.

The countermeasure is not vigilance. It is that the governing record and the artifact
are bound mechanically, so a mismatch fails at import rather than being noticed. That
is what D100 does for Paper 1 and what `src/p2_decisions.py` does here.

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

**Status:** adopted. Supersedes P2-D11 and P2-D8's gating role.
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

## Standing checks

| check | where |
|---|---|
| `src/framings.py` renders with `P2D1_VARIANT`, asserted at import | `p2_decisions.bind` |
| `src/framings.py` splices at `P2D2_SLOT_ANCHOR`, asserted at import | `p2_decisions.bind` |
| Framing ids are exactly `F0`, `F1`, `F2`, with no variant axis | `p2_decisions.bind` |
| The constants still match the decision text in this file | `p2_decisions.check_log` |
| A change to either constant fails the suite | `tests/test_framings.py` |
