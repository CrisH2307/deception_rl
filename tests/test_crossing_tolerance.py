"""P2-D28 and P2-D29, asserted from `results/T1_crossing_tolerance.json` and from the
live constant, so the artifact, the binding and `adversary._crossings` cannot drift apart.

The invariant this turns a false alarm into: after P2-D29 the closed form disagrees
with bisection on exactly the tolerance-determined items, because it tests strict
crossing and cannot see a tie-break flip, and on no other item.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import adversary as adv      # noqa: E402
import p2_decisions as d     # noqa: E402

R = json.load(open("results/T1_crossing_tolerance.json"))


def test_bindings_hold_on_the_live_constant():
    assert d.bind_parallel_tol(adv.PARALLEL_TOL, R)
    assert set(d.bind_tolerance_determined_disclosure(R)) == set(d.P2D28_DISCLOSURE_FIELDS)


def test_residual_is_exactly_the_tolerance_determined_set():
    for name, base in R["bases"].items():
        after = base["cross_check_adopted_parallel_tol"]
        assert after["residual_equals_tol_set"], name
        assert after["n_classification_disagree"] == base["n_tolerance_determined"], name
        assert after["n_bisection_inf_closed_form_finite"] == 0, name
        assert after["max_abs_gap_both_finite_outside_tol_set"] < R["gap_edge"], name


def test_the_rejected_rule_leaves_parallel_roots_in_place():
    """Why P2-D29 tests the coefficient of x alone: converging pairs carry a real
    numerator over a rounding-size denominator, so the both-coefficients rule keeps
    their roots. Premise, not range: the denominator sits below the gap, the
    numerator above it."""
    c = R["bases"]["pool_200000"]["coefficients"]
    assert c["n_root_pairs_converging"] > 0
    assert c["converging_max_abs_den"] <= c["den_gap"][0] < adv.PARALLEL_TOL
    assert c["converging_min_abs_num"] > adv.PARALLEL_TOL
    rej = R["bases"]["pool_200000"]["cross_check_both_below_not_adopted"]
    assert rej["n_classification_disagree"] < R["bases"]["pool_200000"]["n_tolerance_determined"]


def test_every_tolerance_determined_item_is_divergent_only_by_tie_break():
    p = R["bases"]["pool_200000"]
    assert p["tiebreak_only_subset_of_tolerance_determined"]
    assert p["n_divergent_only_by_tie_break"] == p["n_tolerance_determined"]
