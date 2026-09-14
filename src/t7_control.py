"""T7 step 4, and the part of step 5 P2-D25 authorizes. Nothing else.

WHAT THIS EMITS, AND UNDER WHAT STANDING.

P2-D25 rules what `A_null(m, F)` and `ΔA_null(m, F)` may be used for, and it ruled
it BEFORE either existed: the author split the sessions so the ruling was made
blind to the values. This script is the other half of that split. It computes
under the ruling and it revisits nothing.

  STEP 4, the `beta_c = infinity` control (`v2.0` section 4.4, first paragraph).
      `TV(m, F) = 0.5 * sum_o |p^ctrl_{m,F}(o) - p^ctrl_{m,F0}(o)|`, the total
      variation between a model's option marginals under the arm and under `F0`,
      on items where `o*_0 = o*_infinity`. There is nothing adversary-relevant to
      move toward there, so movement is prompt sensitivity. That purpose is
      independent of the attribution cap and P2-D6 and P2-D12 do not reach it: it
      is a function of chosen options, not of `ΔA`, of `A` or of `ext_i`.
      DESCRIPTIVE, and it was never anything else.

      The base is the `size` tile's adversary-robust items (P2-D25, P2-D4): the
      only base whose option arity matches the set the cap reweights. The all-tile
      figure is reported BESIDE it with its base named, never alone (P2-D19's
      discipline, applied to a second pair of bases). It is formed per tile and
      then item-weighted, never by pooling a marginal across `|O| in {3,3,4,6}`,
      which P2-D3 rejected and which `bind_marginal_null_use` asserts against.

  THE ATTRIBUTION CAP (`v2.0` section 4.4).
      `ΔA_null(m, F) = sum_o (p^ctrl_{m,F}(o) - p^ctrl_{m,F0}(o)) * mean_i A_i(o)`,
      compared against the observed mean `ΔA`. P2-D6 DEMOTED mean `ΔA` rather than
      deleting it, so the cap follows its quantity down and applies to it
      unchanged, at descriptive standing. No successor is authorized and none is
      needed (P2-D25). P2-D6's mixture finding reaches BOTH sides of the
      comparison, since `ΔA_null` is built from `mean_i A_i(o)`, and the defect is
      emitted beside the comparison rather than repaired.

  STEP 5, reference-set placement (`v2.0` section 3.3).
      `A_null(m, F) = sum_o p_{m,F}(o) * A_i(o)` on the confirmatory set, with
      section 3.2's two aggregates, placed beside the Bayes oracle at `A = 0`, the
      adversary oracle at `A = 1`, and salience at `A_i(o_fit)`. DESCRIPTIVE: a
      reference is not a test, and the confirmatory family stays at 21 tests at
      `alpha = 0.05/21` (P2-D25).

WHAT THIS DOES NOT EMIT, AND WHY EACH ABSENCE IS DELIBERATE.

  * NO mapping from `A_null` or `ΔA_null` onto quantity (c). P2-D25 authorizes
    none and rules that none may be written: (c) is a sign proportion, both of
    these are levels in `A` units, and a bridge written now is written with all
    fourteen of (c)'s cells published.
  * NO successor cap, and no direction claim of any kind (P2-D24).
  * NO control-set same-option or change rate. It would be the natural companion
    to quantity (a) and P2-D25 does not authorize it; `v2.0` section 4.4's control
    measure is `TV` and `TV` is what is computed.
  * NO marginal over rendered menu POSITIONS. P2-D25 rejected one: it is a new
    quantity chosen after the (4,5) signature was seen, and the signature is on
    canonical option ids, which P1's Format V permutes per item and per
    permutation.
  * NO verdict on H-B. P2-D5's second conjunct is UNRULED and stays the author's.
    P2-D25 holds whichever way it goes and this script inherits that.

THE `ext_i` FLOOR. P2-D23 leaves the `ext_i >= 0.02` floor in force on every mean
or median of per-item `A` and on the `ΔA` null, and P2-D25 requires it applied
here. It reaches the confirmatory `A` aggregates and the count it removes is
reported. It does NOT reach the control marginals, which read chosen options only
and form no ratio, and it cannot: `ext_i = 0` is the defining property of the
control set, so a floor applied there would delete the control set itself.

Run: python3 src/t7_control.py          (writes results/T7_control_marginal_null.json
                                         and reports/T7_control_marginal_null.md)
     python3 src/t7_control.py --demo   (self-checks that do not need the write)
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c5_effect as CE          # noqa: E402
import inertness_ceiling as IC  # noqa: E402
import p1                       # noqa: E402
import p2_decisions as P2D      # noqa: E402
import t6_f0_headroom as H      # noqa: E402
import t7_armb as T7            # noqa: E402
import tie_reference as TR      # noqa: E402

OUT = "results/T7_control_marginal_null.json"
REPORT = "reports/T7_control_marginal_null.md"

BASE = T7.BASE          # "F0"
ARMS = T7.ARMS          # ("F1", "F2")
LADDER = TR.LADDER
FLOOR = H.EXT_FLOOR     # 0.02, v2.0 section 6 / P2-D23


def geometry():
    """The frozen item geometry every quantity here reads, and its masks.

    `A`'s domain is `isfinite(beta_c)`, never the float sign of `ext_i`
    (`T7.md` note 1): `tie_reference.item_sets` already takes it from `beta_c`,
    and the control set is its complement on the same test, so the one frozen item
    where the two disagree lands on the control side exactly once.
    """
    df, cols, A, ids, sets = TR.item_sets()
    _, _, _, ext = H.item_axis()
    tiles = df["tile"].values
    robust = ~np.isfinite(cols["beta_c"])
    conf = sets["size_tile_confirmatory"]
    return {
        "df": df, "cols": cols, "A": A, "ids": ids, "ext": ext, "tiles": tiles,
        "conf": conf,                       # 108 six-option confirmatory items
        "conf_floored": conf & (ext >= FLOOR),
        "robust_by_tile": {t: robust & (tiles == t) for t in sorted(set(tiles))},
    }


def marginal(chosen, k):
    """`p(o)` over canonical option ids, on the renderings given.

    The support is the item set's full option arity, not the ids observed, so two
    marginals are always subtractable. `total_variation` below checks this against
    `c5_effect.tv`, which forms the same distribution over the observed union;
    they agree because an unobserved id contributes zero to both.
    """
    c = np.asarray(chosen, dtype=int)
    if c.size == 0:
        raise AssertionError("empty cell: no surviving rendering to form a "
                             "marginal from. Stop rather than emit nan.")
    return np.bincount(c, minlength=k) / c.size


def control_cell(kept, model, keep, k, arm):
    """`TV(m, F)` and the signed marginal shift on one control base. `v2.0` 4.4.

    The signed shift is the cap's input and `TV` is its absolute half-sum, so both
    come from one pair of marginals rather than from two passes. `c5_effect.tv` is
    the frozen implementation of the distance and is called as the cross-check
    rather than reimplemented.
    """
    g = kept[(kept["model"] == model) & (kept["item_id"].isin(keep))]
    c0 = g[g["framing"] == BASE]["chosen_option"].values
    c1 = g[g["framing"] == arm]["chosen_option"].values
    p0, p1_ = marginal(c0, k), marginal(c1, k)
    shift = p1_ - p0
    tv = float(0.5 * np.abs(shift).sum())
    frozen = CE.tv(c0, c1)
    assert abs(tv - frozen) < 1e-12, (
        f"TV from the padded marginal is {tv!r} and c5_effect.tv gives "
        f"{frozen!r}. They are the same quantity; a gap means the support "
        "padding changed the distribution.")
    return {"tv": tv, "shift": shift, "p_base": p0, "p_arm": p1_,
            "n_renderings_base": int(len(c0)), "n_renderings_arm": int(len(c1)),
            "n_items": int(len(keep)), "arity": int(k)}


def mean_A_by_option(A, ids, mask):
    """`mean_i A_i(o)`, the cap's weight vector, on the floored confirmatory set.

    One value per canonical option id. P2-D6 measured what this object is: a mean
    over a three-way mixture, poles at exactly 0 and exactly 1 and an off-pole
    tail unbounded below. That defect is reported beside every number built from
    it and is not repaired here, because repairing it is the successor P2-D25
    declines.
    """
    rows = np.array([A[int(i)] for i in ids[mask]])
    assert np.isfinite(rows).all(), "A is undefined on an item in the " \
        "confirmatory mask; the domain was taken from ext_i rather than beta_c"
    return rows.mean(axis=0)


def per_item_delta_A(kept, A, model, keep, arm):
    """`v2.0` section 3.2's per-item `ΔA`: pair values averaged within item.

    Routed through `inertness_ceiling.pair_delta_A`, which is also what quantity
    (c) reads, so the cap's left-hand side and the sign test see the same pairs
    under the same P2-D16 exclusion.
    """
    it, _, _, d = IC.pair_delta_A(kept, A, model, keep, "framing", BASE, arm)
    return pd.Series(d, index=it).groupby(level=0).mean()


def compute():
    """Every authorized quantity and every disclosure. No verdict, no mapping."""
    G = geometry()
    A, ids, ext = G["A"], G["ids"], G["ext"]
    conf, confF = G["conf"], G["conf_floored"]
    keep_conf = set(int(i) for i in ids[confF])
    kept, raw = T7.load_t7()

    # ---- the control bases. Arity is constant within a tile, so a per-tile TV
    # never forms a marginal across arities and the all-tile figure is an
    # item-weighted mean of four within-arity distances rather than a pooled one.
    bases = {}
    for t, m in G["robust_by_tile"].items():
        k = int(len(A[int(ids[m][0])]))
        bases[t] = {"mask": m, "keep": set(int(i) for i in ids[m]),
                    "arity": k, "n": int(m.sum())}

    # ---- bindings. A run that departs from a decision fails here, not in a number.
    P2D.bind_armb(P2D.P2D3_TILE, p1.artifact_hash(p1.ITEMS_FINAL), pooled=False)
    P2D.bind_ext_floor(float(ext[conf].min()), int(conf.sum()),
                       quantities_reading_ext=())
    P2D.check_p1_ext_floor_source()
    # P2-D25. The six premises that make a use of these quantities well formed.
    # No value of A_null, dA_null or TV appears in the call and none can make it
    # pass or fail: the ruling was made before any of them existed.
    P2D.bind_marginal_null_use(
        in_confirmatory_family=False,
        confirmatory_family_size=21,
        alpha=P2D.P2D6_ALPHA,
        mapping_to_quantity_c=None,
        successor_cap=None,
        control_arity=bases[P2D.P2D25_CONTROL_TILE]["arity"],
        confirmatory_arity=P2D.P2D25_CONFIRMATORY_ARITY,
        hypothesis_support="canonical_option_id",
        ext_floor_applied=True)

    assert bases["size"]["n"] == P2D.P2D25_CONTROL_N, (
        f"the size tile carries {bases['size']['n']} adversary-robust items and "
        f"P2-D25 names {P2D.P2D25_CONTROL_N} as the control base")
    n_all = sum(b["n"] for b in bases.values())
    assert n_all == P2D.P2D25_CONTROL_N_ALL_TILES, (
        f"{n_all} adversary-robust items across tiles against P2-D25's "
        f"{P2D.P2D25_CONTROL_N_ALL_TILES}")

    mean_A = mean_A_by_option(A, ids, confF)
    o_fit = G["df"]["o_fit"].values.astype(int)
    a_fit = np.array([A[int(i)][int(o)] for i, o in zip(ids[confF], o_fit[confF])])

    oracle = T7.oracle_check(kept, A, set(int(i) for i in ids[conf]))

    # ---- step 5's placement. Per MODEL, not per arm: A_null is a function of the
    # cell's own option marginal, so `F0` is one row like `F1` and `F2` rather
    # than a baseline subtracted from them.
    placement = {}
    for m in LADDER:
        g = kept[(kept["model"] == m) & (kept["item_id"].isin(keep_conf))]
        placement[m] = {}
        for F in (BASE,) + ARMS:
            gg = g[g["framing"] == F]
            p = marginal(gg["chosen_option"].values,
                         P2D.P2D25_CONFIRMATORY_ARITY)
            per_item_null = np.array([float(p @ A[int(i)]) for i in ids[confF]])
            assert (per_item_null <= 1.0 + P2D.P2D19_EPS).all(), (
                "A_null above the adversary oracle. A_null is a convex "
                "combination of A_i(o) and A <= 1 identically, so this is a "
                "misspecified coordinate or item join, never a result. "
                "CLAUDE.md: beating the oracle is a bug.")
            obs = np.array([A[int(i)][int(o)] for i, o
                            in zip(gg["item_id"].values,
                                   gg["chosen_option"].values)])
            oi = pd.Series(obs, index=gg["item_id"].values).groupby(level=0).mean()
            placement[m][F] = {
                "option_marginal": [float(x) for x in p],
                "n_renderings": int(len(gg)),
                "n_items": int(oi.size),
                "A_null_median_of_per_item": float(np.median(per_item_null)),
                "A_null_from_the_means": float(p @ mean_A),
                "A_observed_median_of_per_item": float(oi.median()),
                "A_observed_from_the_means": float(oi.mean()),
                "excess_median": float(oi.median() - np.median(per_item_null)),
                "excess_from_the_means": float(oi.mean() - p @ mean_A),
                "excess_is":
                    "DESCRIPTIVE and licenses nothing. v2.0 section 3.3 defines "
                    "excess as A_observed - A_null; P2-D5's second conjunct, "
                    "which would make it load-bearing, is UNRULED and stays the "
                    "author's. P2-D25 holds under all three readings of it and "
                    "this run claims none of them.",
            }

    cells, tiles_out = {}, {}
    for arm in ARMS:
        for m in LADDER:
            per_tile = {t: control_cell(kept, m, b["keep"], b["arity"], arm)
                        for t, b in bases.items()}
            tiles_out[f"{m}|{arm}"] = {
                t: {"tv": v["tv"], "n_items": v["n_items"], "arity": v["arity"],
                    "n_renderings_base": v["n_renderings_base"],
                    "n_renderings_arm": v["n_renderings_arm"]}
                for t, v in per_tile.items()}
            size = per_tile["size"]
            tv_all = float(sum(per_tile[t]["tv"] * bases[t]["n"]
                               for t in per_tile) / n_all)

            # the cap, on the base P2-D25 names
            dA_null = float(size["shift"] @ mean_A)
            s = per_item_delta_A(kept, A, m, keep_conf, arm)
            mean_dA, med_dA = float(s.mean()), float(s.median())

            cells[f"{m}|{arm}"] = {
                "model": m, "framing": arm, "contrast": f"{arm} - {BASE}",
                "control_TV": {
                    "value": size["tv"],
                    "base": f"size tile, beta_c = infinity, n = {bases['size']['n']} "
                            f"items, |O| = {size['arity']} (P2-D25, P2-D4)",
                    "n_items": size["n_items"],
                    "n_renderings_base": size["n_renderings_base"],
                    "n_renderings_arm": size["n_renderings_arm"],
                    "option_marginal_base": [float(x) for x in size["p_base"]],
                    "option_marginal_arm": [float(x) for x in size["p_arm"]],
                    "signed_shift": [float(x) for x in size["shift"]],
                    "all_tiles_value": tv_all,
                    "all_tiles_base":
                        f"all four tiles, beta_c = infinity, n = {n_all} items, "
                        "|O| in {3, 3, 4, 6}. Item-weighted mean of the four "
                        "WITHIN-TILE distances; no marginal is pooled across "
                        "arities (P2-D3, and bind_marginal_null_use's arity "
                        "premise). Reported beside the size figure, never alone.",
                    "role":
                        "DESCRIPTIVE, and never anything else. v2.0 section 4.4's "
                        "first paragraph: o*_0 = o*_infinity on these items, so "
                        "there is nothing for an adversary-aware model to move "
                        "toward and any change in the choice distribution is "
                        "PROMPT SENSITIVITY. That ground is independent of the "
                        "cap, of mean dA and of A, so P2-D6 and P2-D12 do not "
                        "reach it (P2-D25).",
                    "what_it_cannot_say":
                        "It cannot size how much of the confirmatory movement it "
                        "explains. Sizing that is the reweighting, the "
                        "reweighting lands in A units at the level, and A is "
                        "undefined on the control set by v2.0 section 3.2. The "
                        "control set can show that generic movement exists; it "
                        "cannot adjudicate whether the confirmatory movement IS "
                        "that movement (P2-D25).",
                },
                "attribution_cap": {
                    "dA_null": dA_null,
                    "observed_mean_dA": mean_dA,
                    "observed_median_dA": med_dA,
                    "n_items": int(s.size),
                    "cap_is": "SLACK" if mean_dA > dA_null else "BINDING",
                    "criterion":
                        "v2.0 section 4.4: a confirmatory tracking claim required "
                        "BOTH that the interval on mean dA exclude zero in the "
                        "POSITIVE direction and that observed mean dA exceed "
                        "dA_null. The first conjunct was retired when P2-D6 "
                        "demoted the mean. What is computed here is the second, "
                        "against the quantity it was written for, at that "
                        "quantity's current descriptive standing (P2-D25).",
                    "standing":
                        "DESCRIPTIVE on both sides. No successor cap is "
                        "authorized and none is claimed; no mapping onto quantity "
                        "(c) exists and none may be written (P2-D25).",
                    "P2D6_mixture_defect":
                        "Named rather than repaired. P2-D6 measured what a mean "
                        "of per-item A is on this geometry: a three-way mixture, "
                        "470 option-cells at exactly 0, 439 at exactly 1, 841 "
                        "off-pole at median -3.329, unbounded below. dA_null is "
                        "built from mean_i A_i(o) and the observed side is a mean "
                        "of per-item A differences, so the defect reaches BOTH "
                        "ends and the comparison is weak on both. Substituting a "
                        "median, a bounded transform or a trimmed mean would be "
                        "inventing the successor P2-D25 declines.",
                    "mean_A_by_option": [float(x) for x in mean_A],
                },
            }

    return {
        "purpose":
            "T7 step 4 (the beta_c = infinity control) and the part of step 5 "
            "P2-D25 authorizes: A_null, dA_null and TV, all DESCRIPTIVE. No "
            "mapping onto quantity (c), no successor cap, no direction claim, no "
            "verdict on H-B.",
        "emitted_by": "src/t7_control.py",
        "ruled_by": "P2-D25 / PREREGISTRATION_v2.16.md, recorded in "
                    "PREREGISTRATION_v2.17.md",
        "rule": TR.RULE, "prompt_form": TR.FORM, "base_framing": BASE,
        "alpha_unchanged": P2D.P2D6_ALPHA,
        "confirmatory_family_size": P2D.P2D25_CONFIRMATORY_FAMILY_SIZE,
        "choices_sha256": p1.artifact_hash(T7.CHOICES),
        "items_sha256": p1.artifact_hash(p1.ITEMS_FINAL),
        "ext_floor": {
            "value": FLOOR,
            "in_force_on":
                "The A-ratio aggregates on the CONFIRMATORY set: A_null's two "
                "aggregates, the observed A aggregates, mean_i A_i(o) inside "
                "dA_null, and mean dA. P2-D23 leaves the floor in force on every "
                "mean or median of per-item A and on the dA null; P2-D25 requires "
                "it applied and the removed count reported.",
            "not_in_force_on":
                "The control marginals and TV, which read chosen options only and "
                "form no ratio. It could not apply there in any case: ext_i = 0 "
                "is the defining property of the control set, so a floor there "
                "would delete the set itself.",
            "n_confirmatory_before": int(conf.sum()),
            "n_confirmatory_after": int(confF.sum()),
            "n_removed": int(conf.sum() - confF.sum()),
            "item_ids_removed": [int(i) for i in ids[conf & ~(ext >= FLOOR)]],
            "min_ext_confirmatory": float(ext[conf].min()),
            "max_ext_confirmatory": float(ext[conf].max()),
            "note":
                "This count is the one PREREGISTRATION_v2.16.md section 7 records "
                "the ruling session as wanting and declining to compute, and "
                "P2-D23 declined before it. It changes a descriptive figure, not "
                "its standing. The CONFIRMATORY n is untouched and stays "
                f"{P2D.P2D23_CONFIRMATORY_N} (P2-D23).",
        },
        "control_bases": {
            "primary": {
                "tile": P2D.P2D25_CONTROL_TILE,
                "n_items": bases["size"]["n"],
                "arity": bases["size"]["arity"],
                "why": "P2-D4's base, and the only one whose option arity matches "
                       "the set the cap reweights: dA_null multiplies p^ctrl(o) "
                       "by mean_i A_i(o) over the six-option confirmatory items, "
                       "so the control marginal must live on the same support.",
            },
            "reported_beside": {
                "n_items": n_all,
                "per_tile": {t: {"n_items": b["n"], "arity": b["arity"]}
                             for t, b in bases.items()},
                "why": "T7.md's SCOPE sentence names the 540 non-divergent items. "
                       "That sentence is about how much inference to buy, not "
                       "about the cap's base, and the two numbers are both "
                       "correct about different sets (P2-D25).",
            },
        },
        "salience_reference": {
            "definition": "A_i(o_fit) on the floored confirmatory set; where a "
                          "salience-driven chooser lands (v2.0 section 3.3)",
            "n": int(len(a_fit)),
            "median": float(np.median(a_fit)),
            "from_the_means": float(a_fit.mean()),
            "n_exactly_1": int((a_fit == 1.0).sum()),
            "share_exactly_1": float((a_fit == 1.0).mean()),
            "coincides_with_the_adversary_oracle": bool((a_fit == 1.0).all()),
            "note": "A_i(o*_infinity) = 1 by construction, so A_i(o_fit) = 1 "
                    "wherever the two coincide. On the divergence set they "
                    "coincide on 452 of 460 items (P2-D5), and `results/"
                    "T6_F0_headroom.json` puts ZERO of the eight exceptions on "
                    "the size tile. So on the confirmatory set the salience "
                    "reference and the adversary oracle are the SAME POINT and "
                    "the four-reference set of v2.0 section 3.3 collapses to "
                    "three. That is P2-D5's level confound at its sharpest: it "
                    "is a property of the frozen item geometry, measured before "
                    "any model is read, and it is why v2.0 section 3.3 puts "
                    "every content claim on excess over the marginal null rather "
                    "than on raw A.",
        },
        "reference_set": {
            "bayes_oracle": 0.0, "adversary_oracle": 1.0,
            "note": "A_i(o*_0) = 0 and A_i(o*_infinity) = 1 by construction "
                    "(v2.0 section 3.2). The point is where a chooser sits on the "
                    "interval, not whether it beats a baseline (T7.md step 5).",
        },
        "f0_replication_on_excess": {
            "source": "results/T7_f0_replication.json",
            "size_tile_disagreeing_renderings": 0,
            "size_tile_renderings": 3500,
            "what_it_means":
                "v2.0 section 4.2 requires the F0 replication to be reported on "
                "post_norm AND on excess over the marginal null. F0 and Paper 1's "
                "cond4 disagree on ZERO of the 3,500 size-tile renderings, so "
                "every function of chosen options agrees identically there, "
                "A_null and the excess included. The gate is satisfied BY "
                "CONSTRUCTION on this tile and A_null adds no information to it. "
                "Recorded so it is never presented as a check that passed on its "
                "own strength (PREREGISTRATION_v2.16.md section 5.2).",
        },
        "oracle_check": oracle,
        "reference_placement": placement,
        "cells": cells,
        "control_TV_by_tile": tiles_out,
        "steps_not_run": {
            "step_4_control_change_rate":
                "NOT COMPUTED. A same-option or change rate on the control set "
                "would be the natural companion to quantity (a), and P2-D25 does "
                "not authorize it: v2.0 section 4.4's control measure is TV and TV "
                "is what is computed. Compute no quantity P2-D25 did not "
                "authorize.",
            "step_5_direction_and_verdict":
                "NOT ISSUED. The placement is emitted; the reading of it as "
                "content is blocked by P2-D5's second conjunct, which is UNRULED "
                "and stays the author's, and by P2-D24 for anything about "
                "direction.",
            "step_6_size_ladder":
                "NOT RUN. Step 6 asks whether adversary sensitivity appears at "
                "any scale, which is a statement that a model does or does not "
                "track the adversary, and that is exactly what P2-D5's unruled "
                "conjunct blocks. P2-D25 authorizes no quantity for it and "
                "explicitly does not rule the blocker. Every table here is "
                "ordered by the ladder, so the descriptive substrate exists the "
                "moment the blocker is ruled.",
            "menu_position_marginal":
                "NOT COMPUTED. P2-D25 alternative 4 rejected it twice over: it is "
                "a new preregistered quantity chosen after the (4,5) signature "
                "was seen, and the signature is on canonical option ids, which "
                "P1's Format V permutes per item and per permutation.",
        },
        "blocker": {
            "id": "P2-D5's second conjunct, excess over the marginal null",
            "status": "UNRULED, and P2-D25 does not rule it",
            "effect_here":
                "The excess A_observed - A_null is emitted per cell and is "
                "DESCRIPTIVE. Under all three readings of the conjunct it stays "
                "descriptive: if the conjunct travels and needs an operational "
                "form, the excess would have to enter the confirmatory family and "
                "nothing here puts one there; if it expired with the mean, there "
                "is no conjunct to satisfy; if (a), (b) and (c) already satisfy "
                "it, it is discharged by quantities this run does not touch. "
                "Nothing here is offered as discharging it "
                "(PREREGISTRATION_v2.16.md section 5.5).",
        },
    }


def _fmt(x, n=4):
    return f"{x:.{n}f}"


def report(out):
    """The markdown report. Every number in it comes from `out`, none is typed."""
    L = []
    w = L.append
    cb = out["control_bases"]
    w("# T7 step 4: the `beta_c = infinity` control, and the marginal null\n")
    w(f"Generated by `python3 src/t7_control.py`. Every number is emitted by that "
      f"script from `{T7.CHOICES}` and Paper 1's frozen artifacts.\n")
    w("**Everything here is DESCRIPTIVE.** P2-D25 rules `A_null`, `ΔA_null` and the "
      "control `TV` out of the confirmatory family, which stays at "
      f"{out['confirmatory_family_size']} tests at `alpha` = "
      f"{out['alpha_unchanged']:.6f}. No mapping onto quantity (c) exists and none "
      "may be written; no successor to the attribution cap is authorized; no "
      "direction claim is made (P2-D24); no verdict on H-B is issued.\n")
    f = out["ext_floor"]
    w(f"`ext_i` floor {f['value']} (P2-D23, applied per P2-D25): the confirmatory "
      f"`A` aggregates run on **{f['n_confirmatory_after']}** of "
      f"{f['n_confirmatory_before']} items, **{f['n_removed']} removed**. The "
      "confirmatory `n` for the three Arm B quantities is untouched and stays "
      f"{P2D.P2D23_CONFIRMATORY_N}. The floor does not reach the control "
      "marginals, which read chosen options only.\n")
    w(f"Item file `sha256` `{out['items_sha256']}`; T7 choices `sha256` "
      f"`{out['choices_sha256']}`.\n")

    w("## 1. Step 4: the control result, per model and framing\n")
    w("`o*_0 = o*_infinity` on these items, so the optimal option does not change "
      "and there is nothing for an adversary-aware model to move toward. "
      "`TV(m, F) = 0.5 * sum_o |p_F(o) - p_F0(o)|` over canonical option ids. "
      "**Any change here is prompt sensitivity, not adversary tracking, and it "
      "caps how much of the divergence-set effect can be attributed** (`v2.0` "
      "section 4.4, first paragraph; T7 step 4).\n")
    w(f"**Primary base:** `{cb['primary']['tile']}` tile, `beta_c = infinity`, "
      f"**n = {cb['primary']['n_items']}** items, `|O|` = "
      f"{cb['primary']['arity']}. {cb['primary']['why']}\n")
    per_tile = ", ".join(f"`{t}` {v['n_items']} at arity {v['arity']}"
                         for t, v in cb["reported_beside"]["per_tile"].items())
    w(f"**Reported beside it:** all four tiles, **n = "
      f"{cb['reported_beside']['n_items']}** ({per_tile}). Item-weighted mean of "
      "the four within-tile distances; no marginal is pooled across arities. "
      f"{cb['reported_beside']['why']}\n")
    w("| model | framing | `TV` on the 142 | `TV` on the 540 | control renderings "
      "`F0` | control renderings arm |")
    w("|---|---|---:|---:|---:|---:|")
    for arm in ARMS:
        for m in LADDER:
            c = out["cells"][f"{m}|{arm}"]["control_TV"]
            w(f"| `{m}` | `{arm}` | {_fmt(c['value'])} | "
              f"{_fmt(c['all_tiles_value'])} | {c['n_renderings_base']} | "
              f"{c['n_renderings_arm']} |")
    w("")
    w("Per tile, so neither base can be quoted without the other:\n")
    w("| model | framing | " + " | ".join(
        f"`{t}` (n={v['n_items']}, arity {v['arity']})"
        for t, v in cb["reported_beside"]["per_tile"].items()) + " |")
    w("|---|---|" + "---:|" * len(cb["reported_beside"]["per_tile"]))
    for arm in ARMS:
        for m in LADDER:
            r = out["control_TV_by_tile"][f"{m}|{arm}"]
            w(f"| `{m}` | `{arm}` | " + " | ".join(
                _fmt(r[t]["tv"]) for t in cb["reported_beside"]["per_tile"]) + " |")
    w("")
    w("What `TV` cannot say: it cannot size how much of the confirmatory movement "
      "it explains. Sizing that is the reweighting, the reweighting lands in `A` "
      "units at the level, and `A` is undefined on the control set by `v2.0` "
      "section 3.2. **The control set can show that generic movement exists. It "
      "cannot adjudicate whether the confirmatory movement is that movement.**\n")

    w("## 2. The attribution cap, against the descriptive mean `ΔA`\n")
    w("`ΔA_null(m, F) = sum_o (p_F^ctrl(o) - p_F0^ctrl(o)) * mean_i A_i(o)`, the "
      "control-set option-frequency shift applied as a reweighting on the "
      f"confirmatory set ({f['n_confirmatory_after']} items after the floor). "
      "`v2.0` section 4.4 required a confirmatory tracking claim to clear it; "
      "P2-D6 demoted mean `ΔA` rather than deleting it, so the cap follows its "
      "quantity down and is applied to it unchanged at descriptive standing. "
      "**No successor is authorized and none is claimed** (P2-D25).\n")
    w("SLACK means the observed mean exceeds `ΔA_null`; BINDING means it does "
      "not. This is a descriptive comparison of two means and nothing else: the "
      "criterion's other conjunct, a positive-direction interval on mean `ΔA`, "
      "was retired with the mean, and no reading of either column is licensed "
      "about quantity (c) or about direction.\n")
    w("| model | framing | `ΔA_null` | observed mean `ΔA` | observed median `ΔA` "
      "| cap | `n` |")
    w("|---|---|---:|---:|---:|---|---:|")
    for arm in ARMS:
        for m in LADDER:
            c = out["cells"][f"{m}|{arm}"]["attribution_cap"]
            w(f"| `{m}` | `{arm}` | {_fmt(c['dA_null'])} | "
              f"{_fmt(c['observed_mean_dA'])} | {_fmt(c['observed_median_dA'])} | "
              f"{c['cap_is']} | {c['n_items']} |")
    w("")
    w("The observed median `ΔA` is exactly 0 in every cell, because most items "
      "do not change their chosen option and an unchanged choice has `ΔA = 0` "
      "identically. `v2.0` section 3.2 requires both aggregates and the median is "
      "the one it prefers on this geometry; the cap is stated on the MEAN, which "
      "is the quantity `v2.0` section 4.4 wrote it against, so the mean is what "
      "the comparison uses and the median is reported beside it rather than "
      "substituted for it.\n")
    w("**P2-D6's mixture defect.** " +
      out["cells"][f"{LADDER[0]}|{ARMS[0]}"]["attribution_cap"]
      ["P2D6_mixture_defect"] + "\n")
    mA = out["cells"][f"{LADDER[0]}|{ARMS[0]}"]["attribution_cap"]["mean_A_by_option"]
    w("The weight vector `mean_i A_i(o)` on the floored confirmatory set, which is "
      "where that defect enters: " +
      ", ".join(f"`o={k}` {v:.4f}" for k, v in enumerate(mA)) + ".\n")
    w("**Arm B's confirmatory family therefore carries no defence against the "
      "hypothesis that the movement is a generic prompt-induced shift in option "
      "preference, and it cannot acquire one**, because acquiring one means "
      "writing a level-to-sign mapping with every cell of quantity (c) published. "
      "That inability is the finding and it is reported as a property of the "
      "design, not as a caveat on a result (P2-D25).\n")

    w("## 3. Step 5: reference-set placement on the `A` axis\n")
    s = out["salience_reference"]
    w(f"References (`v2.0` section 3.3): Bayes oracle `o*_0` at **A = 0**, "
      f"adversary oracle `o*_infinity` at **A = 1**, salience `A_i(o_fit)` at "
      f"median **{_fmt(s['median'])}** / from-the-means **{_fmt(s['from_the_means'])}** "
      f"on n = {s['n']} ({s['n_exactly_1']} items at exactly 1, "
      f"{s['share_exactly_1']:.4f}), and the marginal null `A_null(m, F)`. "
      "The point is where a chooser sits on the interval, not whether it beats a "
      "baseline (T7 step 5).\n")
    if s["coincides_with_the_adversary_oracle"]:
        w("**The reference set collapses from four points to three on this "
          "set.** " + s["note"] + "\n")
    w("Both of `v2.0` section 3.2's aggregates are reported for every cell: the "
      "median of per-item values and the value computed from the means. A mean of "
      "per-item `A` is dominated by the off-pole tail and is not read alone.\n")
    w("| model | framing | `A_null` median | `A_null` from means | `A` obs median "
      "| `A` obs from means | excess median | excess from means |")
    w("|---|---|---:|---:|---:|---:|---:|---:|")
    for m in LADDER:
        for F in (BASE,) + ARMS:
            p = out["reference_placement"][m][F]
            w(f"| `{m}` | `{F}` | {_fmt(p['A_null_median_of_per_item'])} | "
              f"{_fmt(p['A_null_from_the_means'])} | "
              f"{_fmt(p['A_observed_median_of_per_item'])} | "
              f"{_fmt(p['A_observed_from_the_means'])} | "
              f"{_fmt(p['excess_median'])} | {_fmt(p['excess_from_the_means'])} |")
    w("")
    w("The excess columns are **descriptive and license nothing**. `v2.0` section "
      "3.3 defines excess as `A_observed - A_null`; P2-D5's second conjunct, which "
      "would make it load-bearing, is UNRULED and stays the author's. The "
      "permitted sentence is the flat one: model `m` under framing `F` sits at or "
      "away from what its own option marginal would produce on this item "
      "geometry. It is not a statement about movement and not a claim that a "
      "model carries adversary-relevant content.\n")
    fr = out["f0_replication_on_excess"]
    w(f"**`F0` replication on excess over the marginal null** (`v2.0` section 4.2). "
      f"{fr['what_it_means']}\n")

    w("## 4. What was not computed, and under which clause\n")
    for k, v in out["steps_not_run"].items():
        w(f"- **`{k}`.** {v}")
    w("")
    w("## 5. Oracle check\n")
    o = out["oracle_check"]
    w(f"{o['renderings_checked']} confirmatory renderings checked; "
      f"{o['n_chosen_options_above_the_adversary_oracle']} chosen options above "
      f"`A = 1`; max `A` over chosen options {o['max_A_over_chosen_options']:.6f}. "
      f"{o['bound_is']} `A_null` is a convex combination of per-option `A`, so it "
      "carries the same bound and is asserted against it per cell.\n")
    return "\n".join(L) + "\n"


def main():
    out = compute()
    os.makedirs("results", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    open(REPORT, "w").write(report(out))
    print(f"{'cell':12s} {'TV(142)':>8s} {'TV(540)':>8s} {'dA_null':>9s} "
          f"{'mean dA':>9s} {'cap':>8s}")
    for arm in ARMS:
        for m in LADDER:
            c = out["cells"][f"{m}|{arm}"]
            t, k = c["control_TV"], c["attribution_cap"]
            print(f"{m + ' ' + arm:12s} {t['value']:8.4f} "
                  f"{t['all_tiles_value']:8.4f} {k['dA_null']:9.4f} "
                  f"{k['observed_mean_dA']:9.4f} {k['cap_is']:>8s}")
    f = out["ext_floor"]
    print(f"\next_i floor {f['value']}: {f['n_removed']} of "
          f"{f['n_confirmatory_before']} confirmatory items removed from the "
          f"descriptive A aggregates; confirmatory n unchanged at "
          f"{P2D.P2D23_CONFIRMATORY_N}")
    print(f"written: {OUT}\n         {REPORT}")
    return 0


def demo():
    """The premises the numbers rest on, checked without writing anything."""
    G = geometry()
    A, ids = G["A"], G["ids"]
    assert int(G["conf"].sum()) == P2D.P2D23_CONFIRMATORY_N
    assert int(G["robust_by_tile"]["size"].sum()) == P2D.P2D25_CONTROL_N
    assert sum(int(m.sum()) for m in G["robust_by_tile"].values()) == \
        P2D.P2D25_CONTROL_N_ALL_TILES
    kept, _ = T7.load_t7()
    keep = set(int(i) for i in ids[G["robust_by_tile"]["size"]])
    c = control_cell(kept, LADDER[0], keep, P2D.P2D25_CONFIRMATORY_ARITY, ARMS[0])
    assert 0.0 <= c["tv"] <= 1.0
    assert abs(c["shift"].sum()) < 1e-12, "a marginal shift must sum to zero"
    print(f"ok: {P2D.P2D23_CONFIRMATORY_N} confirmatory items, "
          f"{P2D.P2D25_CONTROL_N} size-tile control items, "
          f"{P2D.P2D25_CONTROL_N_ALL_TILES} across tiles; TV agrees with "
          "c5_effect.tv and the marginal shift sums to zero")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
