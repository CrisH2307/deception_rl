"""v2.21's verdict rests on these premises. Asserted from the artifact, so a change
to either beta_c method that moves one of them fails here, not in a pool figure.

Premises, not ranges: group A is spurious because both crossing coefficients are
rounding residue and the spec's predicate never leaves o*_0; group B is a tie-break
flip because the winner never strictly beats o*_0; single-crossing holds because
o*_0 never regains; and the 2,748 stands because every closed-form entrant is in
group A.
"""
import json

D = json.load(open("results/T1_beta_c_disagreement.json"))


def test_group_A_is_rounding_residue_and_never_leaves_o0():
    for k in ("group_A_closed_form_finite_bisection_inf", "both_finite_closed_form_earlier"):
        g = D[k]
        assert g["n_both_coeffs_below_eps_tie"] == g["n"], k
        assert g["max_lead_over_o0"] < D["d51_band"], k
        assert g["n_o0_regains"] == 0, k
    a = D["group_A_closed_form_finite_bisection_inf"]
    assert a["n_o0_loses"] == 0 and a["n_live"] == 0


def test_group_B_is_a_tie_break_flip_never_a_strict_overtake():
    for k in ("group_B_bisection_finite_closed_form_inf", "both_finite_closed_form_later"):
        g = D[k]
        assert g["n_winner_inside_d51_band"] == g["n"] == g["n_winner_higher_fit"], k
        assert g["n_margins_equal_1e9"] == g["n"], k
        assert g["max_winner_lead_over_o0"] < D["d51_band"], k
        assert g["n_o0_regains"] == 0, k


def test_the_2748_and_its_all_stand():
    assert D["separating_count_bisection"] == 2748
    assert D["all_separating_inside_span_guard_bisection"] is True
    assert D["separating_that_enter_are_all_in_group_A"] is True


def test_bisection_identity_is_by_construction_and_the_closed_form_carries_the_violations():
    ident = D["identity_beta_c_finite_iff_o0_ne_oinf"]["all"]
    assert ident["bisection_violations"] == 0
    assert ident["closed_form_violations"] == D["n_disagreeing"]
