"""P2-D3 and P2-D4 are tripwires, not comments. Test that they fire.

Separate file from `tests/test_framings.py`, which is T3's and governs P2-D1 and
P2-D2. `dec.check_log` covers all four decisions and is already asserted there;
what is new here is the Arm B bind's negative case and the one number P2-D4
states, which is checkable against the frozen artifact rather than trusted.

Run: python3 tests/test_armb_binding.py
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, "src")

import adversary as adv  # noqa: E402
import p1  # noqa: E402
import p2_decisions as dec  # noqa: E402
import tie_reference as TR  # noqa: E402


def test_bind_armb_accepts_the_governed_values():
    """The decision as adopted: `size` tile, P1's frozen items, not pooled."""
    dec.bind_armb(dec.P2D3_TILE, p1.artifact_hash(p1.ITEMS_FINAL), pooled=False)


def test_bind_armb_rejects_drift():
    """Perturb each governed value in turn; the check must fail on every one.

    The pooled case is the one that matters most: P2-D3 rejected pooling on
    D108, and a later session that pools for the extra `n` is exactly the drift
    this bind exists to stop.
    """
    good_hash = p1.artifact_hash(p1.ITEMS_FINAL)
    drifted = [
        ("pooled", ("size", good_hash, True)),
        ("tile", ("manmade", good_hash, False)),
        ("tile", ("moves", good_hash, False)),
        ("tile", ("", good_hash, False)),
        ("item file", ("size", "0" * 64, False)),
        ("item file", ("size", good_hash[:-1] + "0", False)),
    ]
    for what, args in drifted:
        try:
            dec.bind_armb(*args)
        except AssertionError:
            continue
        raise AssertionError(f"bind_armb accepted a drifted {what}: {args}")


def test_confirmatory_n_matches_the_frozen_artifact():
    """P2-D4 states n = 108. Recompute it rather than trusting the number.

    A decision that names a count and a hash but never checks the count against
    the artifact the hash pins is half a binding: the hash would still match
    after a change to what `finite beta_c` means.
    """
    df = p1.load_items(tile=dec.P2D3_TILE)
    bc = adv.beta_critical_batch(adv.build_batch(df))
    n = int(np.isfinite(bc).sum())
    assert n == dec.P2D4_N_CONFIRMATORY, (
        f"P2-D4 states n = {dec.P2D4_N_CONFIRMATORY} `size`-tile items with "
        f"finite beta_c; the frozen artifact gives {n}. The log is the source: "
        "fix whichever drifted, do not edit the constant to pass.")
    assert len(df) == 250, len(df)


def test_sigma_ceiling_the_adopted_set_covers():
    """The limitation PREREGISTRATION_v2.3 section 3.3 states, recomputed.

    n = 15.05 * sigma^2 / delta^2 at delta = 0.05 gives n = 6020 * sigma^2, so
    108 items cover sigma <= 0.134 and section 8.2's 400 covers sigma <= 0.25.
    Asserted so the stated limitation cannot drift from the arithmetic behind it.
    """
    n_coef = (3.038 + 0.842) ** 2 / 0.05 ** 2
    assert abs(n_coef - 6020) < 20, n_coef
    assert abs((dec.P2D4_N_CONFIRMATORY / n_coef) ** 0.5 - 0.134) < 0.001
    assert abs((377 / n_coef) ** 0.5 - 0.250) < 0.001


def test_p2d6_rejects_a_mean_based_confirmatory_claim():
    """P2-D6 demotes mean `ΔA`. A run that puts a confirmatory claim on it must
    fail at the binding, not in the results table."""
    dec.bind_armb_statistic("sign", dec.P2D6_ALPHA, dec.P2D6_P0, False)
    dec.bind_armb_statistic("tie_rate", dec.P2D6_ALPHA, dec.P2D6_P0, False)
    for bad in ("mean", "mean_delta_A", "value_from_means"):
        try:
            dec.bind_armb_statistic(bad, dec.P2D6_ALPHA, dec.P2D6_P0, False)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"P2-D6 accepted {bad!r} as confirmatory")
    for kwargs in ((0.05, dec.P2D6_P0, False),          # alpha drift
                   (dec.P2D6_ALPHA, 0.6, False),        # sign-test null drift
                   (dec.P2D6_ALPHA, dec.P2D6_P0, True)):  # mean promoted back
        try:
            dec.bind_armb_statistic("sign", *kwargs)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"P2-D6 accepted drift {kwargs}")


def test_sign_power_is_sigma_free_and_matches_the_prereg():
    """P2-D6's power curve must not depend on `sigma`, and the figures quoted in
    PREREGISTRATION_v2.4 section 3.2 must come from the script that emits them."""
    import sign_power as sp
    assert sp.ALPHA == dec.P2D6_ALPHA, "sign_power alpha drifted from P2-D6"
    assert sp.N_CONFIRMATORY == dec.P2D4_N_CONFIRMATORY, "n drifted from P2-D4"
    # the three figures the preregistration quotes, recomputed here
    for n_eff, p1, want in ((108, 0.70, 0.858), (76, 0.70, 0.670), (54, 0.75, 0.740)):
        got = sp.power(n_eff, p1)
        assert abs(got - want) < 5e-4, f"power({n_eff}, {p1}) = {got:.4f}, prereg says {want}"
    assert sp.detectable(108) == 0.691, "detectable p1 at n=108 drifted"


def test_p2d8_reference_table_is_the_source_not_a_recomputation():
    """T7 must use the tabulated c5 reference. A recomputed table that disagrees
    fails at the binding rather than silently recalibrating the comparison."""
    dec.bind_armb_tie(dec.P2D8_C5_REFERENCE, dec.P2D8_BOOT_N,
                      dec.P2D8_BOOT_SEED, False)
    drifted = dict(dec.P2D8_C5_REFERENCE)
    drifted["L1"] = drifted["L1"] - 0.05
    for args in ((drifted, dec.P2D8_BOOT_N, dec.P2D8_BOOT_SEED, False),
                 ({k: v for k, v in list(dec.P2D8_C5_REFERENCE.items())[:3]},
                  dec.P2D8_BOOT_N, dec.P2D8_BOOT_SEED, False),
                 (dec.P2D8_C5_REFERENCE, 1000, dec.P2D8_BOOT_SEED, False),
                 (dec.P2D8_C5_REFERENCE, dec.P2D8_BOOT_N, 1, False),
                 (dec.P2D8_C5_REFERENCE, dec.P2D8_BOOT_N,
                  dec.P2D8_BOOT_SEED, True)):
        try:
            dec.bind_armb_tie(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"P2-D8 accepted drift: {args[1:]}")


def test_p2d8_reference_matches_what_the_script_emits():
    """The preregistered table must be what `src/tie_reference.py` computed, or
    the document and the artifact have drifted apart."""
    import json
    path = "results/T5_tie_reference.json"
    if not os.path.exists(path):
        raise AssertionError(f"{path} missing; run python3 src/tie_reference.py")
    rows = json.load(open(path))["references"]["size_tile_confirmatory"]
    for model, want in dec.P2D8_C5_REFERENCE.items():
        got = rows[model]["c5_same_option_rate"]
        assert abs(got - want) < 1e-9, (
            f"P2-D8 tabulates {want} for {model}; the script emits {got}")
    # the permutation rate must sit below c5 on every model, which is the
    # measured ground on which it was rejected as the primary reference
    for model, r in rows.items():
        assert r["c5_minus_permutation"] > 0, (
            f"{model}: permutation rate is not below c5, so P2-D8's stated "
            "reason for rejecting it as the primary reference no longer holds")


def test_p2d7_declines_the_enlargement():
    """P2-D7 closes variant (b). n stays at P2-D4's 108 and no enlargement is
    authorized, so the item hash is still the binding surface."""
    assert dec.P2D7_ENLARGEMENT_AUTHORIZED is False
    assert dec.P2D4_N_CONFIRMATORY == 108
    dec.bind_armb("size", dec.P2D4_ITEMS_SHA256, False)


def test_p2d10_rates_bind_and_reject_drift():
    """P2-D10 rules the same-option rate primary. A run that resolves H-B's
    no-movement half on the tie rate must fail at the binding.

    The tie rate is not wrong, it is the wrong half: it is an upper bound on the
    same-option rate, so calibrating it against a same-option reference biases
    the comparison toward "no movement" by exactly the blind spot.
    """
    dec.bind_armb_rates(dec.P2D10_PRIMARY_RATE, dec.P2D10_SIGN_TEST_DENOMINATOR,
                        dec.P2D9_C5_IS_ACTIVE)
    for args in (("tie", "non_tie", True),
                 ("tie_rate", "non_tie", True),
                 ("delta_A_zero", "non_tie", True),
                 ("same_option", "same_option", True),
                 ("same_option", "all", True),
                 ("same_option", "non_tie", False)):
        try:
            dec.bind_armb_rates(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"P2-D10/P2-D9 accepted drift: {args}")


def test_p2d10_nesting_is_the_reason_the_two_rates_differ():
    """Same option implies `ΔA = 0`, so same-option rate <= tie rate.

    P2-D10 rests on that inequality. Recomputed on the frozen geometry rather
    than quoted, because if `A` were injective the decision would be empty.
    """
    import json
    path = "results/T5_tie_reference.json"
    inv = json.load(open(path))["a_invisibility"]["size_tile_confirmatory"]
    assert inv["n_A_tied_option_pairs"] > 0, (
        "no A-tied option pairs, so the tie rate and the same-option rate cannot "
        "differ and P2-D10 is deciding nothing")
    assert inv["n_items_with_an_A_tied_option_pair"] == 48
    assert inv["n_items"] == dec.P2D4_N_CONFIRMATORY


def test_p2d19_a_tie_tolerance_and_the_gap_it_sits_in():
    """P2-D19's figures, and the empty interval the tolerance is defensible in.

    Three separate failures, kept separate because they mean different things.
    The exact-equality block must not move, or `v2.5` section 3 and `v2.6`
    section 2.2 stop reproducing. The EPS figures must match the decision, or a
    live document is citing a number the log does not carry. And the gap must
    still be empty: if a real gap ever lands near 1e-12 the tolerance has become
    a chosen threshold, which is a reason to revisit P2-D19, not to widen it.
    """
    import json
    d = json.load(open("results/T5_tie_reference.json"))
    exact = d["a_invisibility"]["size_tile_confirmatory"]
    assert exact["eps"] == 0.0
    assert (exact["n_A_tied_option_pairs"],
            exact["n_items_with_an_A_tied_option_pair"]) == (
        dec.P2D19_EXACT_EQUALITY_PAIRS, dec.P2D19_EXACT_EQUALITY_ITEMS)

    e = d["a_invisibility_at_p1_eps"]["size_tile_confirmatory"]
    dec.bind_a_tie_tolerance(e["eps"], e["n_items_with_an_A_tied_option_pair"],
                             e["n_A_tied_option_pairs"],
                             e["n_unordered_option_pairs"], e["next_gap_above_eps"])
    assert e["n_items"] == dec.P2D4_N_CONFIRMATORY
    assert e["next_gap_above_eps"] == pytest.approx(dec.P2D19_GAP[1])

    # PRIMARY base. The per-item share is the one that misleads, so it is checked
    # against its own base rather than quoted: 0.6759 is items containing ANY tied
    # pair among fifteen, and 0.0519 is the rate a reader hears when they are told
    # the first number.
    assert e["share_option_pairs_invisible_to_A"] == pytest.approx(0.0519, abs=5e-5)
    assert e["share_items_with_an_A_tied_option_pair"] == pytest.approx(0.6759, abs=5e-5)
    assert "PRIMARY" in e["share_option_pairs_invisible_to_A_is"]
    assert "inflated by option count" in e["share_items_with_an_A_tied_option_pair_is"]
    assert e["n_items_with_an_A_tied_option_pair"] > exact[
        "n_items_with_an_A_tied_option_pair"], (
        "a tolerance cannot untie a pair; if this fires, the two blocks were "
        "computed on different item sets")

    # The size-versus-pooled comparison the decision text makes, and the claim that
    # the confirmatory tile is the worst tile on BOTH bases.
    dv = d["a_invisibility_at_p1_eps"]["divergence_set"]
    assert (dv["n_A_tied_option_pairs"], dv["n_unordered_option_pairs"]) == (
        dec.P2D19_DIVERGENCE_PAIRS, dec.P2D19_DIVERGENCE_TOTAL_PAIRS)
    by_tile = d["a_invisibility_by_tile_at_p1_eps"]
    for base in ("share_option_pairs_invisible_to_A",
                 "share_items_with_an_A_tied_option_pair"):
        worst = max(by_tile, key=lambda t: by_tile[t][base])
        assert worst == "size", f"on {base} the worst tile is {worst}, not size"


def test_p2d20_quantity_c_unit_is_the_item_and_both_superseded_readings_hold():
    """P2-D20's `n_eff`, and the two readings it supersedes.

    The superseded columns are asserted because they are the check that the
    recomputation is of the same quantity: if the pair column stopped reproducing
    `v2.7` section 2.1, the item column would be a different measurement rather
    than a different unit of the same one.
    """
    import json
    d = json.load(open("results/T5_inertness_ceiling.json"))
    c5 = d["diagnostic_c5_direction"]["per_model"]
    for m, v in c5.items():
        assert v["n_eff_item"] == dec.P2D20_C5_N_EFF_ITEM[m]
        assert v["n_eff"] == dec.P2D20_C5_N_EFF_PAIR_EXACT[m]
        assert int(round(108 * (1 - v["tie_rate"]))) == dec.P2D20_C5_N_EFF_RESCALED[m]
        assert v["n_items_sign_disagreement"] == dec.P2D20_C5_SIGN_DISAGREEMENT[m]
        assert (v["n_items_sign_disagreement_cancelling"]
                == dec.P2D20_C5_SIGN_DISAGREEMENT_CANCELLING[m])
        # The item unit cannot exceed the item count, and cannot exceed the pair
        # count at the same tolerance: collapsing two votes into one only loses.
        assert v["n_eff_item"] <= v["n_items"] == dec.P2D4_N_CONFIRMATORY
        assert v["n_eff_item"] <= v["n_eff_pair_at_eps"]
        # A cancelling item is a sign-disagreeing item, by construction.
        assert (v["n_items_sign_disagreement_cancelling"]
                <= v["n_items_sign_disagreement"])

    dec.bind_quantity_c_unit(dec.P2D20_UNIT, dec.P2D20_SIGN_DISAGREEMENT,
                             True, True, dec.P2D19_EPS)
    for bad in (("rendering_pair", dec.P2D20_SIGN_DISAGREEMENT, True, True,
                 dec.P2D19_EPS),
                (dec.P2D20_UNIT, "permutation 0", True, True, dec.P2D19_EPS),
                (dec.P2D20_UNIT, dec.P2D20_SIGN_DISAGREEMENT, True, True, 0.0)):
        with pytest.raises(AssertionError):
            dec.bind_quantity_c_unit(*bad)


def test_p2d21_neutral_baseline_at_the_item_unit():
    """P2-D21's recomputed diagnostic, and the two sentences it withdraws.

    The withdrawn sentences are asserted as FALSE rather than deleted. A later
    run that re-derives either as true has either changed the unit back or
    changed the data, and both are things this should catch rather than absorb.
    """
    import json
    d = json.load(open("results/T5_inertness_ceiling.json"))
    c5 = d["diagnostic_c5_direction"]["per_model"]
    for m, v in c5.items():
        assert v["sign_proportion_item"] == pytest.approx(
            dec.P2D21_C5_SIGN_PROPORTION_ITEM[m])
        assert v["type_ii_gap_item"] == pytest.approx(dec.P2D21_TYPE_II_GAP_ITEM[m])
        # The gap is 0.5 minus the proportion, by definition. Asserted so a future
        # edit cannot quietly make it an absolute value and lose the sign.
        assert v["type_ii_gap_item"] == pytest.approx(
            0.5 - v["sign_proportion_item"])

    # Both withdrawn sentences, and the fact that they are withdrawn.
    props = {m: v["sign_proportion_item"] for m, v in c5.items()}
    six = {m: p for m, p in props.items() if m != "CTRL"}
    assert max(props.values()) > 0.5, "the all-seven claim came back true"
    assert max(six.values()) > 0.5, "P2-D15's six-ladder restatement came back true"
    assert dec.P2D21_ALL_SEVEN_CLAIM_HOLDS is False
    assert dec.P2D21_SIX_LADDER_CLAIM_HOLDS is False
    # It fails on a ladder model, not the control. That is what makes it case (b):
    # removing the control cannot rescue it.
    assert tuple(m for m, p in props.items() if p > 0.5) == dec.P2D21_NEUTRAL_ABOVE_P0
    assert "CTRL" not in dec.P2D21_NEUTRAL_ABOVE_P0

    # B2's 0.5556 is not evidence of upward drift. The whole ruling turns on this,
    # so it is recomputed from the counts rather than read from the artifact.
    from scipy.stats import binomtest
    b2 = c5["B2"]
    bt = binomtest(b2["n_positive_item"], b2["n_eff_item"], 0.5)
    lo, hi = bt.proportion_ci(confidence_level=0.95)
    assert lo < 0.5 < hi, "B2's interval no longer contains 0.5"
    assert bt.pvalue > dec.P2D6_ALPHA

    # Only CTRL resolves, and downward. This is what survives the wording.
    sig = tuple(m for m, v in c5.items() if v["significant_at_corrected_alpha_item"])
    assert sig == dec.P2D21_SIGNIFICANT_AT_CORRECTED_ALPHA == ("CTRL",)
    assert props["CTRL"] < 0.5, "the one resolving model no longer departs downward"

    # p0 did not move.
    assert dec.P2D21_P0 == dec.P2D6_P0 == 0.5 and dec.P2D21_P0_MOVED is False

    dec.bind_neutral_baseline(0.5, False, False, ("B2",),
                              dec.P2D21_TYPE_II_GAP_ITEM)
    with pytest.raises(AssertionError):
        dec.bind_neutral_baseline(0.5, True, False, ("B2",),
                                  dec.P2D21_TYPE_II_GAP_ITEM)
    with pytest.raises(AssertionError):
        dec.bind_neutral_baseline(0.5, False, False, (),
                                  dec.P2D21_TYPE_II_GAP_ITEM)
    with pytest.raises(AssertionError):
        # B2's gap reported as a positive Type II cost.
        flipped = dict(dec.P2D21_TYPE_II_GAP_ITEM, B2=0.0556)
        dec.bind_neutral_baseline(0.5, False, False, ("B2",), flipped)


def test_p2d21_pair_unit_figures_still_reproduce():
    """v2.7 section 2.1 and v2.8 sections 2.2 and 3.4 publish the pair unit.

    P2-D21 withdraws claims, not numbers. If a pair-unit figure moved, a
    superseded document stopped reproducing, which is a different and worse
    failure than the one P2-D21 records.
    """
    import json
    c5 = json.load(open("results/T5_inertness_ceiling.json"))[
        "diagnostic_c5_direction"]["per_model"]
    pair = {m: v["sign_proportion"] for m, v in c5.items()}
    assert max(pair.values()) <= 0.5, (
        "a pair-unit proportion rose above 0.5; v2.7 section 2.1 publishes them "
        "as at or below 0.5 and must still reproduce")
    for m, v in c5.items():
        assert 0.5 - pair[m] == pytest.approx(dec.P2D14_TYPE_II_GAP[m], abs=5e-5)
        assert v["n_eff"] == dec.P2D20_C5_N_EFF_PAIR_EXACT[m]


def test_p2d22_b2_sits_at_the_null_across_the_five_aggregations():
    """P2-D22's B2 reading, recomputed from frozen rows rather than quoted.

    The ruling is that B2 is AT the null, not that it is an unresolved
    exception, and that rests entirely on this table. The five aggregations were
    named before any was computed and all five are asserted, including the two
    that put B2 above 0.5, so the test cannot be satisfied by a subset that
    happens to agree.
    """
    import numpy as np, pandas as pd
    from scipy.stats import binomtest
    from tiebreak import EPS
    df, cols, A, ids, sets = TR.item_sets()
    ch = TR.load_choices()
    keep = set(int(i) for i in ids[sets["size_tile_confirmatory"]])
    g = ch[(ch["model"] == "B2") & (ch["prompt_form"] == TR.FORM)
           & (ch["rule"] == TR.RULE) & (ch["item_id"].isin(keep))
           & ch["permutation_id"].notna()]
    w = g.pivot_table(index=["item_id", "permutation_id"], columns="condition",
                      values="chosen_option", aggfunc="first")
    w = w.loc[w.notna().all(axis=1)]
    it = w.index.get_level_values("item_id").values.astype(int)
    d_ = np.array([A[i][int(b)] - A[i][int(a)]
                   for i, a, b in zip(it, w["cond4"].values, w["cond5"].values)])
    mean = pd.Series(d_).groupby(it).mean()
    sgn = pd.Series(np.where(np.abs(d_) > EPS, np.sign(d_), 0)).groupby(it).sum()
    got = {}
    for k, nz, v in (("A", d_ != 0, d_), ("B", np.abs(d_) > EPS, d_),
                     ("C", mean.abs() > EPS, mean), ("D", mean != 0, mean),
                     ("E", sgn != 0, sgn)):
        got[k] = (int(np.asarray(v)[np.asarray(nz)].__gt__(0).sum()), int(np.sum(nz)))
    assert got == dec.P2D22_B2_AGGREGATIONS, (
        f"B2's aggregation table moved: {got} against the recorded "
        f"{dec.P2D22_B2_AGGREGATIONS}. P2-D22's at-the-null ruling rests on it.")

    half = tuple(k for k, (p_, n) in got.items() if p_ * 2 == n)
    above = tuple(k for k, (p_, n) in got.items() if p_ * 2 > n)
    assert half == dec.P2D22_B2_EXACTLY_HALF_UNDER == ("A", "B", "E")
    assert above == dec.P2D22_B2_ABOVE_HALF_UNDER == ("C", "D")
    # Exactly 0.5 under an ITEM aggregation too, which is what makes this a
    # disagreement between aggregations and not between units.
    assert "E" in half and dec.P2D22_B2_AT_THE_NULL

    for k, (p_, n) in got.items():
        bt = binomtest(p_, n, 0.5)
        lo, hi = bt.proportion_ci(confidence_level=0.95)
        assert lo < 0.5 < hi, f"aggregation {k}: B2's interval no longer contains 0.5"
        assert bt.pvalue > dec.P2D6_ALPHA, f"aggregation {k}: B2 resolves against p0"

    # Two votes of 36 return the adopted aggregation to exactly 0.5.
    pC, nC = got["C"]
    assert pC - nC / 2 == 2.0


def test_p2d22_wording_binding_and_no_tally_frame_in_live_strings():
    """P2-D22 forbids the tally frame and "conservative" as p0's justification.

    The artifact strings are checked directly, because the binding records an
    intention and the emitted text is what a reader actually meets.
    """
    import json
    dec.bind_neutral_claim_wording(False, False, False)
    for bad in ((True, False, False), (False, True, False), (False, False, True)):
        with pytest.raises(AssertionError):
            dec.bind_neutral_claim_wording(*bad)
    assert dec.P2D22_TALLY_FRAME_PERMITTED is False
    assert dec.P2D22_CONSERVATIVE_JUSTIFIES_P0 is False

    live = [json.load(open("results/T5_inertness_ceiling.json"))
            ["diagnostic_c5_direction"]["answer_at_item_unit_p2d21"][k]
            for k in ("what_survives", "p0_is_retained_on")]
    af = json.load(open("results/T5_armb_floor.json"))
    live.append(af["type_ii_cost_of_p0_half_at_item_unit"]["statement"])
    live.append(af["d111_ruling"]["restated_at_item_unit_p2d21"]["replacement"])
    for text in live:
        assert "six of seven" not in text.lower(), f"tally frame in a live string: {text[:70]}"
        assert "survives on six models" not in text
        # "conservative" may appear only where it is being withdrawn.
        for i, w in enumerate(text.lower().split("conservativ")[1:]):
            ctx = text.lower().split("conservativ")[i] + "conservativ" + w[:60]
            assert ("withdraw" in ctx or "not on conservativ" in ctx
                    or "is a per-model property" in ctx
                    or "not conservative on b2" in ctx), \
                f"'conservative' used affirmatively in a live string: {ctx[-120:]}"


def test_p2d17_and_p2d18_are_withdrawn_and_carry_no_text():
    """A withdrawn entry has no decision text, so nothing can bind to it.

    `check_log` iterates over entries with text. This is the other half: the two
    retired numbers must stay textless, or a later session can quote one into a
    caller and the log will verify it.
    """
    assert dec.P2D17_WITHDRAWN and dec.P2D18_WITHDRAWN
    assert dec.P2D17_TEXT is None and dec.P2D18_TEXT is None
    log = open("docs/P2/DECISIONS.md").read()
    for n in ("P2-D17", "P2-D18"):
        assert f"## {n}. WITHDRAWN" in log, f"{n} has no tombstone in the log"


def test_p2d9_c5_is_active_against_a_deterministic_no_effect_rate():
    """P2-D9 says the reference moved choices. Check it against what the script
    emits, and against the no-effect rate the decision rests on."""
    import json
    path = "results/T5_c5_effect.json"
    if not os.path.exists(path):
        raise AssertionError(f"{path} missing; run python3 src/c5_effect.py")
    d = json.load(open(path))
    assert d["no_effect_same_option_rate"] == dec.P2D9_NO_EFFECT_SAME_OPTION_RATE
    rows = d["sets"]["size_tile_confirmatory"]
    assert len(rows) == len(dec.P2D8_C5_REFERENCE)
    for model, want in dec.P2D8_C5_REFERENCE.items():
        r = rows[model]
        assert abs(r["same_option_rate"] - want) < 1e-9, (
            f"{model}: c5_effect gives {r['same_option_rate']}, P2-D8 tabulates {want}")
        assert r["excludes_no_effect"], (
            f"{model}: the c5 change rate does not exclude the no-effect rate, so "
            "P2-D9's 'active comparator' no longer holds")
        assert r["ci_lo"] > 0.0
    lo, hi = dec.P2D9_C5_CHANGE_RATE_RANGE
    got = [r["change_rate"] for r in rows.values()]
    assert abs(min(got) - lo) < 1e-9 and abs(max(got) - hi) < 1e-9


def test_p2d11_ceiling_composes_and_binds():
    """P2-D11's bound must be a bound: `n_eff_max` below the unrestricted n, and
    sign power at it below sign power at n. If it did not bind, the decision
    would be stating a ceiling that is not there."""
    import json
    import sign_power as sp
    path = "results/T5_detection_ceiling.json"
    if not os.path.exists(path):
        raise AssertionError(f"{path} missing; run python3 src/detection_ceiling.py")
    d = json.load(open(path))
    assert d["limit_3_information"]["n_benchmark_v2_0_section_8_2"] == \
        dec.P2D11_N_BENCHMARK
    for model, r in d["per_model"].items():
        n_eff = r["n_eff_max_at_that_boundary"]
        assert 0 < n_eff < dec.P2D4_N_CONFIRMATORY, f"{model}: {n_eff} does not bind"
        assert r["framing_change_rate_needed"] > r["c5_change_rate"], (
            f"{model}: the movement half fires below the c5 change rate, so the "
            "first limit is not binding")
        assert sp.power(n_eff, 0.70) <= sp.power(dec.P2D4_N_CONFIRMATORY, 0.70)
        assert sp.power(n_eff, 0.5) <= sp.ALPHA + 1e-12
    for k, (a, b) in dec.P2D11_CEILING.items():
        got_lo, got_hi = d["ranges"][k]
        assert abs(got_lo - a) < 1e-9 and abs(got_hi - b) < 1e-9, (
            f"P2-D11 states {k} of {a} to {b}; the script emits {got_lo} to {got_hi}")


def test_p2d12_c5_must_not_gate():
    """P2-D12's whole content is that the reference comparison gates nothing. A
    run that resolves H-B's no-movement half on it is the superseded design."""
    dec.bind_armb_quantities(dec.P2D12_INERTNESS_NULL, False, dec.P2D6_P0,
                             dec.P2D12_QUANTITIES)
    for args in ((dec.P2D12_INERTNESS_NULL, True, dec.P2D6_P0, dec.P2D12_QUANTITIES),
                 (0.7037, False, dec.P2D6_P0, dec.P2D12_QUANTITIES),
                 (dec.P2D12_INERTNESS_NULL, False, 0.29, dec.P2D12_QUANTITIES),
                 (dec.P2D12_INERTNESS_NULL, False, dec.P2D6_P0,
                  ("inertness", "direction"))):
        try:
            dec.bind_armb_quantities(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"P2-D12 accepted drift: {args}")


def test_p2d12_floor_is_what_the_bootstrap_actually_accepts():
    """The floor is stated as 7 items. Recompute it against P2-D8's own bootstrap
    rather than trusting the analytic solution that produced it."""
    import inertness_ceiling as ic
    k = dec.P2D12_INERTNESS_FLOOR_ITEMS
    assert ic.inertness_floor() == k
    assert ic.check_floor(k)["clears_zero"], f"{k} movers do not clear zero"
    assert not ic.check_floor(k - 1)["clears_zero"], f"{k} is not the smallest"
    # a mover that changes one of its two renderings must count the same
    assert ic.check_floor(k, both_permutations=False)["clears_zero"]


def test_p2d12_buys_what_it_claims_and_not_what_it_does_not():
    """Two checks in opposite directions, because the obvious reading is wrong.

    It must lower the movement bar well below the superseded gate. It must NOT be
    claimed to raise sign-test power: at a c5-like tie rate the effective n is
    smaller than the gated ceiling's, because the gated ceiling was conditional on
    a large framing effect.
    """
    import json
    path = "results/T5_inertness_ceiling.json"
    if not os.path.exists(path):
        raise AssertionError(f"{path} missing; run python3 src/inertness_ceiling.py")
    d = json.load(open(path))
    gated_lo = dec.P2D11_CEILING["change_rate_multiple_of_c5"][0]
    worst = max(v["floor_as_multiple_of_c5"] for v in d["per_model"].values())
    assert worst < gated_lo, (
        f"inertness floor is {worst:.2f}x c5 at worst against the gate's "
        f"{gated_lo:.2f}x at best; P2-D12 lowers no bar")
    gated_n_lo = dec.P2D11_CEILING["n_eff_max"][0]
    n_eff = [v["n_eff_at_a_c5_like_tie_rate"] for v in d["per_model"].values()]
    assert min(n_eff) < gated_n_lo, (
        "a c5-like tie rate gives more effective n than the gated ceiling did, "
        "which would make P2-D12's 'not a power gain' note wrong")
    assert d["quantity_b_magnitude_context"]["role"].startswith("DESCRIPTIVE")


def test_p2d12_rejected_p0_swap_rests_on_a_measurement():
    """P2-D12 declined c5's own sign proportion as `p0` partly because it is at or
    below 0.5, making 0.5 conservative. If that ever stopped holding, the third
    rejected alternative would need revisiting rather than silently standing."""
    import json
    d = json.load(open("results/T5_inertness_ceiling.json"))
    props = [v["sign_proportion"]
             for v in d["diagnostic_c5_direction"]["per_model"].values()]
    assert max(props) <= 0.5 + 1e-12, (
        f"a c5 sign proportion is above 0.5 (max {max(props):.4f}); p0 = 0.5 is no "
        "longer conservative and P2-D12's alternative 3 needs revisiting")
    assert dec.P2D6_P0 == 0.5, "p0 drifted off P2-D6"


def test_p2d13_floor_is_upward_only_and_not_statistical():
    """The floor rule is a maximum, so a quiet environment cannot lower the bar.

    That property is what stops a low measured noise floor from being used to
    make the movement half easier to clear after F1 has been seen, so it is
    asserted rather than left to the docstring.
    """
    import armb_floor as af
    assert dec.P2D13_FLOOR_IS_STATISTICAL is False
    assert dec.P2D13_REVISION_IS_UPWARD_ONLY is True
    assert af.PROVISIONAL_FLOOR == dec.P2D13_PROVISIONAL_FLOOR
    for n in range(0, 120):
        f = af.floor_for_run(n)
        assert f >= dec.P2D13_PROVISIONAL_FLOOR, f"floor fell below at n={n}"
        assert f >= n, f"floor below the measured noise at n={n}"
    assert af.floor_for_run(0) == dec.P2D13_PROVISIONAL_FLOOR


def test_p2d13_bind_rejects_a_floor_that_ignores_the_measurement():
    """A run that keeps the provisional floor against a larger measured noise
    floor must fail at the binding, not report a movement verdict the
    environment could have produced on its own."""
    dec.bind_armb_floor(7, 0, False)
    dec.bind_armb_floor(20, 20, False)
    for args in ((7, 20, False),          # ignored a larger measured floor
                 (25, 20, False),         # invented headroom above the rule
                 (3, 0, False),           # below the provisional floor
                 (7, 0, True)):           # described as statistical
        try:
            dec.bind_armb_floor(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"P2-D13 accepted drift: {args}")
    try:
        dec.bind_armb_floor(7, -1, False)
    except (AssertionError, ValueError):
        pass
    else:
        raise AssertionError("P2-D13 accepted a negative disagreement count")


def test_p2d14_type_ii_gaps_are_nonnegative_and_match_the_emitter():
    """P2-D14 rests on the neutral baseline sitting at or below p0. If a gap ever
    went negative the Type II statement would reverse and p0 = 0.5 would be
    anti-conservative for that model."""
    import json
    path = "results/T5_armb_floor.json"
    if not os.path.exists(path):
        raise AssertionError(f"{path} missing; run python3 src/armb_floor.py")
    got = json.load(open(path))["type_ii_cost_of_p0_half"]["per_model"]
    assert dec.P2D6_P0 == 0.5
    for m, want in dec.P2D14_TYPE_II_GAP.items():
        assert abs(got[m]["gap_to_p0"] - want) < 1e-12, (
            f"P2-D14 states {want} for {m}; the emitter gives {got[m]['gap_to_p0']}")
        assert got[m]["gap_to_p0"] >= 0.0, (
            f"{m}: neutral baseline above p0; the Type II statement reverses")


def test_p2d15_conclusion_survives_the_control_being_excluded():
    """P2-D15 rules the control admissible, and the conclusion is reported both
    ways so it does not rest on the ruling. Check the fallback actually holds."""
    import json
    d = json.load(open("results/T5_armb_floor.json"))["d111_ruling"]
    assert d["admissible"] is dec.P2D15_SIGN_IS_ADMISSIBLE
    assert d["conclusion_holds_without_the_control"], (
        "the neutral-baseline conclusion needs the control, so P2-D15 is "
        "load-bearing and section 3.4's fallback is wrong")
    assert d["max_over_six"] <= 0.5 + 1e-12
    text = dec.P2D15_TEXT.lower()
    for banned in dec.P2D15_STILL_INADMISSIBLE:
        assert banned.lower() in text, (
            f"{banned!r} is bound as still-inadmissible but the decision text "
            "does not name it, so the ruling could be read as a relaxation")


def test_p2d16_bind_accepts_the_rule_and_rejects_every_departure():
    """P2-D16 is a tripwire on attrition handling. Test that it fires.

    The imputation case is the one that matters: counting a tied rendering as
    "same option" adds pairs to quantity (a)'s denominator that cannot reach its
    numerator, in the direction that confirms H-B's no-movement half.
    """
    good = dict(unit=dec.P2D16_EXCLUSION_UNIT, imputed_as_non_mover=False,
                dropped_whole_item=False,
                attrition_fields=dec.P2D16_ATTRITION_FIELDS)
    dec.bind_tie_exclusion(**good)
    drifted = [
        ("imputation", dict(good, imputed_as_non_mover=True)),
        ("whole-item exclusion", dict(good, dropped_whole_item=True)),
        ("item-level unit", dict(good, unit=("item_id",))),
        ("rendering-level unit",
         dict(good, unit=("item_id", "permutation_id", "framing"))),
        ("unreported attrition", dict(good, attrition_fields=())),
        ("a missing denominator",
         dict(good, attrition_fields=dec.P2D16_ATTRITION_FIELDS[:-1])),
    ]
    for what, kw in drifted:
        try:
            dec.bind_tie_exclusion(**kw)
        except AssertionError:
            continue
        raise AssertionError(f"bind_tie_exclusion accepted {what}: {kw}")


def test_p2d16_is_what_the_reference_path_already_does():
    """The decision's ground: the c5 reference was computed under this rule.

    Two things are checked, because the claim has two halves. P1's `n_tied == 1`
    filter keeps a tied rendering out of the choice frame at all, and the pivot
    shape in `c5_movement` and `c5_delta_A` then drops the (item, permutation)
    pair the tie left short a column while KEEPING the item's other permutation.
    If the second half failed, the rule would be whole-item exclusion wearing
    this decision's name.
    """
    import pandas as pd

    ch = TR.load_choices()
    assert (ch["n_tied"] == 1).all(), (
        "P2-D16 says a tied rendering never reaches a contrast, but "
        "tie_reference.load_choices returned one")

    # One item, two permutations; the cond5 rendering of permutation 0 is the
    # tie P1's filter has already removed, so its row is absent.
    g = pd.DataFrame({
        "item_id":        [7, 7, 7],
        "permutation_id": [0, 1, 1],
        "condition":      ["cond4", "cond4", "cond5"],
        "chosen_option":  [2, 2, 5],
    })
    w = g.pivot_table(index=["item_id", "permutation_id"], columns="condition",
                      values="chosen_option", aggfunc="first")
    w = w.loc[w.notna().all(axis=1)]
    assert len(w) == 1, f"the tied pair was not dropped: {w}"
    assert w.index.get_level_values("permutation_id").tolist() == [1], (
        "the surviving permutation is not the one that was kept")
    changed = (w["cond4"].values != w["cond5"].values).astype(float)
    per_item = pd.DataFrame({"i": w.index.get_level_values("item_id"),
                             "v": changed}).groupby("i")["v"].mean()
    assert per_item.loc[7] == 1.0, (
        "a half-observed item must contribute 0 or 1, not 0.5: the mean is over "
        "surviving pairs, not over the two renderings the item would have had")
    assert int((per_item > 0).sum()) == 1, (
        "the item is still in quantity (a)'s denominator and still counts as a "
        "mover; P2-D16 excludes the pair, never the item")


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"ok  {name}")
            except AssertionError as e:
                fails += 1
                print(f"FAIL {name}\n     {e}")
    sys.exit(1 if fails else 0)
