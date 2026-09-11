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

DRIVEN BY `notebooks/kaggle_t7.ipynb`, which stages the launch and holds at the
F0 verdict. Everything the notebook needs is a function here: `capture_env`,
`verify_inputs`, `assert_no_sampling`, `scan_checkpoints`, `plan_run`,
`run_rung`, `export`. `main()` still runs the whole thing unstaged, for a
non-interactive re-run once the verdict has been read.

CHECKPOINTS. Per `(model, tile)`, written the moment the tile finishes, never
accumulated in memory. On start `scan_checkpoints` verifies each one's row count
against what the stimuli imply and quarantines any that disagree, which is what a
session killed mid-write leaves behind. A checkpoint scheme that has never
resumed is an assumption, so `simulate_kill_and_resume` exercises the path
without a GPU.
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

P2_ROOT = os.environ.get("P2_ROOT", "/kaggle/input/deception-p2")
P1_ROOT_K = os.environ.get("P1_ROOT_K", "/kaggle/input/deception-p1")
P1_NOTEBOOKS = os.environ.get("P1_NOTEBOOKS", os.path.join(P1_ROOT_K, "notebooks"))
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

# Paper 1's own resolved commits, from notebooks/results_2/env.json
# (`qwen_revisions`) and results_3/env.json (`models`). This constant is the
# source; `capture_env` cross-checks it against those files when the P1 dataset
# is mounted, so a transcription error fails rather than propagating.
P1_RECORDED_REVISIONS = {k: v[1] for k, v in MODELS.items()}

# Scaled from P1's recorded 2.33 GPU-hours for L4 on 2x T4 (results_2/env.json,
# `l4_cost_hours`) by 1.50x renderings and 1.28x prompt length, then by parameter
# count. An estimate, printed so divergence is visible early, never a budget cap.
ESTIMATE_HOURS = {"L1": 0.33, "L2": 0.95, "L3": 2.23, "L4": 4.46,
                  "B2": 0.95, "B4": 4.46, "CTRL": 3.90}
N_RULES = 3                      # D109: pmi, sum, mean, all recorded

# Paper 1's measured batch-composition flip rates, for context beside T7's own
# F0 disagreement count. results_2 and results_3 `batch_sensitivity.csv`:
# 11 flips in 2,100 renderings over 21 model-by-tile cells, 0.00 to 0.02 per
# cell. The `size` tile is absent because P1 scores it at batch 1 by design,
# which is the rule T7 inherits.
P1_FLIP_RATES = {"L1": 0.010, "L2": 0.000, "L3": 0.003, "L4": 0.013,
                 "B2": 0.007, "B4": 0.003, "CTRL": 0.000}
P1_FLIP_NOTE = ("P1's batch-8-vs-batch-1 flip rates on manmade/moves/hold, "
                "pooled per model. Not the size tile, which P1 and T7 both "
                "score at batch 1. Context for T7's F0 count, not a threshold.")


def _sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def capture_env(path=None):
    """Versions, devices and pinned commits, written BEFORE any model loads.

    Written first so the file exists even if the session is killed during the
    first load, which is when a session is most likely to die.

    The pinned commits are cross-checked against Paper 1's own `env.json` when
    the P1 dataset is mounted. A near-name or a drifted revision fails here
    rather than producing a run that silently scored different weights (P1's
    D95).
    """
    import platform
    env = {
        "captured_utc": pd.Timestamp.utcnow().isoformat(),
        "python": sys.version.split()[0], "platform": platform.platform(),
        "torch": torch.__version__, "numpy": np.__version__,
        "pandas": pd.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
        "cuda_version": torch.version.cuda,
        "cudnn": torch.backends.cudnn.version() if torch.cuda.is_available() else None,
        "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "devices": [], "dtype": str(DTYPE),
        "models": {k: {"repo": v[0], "revision": v[1], "family": v[2]}
                   for k, v in MODELS.items()},
        "estimate_hours": ESTIMATE_HOURS,
        "p1_flip_rates": P1_FLIP_RATES, "p1_flip_note": P1_FLIP_NOTE,
    }
    for i in range(env["device_count"]):
        p = torch.cuda.get_device_properties(i)
        free, total = torch.cuda.mem_get_info(i)
        env["devices"].append({"index": i, "name": p.name,
                               "capability": f"{p.major}.{p.minor}",
                               "total_MiB": total // 2 ** 20,
                               "free_MiB": free // 2 ** 20})
    for mod in ("transformers", "tokenizers", "accelerate", "safetensors"):
        try:
            env[mod] = __import__(mod).__version__
        except Exception as e:                                # noqa: BLE001
            env[mod] = f"UNAVAILABLE: {type(e).__name__}"

    # cross-check the pins against Paper 1's own record
    checked, problems = {}, []
    for rel, key in (("results_2/env.json", "qwen_revisions"),
                     ("results_3/env.json", "models")):
        f = os.path.join(P1_NOTEBOOKS, rel)
        if not os.path.exists(f):
            continue
        for rung, rec in json.load(open(f)).get(key, {}).items():
            checked[rung] = rec["revision"]
            want = P1_RECORDED_REVISIONS.get(rung)
            if want is None:
                problems.append(f"{rung}: in P1's record, absent from MODELS")
            elif rec["revision"] != want:
                problems.append(
                    f"{rung}: P1 recorded {rec['revision'][:12]}, "
                    f"MODELS pins {want[:12]}")
            elif rec["repo"] != MODELS[rung][0]:
                problems.append(
                    f"{rung}: P1 recorded repo {rec['repo']}, "
                    f"MODELS uses {MODELS[rung][0]}")
    env["p1_revision_crosscheck"] = {
        "p1_env_found": bool(checked), "n_checked": len(checked),
        "problems": problems,
        "note": "P1's env.json not mounted; pins verified against the module "
                "constant only" if not checked else "verified against P1's own "
                "env.json",
    }
    ENV.update(env)
    path = path or os.path.join(OUTDIR, "env_t7.json")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    json.dump(ENV, open(path, "w"), indent=2, default=str)
    if problems:
        raise AssertionError(
            "pinned revisions disagree with Paper 1's own record:\n  "
            + "\n  ".join(problems)
            + "\nP1's env.json is the record. Do not edit MODELS to pass.")
    return ENV


def verify_inputs(stimuli=None, items=None, gate_record=None, manifest=None):
    """Hash the two inputs against what the earlier sessions recorded.

    A stale dataset upload is the failure this catches, and it is otherwise
    silent: the run completes, the numbers are wrong, and nothing says so.
    `items_final.parquet` is checked against T6's gate record, which is where the
    kill gate wrote it; `t7_stimuli.parquet` against the manifest T7's rendering
    session wrote beside it.
    """
    stimuli = stimuli or STIMULI
    items = items or ITEMS
    gate_record = gate_record or os.path.join(P2_ROOT, "results/T6_gate_record.json")
    manifest = manifest or os.path.splitext(stimuli)[0] + "_manifest.json"
    out, problems = {}, []
    for label, path, want in (
            ("items_final.parquet", items,
             (json.load(open(gate_record))["artifact_sha256"]["items_final.parquet"]
              if os.path.exists(gate_record) else None)),
            ("t7_stimuli.parquet", stimuli,
             (json.load(open(manifest))["stimuli_sha256"]
              if os.path.exists(manifest) else None))):
        if not os.path.exists(path):
            problems.append(f"{label}: missing at {path}")
            continue
        got = _sha256(path)
        out[label] = {"path": path, "sha256": got, "expected": want,
                      "matches": (want is None or got == want)}
        if want is None:
            problems.append(f"{label}: no recorded hash to check against")
        elif got != want:
            problems.append(f"{label}: sha256 {got[:16]} != recorded {want[:16]}")
    ENV["input_verification"] = out
    if problems:
        raise AssertionError(
            "input verification failed:\n  " + "\n  ".join(problems)
            + "\nRe-upload the dataset. A stale input is silent otherwise.")
    return out


def assert_no_sampling():
    """P2-D9 rests on the scorer being an argmax over teacher-forced log-probs.

    Asserted against the harness source rather than trusted, because every
    decision from P2-D9 onward inherits it: the exact null of 0, the inertness
    floor, the reading of the c5 reference.
    """
    import inspect
    src = inspect.getsource(score_llm)
    banned = (".generate(", "do_sample", "temperature", "top_p", "top_k",
              "multinomial")
    hits = [b for b in banned if b in src]
    ok = {"module": score_llm.__file__, "banned_tokens_found": hits,
          "pick_is_argmax": "argmax" in inspect.getsource(score_llm.pick).lower()
          or "flatnonzero" in inspect.getsource(score_llm.pick)}
    ENV["no_sampling_check"] = ok
    if hits:
        raise AssertionError(
            f"sampling tokens present in {score_llm.__file__}: {hits}. P2-D9 and "
            "everything downstream assume a deterministic argmax scorer.")
    assert ok["pick_is_argmax"], "score_llm.pick is not an argmax over the scores"
    return ok


def expected_rows(S, tile):
    """Rows a completed `(model, tile)` checkpoint must carry.

    Derived from the stimuli rather than hardcoded, so a scope change moves this
    with it instead of silently invalidating every resume check.
    """
    return int((S["tile"] == tile).sum()) * N_RULES


def scan_checkpoints(S, models=None, ckpt=None, quarantine=True):
    """What is already done, what is short, what is still to run.

    A session killed mid-write leaves a parquet that reads but is short, or one
    that does not read at all. Both are treated the same way: not trusted, moved
    aside, and re-run. Trusting a short checkpoint would drop renderings from the
    export and the completeness check at the end is the only thing that would
    notice.
    """
    ckpt = ckpt or CKPT
    models = list(models or MODELS)
    tiles = sorted(S["tile"].unique())
    done, bad, todo = {}, {}, []
    for rung in models:
        for tid in tiles:
            part = os.path.join(ckpt, f"t7_{rung}_{tid}.parquet")
            want = expected_rows(S, tid)
            if not os.path.exists(part):
                todo.append((rung, tid))
                continue
            try:
                n = len(pd.read_parquet(part, columns=["item_id"]))
                reason = None if n == want else f"{n:,} rows, expected {want:,}"
            except Exception as e:                            # noqa: BLE001
                n, reason = None, f"unreadable: {type(e).__name__}"
            if reason is None:
                done[(rung, tid)] = n
            else:
                bad[(rung, tid)] = reason
                todo.append((rung, tid))
                if quarantine:
                    os.replace(part, part + ".bad")
    return {"done": done, "bad": bad, "todo": todo, "tiles": tiles,
            "models": models}


def plan_run(S, models=None, ckpt=None, quarantine=True):
    """Print the scan and return it. Called at the top of every stage."""
    p = scan_checkpoints(S, models, ckpt, quarantine)
    print(f"checkpoint scan over {len(p['models'])} model(s) x "
          f"{len(p['tiles'])} tiles")
    print(f"  complete : {len(p['done'])}")
    for (m, t), n in sorted(p["done"].items()):
        print(f"      {m:5s} {t:8s} {n:,} rows")
    if p["bad"]:
        print(f"  QUARANTINED (re-run): {len(p['bad'])}")
        for (m, t), why in sorted(p["bad"].items()):
            print(f"      {m:5s} {t:8s} {why}"
                  + ("  -> moved to .bad" if quarantine else ""))
    print(f"  to run   : {len(p['todo'])}")
    for m, t in p["todo"]:
        print(f"      {m:5s} {t:8s} expected {expected_rows(S, t):,} rows")
    return p


def simulate_kill_and_resume(S, ckpt=None):
    """Exercise the resume path without a GPU, before the real run.

    Writes a deliberately short checkpoint and an unreadable one, scans, and
    requires both to be caught and scheduled for re-run. A checkpoint scheme
    that has never resumed is an assumption, and this is the cheapest place to
    stop it being one.
    """
    ckpt = ckpt or CKPT
    os.makedirs(ckpt, exist_ok=True)
    tile = S["tile"].iloc[0]
    short = os.path.join(ckpt, f"t7___SIMKILL_short_{tile}.parquet")
    trunc = os.path.join(ckpt, f"t7___SIMKILL_trunc_{tile}.parquet")
    good = os.path.join(ckpt, f"t7___SIMKILL_good_{tile}.parquet")
    want = expected_rows(S, tile)
    try:
        pd.DataFrame({"item_id": np.arange(want // 2)}).to_parquet(short, index=False)
        open(trunc, "wb").write(b"PAR1 truncated by a killed session")
        pd.DataFrame({"item_id": np.arange(want)}).to_parquet(good, index=False)
        p = scan_checkpoints(S, models=["__SIMKILL_short", "__SIMKILL_trunc",
                                        "__SIMKILL_good"],
                             ckpt=ckpt, quarantine=True)
        assert ("__SIMKILL_short", tile) in p["bad"], "short checkpoint trusted"
        assert ("__SIMKILL_trunc", tile) in p["bad"], "unreadable checkpoint trusted"
        assert ("__SIMKILL_good", tile) in p["done"], "good checkpoint not reused"
        assert ("__SIMKILL_short", tile) in p["todo"]
        assert ("__SIMKILL_trunc", tile) in p["todo"]
        assert ("__SIMKILL_good", tile) not in p["todo"], "good checkpoint re-run"
        assert not os.path.exists(short) and os.path.exists(short + ".bad")
        assert not os.path.exists(trunc) and os.path.exists(trunc + ".bad")
        # A second scan must be stable ON THE TILE THAT HAS A CHECKPOINT. The
        # other tiles are legitimately still to run, so an empty `todo` is the
        # wrong check here and asserting it would only be testing the fixture.
        p2 = scan_checkpoints(S, models=["__SIMKILL_good"], ckpt=ckpt)
        assert ("__SIMKILL_good", tile) in p2["done"], "reuse is not idempotent"
        assert ("__SIMKILL_good", tile) not in p2["todo"]
        assert p2["bad"] == {}, "a clean checkpoint was quarantined on rescan"
        print(f"ok: resume path exercised on tile {tile!r} "
              f"(expected {want:,} rows)")
        print(f"    short checkpoint  -> caught, quarantined, re-queued")
        print(f"    unreadable file   -> caught, quarantined, re-queued")
        print(f"    complete one      -> reused, not re-run, scan idempotent")
        return True
    finally:
        for f in (short, trunc, good, short + ".bad", trunc + ".bad",
                  good + ".bad"):
            if os.path.exists(f):
                os.remove(f)


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


def run_rung(rung, S, TILES, ROWS, max_batch=BATCH_DEFAULT,
             done_already=None):
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
    skip = {t for (m, t) in (done_already or set()) if m == rung}
    for tid in TILES:
        part = os.path.join(CKPT, f"t7_{rung}_{tid}.parquet")
        if tid in skip and os.path.exists(part):
            recs.append(pd.read_parquet(part))
            print(f"  {tid}: cached, verified by the scan")
            continue
        # D102 part 3. `size` is the confirmatory tile (P2-D3) and is where the
        # margins inside the fp16 noise floor sit, so it is never batched.
        mb = 1 if tid == CONFIRMATORY_TILE else max_batch
        ts = time.time()
        try:
            got = []
            for framing in ("F0", "F1", "F2"):
                rows_t = S[(S["tile"] == tid) & (S["framing"] == framing)]
                sc = score_llm.score_rows(model, tok, rows_t, TILES, "cuda",
                                          cache=NCACHE, max_batch=mb)
                got += records(rung, rev, framing, rows_t, sc, ROWS)
        except torch.cuda.OutOfMemoryError as e:
            # Checkpoint what completed, record which cell failed, keep going.
            # Aborting the session would throw away every tile already paid for.
            torch.cuda.empty_cache()
            ENV.setdefault("failures", []).append(
                {"model": rung, "tile": tid, "error": "OutOfMemoryError",
                 "max_batch": mb, "detail": str(e)[:300]})
            print(f"  {tid}: OOM at batch={mb}. Checkpointed {len(recs)} tile(s); "
                  "recorded and continuing to the next tile.", flush=True)
            continue
        except Exception as e:                                # noqa: BLE001
            ENV.setdefault("failures", []).append(
                {"model": rung, "tile": tid, "error": type(e).__name__,
                 "max_batch": mb, "detail": str(e)[:300]})
            print(f"  {tid}: {type(e).__name__}, recorded and continuing.",
                  flush=True)
            continue
        d = pd.DataFrame(got)
        # Written the moment the tile finishes. Accumulating in memory and
        # writing at the end is what makes a killed session cost everything.
        d.to_parquet(part, index=False)
        recs.append(d)
        el = time.time() - ts
        ENV.setdefault("tile_hours", {})[f"{rung}/{tid}"] = el / 3600.0
        print(f"  {tid}: {len(d):,} rows  batch={mb}  {el / 60:.1f} min  "
              f"({(time.time() - t0) / 60:.1f} min into {rung})", flush=True)

    pd.DataFrame([{"tile": k[0], "option_order": str(list(k[1])),
                   "option_index": i, "logp_sum": v[0], "logp_mean": v[1],
                   "n_tokens": v[2], "model": rung}
                  for k, vs in NCACHE.items() for i, v in enumerate(vs)]).to_csv(
        os.path.join(CKPT, f"t7_neutral_{rung}.csv"), index=False)

    D = pd.concat(recs, ignore_index=True) if recs else pd.DataFrame()
    if not D.empty:
        D.to_parquet(done, index=False)
    del model
    gc.collect()
    torch.cuda.empty_cache()
    used = (time.time() - t0) / 3600.0
    ENV.setdefault("model_hours", {})[rung] = used
    budget_line(rung, used)
    print(f"{rung} done: {len(D):,} rows in {used * 60:.1f} min")
    return D


def budget_line(rung, used_hours):
    """Per-model actual against the estimate, printed as it happens.

    The point is to see divergence at L1, where it costs twenty minutes, rather
    than at the allowance limit with L4 and B4 unscored.
    """
    est = ESTIMATE_HOURS.get(rung)
    tot_used = sum(ENV.get("model_hours", {}).values())
    tot_est = sum(ESTIMATE_HOURS.values())
    ratio = (used_hours / est) if est else float("nan")
    print(f"  BUDGET {rung}: {used_hours:.2f} h used vs {est:.2f} h estimated "
          f"({ratio:.2f}x) | running {tot_used:.2f} / {tot_est:.2f} h")
    if est and ratio > 1.5:
        print(f"  BUDGET WARNING: {rung} ran {ratio:.2f}x the estimate. At this "
              f"rate the full ladder is ~{tot_est * ratio:.0f} h, against a "
              "30 h weekly allowance. Consider stopping after the next model.")
    return {"model": rung, "used_hours": used_hours, "estimate_hours": est,
            "ratio": ratio, "running_used": tot_used, "running_estimate": tot_est}


def export(S, outdir=None, ckpt=None, models=None):
    """Assemble the checkpoints into one parquet, with a completeness check.

    Reads from disk rather than from whatever is in memory, so an export after a
    resumed session is the same artifact as an export after an uninterrupted one.
    """
    outdir, ckpt = outdir or OUTDIR, ckpt or CKPT
    models = list(models or MODELS)
    scan = scan_checkpoints(S, models, ckpt, quarantine=False)
    parts = [pd.read_parquet(os.path.join(ckpt, f"t7_{m}_{t}.parquet"))
             for (m, t) in sorted(scan["done"])]
    ALL = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    want_per_model = len(S) * N_RULES
    complete = {}
    for m in models:
        got = int((ALL["model"] == m).sum()) if len(ALL) else 0
        complete[m] = {"rows": got, "expected": want_per_model,
                       "complete": got == want_per_model,
                       "missing_tiles": sorted(
                           t for (mm, t) in scan["todo"] if mm == m)}
    ENV["completeness"] = complete
    ENV["export"] = {"rows": int(len(ALL)),
                     "expected": want_per_model * len(models),
                     "models_complete": sum(v["complete"] for v in complete.values()),
                     "models": len(models)}
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "choices_t7.parquet")
    if len(ALL):
        ALL.to_parquet(out, index=False)
    json.dump(ENV, open(os.path.join(outdir, "env_t7.json"), "w"), indent=2,
              default=str)
    print(f"{'model':6s} {'rows':>9s} {'expected':>9s}  status")
    for m, v in complete.items():
        print(f"{m:6s} {v['rows']:9,d} {v['expected']:9,d}  "
              + ("complete" if v["complete"]
                 else f"INCOMPLETE, missing {v['missing_tiles']}"))
    print(f"\ntotal {len(ALL):,} of {want_per_model * len(models):,} expected")
    print(f"written: {out}\n         {os.path.join(outdir, 'env_t7.json')}")
    if ENV.get("failures"):
        print(f"\n{len(ENV['failures'])} failed (model, tile) cell(s):")
        for f in ENV["failures"]:
            print(f"  {f['model']:5s} {f['tile']:8s} {f['error']}")
    return ALL


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
    paths = ([p1_choices_path] if isinstance(p1_choices_path, str)
             else list(p1_choices_path or []))
    paths = [q for q in paths if q and os.path.exists(q)]
    if not paths:
        print("F0 check: P1 choices not mounted here; run it locally instead")
        return None
    P = pd.concat([pd.read_parquet(q) if "prompt_form" in pd.read_parquet(q).columns
                   else pd.read_parquet(q).assign(prompt_form="template")
                   for q in paths], ignore_index=True)
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


def preflight_models(models=None):
    """Can every model actually be loaded here? Fail with a sentence, not a trace.

    Kaggle has no network at run time unless it is enabled, so a missing model
    surfaces deep inside `from_pretrained` as an connection error that reads like
    a bug in this file. Checked up front instead, with the two fixes named.
    """
    from huggingface_hub import try_to_load_from_cache
    models = list(models or MODELS)
    rows, missing = {}, []
    for rung in models:
        repo, rev, _ = MODELS[rung]
        hit = try_to_load_from_cache(repo, "config.json", revision=rev)
        local = isinstance(hit, str) and os.path.exists(hit)
        rows[rung] = {"repo": repo, "revision": rev, "cached": bool(local),
                      "path": hit if local else None}
        if not local:
            missing.append(f"{rung} ({repo} @ {rev[:12]})")
    ENV["preflight_models"] = rows
    for rung, v in rows.items():
        print(f"  {rung:5s} {v['repo']:32s} {'cached' if v['cached'] else 'NOT CACHED'}")
    if missing:
        print(
            "\n" + "=" * 70
            + f"\n{len(missing)} model(s) are not in the local cache:\n  "
            + "\n  ".join(missing)
            + "\n\nTwo ways to fix this, and the notebook will not guess:\n"
              "  1. Turn on 'Internet' in the Kaggle session settings, so\n"
              "     from_pretrained can fetch the pinned revisions from the hub.\n"
              "  2. Attach the models as a Kaggle dataset and set HF_HOME to it,\n"
              "     which is what an offline competition session needs.\n"
              "The revisions are pinned, so either route scores the same weights.\n"
            + "=" * 70)
    return rows, missing


def implied_floor(f0_counts, tile=CONFIRMATORY_TILE):
    """P2-D13's floor from the measured noise, per model and pooled.

    Reported on the whole `size` tile. P2-D13's floor applies to the
    confirmatory subset, the 108 `size` items with finite `beta_c`, and that
    restriction is applied in the analysis session, not here. So this is an upper
    bound on the count and the final floor can only be lower or equal.
    """
    rows, worst = {}, 0
    for m, per_tile in (f0_counts or {}).items():
        d = per_tile.get(tile, {})
        n = int(d.get("disagreeing_items", 0))
        worst = max(worst, n)
        rows[m] = {"disagreeing_items": n, "items": int(d.get("items", 0)),
                   "disagreeing_renderings": int(d.get("disagreeing_renderings", 0)),
                   "renderings": int(d.get("renderings", 0)),
                   "implied_floor": max(PROVISIONAL_FLOOR, n),
                   "p1_batch_flip_rate": P1_FLIP_RATES.get(m)}
    return {"tile": tile, "per_model": rows,
            "pooled_worst_case_floor": max(PROVISIONAL_FLOOR, worst),
            "provisional_floor": PROVISIONAL_FLOOR,
            "rule": "floor = max(7, F0-versus-cond4 disagreement items); "
                    "upward-only (P2-D13)",
            "caveat": "counted on the full size tile; the confirmatory subset is "
                      "the 108 items with finite beta_c, restricted in the "
                      "analysis session, so this is an upper bound"}


def main(models=None, stage=None):
    os.makedirs(CKPT, exist_ok=True)
    capture_env()
    verify_inputs()
    assert_no_sampling()
    S = pd.read_parquet(STIMULI)
    TILES = {t["id"]: t for t in json.load(open(TILES_JSON))["tiles"]}
    ROWS = pd.read_parquet(ITEMS)
    models = list(models or MODELS)
    print(f"{len(S):,} renderings, {S['item_id'].nunique():,} items, "
          f"framings {sorted(S['framing'].unique())}")
    preflight_models(models)
    plan = plan_run(S, models)

    determinism_gate("L1", S, TILES)

    ALL = pd.concat([run_rung(k, S, TILES, ROWS,
                              done_already=set(plan["done"]))
                     for k in models], ignore_index=True)
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
