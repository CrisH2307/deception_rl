"""Do F0->F1 and F0->F2 switches concentrate on the A-tied option pairs?

P2-D19 bounds the `A` coordinate's blind spot at the PER-PAIR rate, 84 of 1,620
unordered option pairs on the confirmatory set, 0.0519. P2-D22 section 3.4.1 and
`v2.13` section 3.4.1 both record the assumption that bound rests on, and record
that it was not checked:

  > The bound holds if the option pairs models actually switch between are not
  > concentrated on the tied pairs. They may be: the tied pairs are concentrated
  > at the two ends of the option order.

Checking it reads model choices, so neither version could do it. T7's confirmatory
run did not do it either. This script does, and it does nothing else: it adjusts
no statistic, and P2-D19's tolerance, P2-D20's unit and the three quantities are
untouched.

Two quantities, per (model, framing) cell:

  THE REALIZED BLIND SPOT, as a count. Items that changed option but carry
  `ΔA = 0` at P2-D20's item unit. This is quantity (a)'s moving-item count minus
  quantity (c)'s `n_eff`, and it is what (c) cannot see of what (a) sees.

  THE CONCENTRATION. Of the switches that occur, the share whose {from, to}
  option pair is `A`-tied, against the share expected if switches were uniform
  over the item's own 15 unordered pairs. A ratio above 1 means switches prefer
  the tied pairs and the per-pair bound UNDERSTATES the blind spot.

Run: python3 src/t7_switch_concentration.py
     python3 src/t7_switch_concentration.py --demo
"""
import json
import os
import sys
from collections import Counter

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2_decisions as P2D  # noqa: E402
import tie_reference as TR  # noqa: E402
from tiebreak import EPS    # noqa: E402

OUT = "results/T7_switch_concentration.json"
CHOICES = "data/raw_t7/choices_t7.parquet"
ARMS = ("F1", "F2")
BASE = "F0"


def tied_pairs(A, item):
    """The `A`-tied unordered option pairs on one item, at P2-D19's EPS."""
    a = np.asarray(A[int(item)])
    k = len(a)
    return {(x, y) for x in range(k) for y in range(x + 1, k)
            if abs(a[x] - a[y]) <= EPS}


def load():
    # `prompt_form` is absent from the T7 parquet and is labelled rather than
    # filtered, exactly as `t7_armb.load` does it, so `pair_frame`'s shared
    # filter applies unchanged and this file does not fork that decision.
    d = pd.read_parquet(CHOICES).assign(prompt_form=TR.FORM)
    return d[(d["format"] == "V") & (d["n_tied"] == 1)
             & (d["unscored_reason"].fillna("").astype(str) == "")
             & (d["rule"] == TR.RULE)]


def cell(ch, A, keep, model, arm, tied, npairs):
    """One (model, framing) cell. Reuses P2-D16's pivot; no second copy."""
    w = TR.pair_frame(ch, model, keep, "framing", BASE, arm)
    it = w.index.get_level_values("item_id").values.astype(int)
    b, a_ = w[BASE].values.astype(int), w[arm].values.astype(int)

    # P2-D20's item unit, formed exactly as `_item_reading` forms it.
    d = np.array([A[i][y] - A[i][x] for i, x, y in zip(it, b, a_)])
    mean = pd.Series(d).groupby(it).mean()
    changed = pd.Series((b != a_).astype(float)).groupby(it).mean()
    n_moved = int((changed > 0).sum())
    n_eff = int((mean.abs() > EPS).sum())

    # Switches, at the rendering pair, which is where an option pair exists.
    sw = [(i, tuple(sorted((x, y)))) for i, x, y in zip(it, b, a_) if x != y]
    on_tied = [p for i, p in sw if p in tied[i]]
    # Expected share if a switch were uniform over that item's own pairs.
    exp = float(np.mean([len(tied[i]) / npairs for i, _ in sw])) if sw else float("nan")
    obs = len(on_tied) / len(sw) if sw else float("nan")
    return {
        "n_items_moved_quantity_a": n_moved,
        "n_eff_item_quantity_c": n_eff,
        "n_items_changed_but_delta_A_zero": n_moved - n_eff,
        "n_switches": len(sw),
        "n_switches_on_an_A_tied_pair": len(on_tied),
        "observed_share_on_tied_pairs": obs,
        "expected_share_if_uniform_within_item": exp,
        "concentration_ratio": (obs / exp) if exp and np.isfinite(exp) and exp > 0
                               else float("nan"),
        "tied_switch_option_pairs": {f"{p[0]},{p[1]}": n
                                     for p, n in sorted(Counter(on_tied).items())},
    }


def main():
    df, cols, A, ids, sets = TR.item_sets()
    SZ = sets["size_tile_confirmatory"]
    keep = set(int(i) for i in ids[SZ])
    ch = load()
    inv = TR.a_invisibility(A, ids, SZ, eps=EPS)
    P2D.bind_a_tie_tolerance(inv["eps"], inv["n_items_with_an_A_tied_option_pair"],
                             inv["n_A_tied_option_pairs"],
                             inv["n_unordered_option_pairs"], inv["next_gap_above_eps"])
    tied = {i: tied_pairs(A, i) for i in keep}
    k = len(A[next(iter(keep))])
    npairs = k * (k - 1) // 2
    assert npairs * len(keep) == inv["n_unordered_option_pairs"], (
        "the per-item pair count does not reconstruct the set total; the "
        "confirmatory tile is not uniform in option count and the expected-share "
        "baseline below would be mis-specified")

    rows = {f"{m}/{a}": cell(ch, A, keep, m, a, tied, npairs)
            for a in ARMS for m in TR.LADDER}
    out = {
        "purpose": "The assumption P2-D19's per-pair blind-spot bound rests on, "
                   "checked. v2.13 section 3.4.1 records it as unchecked.",
        "emitted_by": "src/t7_switch_concentration.py",
        "adjusts_nothing": "No statistic is changed by this file. P2-D19's EPS, "
                           "P2-D20's unit and P2-D12's three quantities are "
                           "untouched. This is a diagnostic and it is reported.",
        "eps": EPS,
        "per_pair_bound": inv["share_option_pairs_invisible_to_A"],
        "n_A_tied_option_pairs": inv["n_A_tied_option_pairs"],
        "n_unordered_option_pairs": inv["n_unordered_option_pairs"],
        "reading": "concentration_ratio > 1 means switches land on A-tied pairs "
                   "more often than a within-item uniform switch would, so the "
                   "per-pair bound UNDERSTATES the realized blind spot. Below 1, "
                   "it overstates it.",
        "per_cell": rows,
    }
    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    print(f"per-pair bound {out['per_pair_bound']:.4f} "
          f"({out['n_A_tied_option_pairs']}/{out['n_unordered_option_pairs']})\n")
    print(f"{'cell':10s} {'(a) moved':>9s} {'(c) n_eff':>9s} {'blind':>6s} "
          f"{'switches':>9s} {'on tied':>8s} {'obs':>7s} {'exp':>7s} {'ratio':>6s}")
    for kk, v in rows.items():
        print(f"{kk:10s} {v['n_items_moved_quantity_a']:9d} "
              f"{v['n_eff_item_quantity_c']:9d} "
              f"{v['n_items_changed_but_delta_A_zero']:6d} {v['n_switches']:9d} "
              f"{v['n_switches_on_an_A_tied_pair']:8d} "
              f"{v['observed_share_on_tied_pairs']:7.4f} "
              f"{v['expected_share_if_uniform_within_item']:7.4f} "
              f"{v['concentration_ratio']:6.2f}")
    agg = Counter()
    for v in rows.values():
        agg.update(v["tied_switch_option_pairs"])
    print("\ntied-pair switches by option-index pair:", dict(agg.most_common()))
    print(f"\nwritten: {OUT}")
    return 0


def demo():
    """The blind spot is a count of items (c) cannot see and (a) can, so it is
    non-negative by construction: a same-option item has dA = 0 exactly."""
    d = json.load(open(OUT)) if os.path.exists(OUT) else None
    assert d, f"{OUT} missing; run python3 {__file__} first"
    for k, v in d["per_cell"].items():
        assert v["n_items_changed_but_delta_A_zero"] >= 0, k
        assert v["n_eff_item_quantity_c"] <= v["n_items_moved_quantity_a"], (
            f"{k}: n_eff exceeds the moving-item count, so (c) resolves an item "
            "(a) says did not move. A same-option item has dA = 0 exactly, so "
            "this is a join error, not a result.")
        assert v["n_switches_on_an_A_tied_pair"] <= v["n_switches"], k
    print(f"ok: blind spot non-negative and n_eff <= moved in all "
          f"{len(d['per_cell'])} cells")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
