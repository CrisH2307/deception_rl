"""Export per-item, per-option `marg_norm` for the 108 confirmatory items.

So `v2.7` section 2.1's `c5` sign proportions and section 2.2's measured blind
spot can be recomputed by someone who does not run this repo. Both were checked
only by `src/inertness_ceiling.py`, which produced them.

Under P2-D15, `sign(ΔA) = sign(marg_norm(o_5) - marg_norm(o_4))`, and two options
are `A`-tied exactly when their `marg_norm` is equal, because `A` is affine in
`marg_norm` with a per-item slope `1 / ext_i > 0`. So `marg_norm` plus Paper 1's
frozen `cond4` / `cond5` chosen options is everything the recomputation needs.
`A` is exported beside it for convenience and is not used by `--demo`.

Floats are written at 17 significant digits. Read them with a round-trip parser
(`pd.read_csv(..., float_precision="round_trip")`): pandas' default parser is not
exact, and on this table it collapses near-ties that decide a sign.

Run: python3 src/t7_marg_norm_export.py          (writes the CSV)
     python3 src/t7_marg_norm_export.py --demo   (recomputes both from marg_norm)
"""
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import binomtest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1  # noqa: E402
import t6_f0_headroom as H  # noqa: E402
import tie_reference as TR  # noqa: E402

OUT = "results/T7_confirmatory_marg_norm.csv"
CEILING = "results/T5_inertness_ceiling.json"
RECOMPUTE = "results/T7_marg_norm_recompute.json"


def table():
    df, cols, A, ext, MN = H.item_axis(with_marg=True)
    ids, tiles = df["item_id"].values, df["tile"].values
    conf = np.isfinite(cols["beta_c"]) & (tiles == "size")   # domain from beta_c, T7.md note 1
    rows = []
    for j in np.where(conf)[0]:
        i = int(ids[j])
        for o, (m, a) in enumerate(zip(MN[i], A[i])):
            rows.append({"item_id": i, "option": o, "marg_norm": float(m),
                         "A": float(a), "ext_i": float(ext[j]),
                         "beta_c": float(cols["beta_c"][j]),
                         "o_star_0": int(cols["o0"][j]),
                         "is_o_star_0": o == int(cols["o0"][j])})
    t = pd.DataFrame(rows)
    assert t["item_id"].nunique() == 108, t["item_id"].nunique()
    return t


def main():
    t = table()
    t.to_csv(OUT, index=False, float_format="%.17g")   # 17 digits round-trips float64
    back = pd.read_csv(OUT, float_precision="round_trip")
    for c in ("marg_norm", "A", "ext_i"):
        assert np.array_equal(back[c].values, t[c].values), f"{c} does not round-trip"
    print(f"{t['item_id'].nunique()} items, {len(t)} option rows\nwritten: {OUT}\n"
          f"sha256 {p1.artifact_hash(OUT)}")
    return 0


def demo():
    """Recompute c5's sign proportion, n_eff and blind spot from the CSV's
    marg_norm alone, and compare to what inertness_ceiling.py reported."""
    t = pd.read_csv(OUT, float_precision="round_trip")
    mn = {i: g.sort_values("option")["marg_norm"].values for i, g in t.groupby("item_id")}
    ch = TR.load_choices()
    want = json.load(open(CEILING))["diagnostic_c5_direction"]["per_model"]
    bad = []
    for m, w in want.items():
        g = ch[(ch["model"] == m) & (ch["prompt_form"] == TR.FORM)
               & (ch["rule"] == TR.RULE) & ch["item_id"].isin(mn)
               & ch["permutation_id"].notna()]
        p = g.pivot_table(index=["item_id", "permutation_id"], columns="condition",
                          values="chosen_option", aggfunc="first").dropna()
        it = p.index.get_level_values("item_id").values
        d = np.array([np.sign(mn[i][int(b)] - mn[i][int(a)])
                      for i, a, b in zip(it, p["cond4"], p["cond5"])])
        n_eff, pos = int((d != 0).sum()), int((d > 0).sum())
        same = float((p["cond4"].values == p["cond5"].values).mean())
        got = {"n_eff": n_eff, "n_positive": pos, "sign_proportion": pos / n_eff,
               "blind_spot": float((d == 0).mean()) - same,
               "p_two_sided": binomtest(pos, n_eff, 0.5).pvalue}
        for k, v in got.items():
            if abs(v - w[k]) > 1e-12:
                bad.append((m, k, v, w[k]))
        print(f"  {m:5s} n_eff={n_eff:3d} pos={pos:3d} prop={got['sign_proportion']:.4f} "
              f"blind_spot={got['blind_spot']:.4f}")
    # Not asserted away. A disagreement here is a float-equivalence break of
    # P2-D15's identity sign(dA) = sign(d marg_norm), and it is reported as data.
    json.dump({"source": CEILING, "csv": OUT,
               "csv_sha256": p1.artifact_hash(OUT),
               "disagreements": [{"model": m, "field": k, "from_marg_norm": v,
                                  "reported": r} for m, k, v, r in bad],
               "a_vs_marg_norm_tie_disagreements": [
                   {"item_id": int(i), "options": [int(x), int(y)],
                    "marg_norm": [float(g.marg_norm.iat[x]), float(g.marg_norm.iat[y])],
                    "A": [float(g.A.iat[x]), float(g.A.iat[y])]}
                   for i, g in t.sort_values(["item_id", "option"]).groupby("item_id")
                   for x in range(len(g)) for y in range(x + 1, len(g))
                   if (g.A.iat[x] == g.A.iat[y]) != (g.marg_norm.iat[x] == g.marg_norm.iat[y])],
               "note": "A disagreement is a float-equivalence break of P2-D15's "
                       "identity sign(dA) = sign(d marg_norm). No tolerance is "
                       "introduced to pick one reading."},
              open(RECOMPUTE, "w"), indent=2)
    print(f"{'DISAGREES' if bad else 'ok'}: {len(bad)} field(s) differ from "
          f"{CEILING}; written {RECOMPUTE}")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
