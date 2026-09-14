"""T7 confirmatory analysis: Arm B's three quantities per (model, framing) cell.

P2-D12 fixes three quantities and none of them gates another, on the 108-item
`size` confirmatory set (P2-D3, P2-D4), for the `F1`-versus-`F0` and
`F2`-versus-`F0` contrasts:

  (a) INERTNESS        the same-option change rate against ZERO, at full `n`,
                       with P2-D8's cluster bootstrap. Zero is the exact null
                       because P1's scorer is an argmax over teacher-forced
                       log-probabilities with no sampling (P2-D9), so the cell
                       clears the floor by carrying changed renderings on at
                       least `floor` items, and the floor is NUMERICAL rather
                       than statistical (P2-D13).

  (b) MAGNITUDE CONTEXT  the same-option rate against Paper 1's `R_m`, with the
                       bootstrap half-width stated. Descriptive; it gates nothing
                       and spends no alpha (P2-D12). `R_m` is an ACTIVE
                       comparator, not a no-manipulation baseline (P2-D9).

  (c) DIRECTION        the exact two-sided sign test against `p0 = 0.5`
                       (P2-D6, P2-D14 as corrected by P2-D21 and P2-D22), at
                       P2-D20's ITEM unit with P2-D19's `EPS`.

WHAT THIS SCRIPT DOES NOT DO, AND WHY THAT IS THE POINT.

It issues NO verdict on H-B. P2-D5 is adopted and binds any Arm B analysis or
reporting script: every claim that a model carries adversary-relevant content is
made on a framing contrast AND on excess over the marginal null, never on raw
`A`. P2-D12's three quantities contain no excess-over-the-marginal-null quantity.
`p2_decisions.scope_audit()` surfaced that gap on 2026-09-14 and it is UNRULED.
Three readings are in circulation and they differ in what Arm B may claim, so
choosing among them here would be resolving an ambiguity by choosing, which is
the one thing `CLAUDE.md` forbids outright. The quantities and every disclosure
the decisions require are computed and emitted; the verdict is not, and the
blocker is emitted beside them as a field rather than left to a reader.

NOTHING HERE REIMPLEMENTS A FROZEN COMPUTATION. Quantity (a) is
`c5_effect.c5_movement` and quantity (c) is `inertness_ceiling.c5_delta_A`, both
called with `col="framing"`, `base="F0"`: the same statistics on a different
contrast. P2-D16's pairwise exclusion is `tie_reference.pair_frame`, which those
two also call.

Run: python3 src/t7_armb.py          (writes results/T7_armb_quantities.json
                                      and reports/T7_armb_quantities.md)
     python3 src/t7_armb.py --demo   (self-checks that do not need the write)
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import armb_floor as AF     # noqa: E402
import c5_effect as CE      # noqa: E402
import inertness_ceiling as IC  # noqa: E402
import p1                   # noqa: E402
import p2_decisions as P2D  # noqa: E402
import sign_power as SP     # noqa: E402
import t6_f0_headroom as H  # noqa: E402
import tie_reference as TR  # noqa: E402

CHOICES = "data/raw_t7/choices_t7.parquet"
F0_REPLICATION = "results/T7_f0_replication.json"
CEILING = "results/T5_inertness_ceiling.json"
OUT = "results/T7_armb_quantities.json"
REPORT = "reports/T7_armb_quantities.md"

BASE = "F0"                 # P2-D1: Paper 1's Format V `base` rendering
ARMS = ("F1", "F2")
LADDER = TR.LADDER
P_GRID = (0.60, 0.65, 0.70, 0.75, 0.80, 0.90)
PERMUTATIONS = 2            # Format V, D103; P2-D1 retires the variant axis


def load_t7(path=CHOICES):
    """T7's Format V rows under the primary rule, Paper 1's own filters applied.

    The filters are Paper 1's and not this script's: `format == "V"` (D103),
    `rule == "pmi"` (D98/D109 primary), `n_tied == 1` (a tie carries no chosen
    option), and an empty `unscored_reason`. `prompt_form` is labelled rather than
    filtered, because every T7 rendering is the templated one; the label exists so
    the shared `pair_frame` filter applies unchanged.

    Returns `(kept, raw)`. `raw` is the same rows before the tie and unscored
    filters, so P2-D16's attrition can be attributed to a cause rather than
    inferred from a count.
    """
    T = pd.read_parquet(path).assign(prompt_form=TR.FORM)
    raw = T[(T["format"] == "V") & (T["rule"] == TR.RULE)]
    kept = raw[(raw["n_tied"] == 1)
               & (raw["unscored_reason"].fillna("").astype(str) == "")]
    return kept, raw


def attrition(raw, kept, model, keep, arm):
    """P2-D16's per-cell attrition, with the item denominator it implies.

    A pair leaves both the numerator and the denominator of every quantity
    whenever EITHER of its two renderings is tied; the item's other permutation is
    retained and the item is never dropped whole. The `F0` losses are reported
    separately because `F0` is the common baseline: one tied `F0` rendering
    removes that pair from the `F1` contrast AND the `F2` contrast, so the
    attrition is correlated across the two cells of a model and is a baseline loss
    rather than two independent ones.
    """
    w = TR.pair_frame(kept, model, keep, "framing", BASE, arm)
    per_item = w.groupby(level="item_id").size()
    n_items = len(keep)
    sub = raw[(raw["model"] == model) & (raw["item_id"].isin(keep))
              & raw["framing"].isin((BASE, arm))]
    tied = sub[sub["n_tied"] != 1]
    unscored = sub[sub["unscored_reason"].fillna("").astype(str) != ""]
    return {
        "pairs_expected": n_items * PERMUTATIONS,
        "pairs_surviving": int(len(w)),
        "pairs_excluded_for_a_tie": n_items * PERMUTATIONS - int(len(w)),
        "items_with_two_surviving_pairs": int((per_item == 2).sum()),
        "items_with_one_surviving_pair": int((per_item == 1).sum()),
        "items_with_no_surviving_pair": n_items - int(len(per_item)),
        "item_denominator": int(len(per_item)),
        "tied_renderings_on_the_baseline_F0": int((tied["framing"] == BASE).sum()),
        "tied_renderings_on_the_arm": int((tied["framing"] == arm).sum()),
        "unscored_renderings": int(len(unscored)),
        "parse_failures": 0,
        "parse_failures_note":
            "Structurally zero. The measurement is forced-choice log-probability "
            "scoring over option strings under Format V (v2.0 section 7.2), so "
            "there is nothing to parse. A nonzero rate would mean the harness "
            "changed and is escalated, not filtered.",
    }


def magnitude_context(kept, P, model, keep, arm):
    """(b): the framing same-option rate against Paper 1's `R_m`. P2-D8, P2-D12.

    P2-D13 records why (b) keeps the bootstrap that (a) lost: (b) compares two
    population rates BOTH estimated from a finite item sample in the interior of
    the parameter space, where an interval is the right instrument. So both arms
    are resampled, paired on the item, which is also what keeps the clustering
    P2-D8's bootstrap exists to respect.

    The two contrasts can lose different pairs to ties, so the bootstrap runs on
    the items surviving in both and the aligned count is reported.
    """
    def per_item_same(w, lo, hi):
        s = pd.Series((w[lo].values == w[hi].values).astype(float),
                      index=w.index.get_level_values("item_id"))
        return s.groupby(level=0).mean()

    wf = TR.pair_frame(kept, model, keep, "framing", BASE, arm)
    wc = TR.pair_frame(P, model, keep)
    sf, sc = per_item_same(wf, BASE, arm), per_item_same(wc, "cond4", "cond5")
    j = sf.index.intersection(sc.index)
    r = TR.cluster_bootstrap_diff(j.values, sf.loc[j].values, sc.loc[j].values)
    return {
        "role": "DESCRIPTIVE. Gates nothing and spends no alpha (P2-D12).",
        # The pair-level rate is the one directly comparable with `R_m`, which is
        # a pair-level rate. The item-mean rates are what the bootstrap resamples,
        # per P2-D8's decision rule, and they differ from the pair rates exactly
        # on the models carrying a one-pair item. Both are emitted so neither
        # comparison has to be reconstructed from the other.
        "framing_same_option_rate_pairs":
            float((wf[BASE].values == wf[arm].values).mean()),
        "framing_same_option_rate_item_mean": float(sf.mean()),
        "c5_same_option_rate_item_mean": float(sc.mean()),
        "c5_same_option_rate_preregistered_R_m": P2D.P2D8_C5_REFERENCE[model],
        "difference_framing_minus_c5": r["difference"],
        "difference_is": "item-mean framing rate minus item-mean c5 rate, on the "
                         "items surviving in BOTH contrasts, which is the "
                         "quantity the cluster bootstrap resamples (P2-D8).",
        "ci_lo": r["lo"], "ci_hi": r["hi"],
        "half_width": float((r["hi"] - r["lo"]) / 2),
        "alpha": r["alpha"], "n_items_aligned": r["n_items"],
        "resolves": bool(r["excludes_zero"]),
        "reference_is": "ACTIVE COMPARATOR (P2-D9). c5 changes the chosen option "
                        "on 0.1389 to 0.3704 of confirmatory pairs with every "
                        "interval excluding a no-effect rate of exactly 1.0, so a "
                        "framing rate indistinguishable from R_m reads as 'the "
                        "framing moved choices about as much as a known-effective "
                        "content insertion in the same slot did', never as 'the "
                        "framing moved nothing'.",
    }


def oracle_check(kept, A, keep):
    """`A = 1` is the adversary oracle. Nothing may sit above it. P2-D23 premise.

    `A_i(o) = (marg_norm_i(o) - marg_norm_i(o*_0)) / ext_i` with `marg_norm <= 1`
    and `marg_norm_i(o*_infinity) = 1`, so `A <= 1` identically and a chosen
    option scoring above the analytically computed optimum is a misspecification
    of the coordinate or of the item join, never a result. Asserted on every
    confirmatory chosen option in the run, which is the only place a bad join
    would show.
    """
    g = kept[kept["item_id"].isin(keep)]
    a = np.array([A[int(i)][int(o)] for i, o
                  in zip(g["item_id"].values, g["chosen_option"].values)])
    worst = float(np.nanmax(a))
    n_above = int(np.sum(a > 1.0 + P2D.P2D19_EPS))
    if n_above:
        raise AssertionError(
            f"{n_above} chosen options carry A > 1, max {worst!r}. A is bounded "
            "above by 1 because marg_norm <= 1 and A(o*_infinity) = 1, so this "
            "is a chooser sitting above the analytically computed adversary "
            "optimum. That is a bug in the coordinate or the item join. "
            "CLAUDE.md: beating the oracle is a bug.")
    return {"max_A_over_chosen_options": worst,
            "n_chosen_options_above_the_adversary_oracle": n_above,
            "renderings_checked": int(len(a)),
            "bound_is": "A <= 1 identically: marg_norm <= 1 and "
                        "marg_norm(o*_infinity) = 1, so A(o*_infinity) = 1 is the "
                        "adversary oracle and nothing can exceed it."}


def compute():
    """Every quantity and every disclosure, with no verdict. Returns the artifact."""
    df, cols, A, ids, sets = TR.item_sets()
    sz = sets["size_tile_confirmatory"]
    keep = set(int(i) for i in ids[sz])
    kept, raw = load_t7()
    P = TR.load_choices()

    # ---- bindings. A run that departs from a decision fails here, not in a number.
    P2D.bind_armb(P2D.P2D3_TILE, p1.artifact_hash(p1.ITEMS_FINAL), pooled=False)
    P2D.bind_armb_statistic("sign", SP.ALPHA, 0.5, mean_is_confirmatory=False)
    P2D.bind_armb_rates(P2D.P2D10_PRIMARY_RATE, P2D.P2D10_SIGN_TEST_DENOMINATOR,
                        c5_is_active=True)
    P2D.bind_armb_quantities(0.0, c5_gates=False, sign_p0=0.5,
                             quantities=P2D.P2D12_QUANTITIES)
    P2D.bind_tie_exclusion(P2D.P2D16_EXCLUSION_UNIT, imputed_as_non_mover=False,
                           dropped_whole_item=False,
                           attrition_fields=P2D.P2D16_ATTRITION_FIELDS)
    P2D.bind_quantity_c_unit(P2D.P2D20_UNIT, P2D.P2D20_SIGN_DISAGREEMENT,
                             True, True, P2D.P2D19_EPS)
    P2D.bind_neutral_claim_wording(tally_frame_used=False,
                                   conservative_justifies_p0=False,
                                   b2_described_as_drifting=False)
    _, _, _, ext = H.item_axis()
    P2D.bind_ext_floor(float(ext[sz].min()), int(sz.sum()), ())
    P2D.check_p1_ext_floor_source()
    # P2-D24. The premises a direction claim on (c) would need, asserted as
    # premises: no confirmatory quantity is an excess over the marginal null, the
    # c5 neutral diagnostic resolves on CTRL alone, and the direction of the
    # switches the A coordinate discards is not established. This run makes no
    # direction claim and none is licensed.
    P2D.bind_direction_claim(
        direction_claim_made=False,
        neutral_resolves_on=tuple(
            m for m in LADDER
            if json.load(open(CEILING))["diagnostic_c5_direction"][
                "per_model"][m]["significant_at_corrected_alpha_item"]),
        excess_over_marginal_null_quantities=(),
        discarded_switch_direction_established=False)

    # P2-D8's reference is the preregistered table, not a recomputation. The
    # recomputation is the check that this read of the frozen artifact is of the
    # same quantity the table names; a drift fails here, before any (b) number.
    R_m = {m: CE.c5_movement(P, m, keep)["same_option_rate"] for m in LADDER}
    P2D.bind_armb_tie(R_m, TR.BOOT_N, TR.BOOT_SEED, tie_in_main_family=False)

    # P2-D19 binds the resolution figures the blind spot below is read against.
    inv = TR.a_invisibility(A, ids, sz, eps=P2D.P2D19_EPS)
    P2D.bind_a_tie_tolerance(inv["eps"], inv["n_items_with_an_A_tied_option_pair"],
                             inv["n_A_tied_option_pairs"],
                             inv["n_unordered_option_pairs"],
                             inv["next_gap_above_eps"])

    # P2-D13's floor: max(7, T7's own F0-versus-cond4 disagreement count). The
    # measurement is T7 step 2's and is read, not recomputed.
    rep = json.load(open(F0_REPLICATION))
    f0_dis = int(rep["floor"]["measured_worst_case_items"])
    floor = AF.floor_for_run(f0_dis)
    P2D.bind_armb_floor(floor, f0_dis, floor_is_statistical=False)

    gap_item = AF.type_ii_gap_item(CEILING)
    P2D.bind_neutral_baseline(0.5, P2D.P2D21_ALL_SEVEN_CLAIM_HOLDS,
                              P2D.P2D21_SIX_LADDER_CLAIM_HOLDS,
                              P2D.P2D21_NEUTRAL_ABOVE_P0,
                              {m: v["gap_to_p0"] for m, v in gap_item.items()})

    oracle = oracle_check(kept, A, keep)

    cells = {}
    for arm in ARMS:
        direction = IC.c5_delta_A(kept, A, keep, "framing", BASE, arm)
        for m in LADDER:
            mv = CE.c5_movement(kept, m, keep, "framing", BASE, arm)
            d = direction[m]
            n_eff = d["n_eff_item"]
            att = attrition(raw, kept, m, keep, arm)
            cells[f"{m}|{arm}"] = {
                "model": m, "framing": arm, "contrast": f"{arm} - {BASE}",
                "a_inertness": {
                    "null": 0.0,
                    "change_rate_renderings": mv["change_rate"],
                    "change_rate_item_mean": mv["change_rate_item_mean"],
                    "n_changed_pairs": mv["n_changed"],
                    "n_pairs": mv["n_pairs"],
                    "ci_lo": mv["ci_lo"], "ci_hi": mv["ci_hi"],
                    "alpha": mv["alpha"],
                    "interval_excludes_zero": mv["excludes_no_effect"],
                    "n_items_with_a_changed_pair":
                        mv["n_items_with_a_changed_pair"],
                    "item_denominator": mv["n_items"],
                    "floor_items": floor,
                    "clears_the_floor":
                        bool(mv["n_items_with_a_changed_pair"] >= floor),
                    "tv_option_marginal": mv["tv_option_marginal"],
                },
                "b_magnitude_context":
                    magnitude_context(kept, P, m, keep, arm),
                "c_direction": {
                    "unit": "item (P2-D20)",
                    "p0": 0.5,
                    "eps": P2D.P2D19_EPS,
                    "n_eff_item": n_eff,
                    "n_positive_item": d["n_positive_item"],
                    "sign_proportion_item": d["sign_proportion_item"],
                    "p_two_sided_item": d["p_two_sided_item"],
                    "significant_at_corrected_alpha_item":
                        d["significant_at_corrected_alpha_item"],
                    "ci95_item": d["ci95_item"],
                    "tie_rate_item": d["tie_rate_item"],
                    "realized_power_at": {str(p): SP.power(n_eff, p)
                                          for p in P_GRID},
                    "realized_p1_at_80_power": SP.detectable(n_eff),
                    "n_items_with_both_pairs": d["n_items_with_both_pairs"],
                    "n_items_with_one_pair": d["n_items_with_one_pair"],
                    "n_items_sign_disagreement": d["n_items_sign_disagreement"],
                    "n_items_sign_disagreement_cancelling":
                        d["n_items_sign_disagreement_cancelling"],
                    "n_eff_pair_at_eps": d["n_eff_pair_at_eps"],
                    "type_ii_gap_signed": gap_item[m]["gap_to_p0"],
                    "gap_is_a_type_ii_cost": gap_item[m]["gap_is_a_type_ii_cost"],
                    "neutral_baseline_above_p0":
                        gap_item[m]["baseline_above_p0"],
                    "type_i_exposure":
                        None if gap_item[m]["gap_is_a_type_ii_cost"] else
                        "The content-neutral baseline sits above p0 for this "
                        "model at the item unit, so the signed gap is negative. "
                        "That is not a smaller Type II cost but a different "
                        "quantity: a result significant against p0 = 0.5 but at "
                        "or below "
                        f"{gap_item[m]['neutral_sign_proportion']:.4f} is "
                        "nominally positive while sitting at or below what a "
                        "content-neutral insert does, which is a Type I exposure "
                        "P2-D14's licence box has no sentence for (P2-D21). B2 "
                        "sits AT the null: exactly 0.5000 under three of five "
                        "aggregations of the same frozen rows, and every 95% "
                        "exact interval contains 0.5.",
                },
                "blind_spot_P2D10": {
                    "definition": "tie rate minus same-option rate: choice "
                                  "movement between two options that share an A",
                    "same_option_rate": mv["same_option_rate"],
                    "tie_rate_pair": d["tie_rate"],
                    "gap": d["tie_rate"] - mv["same_option_rate"],
                },
                "attrition_P2D16": att,
            }

    unruled = P2D.scope_audit()
    return {
        "purpose":
            "T7 confirmatory analysis. Arm B's three quantities (P2-D12) per "
            "(model, framing) cell on the 108-item size confirmatory set "
            "(P2-D3, P2-D4), for the F1-F0 and F2-F0 contrasts, with every "
            "disclosure the decisions require. NO VERDICT ON H-B IS ISSUED; see "
            "`blocker`.",
        "emitted_by": "src/t7_armb.py",
        "rule": TR.RULE, "prompt_form": TR.FORM, "base_framing": BASE,
        "alpha": SP.ALPHA, "p0": 0.5,
        "n_confirmatory": P2D.P2D23_CONFIRMATORY_N,
        "choices_sha256": p1.artifact_hash(CHOICES),
        "items_sha256": p1.artifact_hash(p1.ITEMS_FINAL),
        "bootstrap": {"resamples": TR.BOOT_N, "seed": TR.BOOT_SEED,
                      "unit": "item", "alpha": TR.ALPHA_TIE},
        "inertness_floor": {
            "value": floor,
            "provisional": P2D.P2D13_PROVISIONAL_FLOOR,
            "f0_versus_cond4_disagreement_items": f0_dis,
            "rule": "floor = max(7, F0-versus-cond4 disagreement items), "
                    "upward-only by construction (P2-D13)",
            "revised": floor != P2D.P2D13_PROVISIONAL_FLOOR,
            "is_statistical": False,
            "what_it_is":
                "A NUMERICAL noise floor, not a significance threshold. Under "
                "P2-D9's deterministic scorer the strict null has no sampling "
                "variation, every resample returns exactly zero, and Type I "
                "error is exactly 0 rather than alpha, so the bootstrap guards "
                "nothing in quantity (a). The measured disagreement count is the "
                "first empirical measurement of the no-effect rate v2.6 section "
                "1.1 could only argue from Paper 1's code path; F0 and cond4 are "
                "identical text under P2-D1, and F1 and F2 are longer prompts "
                "with different batch shapes, so the F0 rate is a LOWER BOUND on "
                "the noise floor and is used rather than scaled.",
        },
        "reference_R_m": P2D.P2D8_C5_REFERENCE,
        "detection_limits_P2D11": {
            "source": "results/T5_inertness_ceiling.json, computed before T7 ran "
                      "(PREREGISTRATION_v2.7.md section 3). Not derived from any "
                      "observed tie rate, which would be a post-hoc power "
                      "calculation.",
            "quantity_b_half_width_range": list(P2D.P2D11_CEILING["half_width"]),
            "n_benchmark": P2D.P2D11_N_BENCHMARK,
            "n_realized": P2D.P2D23_CONFIRMATORY_N,
            "statement":
                "A same-option-rate gap below roughly 0.15 is not resolvable by "
                "quantity (b), which under P2-D12 limits what the CONTEXT can "
                "say and not whether anything fires. Quantity (c)'s power is set "
                "by the observed tie rate and is reported per cell at the "
                "realized n_eff. n = 108 against v2.0 section 8.2's benchmark of "
                "400 is a third shortfall and it does not disappear because "
                "P2-D6 changed the statistic.",
        },
        "a_tie_resolution_P2D19": {
            "eps": inv["eps"],
            "primary_per_pair": [inv["n_A_tied_option_pairs"],
                                 inv["n_unordered_option_pairs"],
                                 inv["share_option_pairs_invisible_to_A"]],
            "secondary_per_item": [inv["n_items_with_an_A_tied_option_pair"],
                                   inv["n_items"],
                                   inv["share_items_with_an_A_tied_option_pair"]],
            "note": "The per-item figure counts items containing AT LEAST ONE "
                    "tied pair among fifteen and is inflated by option count. It "
                    "is never quoted alone. This is a limitation of the "
                    "coordinate, not a property of any model.",
        },
        "oracle_check": oracle,
        "cells": cells,
        "direction_reading_P2D24": {
            "ruling": "The five resolving cells license NO claim about direction. "
                      "Quantity (c) is reported as computed and nothing is "
                      "withheld; what is blocked is the reading of its sign, not "
                      "the statistic.",
            "direction_claim_licensed": P2D.P2D24_DIRECTION_CLAIM_LICENSED,
            "movement_claim_licensed": P2D.P2D24_MOVEMENT_CLAIM_LICENSED,
            "resolving_cells": list(P2D.P2D24_RESOLVING_CELLS),
            "resolving_all_downward": P2D.P2D24_RESOLVING_ALL_DOWNWARD,
            "premise_1_excess_over_the_marginal_null":
                "P2-D5's second conjunct names A_null(m, F) = sum_o p_{m,F}(o) "
                "A_i(o), v2.0 section 3.3's object. P2-D12's three quantities "
                "contain no excess quantity, and neither a same-option rate nor "
                "p0 = 0.5 is that object. A_null and v2.0 section 4.4's "
                "attribution cap dA_null have never been computed for Paper 2. "
                "Computing them as specified would be preregistered; using "
                "either to license a direction claim on (c) would be post-hoc, "
                "because no rule maps a level excess onto a sign proportion.",
            "premise_2_the_neutral_baseline":
                "A content-neutral insert departs downward on the one model "
                "whose own diagnostic resolves at the corrected alpha, which is "
                "CTRL and only CTRL. Downward departure is therefore not "
                "established as a property of adversary content rather than of "
                "inserted text. Reading an F1 or F2 proportion against a "
                "non-resolving neutral point estimate, which is what four of the "
                "five resolving cells would require, is the recalibration "
                "P2-D12, P2-D14 and P2-D21 each declined, moved into the "
                "reporting where it has no alpha at all.",
            "premise_3_the_discarded_switches":
                "On three of the five resolving cells the coordinate discards "
                "the switches it cannot see at 1.81 to 4.09 times P2-D19's "
                "per-pair bound. That is selection, not measurement error, and "
                "nothing establishes that the discarded switches carry the "
                "direction of the retained ones.",
            "neutral_resolves_on": list(P2D.P2D24_NEUTRAL_RESOLVES_ON),
            "concentrated_resolving_cells":
                list(P2D.P2D24_CONCENTRATED_RESOLVING_CELLS),
            "concentration_ratio_on_those_cells":
                list(P2D.P2D24_CONCENTRATION_RATIO_RESOLVING),
            "marginal_null_computed": P2D.P2D24_MARGINAL_NULL_COMPUTED,
            "marginal_null_specified_in": P2D.P2D24_MARGINAL_NULL_SPEC,
            "independent_of_the_blocker":
                "The ruling holds under all three readings of P2-D5's blocker: "
                "premises 2 and 3 are untouched by how it goes. The blocker "
                "stays open and stays the author's.",
        },
        "blocker": {
            "id": "P2-D5's second conjunct, excess over the marginal null",
            "status": "UNRULED",
            "surfaced_by": "p2_decisions.scope_audit(), 2026-09-14",
            "unruled_registry_entries": unruled,
            "what_it_blocks":
                "Any verdict on H-B, and any statement that a model does or does "
                "not carry adversary-relevant content, track the adversary, or "
                "fail to.",
            "why":
                "P2-D5 is adopted and binds any Arm B analysis or reporting "
                "script: every claim that a model carries adversary-relevant "
                "content is made on a framing contrast AND on excess over the "
                "marginal null, never on raw A. P2-D12's three quantities "
                "contain no excess-over-the-marginal-null quantity. v2.0 section "
                "4 required both that the interval on mean dA exclude zero and "
                "that observed mean dA exceed dA_null(m, F); P2-D6 retires the "
                "first conjunct by demoting the mean and does not name the "
                "second. Three readings are available and they differ in what "
                "Arm B may claim: that P2-D5's conjunct travels to the new "
                "quantities and needs an operational form; that it expired with "
                "the mean the way the ext_i floor's scope did; or that (a), (b) "
                "and (c) already satisfy it because a framing contrast against a "
                "same-option baseline is an excess. Choosing among them is the "
                "author's.",
            "what_is_emitted_anyway":
                "Emitted anyway, because the numbers are not what is blocked: "
                "all three quantities, per-cell tie attrition and item "
                "denominators (P2-D16), the signed per-model Type II gap "
                "(P2-D14 as corrected by P2-D21 and P2-D22), the realized n_eff "
                "at the item unit and the realized power (P2-D6, P2-D12), the "
                "floor P2-D13 gives for this run, P2-D10's blind spot, and "
                "P2-D19's resolution figures. Reporting a blocked gate is a "
                "successful task outcome; the numbers are not withheld, the "
                "claim is.",
        },
    }


def main():
    out = compute()
    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    _write_report(out)

    floor = out["inertness_floor"]["value"]
    print(f"n = {out['n_confirmatory']}, alpha = {out['alpha']:.6f}, "
          f"p0 = {out['p0']}, inertness floor = {floor} items "
          f"(max(7, {out['inertness_floor']['f0_versus_cond4_disagreement_items']}))\n")
    hdr = (f"  {'cell':9s} {'(a) rate':>9s} {'(a) CI':>20s} {'moved':>6s} "
           f"{'(b) diff':>9s} {'(b) hw':>7s} {'n_eff':>6s} {'(c) prop':>9s} "
           f"{'(c) p':>9s} {'pow.75':>7s} {'gap':>8s} {'den':>4s} {'lost':>5s}")
    for arm in ARMS:
        print(f"\n{arm} - {BASE}")
        print(hdr)
        for m in LADDER:
            c = out["cells"][f"{m}|{arm}"]
            a, b, d, at = (c["a_inertness"], c["b_magnitude_context"],
                           c["c_direction"], c["attrition_P2D16"])
            print(f"  {m:9s} {a['change_rate_renderings']:9.4f} "
                  f"[{a['ci_lo']:+.4f}, {a['ci_hi']:+.4f}] "
                  f"{a['n_items_with_a_changed_pair']:6d} "
                  f"{b['difference_framing_minus_c5']:+9.4f} "
                  f"{b['half_width']:7.4f} {d['n_eff_item']:6d} "
                  f"{d['sign_proportion_item']:9.4f} "
                  f"{d['p_two_sided_item']:9.6f} "
                  f"{d['realized_power_at']['0.75']:7.3f} "
                  f"{d['type_ii_gap_signed']:+8.4f} "
                  f"{at['item_denominator']:4d} "
                  f"{at['pairs_excluded_for_a_tie']:5d}")
    print(f"\noracle check: max A over {out['oracle_check']['renderings_checked']:,} "
          f"chosen options = {out['oracle_check']['max_A_over_chosen_options']:.6f}, "
          f"{out['oracle_check']['n_chosen_options_above_the_adversary_oracle']} "
          "above the adversary oracle")
    print(f"\nBLOCKER ({out['blocker']['status']}): {out['blocker']['id']}")
    print(f"  {out['blocker']['what_it_blocks']}")
    print(f"\nwritten: {OUT}\n         {REPORT}")
    return 0


def _write_report(out):
    b, floor = [], out["inertness_floor"]["value"]
    W = b.append
    W("# T7: Arm B's three quantities on the confirmatory set\n")
    W("Generated by `python3 src/t7_armb.py`. Every number here is emitted by "
      "that script from `data/raw_t7/choices_t7.parquet` and Paper 1's frozen "
      "artifacts. **No verdict on H-B is issued**, and section 6 says why.\n")
    W(f"`n` = {out['n_confirmatory']} items, `size` tile, finite `beta_c` "
      f"(P2-D3, P2-D4, P2-D23). `alpha` = {out['alpha']:.6f} over the 21-test "
      f"family. `p0` = {out['p0']}. Rule `{out['rule']}`, Format V. Bootstrap: "
      f"{out['bootstrap']['resamples']:,} resamples over items, seed "
      f"{out['bootstrap']['seed']} (P2-D8).\n")
    W(f"Item file `sha256` `{out['items_sha256']}`; T7 choices `sha256` "
      f"`{out['choices_sha256']}`.\n")

    W("## 1. The inertness floor for this run (P2-D13)\n")
    f = out["inertness_floor"]
    W(f"`floor = max({f['provisional']}, "
      f"{f['f0_versus_cond4_disagreement_items']}) = {f['value']}` items, "
      f"{'REVISED' if f['revised'] else 'unrevised'}.\n")
    W(f["what_it_is"] + "\n")

    for arm in ARMS:
        W(f"## 2.{ARMS.index(arm) + 1} `{arm}` minus `{BASE}`\n")
        W("| model | (a) change rate | (a) CI vs 0 | items moved | clears floor "
          f"of {floor} | (b) framing rate | (b) `R_m` | (b) diff | (b) half-width "
          "| (c) `n_eff` | (c) positive | (c) proportion | (c) `p` | (c) 95% CI |")
        W("|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for m in LADDER:
            c = out["cells"][f"{m}|{arm}"]
            a, mc, d = (c["a_inertness"], c["b_magnitude_context"],
                        c["c_direction"])
            W(f"| `{m}` | {a['change_rate_renderings']:.4f} | "
              f"[{a['ci_lo']:+.4f}, {a['ci_hi']:+.4f}] | "
              f"{a['n_items_with_a_changed_pair']} | "
              f"{'yes' if a['clears_the_floor'] else 'no'} | "
              f"{mc['framing_same_option_rate_pairs']:.4f} | "
              f"{mc['c5_same_option_rate_preregistered_R_m']:.4f} | "
              f"{mc['difference_framing_minus_c5']:+.4f} | "
              f"{mc['half_width']:.4f} | {d['n_eff_item']} | "
              f"{d['n_positive_item']} | {d['sign_proportion_item']:.4f} | "
              f"{d['p_two_sided_item']:.6f} | "
              f"[{d['ci95_item'][0]:.4f}, {d['ci95_item'][1]:.4f}] |")
        W("")

    W("## 3. Realized power at the item unit (P2-D6, P2-D12)\n")
    W("Realized, at the observed `n_eff`, not assumed. P2-D6's defect stated "
      "rather than argued away: a high tie rate is the outcome H-B predicts and "
      "ties carry no sign, so the sign test has least power exactly where the "
      "null is true.\n")
    W("| cell | `n_eff` | tie rate (item) | " +
      " | ".join(f"power at `p1`={p}" for p in P_GRID) + " | `p1` at 80% |")
    W("|---|---:|---:|" + "---:|" * (len(P_GRID) + 1))
    for arm in ARMS:
        for m in LADDER:
            d = out["cells"][f"{m}|{arm}"]["c_direction"]
            W(f"| `{m}` `{arm}` | {d['n_eff_item']} | "
              f"{d['tie_rate_item']:.4f} | "
              + " | ".join(f"{d['realized_power_at'][str(p)]:.3f}"
                           for p in P_GRID)
              + f" | {d['realized_p1_at_80_power']} |")
    W("")

    W("## 4. Tie attrition and item denominators (P2-D16)\n")
    W("A tied rendering carries no chosen option, so its `(item, permutation)` "
      "pair leaves both the numerator and the denominator of every quantity, the "
      "item's other permutation is retained, and the item is never dropped whole. "
      "A tie is never imputed as a non-mover. `F0` losses are a BASELINE loss: "
      "one tied `F0` rendering removes that pair from the `F1` contrast and from "
      "the `F2` contrast, so the attrition is correlated across a model's two "
      "cells and is counted once, not twice.\n")
    W("| cell | pairs expected | pairs surviving | pairs excluded for a tie | "
      "tied on `F0` | tied on the arm | items with 2 pairs | items with 1 pair | "
      "items with 0 pairs | item denominator | parse failures |")
    W("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for arm in ARMS:
        for m in LADDER:
            at = out["cells"][f"{m}|{arm}"]["attrition_P2D16"]
            W(f"| `{m}` `{arm}` | {at['pairs_expected']} | "
              f"{at['pairs_surviving']} | {at['pairs_excluded_for_a_tie']} | "
              f"{at['tied_renderings_on_the_baseline_F0']} | "
              f"{at['tied_renderings_on_the_arm']} | "
              f"{at['items_with_two_surviving_pairs']} | "
              f"{at['items_with_one_surviving_pair']} | "
              f"{at['items_with_no_surviving_pair']} | "
              f"**{at['item_denominator']}** | {at['parse_failures']} |")
    W("\nThe floor is an absolute count of items and does not move with the "
      "denominator, so a denominator below 108 makes the floor marginally harder "
      "to clear. That is reported, not adjusted.\n")

    W("## 5. The signed Type II gap, with every (c) row (P2-D14, P2-D21, P2-D22)\n")
    W("`p0 = 0.5` stands on the structural ground: moving it recalibrates a "
      "preregistered test against a different manipulation, on a coordinate Paper "
      "1 never used. The content-neutral baseline does not drift toward the "
      "salience pole. At P2-D20's item unit the per-model proportion runs 0.1951 "
      "to 0.5556, only `CTRL` resolves at the corrected `alpha` and it resolves "
      "downward, and `B2` sits at the null: 0.5556 on `n_eff` 36, `p` = 0.6177, "
      "95% exact [0.3810, 0.7206], and exactly 0.5000 under three of five "
      "aggregations of the same rows.\n")
    W("| model | neutral proportion (item) | signed gap to `p0` | reading |")
    W("|---|---:|---:|---|")
    seen = set()
    for arm in ARMS:
        for m in LADDER:
            if m in seen:
                continue
            seen.add(m)
            d = out["cells"][f"{m}|{arm}"]["c_direction"]
            rd = ("Type II cost of that size" if d["gap_is_a_type_ii_cost"]
                  else "NEGATIVE. Not a smaller cost but a Type I exposure: a "
                       "result significant against `p0` = 0.5 but at or below the "
                       "neutral proportion is nominally positive while sitting at "
                       "or below what a content-neutral insert does.")
            W(f"| `{m}` | {0.5 - d['type_ii_gap_signed']:.4f} | "
              f"{d['type_ii_gap_signed']:+.4f} | {rd} |")
    W("")

    W("## 6. The blocker: no verdict on H-B is issued\n")
    bl = out["blocker"]
    W(f"**{bl['id']}. Status: {bl['status']}.** Surfaced by "
      "`p2_decisions.scope_audit()` on 2026-09-14 and recorded in "
      "`docs/P2/DECISIONS.md` under \"What the registry surfaced on its first "
      "run\".\n")
    W(bl["why"] + "\n")
    W(f"**Blocked:** {bl['what_it_blocks']}\n")
    W(bl["what_is_emitted_anyway"] + "\n")

    W("## 6b. Direction: no claim is licensed (P2-D24)\n")
    dr = out["direction_reading_P2D24"]
    W(dr["ruling"] + "\n")
    W("Five of the fourteen cells depart from `p0` = 0.5 at the corrected "
      "`alpha`: " + ", ".join(f"`{c}`" for c in dr["resolving_cells"]) +
      ". All five departures are below 0.5. That arithmetic statement is what "
      "the section 2 tables carry and it stands. Reading it as movement away "
      "from `o*_infinity`, as evidence about adversary tracking, or as a "
      "property of a model does not. Such a reading needs three premises and "
      "none holds.\n")
    W(f"1. **Excess over the marginal null.** {dr['premise_1_excess_over_the_marginal_null']}")
    W(f"2. **The neutral baseline.** {dr['premise_2_the_neutral_baseline']}")
    W(f"3. **The discarded switches.** {dr['premise_3_the_discarded_switches']} "
      "The affected cells are " +
      ", ".join(f"`{c}`" for c in dr["concentrated_resolving_cells"]) +
      " (`reports/T7_switch_concentration.md`).\n")
    W(dr["independent_of_the_blocker"] + "\n")
    W("**What IS licensed.** Movement, at quantity (a): both framings changed "
      "the chosen option on every model, 30 to 77 items of 108 per cell, every "
      "cell clearing the floor of 7, every interval excluding zero, against an "
      "exact null of zero under P2-D9's deterministic scorer. Magnitude, per "
      "cell, at quantity (b): three cells resolve against `R_m` and eleven do "
      "not, and the three are reported as three rather than pooled into a "
      "magnitude word.\n")

    W("## 7. What the numbers above do not license\n")
    W("Beyond the blocker, three limits stand on their own and compose.\n")
    W(f"1. Quantity (b) cannot resolve a same-option-rate gap below roughly "
      f"{out['detection_limits_P2D11']['quantity_b_half_width_range'][0]:.4f} to "
      f"{out['detection_limits_P2D11']['quantity_b_half_width_range'][1]:.4f}. "
      "Under P2-D12 that limits what the context can say, not whether anything "
      "fires. The realized half-widths in section 2 are smaller than that range, "
      "and the two are not in conflict: P2-D11's figure is the half-width of the "
      "permutation-versus-`c5` instrument check, two unrelated manipulations, "
      "while the realized one is a framing-versus-`c5` difference on the same "
      "items sharing the `F0`/`cond4` baseline, so it is paired and tighter. "
      "P2-D11's figure is the preregistered bound and is reported as such; the "
      "realized one is data.")
    W(f"2. `n` = {out['n_confirmatory']} against `v2.0` section 8.2's benchmark of "
      f"{out['detection_limits_P2D11']['n_benchmark']}. P2-D6 changed the "
      "statistic; it did not repair the information shortfall.")
    W("3. The `A` coordinate cannot see a switch between two `A`-tied options. At "
      f"Paper 1's `EPS` = {out['a_tie_resolution_P2D19']['eps']:g} that is "
      f"{out['a_tie_resolution_P2D19']['primary_per_pair'][0]} of "
      f"{out['a_tie_resolution_P2D19']['primary_per_pair'][1]} unordered option "
      f"pairs, {out['a_tie_resolution_P2D19']['primary_per_pair'][2]:.4f}. The "
      f"per-item figure, "
      f"{out['a_tie_resolution_P2D19']['secondary_per_item'][0]} of "
      f"{out['a_tie_resolution_P2D19']['secondary_per_item'][1]}, counts items "
      "containing at least one tied pair among fifteen and is never quoted alone. "
      "This is a limitation of the coordinate, not a property of any model.\n")
    W(f"The oracle bound holds: the largest `A` over all "
      f"{out['oracle_check']['renderings_checked']:,} confirmatory chosen options "
      f"is {out['oracle_check']['max_A_over_chosen_options']:.6f}, and "
      f"{out['oracle_check']['n_chosen_options_above_the_adversary_oracle']} sit "
      "above the adversary oracle at `A` = 1. Nothing beat the oracle.\n")
    os.makedirs("reports", exist_ok=True)
    open(REPORT, "w").write("\n".join(b) + "\n")


def demo():
    """The checks that must hold before any of the above is believable.

    Three, and they fail for different reasons. The generalised contrast must
    reproduce Paper 1's frozen `R_m`, or quantity (b) is calibrated against a
    number nothing recomputes. Nothing may sit above the adversary oracle. And
    P2-D5's conjunct must still be unruled, because this script's whole shape,
    quantities emitted and verdict withheld, is wrong the moment it is ruled.
    """
    df, cols, A, ids, sets = TR.item_sets()
    keep = set(int(i) for i in ids[sets["size_tile_confirmatory"]])
    P = TR.load_choices()
    got = {m: CE.c5_movement(P, m, keep)["same_option_rate"] for m in LADDER}
    P2D.bind_armb_tie(got, TR.BOOT_N, TR.BOOT_SEED, False)
    kept, _ = load_t7()
    o = oracle_check(kept, A, keep)
    unruled = [r["passage"] for r in P2D.scope_audit()]
    assert unruled, (
        "P2-D5's second conjunct is no longer unruled. This script withholds "
        "Arm B's verdict BECAUSE it is unruled; once it is ruled, the ruling "
        "governs what may be claimed and this file has to be revisited rather "
        "than re-run.")
    print(f"ok: R_m reproduces P2-D8's table on all {len(got)} models")
    print(f"    max A over {o['renderings_checked']:,} chosen options = "
          f"{o['max_A_over_chosen_options']:.6f} <= 1, nothing beat the oracle")
    print(f"    still unruled, so no verdict is issued: {unruled}")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
