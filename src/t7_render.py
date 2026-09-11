"""T7's stimulus table: 1,000 items x 2 permutations x 3 framings, with a manifest.

Built locally and verified locally, so the only thing Kaggle has to do is score
it. Splitting the two is deliberate: rendering is deterministic and checkable
without a GPU, and a rendering bug found on Kaggle costs a T4 session.

`F0` is Paper 1's Format V `base` text, taken from P1's frozen
`items_rendered.parquet` rather than regenerated, so it is Paper 1's prompt by
construction and not a reproduction of it. `src/framings.py` section 2 already
verified that regenerating gives the frozen text byte for byte on all 2,000
Format V base renderings; this module does not repeat that, it just uses the
frozen column.

SCOPE, per `T7.md`: all 1,000 items, both permutations, three framings. The
`size`-tile 108 remains the confirmatory set (P2-D3, P2-D4). The full set is
needed because the `beta_c = infinity` control runs on the 540 non-divergent
items and the `F0` replication is stronger on the full set.

Run: python3 src/t7_render.py          (writes data/processed/t7_stimuli.parquet)
     python3 src/t7_render.py --demo   (self-check: F0 identity, block leak, counts)
"""
import hashlib
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import framings as FR  # noqa: E402
import p1  # noqa: E402
import p2_decisions as P2D  # noqa: E402

OUT = "data/processed/t7_stimuli.parquet"
MANIFEST = "data/processed/t7_stimuli_manifest.json"
RENDERED = os.path.join(p1.P1_ROOT, "data/processed/items_rendered.parquet")


def build():
    """One row per (item, permutation, framing). F0 is the frozen text verbatim."""
    V = pd.read_parquet(RENDERED)
    V = V[(V["format"] == "V") & (V["variant"] == "base")].reset_index(drop=True)
    rows = []
    for r in V.itertuples():
        for framing in P2D.P2_FRAMING_IDS:
            txt = FR.splice(r.text, FR.FRAMINGS[framing])
            rows.append({
                "item_id": int(r.item_id), "tile": r.tile, "format": "V",
                "permutation_id": int(r.permutation_id),
                "option_order": list(map(int, r.option_order)),
                "framing": framing,
                "n_options": int(r.n_options),
                "n_chars": len(txt), "n_words": len(txt.split()),
                "text": txt,
            })
    return pd.DataFrame(rows)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    S = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    S.to_parquet(OUT, index=False)
    man = {
        "purpose": "T7 Arm B stimuli. Scored on Kaggle T4s; rendered and checked "
                   "here so a rendering bug does not cost a T4 session.",
        "scope": "all 1,000 items, 2 permutations, 3 framings, Format V base",
        "confirmatory_subset": f"{P2D.P2D3_TILE} tile, "
                               f"n = {P2D.P2D4_N_CONFIRMATORY} with finite beta_c "
                               "(P2-D3, P2-D4)",
        "n_rows": int(len(S)),
        "n_items": int(S["item_id"].nunique()),
        "per_framing": {k: int(v) for k, v in S["framing"].value_counts().items()},
        "per_tile": {k: int(v) for k, v in S["tile"].value_counts().items()},
        "framing_ids": list(P2D.P2_FRAMING_IDS),
        "variant": P2D.P2D1_VARIANT,
        "slot_anchor": P2D.P2D2_SLOT_ANCHOR,
        "f0_replication_target": P2D.P2_F0_REPLICATION_TARGET,
        "source_items_rendered_sha256": sha256(RENDERED),
        "items_final_sha256": P2D.P2D4_ITEMS_SHA256,
        "stimuli_sha256": sha256(OUT),
        "median_chars": {k: int(g["n_chars"].median())
                         for k, g in S.groupby("framing")},
        "batch_rule": "D102 part 3: the `size` tile is scored at max_batch = 1. "
                      "P1 does this because size carries the primary curve and "
                      "is where margins inside the fp16 noise floor sit. T7 "
                      "inherits it, and size is also the confirmatory tile.",
    }
    json.dump(man, open(MANIFEST, "w"), indent=2)
    print(f"{len(S):,} renderings, {S['item_id'].nunique():,} items")
    for k, g in S.groupby("framing"):
        print(f"  {k}  {len(g):,} rows  median {int(g['n_chars'].median()):,} chars")
    print(f"\n  sha256 stimuli  {man['stimuli_sha256']}")
    print(f"  written: {OUT}\n           {MANIFEST}")
    return 0


def demo():
    """Three checks, each of which has to hold before any GPU time is spent.

    F0 must be the frozen text byte for byte, not a re-render. F1 and F2 must
    reduce to F0 by removing their block, which is the leak check: a block
    carrying anything item-specific would fail to unsplice on some item. And the
    counts must match the declared scope.
    """
    V = pd.read_parquet(RENDERED)
    V = V[(V["format"] == "V") & (V["variant"] == "base")].reset_index(drop=True)
    S = build()
    f0 = S[S["framing"] == "F0"].reset_index(drop=True)
    assert (f0["text"].values == V["text"].values).all(), \
        "F0 is not Paper 1's frozen text byte for byte"
    n_bad = 0
    for framing in ("F1", "F2"):
        blk = FR.FRAMINGS[framing]
        g = S[S["framing"] == framing].reset_index(drop=True)
        for txt, want in zip(g["text"].values, V["text"].values):
            if FR.unsplice(txt, blk) != want:
                n_bad += 1
    assert n_bad == 0, f"{n_bad} renderings do not unsplice back to F0"
    assert len(S) == len(V) * 3 == 6000, len(S)
    assert S["item_id"].nunique() == 1000, S["item_id"].nunique()
    assert set(S["framing"]) == set(P2D.P2_FRAMING_IDS)
    assert (S.groupby("framing")["item_id"].nunique() == 1000).all()
    # the menu must still be contiguous in the spliced text, or score_rows raises
    tiles = {t["id"]: t for t in json.load(open(p1.TILES))["tiles"]}
    miss = 0
    for r in S.sample(300, random_state=7).itertuples():
        opts = [tiles[r.tile]["options"][i] for i in r.option_order]
        if "\n".join(f"  {o}" for o in opts) not in r.text:
            miss += 1
    assert miss == 0, f"{miss} spliced prompts no longer contain the rendered menu"
    print(f"ok: F0 byte-identical to P1's frozen renderings on {len(f0):,} rows; "
          f"F1 and F2 unsplice back to F0 on all {len(V) * 2:,}; "
          f"{len(S):,} rows over {S['item_id'].nunique():,} items; menu intact")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
