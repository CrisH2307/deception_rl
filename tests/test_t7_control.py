"""T7 step 4 and the authorized part of step 5: the premises the numbers rest on.

Per the binding note in `docs/P2/DECISIONS.md`, a test that pins a number goes
stale with the unit, tolerance or estimator; a test that asserts the PREMISE an
argument needs survives those and fails when the argument stops holding. Each test
below names its premise.

The exception is the refactor check: `inertness_ceiling.c5_delta_A` now routes
through `pair_delta_A`, and the frozen `n_eff` counts `v2.7` publishes must be
untouched by that.

Run: python3.11 -m pytest tests/test_t7_control.py -q
"""
import json
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, "src")

import c5_effect as CE          # noqa: E402
import inertness_ceiling as IC  # noqa: E402
import p2_decisions as dec      # noqa: E402
import t7_armb as T7            # noqa: E402
import t7_control as TC         # noqa: E402
import tie_reference as TR      # noqa: E402

ARTIFACT = "results/T7_control_marginal_null.json"


@pytest.fixture(scope="module")
def G():
    return TC.geometry()


@pytest.fixture(scope="module")
def out():
    if not os.path.exists(ARTIFACT):
        pytest.skip(f"{ARTIFACT} not built; run python3 src/t7_control.py")
    return json.load(open(ARTIFACT))


@pytest.fixture(scope="module")
def kept():
    return T7.load_t7()[0]


# ------------------------------------------------- P2-D25, the ruling's premises

def test_the_binding_the_run_must_call_passes_on_this_run():
    """The six premises P2-D25 makes a use of these quantities well formed on.

    This is the call `src/t7_control.py` makes before emitting anything. If it
    raises, the run is using a quantity outside what the ruling authorizes.
    """
    dec.bind_marginal_null_use(
        in_confirmatory_family=False, confirmatory_family_size=21,
        alpha=dec.P2D6_ALPHA, mapping_to_quantity_c=None, successor_cap=None,
        control_arity=6, confirmatory_arity=6,
        hypothesis_support="canonical_option_id", ext_floor_applied=True)


@pytest.mark.parametrize("kw", [
    {"in_confirmatory_family": True},
    {"confirmatory_family_size": 22},
    {"alpha": 0.05},
    {"mapping_to_quantity_c": "excess -> sign proportion"},
    {"successor_cap": "reweighted sign cap"},
    {"control_arity": 3},
    {"hypothesis_support": "menu_position"},
    {"ext_floor_applied": False},
])
def test_crossing_any_premise_fails(kw):
    """Each of P2-D25's premises is load-bearing, so each must fail on its own.

    A binding that passes when a premise is crossed is decoration. `control_arity`
    of 3 is the pooling P2-D3 rejected; `menu_position` is the hypothesis P2-D25
    rules unadjudicable by any preregistered quantity.
    """
    args = dict(in_confirmatory_family=False, confirmatory_family_size=21,
                alpha=dec.P2D6_ALPHA, mapping_to_quantity_c=None,
                successor_cap=None, control_arity=6, confirmatory_arity=6,
                hypothesis_support="canonical_option_id", ext_floor_applied=True)
    args.update(kw)
    with pytest.raises(AssertionError):
        dec.bind_marginal_null_use(**args)


def test_the_run_declares_nothing_the_ruling_forbids(out):
    """The artifact must not carry a mapping, a successor cap or a verdict.

    P2-D25's three prohibitions, checked on the emitted object rather than on the
    call, because the call is what the script chose to say and this is what it
    actually wrote.
    """
    blob = json.dumps(out).lower()
    assert out["confirmatory_family_size"] == dec.P2D25_CONFIRMATORY_FAMILY_SIZE
    assert abs(out["alpha_unchanged"] - dec.P2D6_ALPHA) < 1e-12
    assert "successor" not in blob or "no successor" in blob
    assert out["blocker"]["status"].startswith("UNRULED")
    for c in out["cells"].values():
        assert c["attribution_cap"]["cap_is"] in ("SLACK", "BINDING")
        assert "P2D6_mixture_defect" in c["attribution_cap"]


# ------------------------------------------------------------- the control bases

def test_the_two_control_bases_are_what_P2D25_names(G):
    """The cap's base is the size tile's robust items; the 540 is a DIFFERENT set.

    P2-D25 fixes the primary base at the `size` tile's `beta_c = infinity` items,
    because it is the only one whose arity matches the set the cap reweights, and
    requires the all-tile figure beside it with its base named. If either count
    moves, the artifact is describing a different set from the one ruled on.
    """
    assert int(G["robust_by_tile"]["size"].sum()) == dec.P2D25_CONTROL_N
    assert sum(int(m.sum()) for m in G["robust_by_tile"].values()) == \
        dec.P2D25_CONTROL_N_ALL_TILES
    assert int(G["conf"].sum()) == dec.P2D23_CONFIRMATORY_N


def test_no_marginal_is_pooled_across_arities(G, out):
    """`ΔA_null` sums over ONE option index, so the supports must coincide.

    The all-tile `TV` is an item-weighted mean of the four within-tile distances.
    Recomputed here from the per-tile table, which is the check that it was never
    formed by pooling a marginal across `|O| in {3, 3, 4, 6}` (P2-D3).
    """
    n = {t: int(m.sum()) for t, m in G["robust_by_tile"].items()}
    total = sum(n.values())
    for key, cell in out["cells"].items():
        per_tile = out["control_TV_by_tile"][key]
        want = sum(per_tile[t]["tv"] * n[t] for t in n) / total
        assert abs(cell["control_TV"]["all_tiles_value"] - want) < 1e-12, key
        assert abs(cell["control_TV"]["value"] - per_tile["size"]["tv"]) < 1e-12


def test_the_540_figure_is_never_emitted_without_its_base(out):
    """P2-D19's discipline, applied to a second pair of bases.

    Both figures carry a base string naming the item count and the arity, so a
    reader cannot lift one number out of the artifact without the set it is on.
    """
    for cell in out["cells"].values():
        c = cell["control_TV"]
        assert str(dec.P2D25_CONTROL_N) in c["base"]
        assert str(dec.P2D25_CONTROL_N_ALL_TILES) in c["all_tiles_base"]


# -------------------------------------------------------------- the ext_i floor

def test_the_floor_is_applied_and_its_cost_is_reported(G, out):
    """P2-D23 leaves the floor in force on these aggregates and P2-D25 applies it.

    The premise is that the floor reaches the `A`-ratio aggregates and reaches
    nothing confirmatory. If the removed count were not emitted, the descriptive
    figure would be reported without saying what it excludes.
    """
    f = out["ext_floor"]
    assert f["value"] == dec.P2D23_FLOOR
    assert f["n_confirmatory_before"] == dec.P2D23_CONFIRMATORY_N
    assert f["n_removed"] == f["n_confirmatory_before"] - f["n_confirmatory_after"]
    assert f["n_removed"] == len(f["item_ids_removed"])
    assert f["min_ext_confirmatory"] > 0.0
    ext = G["ext"]
    assert int((G["conf"] & (ext < dec.P2D23_FLOOR)).sum()) == f["n_removed"]
    # and the confirmatory n for the three Arm B quantities is untouched
    assert dec.P2D23_APPLIES_TO_CONFIRMATORY is False


def test_A_is_defined_on_every_item_the_aggregates_use(G):
    """`A`'s domain is `isfinite(beta_c)`, never the float sign of `ext_i`.

    `T7.md` note 1: the two disagree on one frozen item, and an implementation
    that takes the domain from `ext_i > 0` hands an adversary-robust item a finite
    `A` of order 1e16. The floored confirmatory mask must contain no such item.
    """
    A, ids = G["A"], G["ids"]
    rows = np.array([A[int(i)] for i in ids[G["conf_floored"]]])
    assert np.isfinite(rows).all()
    for t, m in G["robust_by_tile"].items():
        assert np.isnan(np.array([A[int(i)] for i in ids[m]])).all(), t


# ------------------------------------------------- the quantities' own geometry

def test_TV_agrees_with_the_frozen_implementation(G, kept):
    """`c5_effect.tv` is the frozen distance; this run must not have a second one.

    `CLAUDE.md` treats a copied frozen computation as a duplication bug. The run
    forms a padded marginal so the signed shift is subtractable, and the premise
    is that padding the support changes no distance.
    """
    ids = G["ids"]
    keep = set(int(i) for i in ids[G["robust_by_tile"]["size"]])
    for m in TR.LADDER:
        for arm in TC.ARMS:
            c = TC.control_cell(kept, m, keep, 6, arm)
            g = kept[(kept["model"] == m) & (kept["item_id"].isin(keep))]
            want = CE.tv(g[g["framing"] == TC.BASE]["chosen_option"].values,
                         g[g["framing"] == arm]["chosen_option"].values)
            assert abs(c["tv"] - want) < 1e-12
            assert abs(c["shift"].sum()) < 1e-12
            assert 0.0 <= c["tv"] <= 1.0


def test_nothing_sits_above_the_adversary_oracle(G, out, kept):
    """`A <= 1` identically, so `A_null <= 1` identically. Beating it is a bug.

    `A_null` is a convex combination of per-option `A` and `A` is bounded above by
    1 because `marg_norm <= 1` and `A(o*_infinity) = 1`. A value above 1 is a
    misspecified coordinate or item join, never a result.
    """
    assert out["oracle_check"]["n_chosen_options_above_the_adversary_oracle"] == 0
    assert out["oracle_check"]["max_A_over_chosen_options"] <= 1.0 + dec.P2D19_EPS
    for rows in out["reference_placement"].values():
        for p in rows.values():
            assert p["A_null_median_of_per_item"] <= 1.0 + dec.P2D19_EPS
            assert p["A_null_from_the_means"] <= 1.0 + dec.P2D19_EPS
            assert p["A_observed_median_of_per_item"] <= 1.0 + dec.P2D19_EPS
            assert abs(sum(p["option_marginal"]) - 1.0) < 1e-12


def test_A_null_from_the_means_is_the_reweighting_the_cap_uses(G, out):
    """One weight vector, two users, so the cap and the placement cannot drift.

    `A_null`'s from-the-means aggregate is `p . mean_i A_i(o)` and `ΔA_null` is
    `(p_arm - p_F0) . mean_i A_i(o)` on the control marginals. Both read the same
    `mean_i A_i(o)`, recomputed here from the frozen geometry rather than from the
    artifact.
    """
    A, ids = G["A"], G["ids"]
    want = np.array([A[int(i)] for i in ids[G["conf_floored"]]]).mean(axis=0)
    for cell in out["cells"].values():
        got = np.array(cell["attribution_cap"]["mean_A_by_option"])
        assert np.allclose(got, want, atol=1e-12)
        shift = np.array(cell["control_TV"]["signed_shift"])
        assert abs(float(shift @ want)
                   - cell["attribution_cap"]["dA_null"]) < 1e-12
    for m, rows in out["reference_placement"].items():
        for p in rows.values():
            assert abs(float(np.array(p["option_marginal"]) @ want)
                       - p["A_null_from_the_means"]) < 1e-12


def test_the_cap_verdict_is_the_comparison_it_claims_to_be(out):
    """SLACK means the observed mean exceeds `ΔA_null`; there is no third case.

    The premise is that the label is a function of the two emitted numbers and of
    nothing else, so it cannot drift into a judgement while looking like one.
    """
    for key, cell in out["cells"].items():
        k = cell["attribution_cap"]
        want = "SLACK" if k["observed_mean_dA"] > k["dA_null"] else "BINDING"
        assert k["cap_is"] == want, key


# --------------------------------------------------------- the refactor's effect

def test_pair_delta_A_leaves_the_frozen_c5_counts_untouched():
    """`c5_delta_A` gained a helper; `v2.7`'s published `n_eff` must still hold.

    `inertness_ceiling.pair_delta_A` was factored out so `t7_control` could reuse
    the per-pair `ΔA` instead of copying it. If that changed what the default
    contrast computes, every quantity calibrated against `c5` would be measured
    against a reference nothing reproduces.
    """
    df, cols, A, ids, sets = TR.item_sets()
    keep = set(int(i) for i in ids[sets["size_tile_confirmatory"]])
    got = IC.c5_delta_A(TR.load_choices(), A, keep)
    assert {m: v["n_eff_item"] for m, v in got.items()} == dict(
        dec.P2D20_C5_N_EFF_ITEM)
    assert {m: v["n_eff"] for m, v in got.items()} == dict(
        dec.P2D20_C5_N_EFF_PAIR_EXACT)
    stored = json.load(open("results/T5_inertness_ceiling.json"))
    per = stored["diagnostic_c5_direction"]["per_model"]
    for m, v in got.items():
        assert abs(v["sign_proportion_item"] - per[m]["sign_proportion_item"]) \
            < 1e-12, m


def test_per_item_delta_A_is_the_pairs_averaged_within_item(G, kept):
    """`v2.0` section 3.2's item value, and P2-D20's unit for the same rows.

    An item with one surviving pair contributes that pair (P2-D16), so the item
    count is the number of distinct items with at least one surviving pair and
    never the pair count.
    """
    A, ids = G["A"], G["ids"]
    keep = set(int(i) for i in ids[G["conf_floored"]])
    for m in TR.LADDER:
        for arm in TC.ARMS:
            it, _, _, d = IC.pair_delta_A(kept, A, m, keep, "framing",
                                          TC.BASE, arm)
            s = TC.per_item_delta_A(kept, A, m, keep, arm)
            assert set(s.index) == set(it)
            assert len(s) <= len(d)
            assert abs(float(s.loc[it[0]])
                       - float(d[it == it[0]].mean())) < 1e-12
