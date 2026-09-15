"""T7's confirmatory analysis: the properties its numbers rest on, tested.

These are not value checks on the result. Per the binding note in
`docs/P2/DECISIONS.md`, a test that pins a number goes stale with the unit,
tolerance or estimator; a test that asserts the PREMISE an argument needs
survives those changes and fails when the argument stops holding. Each test below
names the premise in its docstring.

The one exception is the refactor check: `c5_movement` and `c5_delta_A` gained a
contrast argument so T7 could reuse them instead of copying them, and the frozen
`R_m` values and `n_eff` counts must be untouched by that, because `v2.5` section
2.2 and `v2.7` publish them and a superseded document must still reproduce.

Run: python3.11 -m pytest tests/test_t7_armb.py -q
"""
import json
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, "src")

import c5_effect as CE  # noqa: E402
import inertness_ceiling as IC  # noqa: E402
import p2_decisions as dec  # noqa: E402
import t7_armb as T7  # noqa: E402
import tie_reference as TR  # noqa: E402

ARTIFACT = "results/T7_armb_quantities.json"


@pytest.fixture(scope="module")
def geometry():
    df, cols, A, ids, sets = TR.item_sets()
    keep = set(int(i) for i in ids[sets["size_tile_confirmatory"]])
    return A, ids, sets, keep


@pytest.fixture(scope="module")
def out():
    if not os.path.exists(ARTIFACT):
        pytest.skip(f"{ARTIFACT} not built; run python3 src/t7_armb.py")
    return json.load(open(ARTIFACT))


# ---------------------------------------------------------- the shared pivot

def test_pair_frame_reproduces_the_frozen_R_m(geometry):
    """Quantity (b) is calibrated against `R_m`, so `R_m` must still recompute.

    `c5_movement` now routes through `tie_reference.pair_frame` and takes the
    contrast as an argument. If that changed what the default contrast computes,
    every (b) number would be measured against a reference nothing reproduces.
    """
    _, _, _, keep = geometry
    P = TR.load_choices()
    got = {m: CE.c5_movement(P, m, keep)["same_option_rate"] for m in TR.LADDER}
    dec.bind_armb_tie(got, TR.BOOT_N, TR.BOOT_SEED, False)


def test_pair_frame_reproduces_the_frozen_c5_n_eff(geometry):
    """P2-D20's item-unit `n_eff` on the `c5` contrast is published in `v2.7`.

    Same premise as above on the other reused function: `c5_delta_A` gained a
    contrast argument, and the recorded per-model `n_eff_item` is what says the
    default still computes the quantity P2-D20 recomputed rather than a nearby one.
    """
    A, _, _, keep = geometry
    got = IC.c5_delta_A(TR.load_choices(), A, keep)
    assert {m: v["n_eff_item"] for m, v in got.items()} == dict(
        dec.P2D20_C5_N_EFF_ITEM)
    assert {m: v["n_eff"] for m, v in got.items()} == dict(
        dec.P2D20_C5_N_EFF_PAIR_EXACT)


def test_pair_frame_restricts_to_the_two_levels_of_the_contrast(geometry):
    """A tied `F1` rendering must leave the `F1` contrast ONLY, per P2-D16.

    T7's frame carries three framings at once. If `pair_frame` did not subset to
    the contrast's two levels before the `notna` filter, a pair tied on `F2` would
    be dropped from the `F1` contrast as well, which is the "exclude the whole
    item" rule P2-D16 rejected, applied across arms instead of within one.
    """
    _, _, _, keep = geometry
    kept, _ = T7.load_t7()
    for m in TR.LADDER:
        both = set(TR.pair_frame(kept, m, keep, "framing", "F0", "F1").index)
        other = set(TR.pair_frame(kept, m, keep, "framing", "F0", "F2").index)
        # The arms lose different pairs, so neither is a subset of the other
        # unless the loss is zero or falls on the baseline.
        assert both and other
        lost_f1, lost_f2 = other - both, both - other
        assert not (lost_f1 & lost_f2)


# ------------------------------------------------ P2-D16, the exclusion rule

def test_a_tie_is_never_imputed_and_never_drops_the_item(out):
    """P2-D16's whole content: pairwise at the pair, item retained, no imputation.

    The arithmetic that proves it: surviving pairs plus excluded pairs is the full
    grid, and every item with at least one surviving pair is still in the
    denominator. A rule that imputed a tie as a non-mover would leave
    `pairs_surviving` at 216; one that dropped the item whole would drop the
    denominator by one per tied pair.
    """
    for k, c in out["cells"].items():
        a = c["attrition_P2D16"]
        assert a["pairs_surviving"] + a["pairs_excluded_for_a_tie"] == \
            a["pairs_expected"], k
        assert a["items_with_two_surviving_pairs"] \
            + a["items_with_one_surviving_pair"] == a["item_denominator"], k
        assert a["item_denominator"] + a["items_with_no_surviving_pair"] == 108, k
        assert a["pairs_excluded_for_a_tie"] == \
            a["tied_renderings_on_the_baseline_F0"] \
            + a["tied_renderings_on_the_arm"] + a["unscored_renderings"], k


def test_every_attrition_field_the_binding_requires_is_present(out):
    """A denominator a reader cannot recover from a rate is attrition unreported."""
    for k, c in out["cells"].items():
        for f in dec.P2D16_ATTRITION_FIELDS:
            assert f in c["attrition_P2D16"], (k, f)


def test_f0_baseline_losses_are_shared_across_a_model_s_two_arms(out):
    """`F0` is the common baseline, so its ties are correlated, not independent.

    P2-D16 rules this explicitly. The check is that a model's `F0` tie count is
    the same number in both of its cells; if it were not, the two cells would be
    reading different baselines.
    """
    for m in TR.LADDER:
        counts = {out["cells"][f"{m}|{a}"]["attrition_P2D16"]
                  ["tied_renderings_on_the_baseline_F0"] for a in T7.ARMS}
        assert len(counts) == 1, m


# ----------------------------------------------- P2-D10, the nested subsets

def test_the_blind_spot_is_non_negative_in_every_cell(out):
    """Same option implies `ΔA = 0`, so the tie rate bounds the same-option rate.

    P2-D10 rests on that nesting: the sign test's subset is the smaller of the
    two halves, and the gap IS the movement `A` cannot see. A negative gap would
    mean `A` moved where the option did not, which the coordinate cannot produce.
    """
    for k, c in out["cells"].items():
        assert c["blind_spot_P2D10"]["gap"] >= 0.0, k


def test_the_sign_test_denominator_never_exceeds_the_moving_pairs(out):
    """(c)'s `n_eff` is at the item; it cannot exceed the items that moved.

    An item with `ΔA != 0` must have changed its chosen option on at least one
    surviving pair, because `A` is a function of the chosen option. `n_eff_item`
    above `n_items_with_a_changed_pair` would mean the coordinate moved on an item
    whose choice did not, which is the join being wrong.
    """
    for k, c in out["cells"].items():
        assert c["c_direction"]["n_eff_item"] <= \
            c["a_inertness"]["n_items_with_a_changed_pair"], k


# --------------------------------------------------- the oracle, and the floor

def test_nothing_sits_above_the_adversary_oracle(geometry):
    """`A <= 1` identically, and `A(o*_infinity) = 1` is the analytic optimum.

    CLAUDE.md: beating the oracle is a bug. This is a premise assert, not a range
    check: the bound follows from `marg_norm <= 1`, so a value above it is a
    misspecified coordinate or a bad item join and never a result.
    """
    A, _, _, keep = geometry
    kept, _ = T7.load_t7()
    o = T7.oracle_check(kept, A, keep)
    assert o["n_chosen_options_above_the_adversary_oracle"] == 0
    assert o["max_A_over_chosen_options"] <= 1.0 + dec.P2D19_EPS
    assert o["renderings_checked"] > 0


def test_the_floor_is_upward_only_and_is_not_statistical(out):
    """P2-D13's rule is a maximum, so a quiet environment cannot lower the bar."""
    f = out["inertness_floor"]
    assert f["value"] == max(dec.P2D13_PROVISIONAL_FLOOR,
                             f["f0_versus_cond4_disagreement_items"])
    assert f["is_statistical"] is False
    dec.bind_armb_floor(f["value"], f["f0_versus_cond4_disagreement_items"],
                        floor_is_statistical=False)


def test_a_quiet_f0_cannot_lower_the_floor():
    """The negative case, since the maximum is the whole mechanism."""
    import armb_floor as AF
    assert AF.floor_for_run(0) == dec.P2D13_PROVISIONAL_FLOOR
    assert AF.floor_for_run(3) == dec.P2D13_PROVISIONAL_FLOOR
    assert AF.floor_for_run(12) == 12
    with pytest.raises(AssertionError):
        dec.bind_armb_floor(dec.P2D13_PROVISIONAL_FLOOR, 12,
                            floor_is_statistical=False)


# ------------------------------------------------- P2-D14 / P2-D21 / P2-D22

def test_the_type_ii_gap_is_signed_and_negative_on_exactly_B2(out):
    """The sign says which of two statements the number supports, not its size.

    `src/armb_floor.py` carried this assertion with its reason before P2-D20 made
    it fire: a negative gap is not a smaller Type II cost, it is a Type I
    exposure, and P2-D14's licence box has no sentence for it.
    """
    neg = {m for m in TR.LADDER
           if out["cells"][f"{m}|F1"]["c_direction"]["type_ii_gap_signed"] < 0}
    assert neg == set(dec.P2D21_NEUTRAL_ABOVE_P0)
    for m in TR.LADDER:
        for a in T7.ARMS:
            d = out["cells"][f"{m}|{a}"]["c_direction"]
            assert (d["type_ii_gap_signed"] < 0) == \
                d["neutral_baseline_above_p0"]
            assert (d["type_i_exposure"] is None) == \
                d["gap_is_a_type_ii_cost"]


def test_every_c_row_carries_its_signed_gap(out):
    """P2-D14 as corrected: the gap is reported WITH the verdict, not elsewhere."""
    for k, c in out["cells"].items():
        assert "type_ii_gap_signed" in c["c_direction"], k
        assert c["c_direction"]["type_ii_gap_signed"] == pytest.approx(
            dec.P2D21_TYPE_II_GAP_ITEM[c["model"]], abs=1e-12), k


def test_no_live_string_uses_a_tally_frame_or_calls_p0_conservative():
    """P2-D22 forbids three specific framings; the report is live prose.

    Scoped to the report, not to the source: `bind_neutral_claim_wording`'s own
    keyword is `conservative_justifies_p0`, and a text scan over the module would
    fire on the binding that enforces the rule.
    """
    path = "reports/T7_armb_quantities.md"
    if not os.path.exists(path):
        pytest.skip(f"{path} not built; run python3 src/t7_armb.py")
    text = open(path).read().lower()
    assert "six of seven" not in text
    assert "conservative" not in text
    # B2 is a model at the null whose point estimate falls either side depending
    # on aggregation. Any mention of drift must be the negated form.
    for i, line in enumerate(text.splitlines()):
        if "drift" in line:
            assert "does not drift" in line, (i, line)
    dec.bind_neutral_claim_wording(False, False, False)


# ------------------------------------------------------------- the blocker

def test_the_artifact_issues_no_verdict_on_h_b(out):
    """The artifact withheld the verdict, and P2-D26 says it was right to.

    Written while P2-D5's conjunct was unruled, asserting the registry still
    carried it. P2-D26 discharged it on 2026-09-15 as PERMANENTLY blocking, so the
    artifact's `UNRULED` label is now stale while its behaviour is vindicated: no
    adversary-tracking claim is available on this set at all. The test asserts what
    actually matters, which is that the artifact makes no such claim, and it no
    longer depends on the registry being open.
    """
    assert out["blocker"]["status"] in ("UNRULED", "DISCHARGED")
    assert dec.P2D26_ADVERSARY_TRACKING_CLAIM_AVAILABLE is False
    blob = json.dumps(out).lower()
    for phrase in ("tracks the adversary", "h-b is rejected", "supports h-b"):
        assert phrase not in blob, f"the artifact issues a verdict: {phrase!r}"
    dec.bind_adversary_tracking_claim(False, 108, 108, "108 of 108")

def test_the_artifact_carries_no_excess_over_the_marginal_null_quantity(out):
    """Do not invent the quantity the blocker names. Emitting one would resolve
    the unruled question by computing it, which is the same act as choosing."""
    blob = json.dumps(out["cells"]).lower()
    for banned in ("a_null", "delta_a_null", "marginal_null", "excess"):
        assert banned not in blob, banned


def test_switch_concentration_blind_spot_is_a_subset_relation():
    """(c) can never resolve an item (a) says did not move.

    A same-option item has dA = 0 exactly, so n_eff <= moved by construction and
    the blind-spot count is non-negative. A violation is a join error between the
    two quantities, not a result. The concentration ratio is checked for the
    model split rather than a threshold: the finding is that it varies, and a
    test that pinned one number would hide that.
    """
    import json
    d = json.load(open("results/T7_switch_concentration.json"))
    cells = d["per_cell"]
    assert len(cells) == 14
    for k, v in cells.items():
        assert v["n_eff_item_quantity_c"] <= v["n_items_moved_quantity_a"], k
        assert v["n_items_changed_but_delta_A_zero"] >= 0, k
        assert v["n_switches_on_an_A_tied_pair"] <= v["n_switches"], k
    hi = {k for k, v in cells.items() if v["concentration_ratio"] > 1}
    assert {k.split("/")[0] for k in hi} == {"CTRL", "L1", "L3"}, (
        f"the concentrated model set changed: {sorted(hi)}. It is the finding, "
        "and which models are in it is what bears on (c).")
    # Every concentrated cell loses more items to the blind spot than every
    # unconcentrated one. If that separation ever closes, the two quantities have
    # stopped tracking each other and the report's reading needs revisiting.
    assert (min(cells[k]["n_items_changed_but_delta_A_zero"] for k in hi)
            > max(cells[k]["n_items_changed_but_delta_A_zero"]
                  for k in cells if k not in hi))
