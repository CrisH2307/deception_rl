"""Spec section 6.3's closed-form-versus-bisection cross-check, emitted.

The spec recommends it and `tests/test_adversary.py` has always asserted it, but
no artifact carried the result, so the paper could not cite it. This emits the
same function the test asserts on, `adversary.bisection_vs_closed_form`, on both
bases the paper cites `beta_c` at: the frozen 1,000 and the 200k pool.

Bookkeeping only. `beta_c`'s value of record stays the bisected value (spec
section 9, beta_critical); nothing here changes it or any artifact carrying it.

Run: python3 src/beta_c_crosscheck.py     (writes results/T1_beta_c_crosscheck.json)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adversary as adv  # noqa: E402
import k2_gate as K      # noqa: E402
import p1                # noqa: E402
from p1 import TAU_MAIN  # noqa: E402

OUT = "results/T1_beta_c_crosscheck.json"
TILES = ("hold", "manmade", "moves", "size")


def by_tile(df, chunk=None):
    out = {}
    for t in TILES:
        sub = df[df["tile"] == t].reset_index(drop=True)
        parts = ([adv.build_batch(sub)] if chunk is None
                 else list(adv.build_batch(sub, chunk=chunk)))
        rs = [adv.bisection_vs_closed_form(b, parallel_tol=0.0) for b in parts]   # pre-P2-D29 record
        out[t] = {k: (sum(r[k] for r in rs) if k.startswith("n_")
                      else max(r[k] for r in rs)) for k in rs[0]}
    return out


def main():
    bases = {"frozen_1000": by_tile(p1.load_items()),
             "pool_200000": by_tile(K.pool(), chunk=K.CHUNK)}
    for name, tiles in bases.items():
        tiles["all"] = {k: (sum(v[k] for v in tiles.values()) if k.startswith("n_")
                            else max(v[k] for v in tiles.values()))
                        for k in next(iter(tiles.values()))}
    out = {
        "purpose": "Spec section 6.3's recommended cross-check of bisected beta_c "
                   "against the closed-form root, emitted so it is citable.",
        "emitted_by": "src/beta_c_crosscheck.py, via adversary.bisection_vs_closed_form",
        "tau": 1.0,
        "value_of_record": "the bisected beta_c (spec section 9); unchanged here",
        "what_agreement_means": "identical robustness classification, the closed-form "
                                "root an exact root, and the bisected value within one "
                                "P1 D51 tie band. The beta gap is reported, not "
                                "thresholded: the spec's '~1e-6' is an expectation.",
        "tie_band_TAU_MAIN": TAU_MAIN,
        "bases": bases,
    }
    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    for name, tiles in bases.items():
        a = tiles["all"]
        print(f"{name}: {a['n_items']:,} items, {a['n_finite_beta_c']:,} finite; "
              f"robust-class disagreements {a['n_robust_classification_disagree']}; "
              f"max |beta gap| {a['max_abs_beta_gap']:.2e}; closed-form top-two gap "
              f"{a['max_rel_top_two_gap_at_closed_form']:.1e}; bisected "
              f"{a['max_rel_top_two_gap_at_bisected']:.1e} (band {TAU_MAIN:g})")
    print(f"written: {OUT}")


if __name__ == "__main__":
    main()
