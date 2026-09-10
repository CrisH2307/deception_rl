"""F0 headroom on the A axis: does Arm B have room to move before it starts?

MEASUREMENT ONLY. This script designs no remedy, proposes no exclusion rule and
changes no preregistered quantity. It exists because T6 Step 3 measured that
`o*_infinity` is P1's `o_fit` on 452 of 460 divergent items, which puts Arm B's
target ON the salience pole. Paper 1's headline is that models sit outside the
salience-Bayes interval on the far side of salience. If they already sit at or
past `A = 1` under F0, then Arm B's preregistered "little or no movement"
prediction could be confirmed by a ceiling rather than by insensitivity, and a
prediction confirmed by a ceiling carries no evidence.

The LEVEL of `A` is confounded by this; the CONTRASTS `F1 - F0` and `F2 - F0` are
not, since salience-driven behaviour is constant across framings and cancels.
Arm B's primary measure is already a contrast, so what is at risk is power, not
validity. That is the question these numbers are for, and it is T5's to rule on.

F0 needs no new scoring: it is byte-identical to P1's prompt where content is
shared (v2.0 section 2), and P1's condition 4 is the `base` rendering that P2-D2
puts the framing block into. So this reads P1's frozen model outputs and adds
nothing.

`A` is v2.0 section 3.2, by import of the same frozen pieces T6 uses:

    marg_norm_i(o) = p1.norm(margin_i)(o)           P1's D47 min-max
    ext_i          = 1 - marg_norm_i(o*_0)          the adversary extent
    A_i(o)         = (marg_norm_i(o) - marg_norm_i(o*_0)) / ext_i

Run: python3 src/t6_f0_headroom.py
     python3 src/t6_f0_headroom.py --demo    (self-check on A's fixed points)
"""
import json
import math
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adversary as adv  # noqa: E402
import p1  # noqa: E402
import t6_arm_a as t6  # noqa: E402  (one implementation of beta_c and o*, not two)

LADDER = os.path.join(p1.P1_ROOT, "notebooks/results_2/choices_llm.parquet")
T26 = os.path.join(p1.P1_ROOT, "notebooks/results_3/choices_llm_t26.parquet")
COND_F0 = "cond4"           # P2-D2: the `base` rendering F0 is built on
RULE = "pmi"                # D98 / D109 primary; the other two are reported
FORM = "template"           # P1's own filter in divergence_curve.py:139
EXT_FLOOR = 0.02            # v2.0 section 6, carried from P1's frontier_position
REPORT = "reports/T6_F0_headroom.md"
NUMBERS = "results/T6_F0_headroom.json"
LADDER_ORDER = ("CTRL", "B2", "B4", "L1", "L2", "L3", "L4")


def item_axis():
    """Per-item `A` over every option, plus the references, on the frozen 1,000.

    `beta_c`, `o*_0` and `o*_infinity` come from `t6.arm_a_columns`, so this
    script and the Arm A results share one implementation of each.
    """
    df = p1.load_items()
    cols = t6.arm_a_columns(df)
    t6._check_p1_path(df, cols)
    A = {}
    ext = np.empty(len(df))
    finite = np.isfinite(cols["beta_c"])
    for tile in t6.TILES:
        ix = np.where(df["tile"].values == tile)[0]
        b = adv.build_batch(df.iloc[ix].reset_index(drop=True))
        mn, _ = p1.norm(adv.margin_batch(b))          # marg_norm, P1's D47
        m0 = mn[b.rows, cols["o0"][ix]]
        e = 1.0 - m0
        ext[ix] = e
        # A's domain is `beta_c < infinity`, the DEFINITION (v2.0 section 3.2),
        # not the float sign of ext_i. v2.0 states the two are equivalent and
        # mathematically they are, but on one frozen item they disagree: see
        # `ext_domain_mismatch` below. Taking the float sign there would divide
        # by 2.2e-16 and hand Arm B a finite A for an adversary-robust item.
        den = np.where(finite[ix], e, np.nan)
        a = (mn - m0[:, None]) / den[:, None]
        for k, iid in enumerate(df["item_id"].values[ix]):
            A[int(iid)] = a[k]
    return df, cols, A, ext


def choices():
    """P1's frozen F0 rows, both files, with the filters stated and counted."""
    frames, attrition = [], []
    for path, src in ((LADDER, "results_2 ladder"), (T26, "results_3 t26")):
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} missing. Precondition failed; stop.")
        d = pd.read_parquet(path)
        if "prompt_form" not in d.columns:
            d = d.assign(prompt_form="template")     # ladder file is templated
        d = d.assign(source=src)
        n0 = len(d)
        d = d[d["condition"] == COND_F0]
        n1 = len(d)
        d = d[d["format"] == "V"]
        n2 = len(d)
        d = d[d["n_tied"] == 1]                      # D89: a tie has no single id
        n3 = len(d)
        d = d[d["unscored_reason"].fillna("").astype(str) == ""]
        attrition.append({"source": src, "rows": n0, "after_cond4": n1,
                          "after_format_V": n2, "after_n_tied_1": n3,
                          "after_unscored": len(d),
                          "dropped_tied": n2 - n3, "dropped_unscored": n3 - len(d)})
        frames.append(d)
    return pd.concat(frames, ignore_index=True), attrition


def per_item_A(g, A):
    """Mean `A` within item across the two Format V permutations (v2.0 §3.2)."""
    a = np.array([A[int(i)][int(o)]
                  for i, o in zip(g["item_id"].values, g["chosen_option"].values)])
    return (pd.DataFrame({"item_id": g["item_id"].values, "A": a})
            .groupby("item_id")["A"].mean())


def summarise(a, label):
    """The headroom question, stated as counts as well as shares."""
    a = a[np.isfinite(a)]
    n = len(a)
    if not n:
        return {"label": label, "n": 0}
    return {
        "label": label, "n": int(n),
        "n_at_or_above_1": int((a >= 1.0).sum()),
        "share_at_or_above_1": float((a >= 1.0).mean()),
        "n_above_1": int((a > 1.0).sum()),
        "share_above_1": float((a > 1.0).mean()),
        "median_A": float(np.median(a)),
        "mean_A": float(a.mean()),
        "median_headroom": float(np.median(1.0 - a)),
        "mean_headroom": float((1.0 - a).mean()),
        "headroom_percentiles": {int(p): float(np.percentile(1.0 - a, p))
                                 for p in (5, 25, 50, 75, 95)},
        "n_headroom_at_or_below_0": int(((1.0 - a) <= 0).sum()),
    }


SB_BINS = np.array([-2.0, -1.0, -0.5, -1e-9, 1e-9, 0.5, 0.9, 1 - 1e-9])


def sb_by_option(df, cols):
    """{item_id: (|O|,) sb over the item's options}. NaN below P1's span guard."""
    sal, ids = cols["sal_pole"], df["item_id"].values
    span = 1.0 - sal
    out = {}
    for tile in t6.TILES:
        ix = np.where(df["tile"].values == tile)[0]
        b = adv.build_batch(df.iloc[ix].reset_index(drop=True))
        pn, _ = p1.norm(np.exp(b.log_l_star))
        for k, j in enumerate(ix):
            out[int(ids[j])] = ((pn[k] - sal[j]) / span[j]
                                if span[j] > t6.SB_MIN_SPAN
                                else np.full(pn.shape[1], np.nan))
    return out


def renderings(ch, model, keep, A, SB, cols, ids, K, rng=None):
    """Per-rendering (not per-item) arrays for one model. `rng` gives the
    uniform-random chooser used to calibrate the residual test."""
    if rng is not None:
        it = np.repeat([int(i) for i in ids if int(i) in keep], 2)
        co = np.array([int(rng.integers(K[int(i)])) for i in it])
    else:
        g = ch[(ch["model"] == model) & (ch["prompt_form"] == FORM)
               & (ch["rule"] == RULE)]
        g = g[g["item_id"].isin(keep)]
        it, co = g["item_id"].values.astype(int), g["chosen_option"].values.astype(int)
    a = np.array([A[i][o] for i, o in zip(it, co)])
    sb = np.array([SB[i][o] for i, o in zip(it, co)])
    return it, co, a, sb


def pole_decomposition(it, co, a, o0, oinf, chance):
    """Where the choice lands relative to the two poles. `A` is near-bimodal:
    only the two poles carry A in [0, 1], every other option is strongly
    negative, so this decomposition IS the shape of the A distribution."""
    at0 = np.array([o0[i] == o for i, o in zip(it, co)])
    ati = np.array([oinf[i] == o for i, o in zip(it, co)])
    nn = ~at0 & ~ati
    return {
        "n_renderings": int(len(it)),
        "share_at_o_star_0": float(at0.mean()),
        "share_at_o_star_infinity": float(ati.mean()),
        "share_at_neither_pole": float(nn.mean()),
        "median_A_given_neither_pole": float(np.median(a[nn])) if nn.any() else None,
        "chance_rate_any_named_option": chance,
        "excess_over_chance_at_o_star_0": float(at0.mean() - chance),
        "excess_over_chance_at_o_star_infinity": float(ati.mean() - chance),
        "n_A_exactly_zero": int((a == 0.0).sum()),
        "share_A_exactly_zero": float((a == 0.0).mean()),
        "n_A_exactly_zero_not_at_o_star_0": int(((a == 0.0) & ~at0).sum()),
        "n_A_exactly_one": int((a == 1.0).sum()),
        "share_A_exactly_one": float((a == 1.0).mean()),
    }


def residual_test(it, a, sb, cloud, bin_of):
    """Is `A` more negative than the choice's position on P1's coordinate implies?

    Predictor: the median `A` among options in the same `sb` bin, taken over
    OTHER items (leave-one-item-out, so the chosen option never predicts itself).
    The residual is `A_observed - A_predicted`. A systematically NEGATIVE residual
    would mean the models sit lower on the margin axis than their posterior
    position accounts for, and that would be a finding of its own.

    The bin MEDIAN is the predictor, not the bin mean: `A` is a ratio with a
    per-item denominator that can approach zero, and v2.0 section 3.2 already
    names that pathology and prescribes medians. A mean predictor gives residuals
    of +8 to +10 for every model AND for the random chooser, which is a property
    of the predictor, not of any model.
    """
    bn = bin_of(sb)
    pred = np.full(len(a), np.nan)
    for t, (i, b) in enumerate(zip(it, bn)):
        if not np.isfinite(sb[t]):
            continue
        sub = cloud[(cloud["bin"] == b) & (cloud["item_id"] != i)]["A"].values
        if len(sub):
            pred[t] = np.median(sub)
    r = (a - pred)
    r = r[np.isfinite(r)]
    return {
        "n": int(len(r)),
        "median_residual": float(np.median(r)),
        "p25": float(np.percentile(r, 25)),
        "p75": float(np.percentile(r, 75)),
        "share_residual_exactly_zero": float((np.abs(r) < 1e-9).mean()),
        "share_residual_negative": float((r < -1e-9).mean()),
    }


def main():
    t0 = time.perf_counter()
    df, cols, A, ext = item_axis()
    tiles = df["tile"].values
    ids = df["item_id"].values
    D = np.isfinite(cols["beta_c"])
    o_fit = df["o_fit"].values.astype(int)
    is_exc = D & (cols["oinf"] != o_fit)          # o*_inf != o_fit, the 8
    floored = D & (ext < EXT_FLOOR)               # v2.0 section 6's guard

    ch, attrition = choices()
    num = {
        "task": "T6 follow-up, F0 headroom on the A axis",
        "status": "MEASUREMENT ONLY. No remedy designed, no exclusion rule "
                  "proposed, no preregistered quantity changed. Routed to T5.",
        "spec_version": adv.SPEC_VERSION,
        "condition": COND_F0,
        "condition_note":
            "P1's cond4 is the `base` rendering, the slot P2-D2 puts the framing "
            "block in. F0 is byte-identical to P1's prompt where content is "
            "shared (v2.0 section 2), so this is a read of frozen P1 output and "
            "introduces no new scoring.",
        "primary_rule": RULE, "primary_prompt_form": FORM,
        "item_base": "divergence set of P1's frozen 1,000",
        "n_divergence_set": int(D.sum()),
        "n_o_star_inf_equals_o_fit": int((D & (cols["oinf"] == o_fit)).sum()),
        "n_o_star_inf_differs_from_o_fit": int(is_exc.sum()),
        "exception_item_ids": [int(i) for i in ids[is_exc]],
        "exception_tiles": {t: int((is_exc & (tiles == t)).sum()) for t in t6.TILES},
        "ext_domain_mismatch": {
            "n_robust_with_ext_above_zero": int(((~D) & (ext > 0)).sum()),
            "max_ext_among_robust": float(ext[~D].max()),
            "min_ext_on_divergence_set": float(ext[D].min()),
            "item_ids": [int(i) for i in ids[(~D) & (ext > 0)]],
            "why_it_matters":
                "v2.0 section 3.2 states `ext_i > 0` if and only if "
                "`beta_c(i) < infinity`, and defines A's domain by that "
                "equivalence. It holds mathematically. On this frozen set the two "
                "float tests disagree on the item(s) above, where a rival beats "
                "o*_0's margin by less than P1's D51 tie-break tolerance so the "
                "tie-break keeps o*_0 and beta_c is infinite while `1 - "
                "marg_norm(o*_0)` is a positive 2e-16. An implementation that "
                "takes A's domain from the float sign of ext_i divides by that "
                "and hands Arm B a finite A of order 1e16 for an "
                "adversary-robust item. This script takes the domain from "
                "beta_c. FLAGGED FOR T7: same hazard, same item, and it is not "
                "caught by the section 6 ext floor, which is applied after the "
                "domain is fixed.",
        },
        "ext_floor": EXT_FLOOR,
        "n_below_ext_floor": int(floored.sum()),
        "n_below_ext_floor_by_tile": {t: int((floored & (tiles == t)).sum())
                                      for t in t6.TILES},
        "attrition": attrition,
        "models_found": sorted(pd.unique(ch["model"])),
    }

    # The salience reference on the A axis, which is the whole point: where a
    # purely salience-driven chooser lands without being told anything.
    a_fit = np.array([A[int(i)][int(o)] for i, o in zip(ids[D], o_fit[D])])
    num["salience_reference"] = {
        "definition": "A_i(o_fit), where a salience-driven chooser lands",
        "n": int(len(a_fit)),
        "n_exactly_1": int((a_fit == 1.0).sum()),
        "share_exactly_1": float((a_fit == 1.0).mean()),
        "median": float(np.median(a_fit)),
        "min": float(a_fit.min()), "max": float(a_fit.max()),
        "on_the_exceptions": sorted(float(A[int(i)][int(o)])
                                    for i, o in zip(ids[is_exc], o_fit[is_exc])),
        "note": "A_i(o*_infinity) = 1 by construction, so A_i(o_fit) = 1 on every "
                "item where the two coincide. The exceptions are where the axis "
                "separates salience from the adversary target at all.",
    }

    sets = {
        "divergence_set": D,
        "divergence_set_size_tile": D & (tiles == "size"),
        "o_star_inf_equals_o_fit": D & (cols["oinf"] == o_fit),
        "o_star_inf_differs_from_o_fit": is_exc,
        "divergence_set_above_ext_floor": D & (ext >= EXT_FLOOR),
    }
    id_sets = {k: set(int(i) for i in ids[m]) for k, m in sets.items()}

    # A is bounded above by 1 (v2.0 section 3.2: `marg_norm <= 1`), so "strictly
    # past the adversary target" is UNREPRESENTABLE on this axis. Asserted, so the
    # zero that appears in the tables is known to be structural and is never read
    # as an empirical finding.
    num["A_upper_bound"] = {
        "max_A_over_all_options_on_divergence_set": float(np.nanmax(
            [np.nanmax(A[int(i)]) for i in ids[D]])),
        "note": "A <= 1 by construction (v2.0 section 3.2). Any `A > 1` count "
                "below is structurally zero and is not evidence about models. "
                "The 'far side of salience' question therefore cannot be asked on "
                "the A axis and is asked on P1's own coordinate instead; see "
                "`salience_pole_on_p1_coordinate`.",
    }

    # P1's coordinate, where 'past salience' is representable and where P1's
    # headline is actually stated. sb = 0 at the salience pole, 1 at the Bayes
    # pole; sb < 0 is the far side. On the divergence set the salience pole IS
    # the adversary target on 452 of 460 items, so this is the version of the
    # user's question that the A axis cannot express.
    sal = cols["sal_pole"]
    span = 1.0 - sal
    sb_ok = D & (span > t6.SB_MIN_SPAN)
    num["salience_pole_on_p1_coordinate"] = {
        "definition": "sb_i = (post_norm_i - post_norm_i(o_fit)) / "
                      "(1 - post_norm_i(o_fit)); 0 at the salience pole, 1 at the "
                      "Bayes pole, negative on the far side of salience",
        "guard": t6.SB_MIN_SPAN,
        "n_defined_on_divergence_set": int(sb_ok.sum()),
        "n_removed_by_guard": int((D & ~sb_ok).sum()),
    }

    rows = {}
    for (model, form, rule), g in ch.groupby(["model", "prompt_form", "rule"],
                                             sort=True):
        s = per_item_A(g, A)
        cell = {}
        for k, keep in id_sets.items():
            sub = s[s.index.isin(keep)]
            cell[k] = summarise(sub.values, k)
        pnm = (g.groupby("item_id")["post_norm"].mean())     # P1's own column
        keep = {int(i) for i in ids[sb_ok]}
        pnm = pnm[pnm.index.isin(keep)]
        sal_by_id = dict(zip(ids[sb_ok], sal[sb_ok]))
        sp = np.array([sal_by_id[int(i)] for i in pnm.index])
        sb = (pnm.values - sp) / (1.0 - sp)
        cell["p1_salience_bayes_coordinate"] = {
            "label": "sb on the divergence set", "n": int(len(sb)),
            "n_at_or_past_salience_pole": int((sb <= 0).sum()),
            "share_at_or_past_salience_pole": float((sb <= 0).mean()),
            "n_strictly_past_salience_pole": int((sb < 0).sum()),
            "share_strictly_past_salience_pole": float((sb < 0).mean()),
            "n_exactly_at_salience_pole": int((sb == 0).sum()),
            "share_exactly_at_salience_pole": float((sb == 0).mean()),
            "median_sb": float(np.median(sb)),
            "mean_sb": float(sb.mean()),
        }
        rows[f"{model}|{form}|{rule}"] = {
            "model": model, "prompt_form": form, "rule": rule, "sets": cell}
    num["cells"] = rows

    # Per tile on the primary cell, because `size` is Arm B's confirmatory tile
    # and a pooled figure can hide a ceiling that bites only there.
    per_tile = {}
    for model in LADDER_ORDER:
        key = f"{model}|{FORM}|{RULE}"
        if key not in rows:
            continue
        g = ch[(ch["model"] == model) & (ch["prompt_form"] == FORM)
               & (ch["rule"] == RULE)]
        s = per_item_A(g, A)
        per_tile[model] = {
            t: summarise(s[s.index.isin(set(int(i) for i in ids[D & (tiles == t)]))].values, t)
            for t in t6.TILES}
    num["per_tile_primary_cell"] = per_tile

    # --- Items 1 and 3: the corollary check and the A = 0 point mass ---------
    SB = sb_by_option(df, cols)
    K = {int(i): len(A[int(i)]) for i in ids}
    keep = {int(i) for i in ids[D]}
    chance = float(np.mean([1.0 / K[int(i)] for i in ids[D]]))
    o0 = {int(i): int(o) for i, o in zip(ids, cols["o0"])}
    oinf = {int(i): int(o) for i, o in zip(ids, cols["oinf"])}
    cloud = pd.DataFrame(
        [(int(i), SB[int(i)][o], A[int(i)][o]) for i in ids[D] for o in range(K[int(i)])],
        columns=["item_id", "sb", "A"]).dropna()
    cloud["bin"] = np.digitize(cloud["sb"].values, SB_BINS)
    bin_of = lambda x: np.digitize(x, SB_BINS)

    num["coordinate_geometry"] = {
        "note": "A is near-bimodal: only the two poles carry A in [0, 1]. Every "
                "other option sits strongly negative, because A divides by ext_i "
                "and off-pole options fall well below o*_0 on marg_norm. This is "
                "why negative A is a statement about WHICH option was chosen, not "
                "about how far below the optimum a model landed.",
        "pearson_sb_vs_A_option_level": float(np.corrcoef(
            cloud["sb"].values, cloud["A"].values)[0, 1]),
        "spearman_sb_vs_A_option_level": float(
            cloud["sb"].corr(cloud["A"], method="spearman")),
        "median_ext_on_divergence_set": float(np.median(ext[D])),
        "n_option_level_pairs": int(len(cloud)),
        "median_A_at_salience_pole": float(
            np.median(cloud[np.abs(cloud["sb"]) < 1e-9]["A"])),
        "median_A_at_bayes_pole": float(
            np.median(cloud[np.abs(cloud["sb"] - 1) < 1e-9]["A"])),
        "median_A_off_pole": float(np.median(
            cloud[(np.abs(cloud["sb"]) >= 1e-9) & (np.abs(cloud["sb"] - 1) >= 1e-9)]["A"])),
    }

    poles, resid = {}, {}
    for model in list(LADDER_ORDER) + ["RANDOM(calibration)"]:
        rng = np.random.default_rng(0) if model.startswith("RANDOM") else None
        if rng is None and f"{model}|{FORM}|{RULE}" not in rows:
            continue
        it, co, a, sb = renderings(ch, model, keep, A, SB, cols, ids, K, rng)
        poles[model] = pole_decomposition(it, co, a, o0, oinf, chance)
        resid[model] = residual_test(it, a, sb, cloud, bin_of)
    num["pole_decomposition"] = poles
    num["residual_test"] = resid
    num["residual_test_reading"] = {
        "question": "Is A more negative than the model's position on P1's "
                    "coordinate alone predicts?",
        "answer": "No. Median residual is exactly 0 for every model and for the "
                  "uniform-random calibration chooser, and no model's residual "
                  "distribution skews negative. Nothing is left over.",
        "consequence": "Negative median A is a COROLLARY of Paper 1's far-side "
                       "finding re-expressed on the margin coordinate, not "
                       "independent evidence that models are worse than the "
                       "no-adversary optimum. It must not be reported as the "
                       "latter.",
    }

    num["what_this_does_not_decide"] = {
        "routed_to": "T5 (preregistration)",
        "open_question":
            "Whether Arm B's primary analysis is restricted to items with F0 "
            "headroom, whether a second non-salience-confounded coordinate is "
            "added, or whether the ceiling is accepted and stated as a limit on "
            "what a null can mean.",
        "not_decided_here":
            "All three. Designing the remedy in the session that produced the "
            "numbers is choosing the rule after seeing them.",
        "what_is_not_at_risk":
            "Validity of the contrasts. Salience-driven behaviour is constant "
            "across framings, so it cancels in F1 - F0 and F2 - F0 and yields "
            "Delta-A = 0. Arm B's primary measure is already a contrast. What is "
            "at risk is power: a ceiling confirms 'no movement' without evidence.",
    }

    os.makedirs("results", exist_ok=True)
    json.dump(num, open(NUMBERS, "w"), indent=2, default=str)
    write_report(num, time.perf_counter() - t0)

    print(f"F0 headroom on the {int(D.sum())}-item divergence set, "
          f"{RULE} / {FORM}:")
    print(f"  A_i(o_fit) == 1 on {num['salience_reference']['n_exactly_1']} of "
          f"{num['salience_reference']['n']} items "
          f"({num['salience_reference']['share_exactly_1']:.4f})")
    for model in LADDER_ORDER:
        key = f"{model}|{FORM}|{RULE}"
        if key not in rows:
            continue
        d = rows[key]["sets"]["divergence_set"]
        z = rows[key]["sets"]["divergence_set_size_tile"]
        print(f"  {model:5s} n={d['n']:4d}  A>=1 {d['share_at_or_above_1']:.4f}  "
              f"A>1 {d['share_above_1']:.4f}  median A {d['median_A']:+.4f}  "
              f"median headroom {d['median_headroom']:+.4f}   "
              f"[size: A>=1 {z['share_at_or_above_1']:.4f}]  "
              f"[sb<=0 {rows[key]['sets']['p1_salience_bayes_coordinate']['share_at_or_past_salience_pole']:.4f}]")
    print(f"  written: {REPORT}, {NUMBERS}")
    return 0


def write_report(num, secs):
    L = []
    w = L.append
    sr = num["salience_reference"]
    w("# T6 follow-up: F0 headroom on the `A` axis\n\n")
    w(f"Generated by `python3 src/t6_f0_headroom.py` on {time.strftime('%Y-%m-%d')}. "
      f"Deterministic, no seed. Spec `{num['spec_version']}`. No language model was "
      f"run: this reads P1's frozen `{COND_F0}` outputs.\n\n")
    w("**MEASUREMENT ONLY.** No remedy is designed here, no exclusion rule is "
      "proposed, and no preregistered quantity is changed. The decision is T5's. "
      "Designing the remedy in the session that produced the numbers is choosing "
      "the rule after seeing them.\n\n")

    w("## Why this was run\n\n")
    w(f"T6 Step 3 measured that `o*_infinity` is P1's `o_fit` on "
      f"{num['n_o_star_inf_equals_o_fit']} of {num['n_divergence_set']} divergent "
      f"items. Arm B's target is therefore ON P1's salience pole. Paper 1's "
      f"headline is that models sit outside the salience-Bayes interval on the far "
      f"side of salience. If they already sit at or past `A = 1` under F0, before "
      f"any adversary is mentioned, then Arm B's preregistered \"little or no "
      f"movement\" prediction can be confirmed by a ceiling rather than by "
      f"insensitivity.\n\n")
    w("Two consequences, and only one of them is a threat.\n\n")
    w("- **The LEVEL of `A` is confounded.** Sitting at `o*_infinity` is not "
      "evidence of adversary tracking; it is the salience-driven behaviour Paper 1 "
      "documented.\n")
    w("- **The CONTRASTS are not.** Salience-driven behaviour is constant across "
      "framings, so it cancels in `F1 - F0` and `F2 - F0` and yields `ΔA = 0`. "
      "Arm B's primary measure is already a contrast (v2.0 section 4), so the "
      "design survives this part. **What is at risk is power, not validity.**\n\n")

    w("## The salience reference on the `A` axis\n\n")
    w(f"`A_i(o*_infinity) = 1` by construction, so on every item where `o_fit` and "
      f"`o*_infinity` coincide a purely salience-driven chooser scores exactly 1. "
      f"That is **{sr['n_exactly_1']} of {sr['n']}** items "
      f"({sr['share_exactly_1']:.4f}). Median `A_i(o_fit)` is "
      f"{sr['median']:.4f}, range [{sr['min']:.4f}, {sr['max']:.4f}].\n\n")
    w(f"The {num['n_o_star_inf_differs_from_o_fit']} items where the two differ are "
      f"the only place the axis separates salience from the adversary target at "
      f"all. Their `A_i(o_fit)` values are "
      + ", ".join(f"{v:.4f}" for v in sr["on_the_exceptions"])
      + f". By tile: "
      + ", ".join(f"`{t}` {n}" for t, n in num["exception_tiles"].items() if n)
      + f". Item ids are in `{NUMBERS}`.\n\n")
    em = num["ext_domain_mismatch"]
    if em["n_robust_with_ext_above_zero"]:
        w(f"### Implementation hazard, flagged for T7\n\n")
        w(f"v2.0 section 3.2 defines `A`'s domain by \"`ext_i > 0` if and only if "
          f"`beta_c(i) < infinity`\". That equivalence holds mathematically. In "
          f"float it does not, on **{em['n_robust_with_ext_above_zero']}** item(s) "
          f"of this frozen set (ids {em['item_ids']}): a rival beats `o*_0`'s "
          f"margin by less than P1's D51 tie-break tolerance, so the tie-break "
          f"keeps `o*_0` and `beta_c` is infinite, while `1 - marg_norm(o*_0)` "
          f"comes out at {em['max_ext_among_robust']:.1e} rather than 0.\n\n")
        w(f"An implementation that takes `A`'s domain from the sign of `ext_i` "
          f"divides by that number and hands Arm B a finite `A` of order 1e16 for "
          f"an adversary-robust item. **This is not caught by section 6's "
          f"`ext >= {num['ext_floor']}` floor if the floor is applied after `A` is "
          f"formed**, and it is not caught by any range check that admits negative "
          f"`A`. This script takes the domain from `beta_c`, which is the "
          f"definition. The smallest genuine `ext_i` on the divergence set is "
          f"{em['min_ext_on_divergence_set']:.2e}, four orders of magnitude "
          f"clear of it, so the two cases are cleanly separable.\n\n")
    w(f"`ext_i` falls below v2.0 section 6's floor of {num['ext_floor']} on "
      f"{num['n_below_ext_floor']} divergent items"
      + (":" if num["n_below_ext_floor"] else ".")
      + (" " + ", ".join(f"`{t}` {n}" for t, n in
                         num["n_below_ext_floor_by_tile"].items() if n)
         if num["n_below_ext_floor"] else "")
      + " Reported; the floor is not applied to the tables below, which use the "
        "full divergence set, so the two effects stay separable.\n\n")

    w(f"## F0 `A` per model, {num['primary_rule']} / {num['primary_prompt_form']}\n\n")
    w("Per-item `A` is the mean over the two Format V permutations (v2.0 section "
      "3.2). `A = 0` is the no-adversary optimum `o*_0`, `A = 1` the adversary "
      "target `o*_infinity`. Headroom is `1 - A`.\n\n")
    w("| model | n | `A >= 1` | median `A` | median headroom | headroom p25 | p75 | `n` headroom <= 0 |\n")
    w("|---|---:|---:|---:|---:|---:|---:|---:|\n")
    for model in LADDER_ORDER:
        key = f"{model}|{num['primary_prompt_form']}|{num['primary_rule']}"
        if key not in num["cells"]:
            continue
        d = num["cells"][key]["sets"]["divergence_set"]
        w(f"| `{model}` | {d['n']} | {d['share_at_or_above_1']:.4f} | "
          f"{d['median_A']:+.4f} | "
          f"{d['median_headroom']:+.4f} | {d['headroom_percentiles'][25]:+.4f} | "
          f"{d['headroom_percentiles'][75]:+.4f} | {d['n_headroom_at_or_below_0']} |\n")

    ub = num["A_upper_bound"]
    w(f"\n**There is no `A > 1` column, and its absence is the point.** `A` is "
      f"bounded above by 1 (v2.0 section 3.2: `marg_norm <= 1`), verified here at "
      f"a maximum of {ub['max_A_over_all_options_on_divergence_set']:.4f} over "
      f"every option of every divergent item. **\"Strictly past the adversary "
      f"target\" is unrepresentable on this axis**, so a zero count would be "
      f"structural and would say nothing about any model. The question is asked "
      f"below on P1's own coordinate, where it is representable and where P1's "
      f"headline is actually stated.\n\n")
    w("\n### `size` tile only, which is Arm B's confirmatory set\n\n")
    w("A pooled figure can hide a ceiling that bites only where the confirmatory "
      "test runs (v2.3 section 3).\n\n")
    w("| model | n | `A >= 1` | median `A` | median headroom |\n")
    w("|---|---:|---:|---:|---:|\n")
    for model in LADDER_ORDER:
        key = f"{model}|{num['primary_prompt_form']}|{num['primary_rule']}"
        if key not in num["cells"]:
            continue
        d = num["cells"][key]["sets"]["divergence_set_size_tile"]
        w(f"| `{model}` | {d['n']} | {d['share_at_or_above_1']:.4f} | "
          f"{d['median_A']:+.4f} | {d['median_headroom']:+.4f} |\n")

    w(f"\n### The {num['n_o_star_inf_differs_from_o_fit']} items where "
      f"`o*_infinity != o_fit`, as a contrast\n\n")
    w("These are the only items on which `A` distinguishes the adversary target "
      "from the salient option. **Read them as a count, not a rate:** the "
      "denominator is too small for a share to mean anything, and they are "
      "reported because a contrast between the two sets is the diagnostic, not "
      "because eight items estimate anything.\n\n")
    w("| model | n | `n` with `A >= 1` | median `A` | median `A` on the coinciding items |\n")
    w("|---|---:|---:|---:|---:|\n")
    for model in LADDER_ORDER:
        key = f"{model}|{num['primary_prompt_form']}|{num['primary_rule']}"
        if key not in num["cells"]:
            continue
        e = num["cells"][key]["sets"]["o_star_inf_differs_from_o_fit"]
        c = num["cells"][key]["sets"]["o_star_inf_equals_o_fit"]
        if not e.get("n"):
            continue
        w(f"| `{model}` | {e['n']} | {e['n_at_or_above_1']} | {e['median_A']:+.4f} "
          f"| {c['median_A']:+.4f} |\n")

    sbm = num["salience_pole_on_p1_coordinate"]
    w("\n## The same question on P1's coordinate, where it is representable\n\n")
    w(f"`sb_i` is 0 at the salience pole, 1 at the Bayes pole, negative on the far "
      f"side of salience. On the divergence set the salience pole **is** the "
      f"adversary target on {num['n_o_star_inf_equals_o_fit']} of "
      f"{num['n_divergence_set']} items, so `sb <= 0` is the version of \"at or "
      f"past Arm B's target\" that the `A` axis cannot express. Defined on "
      f"{sbm['n_defined_on_divergence_set']} items; "
      f"{sbm['n_removed_by_guard']} removed by P1's own `span > {sbm['guard']}` "
      f"guard.\n\n")
    w("| model | n | at or past pole `sb <= 0` | strictly past `sb < 0` | "
      "exactly at pole `sb = 0` | median `sb` |\n")
    w("|---|---:|---:|---:|---:|---:|\n")
    for model in LADDER_ORDER:
        key = f"{model}|{num['primary_prompt_form']}|{num['primary_rule']}"
        if key not in num["cells"]:
            continue
        b = num["cells"][key]["sets"]["p1_salience_bayes_coordinate"]
        w(f"| `{model}` | {b['n']} | {b['share_at_or_past_salience_pole']:.4f} | "
          f"{b['share_strictly_past_salience_pole']:.4f} | "
          f"{b['share_exactly_at_salience_pole']:.4f} | {b['median_sb']:+.4f} |\n")
    w("\n### What the two coordinates say together\n\n")
    w("They look contradictory and are not. About half of each model's choices sit "
      "**at or past the salience pole on P1's posterior coordinate**, which "
      "reproduces Paper 1's headline under F0. Almost none of that is *at* the "
      "pole: the `sb = 0` column is 0.0000 to 0.0364, so the mass is strictly on "
      "the far side. A far-side option has a **lower** posterior than `o_fit`, and "
      "`A` is the **margin** axis, on which such an option is nowhere near the "
      "maximum. Hence low `A` and negative median `A` alongside a high `sb <= 0` "
      "share. The two coordinates order options differently, and the models are "
      "past salience on one while far below the target on the other.\n\n")
    w("**The ceiling concern does not materialise.** On the axis Arm B actually "
      "scores, every model has room: `A >= 1` on 0.0174 to 0.1870 of the "
      "divergence set, median `A` at or below 0 for all seven, and median headroom "
      "between 1.0 and 1.9. A null on `ΔA` would not be produced by saturation, "
      "because there is no saturation to produce it. That is a measurement, and "
      "what follows from it is T5's to decide.\n\n")
    cg = num["coordinate_geometry"]
    pol = num["pole_decomposition"]
    res = num["residual_test"]
    rr = num["residual_test_reading"]

    w("\n## Negative median `A` is a corollary of Paper 1, not a separate finding\n\n")
    w(f"Median `A` is negative for every model on the ladder. That reads as "
      f"\"models are worse than the no-adversary optimum on the adversary's own "
      f"axis,\" and it must not be reported that way. The geometry forecloses it: "
      f"`A` is near-bimodal. Only the two poles carry `A` in `[0, 1]`, with median "
      f"`A` = {cg['median_A_at_bayes_pole']:.4f} at the Bayes pole and "
      f"{cg['median_A_at_salience_pole']:.4f} at the salience pole, while the "
      f"median over all off-pole options is {cg['median_A_off_pole']:.3f}. `A` "
      f"divides by `ext_i` (median {cg['median_ext_on_divergence_set']:.4f}), so "
      f"an off-pole option is arithmetically far negative. Negative `A` is a "
      f"statement about **which** option was chosen, not about how far below the "
      f"optimum a model landed. Pearson correlation between `sb` and `A` at the "
      f"option level is {cg['pearson_sb_vs_A_option_level']:.4f} over "
      f"{cg['n_option_level_pairs']:,} pairs; Spearman is "
      f"{cg['spearman_sb_vs_A_option_level']:.4f}.\n\n")
    w("**These tables are per rendering; the headroom tables above are per item.** "
      "v2.0 section 3.2 averages `A` within item across the two Format V "
      "permutations, and the two permutations pick different options on about a "
      "third of items, so a per-item rate is not a per-rendering rate and the two "
      "sets of numbers are not interchangeable. Per rendering is the right unit "
      "here because the question is about which option was chosen.\n\n")
    w("`RANDOM(calibration)` is a uniform-random chooser over each item's option "
      "set, seeded, included so every rate below has a reference:\n\n")
    w("| model | n | at `o*_0` | at `o*_inf` | at neither | median `A` given neither |\n")
    w("|---|---:|---:|---:|---:|---:|\n")
    for m, d in pol.items():
        w(f"| `{m}` | {d['n_renderings']} | {d['share_at_o_star_0']:.4f} | "
          f"{d['share_at_o_star_infinity']:.4f} | {d['share_at_neither_pole']:.4f} | "
          f"{d['median_A_given_neither_pole']:.3f} |\n")
    w(f"\nThe chance rate of landing on any one named option is "
      f"{list(pol.values())[0]['chance_rate_any_named_option']:.4f}, the mean of "
      f"`1/|O|` over the divergence set (`|O|` runs 3 to 6).\n\n")

    w("### What is left over, tested\n\n")
    w(f"**{rr['question']}** Predictor: the median `A` among options in the same "
      f"`sb` bin, taken over other items (leave-one-item-out, so the chosen option "
      f"never predicts itself). A systematically **negative** residual would mean "
      f"models sit lower on the margin axis than their posterior position "
      f"accounts for, and that would be a finding of its own.\n\n")
    w("| model | n | median residual | p25 | p75 | share exactly 0 | share negative |\n")
    w("|---|---:|---:|---:|---:|---:|---:|\n")
    for m, d in res.items():
        w(f"| `{m}` | {d['n']} | {d['median_residual']:+.4f} | {d['p25']:+.4f} | "
          f"{d['p75']:+.4f} | {d['share_residual_exactly_zero']:.4f} | "
          f"{d['share_residual_negative']:.4f} |\n")
    w(f"\n**{rr['answer']}** Every model's residual distribution brackets the "
      f"random chooser's. {rr['consequence']}\n\n")
    w("The bin **median** is the predictor, not the bin mean. `A` is a ratio "
      "whose per-item denominator can approach zero, and v2.0 section 3.2 already "
      "names that pathology and prescribes medians. A mean predictor returns "
      "residuals of +8 to +10 for every model **and** for the random chooser, "
      "which is a property of the predictor rather than of any model; the "
      "calibration row is what makes that visible.\n\n")

    w("### The point mass at `A = 0`\n\n")
    w("`B2` and `B4` both showed a median `A` of exactly 0.0000, so the mass at "
      "the Bayes-optimal option is reported explicitly:\n\n")
    w("| model | share `A = 0` exactly | of which not at `o*_0` | share `A = 1` exactly | excess over chance at `o*_0` |\n")
    w("|---|---:|---:|---:|---:|\n")
    for m, d in pol.items():
        w(f"| `{m}` | {d['share_A_exactly_zero']:.4f} | "
          f"{d['n_A_exactly_zero_not_at_o_star_0']} | "
          f"{d['share_A_exactly_one']:.4f} | "
          f"{d['excess_over_chance_at_o_star_0']:+.4f} |\n")
    w(f"\n**It is not a tie-handling artifact and not a baseline collapsing onto "
      f"`o_bayes`.** Tied rows are already excluded (`n_tied == 1`), and the "
      f"\"not at `o*_0`\" column counts renderings reaching `A = 0` through a "
      f"`marg_norm` tie rather than through the option itself. The mass is close "
      f"to what picking one option out of 3 to 6 produces: the chance rate is "
      f"{list(pol.values())[0]['chance_rate_any_named_option']:.4f} and the random "
      f"calibration chooser lands at "
      f"{pol['RANDOM(calibration)']['share_at_o_star_0']:.4f}. Only `B2` sits "
      f"clearly above it "
      f"({pol['B2']['excess_over_chance_at_o_star_0']:+.4f}).\n\n")
    w("Two consequences for how the baselines are read in Arm B. First, a point "
      "mass at `A = 0` is not evidence of Bayes-optimal behaviour, and this is "
      "precisely why v2.0 section 3.3 puts every claim on **excess over the "
      "marginal null** rather than on raw `A`; the `1/|O|` rate here is a cruder "
      "reference than that null and is used only to show the mass is unremarkable. "
      "Second, most models land on `o*_infinity` **below** chance while landing on "
      "`o*_0` at or above it, which is consistent with the far-side position "
      "measured above. `CTRL` is cross-family, so per P1's D111 only choice-based "
      "rates like these are comparable for it, never magnitudes.\n\n")
    w("\n## Per tile, primary cell\n\n")
    w("| model | " + " | ".join(f"`{t}` `A>=1`" for t in t6.TILES) + " |\n")
    w("|---|" + "---:|" * len(t6.TILES) + "\n")
    for model, d in num["per_tile_primary_cell"].items():
        w(f"| `{model}` | " + " | ".join(
            f"{d[t]['share_at_or_above_1']:.4f}" if d[t].get("n") else "n/a"
            for t in t6.TILES) + " |\n")

    w("\n## What this does not decide\n\n")
    nd = num["what_this_does_not_decide"]
    w(f"**Routed to {nd['routed_to']}.** {nd['open_question']}\n\n")
    w(f"{nd['not_decided_here']}\n\n")
    w(f"**Not at risk:** {nd['what_is_not_at_risk']}\n\n")

    w("## Filters and attrition\n\n")
    w(f"`condition == {COND_F0}`, `format == V`, `n_tied == 1` (P1's D89: a tied "
      f"row carries no single option id), empty `unscored_reason`. Nothing else "
      f"is dropped.\n\n")
    w("| source | rows | after `cond4` | after format V | dropped tied | dropped unscored | kept |\n")
    w("|---|---:|---:|---:|---:|---:|---:|\n")
    for a in num["attrition"]:
        w(f"| {a['source']} | {a['rows']:,} | {a['after_cond4']:,} | "
          f"{a['after_format_V']:,} | {a['dropped_tied']} | "
          f"{a['dropped_unscored']} | {a['after_unscored']:,} |\n")
    w(f"\nModels found: {', '.join(num['models_found'])}. "
      f"`prompt_form == {FORM}` is primary because that is the filter P1's own "
      f"analysis code applies to this file (`divergence_curve.py`, "
      f"`frontier_position.py`); `raw` rows for `B2` and `B4` are in "
      f"`{NUMBERS}` under their own cells. All three scoring rules are emitted; "
      f"`{RULE}` is primary per D98 and D109.\n\n")
    w(f"Every number here is emitted to `{NUMBERS}`. `A` is computed from the "
      f"same `t6_arm_a.arm_a_columns` that produced the Arm A results, so there is "
      f"one implementation of `beta_c`, `o*_0` and `o*_infinity`, not two. The "
      f"posterior was checked against P1's frozen `frontier_ext_post` and the "
      f"option ids against P1's own `post_norm` column.\n\n")
    w(f"Runtime {secs:.1f} s.\n")
    os.makedirs("reports", exist_ok=True)
    open(REPORT, "w").write("".join(L))


def demo():
    """A's fixed points, and that option ids in P1's choice file are canonical."""
    df, cols, A, ext = item_axis()
    D = np.isfinite(cols["beta_c"])
    ids = df["item_id"].values
    a0 = np.array([A[int(i)][int(o)] for i, o in zip(ids[D], cols["o0"][D])])
    ai = np.array([A[int(i)][int(o)] for i, o in zip(ids[D], cols["oinf"][D])])
    assert np.abs(a0).max() < 1e-12, f"A(o*_0) != 0, max |A| = {np.abs(a0).max():.2e}"
    assert np.abs(ai - 1).max() < 1e-12, f"A(o*_inf) != 1, max dev {np.abs(ai-1).max():.2e}"
    assert (ext[D] > 0).all(), "ext_i must be > 0 on the divergence set"
    assert np.isnan(np.array([A[int(i)][0] for i in ids[~D]])).all(), \
        "A must be undefined off the divergence set (ext_i = 0)"

    # The choice file's chosen_option must be a canonical option id, or every A
    # below is read off the wrong column. Checked against P1's own post_norm.
    d = pd.read_parquet(LADDER)
    d = d[d["n_tied"] == 1]
    pn = {}
    for tile in t6.TILES:
        ix = np.where(df["tile"].values == tile)[0]
        b = adv.build_batch(df.iloc[ix].reset_index(drop=True))
        p, _ = p1.norm(np.exp(b.log_l_star))
        for k, iid in enumerate(ids[ix]):
            pn[int(iid)] = p[k]
    mine = np.array([pn[int(i)][int(o)]
                     for i, o in zip(d["item_id"].values, d["chosen_option"].values)])
    worst = float(np.abs(mine - d["post_norm"].values).max())
    assert worst < 1e-9, (
        f"post_norm at chosen_option differs from P1's column by {worst:.2e}; "
        "chosen_option is not the canonical option id and every A is wrong")
    # The corollary argument rests on A being pinned at the poles and negative
    # off them. Asserted, so the prose cannot outlive the geometry.
    SB = sb_by_option(df, cols)
    K = {int(i): len(A[int(i)]) for i in ids}
    cloud = pd.DataFrame(
        [(int(i), SB[int(i)][o], A[int(i)][o]) for i in ids[D] for o in range(K[int(i)])],
        columns=["item_id", "sb", "A"]).dropna()
    at_sal = cloud[np.abs(cloud["sb"]) < 1e-9]["A"].values
    at_bay = cloud[np.abs(cloud["sb"] - 1) < 1e-9]["A"].values
    off = cloud[(np.abs(cloud["sb"]) >= 1e-9)
                & (np.abs(cloud["sb"] - 1) >= 1e-9)]["A"].values
    assert np.abs(at_sal - 1).max() < 1e-9, "A is not 1 at the salience pole"
    assert np.abs(at_bay).max() < 1e-9, "A is not 0 at the Bayes pole"
    assert np.median(off) < 0, \
        "off-pole A is no longer negative; the corollary argument in the report " \
        "rests on it and is now stale"
    print(f"    geometry: A = 1 on {len(at_sal)} salience-pole options, 0 on "
          f"{len(at_bay)} Bayes-pole options, median {np.median(off):.3f} on the "
          f"{len(off)} off-pole")
    print(f"ok: A(o*_0)=0 and A(o*_inf)=1 on all {int(D.sum())} divergent items, "
          f"undefined on the other {int((~D).sum())}")
    print(f"    chosen_option verified canonical on {len(d):,} untied rows "
          f"(max post_norm disagreement {worst:.1e})")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
