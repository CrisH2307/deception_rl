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
    """0.5 minus each model's content-neutral sign proportion.

    P2-D6 fixes `p0 = 0.5` and P2-D12 declined to move it. That is conservative
    against Type I and costly in Type II, and this is the size of the cost: a
    real directional effect that lifts F1 above the neutral baseline but not
    above 0.5 is not detected. Reported so a reader can size it per model rather
    than being told it exists.
    """
    d = json.load(open(path))["diagnostic_c5_direction"]["per_model"]
    return {m: {"neutral_sign_proportion": v["sign_proportion"],
                "gap_to_p0": 0.5 - v["sign_proportion"],
                "n_eff": v["n_eff"],
                "below_p0_at_corrected_alpha":
                    v["significant_at_corrected_alpha"]}
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
    }


def main():
    gaps = type_ii_gap()
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
    assert d["conclusion_holds_without_the_control"], (
        "the neutral-baseline conclusion needs CTRL, so the D111 ruling is "
        "load-bearing and the fallback restatement does not hold")
    g = type_ii_gap()
    assert all(v["gap_to_p0"] >= 0 for v in g.values()), \
        "a neutral baseline sits above p0 = 0.5; the Type II statement reverses"
    assert abs(P2D.P2D12_INERTNESS_FLOOR_ITEMS - PROVISIONAL_FLOOR) == 0
    print(f"ok: floor is upward-only and never below {PROVISIONAL_FLOOR} or the "
          f"measured noise; D111 conclusion holds on the six ladder models "
          f"(max {d['max_over_six']:.4f}); all Type II gaps non-negative")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
