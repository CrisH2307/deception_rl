"""The closed form's parallel-case tolerance, measured before it is set.

`adversary._crossings` tests spec section 6.3's degenerate case with an exact
`den != 0`, and on 62 pool items two float-identical curves yield two rounding-size
coefficients whose ratio passes as a root (`PREREGISTRATION_v2.21.md` section 7).
v2.21 proposed treating a pair as identical when both coefficients fall below a
tolerance. Whether a tolerance can be set at all depends on the coefficients of
pairs that genuinely cross, which this measures, and it shows the tolerance belongs
on the coefficient of x alone (P2-D29): that is the spec's degenerate test in both
of its cases, and 37 root pairs are parallel with a real numerator and a
rounding-size denominator, which the both-coefficients rule leaves as roots.

Classes are defined by `V_beta`, never by the coefficients themselves. For a
linear-fractional `V_beta` the ratio `V_rival / V_o*_0` is monotone in `x`, so its
largest departure from 1 over `x >= 1` is at an endpoint: `beta = 0` or
`beta = infinity`, where it is the margin difference. A pair with a root is
INDISTINGUISHABLE when both endpoints sit inside D51's band, GENUINE otherwise.

Also emitted, per author ruling P2-D28: the tolerance-determined items (the
tie-broken winner at bisection's `beta_c` never leads `o*_0` beyond the band at any
`beta`), and the ones divergent only by tie-break (no rival ever does).

Run: python3 src/crossing_tolerance.py   (writes results/T1_crossing_tolerance.json)
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adversary as adv  # noqa: E402
import k2_gate as K      # noqa: E402
import p1                # noqa: E402
import t6_arm_a as t6    # noqa: E402
from p1 import TAU_MAIN  # noqa: E402

OUT = "results/T1_crossing_tolerance.json"
TILES = ("hold", "manmade", "moves", "size")
BAND = TAU_MAIN + 1e-12      # D51 as tiebreak.lex_obayes applies it


def per_batch(b, bc):
    """Pair coefficients (raw, before any tolerance) and per-item flags for one batch."""
    a, bb, cc = adv._abc(b, 1.0)
    r = b.rows
    o0 = adv.optimal_option(b, 0.0)
    a0, b0, c0 = a[r, o0, None], bb[r, o0, None], cc[r, o0, None]
    num = cc * a0 - c0 * a
    den = c0 * bb - cc * b0
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.where(den != 0, num / den, np.inf)
    rival = np.ones_like(x, bool); rival[r, o0] = False
    root = rival & np.isfinite(x) & (x >= 1.0)

    lv0 = adv.log_v_beta(b, 0.0)
    mg = adv.margin_batch(b)
    d0 = np.expm1(lv0 - lv0[r, o0, None])          # rival lead at beta = 0
    dinf = np.expm1(mg - mg[r, o0, None])           # rival lead at beta = infinity
    distinct = np.maximum(np.abs(d0), np.abs(dinf)) > BAND

    # the tie-broken winner just past bisection's beta_c, per row
    c, log_a, lb = adv._curve(b, 1.0)
    fb = np.isfinite(bc)
    beta = np.where(fb, bc * (1 + 1e-6) + 1e-9, 0.0)
    w = adv._select(c - np.logaddexp(log_a, lb + beta[:, None]), b.fit_star)
    tol_set = fb & (dinf[r, w] <= BAND)
    dinf_r = np.where(rival, dinf, -np.inf)
    tiebreak_only = fb & (dinf_r.max(axis=1) <= BAND)
    oinf = adv.optimal_option(b, math.inf)
    beyond_inf = np.abs(dinf) > BAND
    return dict(num=np.abs(num), den=np.abs(den), root=root, distinct=distinct,
                beyond_inf=beyond_inf,
                tol_set=tol_set, tiebreak_only=tiebreak_only, oinf=oinf, o0=o0)


def log_root(x):
    xm = x.min(axis=1)
    return np.where(np.isfinite(xm), np.log(xm), np.inf)


def both_below_rule(p, tol):
    """v2.21's proposed rule, NOT adopted: no root only when both coefficients < tol."""
    keep = p["root"] & (np.maximum(p["num"], p["den"]) >= tol)
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.where(keep, p["num"] / p["den"], np.inf)
    # num/den of the absolute values equals the signed root wherever `root` holds
    return log_root(x)


def scan(df, bc_all, chunk):
    tiles = df["tile"].values
    pairs = {"indistinguishable": [], "genuine": [], "converging": [], "strict": []}
    items = {k: np.zeros(len(df), bool) for k in ("tol_set", "tiebreak_only")}
    cf = {k: np.empty(len(df)) for k in ("exact", "adopted", "both_below")}
    oinf = np.empty(len(df), int)
    o0 = np.empty(len(df), int)
    for t in TILES:
        ix = np.where(tiles == t)[0]
        sub = df.iloc[ix].reset_index(drop=True)
        parts = adv.build_batch(sub, chunk=chunk) if chunk else [adv.build_batch(sub)]
        pos = 0
        for b in parts:
            j = ix[pos:pos + len(b)]; pos += len(b)
            p = per_batch(b, bc_all[j])
            for name, m in (("indistinguishable", p["root"] & ~p["distinct"]),
                            ("genuine", p["root"] & p["distinct"]),
                            ("converging", p["root"] & p["distinct"] & ~p["beyond_inf"]),
                            ("strict", p["root"] & p["beyond_inf"])):
                pairs[name].append(np.stack([p["num"][m], p["den"][m]], axis=1))
            for k in items:
                items[k][j] = p[k]
            cf["exact"][j] = log_root(adv._crossings(b, 1.0, parallel_tol=0.0))
            cf["adopted"][j] = log_root(adv._crossings(b, 1.0))     # adv.PARALLEL_TOL
            cf["both_below"][j] = both_below_rule(p, adv.EPS_TIE)
            oinf[j] = p["oinf"]; o0[j] = p["o0"]
    pairs = {k: np.concatenate(v) for k, v in pairs.items()}
    return pairs, items, cf, oinf, o0


def coefficient_summary(pairs):
    ind, gen = pairs["indistinguishable"], pairs["genuine"]
    m_ind = ind.max(axis=1) if len(ind) else np.array([])
    m_gen = gen.max(axis=1)
    out = {"n_root_pairs_indistinguishable": int(len(ind)), "n_root_pairs_genuine": int(len(gen)),
           "indistinguishable_max_abs_num": float(ind[:, 0].max()) if len(ind) else None,
           "indistinguishable_max_abs_den": float(ind[:, 1].max()) if len(ind) else None,
           "indistinguishable_max_of_larger_coeff": float(m_ind.max()) if len(ind) else None,
           "genuine_min_abs_num": float(gen[:, 0].min()),
           "genuine_min_abs_den": float(gen[:, 1].min()),
           "genuine_min_of_larger_coeff": float(m_gen.min()),
           "n_genuine_with_larger_coeff_below_1e-9": int((m_gen < 1e-9).sum())}
    lo = out["indistinguishable_max_of_larger_coeff"] or 0.0
    out["empty_gap"] = [lo, out["genuine_min_of_larger_coeff"]]
    out["empty_gap_exists"] = bool(lo < out["genuine_min_of_larger_coeff"])
    out["eps_tie_inside_gap"] = bool(lo < adv.EPS_TIE < out["genuine_min_of_larger_coeff"])
    # GENUINE splits by the beta = infinity endpoint: CONVERGING pairs differ beyond
    # the band only at beta = 0, so their root is a crossing below the band's
    # resolution; STRICT pairs end beyond the band. Only the larger coefficient
    # decides the fix, and the denominator alone is not a separator.
    for k in ("converging", "strict"):
        g = pairs[k]
        out[f"n_root_pairs_{k}"] = int(len(g))
        out[f"{k}_min_abs_num"] = float(g[:, 0].min()) if len(g) else None
        out[f"{k}_min_abs_den"] = float(g[:, 1].min()) if len(g) else None
        out[f"{k}_max_abs_den"] = float(g[:, 1].max()) if len(g) else None
    flat = np.concatenate([ind, pairs["converging"]])
    out["den_gap"] = [float(flat[:, 1].max()) if len(flat) else 0.0, out["strict_min_abs_den"]]
    out["den_gap_exists"] = bool(out["den_gap"][0] < out["den_gap"][1])
    out["parallel_tol_inside_den_gap"] = bool(out["den_gap"][0] < adv.PARALLEL_TOL < out["den_gap"][1])
    out["genuine_log10_larger_coeff_quantiles"] = {
        q: float(np.log10(np.quantile(m_gen, float(q)))) for q in ("0", "0.001", "0.01", "0.5")}
    return out


def residual(bc, cf, tol_set, gap_edge):
    fb, fc = np.isfinite(bc), np.isfinite(cf)
    with np.errstate(invalid="ignore"):
        g = np.abs(cf - bc)
    both = fb & fc
    disagree = (fb != fc) | (both & (g > gap_edge))
    return disagree, {
        "n_classification_disagree": int((fb != fc).sum()),
        "n_bisection_finite_closed_form_inf": int((fb & ~fc).sum()),
        "n_bisection_inf_closed_form_finite": int((~fb & fc).sum()),
        "max_abs_gap_both_finite_outside_tol_set": float(g[both & ~tol_set].max()) if (both & ~tol_set).any() else 0.0,
        "min_abs_gap_both_finite_inside_tol_set": float(g[both & tol_set].min()) if (both & tol_set).any() else None,
        "n_residual": int(disagree.sum()),
        "residual_equals_tol_set": bool((disagree == tol_set).all()),
    }


def base_report(name, df, bc, chunk, gap_edge, extra=None):
    pairs, items, cf, oinf, o0 = scan(df, bc, chunk)
    assert (np.isfinite(bc) == (o0 != oinf)).all(), f"{name}: bisection identity broken"
    ts, tb = items["tol_set"], items["tiebreak_only"]
    checks = {k: residual(bc, v, ts, gap_edge)[1] for k, v in cf.items()}
    rep = {"n_items": int(len(df)), "n_finite_beta_c": int(np.isfinite(bc).sum()),
           "coefficients": coefficient_summary(pairs),
           "n_tolerance_determined": int(ts.sum()),
           "n_divergent_only_by_tie_break": int(tb.sum()),
           "tiebreak_only_subset_of_tolerance_determined": bool((~tb | ts).all()),
           "tolerance_determined_beta_c_range": ([float(bc[ts].min()), float(bc[ts].max())]
                                                 if ts.any() else None),
           "tolerance_determined_all_above_grid_endpoint": bool((bc[ts] > max(adv.BETA_GRID)).all()),
           "cross_check_exact_den_test": checks["exact"],
           "cross_check_adopted_parallel_tol": checks["adopted"],
           "cross_check_both_below_not_adopted": checks["both_below"]}
    if extra is not None:
        rep.update(extra(ts, tb))
    return rep


def main():
    frozen = p1.load_items()
    bc_f = np.empty(len(frozen))
    for t in TILES:
        ix = np.where(frozen["tile"].values == t)[0]
        bc_f[ix] = adv.beta_critical_batch(adv.build_batch(frozen.iloc[ix].reset_index(drop=True)))

    pool = K.pool()
    cols = t6.arm_a_columns(pool, chunk=K.CHUNK)
    bc_p = np.asarray(cols["beta_c"], float)
    fb = np.isfinite(bc_p)
    sep = fb & (np.asarray(cols["oinf"]).astype(int) != pool["o_fit"].values.astype(int))
    guard = (1.0 - np.asarray(cols["sal_pole"], float)) <= t6.SB_MIN_SPAN

    def pool_extra(ts, tb):
        return {"n_divergent": int(fb.sum()),
                "n_separating": int(sep.sum()),
                "all_separating_inside_span_guard": bool(guard[sep].all()),
                "n_separating_tolerance_determined": int((sep & ts).sum()),
                "n_separating_divergent_only_by_tie_break": int((sep & tb).sum())}

    # The both-finite gap edge: a closed-form root and a bisected root of the same
    # crossing differ by the bisection tolerance (~1e-6 on the frozen base); a
    # tie-break flip differs by O(1). The edge is reported with the empty interval
    # it sits in (`max_abs_gap_both_finite_outside_tol_set`,
    # `min_abs_gap_both_finite_inside_tol_set`), not chosen.
    GAP_EDGE = 1e-3
    out = {
        "purpose": "Crossing-coefficient distribution on genuinely crossing pairs, the "
                   "parallel-case tolerance, and the cross-check's expected residual.",
        "emitted_by": "src/crossing_tolerance.py",
        "d51_band": BAND, "eps_tie": adv.EPS_TIE, "parallel_tol": adv.PARALLEL_TOL,
        "gap_edge": GAP_EDGE,
        "class_definition": "root pair = rival with a closed-form root x >= 1 under the "
                            "exact den != 0 test. INDISTINGUISHABLE: its lead over o*_0 is "
                            "inside the D51 band at beta = 0 and at beta = infinity, hence "
                            "everywhere (the ratio is monotone in x). GENUINE: otherwise.",
        "tolerance_determined_definition": "finite bisected beta_c whose tie-broken winner "
                                           "just past beta_c never leads o*_0 beyond the band "
                                           "(margin-difference lead <= band at infinity).",
        "tiebreak_only_definition": "finite bisected beta_c and no rival ever leads o*_0 "
                                    "beyond the band.",
        "bases": {"frozen_1000": base_report("frozen_1000", frozen, bc_f, None, GAP_EDGE),
                  "pool_200000": base_report("pool_200000", pool, bc_p, K.CHUNK, GAP_EDGE,
                                             pool_extra)},
    }
    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    print(json.dumps(out["bases"], indent=1))
    print(f"written: {OUT}")
    import p2_decisions as D
    D.bind_parallel_tol(adv.PARALLEL_TOL, out)
    print("P2-D28 disclosure:", D.bind_tolerance_determined_disclosure(out))


if __name__ == "__main__":
    main()
