"""Quantity (a)'s floor, restated on numerical grounds, and two rulings beside it.

WHAT CHANGED, AND WHY THE OLD JUSTIFICATION WAS WRONG.

P2-D12 set the inertness floor at 7 of 108 items by asking how many movers the
cluster bootstrap needs before its lower bound clears zero. That derivation does
not survive P2-D9. Under P2-D9 the scorer is deterministic, so if the framing
truly moves nothing then every item has `ΔA = 0`, every resample returns exactly
0, and the lower bound never clears. **Type I error is exactly 0, not `alpha`.**
The bootstrap was guarding no statistical quantity, and a single changed option
already establishes deductively that the framing moved something.

The bootstrap keeps its role in quantity (b) and loses it in (a), and the
asymmetry is real rather than a convenience. (b) compares two population rates
that are both estimated from a finite item sample, in the interior of the
parameter space; an interval is the right instrument there. (a) tests a one-sided
point null at the boundary, `rate = 0`, against data with no sampling error in
the choice given the prompt. Nothing is estimated, so nothing needs an interval.

THE REAL HAZARD IS NUMERICAL. Floating-point nondeterminism across batch
compositions can flip a near-tie argmax, and T7 runs in a different session and
on different hardware than the run that produced Paper 1's frozen `cond4`. That
noise is not zero and it is not knowable in advance.

IT IS ALSO ALREADY BEING MEASURED. Under P2-D1, `F0` is Paper 1's Format V `base`
rendering, so `F0`'s prompt is the `cond4` prompt. T7's `F0`-versus-`cond4`
disagreement count is therefore a null perturbation: identical text, different
run. It is the empirical noise floor, and `T7.md` step 2 already computes it for
the environment-equivalence check, for a purpose that predates this decision.

This also closes something `PREREGISTRATION_v2.6.md` section 1.1 had to leave
open. It said the no-effect rate of 1.0 could be argued from the code path but
not corroborated, because the frozen artifacts contain no repeated rendering.
T7's `F0` run is that repeated rendering. The quantity v2.6 could only argue,
T7 measures.

Run: python3 src/armb_floor.py          (writes results/T5_armb_floor.json)
     python3 src/armb_floor.py --demo   (self-check on the floor rule and D111)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2_decisions as P2D  # noqa: E402

CEILING = "results/T5_inertness_ceiling.json"
OUT = "results/T5_armb_floor.json"
PROVISIONAL_FLOOR = 7        # P2-D12's value, kept as a conservative convention
CROSS_FAMILY = "CTRL"        # P1's D110 cross-family control
LADDER_SIX = ("B2", "B4", "L1", "L2", "L3", "L4")


def floor_for_run(f0_disagreement_items):
    """The inertness floor T7 actually uses. Upward-only revision.

    `f0_disagreement_items` is the number of confirmatory items on which the
    re-run `F0` disagrees with Paper 1's frozen `cond4`. Identical text, different
    run, so it is the measured noise floor.

    The revision is upward-only **by construction**, not by an instruction a
    later session could read past: the rule is a max. A measured noise floor
    below the provisional one cannot lower the bar, which is what stops a quiet
    environment from being used to make the movement half easier to clear after
    F1 has been seen.
    """
    n = int(f0_disagreement_items)
    if n < 0:
        raise ValueError(f"disagreement count cannot be negative: {n}")
    return max(PROVISIONAL_FLOOR, n)


def type_ii_gap(path=CEILING):
    """0.5 minus each model's content-neutral sign proportion, at the PAIR unit.

    P2-D6 fixes `p0 = 0.5` and P2-D12 declined to move it. That is conservative
    against Type I and costly in Type II, and this is the size of the cost: a
    real directional effect that lifts F1 above the neutral baseline but not
    above 0.5 is not detected. Reported so a reader can size it per model rather
    than being told it exists.

    SUPERSEDED for live citation by `type_ii_gap_item` below, per P2-D21. This
    reads the pair block, which P2-D20 superseded as quantity (c)'s unit, and it
    keeps emitting unchanged because `v2.8` section 2.2 publishes its values.
    Every gap here is non-negative; at the item unit one is not.
    """
    d = json.load(open(path))["diagnostic_c5_direction"]["per_model"]
    return {m: {"neutral_sign_proportion": v["sign_proportion"],
                "gap_to_p0": 0.5 - v["sign_proportion"],
                "n_eff": v["n_eff"],
                "below_p0_at_corrected_alpha":
                    v["significant_at_corrected_alpha"]}
            for m, v in d.items()}


def type_ii_gap_item(path=CEILING):
    """The same gap at P2-D20's ITEM unit, which is the unit (c) runs on. P2-D21.

    The gap is SIGNED and one of them is negative. P2-D14 calls this quantity a
    Type II cost, and that reading holds only while the neutral baseline sits at
    or below `p0`. On `B2` at the item unit it does not: the baseline is 0.5556,
    the gap is -0.0556, and there is no gap for a real effect to fail to clear.
    What there is instead is the reverse exposure, a `B2` result significant
    against `p0 = 0.5` but at or below what a content-neutral insert does, which
    is Type I and which P2-D14's licence box has no sentence for.

    The sign is therefore not a detail of presentation. It says which of two
    different statements the number supports, so it is emitted rather than
    reported as a magnitude.
    """
    d = json.load(open(path))["diagnostic_c5_direction"]["per_model"]
    return {m: {"neutral_sign_proportion": v["sign_proportion_item"],
                "gap_to_p0": v["type_ii_gap_item"],
                "gap_is_a_type_ii_cost": v["type_ii_gap_item"] >= 0,
                "baseline_above_p0": v["type_ii_gap_item"] < 0,
                "n_eff": v["n_eff_item"],
                "ci95": v["ci95_item"],
                "p_two_sided": v["p_two_sided_item"],
                "departs_from_p0_at_corrected_alpha":
                    v["significant_at_corrected_alpha_item"]}
            for m, v in d.items()}


def d111_verdict(path=CEILING):
    """Is `sign(ΔA)` admissible for the cross-family control under P1's D111?

    D111 restricts cross-family comparison to choice-based statistics and bans
    raw PMI magnitudes, because the control's tokenizer differs by construction
    and log-probability magnitudes stop being commensurable.

    The operational test, which is what makes this decidable rather than a
    judgement call: **does the statistic change if the tokenizer changes but the
    chosen options do not?** For `sign(ΔA)` it does not.
    `A(o) = (marg_norm(o) - marg_norm(o*_0)) / ext_i` with `ext_i > 0` a per-item
    constant, so `sign(ΔA) = sign(marg_norm(o_5) - marg_norm(o_4))`: an ordinal
    comparison of two options on frozen, model-free item geometry, selected by
    the model's choice and nothing else. No log-probability enters, and the
    statistic is computed within a model and reported as a rate.

    The conclusion is reported both ways regardless, so it does not rest on the
    ruling.
    """
    d = json.load(open(path))["diagnostic_c5_direction"]["per_model"]
    six = {m: d[m]["sign_proportion"] for m in LADDER_SIX}
    return {
        "admissible": True,
        "rule": "sign(delta-A) depends only on which options were chosen and on "
                "frozen model-free item geometry. No log-probability magnitude "
                "enters, and it is computed within a model and reported as a "
                "rate, which is what D111 permits.",
        "operational_test": "Does the statistic change if the tokenizer changes "
                            "but the chosen options do not? For sign(delta-A), "
                            "no. For raw PMI, yes. That is the line D111 draws.",
        "what_remains_inadmissible":
            "logp_sum_chosen, logp_neutral_chosen and any PMI value, compared "
            "across families. The ruling here extends to nothing that reads a "
            "model's scores rather than its choice.",
        "conclusion_holds_without_the_control": max(six.values()) <= 0.5,
        "six_ladder_models": six,
        "max_over_six": max(six.values()),
        "control_proportion": d[CROSS_FAMILY]["sign_proportion"],
        "restated_if_inadmissible":
            "On the six ladder models alone the neutral sign proportion runs "
            f"{min(six.values()):.4f} to {max(six.values()):.4f}, still at or "
            "below 0.5 on every one, so p0 = 0.5 remains conservative and "
            "P2-D12's third rejected alternative stands either way.",
        # P2-D21. Everything above reads the PAIR block and is kept because
        # v2.8 section 3.4 publishes it. At P2-D20's item unit the fallback
        # restatement FAILS, and it fails on a ladder model rather than on the
        # control, so it breaks where the ruling it exists to make optional does
        # not. The ruling itself is untouched: it reads no proportion.
        "restated_at_item_unit_p2d21": _six_ladder_at_item_unit(path),
    }


def _six_ladder_at_item_unit(path=CEILING):
    """P2-D15's fallback restatement, re-evaluated at P2-D20's unit. P2-D21.

    P2-D15 exists to show the D111 admissibility ruling is not load-bearing, by
    restating the conclusion on the six ladder models with the control removed.
    At the item unit that restatement is false, because `B2` is above 0.5 and
    `B2` is a ladder model. The control moves the other way, 0.2453 to 0.1951,
    so the ruling is still not load-bearing for the direction it was about. What
    fails is a universally quantified sentence, not the ruling under it.
    """
    d = json.load(open(path))["diagnostic_c5_direction"]["per_model"]
    six = {m: d[m]["sign_proportion_item"] for m in LADDER_SIX}
    above = [m for m, v in six.items() if v > 0.5]
    return {
        "holds": max(six.values()) <= 0.5,
        "six_ladder_models": six,
        "range": [min(six.values()), max(six.values())],
        "models_above_p0": above,
        "control_proportion": d[CROSS_FAMILY]["sign_proportion_item"],
        "why_it_fails":
            "B2 is above 0.5 at the item unit and B2 is a ladder model, so "
            "removing the control does not rescue the sentence. The control "
            "moves further below 0.5 at this unit, 0.2453 to 0.1951, so the "
            "D111 ruling is still not load-bearing for the direction P2-D15 "
            "was about. The ruling reads no proportion and is untouched; the "
            "restatement is a universal over six models and one exception "
            "breaks it.",
        "replacement":
            "Six of seven models sit at or below 0.5 and the seventh, B2, is "
            "not distinguishable from it. Only CTRL departs at the corrected "
            "alpha and it departs downward, with or without the control "
            "admitted. p0 = 0.5 is retained on the structural ground in P2-D21, "
            "not on a universal claim about the seven.",
    }


def main():
    gaps = type_ii_gap()
    gaps_item = type_ii_gap_item()
    d111 = d111_verdict()
    out = {
        "purpose": "Quantity (a)'s floor on numerical grounds, the Type II cost "
                   "of p0 = 0.5, and the D111 ruling on the control's sign "
                   "proportion. Written before T7 runs.",
        "floor": {
            "provisional": PROVISIONAL_FLOOR,
            "rule": "floor = max(provisional, F0-versus-cond4 disagreement items)",
            "revision_is_upward_only": True,
            "why_not_statistical":
                "Under P2-D9 the scorer is deterministic, so the strict null "
                "gives every item delta-A = 0, every resample returns exactly 0, "
                "and the bootstrap lower bound never clears. Type I error is 0, "
                "not alpha. A single changed option settles inertness "
                "deductively, so the bootstrap guarded no statistical quantity "
                "in quantity (a).",
            "why_not_lowered_to_one":
                "Because the numerical hazard is not zero and is unmeasured "
                "until T7 runs. Setting the floor at 1 before measuring would "
                "set it at its most permissive on an untested assumption of "
                "noiseless reproduction. The provisional 7 is a conservative "
                "convention with no statistical derivation, and it is labelled "
                "as one rather than presented as a computed threshold.",
            "measured_by": "T7.md step 2's F0-versus-cond4 disagreement count, "
                           "computed for the environment-equivalence check, "
                           "whose purpose predates this decision.",
            "caveat":
                "F0 and cond4 are identical text, so the F0 rate measures noise "
                "under an identical prompt. F1 and F2 are longer prompts with "
                "different batch shapes, so their numerical noise could exceed "
                "it. The F0 rate is therefore a LOWER bound on the noise floor, "
                "and it is used as the floor rather than scaled, because any "
                "scaling factor would be invented here.",
            "bootstrap_retained_in_quantity_b":
                "(b) compares two population rates both estimated from a finite "
                "item sample, in the interior of the parameter space. An "
                "interval is the right instrument there and P2-D8's is kept "
                "unchanged, seed included.",
        },
        "type_ii_cost_of_p0_half": {
            "statement": "p0 = 0.5 is conservative against Type I and costly in "
                         "Type II. A null on (c) does not distinguish 'no "
                         "directional effect' from 'a directional effect that "
                         "did not clear the gap between 0.5 and the measured "
                         "content-neutral baseline'.",
            "p0": 0.5,
            "per_model": gaps,
            "gap_range": [min(v["gap_to_p0"] for v in gaps.values()),
                          max(v["gap_to_p0"] for v in gaps.values())],
            "unit_is":
                "PAIR. SUPERSEDED for live citation by P2-D21: quantity (c)'s "
                "unit is the item (P2-D20), and at the item unit one gap is "
                "negative. Retained unchanged because v2.8 section 2.2 "
                "publishes these values and a superseded document must still "
                "reproduce. The live figures are in "
                "type_ii_cost_of_p0_half_at_item_unit.",
        },
        # P2-D21. Additive beside the pair block, never in place of it.
        "type_ii_cost_of_p0_half_at_item_unit": {
            "statement":
                "At P2-D20's item unit the gap is SIGNED and B2's is negative. "
                "p0 = 0.5 is conservative against Type I on the six models whose "
                "gap is positive, and costly in Type II there by the size of the "
                "gap. On B2 the neutral baseline sits ABOVE p0, so there is no "
                "gap for a real effect to fail to clear and the exposure runs "
                "the other way: a B2 (c) result significant against p0 = 0.5 but "
                "at or below 0.5556 is nominally positive while sitting at or "
                "below what a content-neutral insert does. That is Type I and "
                "P2-D14's licence box has no sentence for it.",
            "p0": 0.5,
            "p0_moved": False,
            "per_model": gaps_item,
            "gap_range": [min(v["gap_to_p0"] for v in gaps_item.values()),
                          max(v["gap_to_p0"] for v in gaps_item.values())],
            "models_with_baseline_above_p0":
                [m for m, v in gaps_item.items() if v["baseline_above_p0"]],
            "b2_is_not_evidence_of_upward_drift":
                "B2 is 0.5556 on n_eff 36 with a two-sided p of 0.6177 and a 95% "
                "exact interval of [0.3810, 0.7206], which contains 0.5. The "
                "point estimate reverses the sign of the gap; the evidence does "
                "not establish the reversal. Both facts are reported, because "
                "reporting only the first overstates and only the second hides "
                "the exposure.",
            "reported_with_the_verdict":
                "The signed gap is reported with every (c) verdict, and on B2 "
                "the Type I exposure is named beside it. That is P2-D14's own "
                "disclosure mechanism applied to the case P2-D14 did not have.",
        },
        "d111_ruling": d111,
    }
    # The log is the source (D100); this script reproduces it.
    assert PROVISIONAL_FLOOR == P2D.P2D13_PROVISIONAL_FLOOR
    assert P2D.P2D13_FLOOR_IS_STATISTICAL is False
    assert P2D.P2D13_REVISION_IS_UPWARD_ONLY is True
    assert P2D.P2D15_SIGN_IS_ADMISSIBLE == d111["admissible"]
    for m, want in P2D.P2D14_TYPE_II_GAP.items():
        got = gaps[m]["gap_to_p0"]
        assert abs(got - want) < 1e-12, (
            f"P2-D14 states a Type II gap of {want} for {m}; this run gives {got}")
    P2D.bind_armb_floor(floor_for_run(0), 0, floor_is_statistical=False)
    # P2-D21. p0 does not move, the universal claim is withdrawn, and the signed
    # item-unit gaps are bound. A run that re-asserts "at or below 0.5 on all
    # seven models", or that reports B2's gap as a positive Type II cost, fails
    # here rather than reproducing a claim the log has withdrawn.
    P2D.bind_neutral_baseline(
        out["type_ii_cost_of_p0_half_at_item_unit"]["p0"],
        all_seven_holds=all(v["gap_to_p0"] >= 0 for v in gaps_item.values()),
        six_ladder_holds=d111["restated_at_item_unit_p2d21"]["holds"],
        above_p0=tuple(out["type_ii_cost_of_p0_half_at_item_unit"]
                       ["models_with_baseline_above_p0"]),
        gap_item={m: v["gap_to_p0"] for m, v in gaps_item.items()})

    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)

    print(f"floor: provisional {PROVISIONAL_FLOOR}, "
          f"revised to max({PROVISIONAL_FLOOR}, F0 disagreement items)")
    for n in (0, 3, 7, 12, 40):
        print(f"    F0 disagreement {n:3d} items -> floor {floor_for_run(n):3d}")
    print(f"\nType II cost of p0 = 0.5, gap to the content-neutral baseline")
    print(f"  {'model':6s} {'neutral':>8s} {'gap to 0.5':>11s} {'n_eff':>6s}")
    for m, v in gaps.items():
        print(f"  {m:6s} {v['neutral_sign_proportion']:8.4f} "
              f"{v['gap_to_p0']:11.4f} {v['n_eff']:6d}"
              + ("   below 0.5 at the corrected alpha"
                 if v["below_p0_at_corrected_alpha"] else ""))
    print(f"\nP2-D21: the same gap at P2-D20's ITEM unit, which is (c)'s unit")
    print(f"  {'model':6s} {'neutral':>8s} {'gap to 0.5':>11s} {'n_eff':>6s}")
    for m, v in gaps_item.items():
        print(f"  {m:6s} {v['neutral_sign_proportion']:8.4f} "
              f"{v['gap_to_p0']:+11.4f} {v['n_eff']:6d}"
              + ("   departs from 0.5 at the corrected alpha"
                 if v["departs_from_p0_at_corrected_alpha"] else "")
              + ("   BASELINE ABOVE p0: Type I exposure, not a Type II cost"
                 if v["baseline_above_p0"] else ""))
    r = d111["restated_at_item_unit_p2d21"]
    print(f"  P2-D15's six-ladder restatement at this unit holds: {r['holds']}"
          f"  (above p0: {r['models_above_p0']})")
    print(f"  p0 retained at 0.5 on the structural ground; not moved")

    print(f"\nD111: sign(delta-A) for {CROSS_FAMILY} is "
          f"{'ADMISSIBLE' if d111['admissible'] else 'NOT ADMISSIBLE'}")
    print(f"      conclusion without the control: max over six ladder models = "
          f"{d111['max_over_six']:.4f}, holds = {d111['conclusion_holds_without_the_control']}")
    print(f"\nwritten: {OUT}")
    return 0


def demo():
    """The floor rule must be upward-only, and the D111 conclusion must not
    depend on the model the ruling is about."""
    assert floor_for_run(0) == PROVISIONAL_FLOOR, "a quiet environment lowered the floor"
    assert floor_for_run(PROVISIONAL_FLOOR - 1) == PROVISIONAL_FLOOR
    assert floor_for_run(PROVISIONAL_FLOOR + 5) == PROVISIONAL_FLOOR + 5
    for n in range(0, 60):
        assert floor_for_run(n) >= PROVISIONAL_FLOOR, f"floor fell below at {n}"
        assert floor_for_run(n) >= n, f"floor below the measured noise at {n}"
    try:
        floor_for_run(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative disagreement count was accepted")
    d = d111_verdict()
    # The PAIR unit. Kept because v2.8 sections 2.2 and 3.4 publish it and a
    # superseded document must still reproduce.
    assert d["conclusion_holds_without_the_control"], (
        "the pair-unit fallback restatement no longer holds; v2.8 section 3.4 "
        "publishes it and it must still reproduce")
    g = type_ii_gap()
    assert all(v["gap_to_p0"] >= 0 for v in g.values()), \
        "a pair-unit neutral baseline sits above p0 = 0.5; v2.8 section 2.2 " \
        "publishes these gaps as non-negative and must still reproduce"
    assert abs(P2D.P2D12_INERTNESS_FLOOR_ITEMS - PROVISIONAL_FLOOR) == 0

    # P2-D21, at P2-D20's unit, which is where the claim actually lives. These
    # assert the CORRECTED finding, so they fail if it drifts back. The two
    # asserts above encode the withdrawn wording and are retained only because
    # they guard a published artifact; these are the live ones.
    gi = type_ii_gap_item()
    above = {m for m, v in gi.items() if v["baseline_above_p0"]}
    assert above == set(P2D.P2D21_NEUTRAL_ABOVE_P0), (
        f"P2-D21 records {P2D.P2D21_NEUTRAL_ABOVE_P0} as the models whose "
        f"item-unit neutral baseline sits above p0; this run gives "
        f"{sorted(above)}. The set decides whether the exposure on a model is "
        "Type I or Type II, so it is not a presentational detail.")
    assert not all(v["gap_to_p0"] >= 0 for v in gi.values()), (
        "every item-unit gap is non-negative, so the withdrawn claim 'at or "
        "below 0.5 on all seven models' would hold and P2-D21 would have "
        "nothing to withdraw. Either the unit reverted to the pair or the "
        "diagnostic changed; both are bugs.")
    assert not d["restated_at_item_unit_p2d21"]["holds"], (
        "P2-D15's six-ladder restatement holds at the item unit, which P2-D21 "
        "records as false. The exception is a ladder model, so a run where the "
        "restatement holds is reading the wrong unit.")
    b2 = gi["B2"]
    assert not b2["departs_from_p0_at_corrected_alpha"], (
        "B2's item-unit baseline departs from 0.5 at the corrected alpha, so "
        "0.5556 would be evidence of upward drift and P2-D21's ruling that p0 "
        "stands on the structural ground alone would need revisiting")
    assert b2["ci95"][0] < 0.5 < b2["ci95"][1], (
        f"B2's 95% exact interval {b2['ci95']} no longer contains 0.5; P2-D21 "
        "cites it as the reason 0.5556 is not evidence of drift")
    assert gi["CTRL"]["departs_from_p0_at_corrected_alpha"] and \
        gi["CTRL"]["gap_to_p0"] > 0, (
        "CTRL no longer departs from 0.5 downward at the corrected alpha; "
        "P2-D21's 'the conclusion survives' rests on the only significant "
        "departure still being downward")
    print(f"ok: floor is upward-only and never below {PROVISIONAL_FLOOR} or the "
          f"measured noise; pair-unit figures still reproduce (max over six "
          f"{d['max_over_six']:.4f}, all gaps non-negative); at P2-D20's item "
          f"unit the baseline is above p0 on {sorted(above)}, the six-ladder "
          f"restatement fails, and B2's 95% interval "
          f"[{b2['ci95'][0]:.4f}, {b2['ci95'][1]:.4f}] contains 0.5")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
