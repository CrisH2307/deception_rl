"""P2-D25 is a ruling made before either quantity existed, so its tests are premises.

No value of `A_null`, `dA_null` or control-set `TV` appears here, and none could,
because the session that wrote the ruling computed none of them. What is tested is
the shape of the ruling and the one empirical claim it rests on: that canonical
option ids are not menu positions. That claim is checked against Paper 1's frozen
rendering table rather than trusted, because it is the claim that overturned the
reading `reports/T7_switch_concentration.md` first recorded.

Run: python3.11 -m pytest tests/test_p2d25_marginal_null.py -q
"""
import os
import sys

import pytest

sys.path.insert(0, "src")

import p2_decisions as dec  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")

OK = dict(in_confirmatory_family=False, confirmatory_family_size=21,
          alpha=dec.P2D6_ALPHA, mapping_to_quantity_c=None, successor_cap=None,
          control_arity=6, confirmatory_arity=6,
          hypothesis_support="canonical_option_id", ext_floor_applied=True)


def test_check_log_covers_p2d25():
    """The decision text and every rejected alternative are in the log verbatim."""
    assert dec.check_log(os.path.join(ROOT, "docs/P2/DECISIONS.md"))
    assert len(dec.P2D25_REJECTED) == 4


def test_a_conforming_run_passes():
    assert dec.bind_marginal_null_use(**OK) is None


@pytest.mark.parametrize("field,bad", [
    # Neither quantity is a test, so a caller that makes one a test fails.
    ("in_confirmatory_family", True),
    # Admitting one would move alpha for 21 already-published tests.
    ("confirmatory_family_size", 22),
    ("alpha", 0.05 / 23),
    # A level in A units has no preregistered bridge to a sign proportion.
    ("mapping_to_quantity_c", "excess > 0 implies sign proportion > 0.5"),
    # The cap's object still exists at descriptive standing; a successor is new.
    ("successor_cap", "median dA_null"),
    # The reweighting sums over one option index; the supports must match.
    ("control_arity", 3),
    # A canonical-id marginal cannot express a menu-position preference.
    ("hypothesis_support", "rendered_menu_position"),
    # P2-D23 leaves the ext_i floor in force on every mean or median of per-item A.
    ("ext_floor_applied", False),
])
def test_each_premise_fires(field, bad):
    kw = dict(OK, **{field: bad})
    with pytest.raises(AssertionError):
        dec.bind_marginal_null_use(**kw)


def test_the_constants_say_what_the_ruling_says():
    assert dec.P2D25_IN_CONFIRMATORY_FAMILY is False
    assert dec.P2D25_CONFIRMATORY_FAMILY_SIZE == 21
    assert dec.P2D25_MAPPING_TO_QUANTITY_C is None
    assert dec.P2D25_SUCCESSOR_CAP_AUTHORIZED is False
    assert dec.P2D25_CONTROL_TV_AUTHORIZED is True
    assert dec.P2D25_MENU_POSITION_ADJUDICABLE is False
    assert dec.P2D25_MARGINAL_SUPPORT == "canonical_option_id"
    assert dec.P2D25_EXT_FLOOR_IN_FORCE is True
    # P2-D25 does not move p0, change the family, or reopen P2-D24.
    assert dec.P2D21_P0 == 0.5 and dec.P2D6_P0 == 0.5
    assert abs(dec.P2D6_ALPHA - 0.05 / 21) < 1e-15
    assert dec.P2D24_DIRECTION_CLAIM_LICENSED is False


def test_the_undefended_entry_is_not_cleared():
    """P2-D25 answered the cap half. P2-D5's conjunct is the author's and is open.

    Clearing `ruled_by` would silence `undefended()`, and the hypothesis IS still
    undefended in the confirmatory family. The louder half of the audit has to keep
    saying so, which is the whole point of the field.
    """
    open_scopes = dec.scope_audit()
    und = dec.undefended()
    assert len(und) == 1, und
    entry = und[0]
    assert entry["ruled_by"] is None
    assert "P2-D25" in entry["partly_ruled_by"]
    assert "P2-D5" in entry["partly_ruled_by"]
    assert entry in open_scopes


def test_canonical_option_ids_are_not_menu_positions():
    """The empirical premise of question 3, recomputed from P1's frozen renderings.

    `chosen_option` is a canonical option id and `option_order` is the rendered
    menu. If canonical 4 and 5 sat at the end of the menu, a generic menu-position
    shift WOULD produce the (4,5) signature and P2-D25's ruling on question 3 would
    be wrong. They do not: both fall in every menu position at rates no more than
    twice the uniform 1/6. This is the assert that fails if a later rendering change
    makes the position reading true after all.
    """
    pd = pytest.importorskip("pandas")
    import p1  # noqa: E402
    path = os.path.join(p1.P1_ROOT, "data/processed/items_rendered.parquet")
    if not os.path.exists(path):
        pytest.skip(f"{path} not present")
    V = pd.read_parquet(path)
    V = V[(V["format"] == "V") & (V["variant"] == "base")
          & (V["tile"] == dec.P2D25_CONTROL_TILE)]
    assert len(V) > 0
    k = dec.P2D25_CONFIRMATORY_ARITY
    for canonical in dec.P2D25_CANONICAL_TAIL_IDS:
        for pid, g in V.groupby("permutation_id"):
            pos = [list(o).index(canonical) for o in g["option_order"]]
            assert set(pos) == set(range(k)), (canonical, pid, sorted(set(pos)))
            share = [pos.count(j) / len(pos) for j in range(k)]
            assert max(share) < 2.0 / k, (canonical, pid, share)
