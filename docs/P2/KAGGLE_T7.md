# Running T7 on Kaggle

T7 scores three prompt framings on Paper 1's seven-model ladder. Scoring needs
GPUs; everything else happens locally. This document is the whole procedure and
assumes no knowledge of the session that produced it.

**The notebook scores and exports. It computes no Arm B statistic.** Analysis
happens locally afterwards, against the preregistration.

---

## 1. What runs where

| step | where | artifact |
|---|---|---|
| Render the stimuli | local | `data/processed/t7_stimuli.parquet` |
| Score them | Kaggle, 2x T4 | `choices_t7.parquet` |
| Analyse | local | reports, against `PREREGISTRATION_v2.*.md` |

Rendering is deterministic and checkable without a GPU, so it is done and
verified first. A rendering bug found on Kaggle costs a session.

Before uploading, regenerate and check the stimuli:

```bash
python3 src/t7_render.py --demo    # F0 byte-identical to P1, F1/F2 unsplice, menu intact
python3 src/t7_render.py           # writes the parquet and its manifest
```

## 2. Upload two Kaggle datasets

Both are private datasets of plain files. Names matter: the notebook's default
paths are built from them.

| dataset slug | contents | mounts at |
|---|---|---|
| `deception-p2` | this repository | `/kaggle/input/deception-p2` |
| `deception-p1` | Paper 1's repository | `/kaggle/input/deception-p1` |

From `deception-p2` the notebook needs `notebooks/`, `src/`, `results/`, and
`data/processed/t7_stimuli.parquet` with its `_manifest.json`. Uploading the
whole repository is simplest and small.

From `deception-p1` it needs:

```
src/                                        ALL of it. The harness is imported,
                                            not copied, and score_llm pulls in
                                            decisions, fit, score_items and more.
                                            Do not cherry-pick files.
data/reference/tiles.json
data/processed/items_final.parquet
notebooks/results_2/env.json                pinned revisions, cross-checked
notebooks/results_3/env.json
notebooks/results_2/choices_llm.parquet     Paper 1's cond4, for the F0 check
notebooks/results_3/choices_llm_t26.parquet
```

Paper 1 gitignores `data/**` and `notebooks/**` outputs, so these will not be in
a git clone. Copy them from the working tree.

**The folder structure inside either dataset does not matter.** Cell 1 calls
`locate()`, which walks `/kaggle/input` and binds every path to whatever it
finds, so a zip that extracts to `deception-p2/deception_RL/data/...` works
exactly as well as one that extracts to `deception-p2/data/...`. If a file is
absent, `locate()` names it and says which dataset it belongs in, rather than
failing later with a stack trace.

### Sizes, so you know what you are uploading

Nothing here is large. If you hit a 1 MB limit you are using the wrong upload
mechanism, not exceeding a dataset quota: see section 3a.

| | |
|---|---:|
| `deception-p2` total | ~550 KB |
| `deception-p1` total | ~2 MB |

## 3a. The notebook and the dataset are separate uploads

This is the one thing that reliably goes wrong.

| what | how it gets to Kaggle | size |
|---|---|---:|
| `notebooks/kaggle_t7.ipynb` | **Import Notebook**, the `.ipynb` on its own, never zipped | 12 KB |
| `notebooks/kaggle_t7_framings.py` | **inside the `deception-p2` dataset** | 35 KB |

The `.py` is not a notebook and is not imported as one. It is a data file as far
as Kaggle is concerned, and it lives in the dataset with everything else. Kaggle's
notebook import has a size limit that a zip of both files will exceed; the
notebook alone is 12 KB and will not.

## 4. Session settings

- **Accelerator: GPU T4 x2.** Paper 1 ran on 2x T4 and the cost estimate is
  scaled from that run. Cell 1 asserts a GPU is present.
- **Internet: on**, unless you are supplying the models as a dataset. See below.
- Persistence: not required. Checkpoints go to `/kaggle/working`, which survives
  within a session; across sessions you re-upload or re-run, and the resume path
  handles it.

### Where the seven models come from

The notebook does not guess. Either:

1. **From the hub.** Turn Internet on in session settings. `from_pretrained`
   fetches each pinned revision. This is the simple path.
2. **From a Kaggle dataset.** Attach a dataset containing a Hugging Face cache
   and set `HF_HOME` to it in cell 1, before `kaggle_t7_framings` is imported.
   Needed for an offline session.

Every repository is pinned to the commit Paper 1 resolved, so both routes score
the same weights. Cell 2 calls `preflight_models()`, which checks the cache and,
if anything is missing, prints both fixes and stops. It will not fall through to
a download error inside a model load.

The ladder is `Qwen3-0.6B / 1.7B / 4B / 8B`, the two base siblings
`Qwen3-1.7B-Base` and `Qwen3-8B-Base`, and the cross-family control
`allenai/OLMo-2-1124-7B-Instruct`. About 40 GB of weights in total.

## 5. Run order

Open `notebooks/kaggle_t7.ipynb`. Run cells in order. **Do not Run All.**

| cell | does | stops you if |
|---|---|---|
| 1 | environment capture, writes `env_t7.json` before any model loads | a pinned commit disagrees with Paper 1's own record |
| 2 | SHA256 of both inputs, no-sampling assert, model preflight | a dataset is stale or a model is missing |
| 2b | resume drill: writes a broken checkpoint and requires it to be caught | the checkpoint scheme does not actually resume |
| 3 | **stage 1**, the smallest model only | the scorer is not bit-identical on a re-score |
| 4 | **stage 1 verdict**, then halts | nothing; read the number |
| 5 | **stage 2**, the other six, flag defaults off | you have not set `RUN_STAGE2 = True` |
| 6 | export and completeness check | nothing; reports what is missing |

Stage 1 runs and finishes on its own. Cell 5 defaults to `RUN_STAGE2 = False`
specifically so a Run All cannot skip cell 4.

### What cell 4 is telling you

`F0` is Paper 1's condition-4 prompt byte for byte, so a disagreement between
T7's `F0` and Paper 1's frozen `cond4` is pure environment noise: identical
text, different run. The count sets the inertness floor for the whole Arm B
analysis, `floor = max(7, disagreeing items)`, revised upward only.

For context, Paper 1's own batch-composition flip rates were 0.000 to 0.013 per
model on the non-`size` tiles, and the `size` tile is scored at batch 1 by
design in both runs. A count far above that means this environment is noisier
than the one that produced `cond4`, and the floor rises with it. **That is the
measurement working, not a failure.** Record it and continue.

## 6. Interruptions

Kaggle sessions are killed at the time limit. The run is built for it.

- Each `(model, tile)` is written to `/kaggle/working/ckpt` the moment it
  finishes, never accumulated in memory.
- On start, `plan_run` scans the checkpoints, verifies each one's row count
  against what the stimuli imply, and moves any that disagree to `.bad` so they
  are re-run. This catches the parquet a killed session leaves half-written,
  which reads fine and is short.
- Re-running a cell after an interruption reuses what is complete and prints
  what it found and what it will run.

Every completed `(model, tile)` must have **4,500 rows**: 1,500 renderings times
three scoring rules. A model is complete at **18,000 rows**, the full ladder at
**126,000**.

If a model runs out of memory, the failure is recorded, completed tiles stay on
disk, and the run continues to the next model rather than aborting the session.
Cell 6 lists any failed cells.

## 7. Budget

About **17 GPU-hours** for the full ladder, scaled from Paper 1's recorded 2.33
hours for the 8B model, adjusted for 1.5x the renderings and 1.28x the prompt
length. Kaggle's weekly allowance is 30 GPU-hours, so plan for two sessions.

Each model prints its actual against its estimate as it finishes, with a warning
above 1.5x. The point is to see divergence at the 0.6B model, where it costs
twenty minutes, rather than at the allowance limit with the two 8B models
unscored.

Cheapest first if you are splitting sessions: `L1`, `L2`, `B2`, `L3`, `CTRL`,
`L4`, `B4`.

## 8. What to bring back

From `/kaggle/working`:

```
choices_t7.parquet     the scored choices, 126,000 rows when complete
env_t7.json            environment, pins, F0 counts, budget, any failures
```

Put them where the analysis session can read them and say so. Nothing else is
needed; the checkpoints under `ckpt/` are redundant once the export is complete.

## 9. If something is wrong

| symptom | cause | fix |
|---|---|---|
| cell 1 raises on revisions | a pin drifted from Paper 1's record | Paper 1's `env.json` is the record. Do not edit `MODELS` to pass. |
| cell 2 raises on SHA256 | a stale dataset upload | re-upload, and re-run `src/t7_render.py` first |
| cell 2 says models not cached | no internet and no model dataset | see section 4 |
| cell 3 determinism assert fails | the scorer is not bit-identical within the session | stop and report. P2-D13's floor assumes it is. |
| a tile is quarantined on resume | a session died mid-write | expected, it re-runs automatically |
| export says INCOMPLETE | a model or tile did not finish | re-run cell 5, it resumes |
