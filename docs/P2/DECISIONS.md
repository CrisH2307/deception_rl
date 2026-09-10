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

## Standing checks

| check | where |
|---|---|
| `src/framings.py` renders with `P2D1_VARIANT`, asserted at import | `p2_decisions.bind` |
| `src/framings.py` splices at `P2D2_SLOT_ANCHOR`, asserted at import | `p2_decisions.bind` |
| Framing ids are exactly `F0`, `F1`, `F2`, with no variant axis | `p2_decisions.bind` |
| The constants still match the decision text in this file | `p2_decisions.check_log` |
| A change to either constant fails the suite | `tests/test_framings.py` |
