"""P2-D24 is a ruling about what may be said, so its tripwires are premises.

The ruling is that quantity (c)'s five resolving cells license no claim about
direction, because three premises a direction claim would need do not hold. A test
that only checked `p` values would pass while the ruling silently stopped applying,
which is the expired-scope failure `docs/P2/DECISIONS.md` case 4 describes. So each
test here checks a premise against the artifact that establishes it, and the bind
tests check that the binding fires when a premise becomes established.

Run: python3.11 -m pytest tests/test_p2d24_direction.py -q
"""
import json
import os
import sys

import pytest

sys.path.insert(0, "src")

import p2_decisions as dec  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
ARMB = os.path.join(ROOT, "results/T7_armb_quantities.json")
SWITCH = os.path.join(ROOT, "results/T7_switch_concentration.json")
CEILING = os.path.join(ROOT, "results/T5_inertness_ceiling.json")
REPORT = os.path.join(ROOT, "reports/T7_armb_quantities.md")


def _load(path):
    if not os.path.exists(path):
        pytest.skip(f"{path} not present")
    return json.load(open(path))


def test_check_log_covers_p2d24():
    """The decision text and every rejected alternative are in the log verbatim."""
    assert dec.check_log(os.path.join(ROOT, "docs/P2/DECISIONS.md"))
    assert len(dec.P2D24_REJECTED) == 3


def test_the_five_resolving_cells_reproduce():
    """A cell entering or leaving the resolving set changes what the ruling covers."""
    d = _load(ARMB)
    got = tuple(k for k, v in d["cells"].items()
                if v["c_direction"]["significant_at_corrected_alpha_item"])
    assert got == dec.P2D24_RESOLVING_CELLS, (
        f"the resolving set is {got}; P2-D24 rules on "
        f"{dec.P2D24_RESOLVING_CELLS}. The ruling is re-read, not extended.")


def test_every_resolving_departure_is_downward():
    """The ruling is about downward departures. An upward one is a different case.

    P2-D24 rejects reading any of them as direction, but the reasons are stated on
    departures below `p0`: the neutral insert departs downward and the discarded
    switches are the ones a downward reading would rest on. An upward resolving
    cell would need its own reading rather than inheriting this one.
    """
    d = _load(ARMB)
    props = {k: d["cells"][k]["c_direction"]["sign_proportion_item"]
             for k in dec.P2D24_RESOLVING_CELLS}
    assert all(p < 0.5 for p in props.values()) is dec.P2D24_RESOLVING_ALL_DOWNWARD, (
        f"resolving proportions {props}; P2-D24 rules on departures below p0.")


def test_premise_2_the_neutral_diagnostic_resolves_on_ctrl_alone():
    """Reading a departure against the neutral figure needs one that resolves.

    This is the premise the author instruction got wrong: it named `L3` as
    resolving, and `L3`'s two-sided `p` at the item unit is 0.004551 against
    `alpha` = 0.002381.
    """
    d = _load(CEILING)
    per = d["diagnostic_c5_direction"]["per_model"]
    got = tuple(m for m in ("CTRL", "B2", "B4", "L1", "L2", "L3", "L4")
                if per[m]["significant_at_corrected_alpha_item"])
    assert got == dec.P2D24_NEUTRAL_RESOLVES_ON, (
        f"the neutral diagnostic resolves on {got}; P2-D24 rests on "
        f"{dec.P2D24_NEUTRAL_RESOLVES_ON}. If a second model resolves, the "
        "reading P2-D24 rejected may now be available.")
    assert per["L3"]["p_two_sided_item"] > d["alpha"]


def test_premise_3_the_concentrated_resolving_cells():
    """Which resolving cells run on a subset the coordinate selected, and how hard."""
    s = _load(SWITCH)
    conc = tuple(c.replace("/", "|") for c, v in s["per_cell"].items()
                 if v["concentration_ratio"] > 1.0)
    got = tuple(c for c in dec.P2D24_RESOLVING_CELLS if c in conc)
    assert got == dec.P2D24_CONCENTRATED_RESOLVING_CELLS, (
        f"concentrated resolving cells are {got}; P2-D24 records "
        f"{dec.P2D24_CONCENTRATED_RESOLVING_CELLS}.")
    ratios = [s["per_cell"][c.replace("|", "/")]["concentration_ratio"] for c in got]
    lo, hi = dec.P2D24_CONCENTRATION_RATIO_RESOLVING
    assert (round(min(ratios), 2), round(max(ratios), 2)) == (lo, hi)


def test_the_binding_passes_on_the_run_as_it_stands():
    d = _load(CEILING)
    per = d["diagnostic_c5_direction"]["per_model"]
    resolves = tuple(m for m in ("CTRL", "B2", "B4", "L1", "L2", "L3", "L4")
                     if per[m]["significant_at_corrected_alpha_item"])
    dec.bind_direction_claim(False, resolves, (), False)


@pytest.mark.parametrize("kwargs,needle", [
    (dict(direction_claim_made=True), "direction claim"),
    (dict(excess_over_marginal_null_quantities=("excess dA",)), "premise 1"),
    (dict(neutral_resolves_on=("CTRL", "L3")), "premise 2"),
    (dict(discarded_switch_direction_established=True), "premise 3"),
])
def test_the_binding_fires_when_a_premise_moves(kwargs, needle):
    """Each premise, not each number. A drifted proportion does not fire these."""
    args = dict(direction_claim_made=False,
                neutral_resolves_on=dec.P2D24_NEUTRAL_RESOLVES_ON,
                excess_over_marginal_null_quantities=(),
                discarded_switch_direction_established=False)
    args.update(kwargs)
    with pytest.raises(AssertionError) as e:
        dec.bind_direction_claim(**args)
    assert needle in str(e.value)


def test_the_marginal_null_is_computed_and_premise_1_is_untouched():
    """The trigger fired and was answered by a factual correction, not a ruling.

    P2-D24 said the marginal null had never been computed. `src/t7_control.py`
    computed both under P2-D25, which is the preregistered outcome P2-D24 itself
    predicted, so the fact changed and the premise did not. What must NOT change
    is premise 1's substance: no confirmatory quantity is an excess over the
    marginal null, and none may be mapped onto (c).
    """
    assert dec.P2D24_MARGINAL_NULL_COMPUTED is True
    assert dec.P2D24_MARGINAL_NULL_COMPUTED_BY
    assert dec.P2D25_MAPPING_TO_QUANTITY_C is None
    assert dec.P2D25_IN_CONFIRMATORY_FAMILY is False
    d = _load(ARMB)
    blob = json.dumps(d["cells"])
    assert "A_null" not in blob, (
        "an A_null quantity has entered the confirmatory cells. P2-D24 rules "
        "that computing it is preregistered but that using it to license a "
        "direction claim on (c) would be post-hoc. Re-read the entry.")


def test_the_live_report_states_the_ruling_and_makes_no_direction_claim():
    if not os.path.exists(REPORT):
        pytest.skip("report not present")
    text = open(REPORT).read()
    assert "P2-D24" in text and "no claim is licensed" in text
    d = _load(ARMB)
    assert d["direction_reading_P2D24"]["direction_claim_licensed"] is False
    for banned in ("runs away from the adversary-aware optimum",
                   "move choices substantially"):
        assert banned not in text, (
            f"the live report says {banned!r}, which P2-D24 does not license.")
