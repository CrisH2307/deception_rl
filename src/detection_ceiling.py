"""The two Arm B power limits in one place, and what a null therefore licenses.

The design has two separate resolution limits and they are stated in two separate
documents. A reader assembling them has to combine `PREREGISTRATION_v2.5.md`
section 2.3 with `v2.4` section 3.2, and nothing tells them the two compose. They
do, and unfavourably.

  LIMIT 1, the reference comparison.  P2-D8's cluster bootstrap has a half-width
  of 0.1412 to 0.1667 on the confirmatory set. A framing whose same-option rate
  sits within roughly 0.15 of the model's `R_m` is "indistinguishable", which
  P2-D8 already rules is not support for H-B. So the movement half only fires on
  a framing that changes choices on `R_m - h_m` fewer pairs than `c5` does.

  LIMIT 2, the sign test.  Ties carry no sign, so the effective `n` is
  `108 * (1 - tie rate)`. At a 30% tie rate the test reaches 80% power only at
  `p1 = 0.721`.

HOW THEY COMPOSE.  Rejecting H-B for a cell needs both halves (P2-D8). The
movement half fires only at a framing same-option rate at or below
`T*_m = R_m - h_m`. Since same-option <= tie (`v2.5` section 3), the tie rate at
that boundary is at least `T*_m`, so the sign test's effective `n` there is AT
MOST `108 * (1 - T*_m)`. That is an upper bound on the sign test's power at the
weakest framing effect limit 1 can resolve, and it is computed per model below.

The direction to notice: the two limits do not trade off. A framing weak enough
to sit near limit 1's boundary leaves the sign test with the effective `n` printed
in `n_eff_max`, and on the models with a high `R_m` that is a small number.

Also recorded here because it belongs with these two and is stated a third place
(`v2.5` section 1): `n = 108` against `v2.0` section 8.2's benchmark of 400. The
shortfall in information is real and does not disappear because P2-D6 changed the
statistic. These three are the whole of what limits Arm B's detection, and this
file is where a reader gets them together.

Run: python3 src/detection_ceiling.py          (writes results/T5_detection_ceiling.json)
     python3 src/detection_ceiling.py --demo   (self-check on the composition)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2_decisions as P2D  # noqa: E402
import sign_power as SP     # noqa: E402

TIE_REF = "results/T5_tie_reference.json"
OUT = "results/T5_detection_ceiling.json"
N = SP.N_CONFIRMATORY
P_GRID = (0.60, 0.65, 0.70, 0.75, 0.80)


def half_widths(path=TIE_REF):
    """P2-D8's instrument resolution, per model, from its own adoption check.

    The check ran the two references against each other on the confirmatory set.
    Its interval half-width is the smallest reference gap the instrument can
    resolve, and it is model-specific rather than the 0.1412-to-0.1667 range the
    preregistration quotes as a summary.
    """
    d = json.load(open(path))["instrument_check_permutation_minus_c5"]
    return {m: (v["hi"] - v["lo"]) / 2.0 for m, v in d.items()}


def main():
    h = half_widths()
    rows = {}
    for m, R in P2D.P2D8_C5_REFERENCE.items():
        t_star = R - h[m]
        n_eff_max = int(N * (1 - t_star))          # tie >= same-option, so this bounds
        rows[m] = {
            "c5_reference_R_m": R,
            "c5_change_rate": 1 - R,
            "bootstrap_half_width": h[m],
            "framing_same_option_rate_needed": t_star,
            "framing_change_rate_needed": 1 - t_star,
            "change_rate_multiple_of_c5": (1 - t_star) / (1 - R),
            "n_eff_max_at_that_boundary": n_eff_max,
            "sign_power_upper_bound_at": {
                str(p): SP.power(n_eff_max, p) for p in P_GRID},
            "p1_at_80_power_upper_bound": SP.detectable(n_eff_max),
        }
    out = {
        "purpose": "The two Arm B detection limits stated together, with what a "
                   "null does and does not license. Written before T7 runs.",
        "n_confirmatory": N,
        "alpha": SP.ALPHA,
        "limit_1_reference_comparison": {
            "instrument": "P2-D8 cluster bootstrap, items, 10,000 resamples, "
                          "seed 20260910, at 1 - alpha",
            "half_width_range": [min(h.values()), max(h.values())],
            "consequence": "A same-option-rate gap below roughly 0.15 is not "
                           "resolvable. Such a cell is 'indistinguishable', which "
                           "P2-D8 rules is not support for H-B.",
        },
        "limit_2_sign_test": {
            "instrument": "P2-D6 exact two-sided sign test against p0 = 0.5",
            "effective_n": "108 * (1 - tie rate); ties carry no sign",
            "p1_at_80_power_at_30_percent_ties": 0.721,
            "source": "results/T5_sign_power.json",
        },
        "limit_3_information": {
            "n_adopted": N,
            "n_benchmark_v2_0_section_8_2": 400,
            "statement": "P2-D6 replaced the mean with a sign test, so section "
                         "8.2's curve no longer governs the confirmatory test. "
                         "The shortfall in information is unchanged by that. A "
                         "modest directional effect will not be detected, and "
                         "realized power is reported rather than assumed.",
        },
        "composition":
            "Rejecting H-B needs both halves. The movement half fires only at a "
            "framing same-option rate at or below R_m - h_m. Same-option <= tie, "
            "so at that boundary the tie rate is at least R_m - h_m and the sign "
            "test's effective n is at most 108 * (1 - (R_m - h_m)). The per-model "
            "sign_power_upper_bound_at values are that bound. The two limits do "
            "not trade off in the design's favour.",
        "per_model": rows,
        "a_null_licenses":
            "That the framing did not move choices detectably more than Paper 1's "
            "c5 insert moved them, at this n, on this tile, with this coordinate. "
            "c5 is an active comparator, not a no-manipulation baseline "
            "(results/T5_c5_effect.json), so this is a statement about relative "
            "magnitude and not about absence of movement.",
        "a_null_does_not_license":
            "That models are insensitive to adversary structure. Three separate "
            "readings produce the same null and the design does not separate "
            "them: the models are insensitive; T3's F1/F2 are too weak to move "
            "anything, which is a fact about the templates; or the effect is real "
            "and smaller than the limits above. The A coordinate additionally "
            "cannot see a switch between two A-tied options, on 48 of 108 "
            "confirmatory items (v2.5 section 3).",
    }
    # P2-D11 quotes these four ranges. The constant is the source; this script
    # must reproduce it. A drift fails here, not in the paper.
    span = {
        "half_width": (min(h.values()), max(h.values())),
        "change_rate_multiple_of_c5": (
            min(v["change_rate_multiple_of_c5"] for v in rows.values()),
            max(v["change_rate_multiple_of_c5"] for v in rows.values())),
        "n_eff_max": (min(v["n_eff_max_at_that_boundary"] for v in rows.values()),
                      max(v["n_eff_max_at_that_boundary"] for v in rows.values())),
        "p1_at_80_power": (
            min(v["p1_at_80_power_upper_bound"] for v in rows.values()),
            max(v["p1_at_80_power_upper_bound"] for v in rows.values())),
    }
    for k, (a, b) in span.items():
        wa, wb = P2D.P2D11_CEILING[k]
        assert abs(a - wa) < 1e-9 and abs(b - wb) < 1e-9, (
            f"P2-D11 states {k} of {wa} to {wb}; this run gives {a} to {b}. "
            "docs/P2/DECISIONS.md is the source.")
    out["ranges"] = {k: list(v) for k, v in span.items()}
    assert out["limit_3_information"]["n_benchmark_v2_0_section_8_2"] == \
        P2D.P2D11_N_BENCHMARK

    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    print(f"n = {N}, alpha = {SP.ALPHA:.6f}\n")
    print(f"  {'model':6s} {'R_m':>7s} {'h_m':>7s} {'T* needed':>10s} "
          f"{'change needed':>14s} {'x c5':>6s} {'n_eff<=':>8s} "
          + " ".join(f"p1={p:.2f}" for p in P_GRID) + "   p1@80%")
    for m, v in rows.items():
        print(f"  {m:6s} {v['c5_reference_R_m']:7.4f} {v['bootstrap_half_width']:7.4f} "
              f"{v['framing_same_option_rate_needed']:10.4f} "
              f"{v['framing_change_rate_needed']:14.4f} "
              f"{v['change_rate_multiple_of_c5']:6.2f} "
              f"{v['n_eff_max_at_that_boundary']:8d} "
              + " ".join(f"{v['sign_power_upper_bound_at'][str(p)]:7.3f}" for p in P_GRID)
              + f"   {v['p1_at_80_power_upper_bound']}")
    print(f"\nwritten: {OUT}")
    return 0


def demo():
    """The composition must be an upper bound, and it must bind.

    If `n_eff_max` were not smaller than the unrestricted `n`, limit 1 would cost
    the sign test nothing and this file would be claiming a ceiling that is not
    there.
    """
    h = half_widths()
    for m, R in P2D.P2D8_C5_REFERENCE.items():
        t_star = R - h[m]
        n_eff_max = int(N * (1 - t_star))
        assert 0 < n_eff_max < N, f"{m}: n_eff_max {n_eff_max} does not bind"
        assert SP.power(n_eff_max, 0.70) <= SP.power(N, 0.70), f"{m}: not a bound"
        assert SP.power(n_eff_max, 0.5) <= SP.ALPHA + 1e-12, f"{m}: size above alpha"
    lo, hi = min(h.values()), max(h.values())
    assert 0.14 < lo < 0.15 and 0.16 < hi < 0.17, \
        f"half-widths {lo:.4f} to {hi:.4f} no longer match the 0.1412-0.1667 quoted"
    print(f"ok: half-widths {lo:.4f} to {hi:.4f} match the preregistered range; "
          f"n_eff_max binds on all {len(h)} models")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
