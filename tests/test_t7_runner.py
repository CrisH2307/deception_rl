"""The T7 Kaggle runner's non-GPU paths, exercised rather than assumed.

Everything here runs without a GPU and without loading a model, which is the
point: the checkpoint scheme, the input hashes and the pin cross-check are what
decide whether a T4 session is worth starting, and all three are checkable here.

`notebooks/kaggle_t7_framings.simulate_kill_and_resume` is the in-module drill
the notebook runs before the real job. This file adds the cases that drill does
not cover: a realistic partial kill across tiles, the stale-upload negative
control, and the floor arithmetic.

Run: python3 tests/test_t7_runner.py
"""
import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P1 = os.environ.get("P1_ROOT", "/Users/crishuynh/Documents/SoftwareProject/deception")
os.environ.update(
    P2_ROOT=REPO, P1_ROOT_K=P1, P1_SRC=f"{P1}/src", P2_SRC=f"{REPO}/src",
    P1_NOTEBOOKS=f"{P1}/notebooks",
    T7_STIMULI=os.path.join(REPO, "data/processed/t7_stimuli.parquet"),
    T7_TILES=f"{P1}/data/reference/tiles.json",
    T7_ITEMS=f"{P1}/data/processed/items_final.parquet")
sys.path.insert(0, os.path.join(REPO, "notebooks"))
sys.path.insert(0, os.path.join(REPO, "src"))

import kaggle_t7_framings as K  # noqa: E402

MANIFEST = os.path.join(REPO, "data/processed/t7_stimuli_manifest.json")


def _stimuli():
    return pd.read_parquet(K.STIMULI)


def test_pins_agree_with_paper_1s_own_record():
    """The revisions are Paper 1's. Cross-check them against P1's env.json.

    A near-name or a drifted revision means a run that silently scored different
    weights, which no downstream check would catch (P1's D95).
    """
    tmp = tempfile.mkdtemp()
    env = K.capture_env(os.path.join(tmp, "env_t7.json"))
    x = env["p1_revision_crosscheck"]
    assert x["p1_env_found"], "P1's env.json not readable; the pins are unchecked"
    assert x["n_checked"] == len(K.MODELS), (x["n_checked"], len(K.MODELS))
    assert not x["problems"], x["problems"]
    assert os.path.exists(os.path.join(tmp, "env_t7.json")), \
        "env must be written before any model loads, so a dead session leaves it"


def test_input_hashes_and_the_stale_upload_they_catch():
    """A stale dataset upload is silent: the run completes and is wrong."""
    ver = K.verify_inputs()
    assert all(v["matches"] for v in ver.values()), ver
    tmp = tempfile.mkdtemp()
    stale = os.path.join(tmp, "stale.parquet")
    _stimuli().head(10).to_parquet(stale, index=False)
    try:
        K.verify_inputs(stimuli=stale, manifest=MANIFEST)
    except AssertionError as e:
        assert "sha256" in str(e)
    else:
        raise AssertionError("a stale stimuli file passed verification")


def test_no_sampling_in_the_harness():
    """P2-D9, and every decision after it, assume a deterministic argmax."""
    ok = K.assert_no_sampling()
    assert ok["banned_tokens_found"] == [], ok
    assert ok["pick_is_argmax"]


def test_resume_drill_the_notebook_runs():
    K.CKPT = tempfile.mkdtemp()
    assert K.simulate_kill_and_resume(_stimuli(), ckpt=K.CKPT)


def test_a_realistic_partial_kill_resumes_correctly():
    """Two tiles complete, one killed mid-write, one never started."""
    S = _stimuli()
    tmp = tempfile.mkdtemp()
    tiles = sorted(S["tile"].unique())
    for t in tiles[:2]:
        n = K.expected_rows(S, t)
        pd.DataFrame({"item_id": np.arange(n)}).to_parquet(
            os.path.join(tmp, f"t7_L1_{t}.parquet"), index=False)
    pd.DataFrame({"item_id": np.arange(K.expected_rows(S, tiles[2]) // 3)}
                 ).to_parquet(os.path.join(tmp, f"t7_L1_{tiles[2]}.parquet"),
                              index=False)
    p = K.scan_checkpoints(S, models=["L1"], ckpt=tmp)
    assert len(p["done"]) == 2, p["done"]
    assert ("L1", tiles[2]) in p["bad"], p["bad"]
    assert sorted(t for _, t in p["todo"]) == sorted(tiles[2:]), p["todo"]
    # rescanning must not re-quarantine what it already cleared
    p2 = K.scan_checkpoints(S, models=["L1"], ckpt=tmp)
    assert len(p2["done"]) == 2 and p2["bad"] == {}, (p2["done"], p2["bad"])


def test_export_reports_incompleteness_instead_of_truncating():
    """The failure mode is a short export that looks finished."""
    S = _stimuli()
    ckpt, out = tempfile.mkdtemp(), tempfile.mkdtemp()
    tiles = sorted(S["tile"].unique())
    for t in tiles[:2]:
        n = K.expected_rows(S, t)
        pd.DataFrame({"item_id": np.arange(n), "model": "L1", "tile": t}
                     ).to_parquet(os.path.join(ckpt, f"t7_L1_{t}.parquet"),
                                  index=False)
    K.ENV.clear()
    K.export(S, outdir=out, ckpt=ckpt, models=["L1"])
    c = K.ENV["completeness"]["L1"]
    assert not c["complete"]
    assert sorted(c["missing_tiles"]) == sorted(tiles[2:]), c
    assert c["rows"] == 2 * K.expected_rows(S, tiles[0])
    assert c["expected"] == len(S) * K.N_RULES


def test_expected_rows_track_the_stimuli_not_a_constant():
    """A scope change must move the resume check with it."""
    S = _stimuli()
    for t in S["tile"].unique():
        assert K.expected_rows(S, t) == int((S["tile"] == t).sum()) * K.N_RULES
    assert sum(K.expected_rows(S, t) for t in S["tile"].unique()) == len(S) * 3


def test_implied_floor_is_upward_only():
    """P2-D13's rule, on the numbers the notebook will actually hand it."""
    import p2_decisions as dec
    for n, want in ((0, 7), (3, 7), (7, 7), (8, 8), (19, 19)):
        f = K.implied_floor({"L1": {"size": {"disagreeing_items": n, "items": 250,
                                             "renderings": 1500,
                                             "disagreeing_renderings": n}}})
        assert f["per_model"]["L1"]["implied_floor"] == want, (n, f)
    assert K.PROVISIONAL_FLOOR == dec.P2D13_PROVISIONAL_FLOOR


def test_notebook_stage_2_defaults_off():
    """A Run All must stop at the stage 1 verdict."""
    import re
    nb = json.load(open(os.path.join(REPO, "notebooks/kaggle_t7.ipynb")))
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    src = "\n".join("\n".join(c["source"]) for c in code)
    assert re.search(r"^RUN_STAGE2 = False\b", src, re.M), \
        "stage 2 does not default to off; a Run All would skip the verdict"
    assert "HALT" in src, "the stage 1 verdict does not halt"
    for fn in ("capture_env", "verify_inputs", "assert_no_sampling",
               "simulate_kill_and_resume", "plan_run", "run_rung", "export"):
        assert f"K.{fn}" in src, f"the notebook never calls {fn}"
    # the notebook must not re-implement the harness rules it inherits
    for banned in ("score_rows(", "max_batch=1", "def records", "AutoModelForCausalLM"):
        assert banned not in src, (
            f"the notebook contains {banned!r}; it must drive "
            "kaggle_t7_framings.py, not re-implement it")


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"ok  {name}")
            except AssertionError as e:
                fails += 1
                print(f"FAIL {name}\n     {e}")
    sys.exit(1 if fails else 0)
