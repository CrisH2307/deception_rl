"""P2-D27 is a ruling made before the control change rate existed, so its tests are premises.

No value of the control change rate appears here, and none could: the session that
wrote the ruling did not compute it. What is tested is the shape of the ruling and the
facts it rests on, each checked against the record or frozen model-free geometry
rather than trusted: that P2-D25's text is silent on a change rate, that the control
base is the 142 adversary-robust `size` items and disjoint from the confirmatory set,
and that (a)'s instrument reads chosen options and nothing else.

The tests after the divider read the rate computed later under the ruling
(`PREREGISTRATION_v2.20.md`). They pin no value either: they check that the artifact
reproduces from its script, carries exactly the ruled fields, and respects the TV
bound P2-D27 disclosed.

Run: python3.11 -m pytest tests/test_p2d27_control_change_rate.py -q
"""
import json
import os
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, "src")

import c5_effect as CE  # noqa: E402
import p2_decisions as dec  # noqa: E402
import tie_reference as TR  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")

OK = dict(instrument=CE.c5_movement, contrast=("framing", "F0"), arms=("F1", "F2"),
          control_beta_c=[float("inf")] * 142, control_tiles=["size"] * 142,
          reads_A=False, in_confirmatory_family=False, alpha=dec.P2D6_ALPHA,
          emitted_fields=dec.P2D27_FIELDS, derived_quantities=(), floor_applied=False)


def test_check_log_covers_p2d27():
    """The decision text and every rejected alternative are in the log verbatim."""
    assert dec.check_log(os.path.join(ROOT, "docs/P2/DECISIONS.md"))
    assert len(dec.P2D27_REJECTED) == 5


def test_a_conforming_run_passes():
    assert dec.bind_control_change_rate(**OK) is None


def _other_instrument(*a, **k):
    return None


@pytest.mark.parametrize("field,bad", [
    # Not (a)'s instrument: the side-by-side would compare two instruments.
    ("instrument", _other_instrument),
    # (a) has no F2-versus-F1 cell and no other base.
    ("contrast", ("framing", "F1")),
    ("arms", ("F1", "F2", "F3")),
    # One finite beta_c item is an item where the adversary does move the optimum.
    ("control_beta_c", [float("inf")] * 141 + [2.0]),
    # The 540-item base mixes arities; P2-D27 declines it.
    ("control_beta_c", [float("inf")] * 540),
    ("control_tiles", ["size"] * 141 + ["moves"]),
    # A is undefined on the control set.
    ("reads_A", True),
    ("in_confirmatory_family", True),
    ("alpha", 0.05),
    # A verdict flag, a floor, or a second TV is outside the ruling.
    ("emitted_fields", dec.P2D27_FIELDS + ("clears_the_floor",)),
    ("emitted_fields", dec.P2D27_FIELDS + ("interval_excludes_zero",)),
    ("emitted_fields", dec.P2D27_FIELDS + ("tv_option_marginal",)),
    # The item count must sit beside the rate, as it does for (a).
    ("emitted_fields", tuple(f for f in dec.P2D27_FIELDS
                             if f != "n_items_with_a_changed_pair")),
    # Side by side and nothing beyond.
    ("derived_quantities", ("difference_a_minus_control",)),
    ("derived_quantities", ("attributable_share",)),
    ("floor_applied", True),
])
def test_each_premise_fires(field, bad):
    kw = dict(OK, **{field: bad})
    with pytest.raises(AssertionError):
        dec.bind_control_change_rate(**kw)


def test_p2d25_is_silent_on_a_change_rate():
    """The ruling's first ground: P2-D25 neither declined nor authorized one.

    If a later edit made P2-D25 address a control change rate, P2-D27's reading of
    it as silence would be stale and must be re-read.
    """
    text = (dec.P2D25_TEXT + " ".join(dec.P2D25_REJECTED)).lower()
    assert "change rate" not in text and "same-option" not in text
    assert dec.P2D27_P2D25_ADDRESSED is False


def test_the_artifact_records_non_authorization_not_a_ruling():
    """`steps_not_run` records the computing session's reading of silence."""
    d = json.load(open(os.path.join(ROOT, "results/T7_control_marginal_null.json")))
    note = d["steps_not_run"]["step_4_control_change_rate"]
    assert note.startswith("NOT COMPUTED") and "does not authorize" in note


def test_the_control_base_is_the_142_and_disjoint_from_the_confirmatory_set():
    """Frozen, model-free geometry only. No model choice is read."""
    df, cols, A, ids, sets = TR.item_sets()
    tiles = df["tile"].values
    ctrl = ~np.isfinite(cols["beta_c"]) & (tiles == dec.P2D27_CONTROL_TILE)
    conf = sets["size_tile_confirmatory"]
    assert int(ctrl.sum()) == dec.P2D27_CONTROL_N
    assert not (ctrl & conf).any()
    dec.bind_control_change_rate(**dict(
        OK, control_beta_c=cols["beta_c"][ctrl], control_tiles=tiles[ctrl]))


def test_the_instrument_reads_chosen_options_only():
    """`c5_movement` runs on a frame with no geometry in it, so it cannot read `A`.

    Synthetic rows: two items, two permutations, one changed pair. The rate the
    instrument returns is fixed by the choices alone.
    """
    rows = []
    for item in (1, 2):
        for perm in (0, 1):
            for framing, opt in (("F0", 0), ("F1", 3 if (item, perm) == (2, 1) else 0)):
                rows.append({"model": "M", "prompt_form": TR.FORM, "rule": TR.RULE,
                             "item_id": item, "permutation_id": perm,
                             "framing": framing, "chosen_option": opt})
    out = CE.c5_movement(pd.DataFrame(rows), "M", {1, 2}, "framing", "F0", "F1")
    assert out["n_pairs"] == 4 and out["n_changed"] == 1
    assert out["n_items_with_a_changed_pair"] == 1
    assert abs(out["change_rate_item_mean"] - 0.25) < 1e-12


# ------------------------------------------ the computed rate, under P2-D27 (v2.20)
RATE = os.path.join(ROOT, "results/T7_control_change_rate.json")
RECORD = os.path.join(ROOT, "results/T7_control_marginal_null.json")


@pytest.fixture(scope="module")
def rate():
    if not os.path.exists(RATE):
        pytest.skip("run python3 src/t7_control.py --change-rate")
    return json.load(open(RATE))


def test_the_artifact_reproduces_from_its_script(rate):
    """Every emitted number is script-emitted: a rerun gives the committed artifact."""
    import t7_control as TC
    assert json.loads(json.dumps(TC.change_rate())) == rate


def test_each_cell_emits_exactly_the_ruled_fields_and_no_verdict(rate):
    assert set(rate["cells"]) == {f"{m}|{a}" for a in dec.P2D27_ARMS
                                  for m in TR.LADDER}
    for cell, c in rate["cells"].items():
        assert set(c["control_change_rate"]) == set(dec.P2D27_FIELDS), cell
        assert set(c["attrition_P2D16"]) >= set(dec.P2D16_ATTRITION_FIELDS), cell
        assert (c["attrition_P2D16"]["item_denominator"]
                == c["control_change_rate"]["item_denominator"]), cell
    text = json.dumps(rate["cells"])
    for banned in ("interval_excludes_zero", "excludes_no_effect", "clears_the_floor",
                   "tv_option_marginal", '"null"', "difference", "ratio", "share"):
        assert banned not in text, banned
    assert rate["control_base"]["n_items"] == dec.P2D27_CONTROL_N
    assert rate["in_confirmatory_family"] is False


def test_premise_needs_identical_renderings_not_just_a_pair_count():
    import t7_control as TC
    assert TC.tv_bound_premise({"n_renderings_base": 284, "n_renderings_arm": 284}, 284)
    assert not TC.tv_bound_premise({"n_renderings_base": 284, "n_renderings_arm": 283},
                                   283)


def test_tv_of_record_never_exceeds_the_rate_on_identical_renderings(rate):
    """P2-D27's disclosed bound: each changed pair moves at most one unit of mass.

    Re-derived here from both artifacts rather than trusted from the emitted list.
    """
    import t7_control as TC
    rec = json.load(open(RECORD))["cells"]
    holds = []
    for cell, c in rate["cells"].items():
        r, tv = c["control_change_rate"], rec[cell]["control_TV"]
        if TC.tv_bound_premise(tv, r["n_pairs"]):
            holds.append(cell)
            assert tv["value"] <= r["change_rate_renderings"] + 1e-12, cell
    assert holds == rate["tv_bound_check"]["premise_holds_on"]
