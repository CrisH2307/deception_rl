"""Did Paper 1's `c5` insert measurably move choices? P2-D8's reference needs a status.

P2-D8 calibrates Arm B's no-movement half against Paper 1's condition-4-versus-
condition-5 same-option rate `R_m`. It fixes the values and the decision rule and
leaves one thing unstated: **whether `c5` itself moved anything.** That is not a
detail, because it changes what a null licenses.

  c5 moved little or nothing   `R_m` is a no-manipulation baseline, and
                               "F1 indistinguishable from `R_m`" means F1 moved
                               nothing either.
  c5 moved choices             `R_m` is an ACTIVE comparator, and the same result
                               means "F1 moved choices about as much as a
                               known-effective content insertion in the same slot
                               did", which is a different and stronger sentence.

THE NULL RATE IS 1.0 EXACTLY, AND IT IS ARGUED FROM THE CODE PATH, NOT MEASURED.

Paper 1 never samples. `score_llm.score_rows` teacher-forces every option string
and sums token log-probabilities from one forward pass; `score_llm.pick` returns
the argmax set; `n_tied` records exact ties and the analysis keeps `n_tied == 1`.
There is no temperature, no `do_sample`, no seed, and no `generate` call in the
file. So an identical prompt yields an identical `chosen_option`, the same-option
rate under a no-op perturbation is exactly 1, and every changed pair below is
caused by the inserted sentence.

The frozen artifacts contain no repeated rendering (the two files share no model,
and permutation is a real perturbation), so this cannot be corroborated by a
repeat run. The residual is float nondeterminism across batch compositions
perturbing a near-tie; it is stated rather than quantified, because the frozen
columns carry the chosen option's score and not the runner-up's. It is not a
credible explanation for a change rate of 0.14 to 0.37.

Run: python3 src/c5_effect.py          (writes results/T5_c5_effect.json)
     python3 src/c5_effect.py --demo   (self-check against the P2-D8 table)
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2_decisions as P2D  # noqa: E402
import tie_reference as TR  # noqa: E402

OUT = "results/T5_c5_effect.json"
NO_EFFECT_RATE = 1.0        # deterministic scorer; see the module docstring


def tv(a, b):
    """Total variation distance between two option marginals.

    Reported beside the change rate because they answer different questions. A
    high change rate with `tv` near zero is churn: `c5` moves individual
    renderings without shifting the option distribution. Both count as "the
    insert moved choices"; only the second is also a directional effect.
    """
    keys = sorted(set(a) | set(b))
    pa = np.array([(a == k).mean() for k in keys])
    pb = np.array([(b == k).mean() for k in keys])
    return float(0.5 * np.abs(pa - pb).sum())


def c5_movement(ch, model, keep, col="condition", base="cond4", arm="cond5"):
    """Per-model `c5` change rate with the P2-D8 interval, on one item set.

    `col`/`base`/`arm` default to Paper 1's condition contrast, which is what
    P2-D8's `R_m` is computed on. T7's quantity (a) is the same statistic on
    `col="framing"`, `base="F0"`: the same rate against the same null, so it runs
    through this function rather than through a second copy of it.
    """
    w = TR.pair_frame(ch, model, keep, col, base, arm)
    c4, c5 = w[base].values, w[arm].values
    changed = (c4 != c5).astype(float)
    items = w.index.get_level_values("item_id").values
    # Item-level means before resampling, per P2-D8's decision rule: each item
    # contributes two renderings and they are not independent draws.
    per_item = pd.DataFrame({"i": items, "v": changed}).groupby("i")["v"].mean()
    ci = TR.cluster_bootstrap_diff(per_item.index.values, per_item.values,
                                   np.zeros(len(per_item)))
    return {
        "n_pairs": int(len(w)), "n_changed": int(changed.sum()),
        "same_option_rate": float(1 - changed.mean()),
        "change_rate": float(changed.mean()),
        "change_rate_item_mean": float(per_item.mean()),
        "ci_lo": ci["lo"], "ci_hi": ci["hi"], "alpha": ci["alpha"],
        "n_items": ci["n_items"],
        "excludes_no_effect": bool(ci["lo"] > 0.0),
        "n_items_with_a_changed_pair": int((per_item > 0).sum()),
        "share_items_with_a_changed_pair": float((per_item > 0).mean()),
        "tv_option_marginal": tv(c4, c5),
    }


def main():
    df, cols, A, ids, sets = TR.item_sets()
    ch = TR.load_choices()
    out = {
        "purpose": "Status of P2-D8's c5 reference: baseline or active comparator. "
                   "Computed before any Paper 2 model data exists.",
        "rule": TR.RULE, "prompt_form": TR.FORM,
        "no_effect_same_option_rate": NO_EFFECT_RATE,
        "no_effect_rate_provenance":
            "Exactly 1.0 by the code path, not by measurement. P1's chosen option "
            "is the argmax over teacher-forced option log-probabilities "
            "(score_llm.score_rows / score_llm.pick); the file contains no "
            "sampling, no temperature and no seed, and n_tied == 1 is filtered. "
            "An identical prompt therefore gives an identical choice. The frozen "
            "artifacts hold no repeated rendering, so this is argued rather than "
            "corroborated by a repeat run.",
        "residual":
            "Float nondeterminism across batch compositions could flip a "
            "near-tie. Not quantifiable from the frozen columns, which carry the "
            "chosen option's score and not the runner-up's. Not a credible "
            "account of the change rates below.",
        "interval": "cluster bootstrap over items, item-level means, "
                    f"{TR.BOOT_N:,} resamples, seed {TR.BOOT_SEED}, at "
                    f"1 - alpha with alpha = {TR.ALPHA_TIE:.6f} (P2-D8)",
        "sets": {},
    }
    for sname, mask in sets.items():
        keep = set(int(i) for i in ids[mask])
        out["sets"][sname] = {m: c5_movement(ch, m, keep) for m in TR.LADDER}

    sz = out["sets"]["size_tile_confirmatory"]
    rates = [v["change_rate"] for v in sz.values()]
    n_active = sum(v["excludes_no_effect"] for v in sz.values())
    out["verdict"] = {
        "set": "size_tile_confirmatory",
        "models_whose_change_rate_excludes_zero": n_active,
        "models": len(sz),
        "change_rate_range": [min(rates), max(rates)],
        "reading": ("ACTIVE COMPARATOR" if n_active == len(sz) else
                    "MIXED, see per-model rows"),
        "what_it_licenses":
            "R_m is the same-option rate of a manipulation that demonstrably "
            "moves choices in this slot on every model. A framing rate "
            "indistinguishable from R_m therefore reads as 'the framing moved "
            "choices about as much as a known-effective content insertion did', "
            "not as 'the framing moved nothing'. It still does not support H-B, "
            "because H-B is a claim about adversary tracking and this comparison "
            "is blind to direction; the sign test carries direction and P2-D8 "
            "already gives it no claim in the indistinguishable cell.",
    }
    # The constant is the source (D100). This script must reproduce it, not
    # define it; a drift fails here rather than reaching the results table.
    lo, hi = P2D.P2D9_C5_CHANGE_RATE_RANGE
    assert abs(min(rates) - lo) < 1e-12 and abs(max(rates) - hi) < 1e-12, (
        f"P2-D9 states a c5 change rate of {lo} to {hi}; this run gives "
        f"{min(rates)} to {max(rates)}. docs/P2/DECISIONS.md is the source.")
    assert P2D.P2D9_C5_IS_ACTIVE == (n_active == len(sz)), (
        "P2-D9 states the c5 reference is active; this run disagrees")
    assert P2D.P2D9_NO_EFFECT_SAME_OPTION_RATE == NO_EFFECT_RATE

    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    for sname, rows in out["sets"].items():
        print(f"\n{sname}   no-effect same-option rate = {NO_EFFECT_RATE}")
        print(f"  {'model':6s} {'same-opt':>9s} {'change':>8s} {'changed/pairs':>14s} "
              f"{'CI on change rate':>26s} {'items moved':>12s} {'TV':>7s}")
        for m, v in rows.items():
            print(f"  {m:6s} {v['same_option_rate']:9.4f} {v['change_rate']:8.4f} "
                  f"{v['n_changed']:>7d}/{v['n_pairs']:<6d} "
                  f"[{v['ci_lo']:+.4f}, {v['ci_hi']:+.4f}]  "
                  f"{'MOVED' if v['excludes_no_effect'] else 'no':>5s} "
                  f"{v['share_items_with_a_changed_pair']:12.4f} "
                  f"{v['tv_option_marginal']:7.4f}")
    v = out["verdict"]
    print(f"\nverdict: {v['reading']}  "
          f"({v['models_whose_change_rate_excludes_zero']}/{v['models']} models, "
          f"change rate {v['change_rate_range'][0]:.4f} to "
          f"{v['change_rate_range'][1]:.4f} on the confirmatory set)")
    print(f"\nwritten: {OUT}")
    return 0


def demo():
    """The measured same-option rates must reproduce P2-D8's tabulated `R_m`.

    This is the check that matters: if they do not, either the reference in the
    preregistration or this read of the same artifact is wrong, and T7 would
    calibrate against a number nothing recomputes.
    """
    ch = TR.load_choices()
    df, cols, A, ids, sets = TR.item_sets()
    keep = set(int(i) for i in ids[sets["size_tile_confirmatory"]])
    got = {m: c5_movement(ch, m, keep)["same_option_rate"] for m in TR.LADDER}
    P2D.bind_armb_tie(got, TR.BOOT_N, TR.BOOT_SEED, False)
    for m, v in got.items():
        assert abs(v + c5_movement(ch, m, keep)["change_rate"] - 1.0) < 1e-12, m
    print(f"ok: same-option rates reproduce P2-D8's table on all {len(got)} models, "
          "and change rate = 1 - same-option rate exactly")
    print("    " + "  ".join(f"{m}={v:.4f}" for m, v in got.items()))
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
