"""T6, Arm A: the K1 kill gate, then the beta_c characterisation.

Item bases, which are not this script's to choose:

  Step 1, the K1 gate      full unstratified 200,000-candidate pool.
                           v2.0 section 2 "Kill-gate item base"; v2.0 section 7.1.
  Steps 2 through 5        P1's frozen `items_final.parquet`, all 1,000 items,
                           all four tiles. v2.1 section 1.3 ("Arm A is T6 Steps 2
                           through 5 on T2's frozen item set") composed with v2.2
                           section 1.1, which fixes what "T2's frozen item set"
                           resolves to now that K2 has fired: reuse of P1's frozen
                           1,000. No P2 item file exists and none is drawn here.

Steps 1 and 2's gate statistics are REPRODUCTION CHECKS, not fresh gates. K1 was
computed by T1 (`reports/T1_benchmark.md`, disclosed in v2.1 section 1.2) and K2 by
T2 (`reports/T2_k2_gate.md`, applied in v2.2 section 1). Both outcomes are settled.
A discrepancy here is a bug in one of the two runs and halts the task; it does not
reopen either gate.

Nothing here selects, draws, stratifies or excludes items. `beta_c` is T1's
`adversary.beta_critical_batch`; `fit_cost`, `conflict`, `boundary_exact` and every
other item property are read from P1's frozen artifacts, never recomputed.
Deterministic: no seed enters any quantity below.

Run: python3 src/t6_arm_a.py          (writes reports/, results/, figures/)
     python3 src/t6_arm_a.py --demo   (self-check on the spec's own identities)
"""
import json
import math
import os
import sys
import time

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adversary as adv  # noqa: E402
import p1  # noqa: E402

TILES = ("manmade", "moves", "hold", "size")          # ordered by |O|: 3,3,4,6
CHUNK = 20_000
K1_THRESHOLD = 0.10        # v2.0 section 7.1, on the EXISTENCE rate
K2_THRESHOLD = 0.80        # v2.0 section 7.1
GRID = adv.BETA_GRID       # spec section 8.2: (0, .25, .5, 1, 2, 4, 8)
EXTENSION = (16.0, 32.0, 64.0)   # v2.0 section 7.1 outcome 3, in this order
STRUCTURAL_GAP = 0.10      # spec section 7.2, absolute percentage points

REPORT = "reports/T6_arm_a.md"
GATE_RECORD = "results/T6_gate_record.json"
NUMBERS = "results/T6_arm_a_numbers.json"
FROZEN_TABLE = "results/T6_frozen_arm_a.parquet"
POOL_TABLE = "data/pool_beta_c.parquet"          # T2's, for the bit-for-bit check
FIGDIR = "figures"

# Published values this run reproduces. Quoted, never recomputed into agreement.
PUBLISHED = {
    "pool_existence_rate": 0.1823,      # v2.1 section 1.2 (T1)
    "pool_grid_rate": 0.1795,           # v2.1 section 1.2 (T1)
    "pool_tile_existence": {"manmade": 0.0387, "moves": 0.1790,
                            "hold": 0.1775, "size": 0.3338},
    "pool_tile_grid": {"manmade": 0.0385, "moves": 0.1773,
                       "hold": 0.1746, "size": 0.3273},
    "k2_spearman": -0.9036,             # v2.2 section 1 (T2)
    "frozen_finite_rate": 0.4600,       # reports/T2_frozen_set_counts.md
}
RTOL = 5e-5     # published values are quoted to 4 decimals; this is their rounding


# ------------------------------------------------------------------ mechanics
PRIOR_H = None          # 1 / |H|, set from the data on the first batch seen
SB_MIN_SPAN = 0.02      # P1's own guard on the salience-Bayes span
                        # (`divergence_curve.cells`: `ok = span > 0.02`)


def arm_a_columns(df, chunk=None):
    """Every per-item Arm A quantity, in one pass, aligned to `df`'s row order.

    One function for both item bases: the pool (Step 1, chunked) and the frozen
    1,000 (Steps 2 through 5). Two implementations of `price` that could disagree
    is the hazard P1's D22 forbids for `A` and the oracle.

    `post_norm` and the salience-Bayes coordinate are P1's, by import, never
    reimplemented: `p1.norm` is `tiebreak.norm`, the D47 min-max within the item's
    own option set that produced P1's primary DV, and its raw range is the frozen
    `frontier_ext_post` column. `_check_p1_path` asserts that agreement.
    """
    global PRIOR_H
    n = len(df)
    keys = ("beta_c", "price", "L0", "Linf", "post_norm_0", "post_norm_inf",
            "sb_inf", "headroom", "range_post", "sal_pole")
    out = {k: np.empty(n) for k in keys}
    out["o0"] = np.empty(n, int)
    out["oinf"] = np.empty(n, int)
    o_fit_all = df["o_fit"].values.astype(int)
    for tile in TILES:
        ix = np.where(df["tile"].values == tile)[0]
        if not len(ix):                    # single-tile callers, e.g. the self-check
            continue
        sub = df.iloc[ix].reset_index(drop=True)
        batches = adv.build_batch(sub, chunk=chunk) if chunk else [adv.build_batch(sub)]
        pos = 0
        for b in batches:
            j = ix[pos:pos + len(b)]
            pos += len(b)
            r = b.rows
            if PRIOR_H is None:
                PRIOR_H = 1.0 / b.log_posterior.shape[1]
            o0 = adv.optimal_option(b, 0.0)
            oinf = adv.optimal_option(b, math.inf)
            L = np.exp(b.log_l_star)                       # (n, |O|) L(h*|o)
            pn, ext = p1.norm(L)                           # P1's D47 normalisation
            mg = adv.margin_batch(b)
            sp = pn[r, o_fit_all[j]]                       # S pole, P1's frontier
            span = 1.0 - sp                                # B pole is 1.0 at o_bayes
            out["beta_c"][j] = adv.beta_critical_batch(b)
            out["o0"][j], out["oinf"][j] = o0, oinf
            out["L0"][j], out["Linf"][j] = L[r, o0], L[r, oinf]
            out["price"][j] = L[r, o0] - L[r, oinf]
            out["post_norm_inf"][j] = pn[r, oinf]
            # P1's guard, verbatim: below it the salience and Bayes poles are too
            # close for the coordinate to mean anything, and P1 writes NaN.
            out["sb_inf"][j] = np.where(span > SB_MIN_SPAN,
                                        (pn[r, oinf] - sp) / np.where(span > SB_MIN_SPAN, span, 1.0),
                                        np.nan)
            out["sal_pole"][j] = sp
            out["range_post"][j] = ext
            out["headroom"][j] = mg.max(axis=1) - mg[r, o0]
            out["post_norm_0"][j] = pn[r, o0]
            # o*_0 is P1's posterior argmax, so post_norm(o*_0) is 1 up to float
            # rounding: L[o0] and L.max() are the same number reached by different
            # summation orders. A material shortfall would mean D51's relative
            # tolerance had selected a genuinely lower-posterior option, which
            # would change what the price of robustness measures, so it is
            # checked on magnitude rather than assumed away.
            worst = float(1.0 - pn[r, o0].min())
            out["_post_norm_0_max_shortfall"] = max(
                out.get("_post_norm_0_max_shortfall", 0.0), worst)
            out["_post_norm_0_below_one"] = (
                out.get("_post_norm_0_below_one", 0) + int((pn[r, o0] < 1.0).sum()))
            if worst > 1e-9:
                raise AssertionError(
                    f"post_norm(o*_0) falls to {1.0 - worst:.12f}, short of 1 by "
                    f"{worst:.3e}. That is past float rounding: D51's tie-break "
                    "has selected an option materially below the posterior "
                    "maximum, and the price of robustness would no longer be "
                    "measured from the Bayes pole. Surfaced, not clamped.")
    return out


def _check_p1_path(df, cols):
    """The posterior here must be the one that produced P1's frozen artifact.

    Cross-checked against the frozen `frontier_ext_post` column, which is the raw
    range `p1.norm` divides by. Agreement to float64 rounding proves this module
    is on `score_items -> grid_stats -> tiebreak`, the path that wrote
    `items_final.parquet`, and not on a plausible-looking substitute.
    """
    d = np.abs(cols["range_post"] - df["frontier_ext_post"].values.astype(float))
    if d.max() > 1e-12:
        raise AssertionError(
            f"posterior range differs from P1's frozen frontier_ext_post by up to "
            f"{d.max():.3e} on {int((d > 1e-12).sum())} items. The two are the "
            "same quantity; a difference this large is a code-path bug.")
    return float(d.max())


def in_D(bc, beta):
    """D(beta) membership mask. D(0) = {} by convention (spec section 7.1)."""
    if beta == 0:
        return np.zeros(len(bc), bool)
    if beta == math.inf:
        return np.isfinite(bc)
    return bc <= beta + adv.EPS_BETA


def rate_table(bc, tiles, betas):
    """{beta: {"pooled": r, tile: r_t}}, |D(beta)| / N."""
    out = {}
    for b in betas:
        m = in_D(bc, b)
        row = {"pooled": float(m.mean())}
        for t in TILES:
            s = tiles == t
            row[t] = float(m[s].mean())
        out[b] = row
    return out


def disambiguation(r):
    """Spec section 7.2's verdict from a {tile: rate} row. Criteria verbatim."""
    gap = r["size"] - min(r["manmade"], r["moves"])
    if gap >= STRUCTURAL_GAP:
        return "structural / inconclusive", gap
    if max(r[t] for t in TILES) < K1_THRESHOLD:
        return "clean negative", gap
    return "neither condition met", gap


def agrees(got, want, label, problems):
    if abs(got - want) > RTOL:
        problems.append(f"{label}: recomputed {got:.6f}, published {want:.4f}")
    return abs(got - want) <= RTOL


def pct(x, ps=(0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100)):
    return {int(p): float(np.percentile(x, p)) for p in ps}


def price_conventions(cols, D, label, o_fit):
    """The price of robustness under every denominator, on the subset `D`.

    The defined quantity is `L(h*|o*_0) - L(h*|o*_infinity)` (v2.0 section 5, T6
    Step 3), a raw difference of posterior masses. It becomes interpretable only
    against a reference, and the reference is not this session's to invent, so
    P1's own is primary and the alternatives are reported beside it.

      p1_post_norm  PRIMARY. P1's D47 coordinate: the item's own posterior range,
                    `max_o L(h*|o) - min_o L(h*|o)`, the frozen
                    `frontier_ext_post`. Since o*_0 is P1's o_bayes on every item,
                    post_norm(o*_0) = 1 and the price is `1 - post_norm(o*_inf)`.
      p1_salience_bayes  P1's frontier coordinate: the same difference over the
                    salience-to-Bayes span, `1 - post_norm(o_fit)`. NaN below
                    P1's own `span > 0.02` guard. MEASURED DEGENERATE: it returns
                    exactly 1 on every item the guard admits, on both bases,
                    because o*_infinity is o_fit. Reported as that finding, not
                    as a denominator with a distribution.
      above_prior   `L(h*|o*_0) - 1/|H|`, the mass the Bayes-optimal signal earns
                    over an uninformative one. Not a P1 convention; reported
                    because the raw ratio silently counts the prior floor as
                    earned.
      raw           `L(h*|o*_0)`, total posterior mass. The weakest of the four
                    and reported only because it is the one a reader reaches for.

    Every denominator is emitted. Nothing here is read off prose.
    """
    price = cols["price"][D]
    L0, Linf = cols["L0"][D], cols["Linf"][D]
    pn_0, pn_inf = cols["post_norm_0"][D], cols["post_norm_inf"][D]
    sb_inf = cols["sb_inf"][D]
    sb_0 = np.where(np.isfinite(sb_inf),
                    (pn_0 - cols["sal_pole"][D]) / np.where(
                        1.0 - cols["sal_pole"][D] > SB_MIN_SPAN,
                        1.0 - cols["sal_pole"][D], 1.0), np.nan)

    def summary(x, denom_desc, n_defined=None):
        v = x[np.isfinite(x)]
        return {
            "denominator": denom_desc,
            "n": int(len(v)),
            "n_undefined": int(len(x) - len(v)) if n_defined is None else n_defined,
            "mean_of_per_item_ratios": float(v.mean()),
            "median": float(np.median(v)),
            "sd": float(v.std(ddof=1)),
            "p10": float(np.percentile(v, 10)),
            "p90": float(np.percentile(v, 90)),
        }

    out = {
        "raw_difference": {
            "definition": "L(h*|o*_0) - L(h*|o*_infinity), probability scale",
            "n": int(len(price)), "mean": float(price.mean()),
            "median": float(np.median(price)), "sd": float(price.std(ddof=1)),
            "percentiles": pct(price),
        },
        "prior_floor_1_over_H": PRIOR_H,
        "reference_levels": {
            "mean_L_at_o0": float(L0.mean()),
            "mean_L_at_oinf": float(Linf.mean()),
            "mean_L_at_o0_above_prior": float((L0 - PRIOR_H).mean()),
            "mean_L_at_oinf_above_prior": float((Linf - PRIOR_H).mean()),
            "mean_item_posterior_range": float(cols["range_post"][D].mean()),
            "mean_salience_pole_post_norm": float(cols["sal_pole"][D].mean()),
        },
    }
    out["p1_post_norm"] = summary(
        pn_0 - pn_inf,
        "P1 D47: the item's own posterior range (frozen frontier_ext_post). "
        "PRIMARY, because it is the coordinate P1 already normalises this axis "
        "by and the DV Arm B is scored on.")
    out["p1_salience_bayes"] = summary(
        sb_0 - sb_inf,
        f"P1's frontier span, 1 - post_norm(o_fit); NaN where the span is at or "
        f"below P1's own guard of {SB_MIN_SPAN}.")
    out["above_prior"] = summary(
        price / (L0 - PRIOR_H),
        f"L(h*|o*_0) - 1/|H| with 1/|H| = {PRIOR_H}, the mass the Bayes-optimal "
        "signal earns over an uninformative one.")
    out["raw_share_of_total_mass"] = summary(
        price / L0, "L(h*|o*_0), total posterior mass including the prior floor.")

    # Ratio of means, which is not the mean of ratios and is the figure a reader
    # reconstructs from the reference levels above. Both are reported because on
    # `above_prior` they differ materially: the denominator reaches 2.3e-5.
    for k, den in (("p1_post_norm", cols["range_post"][D]),
                   ("above_prior", L0 - PRIOR_H),
                   ("raw_share_of_total_mass", L0)):
        out[k]["ratio_of_means"] = float(price.mean() / den.mean())
    out["p1_salience_bayes"]["ratio_of_means"] = float(
        price.mean() / (cols["range_post"][D] * (1.0 - cols["sal_pole"][D])).mean())

    # Degeneracies, surfaced rather than filtered.
    # o*_infinity is P1's salience argmax on almost every divergent item. This
    # is what collapses the salience-Bayes denominator, and it is a result rather
    # than a nuisance, so it is measured rather than described.
    oi = cols["oinf"][D]
    of = o_fit[D]
    sb_price = sb_0 - sb_inf
    fin_sb = np.isfinite(sb_price)
    out["o_star_infinity_is_o_fit"] = {
        "n": int((oi == of).sum()),
        "n_total": int(D.sum()),
        "share": float((oi == of).mean()),
        "n_exceptions": int((oi != of).sum()),
        "n_exceptions_removed_by_p1_span_guard": int(
            ((oi != of) & ~fin_sb).sum()),
        "sb_at_oinf_exactly_zero": int((sb_inf[np.isfinite(sb_inf)] == 0.0).sum()),
        "sb_defined": int(np.isfinite(sb_inf).sum()),
        "sb_price_max_shortfall_from_one": float(
            (1.0 - sb_price[fin_sb]).max()) if fin_sb.any() else 0.0,
        "note":
            "argmax_o margin(o) and P1's argmax_o f(o,h*) are different functions "
            "and this is not an identity: the exceptions exist. But every "
            "exception falls inside the set P1's own span guard removes, so on "
            "every item where the frontier coordinate is defined the price is "
            "exactly 1. Read: the adversary-robust signal sits ON P1's salience "
            "pole, and buying margin walks the whole salience-to-Bayes interval. "
            "The coordinate therefore carries no distributional information about "
            "this quantity and is not used as its denominator.",
    }
    out["degeneracies"] = {
        "n_salience_span_at_or_below_guard": int((~np.isfinite(sb_inf)).sum()),
        "n_L_at_o0_at_or_below_prior": int((L0 <= PRIOR_H).sum()),
        "n_L_at_oinf_at_or_below_prior": int((Linf <= PRIOR_H).sum()),
        "n_post_norm_at_o0_below_one": int((pn_0 < 1.0).sum()),
        "n_post_norm_at_oinf_exactly_zero": int((pn_inf == 0.0).sum()),
        "post_norm_at_oinf_zero_note":
            "Items where the adversary-robust signal is the item's LOWEST-"
            "posterior option, so the normalised price is exactly 1. Not a "
            "degeneracy: a real corner of the signal space, and the spike at 1 "
            "in the figure.",
        "max_post_norm_at_o0_shortfall_from_one": float((1.0 - pn_0).max()),
        "min_above_prior_denominator": float((L0 - PRIOR_H).min()),
        "n_above_prior_ratio_exceeding_1": int((price / (L0 - PRIOR_H) > 1.0).sum()),
        "note":
            "An `above_prior` ratio above 1 is not an error: it is an item where "
            "the margin-optimal signal leaves the truth BELOW the uniform prior, "
            "so the Scientist surrenders more than the signal earned. Those items "
            "are counted, kept, and are the reason the per-item mean of that "
            "ratio sits above its ratio of means. Nothing is clipped.",
    }
    out["item_base"] = label
    return out


# -------------------------------------------------------------------- step 1
def step1():
    """K1 over the pool. Returns (gate_record, pool_frame, problems)."""
    problems = []
    cand = pd.read_parquet(p1.ITEMS_CANDIDATE)
    scored = pd.read_parquet(p1.ITEMS_SCORED)
    if len(cand) != len(scored) or not (cand["item_id"].values == scored["item_id"].values).all():
        raise AssertionError("candidate and scored pool disagree on item identity")
    cols = arm_a_columns(scored, chunk=CHUNK)
    bc = cols["beta_c"]
    tiles = scored["tile"].values
    n = len(scored)

    # Bit-for-bit against T2's stored table. Same code, same inputs, so anything
    # other than exact equality is a bug in one of the two runs.
    bitwise = None
    if os.path.exists(POOL_TABLE):
        prev = pd.read_parquet(POOL_TABLE)
        aligned = (len(prev) == n and (prev["item_id"].values == scored["item_id"].values).all())
        bitwise = bool(aligned and np.array_equal(prev["beta_c"].values, bc))
        if not bitwise:
            d = int((prev["beta_c"].values != bc).sum()) if aligned else -1
            problems.append(f"beta_c differs from {POOL_TABLE} on {d} items "
                            "(-1 means the tables are not aligned)")

    rates = rate_table(bc, tiles, list(GRID) + [math.inf])
    existence, grid = rates[math.inf]["pooled"], rates[8.0]["pooled"]

    agrees(existence, PUBLISHED["pool_existence_rate"], "pooled existence rate", problems)
    agrees(grid, PUBLISHED["pool_grid_rate"], "pooled grid rate", problems)
    for t in TILES:
        agrees(rates[math.inf][t], PUBLISHED["pool_tile_existence"][t], f"{t} existence rate", problems)
        agrees(rates[8.0][t], PUBLISHED["pool_tile_grid"][t], f"{t} grid rate", problems)

    if existence < K1_THRESHOLD:
        outcome, extension = 1, None
    elif grid >= K1_THRESHOLD:
        outcome, extension = 2, None
    else:
        outcome = 3
        extension = []
        for b in EXTENSION:
            r = float(in_D(bc, b).mean())
            extension.append({"beta": b, "rate": r})
            if r >= K1_THRESHOLD:
                break

    verdict_inf, gap_inf = disambiguation(rates[math.inf])
    verdict_8, gap_8 = disambiguation(rates[8.0])

    record = {
        "task": "T6 Step 1", "gate": "K1",
        "status": "reproduction check of T1's run (PREREGISTRATION_v2.1 section 1.3)",
        "spec_version": adv.SPEC_VERSION,
        "preregistration": "PREREGISTRATION_v2.md section 7.1, unamended",
        "item_base": "full unstratified 200,000-candidate pool",
        "N": n,
        "threshold": K1_THRESHOLD,
        "decision_statistic": "existence rate |D(infinity)| / N",
        "pooled_existence_rate": existence,
        "pooled_grid_rate": grid,
        "per_tile_existence_rate": {t: rates[math.inf][t] for t in TILES},
        "per_tile_grid_rate": {t: rates[8.0][t] for t in TILES},
        "tile_order": list(TILES),
        "tile_n_options": {t: adv.tile_k(t) for t in TILES},
        "disambiguation_verdict": verdict_inf,
        "disambiguation_gap": gap_inf,
        "disambiguation_verdict_at_beta_8": verdict_8,
        "disambiguation_gap_at_beta_8": gap_8,
        "disambiguation_anchor_note":
            "Applied to the beta = infinity rates because the preregistration's "
            "gate decides there; spec section 7.2 anchors at beta = 8 and those "
            "rates are reported alongside. Known open item, v2.0 Appendix A.2 "
            "item 7. Not resolved here.",
        "outcome": outcome,
        "outcome_text": {1: "KILL", 2: "PASS",
                         3: "existence passes, grid too narrow"}[outcome],
        "extension": extension,
        "reproduction": {
            "bitwise_identical_to_T2_pool_table": bitwise,
            "published_matched": not problems,
            "problems": problems,
        },
        "artifact_sha256": {
            "items_candidate.parquet": p1.artifact_hash(p1.ITEMS_CANDIDATE),
            "items_scored.parquet": p1.artifact_hash(p1.ITEMS_SCORED),
            "items_final.parquet": p1.artifact_hash(p1.ITEMS_FINAL),
        },
    }
    record["pool_posterior_range_vs_frozen_frontier_ext_post_max_abs_diff"] = \
        _check_p1_path(scored, cols)
    pool = pd.DataFrame({"item_id": scored["item_id"].values, "tile": tiles,
                         "beta_c": bc, "fit_cost": scored["fit_cost"].values.astype(float),
                         "o_fit": scored["o_fit"].values.astype(int)})
    return record, pool, rates, problems, cols


# ------------------------------------------------------------- steps 2, 3, 4
def arm_a(pool, pool_rates, pool_cols):
    pool_tile_rate = {t: pool_rates[math.inf][t] for t in TILES}
    """Steps 2 through 5 on the frozen 1,000. Returns (numbers, per-item frame)."""
    df = p1.load_items()
    n = len(df)
    cols = arm_a_columns(df)
    _check_p1_path(df, cols)
    bc, price, headroom = cols["beta_c"], cols["price"], cols["headroom"]
    o0, oinf = cols["o0"], cols["oinf"]
    l_at_o0, l_at_oinf = cols["L0"], cols["Linf"]

    fin = np.isfinite(bc)
    fc = df["fit_cost"].values.astype(float)
    tiles = df["tile"].values
    num = {}

    # --- Step 2: distribution, mass at infinity, growth of |D(beta)| ---------
    frozen_rates = rate_table(bc, tiles, list(GRID) + [math.inf])
    num["step2"] = {
        "item_base": "P1 items_final.parquet, all 1,000 items, all four tiles",
        "N": n,
        "n_finite": int(fin.sum()),
        "n_infinite": int((~fin).sum()),
        "finite_rate": float(fin.mean()),
        "n_beta_c_exactly_zero": int((bc == 0.0).sum()),
        "finite_percentiles": pct(bc[fin]),
        "finite_mean": float(bc[fin].mean()),
        "finite_sd": float(bc[fin].std(ddof=1)),
        "n_finite_above_grid_endpoint": int((bc[fin] > 8.0).sum()),
        "divergence_curve_frozen": {str(k): v for k, v in frozen_rates.items()},
        "divergence_curve_pool": {str(k): v for k, v in pool_rates.items()},
        "per_tile_finite_rate": {t: float(fin[tiles == t].mean()) for t in TILES},
        "per_tile_finite_count": {t: int(fin[tiles == t].sum()) for t in TILES},
        "per_tile_finite_median": {t: float(np.median(bc[(tiles == t) & fin])) for t in TILES},
    }

    # --- Step 2: K2 reproduction. K2's item base is the pool, fixed in v2.0 --
    rho_pool = float(spearmanr(pool["beta_c"].values, pool["fit_cost"].values)[0])
    k2_problems = []
    agrees(rho_pool, PUBLISHED["k2_spearman"], "K2 pooled Spearman", k2_problems)
    fin_p = np.isfinite(pool["beta_c"].values)
    num["step2"]["K2"] = {
        "status": "reproduction check; K2 fired in T2 and is not reopened here",
        "item_base": "full 200,000-candidate pool (v2.0 section 7.1)",
        "threshold": K2_THRESHOLD,
        "spearman_pool": rho_pool,
        "fires": bool(abs(rho_pool) >= K2_THRESHOLD),
        "published": PUBLISHED["k2_spearman"],
        "problems": k2_problems,
        "pearson_finite_subset_pool": float(pearsonr(
            pool["beta_c"].values[fin_p], pool["fit_cost"].values[fin_p])[0]),
        "spearman_frozen_set_descriptive": float(spearmanr(bc, fc)[0]),
        "pearson_frozen_finite_descriptive": float(pearsonr(bc[fin], fc[fin])[0]),
    }

    # --- Step 2: the three-optima coincidence, T2's note item 1 -------------
    coin = {}
    for name, m in (("fit_cost_zero", fc == 0.0), ("fit_cost_positive", fc > 0.0)):
        coin[name] = {"N": int(m.sum()),
                      "robust_share": float((~fin)[m].mean()),
                      "finite_share": float(fin[m].mean())}
    coin["marginal_robust_share"] = float((~fin).mean())
    coin["share_of_finite_that_are_conflict"] = float((fc[fin] > 0).mean())
    coin["gap_in_robust_share_points"] = 100.0 * (
        coin["fit_cost_zero"]["robust_share"] - coin["fit_cost_positive"]["robust_share"])
    coin["pool_check"] = {
        k: {"N": int(m.sum()), "robust_share": float((~fin_p)[m].mean())}
        for k, m in (("fit_cost_zero", pool["fit_cost"].values == 0.0),
                     ("fit_cost_positive", pool["fit_cost"].values > 0.0))}
    coin["note"] = ("Confirms the T2 session's byproduct observation on Arm A's own "
                    "base. fit_cost = 0 says o_fit = o_bayes; beta_c = infinity says "
                    "o*_0 = argmax margin. Independence would put both rows near the "
                    "marginal robust share.")
    num["step2"]["three_optima_coincidence"] = coin

    # --- Step 3: the price of robustness ------------------------------------
    neg = int((price < 0).sum())
    if neg:
        raise AssertionError(
            f"{neg} items with negative price of robustness. o*_0 is the posterior "
            "argmax, so this is an implementation bug (v2.0 H-A), not a finding. "
            "Surfaced, not clipped.")
    D = fin                                  # the divergence set: finite beta_c
    pr = price[D]
    zero = pr == 0.0
    be = df["boundary_exact"].values.astype(bool)
    conv = price_conventions(cols, D, "divergence set of the frozen 1,000",
                             df["o_fit"].values.astype(int))
    num["step3"] = {
        "definition": "L(h*|o*_0) - L(h*|o*_infinity), probability scale",
        "item_base": "divergence set of the frozen 1,000 (finite beta_c)",
        "primary_convention": "p1_post_norm",
        "n_divergence_set": int(D.sum()),
        "n_negative": neg,
        "n_exactly_zero": int(zero.sum()),
        "n_exactly_zero_and_boundary_exact": int((zero & be[D]).sum()),
        "n_boundary_exact_in_D": int(be[D].sum()),
        "percentiles": pct(pr),
        "mean": float(pr.mean()),
        "sd": float(pr.std(ddof=1)),
        "conventions": conv,
        "per_tile": {t: {"n": int((D & (tiles == t)).sum()),
                         "mean": float(price[D & (tiles == t)].mean()),
                         "median": float(np.median(price[D & (tiles == t)])),
                         "p90": float(np.percentile(price[D & (tiles == t)], 90)),
                         "p1_post_norm_mean": float(
                             (cols["post_norm_0"][D & (tiles == t)]
                              - cols["post_norm_inf"][D & (tiles == t)]).mean())}
                     for t in TILES},
        "spike_at_one": {
            "definition": "post_norm(o*_infinity) == 0 exactly: the "
                          "adversary-robust signal is the item's lowest-posterior "
                          "option, so the normalised price is exactly 1",
            "n": int((cols["post_norm_inf"][D] == 0.0).sum()),
            "n_also_o_fit": int(((cols["post_norm_inf"][D] == 0.0)
                                 & (cols["oinf"][D] == df["o_fit"].values[D])).sum()),
            "mean_fit_cost": float(fc[D][cols["post_norm_inf"][D] == 0.0].mean()),
            "mean_fit_cost_rest": float(fc[D][cols["post_norm_inf"][D] != 0.0].mean()),
            "per_tile": {t: int(((cols["post_norm_inf"] == 0.0) & D
                                 & (tiles == t)).sum()) for t in TILES},
        },
        "L_at_o0_mean_in_D": float(l_at_o0[D].mean()),
        "L_at_oinf_mean_in_D": float(l_at_oinf[D].mean()),
        "robust_items_price_max": float(price[~D].max()),
    }

    # Robustness check on the pool's divergence set. The frozen set is 50%
    # conflict against the pool's 18.65%, and the price is computed conditional
    # on divergence, where that enrichment may or may not bias it. Untested until
    # here. Cheap, because Step 1's pass already built every column it needs.
    Dp = np.isfinite(pool_cols["beta_c"])
    pool_conv = price_conventions(pool_cols, Dp, "divergence set of the 200k pool",
                                  pool["o_fit"].values.astype(int))
    num["step3"]["pool_robustness_check"] = {
        "status": "descriptive robustness check, not a second estimate",
        "n_divergence_set_pool": int(Dp.sum()),
        "conflict_share_frozen": float((fc > 0).mean()),
        "conflict_share_pool": float((pool["fit_cost"].values > 0).mean()),
        "conflict_share_within_divergence_set_frozen": float((fc[D] > 0).mean()),
        "conflict_share_within_divergence_set_pool": float(
            (pool["fit_cost"].values[Dp] > 0).mean()),
        "conventions": pool_conv,
        "frozen_minus_pool": {
            k: float(conv[k]["mean_of_per_item_ratios"]
                     - pool_conv[k]["mean_of_per_item_ratios"])
            for k in ("p1_post_norm", "p1_salience_bayes", "above_prior",
                      "raw_share_of_total_mass")},
        "raw_mean_frozen_minus_pool": float(
            conv["raw_difference"]["mean"] - pool_conv["raw_difference"]["mean"]),
    }

    # --- Step 4: what predicts a low beta_c. EXPLORATORY --------------------
    num["step4"] = step4(df, bc, fin, price, headroom, tiles, fc,
                         o0 != oinf, pool_tile_rate,
                         {"beta_c": pool_cols["beta_c"], "tile": pool["tile"].values})

    frame = pd.DataFrame({
        "item_id": df["item_id"].values, "tile": tiles,
        "beta_c": bc, "is_robust": ~fin, "in_divergence_set": D,
        "price_of_robustness": price,
        "price_post_norm": cols["post_norm_0"] - cols["post_norm_inf"],
        "post_norm_at_o0": cols["post_norm_0"],
        "post_norm_at_oinf": cols["post_norm_inf"],
        "salience_bayes_at_oinf": cols["sb_inf"],
        "posterior_range": cols["range_post"],
        "o_fit": df["o_fit"].values.astype(int),
        "L_h_star_at_o0": l_at_o0,
        "L_h_star_at_oinf": l_at_oinf, "margin_headroom": headroom,
        "o_star_0": o0, "o_star_inf": oinf,
        "fit_cost": fc, "conflict": df["conflict"].values,
        "boundary_exact": be, "decision_margin": df["decision_margin"].values,
        "posterior_gap": df["posterior_gap"].values,
        "local_competition_ratio": df["local_competition_ratio"].values,
        "frontier_ext_post": df["frontier_ext_post"].values,
        "n_pareto": df["n_pareto"].values, "tie_set_size": df["tie_set_size"].values,
        "n_options": [adv.tile_k(t) for t in tiles],
    })
    return num, frame


PREDICTORS = ("fit_cost", "decision_margin", "posterior_gap",
              "local_competition_ratio", "frontier_ext_post", "n_pareto",
              "tie_set_size", "margin_headroom")


def step4(df, bc, fin, price, headroom, tiles, fc, o0_ne_oinf,
          pool_tile_rate, pool_bc):
    """EXPLORATORY. v2.0 section 10 lists this and any regression of beta_c on
    item properties as exploratory. No preregistered prediction, no threshold."""
    X = pd.DataFrame({k: df[k].values.astype(float) for k in PREDICTORS if k in df})
    X["margin_headroom"] = headroom
    out = {"status": "EXPLORATORY (v2.0 section 10). No preregistered prediction, "
                     "no threshold, no p-value is a test.",
           "item_base": "frozen 1,000"}

    # (a) The finite/infinite split is an identity, not a finding. State it, and
    #     surface where the float version of it is not exact.
    exceptions = int(((headroom > 0) != fin).sum())
    out["identity_check"] = {
        "note": "beta_c is finite iff o*_0 != o*_infinity. Any 'predictor' of "
                "finiteness that is a function of margin headroom is restating "
                "the definition, so headroom is used only among finite items, "
                "where its magnitude is not implied by membership.",
        "exact_identity_o0_ne_oinf_equals_finite": bool(
            np.array_equal(o0_ne_oinf, fin)),
        "headroom_positive_equals_finite": bool(exceptions == 0),
        "n_headroom_sign_exceptions": exceptions,
        "headroom_max_among_robust": float(headroom[~fin].max()),
        "exceptions_note":
            "The exact identity is on the tie-broken argmax and holds on every "
            "item. The raw sign test `headroom > 0` does not, and the gap is "
            "reported rather than hidden: on the items listed above some rival "
            "exceeds o*_0's margin by less than P1's D51 tie-break tolerance, so "
            "the tie-break keeps o*_0 and beta_c is infinite while the float "
            "difference is positive. The magnitudes involved are of order 1e-16. "
            "Nothing is clamped; the identity used everywhere else in this "
            "script is the argmax one.",
    }

    # (b) Among finite beta_c: rank correlation of beta_c with each property.
    rows = {}
    for k in X.columns:
        v = X[k].values[fin]
        if np.nanstd(v) == 0:
            rows[k] = {"spearman": None, "note": "constant on the finite subset"}
            continue
        rho, p = spearmanr(bc[fin], v)
        per_tile, degenerate = {}, []
        for t in TILES:
            m = fin & (tiles == t)
            # Surfaced, not filled in: a property with no variation on a tile has
            # no rank correlation there, and writing one would be an invention.
            if np.nanstd(X[k].values[m]) == 0:
                per_tile[t], _ = None, degenerate.append(t)
            else:
                per_tile[t] = float(spearmanr(bc[m], X[k].values[m])[0])
        rows[k] = {"spearman": float(rho), "p": float(p), "per_tile": per_tile,
                   "constant_on_tiles": degenerate}
    out["spearman_beta_c_vs_property_finite_subset"] = rows

    # (c) One multivariate fit, on log beta_c. beta_c == 0 items are excluded
    #     because log is undefined there, and the count is stated rather than
    #     absorbed by a shift.
    import statsmodels.api as sm
    pos = fin & (bc > 0)
    Z = X.iloc[np.where(pos)[0]].copy()
    Z = (Z - Z.mean()) / Z.std(ddof=0)
    for t in TILES[1:]:                                  # manmade is the base level
        Z[f"tile_{t}"] = (tiles[pos] == t).astype(float)
    Z = sm.add_constant(Z)
    m = sm.OLS(np.log(bc[pos]), Z).fit()
    out["ols_log_beta_c"] = {
        "n": int(pos.sum()),
        "n_excluded_beta_c_zero": int((fin & (bc == 0)).sum()),
        "note": "Continuous predictors standardized; tile dummies with manmade as "
                "base. Coefficients are on log beta_c, so a negative coefficient "
                "means the property goes with a CHEAPER adversary.",
        "r2": float(m.rsquared), "r2_adj": float(m.rsquared_adj),
        "coef": {k: float(v) for k, v in m.params.items()},
        "se": {k: float(v) for k, v in m.bse.items()},
        "t": {k: float(v) for k, v in m.tvalues.items()},
    }

    # (d) The mechanism question |O| failed: manmade 0.0387 vs moves 0.1790 at
    #     identical |O| = 3. Does a tile's structural resolution track its rate?
    out["mechanism_beyond_n_options"] = mechanism(fin, tiles, pool_tile_rate)
    out["existence_vs_magnitude"] = existence_vs_magnitude(
        bc, fin, tiles, pool_tile_rate, pool_bc)
    return out


def existence_vs_magnitude(bc, fin, tiles, pool_tile_rate, pool_bc):
    """EXPLORATORY. The tiles differ in WHETHER items diverge, barely in HOW MUCH
    budget is needed once they do.

    Reported separately from the mechanism ordering above because it is a
    different and stronger statement. The |O| ordering and the distinct-fit-vector
    ordering are both attempts to explain the between-tile spread in the existence
    rate. This observation says the spread lives entirely in that rate: conditional
    on divergence, the four tiles need almost the same budget. It also carries a
    reporting consequence, so the per-tile share above the grid endpoint is
    computed to support it.
    """
    med = {t: float(np.median(bc[fin & (tiles == t)])) for t in TILES}
    pool_fin = np.isfinite(pool_bc["beta_c"])
    pool_med = {t: float(np.median(pool_bc["beta_c"][pool_fin & (pool_bc["tile"] == t)]))
                for t in TILES}
    above8 = {t: float((bc[fin & (tiles == t)] > 8.0).mean()) for t in TILES}
    pool_above8 = {t: float((pool_bc["beta_c"][pool_fin & (pool_bc["tile"] == t)] > 8.0).mean())
                   for t in TILES}
    rate_ratio = max(pool_tile_rate.values()) / min(pool_tile_rate.values())
    med_ratio = max(med.values()) / min(med.values())
    return {
        "status": "EXPLORATORY. Separate observation, not part of the ordering "
                  "check above. No preregistered prediction, no threshold.",
        "claim": "The tiles differ in whether items diverge and barely in how much "
                 "budget is needed once they do.",
        "per_tile_median_finite_beta_c_frozen": med,
        "per_tile_median_finite_beta_c_pool": pool_med,
        "per_tile_pool_existence_rate": dict(pool_tile_rate),
        "existence_rate_max_over_min": float(rate_ratio),
        "median_beta_c_max_over_min_frozen": float(med_ratio),
        "median_beta_c_max_over_min_pool": float(
            max(pool_med.values()) / min(pool_med.values())),
        "per_tile_share_of_divergence_set_above_grid_endpoint_frozen": above8,
        "per_tile_share_of_divergence_set_above_grid_endpoint_pool": pool_above8,
        "max_per_tile_share_above_grid_endpoint_pool": float(max(pool_above8.values())),
        "reporting_consequence":
            "The grid endpoint of 8 is adequate PER TILE, not only on average: no "
            "tile leaves more than the share above outside the grid. A grid "
            "adequate on a pooled average could still be short on one tile, and "
            "this rules that out without extending the grid.",
        "why_it_is_a_cleaner_mechanism_statement":
            "It separates the existence condition from the magnitude. Whatever "
            "distinguishes the tiles acts on whether o*_0 is already the "
            "margin-maximizer, not on how far the two options sit apart in beta. "
            "Both the |O| ordering and the distinct-fit-vector ordering are "
            "tile-level covariates fitted to four points; this is a statement "
            "about the shape of the beta_c distribution within each tile and does "
            "not depend on ordering four numbers.",
    }


def mechanism(fin, tiles, pool_tile_rate):
    """EXPLORATORY. |O| does not order the divergence rates (v2.1 section 2.2).
    The candidate v2.1 names is each tile's rating spread relative to its bin
    width. That is measurable on P1's frozen fit matrices without any new data:
    a tile whose concepts collapse onto few distinct fit vectors offers the
    adversary fewer distinguishable options than its |O| suggests.

    **The outcome here is the POOL rate, not the frozen set's.** This is the one
    place in Steps 2 through 5 where that is so, and it is not a base change: the
    between-tile rate differences the mechanism question is about were measured on
    the pool in Step 1, and the frozen set's per-tile rates are flat (0.432 to
    0.488) because P1 drew 250 items per tile with a 50% conflict quota on each.
    Correlating a structural covariate against those would be reading out P1's
    quota. The frozen rates are tabulated beside the pool rates so the flatness is
    visible rather than asserted.
    """
    rows = {}
    for t in TILES:
        F, opts = p1.tile_fits()[t]
        uniq = np.unique(F, axis=0)
        rows[t] = {
            "n_options": len(opts),
            "n_concepts": int(F.shape[0]),
            "n_distinct_fit_vectors": int(uniq.shape[0]),
            "distinct_fraction": float(uniq.shape[0] / F.shape[0]),
            "mean_within_concept_fit_range": float((F.max(1) - F.min(1)).mean()),
            "pool_existence_rate": float(pool_tile_rate[t]),
            "frozen_finite_rate": float(fin[tiles == t].mean()),
        }
    r = pool_tile_rate
    within3 = abs(r["manmade"] - r["moves"])
    between34 = abs(r["hold"] - max(r["manmade"], r["moves"]))
    order = list(TILES)
    y = [rows[t]["pool_existence_rate"] for t in order]

    def rank_order(key):
        return [t for t in sorted(order, key=lambda t: rows[t][key])]

    return {
        "status": "EXPLORATORY. Spec v3.1 section 7.2 assigns the mechanism "
                  "question here and states no prediction.",
        "outcome_variable": "per-tile pool existence rate |D(inf)|/N (Step 1)",
        "per_tile": rows,
        "within_O3_spread_pool": float(within3),
        "O3_to_O4_step_pool": float(between34),
        "within_exceeds_between": bool(within3 > between34),
        "frozen_rate_range": [float(min(rows[t]["frozen_finite_rate"] for t in order)),
                              float(max(rows[t]["frozen_finite_rate"] for t in order))],
        "tile_order_by_pool_rate": rank_order("pool_existence_rate"),
        "tile_order_by_n_options": rank_order("n_options"),
        "tile_order_by_distinct_fraction": rank_order("distinct_fraction"),
        "tile_order_by_fit_range": rank_order("mean_within_concept_fit_range"),
        "distinct_fraction_reproduces_rate_order": bool(
            rank_order("distinct_fraction") == rank_order("pool_existence_rate")),
        "n_options_reproduces_rate_order": bool(
            rank_order("n_options") == rank_order("pool_existence_rate")),
        "caveat": "Four tiles. This is an ordering check, not evidence: with four "
                  "points a rank statistic takes five values and separates nothing, "
                  "and `distinct_fraction` is a tile-level constant, so it cannot be "
                  "told apart from any other tile-level covariate on this design. "
                  "It is reported because it is the first candidate that reproduces "
                  "the ordering `|O|` fails to, and because it is falsifiable on a "
                  "signal space with more tiles.",
    }


# -------------------------------------------------------------- step 5, plots
def figures(frame, pool, pool_rates, frozen_rates):
    """Three figures. The beta_c = infinity mass is drawn in every one of them."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    os.makedirs(FIGDIR, exist_ok=True)
    bc = frame["beta_c"].values
    fin = np.isfinite(bc)
    paths = []

    # 1. |D(beta)| / N versus beta, both bases, with the infinity anchor drawn as
    #    a separate point at a break in the axis rather than at a large finite x.
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    xs = list(range(len(GRID)))            # the grid is equally spaced by index;
    x_inf = len(GRID) + 0.8                # a linear beta axis collides 0/.25/.5
    for rates, label, style in ((pool_rates, "200k candidate pool (K1 gate base)", "o-"),
                                (frozen_rates, "frozen 1,000 (Arm A base)", "s-")):
        ys = [rates[b]["pooled"] for b in GRID]
        line, = ax.plot(xs, ys, style, label=label)
        ax.plot([x_inf], [rates[math.inf]["pooled"]], style[0],
                color=line.get_color(), markersize=9, markerfacecolor="none")
        ax.plot([xs[-1], x_inf], [ys[-1], rates[math.inf]["pooled"]], ":",
                color=line.get_color(), linewidth=1)
    ax.axvline(len(GRID) - 0.4, color="0.6", linewidth=0.8)
    ax.axhline(K1_THRESHOLD, color="crimson", linestyle="--", linewidth=1)
    ax.text(0.05, K1_THRESHOLD + 0.008, "K1 threshold 0.10", color="crimson", fontsize=8)
    ax.set_xticks(xs + [x_inf])
    ax.set_xticklabels([f"{b:g}" for b in GRID] + [r"$\infty$"])
    ax.set_xlabel(r"persuasion budget $\beta$, on the reporting grid (equally spaced,"
                  "\n" r"not linear in $\beta$; the $\infty$ anchor is past the rule)")
    ax.set_ylabel(r"$|D(\beta)|\,/\,N$")
    ax.set_title(r"Divergence rate against $\beta$." "\n"
                 r"$D(0)=\emptyset$ by convention (spec 7.1); the $\infty$ point is a"
                 " separate anchor, not a limit of the curve.", fontsize=9)
    ax.legend(fontsize=8, loc="center right")
    ax.set_ylim(0, max(0.5, frozen_rates[math.inf]["pooled"] * 1.15))
    fig.tight_layout()
    paths.append(f"{FIGDIR}/T6_divergence_curve.png")
    fig.savefig(paths[-1], dpi=160)
    plt.close(fig)

    # 2 and 3. Both quantities are conditional on membership, so both figures
    #    show the mass to scale in a stacked bar and the conditional distribution
    #    on its own axis below it. A shared count axis was tried first and buries
    #    the distribution under the 540-item mass; splitting the two jobs shows
    #    both without dropping either.
    def mass_and_hist(values, n_mass, mass_label, color, title, xlabel, mark=None,
                      second=None):
        rows = 2 if second is None else 3
        fig = plt.figure(figsize=(8.2, 5.0 if second is None else 6.8))
        gs = fig.add_gridspec(rows, 1, height_ratios=[1] + [3.4] * (rows - 1),
                              hspace=0.75)
        top, bot = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
        n_val, total = len(values), len(values) + n_mass
        top.barh([0], [n_val], color=color, edgecolor="white")
        top.barh([0], [n_mass], left=n_val, color="#cc6677", edgecolor="white")
        top.text(n_val / 2, 0, f"{n_val} ({n_val/total:.1%})", ha="center",
                 va="center", color="white", fontsize=9, fontweight="bold")
        top.text(n_val + n_mass / 2, 0, f"{n_mass} ({n_mass/total:.1%})",
                 ha="center", va="center", color="white", fontsize=9,
                 fontweight="bold")
        top.set_xlim(0, total); top.set_yticks([])
        top.set_xlabel(f"items, to scale, all {total:,}", fontsize=8)
        top.set_title(f"{title}   |   {mass_label}", fontsize=9)
        for sp in ("top", "right", "left"):
            top.spines[sp].set_visible(False)
        bot.hist(values, bins=45, color=color, edgecolor="white", linewidth=0.4)
        bot.set_xlabel(xlabel); bot.set_ylabel("items")
        bot.set_title(f"the {n_val} shown in colour above, on their own count axis",
                      fontsize=9)
        bot.spines[["top", "right"]].set_visible(False)
        if mark:
            for x, lab in mark:
                bot.axvline(x, color="0.35", linestyle="--", linewidth=1)
                bot.text(x, bot.get_ylim()[1] * 0.93, "  " + lab, fontsize=8,
                         color="0.25")
        if second is not None:
            vals2, xlabel2, title2, mark2 = second
            ax2 = fig.add_subplot(gs[2])
            ax2.hist(vals2, bins=45, color=color, edgecolor="white", linewidth=0.4)
            ax2.set_xlabel(xlabel2); ax2.set_ylabel("items")
            ax2.set_title(title2, fontsize=9)
            ax2.spines[["top", "right"]].set_visible(False)
            for x, lab in mark2:
                ax2.axvline(x, color="0.35", linestyle="--", linewidth=1)
                ax2.text(x, ax2.get_ylim()[1] * 0.93, "  " + lab, fontsize=8,
                         color="0.25")
        return fig

    n_zero = int((bc == 0).sum())
    fig = mass_and_hist(
        bc[fin], int((~fin).sum()),
        r"adversary-robust, $\beta_c=\infty$", "#4477aa",
        r"finite $\beta_c$" + (f", $\\beta_c=0$ on {n_zero} (boundary-tied)"
                               if n_zero else ""),
        r"$\beta_c$", mark=[(8.0, "grid endpoint 8")])
    fig.suptitle(r"$\beta_c$ on the frozen 1,000. The $\infty$ mass is shown to"
                 " scale, not dropped.", fontsize=10, y=0.99)
    paths.append(f"{FIGDIR}/T6_beta_c_distribution.png")
    fig.savefig(paths[-1], dpi=160, bbox_inches="tight")
    plt.close(fig)

    D = frame["in_divergence_set"].values
    pr = frame["price_of_robustness"].values
    pnp = (frame["post_norm_at_o0"].values
           - frame["post_norm_at_oinf"].values)[D]
    fig = mass_and_hist(
        pr[D], int((~D).sum()),
        r"adversary-robust, price $=0$ exactly ($o^*_0=o^*_\infty$)", "#228833",
        "divergence set", r"raw:  $L(h^*|o^*_0) - L(h^*|o^*_\infty)$",
        mark=[(float(pr[D].mean()), f"mean {pr[D].mean():.4f}")],
        second=(pnp,
                r"PRIMARY, on P1's $post\_norm$ (D47):  "
                r"$pn(o^*_0) - pn(o^*_\infty)$",
                "the same items, as a share of the item's own posterior range",
                [(float(pnp.mean()), f"mean {pnp.mean():.4f}")]))
    fig.suptitle("Price of robustness: posterior mass on the truth given up to buy"
                 " margin.\nFrozen 1,000. The robust items' exact zero is shown to"
                 " scale, not dropped.", fontsize=10, y=1.0)
    paths.append(f"{FIGDIR}/T6_price_of_robustness.png")
    fig.savefig(paths[-1], dpi=160, bbox_inches="tight")
    plt.close(fig)
    return paths


# ------------------------------------------------------------------- report
def write_report(rec, num, frame, figs, secs):
    L = []
    w = L.append
    g = num["step2"]
    s3 = num["step3"]
    s4 = num["step4"]

    w("# T6: Arm A. The K1 kill gate and the `beta_c` characterisation\n\n")
    w(f"Generated by `python3 src/t6_arm_a.py` on {time.strftime('%Y-%m-%d')}. "
      f"Deterministic, no seed enters any quantity. Spec `{adv.SPEC_VERSION}`. "
      f"No language model was run.\n\n")
    w("**Item bases, which this script did not choose.** Step 1 runs on the full "
      "unstratified 200,000-candidate pool (v2.0 section 2, section 7.1). Steps 2 "
      "through 5 run on P1's frozen `items_final.parquet`, all 1,000 items, all "
      "four tiles: v2.1 section 1.3 fixes Arm A's base as \"T2's frozen item set\" "
      "and v2.2 section 1.1 fixes what that resolves to now that K2 has fired. "
      "Restriction to the `size` tile is Arm B's (v2.3 section 3) and does not "
      "reach Arm A. Where a pool figure is cheap because Step 1 computes it "
      "anyway it is reported beside the frozen-set figure and labelled.\n\n")

    # ---- Step 1
    rr = num["rate_claim_rule"]
    w("**Which base a rate claim uses.** The pool rate is a property of the "
      "signal space. The frozen rate is a property of P1's 50/50 conflict quota. "
      "Any claim of the form \"X% of items diverge\" therefore uses the **pool** "
      f"figure: **{rr['population_existence_rate']:.4f}** existence, "
      f"**{rr['population_grid_rate']:.4f}** at the grid endpoint. The frozen "
      f"set's {rr['frozen_set_rate_at_grid_endpoint']:.4f} at the endpoint and "
      f"{rr['frozen_set_existence_rate']:.4f} existence are reported only as the "
      "Arm A base's own rates, never as population statements. This applies to "
      "the divergence rate, the existence rate, the grid rate, the per-tile "
      "rates, and the share of items above the grid endpoint. It is a labelling "
      f"rule, not a recomputation, and it is emitted to `{NUMBERS}` under "
      "`rate_claim_rule` so a downstream task does not have to re-derive it.\n\n")
    of = num["step3"]["conventions"]["o_star_infinity_is_o_fit"]
    sp = num["step3"]["spike_at_one"]
    w("---\n\n## Primary findings\n\n")
    w(f"1. **The kill gate passes.** `|D(infinity)| / N` = "
      f"{rec['pooled_existence_rate']:.4f} on the 200,000-candidate pool against a "
      f"threshold of {K1_THRESHOLD:.2f}. The adversary effect exists in this "
      f"signal space and the reporting grid reaches it. Arms B and C may run.\n\n")
    w(f"2. **Robustness against an informed adversary requires abandoning Bayesian "
      f"discrimination entirely and reverting to the salient signal.** "
      f"`o*_infinity` is P1's `o_fit` on **{of['n']} of {of['n_total']}** divergent "
      f"items in the frozen set ({of['share']:.4f}) and on "
      f"{num['step3']['pool_robustness_check']['conventions']['o_star_infinity_is_o_fit']['share']:.4f} "
      f"of the pool's {num['step3']['pool_robustness_check']['n_divergence_set_pool']:,}. "
      f"Measured on P1's own frontier coordinate the price of robustness is "
      f"exactly the whole salience-to-Bayes interval, on every item where that "
      f"coordinate is defined. The Scientist who buys margin walks from the Bayes "
      f"pole to the salience pole and stops there.\n\n")
    w(f"   The {sp['n']}-item spike at a normalised price of exactly 1 is the "
      f"extreme tail of the same phenomenon: there the robust option is the item's "
      f"**lowest**-posterior option, {sp['per_tile'].get('manmade', 0)} of "
      f"{sp['n']} on `manmade`, at mean `fit_cost` {sp['mean_fit_cost']:.4f} "
      f"against {sp['mean_fit_cost_rest']:.4f} on the rest of the divergence "
      f"set.\n\n")
    w("   **The relation to Paper 1, stated narrowly.** Paper 1's finding is about "
      "where language models sit relative to the salience-Bayes interval. This is "
      "about where the normative optimum moves inside it, on the same coordinate, "
      "with no model involved. The two are adjacent, not the same claim, and "
      "nothing in this report measures a model.\n\n")
    w(f"3. **The price of robustness is {num['step3']['conventions']['p1_post_norm']['mean_of_per_item_ratios']:.4f} "
      f"of the item's own posterior range** on P1's `post_norm`, the primary DV "
      f"(Step 3).\n\n")
    w("4. **Existence and magnitude come apart across tiles.** The per-tile "
      f"existence rate spans a factor of "
      f"{s4['existence_vs_magnitude']['existence_rate_max_over_min']:.1f}; the "
      f"median budget needed once an item diverges spans "
      f"{s4['existence_vs_magnitude']['median_beta_c_max_over_min_pool']:.2f} "
      "(Step 4, exploratory).\n\n")
    w("---\n\n## Step 1. K1, the kill gate\n\n")
    w("**Status: reproduction check.** K1's statistic was computed by T1 as a "
      "byproduct and disclosed in v2.1 section 1.2 before T6 ran. This run "
      "recomputes it on the same base with the same code. A discrepancy would be "
      "a bug in one of the two runs, not a new gate.\n\n")
    w("```\n"
      f"existence rate   |D(infinity)| / N = {rec['pooled_existence_rate']:.4f}   "
      f"({int(round(rec['pooled_existence_rate']*rec['N'])):,} / {rec['N']:,})\n"
      f"grid rate        |D(8)| / N        = {rec['pooled_grid_rate']:.4f}\n"
      f"threshold        {K1_THRESHOLD:.2f}, on the EXISTENCE rate (v2.0 section 7.1)\n"
      f"item base        full unstratified 200,000-candidate pool\n"
      f"outcome          {rec['outcome']}, {rec['outcome_text']}\n```\n\n")
    ok = rec["reproduction"]
    w(f"Reproduction: published values matched to 4 decimals: "
      f"**{'yes' if ok['published_matched'] else 'NO'}**. `beta_c` bit-for-bit "
      f"identical to T2's stored `{POOL_TABLE}` over all {rec['N']:,} items: "
      f"**{'yes' if ok['bitwise_identical_to_T2_pool_table'] else 'NO'}**.\n\n")
    if ok["problems"]:
        w("**MISMATCHES:**\n\n" + "".join(f"- {p}\n" for p in ok["problems"]) + "\n")

    w("### Per-tile rates and spec section 7.2's disambiguation\n\n")
    w("| tile | `\\|O\\|` | `\\|D(inf)\\|/N` | `\\|D(8)\\|/N` | published `\\|D(inf)\\|/N` |\n")
    w("|---|---:|---:|---:|---:|\n")
    for t in TILES:
        w(f"| `{t}` | {rec['tile_n_options'][t]} | "
          f"{rec['per_tile_existence_rate'][t]:.4f} | "
          f"{rec['per_tile_grid_rate'][t]:.4f} | "
          f"{PUBLISHED['pool_tile_existence'][t]:.4f} |\n")
    w(f"\nVerdict at `beta = infinity`, the anchor the preregistration's gate "
      f"decides on: **{rec['disambiguation_verdict']}** "
      f"(`r_size - min(r_manmade, r_moves)` = {rec['disambiguation_gap']:+.4f}, "
      f"criterion {STRUCTURAL_GAP:.2f}). At spec section 7.2's own anchor of "
      f"`beta = 8`: **{rec['disambiguation_verdict_at_beta_8']}** "
      f"({rec['disambiguation_gap_at_beta_8']:+.4f}).\n\n")
    w("The anchor mismatch is a known open item (v2.0 Appendix A.2 item 7) and is "
      "not resolved here. It does not bite: the pooled existence rate passes, and "
      "per v2.0 section 7.1 the per-tile clean-negative reading is available only "
      "when the pooled rate has itself failed. The `structural / inconclusive` "
      "verdict is recorded because the criterion is met on the numbers, and it is "
      "inert on a passing gate. Note also that the rates are not monotone in "
      "`|O|` (`moves` at 3 exceeds `hold` at 4), so `|O|` is not the driver the "
      "criterion assumes; that is v2.1 section 2.2's correction and it sends the "
      "mechanism question to Step 4.\n\n")
    w(f"**Kill gate: {'PASSED' if rec['outcome'] == 2 else 'see outcome above'}.** "
      f"{rec['pooled_existence_rate']:.4f} of the 200,000-candidate pool has a "
      f"finite `beta_c`, against a threshold of {K1_THRESHOLD:.2f}. The adversary "
      f"effect exists in this signal space and the reporting grid reaches it "
      f"({rec['pooled_grid_rate']:.4f} at `beta = 8`), so no grid extension is "
      f"triggered. Arms B and C may run.\n\n")
    w(f"Machine-readable gate record: `{GATE_RECORD}`. T7 and T8 read that file, "
      "not this one.\n\n")

    # ---- Step 2
    w("---\n\n## Step 2. `beta_c` on the frozen 1,000\n\n")
    w(f"Finite on **{g['n_finite']}** of {g['N']} items "
      f"({g['finite_rate']:.4f}), infinite on **{g['n_infinite']}** "
      f"({1-g['finite_rate']:.4f}). Exactly zero on {g['n_beta_c_exactly_zero']} "
      f"(boundary-tied, spec section 7.1: these sit in `D(beta)` for every "
      f"`beta > 0` and in `D(0)` for none). Above the grid endpoint of 8 on "
      f"{g['n_finite_above_grid_endpoint']}.\n\n")
    w(f"The frozen set's finite rate of {g['finite_rate']:.4f} is **sampler-"
      f"dependent** and is not a prevalence estimate. It sits above the pool's "
      f"{rec['pooled_existence_rate']:.4f} because P1's draw is 50% conflict "
      f"items, a quota fixed in `final_items.py` before `beta_c` existed as a "
      f"quantity (v2.2 section 1.3, recorded there as benign enrichment).\n\n")
    q = g["finite_percentiles"]
    w("Percentiles of the finite part:\n\n| " + " | ".join(f"p{k}" for k in q)
      + " |\n|" + "---:|" * len(q) + "\n| "
      + " | ".join(f"{v:.4f}" for v in q.values()) + " |\n\n")
    w(f"Mean {g['finite_mean']:.4f}, sd {g['finite_sd']:.4f}.\n\n")

    w("### Growth of `|D(beta)|`\n\n")
    w("| `beta` | frozen `\\|D\\|/N` | frozen `\\|D\\|` | pool `\\|D\\|/N` |\n|---|---:|---:|---:|\n")
    for b in list(GRID) + [math.inf]:
        fr = g["divergence_curve_frozen"][str(b)]["pooled"]
        po = g["divergence_curve_pool"][str(b)]["pooled"]
        w(f"| {'inf' if b == math.inf else f'{b:g}'} | {fr:.4f} | "
          f"{int(round(fr*g['N']))} | {po:.4f} |\n")
    w("\n`D(0)` is empty by convention and is a fixed anchor, not the curve's limit "
      "as `beta -> 0+` (spec section 7.1).\n\n")
    f8, finf = (g["divergence_curve_frozen"]["8.0"]["pooled"],
                g["divergence_curve_frozen"]["inf"]["pooled"])
    p8, pinf = (rec["pooled_grid_rate"], rec["pooled_existence_rate"])
    w(f"Two things the shape says. The curve is **steep between `beta = 1` and "
      f"`beta = 8`**, not flat: on the frozen set it goes {g['divergence_curve_frozen']['1.0']['pooled']:.4f} "
      f"-> {g['divergence_curve_frozen']['4.0']['pooled']:.4f} -> {f8:.4f}, with a "
      f"median finite `beta_c` of {g['finite_percentiles'][50]:.4f}, so the typical "
      f"divergent item needs a budget of two to four rather than a marginal one. "
      f"And it is **nearly saturated at the grid endpoint**: {f8:.4f} of a limit of "
      f"{finf:.4f} on the frozen set, {p8:.4f} of {pinf:.4f} on the pool, leaving "
      f"{g['n_finite_above_grid_endpoint']} frozen-set items with a finite `beta_c` "
      f"above 8. The grid endpoint of 8 is a reporting convention (spec section "
      f"8.2, awaiting author confirmation), and this is the number that says how "
      f"much it costs: about {100*(finf-f8)/finf:.1f}% of the divergence set on the "
      f"frozen set. That is the substantive reading of outcome 2.\n\n")
    w("Per tile on the frozen set: "
      + ", ".join(f"`{t}` {g['per_tile_finite_count'][t]}/"
                  f"{int(round(g['per_tile_finite_count'][t]/g['per_tile_finite_rate'][t]))} "
                  f"= {g['per_tile_finite_rate'][t]:.4f}" for t in TILES) + ".\n\n")

    k2 = g["K2"]
    w("### K2, the `fit_cost` correlation gate: reproduction\n\n")
    w("```\n"
      f"rho_Spearman(beta_c, fit_cost) = {k2['spearman_pool']:+.4f}   "
      f"published {k2['published']:+.4f}\n"
      f"threshold  |rho| >= {K2_THRESHOLD:.2f}      outcome  "
      f"{'FIRES' if k2['fires'] else 'does not fire'}\n"
      f"item base  {k2['item_base']}\n```\n\n")
    w("K2 fired in T2 and v2.2 section 1.1 applied its consequence: the "
      "`beta_c`-stratified redraw does not happen. This is a reproduction check "
      "with the standing v2.1 section 1.3 gives T6's K1 run. It is not a fresh "
      "gate and does not reopen the outcome. K2's item base is the pool, fixed in "
      "v2.0 section 7.1, so it stays on the pool even though the rest of Step 2 is "
      "on the frozen set.\n\n")
    w(f"Descriptive, not the gate: Pearson on the pool's finite-`beta_c` subset "
      f"{k2['pearson_finite_subset_pool']:+.4f}; Spearman on the frozen set "
      f"{k2['spearman_frozen_set_descriptive']:+.4f}; Pearson on the frozen set's "
      f"finite subset {k2['pearson_frozen_finite_descriptive']:+.4f}.\n\n")

    c = g["three_optima_coincidence"]
    w("### The three optima coincide together, confirmed on Arm A's base\n\n")
    w("The T2 session observed this as a byproduct of the gate computation and "
      "asked T6 to confirm it on Arm A's own item base. Confirmed:\n\n")
    w("| conditioned on | N | robust share (frozen) | robust share (pool) |\n|---|---:|---:|---:|\n")
    for k, label in (("fit_cost_zero", "`fit_cost = 0` (non-conflict)"),
                     ("fit_cost_positive", "`fit_cost > 0` (conflict)")):
        w(f"| {label} | {c[k]['N']} | {c[k]['robust_share']:.4f} | "
          f"{c['pool_check'][k]['robust_share']:.4f} |\n")
    w(f"| marginal | {g['N']} | {c['marginal_robust_share']:.4f} | "
      f"{1-rec['pooled_existence_rate']:.4f} |\n\n")
    w(f"The two rows differ by {abs(c['gap_in_robust_share_points']):.1f} percentage "
      f"points on the frozen set. Independence would put both near the marginal. "
      f"`fit_cost = 0` says the salience optimum and the Bayes optimum coincide; "
      f"`beta_c = infinity` says the Bayes optimum and the margin optimum coincide. "
      f"They share one term and neither implies the other, so the concentration is "
      f"substantive: {100*c['share_of_finite_that_are_conflict']:.1f}% of the "
      f"frozen set's divergent items are P1 conflict items. Outside P1's conflict "
      f"set the optimal signal is already margin-maximizing and no persuasion "
      f"budget moves it.\n\n")

    # ---- Step 3
    cv = s3["conventions"]
    rl = cv["reference_levels"]
    dg = cv["degeneracies"]
    of = cv["o_star_infinity_is_o_fit"]
    w("---\n\n## Step 3. The price of robustness\n\n")
    w("`L(h*|o*_0) - L(h*|o*_infinity)`: the posterior mass on the truth the "
      "Scientist gives up to buy margin against an informed adversary. Computed "
      f"over the divergence set of the frozen 1,000, {s3['n_divergence_set']} "
      "items.\n\n")
    w(f"**Bug check first (v2.0 H-A).** Negative values: **{s3['n_negative']}**. "
      f"Non-negativity follows from `o*_0` being the posterior argmax, so any "
      f"negative value would be an implementation bug rather than a finding; the "
      f"script raises instead of reporting one. Exactly zero on "
      f"{s3['n_exactly_zero']} items, of which "
      f"{s3['n_exactly_zero_and_boundary_exact']} carry P1's `boundary_exact` flag "
      f"({s3['n_boundary_exact_in_D']} `boundary_exact` items are in the "
      f"divergence set at all).\n\n")
    q = s3["percentiles"]
    w("The raw difference, which is the quantity the specification defines:\n\n")
    w("| " + " | ".join(f"p{k}" for k in q) + " |\n|" + "---:|" * len(q) + "\n| "
      + " | ".join(f"{v:.4f}" for v in q.values()) + " |\n\n")
    w(f"Mean {s3['mean']:.4f}, sd {s3['sd']:.4f}.\n\n")

    w("### Against what reference\n\n")
    w("A raw difference of posterior masses is not interpretable on its own, and "
      "the reference is not this session's to invent. P1 already normalises this "
      "exact axis, twice, and both of its conventions are used here. Every "
      f"denominator is emitted to `{NUMBERS}`; none is read off prose.\n\n")
    w(f"The item posterior is over `|H|` = {int(round(1/cv['prior_floor_1_over_H']))} "
      f"hypotheses with a uniform prior, so `1/|H|` = "
      f"{cv['prior_floor_1_over_H']:.4f} of any `L(h*|o)` is a prior floor the "
      f"signal did not earn. Mean `L(h*|o*_0)` over the divergence set is "
      f"{rl['mean_L_at_o0']:.4f}, of which {rl['mean_L_at_o0_above_prior']:.5f} is "
      f"above that floor; mean `L(h*|o*_infinity)` is {rl['mean_L_at_oinf']:.4f}, "
      f"of which {rl['mean_L_at_oinf_above_prior']:.5f} is.\n\n")
    w("| convention | denominator | mean of per-item ratios | ratio of means | median | n | undefined |\n")
    w("|---|---|---:|---:|---:|---:|---:|\n")
    order = [("p1_post_norm", "**P1 `post_norm`, D47** (PRIMARY)",
              r"`max_o L(h*\|o) - min_o L(h*\|o)`"),
             ("above_prior", "above the prior floor", r"`L(h*\|o*_0) - 1/\|H\|`"),
             ("raw_share_of_total_mass", "total posterior mass", r"`L(h*\|o*_0)`"),
             ("p1_salience_bayes", "P1 salience-Bayes span (degenerate, below)",
              "`1 - post_norm(o_fit)`")]
    for k, label, den in order:
        v = cv[k]
        w(f"| {label} | {den} | "
          f"{v['mean_of_per_item_ratios']:.4f} | {v['ratio_of_means']:.4f} | "
          f"{v['median']:.4f} | {v['n']} | {v['n_undefined']} |\n")
    pnc = cv["p1_post_norm"]
    w(f"\n**The headline number is {pnc['mean_of_per_item_ratios']:.4f}**, on P1's "
      f"`post_norm`. That is the right denominator for three reasons and not "
      f"because of its value: it is the coordinate P1 already divides this axis "
      f"by (D47, `tiebreak.norm`, whose raw range is the frozen "
      f"`frontier_ext_post` column, matched here to "
      f"{rec['pool_posterior_range_vs_frozen_frontier_ext_post_max_abs_diff']:.1e}); "
      f"it is P1's primary DV and the coordinate Arm B is scored on, so Arm A and "
      f"Arm B stay on one scale; and it is bounded in [0, 1] with no degeneracy "
      f"beyond P1's own EPS rule. Read: **the Scientist surrenders about "
      f"{100*pnc['mean_of_per_item_ratios']:.0f}% of the posterior range its own "
      f"option set spans.**\n\n")
    ap = cv["above_prior"]
    w(f"The above-prior reference gives "
      f"{ap['mean_of_per_item_ratios']:.4f} as a mean of per-item ratios and "
      f"{ap['ratio_of_means']:.4f} as a ratio of means. The two differ because "
      f"the denominator `L(h*|o*_0) - 1/|H|` falls as low as "
      f"{dg['min_above_prior_denominator']:.2e}. Both are reported and neither is "
      f"the headline, because `1/|H|` is not a reference P1 uses; it is the "
      f"correct observation that the raw share of total mass "
      f"({cv['raw_share_of_total_mass']['mean_of_per_item_ratios']:.4f}) counts "
      f"the prior floor as earned, and it is reported for that reason.\n\n")
    w(f"**Not clipped:** on {dg['n_L_at_oinf_at_or_below_prior']} of "
      f"{s3['n_divergence_set']} divergent items the margin-optimal signal leaves "
      f"`L(h*|o*_infinity)` at or below the prior floor, so the above-prior ratio "
      f"exceeds 1 on {dg['n_above_prior_ratio_exceeding_1']} items. Those are the "
      f"items where the robust choice surrenders more than the signal earned. "
      f"They are kept, and they are why that column's mean of ratios sits above "
      f"its ratio of means.\n\n")

    w("### P1's salience-Bayes coordinate is degenerate here, and the reason is a finding\n\n")
    w(f"On **{of['n']} of {of['n_total']}** divergent items "
      f"({of['share']:.4f}), `o*_infinity` is P1's `o_fit`: **the "
      f"margin-maximizing signal is the salience-maximizing signal.** These are "
      f"different functions and this is not an identity, since "
      f"{of['n_exceptions']} exceptions exist, but all "
      f"{of['n_exceptions_removed_by_p1_span_guard']} of them fall inside the "
      f"{dg['n_salience_span_at_or_below_guard']} items P1's own `span > "
      f"{SB_MIN_SPAN}` guard removes. So on all {of['sb_defined']} items "
      f"where the frontier coordinate is defined, `sb(o*_infinity)` is exactly "
      f"zero: {of['sb_at_oinf_exactly_zero']} of {of['sb_defined']}. The price is "
      f"therefore 1, up to a shortfall of "
      f"{of['sb_price_max_shortfall_from_one']:.1e} on the "
      f"{dg['n_post_norm_at_o0_below_one']} items where `post_norm(o*_0)` is "
      f"itself 1 only to float rounding.\n\n")
    w("Two consequences, and they point in opposite directions. As a denominator "
      "the coordinate is useless for this quantity: a constant carries no "
      "distributional information, which is why the primary is `post_norm` and "
      "not this. As a result it is the sharpest sentence in Step 3: **buying "
      "margin against an informed adversary walks the entire salience-to-Bayes "
      "interval, from the Bayes pole to the salience pole.** Paper 1's finding "
      "concerns where language models sit relative to that interval; this is a "
      "statement about where the normative optimum moves inside it, on the same "
      "coordinate. The two are adjacent, not the same claim, and nothing here "
      "measures a model.\n\n")

    w("### Per tile\n\n| tile | n | raw mean | raw median | raw p90 | `post_norm` mean |\n")
    w("|---|---:|---:|---:|---:|---:|\n")
    for t in TILES:
        r = s3["per_tile"][t]
        w(f"| `{t}` | {r['n']} | {r['mean']:.4f} | {r['median']:.4f} | "
          f"{r['p90']:.4f} | {r['p1_post_norm_mean']:.4f} |\n")
    pt = s3["per_tile"]
    sp = s3["spike_at_one"]
    w(f"\nThe raw means are close across tiles ({min(pt[t]['mean'] for t in TILES):.4f} "
      f"to {max(pt[t]['mean'] for t in TILES):.4f}) while the normalised ones are "
      f"not ({min(pt[t]['p1_post_norm_mean'] for t in TILES):.4f} to "
      f"{max(pt[t]['p1_post_norm_mean'] for t in TILES):.4f}, `manmade` highest). "
      f"The figure shows why: a spike of **{sp['n']}** items at a normalised price "
      f"of exactly 1, where `o*_infinity` is the item's **lowest**-posterior "
      f"option. All {sp['n']} have `o*_infinity = o_fit`, their mean `fit_cost` is "
      f"{sp['mean_fit_cost']:.4f} against {sp['mean_fit_cost_rest']:.4f} on the "
      f"rest of the divergence set, and "
      f"{sp['per_tile'].get('manmade', 0)} of {sp['n']} are `manmade`. So the "
      f"tile gap in the normalised column is carried by a small set of "
      f"high-`fit_cost` items where the robust choice is the worst available "
      f"signal by posterior, not by a shift in the bulk. It is a corner of the "
      f"signal space, not a numerical artifact, and it is not dropped.\n\n")
    w(f"On the {g['n_infinite']} adversary-robust items the price is exactly zero "
      f"by construction (`o*_0 = o*_infinity`); the maximum over that set is "
      f"{s3['robust_items_price_max']:.1e}, confirming it.\n\n")

    # ---- Step 3 robustness check
    rb = s3["pool_robustness_check"]
    w("### Robustness: the same price on the pool's divergence set\n\n")
    w(f"The price above is conditional on divergence, computed on an item base "
      f"that is {rb['conflict_share_frozen']:.0%} conflict against the pool's "
      f"{rb['conflict_share_pool']:.4f}. Conditioning may or may not remove that "
      f"enrichment's effect, and it was untested. It is cheap to test, because "
      f"Step 1's pass over the pool already builds every column it needs, so the "
      f"whole distribution is recomputed on the pool's "
      f"{rb['n_divergence_set_pool']:,}-item divergence set. Descriptive, not a "
      f"second estimate.\n\n")
    w("| | frozen 1,000 | 200k pool | difference |\n|---|---:|---:|---:|\n")
    w(f"| conflict share of the item base | {rb['conflict_share_frozen']:.4f} | "
      f"{rb['conflict_share_pool']:.4f} | "
      f"{rb['conflict_share_frozen'] - rb['conflict_share_pool']:+.4f} |\n")
    w(f"| conflict share **within** the divergence set | "
      f"{rb['conflict_share_within_divergence_set_frozen']:.4f} | "
      f"{rb['conflict_share_within_divergence_set_pool']:.4f} | "
      f"{rb['conflict_share_within_divergence_set_frozen'] - rb['conflict_share_within_divergence_set_pool']:+.4f} |\n")
    w(f"| raw mean price | {cv['raw_difference']['mean']:.6f} | "
      f"{rb['conventions']['raw_difference']['mean']:.6f} | "
      f"{rb['raw_mean_frozen_minus_pool']:+.6f} |\n")
    for k, label, _den in order[:3]:
        w(f"| {label.replace('**','').replace(' (PRIMARY)','')} | "
          f"{cv[k]['mean_of_per_item_ratios']:.4f} | "
          f"{rb['conventions'][k]['mean_of_per_item_ratios']:.4f} | "
          f"{rb['frozen_minus_pool'][k]:+.4f} |\n")
    w(f"\nThe enrichment largely washes out under conditioning, which is the "
      f"result the check was run to establish rather than to assume. The two "
      f"bases differ by {abs(rb['conflict_share_frozen'] - rb['conflict_share_pool']):.4f} "
      f"in conflict share overall but only "
      f"{abs(rb['conflict_share_within_divergence_set_frozen'] - rb['conflict_share_within_divergence_set_pool']):.4f} "
      f"within the divergence set, because divergence is itself concentrated in "
      f"conflict items (Step 2). On the primary convention the frozen figure sits "
      f"{abs(rb['frozen_minus_pool']['p1_post_norm']):.4f} above the pool's "
      f"{rb['conventions']['p1_post_norm']['mean_of_per_item_ratios']:.4f}. Where "
      f"the price appears as a population statement, the pool figure is the one "
      f"to use.\n\n")

    # ---- Step 4
    w("---\n\n## Step 4. What predicts a low `beta_c`. EXPLORATORY\n\n")
    w("**Exploratory throughout.** v2.0 section 10 lists \"what predicts a low "
      "`beta_c` (T6 Step 4), and any regression of `beta_c` on item properties\" "
      "as exploratory. There is no preregistered prediction and no threshold. No "
      "p-value below is a test.\n\n")
    ic = s4["identity_check"]
    w(f"**First, what is not a finding.** `beta_c` is finite exactly when "
      f"`o*_0 != o*_infinity`. Verified on all {g['N']} items: "
      f"`{ic['exact_identity_o0_ne_oinf_equals_finite']}`. Any predictor of "
      f"*finiteness* that is a function of the margin gap between those two "
      f"options restates the definition, so margin headroom is used below only "
      f"among finite items, where its magnitude is not implied by membership.\n\n")
    w(f"**A float-level discrepancy, surfaced rather than hidden.** The raw sign "
      f"test `headroom > 0` disagrees with finiteness on "
      f"**{ic['n_headroom_sign_exceptions']}** of {g['N']} items. On those, a rival "
      f"exceeds `o*_0`'s margin by less than P1's D51 tie-break tolerance, so the "
      f"tie-break keeps `o*_0`, `beta_c` is infinite, and the float difference is "
      f"nonetheless positive: the largest headroom among adversary-robust items is "
      f"{ic['headroom_max_among_robust']:.1e}, float64 noise on a log-scale "
      f"difference. Nothing is clamped. The identity every other quantity in this "
      f"script rests on is the argmax one, which is exact.\n\n")
    w("Rank correlation of `beta_c` with each item property, finite subset "
      f"(n = {g['n_finite']}). Negative means the property goes with a *cheaper* "
      "adversary:\n\n")
    w("| property | Spearman | " + " | ".join(f"`{t}`" for t in TILES) + " |\n|---|---:|"
      + "---:|" * len(TILES) + "\n")
    deg = []
    for k, v in sorted(s4["spearman_beta_c_vs_property_finite_subset"].items(),
                       key=lambda kv: -abs(kv[1]["spearman"] or 0)):
        if v["spearman"] is None:
            w(f"| `{k}` | n/a, {v['note']} | | | | |\n")
            continue
        w(f"| `{k}` | {v['spearman']:+.4f} | "
          + " | ".join("constant" if v["per_tile"][t] is None
                       else f"{v['per_tile'][t]:+.4f}" for t in TILES) + " |\n")
        for t in v.get("constant_on_tiles", []):
            deg.append(f"`{k}` has no variation among `{t}`'s finite-`beta_c` "
                       f"items, so no rank correlation is defined there")
    if deg:
        w("\n" + "".join(f"- {d}. Reported as `constant` rather than filled in.\n"
                         for d in deg))
    o = s4["ols_log_beta_c"]
    w(f"\nOne multivariate fit, OLS on `log beta_c`, n = {o['n']} "
      f"({o['n_excluded_beta_c_zero']} finite items excluded because `beta_c = 0` "
      f"and the log is undefined there; stated rather than absorbed by a shift). "
      f"Continuous predictors standardized, tile dummies with `manmade` as base. "
      f"R-squared {o['r2']:.4f} (adjusted {o['r2_adj']:.4f}).\n\n")
    w("| term | coef | se | t |\n|---|---:|---:|---:|\n")
    for k in sorted(o["coef"], key=lambda k: -abs(o["t"][k])):
        w(f"| `{k}` | {o['coef'][k]:+.4f} | {o['se'][k]:.4f} | {o['t'][k]:+.2f} |\n")
    ev = s4["existence_vs_magnitude"]
    w("\n### Existence and magnitude come apart. EXPLORATORY\n\n")
    w("Recorded as a separate observation from the ordering check below, because "
      "it is a different and stronger statement.\n\n")
    w("| tile | pool `\\|D(inf)\\|/N` | median finite `beta_c`, pool | median finite "
      "`beta_c`, frozen | share of `D` above `beta = 8`, pool | frozen |\n")
    w("|---|---:|---:|---:|---:|---:|\n")
    for t in TILES:
        w(f"| `{t}` | {ev['per_tile_pool_existence_rate'][t]:.4f} | "
          f"{ev['per_tile_median_finite_beta_c_pool'][t]:.4f} | "
          f"{ev['per_tile_median_finite_beta_c_frozen'][t]:.4f} | "
          f"{ev['per_tile_share_of_divergence_set_above_grid_endpoint_pool'][t]:.4f} | "
          f"{ev['per_tile_share_of_divergence_set_above_grid_endpoint_frozen'][t]:.4f} |\n")
    w(f"\nThe existence rate spans a factor of "
      f"**{ev['existence_rate_max_over_min']:.1f}** across the four tiles. The "
      f"median budget needed, conditional on divergence, spans a factor of "
      f"**{ev['median_beta_c_max_over_min_pool']:.2f}** on the pool and "
      f"**{ev['median_beta_c_max_over_min_frozen']:.2f}** on the frozen set. "
      f"**The tiles differ in whether items diverge and barely in how much budget "
      f"is needed once they do.**\n\n")
    w("This is a cleaner mechanism statement than either ordering below. It "
      "separates the existence condition from the magnitude: whatever "
      "distinguishes the tiles acts on whether `o*_0` is already the "
      "margin-maximizer, not on how far apart the two options sit in `beta`. And "
      "unlike a tile-level covariate fitted to four points, it is a claim about "
      "the shape of the `beta_c` distribution inside each tile, so it does not "
      "rest on ordering four numbers.\n\n")
    w(f"It also carries a reporting consequence. The grid endpoint of 8 is "
      f"adequate **per tile**, not only on average: the largest per-tile share of "
      f"a divergence set sitting above it is "
      f"{ev['max_per_tile_share_above_grid_endpoint_pool']:.4f} on the pool. A "
      f"grid adequate on a pooled average could still be short on one tile, and "
      f"this rules that out without extending the grid.\n\n")
    m = s4["mechanism_beyond_n_options"]
    w("\n### The mechanism question `|O|` failed\n\n")
    w(f"`|O|` does not order the divergence rates. On the pool `manmade` gives "
      f"{m['per_tile']['manmade']['pool_existence_rate']:.4f} and `moves` "
      f"{m['per_tile']['moves']['pool_existence_rate']:.4f} at identical `|O| = 3`, "
      f"a within-`|O|=3` spread of {m['within_O3_spread_pool']:.4f} against a "
      f"3-to-4 step of {m['O3_to_O4_step_pool']:.4f} (within exceeds between: "
      f"{m['within_exceeds_between']}). v2.1 section 2.2 named a candidate: each "
      f"tile's rating spread relative to its bin width. That is measurable on P1's "
      f"frozen fit matrices with no new data. A tile whose 1,118 concepts collapse "
      f"onto few distinct fit vectors offers the adversary fewer distinguishable "
      f"options than its `|O|` advertises.\n\n")
    w("**The outcome variable here is the pool rate, and this is the one place in "
      "Steps 2 through 5 where that is so.** It is not a base change. The "
      "between-tile differences the question is about were measured on the pool in "
      "Step 1, and the frozen set's per-tile rates span only "
      f"{m['frozen_rate_range'][0]:.4f} to {m['frozen_rate_range'][1]:.4f} because "
      "P1 drew 250 items per tile under a 50% conflict quota on each. Correlating "
      "a structural covariate against those would read out P1's quota rather than "
      "the signal space. Both columns are shown.\n\n")
    w("| tile | `\\|O\\|` | concepts | distinct fit vectors | distinct frac | "
      "mean fit range | pool `\\|D(inf)\\|/N` | frozen finite rate |\n")
    w("|---|---:|---:|---:|---:|---:|---:|---:|\n")
    for t in TILES:
        r = m["per_tile"][t]
        w(f"| `{t}` | {r['n_options']} | {r['n_concepts']} | "
          f"{r['n_distinct_fit_vectors']} | {r['distinct_fraction']:.4f} | "
          f"{r['mean_within_concept_fit_range']:.4f} | "
          f"{r['pool_existence_rate']:.4f} | {r['frozen_finite_rate']:.4f} |\n")
    w("\nOrdering by pool rate: "
      + " < ".join(f"`{t}`" for t in m["tile_order_by_pool_rate"]) + ". By `|O|`: "
      + " < ".join(f"`{t}`" for t in m["tile_order_by_n_options"])
      + f" (reproduces the rate order: **{m['n_options_reproduces_rate_order']}**). "
      + "By distinct-fit-vector fraction: "
      + " < ".join(f"`{t}`" for t in m["tile_order_by_distinct_fraction"])
      + f" (reproduces it: **{m['distinct_fraction_reproduces_rate_order']}**).\n\n")
    w(f"Neither reproduces the order exactly, and the two failures are not alike. "
      f"`|O|` assigns `manmade` and `moves` the same value while their rates differ "
      f"by a factor of "
      f"{m['per_tile']['moves']['pool_existence_rate'] / m['per_tile']['manmade']['pool_existence_rate']:.1f}, "
      f"which is the failure that prompted the question. The distinct-fraction "
      f"ordering misses only the `moves` / `hold` pair, whose rates differ by "
      f"{abs(m['per_tile']['moves']['pool_existence_rate'] - m['per_tile']['hold']['pool_existence_rate']):.4f} "
      f"and are for practical purposes tied; it does separate `manmade` from the "
      f"other three, which is where the large gap actually is. That is a weaker "
      f"claim than \"the mechanism is bin resolution\" and it is the only one the "
      f"four points support.\n\n")
    w(f"{m['caveat']} The item-level version of the same question is the tile "
      f"dummies in the OLS above, where `tile_size` is the largest of the three "
      f"and still among the weakest terms in the model.\n\n")

    # ---- Step 5
    w("---\n\n## Step 5. Figures\n\n")
    for p in figs:
        w(f"- `{p}`\n")
    w("\nEvery figure shows the `beta_c = infinity` mass. In the divergence curve "
      "it is a separate anchor point past an axis rule, never plotted at a large "
      "finite `beta`. The other two quantities are conditional on membership in "
      "the divergence set, so each figure carries a to-scale stacked bar of the "
      "two group sizes above the conditional distribution: the mass is visible in "
      "proportion, and the distribution is legible on its own count axis. A single "
      "shared count axis was tried first and buries the distribution under the "
      "540-item mass, which shows the mass but hides the result.\n\n")

    # ---- custody
    w("---\n\n## Files and chain of custody\n\n")
    w(f"- `{GATE_RECORD}` machine-readable K1 gate record (T7, T8 read this)\n"
      f"- `{NUMBERS}` every number in this report, as JSON\n"
      f"- `{FROZEN_TABLE}` per-item Arm A table on the frozen 1,000\n"
      + "".join(f"- `{p}`\n" for p in figs) + "\n")
    w(f"Spec version `{adv.SPEC_VERSION}`, `docs/spec/adversary-game-v1.md`. "
      f"`beta_c` by `adversary.beta_critical_batch` (bisection to "
      f"`eps_beta = {adv.EPS_BETA:g}`). Every item property read from P1's frozen "
      f"artifacts, never recomputed. No P2 item file or manifest exists, so custody "
      f"is by artifact hash:\n\n| artifact | sha256 |\n|---|---|\n")
    for k, v in rec["artifact_sha256"].items():
        w(f"| `{k}` | `{v}` |\n")
    w(f"\nRuntime {secs:.1f} s.\n")

    os.makedirs("reports", exist_ok=True)
    open(REPORT, "w").write("".join(L))


# ---------------------------------------------------------------------- main
def main():
    t0 = time.perf_counter()
    rec, pool, pool_rates, problems, pool_cols = step1()

    os.makedirs("results", exist_ok=True)
    json.dump(rec, open(GATE_RECORD, "w"), indent=2, default=str)

    if problems:
        print("STEP 1 REPRODUCTION FAILED. Halting before Step 2.", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        print(f"Gate record written to {GATE_RECORD} with the mismatch recorded.",
              file=sys.stderr)
        return 2
    if rec["outcome"] == 1:
        print("K1 KILL. Arms B and C do not run. Stopping before Step 2.", file=sys.stderr)
        return 1

    num, frame = arm_a(pool, pool_rates, pool_cols)
    frozen_rates = {float(k) if k != "inf" else math.inf: v
                    for k, v in num["step2"]["divergence_curve_frozen"].items()}
    figs = figures(frame, pool, pool_rates, frozen_rates)
    frame.to_parquet(FROZEN_TABLE, index=False)
    num["step1_gate_record"] = rec
    num["rate_claim_rule"] = {
        "rule": "Any claim of the form 'X% of items diverge' uses the POOL "
                "figure. The pool rate is a property of the signal space; the "
                "frozen rate is a property of P1's 50/50 conflict quota.",
        "population_existence_rate": rec["pooled_existence_rate"],
        "population_grid_rate": rec["pooled_grid_rate"],
        "population_base": "full unstratified 200,000-candidate pool",
        "frozen_set_rate_at_grid_endpoint": num["step2"]["divergence_curve_frozen"]["8.0"]["pooled"],
        "frozen_set_existence_rate": num["step2"]["finite_rate"],
        "frozen_set_status": "the Arm A base's own rate, sampler-dependent. Never "
                             "a population statement. Its gap from the pool rate "
                             "is fully accounted for by P1's 50% conflict quota "
                             "(v2.2 section 1.3), fixed before beta_c existed.",
        "applies_to": ["divergence rate", "existence rate", "grid rate",
                       "per-tile divergence rate", "share of items above the "
                       "grid endpoint"],
    }
    json.dump(num, open(NUMBERS, "w"), indent=2, default=str)

    secs = time.perf_counter() - t0
    write_report(rec, num, frame, figs, secs)

    print(f"K1  existence |D(inf)|/N = {rec['pooled_existence_rate']:.4f}  "
          f"grid |D(8)|/N = {rec['pooled_grid_rate']:.4f}  "
          f"threshold {K1_THRESHOLD:.2f}  ->  outcome {rec['outcome']}, "
          f"{rec['outcome_text']}")
    print(f"    reproduction: published matched, bit-for-bit vs T2 table = "
          f"{rec['reproduction']['bitwise_identical_to_T2_pool_table']}")
    print(f"K2  rho = {num['step2']['K2']['spearman_pool']:+.4f}  "
          f"(reproduction; fired in T2, not reopened)")
    c3 = num["step3"]["conventions"]
    print(f"    price of robustness over {num['step3']['n_divergence_set']} divergent "
          f"items: raw {num['step3']['mean']:.4f}, "
          f"P1 post_norm {c3['p1_post_norm']['mean_of_per_item_ratios']:.4f} (primary), "
          f"above-prior {c3['above_prior']['mean_of_per_item_ratios']:.4f}")
    print(f"    o*_inf == o_fit on {c3['o_star_infinity_is_o_fit']['share']:.4f} of "
          f"the divergence set; pool check "
          f"{num['step3']['pool_robustness_check']['conventions']['p1_post_norm']['mean_of_per_item_ratios']:.4f}")
    print(f"    written: {REPORT}, {GATE_RECORD}, {NUMBERS}, {FROZEN_TABLE}, "
          + ", ".join(figs))
    print(f"    runtime {secs:.1f} s")
    return 0


def demo():
    """Self-check on the spec's own identities, over the frozen size tile."""
    df = p1.load_items(tile="size")
    b = adv.build_batch(df)
    bc = adv.beta_critical_batch(b)
    r = b.rows
    o0, oinf = adv.optimal_option(b, 0.0), adv.optimal_option(b, math.inf)
    L = np.exp(b.log_l_star)
    price = L[r, o0] - L[r, oinf]

    assert (price >= 0).all(), "price of robustness went negative (v2.0 H-A bug check)"
    assert np.array_equal(np.isfinite(bc), o0 != oinf), \
        "beta_c finite must be exactly o*_0 != o*_infinity (spec section 7)"
    assert not in_D(bc, 0).any(), "D(0) must be empty (spec section 7.1)"
    prev = in_D(bc, 0)
    for beta in GRID[1:] + (math.inf,):
        cur = in_D(bc, beta)
        assert (cur | prev == cur).all(), f"D not nested at beta = {beta}"
        prev = cur
    assert (price[~np.isfinite(bc)] == 0).all(), "robust items must have zero price"
    fin = np.isfinite(bc)
    assert abs(fin.mean() - 108 / 250) < 1e-12, \
        f"size-tile finite rate {fin.mean():.4f}, v2.3 section 3 says 108/250"

    # The normalised price rests on being on P1's own code path and on o*_0
    # sitting at the Bayes pole. Both are checked, not assumed.
    cols = arm_a_columns(df)
    d = _check_p1_path(df, cols)
    pn_price = cols["post_norm_0"][fin] - cols["post_norm_inf"][fin]
    assert (pn_price >= 0).all(), "post_norm price went negative"
    assert (pn_price <= 1 + 1e-12).all(), "post_norm price exceeded 1"
    assert cols["_post_norm_0_max_shortfall"] < 1e-9, \
        "post_norm(o*_0) is materially below 1; o*_0 is not at the Bayes pole"
    sb = cols["sb_inf"][fin]
    ok = np.isfinite(sb)
    assert (sb[ok] == 0.0).all(), \
        "salience-Bayes coordinate at o*_inf is not identically 0; the Step 3 " \
        "degeneracy claim no longer holds and its prose is stale"
    print(f"ok: {len(df)} size-tile items, {int(fin.sum())} finite beta_c, "
          f"price in [{price.min():.2e}, {price.max():.4f}], D nested, D(0) empty")
    print(f"    on P1 code path (max |range - frontier_ext_post|) = {d:.1e}; "
          f"post_norm price mean {pn_price.mean():.4f}; "
          f"sb(o*_inf) == 0 on {int(ok.sum())}/{int(ok.sum())} defined")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
