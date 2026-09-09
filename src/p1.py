"""Bridge to the frozen Paper 1 artifacts.

Nothing in this module recomputes anything Paper 1 already computes. The fit
function, the min-aggregation, the tie-break rule and the rating-column spec are
all imported from P1's own `src/`; only the *assembly* into a P2 item batch
lives here.

P1 root is taken from `$P1_ROOT`, defaulting to the path recorded in
`docs/spec/adversary-game-v1.md`.

Run: python3 src/p1.py     (prints an artifact inventory)
"""
import functools
import json
import os
import sys

import numpy as np
import pandas as pd

P1_ROOT = os.environ.get(
    "P1_ROOT", "/Users/crishuynh/Documents/SoftwareProject/deception")

if not os.path.isdir(os.path.join(P1_ROOT, "src")):
    raise FileNotFoundError(
        f"Paper 1 codebase not found at {P1_ROOT!r}. Set $P1_ROOT. "
        "P2 imports P1's frozen fit function; it does not carry a copy.")
if os.path.join(P1_ROOT, "src") not in sys.path:
    sys.path.insert(0, os.path.join(P1_ROOT, "src"))

# Frozen P1 code, by import. Copying any of this would be a duplication bug.
from fit import fit_matrix, pair_fit                      # noqa: E402
from score_items import SPEC, SIZE_CAP                    # noqa: E402
from tiebreak import lex_obayes, TAU_MAIN                 # noqa: E402

POOL = os.path.join(P1_ROOT, "data/processed/concept_pool.csv")
TILES = os.path.join(P1_ROOT, "data/reference/tiles.json")
RATINGS = os.path.join(P1_ROOT, "data/raw/jum2f/02_object-level/_property-ratings.tsv")
ITEMS_FINAL = os.path.join(P1_ROOT, "data/processed/items_final.parquet")
ITEMS_CANDIDATE = os.path.join(P1_ROOT, "data/processed/items_candidate.parquet")


@functools.lru_cache(maxsize=1)
def tile_fits():
    """{tile_id: (F, options)}. `F` is the (n_concepts, |O|) fit matrix.

    A pure function of three frozen files, so the cache cannot change a result;
    it only avoids re-reading them. Reproduces `score_items.main`'s `F0`
    construction, which is the code path that produced the frozen `o_bayes`.
    """
    pool = pd.read_csv(POOL)
    tiles = {t["id"]: t for t in json.load(open(TILES))["tiles"]}
    r2 = pd.read_csv(RATINGS, sep="\t").set_index("uniqueID").loc[pool["uniqueID"]]
    out = {}
    for tid, t in tiles.items():
        mean_col = SPEC[tid][0]
        iv = [(b["lower"], b["upper"]) for b in t["bin_intervals"]]
        v = r2[mean_col].values.astype(float)
        if tid == "size":
            v = np.minimum(v, SIZE_CAP)
        out[tid] = (fit_matrix(v, iv), list(t["options"]))
    return out


def fit_grid(tile, means, clues):
    """(n, |H|, |O|) array of `f(o, h)` for `n` items on one tile.

    `h` is the flattened Means x Clue index, `h = m * C + c`, matching P1's
    `reshape(M * C, -1)` in `oracle.run_items` and `score_items.grid_stats`.
    """
    F = tile_fits()[tile][0]
    G = pair_fit(F[means][:, :, None, :], F[clues][:, None, :, :])
    n, M, C, K = G.shape
    return G.reshape(n, M * C, K)


def artifact_hash(path):
    """sha256 of a frozen P1 artifact, for the chain of custody.

    P1 gitignores `data/**`, so P2 cannot pin these by commit. Hashing them into
    P2's reports is the available substitute.
    """
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_items(path=ITEMS_FINAL, tile=None, n=None):
    """Frozen P1 item table, optionally one tile / first `n` rows."""
    df = pd.read_parquet(path)
    if tile is not None:
        df = df[df["tile"] == tile]
    return df.iloc[:n].reset_index(drop=True) if n else df.reset_index(drop=True)


def main():
    print(f"P1_ROOT = {P1_ROOT}")
    for name, p in [("items_final", ITEMS_FINAL), ("items_candidate", ITEMS_CANDIDATE)]:
        if os.path.exists(p):
            df = pd.read_parquet(p, columns=["tile"])
            print(f"  {name:16s} {len(df):>7,} rows  "
                  + "  ".join(f"{k}={v}" for k, v in df['tile'].value_counts().items()))
        else:
            print(f"  {name:16s} MISSING at {p}")
    for name, path in [("items_final", ITEMS_FINAL), ("items_candidate", ITEMS_CANDIDATE)]:
        if os.path.exists(path):
            print(f"  sha256 {name:16s} {artifact_hash(path)}")
    for tid, (F, opts) in sorted(tile_fits().items()):
        print(f"  tile {tid:8s} |O|={len(opts)}  fit range "
              f"[{F.min():.4e}, {F.max():.4f}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
