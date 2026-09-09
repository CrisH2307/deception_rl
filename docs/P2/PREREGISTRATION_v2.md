# PREREGISTRATION v2.0

**Paper 2: the adversary effect and the RL Scientist**

Version 2.0 · written 2026-09-09 · produced by T5.

**Data observed at the time of writing: none.** Not the `beta_c` distribution, not
the pool characterization, not a single model output. T1 and T2 have not run and this
repository contains no implementation code. The T5 brief anticipated that the
`beta_c` distribution needed for bin edges would already be visible and asked for it
to be disclosed; it is not, because T2 runs in a parallel Wave 1 session and has not
reported. Every number in this document is therefore fixed with no view of any P2
measurement. Where a number is this document's own judgement call rather than a value
carried over from Paper 1 or from `docs/spec/adversary-game-v1.md`, it is marked
**Proposed here** and listed again in Appendix A.

**Relationship to Paper 1's preregistration.** Paper 1's live preregistration is
`PREREGISTRATION_v1.0.md` as amended by `PREREGISTRATION_v1.1.md`, at
`/Users/crishuynh/Documents/SoftwareProject/deception/`. This is a new standalone
document for Paper 2 that continues that version numbering and inherits its
conventions, its dependent-variable construction, and its correction discipline. It
does not amend Paper 1. Decision identifiers of the form `D<n>` refer to Paper 1's
decision log, `.claude/rules/30-data-decisions.md` in the Paper 1 repository.

**This file is never edited in place** (Paper 1's D148 convention). Amendments are
written as `PREREGISTRATION_v2.1.md` and both are read together.

**Revision record.** One same-day, pre-data amendment was made at author direction
before this document was released to any downstream task: **K1's kill decision moved
from the grid rate `|D(8)| / N` to the existence rate `|D(infinity)| / N`**, with a
third outcome and its response added (§7.1). The reason is stated in §7.1 and is a
correctness fix, not a relaxation: the original wording would have killed a real
adversary effect whenever the `beta_c` distribution sat above the reporting grid's
endpoint. No data of any kind existed when it was made, no prediction in §1 was
changed, and no other kill criterion was touched. It is recorded here rather than
silently absorbed, because D148's rule exists to make exactly this kind of edit
visible.

**Authoritative documents.** `docs/spec/adversary-game-v1.md` (content version v2) is
the single source of truth for the game. Where this document states a formula that
also appears there, the spec wins and this document is wrong.

---

## 0. What is inherited and frozen

Unchanged from Paper 1 and not modified by anything below: the 1,118-concept
vocabulary and SPoSE similarity space; the `fit` function (min-aggregation
exponential decay, no free parameters, D25, D29); the 200,000-candidate pool and
`generate_items.py`; the Format V rendering (format L is retired as a measurement
condition, D103); the four tiles and their option menus, `|O| = 3, 3, 4, 6` for
`manmade`, `moves`, `hold`, `size`; the uniform prior over the 100-hypothesis space;
and Paper 1's oracle `o_bayes`, which the adversary game reproduces exactly at
`beta = 0` (spec §5.1).

One new free parameter is introduced, `beta`. `tau` is fixed at 1 and is not a free
parameter (spec §8.1): `tau = 1` is the unique value at which the quantal-response
listener's `beta = 0` optimum coincides with Paper 1's frozen argmax oracle, so
sweeping it in the main analysis would silently modify a frozen artifact.

---

## 1. Hypotheses and directional predictions

Three arms. Each prediction below is stated with the outcome that would refute it.
Nothing here is written as an expectation whose opposite would also be accepted.

### H-A (Arm A, normative). The adversary effect exists in this signal space.

**Claim.** The adversary reorders the optimal option on a non-trivial fraction of
items, `|D(beta)|` grows strictly with `beta` over the reporting grid
`{0, 0.25, 0.5, 1, 2, 4, 8}`, and a non-trivial fraction of items are
adversary-robust (`beta_c = infinity`).

**Reasoning.** The objective moves continuously from max-posterior to max-margin as
`beta` grows (spec §5.2). Whether the two argmaxes ever differ is a property of the
`fit` geometry, not of the game, and is therefore genuinely open. Small option sets
cap how often a reordering can occur at all, which is why the same measurement is
reported per tile.

**Refuted by.** A pooled existence rate `|D(infinity)| / N` below the K1 threshold in
§7. A grid rate `|D(8)| / N` below that threshold while the existence rate clears it
does not refute H-A; it is K1's outcome 3, a reporting grid too short for the effect
rather than an absent effect.
That outcome is a kill, not a null to be worked around: it says the adversary
mechanism has nothing to bite on in this signal space, and Arms B and C do not run.

**Also predicted, and a bug check rather than a hypothesis.** The price of robustness
`L(h*|o*_0) - L(h*|o*_infinity)` is non-negative for every item, by the definition of
`o*_0` as the posterior argmax. A negative value anywhere is an implementation bug in
T1, not a finding. It is exactly zero only where `o*_0` and `o*_infinity` are tied on
`L(h*|.)` and separated by the tie-break, which Paper 1's `boundary_exact` items can
produce; that count is reported rather than absorbed.

### H-B (Arm B, descriptive). Language models do not track the adversary.

**Claim, stated as the prediction and not as a hope.** For every model on the ladder
and for both framing contrasts, mean adversary displacement does not move from the
no-adversary optimum toward the adversary-aware optimum: the Bonferroni-corrected
interval on mean `ΔA` (§3, §4) contains zero. Any movement that does appear is
uncorrelated with the direction that would indicate adversary awareness, measured as
in §4.3.

**Reasoning.** Paper 1 measured models sitting outside the salience-Bayes interval on
the far side of salience, in all 21 model x rule cells (D120), and confirmed on the
discriminating axis that they are flat like a salience chooser but at `fit_norm`
0.09 to 0.67 against the salience pole's 1.000 (D136). A model that does not track
the stationary target has no established capacity to notice that the target moved.
The `fit_cost` interaction was measured flat under the primary rule for every model,
with no slope interval excluding zero on mean `post_norm` (D134, D136, and v1.1's
A2). The prediction here is the direct consequence of that measured result, not an
independent guess, and it is the reason Paper 2 is worth running: a confirmed null on
a second axis is the finding.

**Refuted by.** Any model whose interval on mean `ΔA` excludes zero in the positive
direction under the corrected threshold, survives all three scoring rules (D109), and
exceeds the attribution cap set by the control set (§4.4).

**Outcomes not on this list.** Paper 1's v1.1 amendment A1 recorded that the observed
model-side outcome was a fourth possibility its refutation list had not anticipated,
and refused to claim it had been foreseen. The same rule binds here. If Arm B
produces a pattern this section does not enumerate, it is recorded as an
unanticipated outcome and is not written as a predicted one.

### H-C (Arm C, constructive). A learned policy recovers the optimum; a policy
### trained without the adversary does not transfer.

**Claim 1, verification.** Self-play between Scientist and adversary converges to the
analytic minimax value computable from the spec, within the tolerance in §7 K3.

**Claim 2, ablation.** A policy trained at `beta = 0` does not transfer to `beta > 0`.
Its value at `beta > 0` is strictly below that of a policy trained at that `beta`,
and the gap widens with `beta`.

**Reasoning.** At `beta = 0` the optimal policy is the posterior-maximizing one and
carries no information about margin (spec §5.1). The two objectives coincide exactly
at `beta = 0` and diverge continuously thereafter, so a `beta = 0` policy is
structurally blind to the quantity that matters at `beta > 0`. A clean negative here
is a good result: it shows the adversary effect must be trained in rather than
emerging from the base objective.

**Claim 3, transfer.** A policy trained against the best-responding adversary
degrades when evaluated against a fixed-heuristic adversary and against a
language-model adversary. The degradation is reported as a number; no direction of
degradation across those two evaluation adversaries is predicted, because there is no
basis for one, and none is claimed after the fact either.

**Refuted by.** Claim 1 by non-convergence, which is first diagnosed as an
environment bug (T8 Step 3 checks the environment before the algorithm). Claim 2 by a
`beta = 0` policy matching a `beta`-trained policy at `beta > 0`.

**Not a result under any circumstance.** A policy that exceeds the analytic optimum.
See §7 K3.

---

## 2. Design

**Item set.** A fresh draw from Paper 1's frozen 200,000-candidate pool, stratified on
`beta_c` instead of `fit_cost` (D2 in `docs/P2/README.md`'s locked decisions).
Produced by T2 with a manifest recording seed, pool hash, bin edges, per-cell counts
and spec version. Overlap with Paper 1's 1,000 items is expected and is quantified
rather than avoided.

**The confirmatory analysis set is the `size` tile.** Paper 1's D49 made `size` the
primary tile because it is the only tile spanning the full `fit_cost` range on its
own, and D108 then measured that the planned low-end replication has no replicating
tiles: `moves` sits below its own marginal null at all four rungs and `hold` carries
approximately nothing. Paper 2 inherits that. The confirmatory Arm B analysis runs on
`size`-tile items with finite `beta_c`; `manmade`, `moves` and `hold` are reported as
secondary, and as the continuation of Paper 1's negative result about which tile
constructions support the task (D105), never as a second estimate of the primary
effect.

Two consequences worth stating in advance. First, every item in the confirmatory set
has `|O| = 6`, so the model's marginal over canonical option ids (§3.3) is a single
six-vector and is not mixed across tiles of different arity. Second, T2's per-cell
quotas must deliver enough `size`-tile items with finite `beta_c` to satisfy §8; that
is a coordination requirement on a parallel session and is listed in Appendix A.

**Kill-gate item base.** The K1 gate in §7 is computed over the **full 200,000
candidate pool**, not over T2's frozen item set, and its kill decision is on the
existence rate `|D(infinity)| / N` rather than on the grid rate `|D(8)| / N`. T2
stratifies on `beta_c`, so a divergence rate measured on that set reads out the
sampler's quotas rather than whether the adversary effect exists in the signal space.
The rate on the frozen set is reported alongside the pooled rates and is labelled
sampler-dependent. `docs/P2/tasks/T6.md` was patched on 2026-09-09 to match; see
Appendix A.2.

**Framings.** Three, from T3, differing only in how the adversary is described:

| framing | content |
|---|---|
| `F0` | No adversary. Byte-identical to Paper 1's prompt where content is shared. |
| `F1` | An audience member already knows the answer and wants the others to guess wrong. The mechanism is not described. |
| `F2` | As `F1`, plus the statement that the adversary will argue for whichever wrong answer the signal makes look most plausible. |

`F1` versus `F2` is the load-bearing contrast. It separates "the model cannot
represent an adversarial audience" from "the model was never told how the adversary
works." Length parity between `F1` and `F2` is T3's responsibility and its word-count
delta is an input to §4.5's cell-4 diagnosis.

**Model ladder.** Paper 1's, unchanged: L1 Qwen3-0.6B Instruct, L2 Qwen3-1.7B
Instruct, L3 Qwen3-4B Instruct, L4 Qwen3-8B Instruct, B2 Qwen3-1.7B Base, B4
Qwen3-8B Base, and the cross-family control at approximately 7B with open
pretraining data (D110). Seven models.

**Measurement.** Forced-choice scoring by log-probability over the option strings
under Format V, with Paper 1's harness, decoding settings, parsing and seed
convention (D101, D103). Two option-order permutations per item; permutation is a
reported factor, never averaged away. Scoring is deterministic at a pinned revision
and seed, so the model contributes no sampling error (D73); all uncertainty in Arm B
is item-level.

**Cross-family restriction.** D111 stands: raw log-probability magnitudes are never
compared across tokenizer families. Every quantity in §3 is a choice-based statistic
computed within a model and compared as a rate, so the cross-family control is
admissible on all of them.

---

## 3. Primary dependent variable

### 3.1 The two coordinates

Both are normalized within an item's own option set, as in Paper 1 (D47). For item
`i` with option set `O_i`:

```
post_norm_i(o) = ( L(h*|o) - min_{o'} L(h*|o') ) / ( max_{o'} L(h*|o') - min_{o'} L(h*|o') )

margin_i(o)    = log L(h*|o) - max_{h != h*} log L(h|o)                    (spec §5.2)

marg_norm_i(o) = ( margin_i(o) - min_{o'} margin_i(o') ) / ( max_{o'} margin_i(o') - min_{o'} margin_i(o') )
```

`post_norm_i(o*_0) = 1` and `marg_norm_i(o*_infinity) = 1`, both by construction:
`o*_0` is the posterior argmax and `o*_infinity` is the margin argmax, which is the
`beta -> infinity` limit of `argmax_o V_beta(o)` for every `tau > 0` (spec §5.2).

### 3.2 The primary measure: adversary displacement

```
ext_i  = 1 - marg_norm_i(o*_0)                                   the item's adversary extent

A_i(o) = ( marg_norm_i(o) - marg_norm_i(o*_0) ) / ext_i
```

`A_i(o*_0) = 0` and `A_i(o*_infinity) = 1`. `A` is signed: an option scoring below the
no-adversary optimum on normalized margin takes a negative value, and that is
information, not an error. `A` is bounded above by 1 because `marg_norm <= 1`.

`ext_i > 0` if and only if `o*_infinity != o*_0`, which is exactly `beta_c(i) <
infinity`. So `A` is defined precisely on the divergence set and undefined on the
adversary-robust items, which is the correct behaviour: where the adversary does not
move the optimum there is no movement to measure. The adversary-robust items are the
control set and carry their own measure (§4.4).

**Primary analysis set:** `D(infinity) = { i : beta_c(i) < infinity }` restricted to
the `size` tile. **Primary target:** `o*_infinity`. The `beta` grid does not enter
Arm B's confirmatory family at all; it indexes Arm A's divergence curve and Arm C's
training and evaluation, both of which are reported quantities rather than hypothesis
tests. Any `beta`-indexed Arm B measure is exploratory (§10).

**Aggregation.** `A` is computed per rendering, averaged within item across the two
Format V permutations, then aggregated across items. Two aggregates are reported for
every cell, following Paper 1's handling of the same ratio pathology in
`src/frontier_position.py`: the **median of per-item values**, and the value computed
**from the means**. A mean of per-item ratios is not usable when the per-item
denominator approaches zero, and Paper 1 measured that failure directly. The
`ext_i >= 0.02` floor in §6 is the same guard, carried over.

### 3.3 The reference set, named explicitly

Every model is placed against four references on the `A` axis, on the same items.
Paper 1's point applies unchanged: what matters is where a chooser sits between the
references, not whether it beats a baseline.

| reference | value on the `A` axis |
|---|---|
| **Bayes oracle** `o*_0` | `A = 0` by construction. The no-adversary optimum. |
| **Adversary oracle** `o*_infinity` | `A = 1` by construction. The adversary-aware optimum. |
| **Salience** `o_fit = argmax_o f(o, h*)` | `A_i(o_fit)`, measured per item. Free to fall anywhere, including outside `[0, 1]`. |
| **Marginal null** | `A_null(m, F) = sum_o p_{m,F}(o) * A_i(o)`, where `p_{m,F}` is model `m`'s own marginal over canonical option ids under framing `F`, computed within model and within framing over the confirmatory analysis set. |

The marginal null is D106's, applied to the `A` coordinate rather than to consistency.
A model with no item-sensitivity at all still produces a moving `A` because the option
geometry varies across items, and mistaking that for content is exactly what D106
exists to prevent. **Excess** is `A_observed - A_null`, and any claim that a model
carries adversary-relevant content is made on excess, never on raw `A`.

`post_norm` is retained and reported alongside `A` for every cell, because it is the
axis on which Paper 1's result is stated and the `F0` replication check (§4.2) is
performed on it.

---

## 4. Primary contrast

### 4.1 The tests

Per model `m`, per item `i` in the confirmatory analysis set:

```
ΔA_1(m, i) = A_i(choice under F1) - A_i(choice under F0)
ΔA_2(m, i) = A_i(choice under F2) - A_i(choice under F0)
ΔA_3(m, i) = A_i(choice under F2) - A_i(choice under F1)
```

The test on each is a paired test across items on the mean of the per-item difference,
reported with a 95% interval at the corrected alpha of §8. The interval is the
analytic t interval on the paired differences, matching Paper 1's convention of OLS
and t intervals on item-level quantities (`src/divergence_curve.py`) rather than a
bootstrap. Items are the only source of sampling variability, because scoring is
deterministic (D73).

`ΔA_3` is not a linear redundancy to be dropped. It is the `F1` versus `F2` contrast
that separates representational failure from an uninformed prompt, and it is the
contrast §2 calls load-bearing, so it is a member of the confirmatory family in its
own right.

### 4.2 `F0` replication, run before anything else

`F0` must reproduce Paper 1's reported result on the items shared between Paper 1's
1,000 and Paper 2's draw, on `post_norm` and on excess over the marginal null. This is
a gate on artifact reuse, not a hypothesis test: if `F0` does not replicate, something
in the reused pipeline has changed and every `F1` and `F2` number is suspect. The
comparison is reported before any `F1` or `F2` analysis is run. No threshold is set
for "reproduces" beyond the requirement that the Paper 1 and Paper 2 `F0` intervals on
the shared items overlap; a failure is reported and escalated rather than tuned away.

### 4.3 What "uncorrelated with the correct direction" means, operationally

H-B predicts that any movement is uncorrelated with the direction indicating adversary
awareness. That is tested as the Spearman rank correlation, within the confirmatory
analysis set, between per-item `ΔA` and per-item `ext_i`. A model that tracks the
adversary should move further where there is further to move. The prediction is that
this correlation's interval contains zero, for every model and both of `ΔA_1` and
`ΔA_2`. This correlation is a member of the exploratory set, not the confirmatory
family, because it is a secondary characterization of a movement whose existence the
primary test is what establishes; it is reported whether or not the primary test
rejects.

### 4.4 The control set and the attribution cap

The adversary-robust items, `beta_c = infinity`, are the built-in control: `o*_0 =
o*_infinity` there, so the optimal option does not change and there is nothing for an
adversary-aware model to move toward. Any change in the choice distribution on those
items is prompt sensitivity.

Because `A` is undefined on the control set, the control measure is the total
variation distance between the model's marginal over canonical option ids under `F1`
(or `F2`) and under `F0`, computed on the control items:

```
TV(m, F) = 0.5 * sum_o | p_{m,F}^{ctrl}(o) - p_{m,F0}^{ctrl}(o) |
```

**Attribution cap, preregistered.** Take the option-frequency shift measured on the
control set, apply it as a reweighting on the confirmatory analysis set, and compute
the displacement it predicts:

```
ΔA_null(m, F) = sum_o ( p_{m,F}^{ctrl}(o) - p_{m,F0}^{ctrl}(o) ) * mean_i A_i(o)
```

A confirmatory claim that a model tracks the adversary requires **both** that the
interval on mean `ΔA` excludes zero in the positive direction at the corrected alpha,
**and** that the observed mean `ΔA` exceeds `ΔA_null(m, F)`. Movement that a generic
prompt-induced shift in option preference already explains is reported as prompt
sensitivity and named as such.

### 4.5 The four cells of the `F1` / `F2` outcome space

All four are filled in advance. "Movement" means the primary test rejects at the
corrected alpha in the positive direction and clears the §4.4 attribution cap.

**Cell 1. No movement in `F1`, no movement in `F2`.** The predicted outcome. Reading:
telling the model an adversary is present does not change its signal choice, and
telling it exactly how the adversary works does not either. Combined with Paper 1,
the headline is that game structure is a second axis of misalignment: models do not
merely miss the target, they do not notice it moved. This is a positive finding about
a null, and it is the reason Arm C exists in the same paper: Arm C shows the
behaviour is learnable, so its absence is not an artifact of the task being
impossible.

**Cell 2. Movement in `F2` only.** Reading: models can act on an adversary once the
mechanism is stated but do not infer the mechanism from the adversary's mere presence.
This separates a knowledge deficit from a representational one and weakens the
"cannot represent" reading in favour of "was not told." The magnitude of `ΔA_3` is
then the quantity of interest, and the paper's claim narrows to inference about the
adversary rather than response to it. This cell also raises a competing explanation
that must be checked before the substantive one is adopted: `F2` names the mechanism
in terms close to the margin criterion itself, so it may be functioning as an
instruction rather than as a description of the audience. The check is whether the
same movement appears in an exploratory wording variant that describes the mechanism
without naming a comparison among wrong answers.

**Cell 3. Movement in both.** Refutes H-B. Reading: the adversary's presence alone is
enough to shift signal selection, and models represent an adversarial audience without
being told how it operates. `ΔA_3` then measures the marginal value of stating the
mechanism, and the paper's contribution shifts from a second null to a measured
capacity, reported against the `A = 1` ceiling so that "moved" is not confused with
"reached the optimum." Paper 1's result is not thereby contradicted: sensitivity to
game structure and accuracy against a fixed target are different quantities.

**Cell 4. Movement in `F1` only.** Strange, and an explanation is prepared rather than
improvised. Checked in this order, and none is adopted unless its own check passes:

1. *Length or register artifact.* T3 adds neutral filler to `F1` if `F2` is
   materially longer. If the filler itself moved choices, the control set will show a
   `TV(m, F1)` comparable to the divergence-set movement and the movement will fail
   §4.4's cap. Check against T3's word-count parity report and the control-set TV.
2. *`F2` triggers a different mode.* An explicit statement that someone will argue for
   a plausible wrong answer may push a post-trained model toward hedging or toward a
   single safe option. Check the per-model option marginals under `F2` for
   concentration on one option relative to `F0` and `F1`; base models B2 and B4 are the
   discriminating comparison, since they carry no such post-training.
3. *`F2` read as an instruction to the model rather than a description of the
   audience.* Check by the same exploratory wording variant named in cell 2.
4. *Chance.* With 21 confirmatory tests, check whether the result survives the
   corrected threshold and whether it holds under all three scoring rules (D109). A
   cell-4 result appearing under one rule only is stated as rule-dependent in the
   sentence that makes it, never in a footnote.

If none of the four checks resolves it, the result is reported as unexplained. It is
not reported as adversary awareness.

---

## 5. Covariates and their planned treatment

| covariate | treatment |
|---|---|
| `beta_c` | Paper 2's stratification variable. **Continuous, never dichotomised.** `infinity` is carried as an explicit `is_robust` boolean alongside the raw value and is never recoded to a large finite number (spec §8.2). `beta_c = 0` boundary-tied items are retained, counted and reported; they sit in `D(beta)` for every `beta > 0` but not in `D(0)` (spec §7.1). |
| `fit_cost` | Paper 1's stratification variable. Reported for continuity with Paper 1 and as the input to K2 in §7. |
| `ext_i` | Adversary extent, the denominator of `A`. Analysis covariate and the subject of §4.3's correlation. Never an input to `fit`. |
| price of robustness | `L(h*|o*_0) - L(h*|o*_infinity)`, from Arm A. Exploratory as a predictor of `ΔA`. |
| `tile` | Reported factor. `size` is confirmatory; the other three are secondary (§2). Never averaged over. |
| `\|O\|` | Reported. It is a structural confound on divergence rate and is handled by spec §7.2's per-tile gate protocol, not by adjustment. |
| option position / permutation | Reported factor, permutation stored per rendering, never averaged away. |
| scoring rule | PMI primary, unnormalised sum and per-token mean both run over the full set and reported alongside (D98, D109). |
| `boundary_exact` | Per concept-and-tile flag, inherited (D26). Reported as the source of any exactly-zero price of robustness. |
| `wn_noun_senses`, `log_subtlex` | Inherited treatments unchanged (D6, D62, D4, D10). Not used in any Paper 2 confirmatory test. |

---

## 6. Pre-specified sensitivity analyses

Results of these are reported as robustness. They are not hypothesis tests and do not
enter §8's correction family.

1. **`tau` robustness, appendix only, protocol fixed by the spec.** Recompute Arm B's
   primary measure at `tau` in `{0.5, 2}`, using as the no-adversary reference the
   **`tau`-local optimum** `argmax_o V_0(o)` at that `tau`, not `o*_0`. Report only
   whether Arm B's qualitative conclusion survives. State explicitly that
   oracle-nesting holds at `tau = 1` only, and that at `tau < 1` the `tau`-local
   reference already embeds rival suppression, so movement found there is not
   attributable to `beta` alone. This is spec §5.1's protocol verbatim and is
   preregistered here rather than decided after seeing data.
2. **Decay family.** The whole of Arm A is recomputed under exponential and Gaussian
   decay and both are reported (D52, D57). The family is Paper 1's largest single
   source of ground-truth uncertainty, flipping `o_bayes` on 29.5% of conflict items.
   Reported for Paper 2: the flip rate of `o*_infinity` and of divergence-set
   membership under the swap. A high flip rate is a stated limit on Arm A's precision,
   not a reason to pick a family.
3. **Scoring rule triad** (D98, escalated by D109). Every reported Arm B finding is
   recomputed under PMI, sum and mean and reported under all three. A finding that
   holds under one rule only is stated as rule-dependent in the sentence that makes
   it. The primary is PMI regardless of which ordering the three produce.
4. **Tie tolerance sweep.** `eps_tie` across 1e-9, 1e-6, 1e-4 and 1e-2, reported.
   Paper 1 found stability across the first three and slight drift at 1e-2; the
   adversary oracle inherits the same sweep because §6.2's tie-break is Paper 1's
   extended one level.
5. **Rating resampling.** 40 draws, each concept redrawn from `SD/sqrt(N)` per its own
   THINGSplus ratings, seed as in Paper 1. Reported: the stability of `beta_c`, of
   divergence-set membership, and of `o*_infinity`.
6. **`beta` grid completeness.** Every `|D(beta)|` figure reports all of
   `{0, 0.25, 0.5, 1, 2, 4, 8}` plus `infinity` as a labelled limiting case.
   `beta = 0` is a fixed separate anchor at `|D(0)| = 0` and the curve is never
   extrapolated from `beta -> 0+` back onto it (spec §7.1). The infinity mass is
   never dropped from a plot.
7. **Adversary extent floor.** The primary analysis applies `ext_i >= 0.02` (§7).
   The analysis is re-run with no floor and both are reported.
8. **fp16 batch-composition noise** (D102). The `size` tile carries the confirmatory
   analysis and is therefore scored at batch 1, with no padding and no batch effect.
   The other three tiles are batched, with a stratified subsample re-scored at batch 1
   and the flip rate reported. The flip rate is a reported quantity, never a threshold
   to pass.

---

## 7. Kill criteria and exclusions

### 7.1 Kill criteria, numeric, fixed before any data

**K1, the divergence-set gate.** Computed by T6 Step 1 over the **full 200,000
candidate pool**. Two rates are reported, not one:

```
grid rate      |D(8)| / N          items that diverge at or below the grid endpoint
existence rate |D(infinity)| / N   items that diverge at any finite budget,
                                   equivalently the fraction with beta_c < infinity
```

> **The kill decision is on the existence rate. If `|D(infinity)| / N < 0.10` over
> the pool, the adversary effect is absent in this signal space. Arms B and C do not
> run.**

**Why the existence rate and not the grid rate** (amended 2026-09-09, before any
data; see the revision record in the header). The two rates fail for different
reasons and only one of them is about the signal space. `beta_c(i) = infinity` means
the adversary never reorders that item's optimum at any budget: the effect genuinely
does not exist there, because `o*_0` is already the margin-maximizer. A finite
`beta_c(i) > 8` means the effect does exist and the reporting grid is too short to
show it. Gating on `|D(8)|` conflates the two, and would kill a real effect whenever
the `beta_c` distribution sits mostly above 8. The grid endpoint of 8 is the spec's
completion of a truncated list (spec §8.2), flagged there as awaiting confirmation,
so it is a reporting convention and is not a fact about the signal space. It has no
business deciding whether Arms B and C run.

The 0.10 is **Proposed here**. Reasoning: the threshold is substantive rather than
power-driven, because availability never binds. Ten percent of the pool is 20,000
candidate items, far more than Arm B or T2 could use, and even one percent would
supply enough; so the number cannot be argued from sample size and has to be argued
from what would count as the effect existing. With `|O|` between 3 and 6, a
reordering of the argmax is structurally hard, and a rate below one item in ten at
any budget whatsoever describes a signal space in which the adversary has almost
nothing to bite on. Reporting that is a successful outcome for T6, not a failure.

**The three outcomes, and the response to each, fixed now.**

1. **Existence rate below 0.10.** Kill. The effect is absent in this signal space.
   Arms B and C do not run. Write up the negative result and stop.
2. **Both rates at or above 0.10.** Pass. The effect exists and the reporting grid
   reaches it. Wave 2 proceeds on the grid as specified.
3. **Existence rate at or above 0.10, grid rate below 0.10.** The effect is real and
   the reporting grid is too narrow. **Not a kill, and not a reason to lower the
   threshold.** The preregistered response is to extend the grid, as follows:

   - Append doubling points `16, 32, 64` to the divergence curve, in order, stopping
     at the first at which `|D(beta)| / N >= 0.10`. Report `|D(beta)| / N` at every
     point reached, and report which point stopped the extension.
   - The extension applies to Arm A's divergence curve only. Every other figure and
     table keeps the original grid `{0, 0.25, 0.5, 1, 2, 4, 8}` plus infinity, so
     that Paper 2's other numbers stay mutually comparable and comparable to the
     spec.
   - **The threshold is never lowered and the extension is never made conditional on
     what the extended points show.** The rule above is the whole rule; running it is
     mechanical.
   - **Hard ceiling at `beta = 64`, on interpretability rather than on numerics.**
     `beta` is a log-odds persuasion budget, so `beta = 8` already multiplies the
     decoy's odds by roughly 3,000 and `beta = 64` by roughly `6e27`. If the grid
     rate is still below 0.10 at 64, the reported finding is that the adversary
     effect exists but is reachable only at persuasion budgets with no plausible
     interpretation. That is carried as a stated limitation on Arms B and C, added to
     §11, and is not a kill, because the existence rate has already established that
     the optimum does move.

   **Arm B is not affected by outcome 3.** Its analysis set is `D(infinity)` and its
   target is `o*_infinity`, both `beta`-free (§3.2), so a short grid cannot weaken the
   confirmatory test. What a short grid weakens is Arm A's divergence curve and Arm
   C's training and evaluation grid, and the extension above is aimed at exactly
   those.

**K1 is applied jointly with spec §7.2's disambiguation protocol**, which is
preregistered by the spec and is restated here so the two cannot drift apart. Compute
the per-tile rate `r_t` for `manmade(3)`, `moves(3)`, `hold(4)`, `size(6)`, ordered by
`|O|` ascending. Spec §7.2 anchors these rates at `beta = 8`; this document's kill
decision is now on the existence rate, so **both sets are computed and reported**, at
`beta = 8` exactly as the spec specifies and at `beta = infinity` to match the gate
quantity. The criteria below are applied to the `beta = infinity` rates, because
those are the ones the kill decision reads; the `beta = 8` rates are reported
alongside and are what a reader compares against the spec. The resulting mismatch
between spec §7.2's anchor and this gate's anchor is flagged in Appendix A.2 for a
spec amendment and is not resolved by editing the spec from here. Then:

- **Structural, inconclusive.** `r_size - min(r_manmade, r_moves) >= 0.10`. The pooled
  outcome is reported as inconclusive, not as a clean negative, because option-space
  size is a plausible binding constraint. The joint multi-tile condition (spec §2.1)
  becomes an author-gated follow-up, not an automatic next step.
- **Clean negative.** `max_t r_t`, including `size`, is still below 0.10. Even the tile
  with the most room to diverge does not clear the bar, so `|O|` is not the limiting
  factor. Report and stop; Arms B and C do not run. This reading is available only
  when the pooled existence rate has itself failed; a per-tile pattern cannot
  overturn a passing existence rate.
- **Neither.** Report all four `r_t` and the pooled figure plainly, state that neither
  criterion was met, and stop for author review. Do not resolve this by picking
  whichever reading is more convenient.

**A pass must be recorded with a number.** T6 emits a machine-readable gate record
carrying the pooled existence rate, the pooled grid rate, the four per-tile rates at
each of `beta = 8` and `beta = infinity`, `N`, the spec version, the disambiguation
verdict, which of the three outcomes above obtained, and, if outcome 3, the extended
grid points and the point at which the extension stopped. T7 and T8 confirm a pass by reading that record. Absence of a
recorded failure is not a pass.

**K2, the `fit_cost` correlation gate.** Computed by T2 Step 1 over the full pool.

> **If `|rho_Spearman(beta_c, fit_cost)| >= 0.80`, the redraw rationale collapses and
> the design needs revisiting before Wave 2 opens.**

The 0.80 is carried over from the T2 brief's "if the correlation is above ~0.8, that
is a finding"; only its operationalization is fixed here. The statistic is **Spearman
rank correlation over the full pool with `beta_c = infinity` ranked as the maximum**,
tied at the top. Rank correlation is used because `beta_c` has a point mass at
infinity that Pearson cannot consume, and discarding the robust items to make Pearson
computable would drop exactly the stratum the redraw exists to create. The Pearson
correlation on the finite subset is reported as a secondary descriptive number and is
not thresholded. **Proposed here:** the choice of Spearman-with-infinity-ranked-top as
the gate statistic.

If K2 fires, the finding is reported prominently and Wave 2 stops for an author
decision. It is not resolved by re-picking the stratification variable inside the same
session.

**K3, the RL oracle gate.**

> **If a learned policy attains a value above the analytic optimum, that is
> misspecification of the oracle or the environment. It is a bug. It is not a
> result and it is not published as one.**

Numeric trigger, **Proposed here**: an estimated policy value exceeding the analytic
`V_beta` by more than three Monte Carlo standard errors, either in aggregate at any
grid `beta` or on any single item, halts T8 and opens a bug hunt in the environment
first and the oracle second. The corresponding success criterion for H-C claim 1 is
`|V_selfplay - V_minimax| <= 0.01` in absolute correct-accusation probability at every
reported grid `beta`; the 0.01 is also **Proposed here** and is a tolerance, not a
target to be reached by tuning. T8's anti-requirement against tuning reward shaping
binds regardless of whether the tolerance is met.

### 7.2 Exclusions

Every rule fixed here, before any data. Counts are reported for each rule separately,
and the primary analysis is re-run with no exclusions as a robustness check.

| exclusion | rule |
|---|---|
| **Adversary extent floor** | Items with `ext_i < 0.02` are excluded from the confirmatory Arm B analysis. `A` is a ratio whose denominator is `ext_i`, and Paper 1 measured this exact pathology on the analogous coordinate: near-zero spans produced values from -1 to -4 on a quantity bounded near `[0, 1]` (`src/frontier_position.py`). The floor is Paper 1's, carried over. The count is reported, the items are listed, and §6.7 re-runs without it. |
| **Scoring ties** | Renderings where the top two options are tied within `eps_tie` are excluded, matching Paper 1's `n_tied == 1` filter. The tie rate is reported per model and per framing. |
| **Nothing is excluded on `beta_c`** | No item is dropped for having an inconvenient `beta_c`, including `beta_c = 0` boundary-tied items and `beta_c = infinity` items, which are the control set. |
| **Parse failures** | The primary measurement is forced-choice log-probability scoring over option strings under Format V, so parse failure is structurally impossible and the reported rate is zero. If the harness reports any nonzero rate, the harness has changed and that is escalated, not filtered. Any generative variant is exploratory and carries its own rule, fixed here: the first exact match of an option string in the output, no retries, no resampling, and failures reported as data. |
| **Format** | Format L is retired as a measurement condition (D103) and is not scored. Format V only. |

---

## 8. Multiple-comparison discipline and power

### 8.1 The confirmatory family

**Seven models x three framing contrasts = 21 tests.** Bonferroni correction over the
family:

```
alpha = 0.05 / 21 = 0.002381    two-sided
```

This matches Paper 1's convention and its reasoning. Paper 1 corrected over the seven
ladder models rather than naming one primary rung, explicitly because no rung had been
argued for (v1.0 §8). That is still true, so all seven stay in. The three framing
contrasts are added because all three are load-bearing: `ΔA_1` and `ΔA_2` are the
movement tests, and `ΔA_3` is the contrast that separates representational failure
from an uninformed prompt.

**What is not in the family, and why:**

- **The `beta` grid.** Arm B's target is `o*_infinity` and its analysis set is
  `D(infinity)`, both `beta`-free (§3.2). The grid indexes Arm A's divergence curve
  and Arm C's training, neither of which is a hypothesis test. Any `beta`-indexed Arm
  B measure is exploratory.
- **The three scoring rules.** Following D109, every finding is recomputed and
  reported under all three rules, with rule-dependence stated in the sentence that
  makes the claim. Paper 1 did not spend alpha on them and neither does this; they are
  a robustness requirement on reporting, not additional tests.
- **The three secondary tiles.** Exploratory (§2, §10), so they do not enter the
  family.
- **The `F0` replication check.** A gate on artifact reuse (§4.2), not a test.
- **§4.3's direction correlation.** Exploratory and reported unconditionally.

### 8.2 Power and the item count T2 must deliver

Uncertainty is item-level only, because scoring is deterministic (D73). For a paired
test on per-item differences at `alpha = 0.002381` two-sided and 80% power, the
required number of items in the confirmatory analysis set is

```
n  =  (z_{alpha/2} + z_{0.20})^2 * sigma^2 / delta^2
   =  (3.038 + 0.842)^2 * sigma^2 / delta^2
   =  15.05 * sigma^2 / delta^2
```

with `sigma` the per-item standard deviation of `ΔA` and `delta` the SESOI.

**SESOI = 0.05 on mean `ΔA`.** Carried over from Paper 1's D74, which set the same
0.05 on mean `post_norm`. `A` and `post_norm` are both within-item normalized
coordinates on the same scale with the same pinned-pole construction, so the smallest
effect Paper 1 judged worth detecting transfers directly rather than being reinvented.

`sigma` is unmeasured, because no P2 data exists. The requirement is therefore stated
as a curve rather than a single number:

| per-item SD of `ΔA` | items needed at 80% power |
|---:|---:|
| 0.10 | 61 |
| 0.15 | 136 |
| 0.20 | 241 |
| 0.25 | 377 |
| 0.30 | 542 |
| 0.40 | 964 |

**T2 target, Proposed here: at least 400 `size`-tile items with finite `beta_c`**,
which covers `sigma` up to 0.25. Paper 1's primary set was 125 `size`-tile conflict
items, so this is a materially larger requirement and it is stated now, before T2
fixes its quotas, rather than discovered when the analysis is underpowered. If the
pool cannot supply 400 such items, that is itself a finding about the signal space and
is reported next to the K1 gate rather than absorbed by relaxing the SESOI.

**The load-bearing assumption, stated rather than buried.** The table rests entirely
on `sigma`, which nothing has measured. Paper 1 recorded the same exposure: its sample
size rested on the model estimate being a deterministic point value, and it said so.
Once T2 delivers the item set and T6 delivers `beta_c`, `sigma` is estimable from `F0`
alone without touching `F1` or `F2`, and the realized power is reported at that point.
Estimating `sigma` from `F0` does not spend any confirmatory alpha, because no
contrast in §4.1 involves `F0` alone.

---

## 9. Reproducibility commitments

- Seeds committed; results reproduce exactly from them.
- The item file carries a manifest recording seed, pool hash, bin edges, per-cell
  counts and spec version.
- Raw model outputs are never overwritten.
- Chain of custody verified by T9: item hash matches manifest, manifest cites spec
  version, spec version matches the one T1 implemented against. A mismatch anywhere is
  a hard failure.
- Every number in the paper is emitted by a script from frozen artifacts and committed
  seeds. No number is read off a plot or copied from a draft. T9's unverified-number
  list has an empty target.
- Parse failures, non-convergence and null results are reported as numbers, not
  retried away.

---

## 10. Confirmatory versus exploratory

**Confirmatory.** Only the following, at Bonferroni-corrected `alpha = 0.002381` over
the 21-test family in §8.1: the three framing contrasts `ΔA_1`, `ΔA_2`, `ΔA_3` on
mean adversary displacement, per model, on `size`-tile items with finite `beta_c`,
subject to §4.4's attribution cap and §7.2's exclusions.

Arm A is a computation, not a test. Its numbers are reported with their distributions
and are not assigned p-values; H-A resolves through the K1 gate, which is a
preregistered threshold rather than an inference.

Arm C's claim 1 is a verification against a computable ground truth and resolves
through the §7 K3 tolerance. Claims 2 and 3 are reported as measured differences with
intervals; they are preregistered directional predictions but do not enter the Arm B
alpha family, because they are tests on a policy rather than on a model ladder and
share no items with it.

**Exploratory, labelled as such wherever it appears:**

- The three secondary tiles `manmade`, `moves`, `hold`, and the continuation of Paper
  1's negative result about which tile constructions support the task.
- §4.3's correlation between per-item `ΔA` and `ext_i`.
- What predicts a low `beta_c` (T6 Step 4), and any regression of `beta_c` on item
  properties.
- The price of robustness as a predictor of anything, as opposed to as a reported
  distribution.
- Any `beta`-indexed Arm B measure, including displacement toward `argmax_o V_beta`
  at a finite grid `beta`.
- The `tau in {0.5, 2}` appendix check (§6.1), which is preregistered in protocol but
  reports robustness only.
- The joint multi-tile construction (spec §2.1), which is not built and is
  author-gated.
- The GRPO stretch goal in T8, which requires author sign-off.
- The language-model adversary in T8's transfer experiment.
- Any wording variant of `F2` used to diagnose cells 2 or 4 of §4.5.
- Format and position effects, per-category breakdowns, and anything suggested by
  looking at the data.

An exploratory result is never reported in language that implies confirmation.

---

## 11. Known limitations, stated in advance

1. **`tau = 1` is forced, not chosen for realism.** It is the unique value at which the
   quantal-response listener's `beta = 0` optimum coincides with Paper 1's frozen
   argmax oracle (spec §5.1). Every conclusion is about a `tau = 1` listener. The
   appendix sweep reports whether the qualitative conclusion survives, and at
   `tau < 1` the `tau`-local reference already embeds rival suppression, so movement
   found there is not attributable to `beta` alone.
2. **The adversary is decoy-only** (D5). It responds to the signal and does not choose
   `h*`. A state-choosing adversary changes the item distribution rather than the
   objective and would break the Paper 1 comparison; it is a different game and
   plausibly a different paper.
3. **`beta` has no empirical calibration.** It is a persuasion budget in log-odds with
   no measured human counterpart, so `beta_c` is interpretable as an ordering over
   items and as a fragility scale, not as a quantity of real-world persuasion. The
   grid endpoint of 8 is the spec's completion of a truncated list, not a calibrated
   maximum.
4. **Option sets are small.** `|O|` between 3 and 6 caps how often the argmax can move
   at all. Spec §7.2's per-tile protocol makes that confound visible; it does not
   remove it.
5. **The confirmatory claim rests on one tile construction.** Paper 1's D108 measured
   that only `size` supports the task, so Arm B's confirmatory result is about
   `size`-tile items and inherits whatever is specific to that tile's six-option
   anchored scale.
6. **The adversary pole is pinned.** `A` is 1 at `o*_infinity` by construction, exactly
   as `post_norm` is 1 at `o_bayes` (Paper 1's limitation 9). All of `A`'s variance
   comes from the non-optimal options, which constrains what any ratio computed on it
   can mean.
7. **No human arm** (D3). Whether human speakers shift toward margin-maximizing
   signals under an adversarial audience remains unmeasured. The gap is stated in
   T4's precise wording and no broader version of it is claimed.
8. **The `F0` replication is on the overlap only.** Paper 2's items are a fresh draw,
   so the replication check runs on whatever items the two draws share, and its power
   depends on an overlap that is not known at the time of writing.
9. **The decay family remains the largest source of ground-truth uncertainty** (D38).
   It is handled by running Arm A under both families, not by excluding items, and the
   `o*_infinity` flip rate under the swap is a stated limit on Arm A's precision.
10. **`sigma` is unmeasured**, so §8.2's power table is a curve over an assumption
    rather than a computed sample size. This is the single most consequential unknown
    in the design and T2's quotas are being set against it.
11. **`beta_c = 0` items are a real category, not an artifact.** They are maximally
    fragile: any positive budget flips them. They sit in `D(beta)` for every
    `beta > 0` but not in `D(0)` (spec §7.1). Their count is reported, and if they
    dominate the divergence set then the effect is concentrated in boundary ties
    rather than distributed over the budget range, which would be a substantive
    qualification on H-A and is checked before H-A is stated as supported.
12. **Paper 1's own limitations are inherited whole**, including SWOW cue-list bias,
    unmitigated polysemy, the image-derived SPoSE space applied to a verbal task, and
    the fact that the informativeness-confusability trade-off is RSA's and not this
    program's discovery.

---

## Appendix A: values proposed here, and coordination items

### A.1 Numbers this document sets that no prior document fixed

Listed so an author reviewing the preregistration can change any of them by changing
one line, and so no downstream task mistakes a judgement call for an inherited value.

| value | where | basis |
|---|---|---|
| K1 threshold `0.10` | §7.1 | Judgement call. Substantive, not power-driven; availability never binds at pool scale. Author-confirmed 2026-09-09. Applies to the existence rate `\|D(infinity)\| / N`, per the same-day amendment. |
| K1 grid extension: `16, 32, 64`, ceiling 64 | §7.1 | Judgement call. Doubling is arbitrary but mechanical, which is the point; the ceiling is set on interpretability of a log-odds budget, not on float range. |
| K2 statistic: Spearman with `infinity` ranked top | §7.1 | The `0.80` is carried over from the T2 brief. The choice of rank correlation with the infinity mass ranked at the maximum is proposed here, because `beta_c` has a point mass Pearson cannot consume and dropping it would discard the stratum the redraw creates. |
| K3 trigger: 3 Monte Carlo SE | §7.1 | Judgement call. Standard tolerance for "exceeds by more than noise". |
| H-C claim 1 tolerance: `0.01` absolute | §7.1 | Judgement call on a probability scale. Not a target to be tuned toward. |
| SESOI `0.05` on mean `ΔA` | §8.2 | Carried over from Paper 1's D74, on the argument that `A` and `post_norm` share the scale and the pinned-pole construction. |
| Adversary extent floor `0.02` | §7.2 | Carried over from Paper 1's frontier span floor, which was set against a measured failure of the same ratio form. |
| T2 target: 400 `size`-tile finite-`beta_c` items | §8.2 | Derived from the power curve at `sigma = 0.25`. The `sigma` is assumed, not measured. |
| Confirmatory family size 21 | §8.1 | Follows from the seven-model ladder and three framing contrasts, both fixed elsewhere. |

### A.2 Coordination items for parallel Wave 1 sessions and for Wave 2

Items 1 and 2 were **applied on 2026-09-09 at author direction**; the rest are stated
and not acted on, because Wave 1 tasks run in separate worktrees and this task does
not otherwise edit another task's brief.

1. **T6 Step 1, patched.** It computed the kill gate on T2's frozen item set. T2
   stratifies on `beta_c`, so that rate measures the sampler and not the signal space.
   `docs/P2/tasks/T6.md` now computes the gate over the full 200,000-candidate pool,
   states why in the brief itself, reports both the grid rate and the existence rate,
   decides on the existence rate, carries K1's three outcomes including the grid
   extension, reports the frozen-set rate alongside labelled sampler-dependent, and
   specifies the gate record's fields.
2. **T2 Step 2, patched.** `docs/P2/tasks/T2.md` now carries §8.2's target of at least
   400 `size`-tile items with finite `beta_c`, against Paper 1's 125, with the power
   curve, the `beta_c = infinity` control stratum drawn from the same tile so control
   and analysis sets are comparable on `|O|`, and an explicit statement that the
   target is provisional because `sigma` is unmeasured and is revisable once Arm A
   supplies a variance estimate.
3. **T2 also owns K2.** Its Step 1 already computes the `fit_cost` relationship; §7.1
   fixes the statistic and the threshold, and T2 should report exactly that statistic
   rather than a Pearson correlation on the finite subset alone.
4. **T3's word-count parity report is an input to §4.5 cell 4.** It should be emitted
   in a form the Arm B analysis can cite, not only stated in prose.
5. **T6 must emit a machine-readable gate record.** T7 and T8's precondition is an
   explicit recorded pass with a number attached, and the project's task-runner
   procedure forbids inferring a pass from the absence of a recorded failure.
6. **Spec §7.2's 10-percentage-point disambiguation threshold** is flagged in the spec
   as awaiting author confirmation. §7.1 restates it rather than replacing it. If the
   author changes it, only the spec subsection and §7.1's restatement change.
7. **Spec §7.2's anchor `beta` needs an amendment.** The protocol computes its
   per-tile rates at `beta = 8`, which was the gate quantity when the spec was
   frozen. §7.1's gate now decides on `beta = infinity`, so the per-tile criteria are
   applied at `beta = infinity` and the `beta = 8` rates are reported alongside. T6
   computes both. The spec should be amended to anchor §7.2 at the gate quantity so
   the two documents stop disagreeing; that is an author edit to the spec, not one
   this task makes.
