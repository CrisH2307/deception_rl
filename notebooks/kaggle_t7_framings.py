"""T7 Arm B: score F0/F1/F2 on Paper 1's seven-model ladder. RUNS ON KAGGLE T4s.

This is the only part of T7 that needs a GPU. Rendering is done and checked
locally by `src/t7_render.py`; this file scores `data/processed/t7_stimuli.parquet`
and writes one parquet of choices. Analysis happens locally afterwards.

It is a `.py` rather than a notebook so it can be diffed, imported and tested.
On Kaggle, upload it with the repo and run `%run kaggle_t7_framings.py`, or paste
it into one cell.

WHAT IT INHERITS FROM PAPER 1, AND WHY EACH ONE MATTERS.

  Harness.     `score_llm.score_rows` / `score_llm.pick`, imported from P1's src.
               Not reimplemented. A copy would be the duplication bug CLAUDE.md
               names.
  Revisions.   Every repo pinned to the commit Paper 1 resolved. Never a
               near-name (P1's D95).
  D102 part 3. The `size` tile is scored at `max_batch = 1`. P1 does this because
               size carries the primary curve and is where margins inside the
               fp16 noise floor sit. It is also Paper 2's confirmatory tile
               (P2-D3), so T7 inherits the rule rather than re-deciding it.
  D104.        The PMI neutral prompt is menu-only and excludes the `{extra}`
               slot, so the normalisation is identical under F0, F1 and F2
               (P2-D2). One neutral cache per model, shared across framings.
  D109.        All three scoring rules recorded, not only `pmi`.
  D111.        The control's tokenizer class is recorded and asserted to differ.
  D117.        The full per-option score vector is kept, not just the argmax.

WHAT IS NEW HERE, AND WHY.

  F0-versus-cond4 disagreement.  P2-D13 sets the inertness floor to
  `max(7, this count)` on the confirmatory items. F0 is Paper 1's `cond4` prompt
  byte for byte (P2-D1), so a disagreement is pure environment noise: identical
  text, different run. It is also the first empirical measurement of the
  no-effect rate `PREREGISTRATION_v2.6.md` section 1.1 could only argue from the
  code path. Reported per model and in total.

  Determinism assert.  Re-score one tile on the loaded model and require
  bit-identical output, as P1's own notebook does. If this fails, stop: the floor
  calibration assumes within-session determinism and everything below inherits it.
"""
import gc
import json
import os
import sys
import time

import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

P1_SRC = os.environ.get("P1_SRC", "/kaggle/input/deception-p1/src")
P2_SRC = os.environ.get("P2_SRC", "/kaggle/input/deception-p2/src")
for p in (P1_SRC, P2_SRC):
    if p not in sys.path:
        sys.path.insert(0, p)

import coords            # noqa: E402  P1
import score_llm         # noqa: E402  P1

STIMULI = os.environ.get("T7_STIMULI", "/kaggle/input/deception-p2/data/processed/t7_stimuli.parquet")
TILES_JSON = os.environ.get("T7_TILES", "/kaggle/input/deception-p1/data/reference/tiles.json")
ITEMS = os.environ.get("T7_ITEMS", "/kaggle/input/deception-p1/data/processed/items_final.parquet")
P1_CHOICES = os.environ.get("T7_P1_CHOICES", "")   # optional: for the F0 check here
OUTDIR = "/kaggle/working" if os.path.isdir("/kaggle/working") else "./outputs"
CKPT = os.path.join(OUTDIR, "ckpt")

DTYPE = torch.float16
CONFIRMATORY_TILE = "size"       # P2-D3
BATCH_DEFAULT = 8
PROVISIONAL_FLOOR = 7            # P2-D13; the local analysis re-derives the rule

# Pinned exactly as Paper 1 resolved them. Do not substitute a near-name (D95).
MODELS = {
    "L1":   ("Qwen/Qwen3-0.6B",             "c1899de289a04d12100db370d81485cdf75e47ca", "qwen3"),
    "L2":   ("Qwen/Qwen3-1.7B",             "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e", "qwen3"),
    "L3":   ("Qwen/Qwen3-4B",               "1cfa9a7208912126459214e8b04321603b3df60c", "qwen3"),
    "L4":   ("Qwen/Qwen3-8B",               "b968826d9c46dd6066d109eabc6255188de91218", "qwen3"),
    "B2":   ("Qwen/Qwen3-1.7B-Base",        "ea980cb0a6c2ae4b936e82123acc929f1cec04c1", "qwen3-base"),
    "B4":   ("Qwen/Qwen3-8B-Base",          "49e3418fbbbca6ecbdf9608b4d22e5a407081db4", "qwen3-base"),
    "CTRL": ("allenai/OLMo-2-1124-7B-Instruct",
             "470b1fba1ae01581f270116362ee4aa1b97f4c84", "control"),
}
# D115: the thinking-toggle assert is scoped by the property, not by family.
# Base models run a borrowed template and the control has no thinking mode.
NATIVE_THINKING = {"L1", "L2", "L3", "L4"}

ENV = {}


def records(rung, rev, framing, rows, scored, ROWS):
    out = []
    for ridx, d in scored.items():
        r = rows.loc[ridx]
        for rule in ("pmi", "sum", "mean"):
            picks = score_llm.pick(d[rule])
            rec = coords.coord(ROWS, r["item_id"], picks)
            rec.update(item_id=int(r["item_id"]), tile=r["tile"],
                       framing=framing, model=rung, revision=rev, format="V",
                       permutation_id=int(r["permutation_id"]), rule=rule,
                       backend="kaggle-cuda", n_options=int(len(d[rule])),
                       logp_sum_chosen=float(d["sum"][picks[0]]) if len(picks) == 1 else np.nan,
                       logp_neutral_chosen=float(d["logp_neutral"][picks[0]]) if len(picks) == 1 else np.nan,
                       scores=[float(x) for x in d[rule]],
                       unscored_reason="")
            out.append(rec)
    return out


def run_rung(rung, S, TILES, ROWS, max_batch=BATCH_DEFAULT):
    repo, rev, family = MODELS[rung]
    done = os.path.join(CKPT, f"t7_{rung}.parquet")
    if os.path.exists(done):
        print(f"{rung}: checkpoint present, skipping")
        return pd.read_parquet(done)
    print(f"\n=== {rung}  {repo}  {rev[:12]} ===", flush=True)
    tok = AutoTokenizer.from_pretrained(repo, revision=rev)
    model = AutoModelForCausalLM.from_pretrained(
        repo, revision=rev, dtype=DTYPE, device_map="auto").eval()
    ENV.setdefault("tokenizer_class", {})[rung] = type(tok).__name__

    native = rung in NATIVE_THINKING
    score_llm.self_check(tok, TILES, rendered=S, assert_thinking=native,
                         exempt_reason=None if native else
                         f"{family}: no native thinking mode (D115)")

    NCACHE = {}                    # D104 neutrals, shared across framings
    recs, t0 = [], time.time()
    for tid in TILES:
        part = os.path.join(CKPT, f"t7_{rung}_{tid}.parquet")
        if os.path.exists(part):
            recs.append(pd.read_parquet(part))
            print(f"  {tid}: cached")
            continue
        # D102 part 3. `size` is the confirmatory tile (P2-D3) and is where the
        # margins inside the fp16 noise floor sit, so it is never batched.
        mb = 1 if tid == CONFIRMATORY_TILE else max_batch
        got = []
        for framing in ("F0", "F1", "F2"):
            rows_t = S[(S["tile"] == tid) & (S["framing"] == framing)]
            sc = score_llm.score_rows(model, tok, rows_t, TILES, "cuda",
                                      cache=NCACHE, max_batch=mb)
            got += records(rung, rev, framing, rows_t, sc, ROWS)
        d = pd.DataFrame(got)
        d.to_parquet(part, index=False)
        recs.append(d)
        print(f"  {tid}: {len(d):,} rows  batch={mb}  "
              f"{time.time() - t0:.0f}s elapsed", flush=True)

    pd.DataFrame([{"tile": k[0], "option_order": str(list(k[1])),
                   "option_index": i, "logp_sum": v[0], "logp_mean": v[1],
                   "n_tokens": v[2], "model": rung}
                  for k, vs in NCACHE.items() for i, v in enumerate(vs)]).to_csv(
        os.path.join(CKPT, f"t7_neutral_{rung}.csv"), index=False)

    D = pd.concat(recs, ignore_index=True)
    D.to_parquet(done, index=False)
    del model
    gc.collect()
    torch.cuda.empty_cache()
    print(f"{rung} done: {len(D):,} rows in {time.time() - t0:.0f}s")
    return D


def determinism_gate(rung, S, TILES):
    """Re-score one tile twice on the loaded model. Bit-identical or stop.

    P2-D13's floor calibration assumes within-session determinism. If this fails
    the assumption is wrong and the F0 disagreement count stops being a clean
    measurement of cross-session noise.
    """
    repo, rev, _ = MODELS[rung]
    tok = AutoTokenizer.from_pretrained(repo, revision=rev)
    m = AutoModelForCausalLM.from_pretrained(repo, revision=rev, dtype=DTYPE,
                                             device_map="auto").eval()
    sub = S[(S["tile"] == "manmade") & (S["framing"] == "F1")].head(64)
    cache = {}
    a = score_llm.score_rows(m, tok, sub, TILES, "cuda", cache=cache)
    b = score_llm.score_rows(m, tok, sub, TILES, "cuda", cache=cache)
    diff = max(float(np.abs(a[i]["pmi"] - b[i]["pmi"]).max()) for i in a)
    ENV["determinism"] = {"model": rung, "tile": "manmade", "framing": "F1",
                          "n": int(len(sub)), "bit_identical": bool(diff == 0.0),
                          "max_abs_diff": diff}
    print("determinism:", ENV["determinism"])
    del m
    gc.collect()
    torch.cuda.empty_cache()
    assert diff == 0.0, (
        f"scorer is not deterministic within the session: max diff {diff:.3e}. "
        "P2-D13's floor calibration assumes it is. Stop and report.")


def f0_disagreement(ALL, p1_choices_path):
    """T7's F0 against Paper 1's frozen cond4. Identical text, different run.

    This is P2-D13's measured noise floor and the first empirical check on the
    no-effect rate. Returns per-model counts on the confirmatory tile.
    """
    if not p1_choices_path or not os.path.exists(p1_choices_path):
        print("F0 check: P1 choices not mounted here; run it locally instead")
        return None
    P = pd.read_parquet(p1_choices_path)
    if "prompt_form" in P.columns:
        P = P[P["prompt_form"] == "template"]
    P = P[(P["condition"] == "cond4") & (P["format"] == "V")
          & (P["rule"] == "pmi") & (P["n_tied"] == 1)]
    T = ALL[(ALL["framing"] == "F0") & (ALL["rule"] == "pmi")
            & (ALL["n_tied"] == 1)]
    key = ["model", "item_id", "permutation_id"]
    j = T.merge(P[key + ["chosen_option"]], on=key, suffixes=("_t7", "_p1"))
    j["disagree"] = j["chosen_option_t7"] != j["chosen_option_p1"]
    out = {}
    for (m, tile), g in j.groupby(["model", "tile"]):
        out.setdefault(m, {})[tile] = {
            "renderings": int(len(g)), "disagreeing_renderings": int(g["disagree"].sum()),
            "items": int(g["item_id"].nunique()),
            "disagreeing_items": int(g[g["disagree"]]["item_id"].nunique()),
        }
    return out


def main():
    os.makedirs(CKPT, exist_ok=True)
    S = pd.read_parquet(STIMULI)
    TILES = {t["id"]: t for t in json.load(open(TILES_JSON))["tiles"]}
    ROWS = pd.read_parquet(ITEMS)
    print(f"{len(S):,} renderings, {S['item_id'].nunique():,} items, "
          f"framings {sorted(S['framing'].unique())}")

    determinism_gate("L1", S, TILES)

    ALL = pd.concat([run_rung(k, S, TILES, ROWS) for k in MODELS],
                    ignore_index=True)
    # D111: the control's tokenizer must differ, asserted rather than remembered.
    tc = ENV.get("tokenizer_class", {})
    ENV["d111"] = {"tokenizer_class": tc,
                   "control_differs": tc.get("CTRL") not in
                   {tc.get(k) for k in MODELS if k != "CTRL"}}
    assert ENV["d111"]["control_differs"], (
        "the cross-family control shares a tokenizer class with the ladder; "
        "D111's premise does not hold and the restriction needs re-deriving")

    ENV["f0_vs_cond4"] = f0_disagreement(ALL, P1_CHOICES)
    ENV["provisional_floor"] = PROVISIONAL_FLOOR
    ALL.to_parquet(os.path.join(OUTDIR, "choices_t7.parquet"), index=False)
    json.dump(ENV, open(os.path.join(OUTDIR, "env_t7.json"), "w"), indent=2,
              default=str)
    print(f"\ntotal rows: {len(ALL):,}")
    print(f"written: {OUTDIR}/choices_t7.parquet")
    print(f"         {OUTDIR}/env_t7.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
