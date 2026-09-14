"""Arm B's detection limits under P2-D12's restructure, and the diagnostics behind it.

P2-D8 made the `c5` comparison a GATE: the movement half of H-B's conjunction
fired only if the framing's same-option rate sat more than a bootstrap half-width
below `R_m`. `results/T5_detection_ceiling.json` measured what that cost, and the
cost was the design: `L1` had to move 2.13 times what `c5` moves before anything
fired, and the effective `n` for the sign test was bounded at 32 to 58.

P2-D9 is what makes the gate unnecessary. Paper 1's scorer is deterministic, so
the no-effect same-option rate is exactly 1.0 and the inertness question the
reference was introduced for ("did F1 move anything, or are T3's templates too
weak") is answered by the change rate against **zero**, at full `n`. The `c5`
comparison is retained as magnitude context and gates nothing.

This file emits three things.

  1. THE INERTNESS FLOOR.  How many of the 108 items must carry a changed
     rendering before the cluster bootstrap's lower bound clears zero. It is a
     count, not a rate, because the bootstrap's lower bound is zero exactly when
     a resample can contain no moving item.

  2. THE SIGN TEST'S POSITION, unbounded by the gate.  Effective `n` is now
     whatever the observed tie rate gives. Since no tie rate is observable before
     T7 runs, `c5`'s own tie rate is reported as an analogue, with the same
     caveat `reports/T5_sigma_prior.md` section 0 attaches to its own: a
     structurally matched manipulation, not a measurement of the quantity.

  3. TWO DIAGNOSTICS that bear on whether the gate bought anything.

     `c5`'s own `ΔA` sign proportion answers the one thing a magnitude gate might
     have been reaching for: whether a content-neutral insertion drifts toward
     `o*_infinity`, which is P1's salience pole on 452 of 460 divergent items. If
     it did, a positive F1 sign test would be explicable without adversary
     tracking. **This is reported, and it is NOT adopted as a null.** Moving
     `p0` off 0.5 would recalibrate a preregistered test against a different
     manipulation, and P2-D6 fixed `p0 = 0.5`.

     P2-D21 corrects what this diagnostic says and P2-D22 fixes how it is said.
     The PAIR block below, which `v2.7` section 2.1 publishes, gives "at or below
     0.5 on all seven models". That claim is withdrawn, and the replacement is
     not a smaller tally. **The content-neutral baseline does not drift toward
     the salience pole.** At P2-D20's ITEM unit, the unit quantity (c) runs on,
     the per-model proportion is 0.1951 to 0.5556; only `CTRL` resolves at the
     corrected `alpha` and it resolves downward; and `B2` sits at the null, at
     0.5000 under three of five aggregations of these rows and 0.5556 under the
     adopted one, never distinguishable from 0.5. `p0 = 0.5` is retained on the
     structural ground. Both readings are emitted, because the pair one is
     published and must still reproduce.

     `c5`'s tie rate minus its same-option rate is P2-D10's blind spot, measured
     on a real manipulation rather than bounded from the geometry.

Run: python3 src/inertness_ceiling.py          (writes results/T5_inertness_ceiling.json)
     python3 src/inertness_ceiling.py --demo   (self-check on the floor)
"""
import json
import os
import sys

import numpy as np
from scipy.stats import binomtest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2_decisions as P2D  # noqa: E402
import sign_power as SP     # noqa: E402
import t6_f0_headroom as H  # noqa: E402
import tie_reference as TR  # noqa: E402

OUT = "results/T5_inertness_ceiling.json"
N = SP.N_CONFIRMATORY
P_GRID = (0.60, 0.65, 0.70, 0.75, 0.80, 0.90)


def inertness_floor(n=N, alpha=SP.ALPHA):
    """Smallest number of moving items whose bootstrap lower bound clears zero.

    The item-level mean of a resample is zero exactly when the resample contains
    no moving item, so the lower bound at `alpha/2` is positive as soon as
    `((n - k) / n) ** n < alpha / 2`. Solved by search and then checked against
    the real bootstrap, because an analytic floor that the implementation does
    not reproduce is worth nothing.
    """
    for k in range(1, n + 1):
        if ((n - k) / n) ** n < alpha / 2:
            return k
    return None


def check_floor(k, n=N, both_permutations=True):
    """Run P2-D8's actual bootstrap on a `k`-mover configuration."""
    v = np.zeros(n)
    v[:k] = 1.0 if both_permutations else 0.5
    r = TR.cluster_bootstrap_diff(np.arange(n), v, np.zeros(n))
    return {"k": k, "item_mean": r["difference"], "lo": r["lo"],
            "clears_zero": bool(r["lo"] > 0)}


def pair_delta_A(ch, A, model, keep, col="condition", base="cond4", arm="cond5"):
    """Per-pair `ΔA` and the item id of each pair, on P2-D16's surviving pairs.

    Factored out of `c5_delta_A` rather than copied, for the reason `CLAUDE.md`
    gives: a second `A[i][b] - A[i][a]` over `pair_frame` would be a duplicated
    frozen computation that can silently diverge. `t7_control` needs the per-item
    mean of this vector, which is `v2.0` section 3.2's item value for `ΔA`, and
    `c5_delta_A` needs the vector itself.

    Returns `(item_ids, base_choices, arm_choices, delta_A)`.
    """
    w = TR.pair_frame(ch, model, keep, col, base, arm)
    it = w.index.get_level_values("item_id").values.astype(int)
    a0, a1 = w[base].values, w[arm].values
    d = np.array([A[i][int(b)] - A[i][int(a)] for i, a, b in zip(it, a0, a1)])
    return it, a0, a1, d


def c5_delta_A(ch, A, keep, col="condition", base="cond4", arm="cond5"):
    """`c5`'s own tie rate, blind spot and `ΔA` sign proportion, per model.

    `col`/`base`/`arm` default to Paper 1's condition contrast. T7's quantity (c)
    is the same computation on `col="framing"`, `base="F0"`, so it reuses this
    rather than reimplementing the pair pivot, the `ΔA` lookup and P2-D20's item
    aggregation a second time.
    """
    out = {}
    for m in TR.LADDER:
        it, c4, c5, d = pair_delta_A(ch, A, m, keep, col, base, arm)
        nz = d != 0
        n_eff, pos = int(nz.sum()), int((d[nz] > 0).sum())
        same = float((c4 == c5).mean())
        tie = float(1 - nz.mean())
        out[m] = {
            "same_option_rate": same, "tie_rate": tie,
            "blind_spot": tie - same,
            "n_eff": n_eff, "n_positive": pos,
            "sign_proportion": pos / n_eff if n_eff else float("nan"),
            "p_two_sided": binomtest(pos, n_eff, 0.5).pvalue if n_eff else float("nan"),
            "significant_at_corrected_alpha":
                bool(n_eff and binomtest(pos, n_eff, 0.5).pvalue < SP.ALPHA),
        }
        # P2-D20: the unit is the ITEM. Everything above is the PAIR reading and
        # is kept byte-identical because `v2.7` section 2.1 publishes it. The
        # item block is the one (c) runs on. Two corrections, emitted separately
        # so they can be told apart: the unit (pair -> item) and the zero test
        # (exact -> P2-D19's EPS).
        out[m].update(_item_reading(it, d))
    return out


def _item_reading(it, d, eps=P2D.P2D19_EPS):
    """P2-D20's item aggregation of per-pair `ΔA`, and the disagreement counts.

    `v2.0` section 3.2 defines the item value as `A` averaged within item across
    the two Format V permutations, and the mean of `A` differences IS the
    difference of mean `A`, so the item statistic is the mean of that item's
    surviving pair `ΔA`s. An item with one surviving pair contributes that pair,
    per P2-D16. An item whose two pairs disagree in sign contributes the sign of
    their mean, and contributes nothing when they cancel to within `eps`, which is
    the same event as a pair-level tie and is counted as one.
    """
    order = np.argsort(it, kind="stable")
    iid, first = np.unique(it[order], return_index=True)
    groups = np.split(d[order], first[1:])
    mean = np.array([g.mean() for g in groups])
    sizes = np.array([len(g) for g in groups])
    nz = np.abs(mean) > eps
    n_eff = int(nz.sum())
    pos = int((mean[nz] > 0).sum())
    # Both pairs present, both nonzero at `eps`, and of opposite sign. The case
    # the unit exists to rule on.
    disagree = np.array([
        len(g) == 2 and bool(np.all(np.abs(g) > eps))
        and bool(g[0] * g[1] < 0) for g in groups])
    cancel = np.array([disagree[k] and abs(mean[k]) <= eps
                       for k in range(len(groups))])
    # The pair reading with the unit held fixed and only the zero test moved to
    # `eps`, so the unit change and the tolerance change are separable.
    n_eff_pair_at_eps = int((np.abs(d) > eps).sum())
    return {
        "n_items": int(len(iid)),
        "n_items_with_both_pairs": int((sizes == 2).sum()),
        "n_items_with_one_pair": int((sizes == 1).sum()),
        "n_eff_item": n_eff, "n_positive_item": pos,
        "tie_rate_item": float(1 - n_eff / len(iid)),
        "sign_proportion_item": pos / n_eff if n_eff else float("nan"),
        "p_two_sided_item":
            binomtest(pos, n_eff, 0.5).pvalue if n_eff else float("nan"),
        "n_items_sign_disagreement": int(disagree.sum()),
        "n_items_sign_disagreement_cancelling": int(cancel.sum()),
        "n_eff_pair_at_eps": n_eff_pair_at_eps,
        "unit_is": "item (P2-D20). `n_eff` above is the superseded PAIR count, "
                   "retained because v2.7 section 2.1 publishes it.",
        # P2-D21. The pair block carries `significant_at_corrected_alpha` and
        # `armb_floor.type_ii_gap` reads its `sign_proportion`; neither had an
        # item-unit counterpart, which is how the diagnostic could be corrected
        # to the item unit in P2-D20 while the claims resting on it kept citing
        # the pair reading. Both are emitted here so they move together.
        "significant_at_corrected_alpha_item": bool(
            n_eff and binomtest(pos, n_eff, 0.5).pvalue < SP.ALPHA),
        # SIGNED. Negative means the neutral baseline sits ABOVE p0, which is a
        # Type I exposure and not the Type II cost P2-D14 describes.
        "type_ii_gap_item": (0.5 - pos / n_eff) if n_eff else float("nan"),
        "ci95_item": list(binomtest(pos, n_eff, 0.5)
                          .proportion_ci(confidence_level=0.95)) if n_eff
                     else [float("nan"), float("nan")],
    }


def main():
    df, cols, A, ids, sets = TR.item_sets()
    ch = TR.load_choices()
    keep = set(int(i) for i in ids[sets["size_tile_confirmatory"]])
    k = inertness_floor()
    checks = [check_floor(j) for j in (k - 2, k - 1, k, k + 1)]
    half = [check_floor(k, both_permutations=False)]
    c5 = c5_delta_A(ch, A, keep)
    # P2-D20 binds the unit. A run that formed n_eff at the pair, or rescaled a
    # 216-pair rate to 108, fails here rather than reporting a denominator a
    # reader cannot tell apart from the right one.
    P2D.bind_quantity_c_unit(P2D.P2D20_UNIT, P2D.P2D20_SIGN_DISAGREEMENT,
                             True, True, P2D.P2D19_EPS)
    eff = json.load(open("results/T5_c5_effect.json"))["sets"]["size_tile_confirmatory"]

    # P2-D21. The universal claim P2-D12 and P2-D14 both rest on, re-evaluated at
    # P2-D20's unit. Emitted rather than asserted in prose, because the claim is
    # what those two decisions cite and it is now false.
    six = tuple(m for m in TR.LADDER if m != "CTRL")
    props = {m: c5[m]["sign_proportion_item"] for m in TR.LADDER}
    gaps = {m: c5[m]["type_ii_gap_item"] for m in TR.LADDER}
    above = tuple(m for m in TR.LADDER if props[m] > 0.5)
    neutral = {
        "unit": "item (P2-D20)",
        "claim_withdrawn": "at or below 0.5 on all seven models",
        "all_seven_at_or_below_p0": max(props.values()) <= 0.5,
        "six_ladder_at_or_below_p0": max(props[m] for m in six) <= 0.5,
        "range_all_seven": [min(props.values()), max(props.values())],
        "range_six_ladder": [min(props[m] for m in six),
                             max(props[m] for m in six)],
        "models_above_p0": list(above),
        "sign_proportion": props,
        "type_ii_gap_signed": gaps,
        "significant_at_corrected_alpha": [
            m for m in TR.LADDER if c5[m]["significant_at_corrected_alpha_item"]],
        "ci95": {m: c5[m]["ci95_item"] for m in TR.LADDER},
        "p0_retained": 0.5,
        "what_survives":
            "The claim itself, stated directly per P2-D22 and not as a tally: a "
            "content-neutral insertion does not drift toward the salience pole. "
            "The per-model proportion runs 0.1951 to 0.5556. Only CTRL resolves "
            "at the corrected alpha and it resolves DOWNWARD, at the item unit "
            "as at the pair unit. B2 sits AT the null: 0.5556 here on n_eff 36, "
            "p = 0.6177, 95% exact [0.3810, 0.7206], and exactly 0.5000 under "
            "three of five aggregations of these same rows, including one at "
            "this unit. Two votes of 36 return it to 0.5000 and it is the only "
            "model whose point estimate changes side between the two units.",
        "what_does_not_survive":
            "The claim as worded, on all seven models, and P2-D15's fallback "
            "restatement on the six ladder models, which fails for a different "
            "reason: the exception is a ladder model and not the control, so the "
            "fallback breaks where the D111 admissibility ruling it exists to "
            "make optional does not. Also P2-D14's clause that recalibrating p0 "
            "would make a positive F1 result easier to obtain, which is true on "
            "six models and false on B2, where recalibration would raise p0.",
        "negative_gap_is_not_a_smaller_cost":
            "P2-D14 defines the gap as 0.5 minus the proportion and calls it a "
            "Type II cost. On B2 it is -0.0556. A negative gap is a different "
            "quantity: there is no gap between p0 and the baseline for a real "
            "effect to fail to clear, and instead a B2 (c) result significant "
            "against p0 = 0.5 but at or below 0.5556 is nominally positive while "
            "sitting at or below what a content-neutral insert does. That is a "
            "Type I exposure and P2-D14's licence box has no sentence for it. It "
            "is reported with B2's (c) verdict.",
        "p0_is_retained_on":
            "The structural ground, which uses no measurement: moving p0 "
            "recalibrates a preregistered test against a different manipulation, "
            "on a coordinate Paper 1 never used. P2-D12 and P2-D14 both state it "
            "first and it is independently sufficient. P2-D22 withdraws "
            "'conservative' as a justification for p0: conservativeness is a "
            "per-model property and the design is not conservative on B2 at the "
            "point estimate. Where a Type II cost is real it is reported as a "
            "signed per-model gap, which says more than the adjective did.",
        "preregistered_conditional_that_fired":
            "v2.7 section 5 wrote both answers before the number was seen: 'a "
            "proportion above 0.5 would have been a reason to keep a "
            "direction-matched reference and to reconsider p0'. At the item unit "
            "the antecedent fires on B2. It is discharged by reconsidering and "
            "retaining, which P2-D21 records, not by reading the antecedent away.",
    }
    P2D.bind_neutral_baseline(0.5, neutral["all_seven_at_or_below_p0"],
                              neutral["six_ladder_at_or_below_p0"], above, gaps)
    # P2-D22 governs how the above is worded wherever it is stated live.
    P2D.bind_neutral_claim_wording(False, False, False)
    # P2-D23. The ext_i floor does not reach the confirmatory set, and the reason
    # is that ext_i is a strictly positive per-item constant. Assert the premise,
    # not the conclusion: at ext_i = 0 the sign identity fails and the floor does
    # reach (c). None of (a), (b), (c) reads ext_i, so the list is empty.
    _, _, _, _ext = H.item_axis()[:4]
    _sz = sets["size_tile_confirmatory"]
    P2D.bind_ext_floor(float(_ext[_sz].min()), int(_sz.sum()), ())
    P2D.check_p1_ext_floor_source()

    rows = {}
    for m, R in P2D.P2D8_C5_REFERENCE.items():
        moved = eff[m]["n_items_with_a_changed_pair"]
        n_eff = int(round(N * (1 - c5[m]["tie_rate"])))
        rows[m] = {
            "c5_items_moved_of_108": moved,
            "inertness_floor_items": k,
            "floor_as_multiple_of_c5": k / moved,
            "c5_change_rate": 1 - R,
            "c5_tie_rate_analogue": c5[m]["tie_rate"],
            "n_eff_at_a_c5_like_tie_rate": n_eff,
            "n_eff_at_a_c5_like_tie_rate_is":
                "SUPERSEDED for quantity (c) by P2-D20: round(108 * (1 - tie_rate)) "
                "applies an item scale to a 216-pair rate and gives neither unit. "
                "Retained unchanged because v2.7 section 3.2 publishes it and the "
                "power figures below are computed from it. P2-D20's n_eff is "
                "diagnostic_c5_direction.per_model[m].n_eff_item.",
            "n_eff_item_p2d20": c5[m]["n_eff_item"],
            "sign_power_at": {str(p): SP.power(n_eff, p) for p in P_GRID},
            "p1_at_80_power": SP.detectable(n_eff),
        }

    out = {
        "purpose": "Arm B's detection limits under P2-D12: inertness against "
                   "zero at full n, c5 as context, sign test ungated. Replaces "
                   "the ceiling in results/T5_detection_ceiling.json, which "
                   "measured the superseded gated design and is kept because "
                   "PREREGISTRATION_v2.6.md section 3.3 reports it.",
        "n_confirmatory": N, "alpha": SP.ALPHA,
        "quantity_a_inertness": {
            "null": 0.0,
            "why_zero_is_the_null":
                "P2-D9: P1's chooser is an argmax over teacher-forced "
                "log-probabilities with no sampling, so an identical prompt "
                "returns an identical choice and a manipulation that changes no "
                "choice is inert exactly. No reference manipulation is needed to "
                "establish that, which is why the c5 comparison no longer gates.",
            "instrument": "P2-D8's cluster bootstrap, items, 10,000 resamples, "
                          "seed 20260910, at 1 - alpha, against 0 rather than R_m",
            "floor_items_of_108": k,
            "floor_share": k / N,
            "floor_checks_both_permutations_moving": checks,
            "floor_check_one_permutation_moving": half,
            "floor_is_a_count_not_a_rate":
                "The item-level mean of a resample is zero exactly when the "
                "resample contains no moving item, so the floor depends on how "
                "many items moved and not on how far. A mover that changes one "
                "of its two renderings counts the same as one that changes both.",
            "full_n": N,
        },
        "quantity_b_magnitude_context": {
            "role": "DESCRIPTIVE. Reported with the bootstrap half-width. Gates "
                    "nothing and spends no alpha.",
            "reference": P2D.P2D8_C5_REFERENCE,
            "half_width_range": list(P2D.P2D11_CEILING["half_width"]),
            "resolution_note":
                "A same-option-rate gap below roughly 0.15 is still unresolvable. "
                "Under P2-D12 that limits what the CONTEXT can say, not whether "
                "the movement half fires.",
        },
        "quantity_c_direction": {
            "instrument": "P2-D6 exact two-sided sign test, p0 = 0.5, unchanged",
            "effective_n": "108 * (1 - tie rate), with no lower bound imposed by "
                           "quantity (b). Under the superseded gate it was capped "
                           "at 32 to 58.",
            "tie_rate_is_not_knowable_before_T7": True,
            "c5_tie_rate_analogue_caveat":
                "c5's tie rate is a structurally matched manipulation's tie rate, "
                "not a measurement of F1's. Same caveat as reports/"
                "T5_sigma_prior.md section 0. It sizes nothing and is reported so "
                "the sign test's likely position is visible rather than assumed.",
        },
        "diagnostic_c5_direction": {
            "question": "Does a content-neutral insertion drift toward "
                        "o*_infinity, which is P1's salience pole? If it did, a "
                        "positive F1 sign test would be explicable without "
                        "adversary tracking.",
            "answer": "No. The sign proportion is at or below 0.5 on all seven "
                      "models, so p0 = 0.5 is conservative for detecting movement "
                      "toward o*_infinity.",
            "not_adopted_as_a_null":
                "P2-D6 fixes p0 = 0.5. Moving it to c5's proportion would "
                "recalibrate a preregistered test against a different "
                "manipulation. This is a reported diagnostic and nothing else.",
            "per_model": c5,
            # P2-D21. `answer` above is the PAIR reading and is kept unchanged
            # because v2.7 section 2.1 publishes it. It is FALSE at P2-D20's item
            # unit, which is the unit quantity (c) runs on, and this block is what
            # a live document cites instead.
            "answer_at_item_unit_p2d21": neutral,
        },
        "diagnostic_blind_spot_measured": {
            "definition": "tie rate minus same-option rate on the c5 contrast, "
                          "which is P2-D10's gap measured on a real manipulation "
                          "rather than bounded from the geometry",
            "range": [min(v["blind_spot"] for v in c5.values()),
                      max(v["blind_spot"] for v in c5.values())],
            "per_model": {m: v["blind_spot"] for m, v in c5.items()},
        },
        "per_model": rows,
        "a_null_licenses":
            "That the framing changed the chosen option on fewer than "
            f"{k} of {N} items, which at this n is indistinguishable from a "
            "manipulation that changes nothing. Because the no-effect rate is "
            "exactly 1.0 and not estimated, this is a statement about the "
            "framing, not about measurement noise.",
        "a_null_does_not_license":
            "That models are insensitive to adversary structure. A framing can "
            "move choices without moving them toward o*_infinity, which is what "
            "quantity (c) separates, and quantity (c)'s power is set by the "
            "observed tie rate. It also does not license any claim about "
            "magnitude: quantity (b)'s resolution is roughly 0.15 on the "
            "same-option rate, so a framing that moves choices materially less "
            "than c5 does is not distinguishable from one that moves them as "
            "much. The A coordinate additionally cannot see a switch between two "
            "A-tied options, measured at 0.0000 to 0.0509 on the c5 contrast.",
    }
    # P2-D12 is the source; this script must reproduce it. A run that gated on
    # the c5 comparison, or that used a floor the log does not state, fails here.
    P2D.bind_armb_quantities(out["quantity_a_inertness"]["null"],
                             c5_gates=False, sign_p0=0.5,
                             quantities=P2D.P2D12_QUANTITIES)
    assert k == P2D.P2D12_INERTNESS_FLOOR_ITEMS, (
        f"P2-D12 states an inertness floor of {P2D.P2D12_INERTNESS_FLOOR_ITEMS} "
        f"items; this run gives {k}. docs/P2/DECISIONS.md is the source.")

    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)

    print(f"n = {N}, alpha = {SP.ALPHA:.6f}\n")
    print(f"(a) inertness floor: {k} of {N} items must carry a changed rendering")
    for c in checks + half:
        print(f"      k={c['k']:2d} item mean {c['item_mean']:.4f}  "
              f"lo {c['lo']:.6f}  {'clears 0' if c['clears_zero'] else 'does not'}")
    print(f"\n  {'model':6s} {'c5 moved':>9s} {'floor/c5':>9s} {'c5 tie':>7s} "
          f"{'n_eff':>6s} " + " ".join(f"p1={p:.2f}" for p in P_GRID) + "   p1@80%")
    for m, v in rows.items():
        print(f"  {m:6s} {v['c5_items_moved_of_108']:9d} "
              f"{v['floor_as_multiple_of_c5']:9.2f} "
              f"{v['c5_tie_rate_analogue']:7.4f} "
              f"{v['n_eff_at_a_c5_like_tie_rate']:6d} "
              + " ".join(f"{v['sign_power_at'][str(p)]:7.3f}" for p in P_GRID)
              + f"   {v['p1_at_80_power']}")
    print("\ndiagnostic: c5's own delta-A sign proportion (reported, not adopted as p0)")
    for m, v in c5.items():
        print(f"  {m:6s} n_eff={v['n_eff']:3d}  prop={v['sign_proportion']:.4f}  "
              f"p={v['p_two_sided']:.4f}  "
              f"{'below 0.5 at the corrected alpha' if v['significant_at_corrected_alpha'] else ''}")
    print("\nP2-D21: the same diagnostic at P2-D20's ITEM unit, which is the unit")
    print("        quantity (c) runs on. The pair block above is superseded for it.")
    for m in TR.LADDER:
        v = c5[m]
        print(f"  {m:6s} n_eff={v['n_eff_item']:3d}  "
              f"prop={v['sign_proportion_item']:.4f}  "
              f"p={v['p_two_sided_item']:.4f}  "
              f"gap={v['type_ii_gap_item']:+.4f}  "
              f"ci95=[{v['ci95_item'][0]:.4f}, {v['ci95_item'][1]:.4f}]"
              + ("  SIGNIFICANT at the corrected alpha"
                 if v["significant_at_corrected_alpha_item"] else "")
              + ("  ABOVE p0: gap is negative, exposure is Type I"
                 if v["type_ii_gap_item"] < 0 else ""))
    print(f'  "at or below 0.5 on all seven models" holds: '
          f'{neutral["all_seven_at_or_below_p0"]}')
    print(f'  P2-D15\'s six-ladder restatement holds:        '
          f'{neutral["six_ladder_at_or_below_p0"]}')
    print(f'  p0 retained at {neutral["p0_retained"]}, on the structural ground')

    b = out["diagnostic_blind_spot_measured"]["range"]
    print(f"\ndiagnostic: P2-D10 blind spot on the c5 contrast, "
          f"{b[0]:.4f} to {b[1]:.4f}")
    print(f"\nwritten: {OUT}")
    return 0


def demo():
    """The floor must be the smallest `k` the real bootstrap accepts, and it must
    be far below what the superseded gate required. If it were not, P2-D12 would
    be restructuring the design for nothing."""
    k = inertness_floor()
    assert check_floor(k)["clears_zero"], f"floor {k} does not clear zero"
    assert not check_floor(k - 1)["clears_zero"], f"{k} is not the smallest"
    assert check_floor(k, both_permutations=False)["clears_zero"], \
        "the floor must not depend on how far a mover moves, only on how many moved"
    eff = json.load(open("results/T5_c5_effect.json"))["sets"]["size_tile_confirmatory"]
    worst = max(k / v["n_items_with_a_changed_pair"] for v in eff.values())
    gated = P2D.P2D11_CEILING["change_rate_multiple_of_c5"][0]
    assert worst < gated, (
        f"the inertness floor is {worst:.2f}x c5 at worst and the superseded gate "
        f"was {gated:.2f}x at best; P2-D12 buys nothing")
    print(f"ok: floor is {k} of {N} items, {worst:.2f}x c5 at worst, against the "
          f"superseded gate's {gated:.2f}x at best")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
