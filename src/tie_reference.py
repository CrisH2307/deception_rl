"""The reference the Arm B tie rate is calibrated against (P2-D7).

P2-D6 makes the tie rate primary. A rate with no reference is not interpretable:
a framing tie rate of 0.9 is equally consistent with models being insensitive to
adversary structure and with F1/F2 being too weak to move anything, and the second
is a fact about T3's templates rather than about models. This script computes the
reference, from frozen Paper 1 output, before T7 runs.

TWO CANDIDATE REFERENCES, and the weaker one is not the primary.

  c5           PRIMARY. Paper 1's condition 4 against condition 5: one sentence
               inserted into the SAME `{extra}` slot P2-D2 puts the framing block
               in, with option order held fixed. Perturbation-matched to the
               framing contrast in slot, kind and direction of variation. It
               differs in content only (D64's `c5` asks the chooser to consider
               every Means-by-Clue pairing; P2's block describes an adversary).

  permutation  SECONDARY, and a BOUND rather than a matched null. Format V
               permutation 0 against permutation 1 within one condition: option
               ORDER varies and text is held fixed, which is the opposite
               perturbation. Reordering is plausibly the stronger of the two, so
               its disagreement rate is closer to an upper bound on surface-driven
               change than to a matched expectation.

A subtlety that has to be measured rather than assumed: `ΔA = 0` is NOT the same
event as "the model chose the same option". `A` is a deterministic function of the
chosen option but is not injective over an option set, so two distinct options can
share an `A`. Same option implies `ΔA = 0`; the converse fails. Both rates are
computed, the same-option rate is what the references calibrate, and the gap
between them is reported as what it is: choice movement that `A` cannot see.

Run: python3 src/tie_reference.py          (writes results/T5_tie_reference.json)
     python3 src/tie_reference.py --demo   (self-check on the rate ordering)
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1  # noqa: E402
import t6_arm_a as t6  # noqa: E402
import t6_f0_headroom as H  # noqa: E402
import p2_decisions as P2D  # noqa: E402

from tiebreak import EPS as P1_EPS  # noqa: E402  Paper 1's frozen 1e-12; P2-D19

RULE, FORM = H.RULE, H.FORM
OUT = "results/T5_tie_reference.json"
LADDER = H.LADDER_ORDER


def paired(ch, model, keep, vary):
    """Same-option rate over paired renderings, and the pair count.

    `vary` is the column that differs within a pair; every other identifying
    column is held fixed. A pair is dropped only if either member fails P1's
    `n_tied == 1` filter, which `H.choices()` has already applied, so the
    attrition here is pairs left incomplete by that filter.
    """
    keys = ["item_id", "condition", "permutation_id"]
    keys.remove(vary)
    g = ch[(ch["model"] == model) & (ch["prompt_form"] == FORM)
           & (ch["rule"] == RULE) & (ch["item_id"].isin(keep))]
    w = g.pivot_table(index=keys, columns=vary, values="chosen_option",
                      aggfunc="first")
    if w.shape[1] != 2:
        return None
    ok = w.notna().all(axis=1)
    a, b = w.loc[ok].iloc[:, 0].values, w.loc[ok].iloc[:, 1].values
    return {"n_pairs": int(ok.sum()), "n_incomplete": int((~ok).sum()),
            "same_option_rate": float((a == b).mean())}


def pair_frame(ch, model, keep, col="condition", base="cond4", arm="cond5"):
    """Wide `(item_id, permutation_id) x {base, arm}` chosen options. P2-D16.

    This is the pivot-and-`notna` shape P2-D16 names as the implementation of its
    rule, factored out of `c5_effect.c5_movement` and
    `inertness_ceiling.c5_delta_A` rather than copied a third time: a rendering
    that failed P1's `n_tied == 1` filter is simply absent, so its
    `(item, permutation)` row is short a column and leaves both the numerator and
    the denominator, while the item's other permutation is retained and the item
    is never dropped whole.

    `col` names the factor that varies within a pair. It defaults to Paper 1's
    `condition` so the frozen `R_m` values recompute unchanged; T7's framing
    contrasts pass `col="framing"` with `base="F0"`. The frame is restricted to
    the two levels of the contrast BEFORE the `notna` filter, because a third
    level present in `ch` would otherwise drop pairs that the contrast at hand can
    still form: P2-D16 requires a tied `F1` rendering to leave the `F1` contrast
    only, not the `F2` one.
    """
    g = ch[(ch["model"] == model) & (ch["prompt_form"] == FORM)
           & (ch["rule"] == RULE) & (ch["item_id"].isin(keep))
           & ch[col].isin((base, arm)) & ch["permutation_id"].notna()]
    w = g.pivot_table(index=["item_id", "permutation_id"], columns=col,
                      values="chosen_option", aggfunc="first")
    w = w.reindex(columns=[base, arm])
    return w.loc[w.notna().all(axis=1)]


def a_invisibility(A, ids, mask, eps=0.0):
    """How much option movement `A` cannot see, on a given item subset.

    Reported because it bounds what the tie rate can mean: on an item where two
    options share an `A`, a real switch between them registers as no movement.

    `eps` is the tolerance at which two options count as `A`-tied. The default of
    0.0 is exact float equality and is what `v2.5` section 3 and `v2.6` section
    2.2 report; it is kept as the default so those figures still reproduce. P2-D19
    adopts Paper 1's `tiebreak.EPS = 1e-12` for anything citing the coordinate's
    resolution, and `main` emits both. `next_gap_above_eps` is the smallest gap the
    tolerance does NOT absorb: it is what says whether the tolerance sits in a gap
    or in a continuum, and a value close to `eps` means this number was chosen
    rather than inherited.
    """
    n_items_with_dup, n_pairs, n_dup_pairs = 0, 0, 0
    next_gap = float("inf")
    for i in ids[mask]:
        a = A[int(i)]
        k = len(a)
        dup = 0
        for x in range(k):
            for y in range(x + 1, k):
                g = abs(a[x] - a[y])
                if g <= eps:
                    dup += 1
                else:
                    next_gap = min(next_gap, float(g))
        n_dup_pairs += dup
        n_pairs += k * (k - 1) // 2
        n_items_with_dup += bool(dup)
    return {"n_items": int(mask.sum()), "eps": float(eps),
            "next_gap_above_eps": next_gap,
            # P2-D19's primary base is the option pair. The per-item share counts
            # items containing AT LEAST ONE tied pair, so it scales with option
            # count: a 6-option item has 15 chances to contain one, a 3-option
            # item has 3. Both are labelled here so neither can be lifted out of
            # the JSON without the other.
            "primary_base": "unordered option pairs",
            "share_option_pairs_invisible_to_A_is":
                "PRIMARY. A-tied option pairs / all unordered option pairs.",
            "share_items_with_an_A_tied_option_pair_is":
                "SECONDARY, and inflated by option count. Items containing at "
                "least one A-tied pair / items. Not the Arm B blind-spot rate: "
                "that needs the two CHOSEN options tied, not the item to contain "
                "a tied pair. Quote only beside the per-pair share.",
            "n_items_with_an_A_tied_option_pair": n_items_with_dup,
            "share_items_with_an_A_tied_option_pair":
                float(n_items_with_dup / max(1, int(mask.sum()))),
            "n_unordered_option_pairs": n_pairs,
            "n_A_tied_option_pairs": n_dup_pairs,
            "share_option_pairs_invisible_to_A":
                float(n_dup_pairs / max(1, n_pairs))}


BOOT_N = 10_000
BOOT_SEED = 20260910
ALPHA_TIE = 0.05 / 21     # Bonferroni within the tie family; see P2-D7


def cluster_bootstrap_diff(item_ids, x, y, alpha=ALPHA_TIE, n=BOOT_N,
                           seed=BOOT_SEED):
    """Interval on mean(x) - mean(y), resampling ITEMS, not renderings.

    Each item contributes two renderings (the two Format V permutations), so a
    plain binomial interval on 216 pairs would treat 108 items as 216 independent
    draws. Resampling whole items keeps the clustering. The interval is at
    `1 - alpha` rather than 95%, which is where the Bonferroni correction for the
    21-cell tie family is applied.
    """
    item_ids = np.asarray(item_ids)
    x, y = np.asarray(x, float), np.asarray(y, float)
    uniq = np.unique(item_ids)
    idx = {i: np.where(item_ids == i)[0] for i in uniq}
    rng = np.random.default_rng(seed)
    obs = float(x.mean() - y.mean())
    draws = np.empty(n)
    for b in range(n):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        sel = np.concatenate([idx[i] for i in pick])
        draws[b] = x[sel].mean() - y[sel].mean()
    lo, hi = np.percentile(draws, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"difference": obs, "lo": float(lo), "hi": float(hi),
            "alpha": alpha, "n_items": int(len(uniq)), "n_renderings": int(len(x)),
            "excludes_zero": bool(hi < 0 or lo > 0),
            "direction": "below" if hi < 0 else ("above" if lo > 0 else "inside"),
            "bootstrap_draws": n, "seed": seed}


def paired_indicator(ch, model, keep, vary):
    """(item_ids, indicator) per matched rendering pair, for the bootstrap."""
    keys = ["item_id", "condition", "permutation_id"]
    keys.remove(vary)
    g = ch[(ch["model"] == model) & (ch["prompt_form"] == FORM)
           & (ch["rule"] == RULE) & (ch["item_id"].isin(keep))]
    w = g.pivot_table(index=keys, columns=vary, values="chosen_option",
                      aggfunc="first")
    ok = w.notna().all(axis=1)
    w = w.loc[ok]
    same = (w.iloc[:, 0].values == w.iloc[:, 1].values).astype(float)
    return w.index.get_level_values("item_id").values, same


def load_choices():
    """P1's Format V choice rows from both frozen files, P1's own filters applied.

    The ladder file has no `prompt_form` column and its prompts are the templated
    rendering, so it is labelled rather than dropped. Exposed as a function
    because a second caller that re-inlined this block would be a duplication bug.
    """
    ch = pd.concat([pd.read_parquet(p) if "prompt_form" in
                    pd.read_parquet(p).columns else
                    pd.read_parquet(p).assign(prompt_form="template")
                    for p in (H.LADDER, H.T26)], ignore_index=True)
    return ch[(ch["format"] == "V") & (ch["n_tied"] == 1)
              & (ch["unscored_reason"].fillna("").astype(str) == "")]


def item_sets():
    """`(df, cols, A, ids, {name: mask})`. The domain is `isfinite(beta_c)`.

    Never `ext_i > 0`: the two are equivalent mathematically and differ on one
    frozen item in float64 (`T7.md`, note 1). Exposed for the same reason
    `load_choices` is.
    """
    df, cols, A, ext = H.item_axis()
    ids, tiles = df["item_id"].values, df["tile"].values
    D = np.isfinite(cols["beta_c"])
    SZ = D & (tiles == "size")
    return df, cols, A, ids, {"divergence_set": D, "size_tile_confirmatory": SZ}


def main():
    df, cols, A, ids, sets = item_sets()
    tiles = df["tile"].values
    D, SZ = sets["divergence_set"], sets["size_tile_confirmatory"]
    ch = load_choices()

    out = {
        "purpose": "Reference for the Arm B tie rate (P2-D6), fixed before T7 runs.",
        "rule": RULE, "prompt_form": FORM,
        "primary_reference": "c5: cond4 vs cond5, one sentence inserted in the "
                             "same {extra} slot P2-D2 uses, option order fixed. "
                             "Perturbation-matched in slot, kind and direction.",
        "secondary_reference": "permutation: perm 0 vs perm 1 within cond4, "
                               "option order varies and text is fixed. The "
                               "opposite perturbation, and plausibly the stronger "
                               "one, so it bounds rather than matches.",
        "delta_A_zero_is_not_same_option":
            "A is a deterministic function of the chosen option but is not "
            "injective over an option set. Same option implies delta-A = 0; the "
            "converse fails. The references calibrate the SAME-OPTION rate, and "
            "the A-invisibility figures below say how far the two can diverge.",
        "a_invisibility": {k: a_invisibility(A, ids, m) for k, m in sets.items()},
        # P2-D19: the same figures at Paper 1's tiebreak tolerance. The exact-
        # equality block above is kept unchanged because `v2.5` and `v2.6` cite it
        # and a superseded document must still reproduce.
        "a_invisibility_at_p1_eps": {k: a_invisibility(A, ids, m, eps=P1_EPS)
                                    for k, m in sets.items()},
        # Per tile, so "size is the worst tile on both bases" has a source. D49
        # and D108 fixed the tile on measured grounds years before this; this is
        # a limitation to state, not a reason to revisit it.
        "a_invisibility_by_tile_at_p1_eps": {
            t: a_invisibility(A, ids, D & (tiles == t), eps=P1_EPS)
            for t in sorted(set(tiles[D]))},
        "references": {},
    }
    for sname, mask in sets.items():
        keep = set(int(i) for i in ids[mask])
        rows = {}
        for m in LADDER:
            c5 = paired(ch[ch["permutation_id"].notna()], m, keep, "condition")
            pm = paired(ch[ch["condition"] == "cond4"], m, keep, "permutation_id")
            if c5 is None or pm is None:
                continue
            rows[m] = {"c5_same_option_rate": c5["same_option_rate"],
                       "c5_n_pairs": c5["n_pairs"],
                       "permutation_same_option_rate": pm["same_option_rate"],
                       "permutation_n_pairs": pm["n_pairs"],
                       "c5_minus_permutation":
                           c5["same_option_rate"] - pm["same_option_rate"]}
        out["references"][sname] = rows

    # Instrument check, run on the two references against each other. If the
    # bootstrap cannot separate a text insert from a reordering, it cannot
    # separate a framing from a text insert either, and T7 should not rely on it.
    keep = set(int(i) for i in ids[SZ])
    chk = {}
    for m in LADDER:
        ic, xc = paired_indicator(ch[ch["permutation_id"].notna()], m, keep,
                                  "condition")
        ip, xp = paired_indicator(ch[ch["condition"] == "cond4"], m, keep,
                                  "permutation_id")
        # different pairings, so align on the item level by per-item means
        dfc = pd.DataFrame({"i": ic, "v": xc}).groupby("i")["v"].mean()
        dfp = pd.DataFrame({"i": ip, "v": xp}).groupby("i")["v"].mean()
        j = dfc.index.intersection(dfp.index)
        chk[m] = cluster_bootstrap_diff(j.values, dfp.loc[j].values,
                                        dfc.loc[j].values)
    out["instrument_check_permutation_minus_c5"] = chk
    out["decision_rule"] = {
        "unit": "matched rendering pair (item x permutation), aggregated to an "
                "item-level mean before resampling",
        "statistic": "framing same-option rate minus the model's c5 same-option "
                     "rate, on the size-tile confirmatory set",
        "interval": f"cluster bootstrap over items, {BOOT_N:,} resamples, seed "
                    f"{BOOT_SEED}, at 1 - alpha with alpha = 0.05/21",
        "alpha": ALPHA_TIE,
        "why_bootstrap": "Each item contributes two renderings, so a binomial "
                         "interval on the pairs would treat 108 items as 216 "
                         "independent draws.",
    }
    # P2-D19 binds the tolerance and the two figures it produces. Asserted here,
    # before the write, so a drift cannot enter the artifact.
    e = out["a_invisibility_at_p1_eps"]["size_tile_confirmatory"]
    P2D.bind_a_tie_tolerance(e["eps"], e["n_items_with_an_A_tied_option_pair"],
                             e["n_A_tied_option_pairs"],
                             e["n_unordered_option_pairs"], e["next_gap_above_eps"])
    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    for sname in sets:
        r = out["references"][sname]
        inv = out["a_invisibility"][sname]
        print(f"\n{sname}  (n = {inv['n_items']}; "
              f"{inv['share_items_with_an_A_tied_option_pair']:.4f} of items carry "
              f"an A-tied option pair, {inv['share_option_pairs_invisible_to_A']:.4f} "
              f"of option pairs invisible to A)")
        print(f"  {'model':6s} {'c5 same-opt':>12s} {'perm same-opt':>14s} {'c5 - perm':>10s}")
        for m, v in r.items():
            print(f"  {m:6s} {v['c5_same_option_rate']:12.4f} "
                  f"{v['permutation_same_option_rate']:14.4f} "
                  f"{v['c5_minus_permutation']:+10.4f}")
    print(f"\ninstrument check, size tile: permutation rate minus c5 rate, "
          f"cluster bootstrap over items at alpha = {ALPHA_TIE:.6f}")
    for m, v in out["instrument_check_permutation_minus_c5"].items():
        print(f"  {m:6s} {v['difference']:+.4f}  "
              f"[{v['lo']:+.4f}, {v['hi']:+.4f}]  "
              f"{'separates' if v['excludes_zero'] else 'DOES NOT SEPARATE'}")
    print(f"\nwritten: {OUT}")
    return 0


def demo():
    """Same option implies delta-A = 0, so the same-option rate never exceeds the
    tie rate. Asserted on the frozen geometry, which is what makes the reference
    a lower bound on the tie rate rather than an estimate of it."""
    df, cols, A, ext = H.item_axis()
    ids = df["item_id"].values
    D = np.isfinite(cols["beta_c"])
    bad = 0
    for i in ids[D]:
        a = A[int(i)]
        for o in range(len(a)):
            if a[o] - a[o] != 0.0:
                bad += 1
    assert bad == 0, "A(o) - A(o) is not zero; same option must give delta-A = 0"
    SZ = D & (df["tile"].values == "size")
    inv = a_invisibility(A, ids, SZ)
    assert inv["n_A_tied_option_pairs"] > 0, (
        "no A-tied option pairs found; the report claims the tie rate and the "
        "same-option rate can differ, and that claim now has no support")
    eps_inv = a_invisibility(A, ids, SZ, eps=P1_EPS)
    # P2-D19 stands on a gap, not on a threshold: the tolerance is inherited and
    # is only defensible while nothing sits near it. If a future geometry puts a
    # real gap inside a decade of 1e-12, the decision has to be revisited rather
    # than silently kept, and this is where that surfaces.
    assert eps_inv["next_gap_above_eps"] > P1_EPS * 1e6, (
        f"P2-D19: the smallest gap above eps is {eps_inv['next_gap_above_eps']:.3g}, "
        f"within six orders of {P1_EPS:g}. The tolerance no longer sits in a gap, "
        "so it is now a chosen threshold and the decision must be revisited.")
    print(f"ok: same option gives delta-A = 0 on all {int(D.sum())} divergent "
          f"items, so same-option rate <= tie rate")
    dv = a_invisibility(A, ids, D, eps=P1_EPS)
    print(f"    size tile, exact equality: {inv['n_A_tied_option_pairs']} A-tied "
          f"option pairs of {inv['n_unordered_option_pairs']}, on "
          f"{inv['n_items_with_an_A_tied_option_pair']} of {inv['n_items']} items")
    print(f"    size tile, eps={P1_EPS:g}: PRIMARY per-pair "
          f"{eps_inv['n_A_tied_option_pairs']}/{eps_inv['n_unordered_option_pairs']} "
          f"= {eps_inv['share_option_pairs_invisible_to_A']:.4f}, against "
          f"{dv['n_A_tied_option_pairs']}/{dv['n_unordered_option_pairs']} "
          f"= {dv['share_option_pairs_invisible_to_A']:.4f} pooled, "
          f"x{eps_inv['share_option_pairs_invisible_to_A'] / dv['share_option_pairs_invisible_to_A']:.2f}")
    print(f"    size tile, eps={P1_EPS:g}: secondary per-item "
          f"{eps_inv['n_items_with_an_A_tied_option_pair']}/{eps_inv['n_items']} "
          f"= {eps_inv['share_items_with_an_A_tied_option_pair']:.4f} (items with "
          f"ANY tied pair; 15 pairs per size item, so inflated by option count)")
    print(f"    next gap above eps {eps_inv['next_gap_above_eps']:.4g}")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
