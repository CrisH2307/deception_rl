"""Direct evaluation of the pool's closed-form-versus-bisection disagreements.

VERIFICATION ONLY. Fixes nothing, rules nothing. `results/T1_beta_c_crosscheck.json`
found 161 pool items where `adversary._crossings` (spec 6.3 closed form) and
`adversary.beta_critical_batch` (bisection, value of record) disagree on whether
`beta_c` is finite. This evaluates V_beta directly on every one of them, and on
the both-finite items whose two values differ by more than 1e-3, to establish
which method is wrong and why.

Run: python3 src/beta_c_disagreement.py   (writes results/T1_beta_c_disagreement.json)
"""
import json
import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adversary as adv  # noqa: E402
import k2_gate as K      # noqa: E402
import t6_arm_a as t6    # noqa: E402
from p1 import TAU_MAIN  # noqa: E402

OUT = "results/T1_beta_c_disagreement.json"
TILES = ("hold", "manmade", "moves", "size")
GRID = np.unique(np.concatenate([np.linspace(0, 20, 4001), np.geomspace(20, 5e3, 400)]))
BAND = TAU_MAIN + 1e-12      # D51 as tiebreak.lex_obayes applies it: rel >= 1 - 1e-9 - 1e-12


def one(df, row):
    return adv.build_batch(df.iloc[[int(row)]].reset_index(drop=True))


def coeffs(b, o0, c):
    a, bb, cc = adv._abc(b, 1.0)
    num = cc[0, c] * a[0, o0] - cc[0, o0] * a[0, c]
    den = cc[0, o0] * bb[0, c] - cc[0, c] * bb[0, o0]
    sn = abs(cc[0, c] * a[0, o0]) + abs(cc[0, o0] * a[0, c])
    sd = abs(cc[0, o0] * bb[0, c]) + abs(cc[0, c] * bb[0, o0])
    return float(num), float(den), float(abs(num) / sn), float(abs(den) / sd)


def trajectory(b, o0, comp):
    """Raw lead of `comp` over o*_0 on GRID, and whether the tie-broken argmax
    (the spec's predicate) ever leaves o*_0 and ever returns to it."""
    L = np.stack([adv.log_v_beta(b, x)[0] for x in GRID])
    lead = np.exp(L[:, comp] - L[:, o0]) - 1.0
    stay = np.array([int(adv.optimal_option(b, x)[0]) == o0 for x in GRID])
    lost = ~stay
    k = int(lost.argmax()) if lost.any() else -1
    return (float(lead.max()), bool(lost.any()),
            bool(lost.any() and stay[k:].any()), k)


def main():
    df = K.pool()
    cols = t6.arm_a_columns(df, chunk=K.CHUNK)
    tiles = df["tile"].values
    o0 = np.asarray(cols["o0"]).astype(int)
    oinf = np.asarray(cols["oinf"]).astype(int)
    ofit = df["o_fit"].values.astype(int)
    bis = np.asarray(cols["beta_c"], float)
    cf = np.empty(len(df)); cfarg = np.full(len(df), -1)
    for t in TILES:
        ix = np.where(tiles == t)[0]
        sub = df.iloc[ix].reset_index(drop=True); xs, ag = [], []
        for b in adv.build_batch(sub, chunk=K.CHUNK):
            x = adv._crossings(b, 1.0, parallel_tol=0.0); xs.append(x.min(axis=1)); ag.append(x.argmin(axis=1))
        xx = np.concatenate(xs)
        cf[ix] = np.where(np.isfinite(xx), np.log(xx), np.inf); cfarg[ix] = np.concatenate(ag)

    fb, fc = np.isfinite(bis), np.isfinite(cf)
    want = o0 != oinf
    identity = {t: {"bisection_violations": int((fb[m] != want[m]).sum()),
                    "closed_form_violations": int((fc[m] != want[m]).sum())}
                for t, m in [(t, tiles == t) for t in TILES] + [("all", np.ones(len(df), bool))]}

    sep = oinf != ofit
    A = np.where(fc & ~fb)[0]; B = np.where(fb & ~fc)[0]
    with np.errstate(invalid="ignore"):
        gap = cf - bis
    early = np.where(fb & fc & (gap < -1e-3))[0]; late = np.where(fb & fc & (gap > 1e-3))[0]

    def closed_form_group(rows):
        rec = dict(n=len(rows), max_abs_num=0.0, max_abs_den=0.0, max_rel_num=0.0,
                   max_rel_den=0.0, n_both_coeffs_below_eps_tie=0, max_lead_over_o0=-1.0,
                   n_o0_loses=0, n_o0_regains=0, n_live=0, pairs=Counter())
        for r in rows:
            b = one(df, r); z = int(adv.optimal_option(b, 0.0)[0]); c = int(cfarg[r])
            num, den, rn, rd = coeffs(b, z, c)
            rec["max_abs_num"] = max(rec["max_abs_num"], abs(num))
            rec["max_abs_den"] = max(rec["max_abs_den"], abs(den))
            rec["max_rel_num"] = max(rec["max_rel_num"], rn); rec["max_rel_den"] = max(rec["max_rel_den"], rd)
            rec["n_both_coeffs_below_eps_tie"] += int(abs(num) < adv.EPS_TIE and abs(den) < adv.EPS_TIE)
            lead, loses, regains, _ = trajectory(b, z, c)
            rec["max_lead_over_o0"] = max(rec["max_lead_over_o0"], lead)
            rec["n_o0_loses"] += loses; rec["n_o0_regains"] += regains
            rec["n_live"] += int(adv.optimal_option(b, np.inf)[0] != z)
            rec["pairs"][f"{tiles[r]}:{min(z, c)},{max(z, c)}"] += 1
        rec["pairs"] = dict(rec["pairs"].most_common())
        return rec

    def tiebreak_group(rows):
        rec = dict(n=len(rows), n_winner_inside_d51_band=0, n_winner_higher_fit=0,
                   n_margins_equal_1e9=0, max_winner_lead_over_o0=-1.0,
                   n_o0_regains=0, bisection_beta_c_range=[float(bis[rows].min()), float(bis[rows].max())])
        for r in rows:
            b = one(df, r); z = int(adv.optimal_option(b, 0.0)[0])
            x = float(bis[r]) * (1 + 1e-6) + 1e-9
            w = int(adv.optimal_option(b, x)[0]); lv = adv.log_v_beta(b, x)[0]
            rel = np.exp(lv - lv.max())
            rec["n_winner_inside_d51_band"] += int(rel[w] >= 1.0 - BAND)
            rec["n_winner_higher_fit"] += int(b.fit_star[0, w] > b.fit_star[0, z])
            m = adv.margin_batch(b)[0]
            rec["n_margins_equal_1e9"] += int(abs(m[w] - m[z]) < 1e-9)
            lead, _, regains, _ = trajectory(b, z, w)
            rec["max_winner_lead_over_o0"] = max(rec["max_winner_lead_over_o0"], lead)
            rec["n_o0_regains"] += regains
        return rec

    gA = closed_form_group(A)
    out = {
        "purpose": "Direct V_beta evaluation of the pool closed-form/bisection disagreements.",
        "emitted_by": "src/beta_c_disagreement.py",
        "status": "VERIFICATION ONLY. No fix applied; value of record unchanged.",
        "d51_band": BAND,
        "identity_beta_c_finite_iff_o0_ne_oinf": identity,
        "identity_note": "bisection returns inf iff optimal_option(inf) == o*_0, so its "
                         "violation count is 0 by construction and is not evidence.",
        "n_disagreeing": int((fb != fc).sum()),
        "separating_count_bisection": int((fb & sep).sum()),
        "separating_count_closed_form": int((fc & sep).sum()),
        "separating_that_enter_under_closed_form": int((fc & ~fb & sep).sum()),
        "separating_that_enter_are_all_in_group_A": bool(np.isin(np.where(fc & ~fb & sep)[0], A).all()),
        "all_separating_inside_span_guard_bisection": bool(
            ((1.0 - np.asarray(cols["sal_pole"], float)) <= t6.SB_MIN_SPAN)[fb & sep].all()),
        "group_A_closed_form_finite_bisection_inf": gA,
        "group_A_search_ceiling": {"n_live": gA["n_live"],
            "max_closed_form_beta": float(cf[A].max()) if len(A) else None,
            "note": "bisection never searches a non-live item, so its ceiling cannot "
                    "explain any group A item"},
        "group_B_bisection_finite_closed_form_inf": tiebreak_group(B),
        "both_finite_closed_form_earlier": closed_form_group(early),
        "both_finite_closed_form_later": tiebreak_group(late),
        "max_abs_gap_both_finite": float(np.nanmax(np.abs(gap[fb & fc]))),
    }
    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    print(json.dumps({k: v for k, v in out.items() if not isinstance(v, dict)}, indent=1))
    print(f"written: {OUT}")


if __name__ == "__main__":
    main()
