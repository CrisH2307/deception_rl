"""The returned T7 run record, checked against the artifact rather than trusted.

`env_t7.json` is the run's own account of itself. Every claim in it that can be
checked against `choices_t7.parquet` or against a frozen repository artifact is
checked here, so a run that misreports itself fails rather than being believed.

Two known gaps are asserted as gaps, not silently tolerated: the on-Kaggle pin
cross-check did not run, and `f0_vs_cond4` covers L1 only because cell 4 ran
between the two stages. Both are closed elsewhere, and this file records where.

Run: python3 tests/test_t7_run_record.py
"""
import json
import os
import sys

import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))

import p1  # noqa: E402
import p2_decisions as dec  # noqa: E402

ENV = os.path.join(REPO, "data/raw_t7/env_t7.json")
CHOICES = os.path.join(REPO, "data/raw_t7/choices_t7.parquet")


def _env():
    return json.load(open(ENV))


def _choices():
    return pd.read_parquet(CHOICES)


def test_completeness_claims_match_the_artifact():
    """A run that says it is complete and is not is the failure that matters."""
    E, T = _env(), _choices()
    assert E["export"]["rows"] == len(T) == 126_000, (E["export"]["rows"], len(T))
    assert E["export"]["models_complete"] == 7 == T["model"].nunique()
    for m, v in E["completeness"].items():
        assert v["rows"] == int((T["model"] == m).sum()) == v["expected"], m
        assert v["complete"] and not v["missing_tiles"], (m, v)


def test_grid_is_the_declared_scope():
    """1,000 items x 2 permutations x 3 framings x 4 tiles x 3 rules, Format V."""
    T = _choices()
    assert T["item_id"].nunique() == 1000
    assert sorted(T["framing"].unique()) == ["F0", "F1", "F2"]
    assert sorted(T["rule"].unique()) == ["mean", "pmi", "sum"]
    assert sorted(T["permutation_id"].unique()) == [0, 1]
    assert set(T["format"].unique()) == {"V"}
    assert int((T["unscored_reason"].fillna("") != "").sum()) == 0
    for (m, f), g in T.groupby(["model", "framing"]):
        assert len(g) == 6000, (m, f, len(g))


def test_input_hashes_match_the_frozen_records():
    """The run verified its inputs; check it verified them against ours."""
    E = _env()
    gate = json.load(open(os.path.join(REPO, "results/T6_gate_record.json")))
    man = json.load(open(os.path.join(REPO, "data/processed/t7_stimuli_manifest.json")))
    iv = E["input_verification"]
    assert iv["items_final.parquet"]["sha256"] == \
        gate["artifact_sha256"]["items_final.parquet"]
    assert iv["t7_stimuli.parquet"]["sha256"] == man["stimuli_sha256"]
    assert all(v["matches"] for v in iv.values())


def test_pins_match_paper_1s_record_and_the_scored_rows():
    """P1's D95: never a near-name. The on-Kaggle cross-check did not run, so
    this is where the pins are actually verified against Paper 1's env.json."""
    E, T = _env(), _choices()
    rec = {}
    for rel, key in (("results_2/env.json", "qwen_revisions"),
                     ("results_3/env.json", "models")):
        blob = json.load(open(os.path.join(p1.P1_ROOT, "notebooks", rel)))
        for k, v in blob.get(key, {}).items():
            rec[k] = (v["repo"], v["revision"])
    assert len(rec) == 7, sorted(rec)
    for k, (repo, revision) in rec.items():
        assert E["models"][k]["repo"] == repo, k
        assert E["models"][k]["revision"] == revision, k
        # and the rows actually carry that revision
        assert set(T[T["model"] == k]["revision"].unique()) == {revision}, k


def test_the_invariants_the_decisions_rest_on():
    """P2-D9's determinism, the no-sampling premise, and D111's tokenizer split."""
    E = _env()
    assert E["no_sampling_check"]["banned_tokens_found"] == []
    assert E["no_sampling_check"]["pick_is_argmax"]
    assert E["determinism"]["bit_identical"]
    assert E["determinism"]["max_abs_diff"] == 0.0
    tc = E["tokenizer_class"]
    assert tc["CTRL"] not in {v for k, v in tc.items() if k != "CTRL"}, tc
    assert E["implied_floor"]["pooled_worst_case_floor"] == \
        dec.P2D13_PROVISIONAL_FLOOR


def test_the_two_known_gaps_are_recorded_not_hidden():
    """Both are closed elsewhere. Asserting them keeps the record honest: if a
    later run does cover them, this test says so and can be retired."""
    E = _env()
    assert E["p1_revision_crosscheck"]["p1_env_found"] is False, (
        "the on-Kaggle pin cross-check now runs; update this test and the report")
    assert E["p1_revision_crosscheck"]["n_checked"] == 0
    assert set(E["f0_vs_cond4"]) == {"L1"}, (
        "env_t7.json now covers more models; the recomputation in "
        "results/T7_f0_replication.json may no longer be the only source")
    full = json.load(open(os.path.join(REPO, "results/T7_f0_replication.json")))
    assert set(full["confirmatory_tile_summary"]) == set(E["models"]), \
        "the gap is not actually closed by T7_f0_replication.json"


def test_budget_is_recorded_against_the_estimate():
    E = _env()
    used = sum(E["model_hours"].values())
    est = sum(E["estimate_hours"].values())
    assert 0 < used < est, (used, est)
    assert set(E["model_hours"]) == set(E["estimate_hours"]) == set(E["models"])


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
