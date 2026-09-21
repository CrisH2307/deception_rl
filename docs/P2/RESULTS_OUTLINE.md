# Paper 2 results outline

**What this is.** Section structure, the claim each section makes, and the source of
every number, by file and key. It is an outline and a citation map. **It is not paper
prose and no passage below is drafted for the paper.**

**Scope ruling this records.** None. This document records no decision, adds no
`P2-D` number, and writes no preregistration version. The ruling it is written under
is the author's, on the counting result in section 3: **Arm C is ruled out in this
design and Paper 2 is Arm A plus Arm B.**

**Citation format.** Every number is cited as a single backticked token
`results/<file>.json:<key path>`. A `*` segment means every key at that level.
`tests/test_results_outline_citations.py` parses this file and asserts each token
resolves in the artifact it names. Nothing below was computed for this document: every
figure was read from `results/`, and where a section needs a figure that is not there,
it is flagged under **Needed and absent** rather than computed.

**Bases are named with every figure.** Four bases are in play and they are not
interchangeable: the 200,000-candidate pool, the frozen 1,000, the 460-item divergence
set, and the 108-item `size` confirmatory set. `p2_decisions.bind_adversary_tracking_claim`
refuses a caller that cites the divergence-set figure where the confirmatory set
governs, and the same discipline binds prose.

---

## 1. The adversary effect formalized

**Claim.** The game has an exact solution. The adversary's best response is fixed by
the signal alone, the Scientist's objective moves continuously in `beta` from Paper 1's
oracle to the margin-maximizing signal (**required condition: `tau = 1`, inherited from
Paper 1; see 1.3**), and the switch point is a closed form rather than a fitted
quantity. This is what makes the paper's optimum computable at every
adversary strength, which is the whole basis on which it differs from work that can
report win rates but not distance from optimal.

**Sub-claims and sources.**

1.1 **R1.** `d*(o) = argmax_{h != h*} L(h|o)`, independent of `beta` and `tau`.
Derivation and verification: `docs/spec/adversary-game-v1.md` section 4. No number.

1.2 **R2, the `beta` continuum.** `V_beta(o)` in closed form, verified by substitution:
`docs/spec/adversary-game-v1.md` section 5. The `beta -> infinity` clause holds for
every `tau > 0` (section 5.3). No number.

1.3 **P1's oracle is the exact `beta = 0` case. Required condition: `tau = 1`, inherited
from Paper 1 and not chosen by Paper 2.** This condition goes in the paper text wherever
the nesting claim appears, not only in the spec: it is the paper's central framing
sentence, it is false without the condition, and a reviewer checking the algebra finds
that in one line.

The claim as it must be stated. At `beta = 0`,
`V_0(o) = L(h*|o)^{1/tau} / sum_h L(h|o)^{1/tau}`. `L(.|o)` is a posterior over `H`, so
`sum_h L(h|o) = 1` for every `o`, and at `tau = 1` the normalizer is therefore
identically 1: `V_0(o) = L(h*|o)`, hence `argmax_o V_0(o) = argmax_o L(h*|o) = o*_0`,
Paper 1's oracle, exactly. At any `tau != 1` the normalizer is the `1/tau`-power sum of
the posterior, which depends on the shape of `L(.|o)` and not only on `L(h*|o)`, so the
identity fails and the spec constructs a counterexample.
Source: `docs/spec/adversary-game-v1.md` section 5.1. No number.

**Why it reads as inherited.** Paper 1's oracle `argmax_o L(h*|o)` is the optimal signal
for a `tau = 1` quantal-response listener. So `tau = 1` is not a parameter Paper 2 sets:
it is the temperature at which Paper 1's frozen oracle is the optimum at all. Any other
`tau` changes which option is the no-adversary optimum, which would be modifying a frozen
Paper 1 artifact. The spec records the resolution fixing `tau` at 1 on exactly this
ground (section 5.1, "Resolution").

**Precision the drafter must keep.** Write "the identity holds only at `tau = 1`", and not
"Paper 1's oracle is suboptimal at every other `tau`". On a given item the two argmaxes
can coincide at `tau != 1` by accident; what fails is the identity, and a counterexample
exists. A reviewer can produce an item where they coincide, so the stronger wording is
falsifiable and the precise one is not.

**Provenance, stated plainly.** The spec records that the original derivation of R2 was
written as general and assumed `tau = 1` without stating it. The condition was found by
re-derivation, not added to rescue a result.

**What `tau != 1` content is permitted.** The spec preregisters one appendix robustness
check at `tau in {0.5, 2}`, against the `tau`-local optimum rather than `o*_0`. It has not
been run and nothing here depends on it. The paper may not claim robustness to `tau`.

1.4 **`beta_c` in closed form.** The pairwise crossing equation is linear in
`x = exp(beta/tau)`, so each rival crosses at most once and
`beta_c(i) = min_{o' != o*_0} beta*_{o'}`: `docs/spec/adversary-game-v1.md` section 6.3.
Monotone nesting of `D(beta)` follows and is what makes bisection valid (section 6.3,
consequence 2). No number. **Required condition: `tau = 1` (1.3), for the tie to Paper 1
only.** The single-crossing argument holds at any `tau`; what needs `tau = 1` is that
`beta_c` is measured from `o*_0` and `o*_0` is Paper 1's oracle only there.

1.5 **The effect exists, at the population base.** Any claim of the form "X% of items
diverge" uses the pool figure, per the emitted rule
`results/T6_arm_a_numbers.json:rate_claim_rule.rule`.

- Pool existence rate `|D(infinity)|/N` = `results/T6_gate_record.json:pooled_existence_rate`
  on `results/T6_gate_record.json:N` candidates, against
  `results/T6_gate_record.json:threshold`.
- Grid rate `|D(8)|/N` = `results/T6_gate_record.json:pooled_grid_rate`.
- K1 outcome: `results/T6_gate_record.json:outcome_text`, reproduction bitwise identical
  to T2's pool table: `results/T6_gate_record.json:reproduction.bitwise_identical_to_T2_pool_table`.
- Per tile: `results/T6_gate_record.json:per_tile_existence_rate.*` and
  `results/T6_gate_record.json:per_tile_grid_rate.*`, with arity at
  `results/T6_gate_record.json:tile_n_options.*`.
- The pool-versus-frozen rule and both rates: `results/T6_arm_a_numbers.json:rate_claim_rule.population_existence_rate`,
  `results/T6_arm_a_numbers.json:rate_claim_rule.frozen_set_existence_rate`, and the
  reason the frozen rate is never a population statement,
  `results/T6_arm_a_numbers.json:rate_claim_rule.frozen_set_status`.

1.6 **`|D(beta)|` grows strictly over the reporting grid.** Pool curve at
`{0, 0.25, 0.5, 1, 2, 4, 8, inf}`: `results/T6_arm_a_numbers.json:step2.divergence_curve_pool.*`.
Frozen curve beside it: `results/T6_arm_a_numbers.json:step2.divergence_curve_frozen.*`.
No item sits at `beta_c = 0`: `results/T6_arm_a_numbers.json:step2.n_beta_c_exactly_zero`.
Items above the grid endpoint: `results/T6_arm_a_numbers.json:step2.n_finite_above_grid_endpoint`,
and the per-tile adequacy of the endpoint,
`results/T6_arm_a_numbers.json:step4.existence_vs_magnitude.max_per_tile_share_above_grid_endpoint_pool`.

1.7 **The identity that defines the divergence set holds exactly on the tie-broken
argmax, and does not hold on the raw sign of `ext_i`.** Exact identity:
`results/T6_arm_a_numbers.json:step4.identity_check.exact_identity_o0_ne_oinf_equals_finite`.
Raw sign test fails: `results/T6_arm_a_numbers.json:step4.identity_check.headroom_positive_equals_finite`,
on `results/T6_arm_a_numbers.json:step4.identity_check.n_headroom_sign_exceptions` item,
at `results/T6_arm_a_numbers.json:step4.identity_check.headroom_max_among_robust`. This
is a methods sentence, not a finding, and it belongs here because it is the reason
`A`'s domain is taken from `np.isfinite(beta_c)`.

**The closed-form-versus-bisection cross-check (spec section 6.3, note for T1), now
emitted.** One function, `adversary.bisection_vs_closed_form`, is what
`tests/test_adversary.py` asserts on and what `src/beta_c_crosscheck.py` emits, so the
artifact and the test cannot disagree. The bisected value remains the value of record
(`results/T1_beta_c_crosscheck.json:value_of_record`), with the tie band at
`results/T1_beta_c_crosscheck.json:tie_band_TAU_MAIN`.

- **Frozen 1,000, clean.** Robustness classification disagreements:
  `results/T1_beta_c_crosscheck.json:bases.frozen_1000.all.n_robust_classification_disagree`.
  Largest `beta` gap `results/T1_beta_c_crosscheck.json:bases.frozen_1000.all.max_abs_beta_gap`;
  closed-form root exact to
  `results/T1_beta_c_crosscheck.json:bases.frozen_1000.all.max_rel_top_two_gap_at_closed_form`;
  bisection fires within one tie band,
  `results/T1_beta_c_crosscheck.json:bases.frozen_1000.all.max_rel_top_two_gap_at_bisected`.
  Every Arm A figure at the frozen base, and all of Arm B, sits on this base.
- **200k pool, NOT clean, reported and not resolved.** Classification disagreements:
  `results/T1_beta_c_crosscheck.json:bases.pool_200000.all.n_robust_classification_disagree`,
  of which bisection-finite and closed-form-infinite
  `results/T1_beta_c_crosscheck.json:bases.pool_200000.all.n_bisection_finite_closed_form_inf`
  and the reverse
  `results/T1_beta_c_crosscheck.json:bases.pool_200000.all.n_bisection_inf_closed_form_finite`;
  concentrated on `size`,
  `results/T1_beta_c_crosscheck.json:bases.pool_200000.size.n_robust_classification_disagree`.
  Among items both call finite the `beta` gap reaches
  `results/T1_beta_c_crosscheck.json:bases.pool_200000.all.max_abs_beta_gap`, far past the
  spec's expected ~1e-6. **The spec names a robustness disagreement as what would be a
  bug.** The pre-existing test ran on the frozen 1,000 only, so this is the first time the
  pool was checked. Figures computed at the pool base on the bisected value, section
  1.5's existence rate and section 3's 2,748 among them, stand as emitted under the value
  of record; whether the disagreement touches them is **not established here**.
  **Needed before drafting any pool-base sentence: a ruling on this.** Not diagnosed, not
  fixed.

---

## 2. Arm A

**Claim.** On items where the adversary moves the optimum, the Scientist pays a
measurable price in posterior mass on the truth to buy margin, and the size of that
price is stated on Paper 1's own normalization. What predicts a cheap adversary is
reported and is labelled exploratory throughout.

**Sub-claims and sources.**

2.1 **The divergence set.** Frozen 1,000: finite `beta_c` on
`results/T6_arm_a_numbers.json:step2.n_finite` items, adversary-robust on
`results/T6_arm_a_numbers.json:step2.n_infinite`, at
`results/T6_arm_a_numbers.json:step2.finite_rate`. Per tile:
`results/T6_arm_a_numbers.json:step2.per_tile_finite_count.*`. `beta_c` distribution
on the finite subset: `results/T6_arm_a_numbers.json:step2.finite_percentiles.*`,
`results/T6_arm_a_numbers.json:step2.finite_mean`,
`results/T6_arm_a_numbers.json:step2.finite_sd`.
**The frozen rate is never quoted as a population rate** (rule at 1.5); the pool rate
is `results/T6_arm_a_numbers.json:rate_claim_rule.population_existence_rate` and the
frozen-set gap is fully accounted for by Paper 1's 50 per cent conflict quota,
`results/T6_arm_a_numbers.json:rate_claim_rule.frozen_set_status`.

2.2 **The price of robustness, on P1's `post_norm` convention.** Definition:
`results/T6_arm_a_numbers.json:step3.definition`, primary convention named at
`results/T6_arm_a_numbers.json:step3.primary_convention`.

- Headline, mean of per-item ratios: `results/T6_arm_a_numbers.json:step3.conventions.p1_post_norm.mean_of_per_item_ratios`.
- Median: `results/T6_arm_a_numbers.json:step3.conventions.p1_post_norm.median`.
- Value from the means: `results/T6_arm_a_numbers.json:step3.conventions.p1_post_norm.ratio_of_means`.
- `n` and undefined count: `results/T6_arm_a_numbers.json:step3.conventions.p1_post_norm.n`,
  `results/T6_arm_a_numbers.json:step3.conventions.p1_post_norm.n_undefined`.
- Raw difference, the quantity the spec defines:
  `results/T6_arm_a_numbers.json:step3.mean`, `results/T6_arm_a_numbers.json:step3.sd`,
  `results/T6_arm_a_numbers.json:step3.percentiles.*`.
- Both alternative denominators reported and neither the headline:
  `results/T6_arm_a_numbers.json:step3.conventions.above_prior.mean_of_per_item_ratios`,
  `results/T6_arm_a_numbers.json:step3.conventions.raw_share_of_total_mass.mean_of_per_item_ratios`.
  The reason `1/|H|` is not the reference Paper 1 uses is stated, not the value:
  `results/T6_arm_a_numbers.json:step3.conventions.above_prior.denominator`.

Median and value-from-the-means are reported together because the quantity is a mean
of per-item ratios, which is the pathology Paper 1 measured directly and which the
`ext_i >= 0.02` floor guards. The floor is retained and its reach is ruled by P2-D23.

2.3 **The bug check, reported as a number rather than assumed.** Non-negativity is a
consequence of `o*_0` being the posterior argmax, so a negative value would be an
implementation bug and not a finding:
`results/T6_arm_a_numbers.json:step3.n_negative`,
`results/T6_arm_a_numbers.json:step3.n_exactly_zero`,
`results/T6_arm_a_numbers.json:step3.n_exactly_zero_and_boundary_exact`,
`results/T6_arm_a_numbers.json:step3.n_boundary_exact_in_D`, and on the robust items
`results/T6_arm_a_numbers.json:step3.robust_items_price_max`.

2.4 **The corner that is kept rather than clipped.** Items where the adversary-robust
signal is the item's lowest-posterior option, so the normalised price is exactly 1:
`results/T6_arm_a_numbers.json:step3.spike_at_one.n`, all of them also `o_fit`
(`results/T6_arm_a_numbers.json:step3.spike_at_one.n_also_o_fit`), concentrated on one
tile (`results/T6_arm_a_numbers.json:step3.spike_at_one.per_tile.*`), at a mean
`fit_cost` of `results/T6_arm_a_numbers.json:step3.spike_at_one.mean_fit_cost` against
`results/T6_arm_a_numbers.json:step3.spike_at_one.mean_fit_cost_rest` on the rest.
Items whose above-prior ratio exceeds 1 are kept and counted:
`results/T6_arm_a_numbers.json:step3.conventions.degeneracies.n_above_prior_ratio_exceeding_1`.

2.5 **Robustness of the price against the frozen set's conflict enrichment.**
Descriptive, not a second estimate
(`results/T6_arm_a_numbers.json:step3.pool_robustness_check.status`). Conflict share
of the two bases: `results/T6_arm_a_numbers.json:step3.pool_robustness_check.conflict_share_frozen`
against `results/T6_arm_a_numbers.json:step3.pool_robustness_check.conflict_share_pool`,
and within the divergence set
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.conflict_share_within_divergence_set_frozen`
against `results/T6_arm_a_numbers.json:step3.pool_robustness_check.conflict_share_within_divergence_set_pool`.
Price on the pool's divergence set,
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.n_divergence_set_pool` items:
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.conventions.p1_post_norm.mean_of_per_item_ratios`.
Signed differences: `results/T6_arm_a_numbers.json:step3.pool_robustness_check.frozen_minus_pool.*`.
**Where the price appears as a population statement the pool figure is the one to
use**, by the same rule as 1.5.

2.6 **What predicts a low `beta_c`. EXPLORATORY.** Labelled at
`results/T6_arm_a_numbers.json:step4.status`. There is no preregistered prediction, no
threshold, and no `p` value below is a test. Say that before any coefficient.

- Rank correlations on the finite subset, strongest first: margin headroom
  `results/T6_arm_a_numbers.json:step4.spearman_beta_c_vs_property_finite_subset.margin_headroom.spearman`,
  posterior gap `results/T6_arm_a_numbers.json:step4.spearman_beta_c_vs_property_finite_subset.posterior_gap.spearman`,
  `fit_cost` `results/T6_arm_a_numbers.json:step4.spearman_beta_c_vs_property_finite_subset.fit_cost.spearman`,
  decision margin `results/T6_arm_a_numbers.json:step4.spearman_beta_c_vs_property_finite_subset.decision_margin.spearman`.
  Each is reported per tile as well, `...per_tile.*`, because a pooled rank statistic
  over four tiles can be carried by tile.
- OLS on `log beta_c`: `results/T6_arm_a_numbers.json:step4.ols_log_beta_c.r2`,
  `results/T6_arm_a_numbers.json:step4.ols_log_beta_c.n`, coefficients at
  `results/T6_arm_a_numbers.json:step4.ols_log_beta_c.coef.*` with standard errors
  `results/T6_arm_a_numbers.json:step4.ols_log_beta_c.se.*`. Sign convention stated at
  `results/T6_arm_a_numbers.json:step4.ols_log_beta_c.note`.
- Margin headroom is excluded from any claim about what makes an item diverge, because
  among the robust items it is a restatement of the definition; it is used only among
  finite items and only for magnitude:
  `results/T6_arm_a_numbers.json:step4.identity_check.note`.

2.7 **Existence and magnitude come apart. EXPLORATORY.** Labelled at
`results/T6_arm_a_numbers.json:step4.existence_vs_magnitude.status`, claim at
`results/T6_arm_a_numbers.json:step4.existence_vs_magnitude.claim`. Existence rate
spans `results/T6_arm_a_numbers.json:step4.existence_vs_magnitude.existence_rate_max_over_min`
across tiles while the median finite `beta_c` spans only
`results/T6_arm_a_numbers.json:step4.existence_vs_magnitude.median_beta_c_max_over_min_pool`.
The `|O|` mechanism check fails to reproduce the rate order
(`results/T6_arm_a_numbers.json:step4.mechanism_beyond_n_options.n_options_reproduces_rate_order`)
and so does distinct-fit-vector fraction
(`results/T6_arm_a_numbers.json:step4.mechanism_beyond_n_options.distinct_fraction_reproduces_rate_order`).
**The four-point caveat is reported with the ordering, not after it:**
`results/T6_arm_a_numbers.json:step4.mechanism_beyond_n_options.caveat`.

2.8 **The K2 gate fired, and what that cost.** K2 is the preregistered `fit_cost`
correlation gate. Pool Spearman: `results/T6_arm_a_numbers.json:step2.K2.spearman_pool`
against threshold `results/T6_arm_a_numbers.json:step2.K2.threshold`,
`results/T6_arm_a_numbers.json:step2.K2.fires`, reproducing the published value
`results/T6_arm_a_numbers.json:step2.K2.published`. Its consequence is that the
`beta_c`-stratified redraw does not happen and Arm B runs on Paper 1's frozen set, which
is P2-D4 and P2-D7 and is where the `n = 108` limitation in section 6 comes from. The
three optima coincide together, on Arm A's own base:
`results/T6_arm_a_numbers.json:step2.three_optima_coincidence.fit_cost_zero.robust_share`
against `results/T6_arm_a_numbers.json:step2.three_optima_coincidence.fit_cost_positive.robust_share`,
marginal `results/T6_arm_a_numbers.json:step2.three_optima_coincidence.marginal_robust_share`,
confirmed on the pool at
`results/T6_arm_a_numbers.json:step2.three_optima_coincidence.pool_check.fit_cost_zero.robust_share`.

**Needed and absent.** Nothing.

---

## 3. The coincidence

**Claim.** The adversary-aware optimum and Paper 1's salience pole are almost always
the same option, and where they separate, Paper 1's frontier coordinate is undefined.
This is a property of the signal space measured on frozen, model-free geometry before
any Paper 2 model output is read. It is the section that governs what sections 4, 5 and
7 may say.

**Three figures, three bases, each stated with its own base and never merged.**

3.1 **Divergence set, 460 items: 452 of 460.**
`results/T6_F0_headroom.json:n_o_star_inf_equals_o_fit` of
`results/T6_F0_headroom.json:n_divergence_set`, share
`results/T6_arm_a_numbers.json:step3.conventions.o_star_infinity_is_o_fit.share`.
Exceptions: `results/T6_F0_headroom.json:n_o_star_inf_differs_from_o_fit`, item ids at
`results/T6_F0_headroom.json:exception_item_ids`, by tile at
`results/T6_F0_headroom.json:exception_tiles`.
**Every one of the exceptions falls inside Paper 1's own span guard:**
`results/T6_arm_a_numbers.json:step3.conventions.o_star_infinity_is_o_fit.n_exceptions`
equals `results/T6_arm_a_numbers.json:step3.conventions.o_star_infinity_is_o_fit.n_exceptions_removed_by_p1_span_guard`.
So on every item where the frontier coordinate is defined,
`results/T6_arm_a_numbers.json:step3.conventions.o_star_infinity_is_o_fit.sb_at_oinf_exactly_zero`
of `results/T6_arm_a_numbers.json:step3.conventions.o_star_infinity_is_o_fit.sb_defined`,
the price on that coordinate is exactly 1, to within
`results/T6_arm_a_numbers.json:step3.conventions.o_star_infinity_is_o_fit.sb_price_max_shortfall_from_one`.
Guard reach: `results/T6_F0_headroom.json:salience_pole_on_p1_coordinate.n_removed_by_guard`
of `results/T6_F0_headroom.json:n_divergence_set`, at
`results/T6_F0_headroom.json:salience_pole_on_p1_coordinate.guard`.

3.2 **Confirmatory set, 108 items: 108 of 108. This is the figure that governs Arm B.**
`results/T6_F0_headroom.json:exception_tiles` puts **zero** of the eight exceptions on
`size`, and the `size` divergence count is
`results/T6_arm_a_numbers.json:step2.per_tile_finite_count.size`. So `o*_infinity` is
`o_fit` on all 108. The figure is bound as
`p2_decisions.P2D26_CONFIRMATORY_COINCIDENCE` and asserted against the artifact by
`p2_decisions.bind_adversary_tracking_claim`, which also **refuses a caller that cites
452 of 460 for the confirmatory set**. The same rule binds prose: 3.1 and 3.2 are
stated as two figures on two named bases, and the divergence-set figure is never
substituted for the confirmatory one, because it understates it.
Corroborated on the floored confirmatory set of
`results/T7_control_marginal_null.json:salience_reference.n` items, where the salience
reference sits at `A = 1` on
`results/T7_control_marginal_null.json:salience_reference.n_exactly_1` of them,
`results/T7_control_marginal_null.json:salience_reference.share_exactly_1`, with
`results/T7_control_marginal_null.json:salience_reference.coincides_with_the_adversary_oracle`.

3.3 **Pool-wide, 36,464 divergent items: all 2,748 separating items sit inside Paper
1's span guard.**
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.conventions.o_star_infinity_is_o_fit.n_exceptions`
of `results/T6_arm_a_numbers.json:step3.pool_robustness_check.conventions.o_star_infinity_is_o_fit.n_total`,
coincidence share
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.conventions.o_star_infinity_is_o_fit.share`,
and the counting result that carries the ruling:
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.conventions.o_star_infinity_is_o_fit.n_exceptions_removed_by_p1_span_guard`
**equals** the exception count. On the
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.conventions.o_star_infinity_is_o_fit.sb_defined`
items where the coordinate is defined, the price is exactly 1 on all of them, to within
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.conventions.o_star_infinity_is_o_fit.sb_price_max_shortfall_from_one`.
Guard reach on the pool:
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.conventions.degeneracies.n_salience_span_at_or_below_guard`.

3.4 **What the coincidence is and is not.** These are different functions and the
coincidence is not an identity; the exceptions exist and are counted. The record of
that, in the artifact's own words:
`results/T6_arm_a_numbers.json:step3.conventions.o_star_infinity_is_o_fit.note`. The
reading it licenses is about where the normative optimum moves inside Paper 1's
interval, and it is adjacent to Paper 1's finding about where models sit relative to
that interval. It is not the same claim and nothing in this section measures a model.

**Needed and absent.** The confirmatory figure is not a single key in any
`results/*.json`. It resolves from two keys read together, both cited at 3.2, and it is
carried as a bound constant in `src/p2_decisions.py`. Nothing was computed for this.
If a single emitted key is wanted, that is a new emission and is **not made here**.

---

## 4. Arm B, what it shows

**Claim.** The framings changed the chosen option. That claim reads chosen options
only, is tested against an exact zero rather than against an estimated baseline, and
holds on every one of the fourteen model-by-framing cells. It carries no claim about
direction and none is made.

**Sub-claims and sources.**

4.1 **The null is exactly zero, and that is now measured rather than argued.** Paper
1's chooser is an argmax over teacher-forced log-probabilities with no sampling, so the
no-effect same-option rate is exactly 1.0:
`results/T5_c5_effect.json:no_effect_same_option_rate`, provenance at
`results/T5_c5_effect.json:no_effect_rate_provenance`, residual risk named at
`results/T5_c5_effect.json:residual`. T7's `F0` re-run is the repeated rendering that
could not previously exist: `results/T7_f0_replication.json:closes_v26_section_1_1`.
On the confirmatory tile, `results/T7_f0_replication.json:environment_equivalence.confirmatory_disagreeing_items`
disagreements over `results/T7_f0_replication.json:environment_equivalence.confirmatory_renderings`
renderings, per model at `results/T7_f0_replication.json:confirmatory_tile_summary.*`.
**Report the verdict as it is worded**,
`results/T7_f0_replication.json:environment_equivalence.verdict`: choice-level output
identity on the confirmatory tile, environment identity **not** established
(`results/T7_f0_replication.json:environment_equivalence.p1_env_found`). Off the
confirmatory tile the rate is nonzero and is reported beside Paper 1's own batch-flip
rate: `results/T7_f0_replication.json:off_confirmatory_summary.*`.

4.2 **The floor, and that it was not revised.** Floor
`results/T7_armb_quantities.json:inertness_floor.value`, provisional
`results/T7_armb_quantities.json:inertness_floor.provisional`, measured disagreement
count `results/T7_armb_quantities.json:inertness_floor.f0_versus_cond4_disagreement_items`,
`results/T7_armb_quantities.json:inertness_floor.revised`. **It is not a significance
threshold and must not be described as one:**
`results/T7_armb_quantities.json:inertness_floor.is_statistical` and
`results/T7_armb_quantities.json:inertness_floor.what_it_is`. The upward-only rule is
structural: `results/T5_armb_floor.json:floor.rule`,
`results/T5_armb_floor.json:floor.revision_is_upward_only`. The caveat that the `F0`
rate is a lower bound on the noise floor is reported, not scaled away:
`results/T5_armb_floor.json:floor.caveat`.

4.3 **Quantity (a) on all fourteen cells.** Full table:
`results/T7_armb_quantities.json:cells.*.a_inertness.n_items_with_a_changed_pair`,
with rates `results/T7_armb_quantities.json:cells.*.a_inertness.change_rate_item_mean`,
bootstrap lower bounds `results/T7_armb_quantities.json:cells.*.a_inertness.ci_lo`,
and the two verdict flags
`results/T7_armb_quantities.json:cells.*.a_inertness.interval_excludes_zero` and
`results/T7_armb_quantities.json:cells.*.a_inertness.clears_the_floor`, every one of
them true. The range runs from
`results/T7_armb_quantities.json:cells.L1|F1.a_inertness.n_items_with_a_changed_pair`
to `results/T7_armb_quantities.json:cells.B4|F2.a_inertness.n_items_with_a_changed_pair`
of `results/T7_armb_quantities.json:n_confirmatory`. Instrument:
`results/T5_inertness_ceiling.json:quantity_a_inertness.instrument`, null and its reason
at `results/T5_inertness_ceiling.json:quantity_a_inertness.null` and
`results/T5_inertness_ceiling.json:quantity_a_inertness.why_zero_is_the_null`.

4.4 **The item denominator is 108 on every cell, and the attrition is reported rather
than absorbed.** `results/T7_armb_quantities.json:cells.*.attrition_P2D16.item_denominator`,
with `results/T7_armb_quantities.json:cells.*.attrition_P2D16.pairs_excluded_for_a_tie`,
`results/T7_armb_quantities.json:cells.*.attrition_P2D16.items_with_one_surviving_pair`
and `results/T7_armb_quantities.json:cells.*.attrition_P2D16.items_with_no_surviving_pair`.
Parse failures are structurally zero and the reason is stated rather than the number
alone: `results/T7_armb_quantities.json:cells.CTRL|F1.attrition_P2D16.parse_failures_note`.

4.5 **Quantity (b), magnitude context, descriptive and gating nothing.** Role:
`results/T7_armb_quantities.json:cells.*.b_magnitude_context.role`. Reference `R_m` per
model: `results/T7_armb_quantities.json:reference_R_m.*`, and `R_m` is an **active**
comparator, not a baseline: `results/T5_c5_effect.json:verdict.reading`,
`results/T5_c5_effect.json:verdict.change_rate_range` on
`results/T5_c5_effect.json:verdict.models` models, every interval excluding the
no-effect rate. Per-cell differences
`results/T7_armb_quantities.json:cells.*.b_magnitude_context.difference_framing_minus_c5`
and resolution flags `results/T7_armb_quantities.json:cells.*.b_magnitude_context.resolves`.
**It resolves on three cells and not on eleven, and the sentence names both counts.**
The three: `results/T7_armb_quantities.json:cells.L3|F1.b_magnitude_context.difference_framing_minus_c5`,
`results/T7_armb_quantities.json:cells.B2|F2.b_magnitude_context.difference_framing_minus_c5`,
`results/T7_armb_quantities.json:cells.L3|F2.b_magnitude_context.difference_framing_minus_c5`,
all in the direction of the framing moving choices more than `c5` does. Instrument
resolution, stated in advance rather than discovered:
`results/T7_armb_quantities.json:detection_limits_P2D11.quantity_b_half_width_range`,
`results/T7_armb_quantities.json:detection_limits_P2D11.statement`.
**Do not compress the three and the eleven into one magnitude word.**

4.6 **The 142-item control, bounding attribution.** Base and why it is that base:
`results/T7_control_marginal_null.json:control_bases.primary.n_items`,
`results/T7_control_marginal_null.json:control_bases.primary.tile`,
`results/T7_control_marginal_null.json:control_bases.primary.arity`,
`results/T7_control_marginal_null.json:control_bases.primary.why`. Total variation
distance between the `F0` and arm option marginals on that set, per cell:
`results/T7_control_marginal_null.json:cells.*.control_TV.value`, with the signed shift
`results/T7_control_marginal_null.json:cells.*.control_TV.signed_shift`. **The 540-item
figure across all four tiles is reported beside it with its base named, never alone:**
`results/T7_control_marginal_null.json:cells.*.control_TV.all_tiles_value`,
`results/T7_control_marginal_null.json:control_bases.reported_beside.n_items`,
per tile at `results/T7_control_marginal_null.json:control_TV_by_tile.CTRL|F1.*`, and
the reason no marginal is pooled across arities,
`results/T7_control_marginal_null.json:cells.CTRL|F1.control_TV.all_tiles_base`.
**What the control can and cannot do is stated with it:**
`results/T7_control_marginal_null.json:cells.CTRL|F1.control_TV.role` and
`results/T7_control_marginal_null.json:cells.CTRL|F1.control_TV.what_it_cannot_say`.
On these items `o*_0 = o*_infinity`, so there is nothing for an adversary-aware model
to move toward and any change in the choice distribution is prompt sensitivity. It
bounds attribution qualitatively. It does not size how much of the confirmatory
movement it explains, and no quantity in the design does.

**The control change rate, beside quantity (a), in the same units. EXPLORATORY
(P2-D27):** `results/T7_control_change_rate.json:standing`. Same instrument as (a),
`results/T7_control_change_rate.json:instrument`, on the 142:
`results/T7_control_change_rate.json:control_base.n_items`. Per cell, the control rate
`results/T7_control_change_rate.json:cells.*.control_change_rate.change_rate_renderings`
and `results/T7_control_change_rate.json:cells.*.control_change_rate.change_rate_item_mean`
beside (a)'s `results/T7_armb_quantities.json:cells.*.a_inertness.change_rate_renderings`
and `results/T7_armb_quantities.json:cells.*.a_inertness.change_rate_item_mean`; the
item counts
`results/T7_control_change_rate.json:cells.*.control_change_rate.n_items_with_a_changed_pair`
of `results/T7_control_change_rate.json:cells.*.control_change_rate.item_denominator`
beside (a)'s `results/T7_armb_quantities.json:cells.*.a_inertness.n_items_with_a_changed_pair`
of `results/T7_armb_quantities.json:cells.*.a_inertness.item_denominator`; control
attrition at `results/T7_control_change_rate.json:cells.*.attrition_P2D16`. Each cell
names its (a) counterpart: `results/T7_control_change_rate.json:cells.*.quantity_a_same_cell`.
The interval is emitted as (a)'s is and carries no inferential role; no floor and no
verdict flag is attached: `results/T7_control_change_rate.json:not_emitted`.
**The comparability sentence, verbatim wherever the two appear together**
(`results/T7_control_change_rate.json:comparison_sentence`): the control change rate
and quantity (a) are reported side by side in the same units and are not comparable as
an attribution: they are taken on disjoint item sets that differ by construction in
whether the adversary can move the optimum, no preregistered rule transfers a rate from
one to the other, and no difference, ratio or share of the two is reported. The TV of
record never exceeds the change rate on the cells where both were formed on identical
renderings, `results/T7_control_change_rate.json:tv_bound_check.premise_holds_on`, and
that premise fails on `results/T7_control_change_rate.json:tv_bound_check.premise_does_not_hold_on`.

4.7 **The oracle check, reported because beating the oracle would be a bug.**
`results/T7_armb_quantities.json:oracle_check.n_chosen_options_above_the_adversary_oracle`
over `results/T7_armb_quantities.json:oracle_check.renderings_checked`, with
`results/T7_armb_quantities.json:oracle_check.max_A_over_chosen_options` and the reason
the bound is structural, `results/T7_armb_quantities.json:oracle_check.bound_is`. Same
check on the control artifact:
`results/T7_control_marginal_null.json:oracle_check.n_chosen_options_above_the_adversary_oracle`.

**Needed and absent.** Nothing for the control. The **change rate on the 142-item
control set**, in quantity (a)'s units and from its instrument, is authorized by P2-D27
as exploratory and descriptive and is now computed, `results/T7_control_change_rate.json:cells.*.control_change_rate`,
and is placed beside (a) in section 4.6. P2-D25 did not address it; it neither declined
nor authorized one. `results/T7_control_marginal_null.json:steps_not_run.step_4_control_change_rate`
records the computing session's reading of that silence under its own instruction, not
a ruling (P2-D27). No difference, ratio or share of the control rate and (a) exists or
is authorized, and section 4.6 states neither as a share of the other.

---

## 5. Arm B, what it cannot show, and why

**Claim, and the shape it must have.** Arm B cannot say what the movement was toward,
and the reason is structural and was fixed before any model was run. On the
confirmatory set the adversary-aware optimum and the salience pole are the same option
on all 108 items (section 3.2), so no function of a chosen option can separate two
labels attached to one option. **The direction question was never answerable on this
set.** That is not a null result and must not be written as one: the experiment did not
look for a direction effect and fail to find one, it could not have found one, and the
counting result in section 3 is why.

**Sub-claims and sources.**

5.1 **P2-D26's structural ground.** The confirmatory coincidence is section 3.2's
figure. The discharge is structural, not pending measurement, and the tile is not
revisitable: `p2_decisions.P2D26_BLOCKER_DISCHARGED`,
`p2_decisions.P2D26_DISCHARGE_IS_STRUCTURAL`,
`p2_decisions.P2D26_ADVERSARY_TRACKING_CLAIM_AVAILABLE`,
`p2_decisions.P2D26_TILE_REVISITABLE`, all bound to the decision text in
`docs/P2/DECISIONS.md` P2-D26 and asserted by `bind_adversary_tracking_claim`.
**No successor measure on `size` helps.** The separation is absent from the item set,
not from the coordinate.

5.2 **P2-D24 reached the same place from three independent premises, and is explained
rather than superseded.** Ruling and the two flags:
`results/T7_armb_quantities.json:direction_reading_P2D24.ruling`,
`results/T7_armb_quantities.json:direction_reading_P2D24.direction_claim_licensed`,
`results/T7_armb_quantities.json:direction_reading_P2D24.movement_claim_licensed`.
The three premises, each independently sufficient and each still true:
`results/T7_armb_quantities.json:direction_reading_P2D24.premise_1_excess_over_the_marginal_null`,
`results/T7_armb_quantities.json:direction_reading_P2D24.premise_2_the_neutral_baseline`,
`results/T7_armb_quantities.json:direction_reading_P2D24.premise_3_the_discarded_switches`.
Independence from how P2-D5's blocker went:
`results/T7_armb_quantities.json:direction_reading_P2D24.independent_of_the_blocker`.

5.3 **Nothing is withheld. Quantity (c) is reported in full and its sign is what is
unread.** Per cell:
`results/T7_armb_quantities.json:cells.*.c_direction.n_eff_item`,
`results/T7_armb_quantities.json:cells.*.c_direction.sign_proportion_item`,
`results/T7_armb_quantities.json:cells.*.c_direction.p_two_sided_item`,
`results/T7_armb_quantities.json:cells.*.c_direction.significant_at_corrected_alpha_item`,
`results/T7_armb_quantities.json:cells.*.c_direction.ci95_item`,
`results/T7_armb_quantities.json:cells.*.c_direction.tie_rate_item`, at unit
`results/T7_armb_quantities.json:cells.CTRL|F1.c_direction.unit`, null
`results/T7_armb_quantities.json:p0`, family `alpha`
`results/T7_armb_quantities.json:alpha`. Five cells resolve:
`results/T7_armb_quantities.json:direction_reading_P2D24.resolving_cells`, all in one
direction, `results/T7_armb_quantities.json:direction_reading_P2D24.resolving_all_downward`.
**The statistic is reported and the reading of its sign is what is blocked**, which is
what makes this a structural limit rather than an absence of evidence. Withholding the
numbers was considered and rejected (P2-D24 alternative 3).

5.4 **The marginal null was computed, and it is descriptive.**
`A_null` and observed `A` per model and framing:
`results/T7_control_marginal_null.json:reference_placement.CTRL.F0.A_null_median_of_per_item`,
`results/T7_control_marginal_null.json:reference_placement.CTRL.F0.A_observed_median_of_per_item`,
excess at `results/T7_control_marginal_null.json:reference_placement.CTRL.F0.excess_median`
and `...excess_from_the_means`, both aggregates reported per `v2.0` section 3.2. Its
standing is emitted with it:
`results/T7_control_marginal_null.json:reference_placement.CTRL.F0.excess_is`, and the
family is unchanged,
`results/T7_control_marginal_null.json:confirmatory_family_size` at
`results/T7_control_marginal_null.json:alpha_unchanged`. **No mapping onto quantity (c)
exists and none may be written.** The reference set the placement is read against:
`results/T7_control_marginal_null.json:reference_set.bayes_oracle`,
`results/T7_control_marginal_null.json:reference_set.adversary_oracle`,
`results/T7_control_marginal_null.json:reference_set.note`.

5.5 **The preregistered defence has no successor, and its absence is the finding.**
`v2.0` section 4.4's attribution cap is applied unchanged to the descriptive mean it
was written for, and its own defect is named rather than repaired: per cell
`results/T7_control_marginal_null.json:cells.*.attribution_cap.dA_null`,
`results/T7_control_marginal_null.json:cells.*.attribution_cap.observed_mean_dA`,
`results/T7_control_marginal_null.json:cells.*.attribution_cap.observed_median_dA`,
verdict `results/T7_control_marginal_null.json:cells.*.attribution_cap.cap_is`, standing
`results/T7_control_marginal_null.json:cells.CTRL|F1.attribution_cap.standing`, the
criterion it came from
`results/T7_control_marginal_null.json:cells.CTRL|F1.attribution_cap.criterion`, and the
mixture defect that reaches both sides of the comparison
`results/T7_control_marginal_null.json:cells.CTRL|F1.attribution_cap.P2D6_mixture_defect`.
**Arm B's confirmatory family carries no defence against the generic-shift hypothesis
and cannot acquire one.** State that as a finding, not as a caveat.

5.6 **What was not run, and under which clause.** Steps 4, 5 and 6 of T7 are not all
issued, and the reason is recorded per step rather than left as a gap:
`results/T7_control_marginal_null.json:steps_not_run.step_5_direction_and_verdict`,
`results/T7_control_marginal_null.json:steps_not_run.step_6_size_ladder`,
`results/T7_control_marginal_null.json:steps_not_run.menu_position_marginal`. A size
ladder is a statement about whether a model tracks the adversary, which is exactly the
claim section 3.2 makes unavailable.

5.7 **The (4,5) signature is on canonical option ids and is not menu-position
evidence.** The concentration itself is at 6.3. What it is a signature of was corrected
by P2-D25: `chosen_option` is a canonical id and Paper 1's Format V permutes the menu
per item and per permutation, so a menu-position preference would not produce it.
Corrected reading and the rejection of a position-shaped quantity:
`results/T7_control_marginal_null.json:steps_not_run.menu_position_marginal`.
`tests/test_p2d25_marginal_null.py` recomputes the menu-position spread from Paper 1's
frozen renderings rather than trusting a quoted figure.

**Needed and absent.** Nothing this section claims. It claims an absence, and the
absence is the thing that is emitted.

---

## 6. Limitations

**Claim.** Five limitations, each stated with its base and its size, none of them
repaired by anything the design can do. They are stated as properties of the item set
and the coordinate, never as properties of a model.

6.1 **`n = 108`, against a preregistered benchmark of 400.**
`results/T7_armb_quantities.json:detection_limits_P2D11.n_realized` against
`results/T7_armb_quantities.json:detection_limits_P2D11.n_benchmark`, also at
`results/T5_detection_ceiling.json:limit_3_information.n_adopted` and
`results/T5_detection_ceiling.json:limit_3_information.n_benchmark_v2_0_section_8_2`,
statement at `results/T5_detection_ceiling.json:limit_3_information.statement`. The
shortfall is a stated limitation and not a repaired one: the redraw was declined
(P2-D4, P2-D7) because sizing it required a quantity that is not observable before the
arm runs. Realized power is reported at the observed effective `n` rather than assumed:
`results/T7_armb_quantities.json:cells.*.c_direction.realized_power_at.0.75`,
`results/T7_armb_quantities.json:cells.*.c_direction.realized_p1_at_80_power`,
`results/T7_armb_quantities.json:cells.*.c_direction.n_eff_item`. `sigma` does not enter
the confirmatory curve and the exchange is stated rather than presented as a saving:
`results/T5_sign_power.json:sigma_enters`,
`results/T5_sign_power.json:unknown_exchanged`, and the defect that the sign test has
least power exactly where the predicted null is true,
`results/T5_sign_power.json:power_is_lowest_where_the_null_is_true`. No SESOI is
invented: `results/T5_sign_power.json:sesoi`.

6.2 **`A`-invisibility, on the per-pair base.** The **primary** figure is per option
pair: `results/T5_tie_reference.json:a_invisibility_at_p1_eps.size_tile_confirmatory.n_A_tied_option_pairs`
of `results/T5_tie_reference.json:a_invisibility_at_p1_eps.size_tile_confirmatory.n_unordered_option_pairs`,
which is `results/T5_tie_reference.json:a_invisibility_at_p1_eps.size_tile_confirmatory.share_option_pairs_invisible_to_A`,
against `results/T5_tie_reference.json:a_invisibility_at_p1_eps.divergence_set.share_option_pairs_invisible_to_A`
pooled over the divergence set. The base is named in the artifact itself:
`results/T5_tie_reference.json:a_invisibility_at_p1_eps.size_tile_confirmatory.share_option_pairs_invisible_to_A_is`.
The per-item figure,
`results/T5_tie_reference.json:a_invisibility_at_p1_eps.size_tile_confirmatory.n_items_with_an_A_tied_option_pair`
of `results/T5_tie_reference.json:a_invisibility_at_p1_eps.size_tile_confirmatory.n_items`
at `results/T5_tie_reference.json:a_invisibility_at_p1_eps.size_tile_confirmatory.share_items_with_an_A_tied_option_pair`,
counts items containing **at least one** tied pair among fifteen and is inflated by
option count. Its own artifact says so:
`results/T5_tie_reference.json:a_invisibility_at_p1_eps.size_tile_confirmatory.share_items_with_an_A_tied_option_pair_is`.
**It is reported beside the per-pair figure, with its base named, and never alone or
first.** Also stated together in the Arm B artifact:
`results/T7_armb_quantities.json:a_tie_resolution_P2D19.primary_per_pair`,
`results/T7_armb_quantities.json:a_tie_resolution_P2D19.secondary_per_item`,
`results/T7_armb_quantities.json:a_tie_resolution_P2D19.note`.
The tolerance is Paper 1's, inherited and not chosen
(`results/T7_armb_quantities.json:a_tie_resolution_P2D19.eps`), and the gap it sits in
is many orders wide, so every tolerance strictly inside it classifies identically and
the choice within that range is not a choice: the smallest gap the tolerance does not
absorb is
`results/T5_tie_reference.json:a_invisibility_at_p1_eps.size_tile_confirmatory.next_gap_above_eps`,
against the exact-equality reading's
`results/T5_tie_reference.json:a_invisibility.size_tile_confirmatory.next_gap_above_eps`.
The two readings give
`results/T5_tie_reference.json:a_invisibility.size_tile_confirmatory.n_A_tied_option_pairs`
pairs and
`results/T5_tie_reference.json:a_invisibility_at_p1_eps.size_tile_confirmatory.n_A_tied_option_pairs`
pairs on the same geometry, and the exact-equality figures stay emitted unchanged
because superseded documents cite them.
**`size` is the worst tile for this, on both bases:**
`results/T5_tie_reference.json:a_invisibility_by_tile_at_p1_eps.size.share_option_pairs_invisible_to_A`
against `results/T5_tie_reference.json:a_invisibility_by_tile_at_p1_eps.manmade.share_option_pairs_invisible_to_A`,
`results/T5_tie_reference.json:a_invisibility_by_tile_at_p1_eps.hold.share_option_pairs_invisible_to_A`
and `results/T5_tie_reference.json:a_invisibility_by_tile_at_p1_eps.moves.share_option_pairs_invisible_to_A`.
**This is a limitation of the coordinate. It is not a reason to revisit the tile**,
which Paper 1's D49 and D108 fixed on measured grounds before any of this was known and
which would be a frozen-artifact change.

6.3 **Switch concentration: the per-pair bound understates the realized blind spot on
some cells and overstates it on others.** The assumption the bound rests on was checked
rather than assumed. Per cell:
`results/T7_switch_concentration.json:per_cell.CTRL/F1.concentration_ratio` and the same
key across `results/T7_switch_concentration.json:per_cell.*`, with the switch counts
`results/T7_switch_concentration.json:per_cell.CTRL/F1.n_switches` and
`results/T7_switch_concentration.json:per_cell.CTRL/F1.n_switches_on_an_A_tied_pair`,
the bound at `results/T7_switch_concentration.json:per_pair_bound`, and the reading rule
at `results/T7_switch_concentration.json:reading`. **The answer is model-split**, which
is the finding: the ratio runs above 1 on some cells and below on others. Three of the
five cells that resolve on quantity (c) sit in the high group, at
`results/T7_armb_quantities.json:direction_reading_P2D24.concentrated_resolving_cells`
and `results/T7_armb_quantities.json:direction_reading_P2D24.concentration_ratio_on_those_cells`.
**Cite the range over the resolving cells, not the range over all six concentrated
cells**, and name which set each range is over: the largest ratio in the file,
`results/T7_switch_concentration.json:per_cell.CTRL/F2.concentration_ratio`, is on a
cell that does **not** resolve. The option pairs the discarded switches land on:
`results/T7_switch_concentration.json:per_cell.CTRL/F1.tied_switch_option_pairs` and
across `results/T7_switch_concentration.json:per_cell.*`. This is selection, not
measurement error: nothing establishes that the discarded switches carry the direction
of the retained ones.

6.4 **The three-way mixture on `A`, which is why the mean is descriptive.** `A` divides
by `ext_i`, so an option well below `o*_0` on normalized margin is arithmetically far
negative and that is normal. Poles and off-pole median:
`results/T6_F0_headroom.json:coordinate_geometry.median_A_at_bayes_pole`,
`results/T6_F0_headroom.json:coordinate_geometry.median_A_at_salience_pole`,
`results/T6_F0_headroom.json:coordinate_geometry.median_A_off_pole`, with
`results/T6_F0_headroom.json:coordinate_geometry.median_ext_on_divergence_set` and the
artifact's own statement of the shape,
`results/T6_F0_headroom.json:coordinate_geometry.note`. The leverage that makes a mean
unusable, over `results/T6_F0_headroom.json:delta_A_leverage.n_ordered_option_pairs`
admissible ordered option pairs:
`results/T6_F0_headroom.json:delta_A_leverage.share_abs_delta_A_exceeding.1` exceed the
target move of `+1` in magnitude and
`results/T6_F0_headroom.json:delta_A_leverage.share_abs_delta_A_exceeding.10` exceed it
tenfold, with the reading at
`results/T6_F0_headroom.json:delta_A_leverage.leverage_reading` and the decomposition by
move kind at `results/T6_F0_headroom.json:delta_A_leverage.by_kind.pole_to_pole.share`,
`results/T6_F0_headroom.json:delta_A_leverage.by_kind.mixed.share`,
`results/T6_F0_headroom.json:delta_A_leverage.by_kind.off_to_off.share`.
**The status line is emitted and belongs in the sentence:**
`results/T6_F0_headroom.json:delta_A_leverage.status`. This is a measurement of the
coordinate and not of any model. The consequence is that the mean is descriptive and
the confirmatory instrument is a change rate plus a sign test.
**Negative mean `A` is not reported as a finding.** The leave-one-item-out test says
why: `results/T6_F0_headroom.json:residual_test_reading.question`,
`results/T6_F0_headroom.json:residual_test_reading.answer`,
`results/T6_F0_headroom.json:residual_test_reading.consequence`, with the correction
family at `results/T6_F0_headroom.json:residual_multiple_comparisons.n_comparisons` and
`results/T6_F0_headroom.json:residual_multiple_comparisons.n_outside_95_band`.

6.5 **The neutral baseline, stated directly and never as a tally.** The claim is: a
content-neutral insertion does not drift toward the salience pole. Per-model
proportions at P2-D20's item unit:
`results/T5_inertness_ceiling.json:diagnostic_c5_direction.answer_at_item_unit_p2d21.sign_proportion.*`,
range at `results/T5_inertness_ceiling.json:diagnostic_c5_direction.answer_at_item_unit_p2d21.range_all_seven`.
**Only `CTRL` resolves at the corrected `alpha` and it resolves downward:**
`results/T5_inertness_ceiling.json:diagnostic_c5_direction.answer_at_item_unit_p2d21.significant_at_corrected_alpha`.
**`B2` sits at the null**, and that is measured rather than conceded:
`results/T5_armb_floor.json:type_ii_cost_of_p0_half_at_item_unit.per_model.B2.ci95`,
`results/T5_armb_floor.json:type_ii_cost_of_p0_half_at_item_unit.per_model.B2.p_two_sided`,
`results/T5_armb_floor.json:type_ii_cost_of_p0_half_at_item_unit.per_model.B2.n_eff`, and
the reading at
`results/T5_armb_floor.json:type_ii_cost_of_p0_half_at_item_unit.b2_is_not_evidence_of_upward_drift`.
**Forbidden phrasings, and they are forbidden rather than discouraged:** do not write
"at or below 0.5 on six of seven models", which is a smaller universal that hands the
reader an exception with no resolution; do not describe `B2` as drifting upward; do not
call `p0 = 0.5` conservative anywhere, because conservativeness is a per-model property
and it does not hold on `B2`. `p0 = 0.5` stands on the structural ground:
`results/T5_inertness_ceiling.json:diagnostic_c5_direction.answer_at_item_unit_p2d21.p0_is_retained_on`,
`results/T5_armb_floor.json:type_ii_cost_of_p0_half_at_item_unit.p0_moved`.
**The signed gap goes with every (c) verdict**, not in a footnote:
`results/T5_armb_floor.json:type_ii_cost_of_p0_half_at_item_unit.per_model.*.gap_to_p0`,
range at `results/T5_armb_floor.json:type_ii_cost_of_p0_half_at_item_unit.gap_range`,
per cell at `results/T7_armb_quantities.json:cells.*.c_direction.type_ii_gap_signed` with
the flag `results/T7_armb_quantities.json:cells.*.c_direction.gap_is_a_type_ii_cost`.
On `B2` the gap is negative, which is not a smaller Type II cost but a Type I exposure,
and it is named beside `B2`'s verdict:
`results/T5_armb_floor.json:type_ii_cost_of_p0_half_at_item_unit.models_with_baseline_above_p0`,
`results/T7_armb_quantities.json:cells.B2|F1.c_direction.type_i_exposure`,
`results/T5_inertness_ceiling.json:diagnostic_c5_direction.answer_at_item_unit_p2d21.negative_gap_is_not_a_smaller_cost`.
The preregistered conditional that fired was discharged by reconsidering and retaining,
not by reading the antecedent away:
`results/T5_inertness_ceiling.json:diagnostic_c5_direction.answer_at_item_unit_p2d21.preregistered_conditional_that_fired`.
**Superseded pair-unit strings are not corrected in place**; `v2.7` and `v2.8` still
reproduce, and the live figures are the item-unit ones.

6.6 **The coordinate's blind spot on the movement half, measured on a real
manipulation.** `results/T5_inertness_ceiling.json:diagnostic_blind_spot_measured.definition`,
range `results/T5_inertness_ceiling.json:diagnostic_blind_spot_measured.range`, per model
`results/T5_inertness_ceiling.json:diagnostic_blind_spot_measured.per_model.*`, and per
Arm B cell `results/T7_armb_quantities.json:cells.*.blind_spot_P2D10.gap`.

**6.4's three-way mixture, now emitted, and it is two partitions, not one.** On the
same `results/T6_F0_headroom.json:coordinate_geometry.n_option_level_pairs` option cells:

- **By P1's `sb` poles**, which is where the recorded figures come from and the split the
  pole medians above use:
  `results/T6_F0_headroom.json:coordinate_geometry.n_option_cells_by_p1_pole.bayes_pole_sb_1`,
  `results/T6_F0_headroom.json:coordinate_geometry.n_option_cells_by_p1_pole.salience_pole_sb_0`,
  `results/T6_F0_headroom.json:coordinate_geometry.n_option_cells_by_p1_pole.off_pole`,
  with the off-pole median `results/T6_F0_headroom.json:coordinate_geometry.median_A_off_pole`.
- **By `A`'s own value**:
  `results/T6_F0_headroom.json:coordinate_geometry.n_option_cells_by_A_value.A_exactly_0`,
  `results/T6_F0_headroom.json:coordinate_geometry.n_option_cells_by_A_value.A_exactly_1`,
  `results/T6_F0_headroom.json:coordinate_geometry.n_option_cells_by_A_value.other`.

**The drafter must name which partition a sentence uses.** P2-D6's reasoning and `T7.md`
describe the recorded figures as cells "at exactly 0" and "exactly 1" of `A`, but they
are the `sb`-pole split; split by `A` itself the counts differ. The near-trichotomy the
argument rests on holds under both, so no conclusion moves; the wording does. The
recorded prose is not edited here.

---

## 7. Future work

**Claim.** Arm C is ruled out in this design, and the requirement it would need is
stated precisely rather than gestured at. It needs two things at once, and the counting
result in section 3 says the current item set supplies neither together.

7.1 **The requirement, stated precisely.** An Arm C would need (i) an item set on which
the adversary-aware optimum and the salience pole are **different options** on a
non-trivial fraction of items, and (ii) a coordinate that is **defined** on those
items. The frozen set supplies (i) on
`results/T6_F0_headroom.json:n_o_star_inf_differs_from_o_fit` items and supplies (ii) on
none of them, because all of them fall inside Paper 1's span guard:
`results/T6_arm_a_numbers.json:step3.conventions.o_star_infinity_is_o_fit.n_exceptions_removed_by_p1_span_guard`.
Pool-wide the same identity holds at scale:
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.conventions.o_star_infinity_is_o_fit.n_exceptions`
separating items, and
`results/T6_arm_a_numbers.json:step3.pool_robustness_check.conventions.o_star_infinity_is_o_fit.n_exceptions_removed_by_p1_span_guard`
of them inside the guard. **So the separation and the coordinate do not co-occur
anywhere in this signal space as currently measured.** An Arm C on this space would
inherit the collapse, which is the ruling this outline is written under.

7.2 **Where the separating items sit, and why that is not a fix.** By tile:
`results/T6_F0_headroom.json:exception_tiles`. They are on the two tiles Paper 1's D108
found carry approximately nothing, and none is on the confirmatory tile. Moving the
confirmatory tile to reach them is closed on three independent grounds: D49 selected
`size` on `fit_cost` coverage and D108 confirmed the primary curve rests on it alone,
both before any of this was known; the separating items are on the tiles D108 excluded;
and it would be a frozen-artifact change. **This section proposes no Arm C design and
selects no item set.**

7.3 **What an item set would have to be built against, stated as open.** The
`fit`-geometry property that makes `o*_infinity` differ from `o_fit` while leaving the
frontier span above the guard is not characterised. Section 2.6's exploratory
regression predicts `beta_c`, which is a different quantity: it says how much adversary
budget an item needs, not whether the two targets separate. Nothing in `results/`
regresses separation on item properties, and nothing here does either.

**Needed and absent.** A regression or characterisation of **which item properties
produce a separating item with a defined frontier coordinate** is **not in `results/`**
and is the quantity a future Arm C design would be sized against. It is named here and
**not computed**. Computing it is a new measurement on the pool, and it is not
authorized by anything in the record.

---

## What this outline does not do

- It does not reopen any decision, propose an Arm C design, or select an item set.
- It records no decision, adds no `P2-D` number, and writes no preregistration version.
- It computes nothing. Every figure above was read from `results/`; every figure a
  section needs and `results/` does not carry is flagged under **Needed and absent** and
  left uncomputed.
- It drafts no paper prose. Each section states the claim and its sources; the wording
  is the paper's to write, under `CLAUDE.md`'s conventions and, for the human-behaviour
  gap in related work, under the wording `docs/P2/tasks/T4.md` fixes and not a broader
  one.
