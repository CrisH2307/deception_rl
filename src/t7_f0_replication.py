"""T7 step 2: does `F0` reproduce Paper 1's frozen `cond4`, and what floor does it set?

Two separable purposes, per `T7.md` step 2 as corrected on 2026-09-10, and they
fail separately:

  ENVIRONMENT EQUIVALENCE against Paper 1's frozen `cond4`. `F0` is Paper 1's
  Format V `base` rendering byte for byte (P2-D1), so a disagreement is not a
  framing effect. If this fails, the link to Paper 1 weakens and the comparison
  to Paper 1's published reference set is approximate, and must be reported so.

  A WITHIN-ENVIRONMENT BASELINE for the F1 and F2 contrasts. This does not depend
  on the first. If equivalence fails, `F0` is still the baseline the contrasts are
  taken against and Arm B's result stands on its own environment.

The same count is also P2-D13's measured noise floor. `F0` and `cond4` are
identical text, so a disagreement is floating-point nondeterminism flipping a
near-tie argmax, and

    floor = max(7, F0-versus-cond4 disagreement items)     upward-only

This closes `PREREGISTRATION_v2.6.md` section 1.1, which argued the no-effect
same-option rate of 1.0 from Paper 1's code path and recorded that the frozen
artifacts held no repeated rendering to corroborate it. T7's `F0` run is that
repeated rendering.

NO ARM B STATISTIC IS COMPUTED HERE. This is the replication check and the floor,
nothing else. F1 and F2 are untouched.

Run: python3 src/t7_f0_replication.py          (writes results + report)
     python3 src/t7_f0_replication.py --demo   (self-check on the floor rule)
"""
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1  # noqa: E402
import p2_decisions as P2D  # noqa: E402
import tie_reference as TR  # noqa: E402

CHOICES = "data/raw_t7/choices_t7.parquet"
OUT = "results/T7_f0_replication.json"
REPORT = "reports/T7_f0_replication.md"
RULE, FORM = TR.RULE, TR.FORM
CONFIRMATORY_TILE = P2D.P2D3_TILE
PROVISIONAL_FLOOR = P2D.P2D13_PROVISIONAL_FLOOR
# Whether the on-Kaggle pin cross-check against Paper 1's env.json ran. It did
# not, so choice identity must not be reported as environment identity.
P1_ENV_FOUND = json.load(open("data/raw_t7/env_t7.json"))[
    "p1_revision_crosscheck"]["p1_env_found"]


def p1_cond4():
    """Paper 1's frozen `cond4` choices, its own filters applied."""
    P = TR.load_choices()
    return P[(P["condition"] == "cond4") & (P["rule"] == RULE)
             & (P["prompt_form"] == FORM)]


def compare(T=None):
    """Per (model, tile): renderings compared, and how many disagree.

    Restricted to `n_tied == 1` on both sides, which is Paper 1's own filter. A
    tie carries no chosen option, so it cannot agree or disagree.
    """
    T = pd.read_parquet(CHOICES) if T is None else T
    t = T[(T["framing"] == "F0") & (T["rule"] == RULE) & (T["n_tied"] == 1)]
    P = p1_cond4()
    P = P[P["n_tied"] == 1]
    key = ["model", "item_id", "permutation_id"]
    j = t.merge(P[key + ["chosen_option"]], on=key, suffixes=("_t7", "_p1"))
    j["disagree"] = j["chosen_option_t7"] != j["chosen_option_p1"]
    out = {}
    for (m, tile), g in j.groupby(["model", "tile"]):
        out.setdefault(m, {})[tile] = {
            "renderings": int(len(g)),
            "disagreeing_renderings": int(g["disagree"].sum()),
            "disagreement_rate": float(g["disagree"].mean()),
            "items": int(g["item_id"].nunique()),
            "disagreeing_items": int(g[g["disagree"]]["item_id"].nunique()),
        }
    return out, int(len(j))


def main():
    T = pd.read_parquet(CHOICES)
    per, n_matched = compare(T)
    models = sorted(per)
    conf = {m: per[m][CONFIRMATORY_TILE] for m in models}
    worst = max(v["disagreeing_items"] for v in conf.values())
    floor = max(PROVISIONAL_FLOOR, worst)
    P2D.bind_armb_floor(floor, worst, floor_is_statistical=False)

    off = {m: {"renderings": sum(v["renderings"] for t, v in per[m].items()
                                 if t != CONFIRMATORY_TILE),
               "disagreeing_renderings": sum(
                   v["disagreeing_renderings"] for t, v in per[m].items()
                   if t != CONFIRMATORY_TILE)} for m in models}
    for m in models:
        o = off[m]
        o["rate"] = o["disagreeing_renderings"] / max(1, o["renderings"])
        o["p1_batch_flip_rate"] = P2D_FLIP.get(m)

    out = {
        "purpose": "T7 step 2. F0 against Paper 1's frozen cond4: environment "
                   "equivalence, the within-environment baseline, and P2-D13's "
                   "measured noise floor. No Arm B statistic is computed here.",
        "rule": RULE, "prompt_form": FORM,
        "choices_sha256": p1.artifact_hash(CHOICES),
        "renderings_compared": n_matched,
        "confirmatory_tile": CONFIRMATORY_TILE,
        "per_model_per_tile": per,
        "confirmatory_tile_summary": conf,
        "off_confirmatory_summary": off,
        "environment_equivalence": {
            "verdict": "CHOICE-LEVEL OUTPUT IDENTITY on the confirmatory tile; "
                       "environment identity NOT established"
                       if worst == 0 else "PARTIAL",
            "confirmatory_disagreeing_items": worst,
            "confirmatory_renderings": sum(v["renderings"] for v in conf.values()),
            "p1_env_found": P1_ENV_FOUND,
            "what_it_licenses":
                "F0 reproduces Paper 1's cond4 chosen option on every one of the "
                f"{sum(v['renderings'] for v in conf.values()):,} confirmatory-tile "
                "renderings, zero disagreements. That is choice-level output "
                "identity on the confirmatory tile, so reference-set comparisons "
                "that read only chosen options on that tile are unaffected by the "
                "re-run. It is NOT environment identity: env_t7.json records "
                "p1_env_found false, so the on-Kaggle pin cross-check against "
                "Paper 1's env.json never ran, and transformers 5.0.0 / torch "
                "2.10.0 is very unlikely to match Paper 1's stack. Off the "
                "confirmatory tile the outputs are not identical (see "
                "off_confirmatory_summary)."
                if worst == 0 else
                "Equivalence is partial; the link to Paper 1 weakens and the "
                "reference-set comparison must be reported as approximate. The "
                "within-environment baseline is unaffected.",
        },
        "floor": {
            "provisional": PROVISIONAL_FLOOR,
            "measured_worst_case_items": worst,
            "adopted": floor,
            "rule": "floor = max(7, F0-versus-cond4 disagreement items), "
                    "upward-only (P2-D13)",
            "revised": floor != PROVISIONAL_FLOOR,
            "caveat": "counted on the full size tile (250 items); the "
                      "confirmatory subset is the 108 with finite beta_c, so a "
                      "count of 0 here is 0 there",
        },
        "closes_v26_section_1_1":
            "PREREGISTRATION_v2.6.md section 1.1 argued the no-effect "
            "same-option rate of 1.0 from Paper 1's code path and recorded that "
            "no repeated rendering existed to corroborate it. This is that "
            "repeated rendering. On the confirmatory tile the measured rate is "
            f"{1.0 if worst == 0 else 'below 1.0'}.",
    }
    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    _write_report(out)
    print(f"{n_matched:,} renderings compared, {len(models)} models\n")
    print(f"  {'model':6s} {'size dis/rend':>15s} {'size items':>11s} "
          f"{'other dis/rend':>16s} {'other rate':>11s} {'P1 flip':>8s}")
    for m in models:
        c, o = conf[m], off[m]
        print(f"  {m:6s} {c['disagreeing_renderings']:7d}/{c['renderings']:<7d} "
              f"{c['disagreeing_items']:11d} "
              f"{o['disagreeing_renderings']:8d}/{o['renderings']:<7d} "
              f"{o['rate']:11.5f} {o['p1_batch_flip_rate']:8.3f}")
    print(f"\n  environment equivalence: "
          f"{out['environment_equivalence']['verdict']}")
    print(f"  floor = max({PROVISIONAL_FLOOR}, {worst}) = {floor}"
          + ("  (unrevised)" if floor == PROVISIONAL_FLOOR else "  (REVISED UP)"))
    print(f"\n  written: {OUT}\n           {REPORT}")
    return 0


# P1's measured batch-composition flip rates, for context beside T7's own count.
P2D_FLIP = {"L1": 0.010, "L2": 0.000, "L3": 0.003, "L4": 0.013,
            "B2": 0.007, "B4": 0.003, "CTRL": 0.000}


def _write_report(out):
    w = [].append
    b = []
    def W(x):
        b.append(x)
    W("# T7 step 2: `F0` against Paper 1's frozen `cond4`\n")
    W("Generated by `python3 src/t7_f0_replication.py`. No Arm B statistic is "
      "computed here.\n")
    e = out["environment_equivalence"]
    W(f"\n## Headline\n\n```\nenvironment equivalence   {e['verdict']}\n"
      f"confirmatory renderings   {e['confirmatory_renderings']:,}\n"
      f"disagreeing items         {e['confirmatory_disagreeing_items']}\n"
      f"floor                     max({out['floor']['provisional']}, "
      f"{out['floor']['measured_worst_case_items']}) = {out['floor']['adopted']}"
      f"\n```\n")
    W("\n## Per model\n")
    W("| model | `size` disagree / renderings | `size` items | other disagree / "
      "renderings | other rate | P1 batch-flip |")
    W("|---|---:|---:|---:|---:|---:|")
    for m in sorted(out["confirmatory_tile_summary"]):
        c, o = out["confirmatory_tile_summary"][m], out["off_confirmatory_summary"][m]
        W(f"| `{m}` | {c['disagreeing_renderings']} / {c['renderings']:,} | "
          f"{c['disagreeing_items']} | {o['disagreeing_renderings']} / "
          f"{o['renderings']:,} | {o['rate']:.5f} | {o['p1_batch_flip_rate']:.3f} |")
    W("\nThe `size` tile is Paper 2's confirmatory tile (P2-D3) and is scored at "
      "`max_batch = 1` in both runs per Paper 1's D102 part 3, so it carries no "
      "batch-composition noise by construction. The other three tiles are "
      "batched, and their disagreement rates sit at the same order as Paper 1's "
      "own batch-8-against-batch-1 flip rates.\n")
    W("\n## What this licenses\n")
    W(f"{e['what_it_licenses']}\n")
    W("\nThe two purposes of the `F0` re-run are separable. The within-environment "
      "baseline for the F1 and F2 contrasts holds. Environment equivalence is "
      "established only as choice-level output identity on the confirmatory "
      "tile: the pin cross-check against Paper 1's `env.json` did not run "
      f"(`p1_env_found: {str(out['environment_equivalence']['p1_env_found']).lower()}`), "
      "and the library stack is very unlikely to match Paper 1's.\n")
    W("\n**Correction.** Commit `4db6f0c`'s message and this report's earlier "
      "version said environment equivalence was exact and the comparison to "
      "Paper 1's reference set exact rather than approximate. That overstated "
      "the result; the wording above replaces it.\n")
    W("\n## The floor\n")
    W(f"```\n{out['floor']['rule']}\nmeasured   {out['floor']['measured_worst_case_items']}"
      f"\nadopted    {out['floor']['adopted']}\n```\n")
    W(f"\n{out['floor']['caveat']}.\n")
    W(f"\n{out['closes_v26_section_1_1']}\n")
    W(f"\n## Chain of custody\n\n```\nsha256  {CHOICES}\n        "
      f"{out['choices_sha256']}\nrenderings compared  {out['renderings_compared']:,}\n```\n")
    os.makedirs("reports", exist_ok=True)
    open(REPORT, "w").write("\n".join(b))


def demo():
    """The floor rule is a maximum, and the confirmatory count is what feeds it."""
    per, n = compare()
    conf = {m: per[m][CONFIRMATORY_TILE] for m in per}
    worst = max(v["disagreeing_items"] for v in conf.values())
    assert all(v["renderings"] == 500 for v in conf.values()), \
        {m: v["renderings"] for m, v in conf.items()}
    floor = max(PROVISIONAL_FLOOR, worst)
    assert floor >= PROVISIONAL_FLOOR and floor >= worst
    P2D.bind_armb_floor(floor, worst, floor_is_statistical=False)
    print(f"ok: {n:,} renderings compared, {len(conf)} models, "
          f"{worst} worst-case confirmatory disagreeing items, floor {floor}")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
