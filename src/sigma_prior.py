"""Per-item SD of a one-sentence-insertion effect in Paper 1, as an ANALOGUE for
`sigma` of Paper 2's `Delta-A`. Measurement only: this script selects nothing,
sizes nothing, and adopts nothing.

**It is an analogue, not a measurement of `sigma`.** Paper 1 scored two
conditions differing by a single inserted sentence in the same `{extra}` prompt
slot that Paper 2's framing block occupies (P2-D2): condition 4 is the `base`
rendering, condition 5 is D64's `c5` insert. Paper 2's `Delta-A` is the F0-to-F1
/F2 difference on the `A` coordinate. Same structural slot, different content
(D64's `c5` tells the chooser to consider every pairing; Paper 2's block
describes an adversary) and a different coordinate (`post_norm`, not `A`). What
this emits is therefore a prior over the magnitude of a one-sentence-insertion
effect's item-level variability.

Nothing here may be used to size or reselect an item set. Realized power and
required `n` are both reported and neither is adopted.

Data: Paper 1's two language-model choice tables, by the paths the T5 brief
names. `prompt_form == "template"` is primary because that is the filter P1's
own analysis code applies (`src/divergence_curve.py:139`,
`src/frontier_position.py:129`); `raw` is reported beside it, not merged in.

Deterministic, no seed.

Run: python3 src/sigma_prior.py     (writes reports/T5_sigma_prior.md)
"""
import os
import statistics
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1  # noqa: E402

LADDER = os.path.join(p1.P1_ROOT, "notebooks/results_2/choices_llm.parquet")
T26 = os.path.join(p1.P1_ROOT, "notebooks/results_3/choices_llm_t26.parquet")
REPORT = "reports/T5_sigma_prior.md"

TILE = "size"              # P2-D3, Arm B's confirmatory tile
FORMAT = "V"               # D103 retires format L
RULES = ("pmi", "sum", "mean")   # pmi primary, D98 / D109
COND_BASE, COND_INSERT = "cond4", "cond5"

# Preregistration v2.0 section 8.2. alpha over the 21-test confirmatory family.
ALPHA = 0.05 / 21
DELTA = 0.05               # SESOI, Paper 1's D74
POWER = 0.80
N_ADOPTED = 108            # PREREGISTRATION_v2.3 section 3 / reports/T2_frozen_set_counts.md
SIGMA_COVERED = 0.134      # the sigma n = 108 covers at 80% power

_N = statistics.NormalDist()
Z_HALF_ALPHA = _N.inv_cdf(1 - ALPHA / 2)
Z_BETA = _N.inv_cdf(POWER)
N_CONST = (Z_HALF_ALPHA + Z_BETA) ** 2 / DELTA ** 2   # section 8.2's 6020


def required_n(sigma):
    """Items needed at 80% power for this sigma. Section 8.2's formula."""
    return N_CONST * sigma ** 2


def realized_power(sigma, n=N_ADOPTED):
    """Normal approximation, the same one section 8.2 inverts. A noncentral-t
    calculation would differ slightly; this one is used so the two numbers in
    the report are comparable to the preregistered curve."""
    return _N.cdf(DELTA * np.sqrt(n) / sigma - Z_HALF_ALPHA)


def load():
    """Both choice tables, with a `prompt_form` column on every row.

    The ladder file has no `prompt_form`; its prompts are the templated Format V
    rendering, so it is labelled `template` to sit in one frame with the Task-26
    file rather than being special-cased downstream.
    """
    frames = []
    for path, src in ((LADDER, "ladder"), (T26, "t26")):
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} missing. Precondition failed; stop.")
        d = pd.read_parquet(path)
        for col in ("item_id", "tile", "model", "format", "permutation_id", "rule",
                    "condition", "post_norm", "n_tied", "unscored_reason"):
            if col not in d.columns:
                raise KeyError(f"{path}: no column {col!r}. Malformed; stop.")
        if "prompt_form" not in d.columns:
            d = d.assign(prompt_form="template")
        frames.append(d.assign(source=src))
    return pd.concat(frames, ignore_index=True)


def attrition(df):
    """Rows removed by each filter, per (model, prompt_form). No silent drops."""
    rows = []
    for key, g in df.groupby(["model", "prompt_form"], sort=True):
        n0 = len(g)
        a = g[g["format"] == FORMAT]
        b = a[a["tile"] == TILE]
        c = b[b["n_tied"] == 1]
        d = c[c["unscored_reason"].fillna("").astype(str) == ""]
        rows.append(dict(model=key[0], prompt_form=key[1], rows=n0,
                         drop_format=n0 - len(a), drop_tile=len(a) - len(b),
                         drop_tied=len(b) - len(c), drop_unscored=len(c) - len(d),
                         kept=len(d)))
    return pd.DataFrame(rows)


def filtered(df):
    m = ((df["format"] == FORMAT) & (df["tile"] == TILE) & (df["n_tied"] == 1)
         & (df["unscored_reason"].fillna("").astype(str) == ""))
    return df[m]


def per_cell(g):
    """One (model, prompt_form, rule) cell: sigma of d_i and its bookkeeping.

    Step 3, per-item mean of `post_norm` within condition across the surviving
    option-order permutations (PREREGISTRATION_v2 section 3.2's aggregation).
    Step 4, `d_i = post_norm(cond5) - post_norm(cond4)` on items present in both
    conditions.
    """
    cell = (g.groupby(["item_id", "condition"])["post_norm"]
             .agg(["mean", "size"]).reset_index())
    single_perm = int((cell["size"] == 1).sum())
    w = cell.pivot(index="item_id", columns="condition", values="mean")
    n_base = int(w[COND_BASE].notna().sum()) if COND_BASE in w else 0
    n_ins = int(w[COND_INSERT].notna().sum()) if COND_INSERT in w else 0
    both = w.dropna(subset=[COND_BASE, COND_INSERT])
    d = (both[COND_INSERT] - both[COND_BASE]).values
    sigma = float(np.std(d, ddof=1))
    return dict(n_items=len(d), n_base=n_base, n_insert=n_ins,
                lost_unpaired=max(n_base, n_ins) - len(d),
                cells_one_perm=single_perm,
                mean_d=float(d.mean()), sd_d=sigma,
                power_108=realized_power(sigma), n_required=required_n(sigma),
                exceeds=sigma > SIGMA_COVERED)


def table(df):
    rows = []
    for (model, pf, rule), g in filtered(df).groupby(
            ["model", "prompt_form", "rule"], sort=True):
        if rule not in RULES:
            continue
        rows.append(dict(model=model, prompt_form=pf, rule=rule, **per_cell(g)))
    return pd.DataFrame(rows)


def md_table(d, cols, fmt):
    head = "| " + " | ".join(c[0] for c in cols) + " |\n"
    head += "|" + "|".join(c[1] for c in cols) + "|\n"
    body = ""
    for r in d.itertuples():
        body += "| " + " | ".join(fmt(c[0], getattr(r, c[2])) for c in cols) + " |\n"
    return head + body


def main():
    df = load()
    att = attrition(df)
    T = table(df)
    tmpl = T[T["prompt_form"] == "template"].sort_values(["rule", "model"])
    raw = T[T["prompt_form"] == "raw"].sort_values(["rule", "model"])
    pmi = tmpl[tmpl["rule"] == "pmi"].sort_values("model")

    def f(col, v):
        if col in ("model", "prompt_form", "rule"):
            return f"`{v}`"
        if col == "exceeds":
            return "**yes**" if v else "no"
        if isinstance(v, (int, np.integer)):
            return f"{v:,}"
        if col == "n required":
            return f"{v:,.0f}"
        return f"{v:.4f}"

    MAIN = [("model", "---", "model"), ("rule", "---", "rule"),
            ("items", "---:", "n_items"), ("mean `d_i`", "---:", "mean_d"),
            ("`sigma_analogue`", "---:", "sd_d"),
            ("power at n = 108", "---:", "power_108"),
            ("n required", "---:", "n_required"),
            ("`sigma` > 0.134", "---:", "exceeds")]
    ATT = [("model", "---", "model"), ("prompt_form", "---", "prompt_form"),
           ("rows", "---:", "rows"), ("format != V", "---:", "drop_format"),
           ("tile != size", "---:", "drop_tile"),
           ("`n_tied` > 1", "---:", "drop_tied"),
           ("`unscored_reason`", "---:", "drop_unscored"),
           ("kept", "---:", "kept")]
    BOOK = [("model", "---", "model"), ("rule", "---", "rule"),
            ("items with `cond4`", "---:", "n_base"),
            ("items with `cond5`", "---:", "n_insert"),
            ("paired", "---:", "n_items"),
            ("lost unpaired", "---:", "lost_unpaired"),
            ("item-condition cells with one permutation", "---:", "cells_one_perm")]

    lo, hi = pmi["sd_d"].min(), pmi["sd_d"].max()
    n_exceed = int(pmi["exceeds"].sum())
    txt = f"""# T5: per-item SD of a one-sentence-insertion effect in Paper 1, as an analogue for `sigma` of `Delta-A`

Generated by `python3 src/sigma_prior.py`. Deterministic, no seed. Measurement
only: this script selects nothing, sizes no item draw, and adopts nothing.

## 0. This is an analogue, and the distinction is not cosmetic

Read this before the number. Paper 1 ran two conditions that differ by a single
sentence inserted into the same `{{extra}}` prompt slot that Paper 2's framing
block occupies (`docs/P2/DECISIONS.md`, P2-D2): condition 4 is the `base`
rendering, condition 5 is the D64 `c5` insert. The measured quantity below is
the per-item difference between those two conditions on `post_norm`, and its
standard deviation across items.

Paper 2's `Delta-A` is the difference between framing `F0` and `F1` / `F2` on the
normalized displacement coordinate `A`. It shares the structural place of the
manipulation with Paper 1's `c5` insert, and nothing else. Two differences:

- **Content.** D64's `c5` insert tells the chooser to consider every
  Means-by-Clue pairing. Paper 2's block describes an adversary who shares the
  audience. These are different interventions that happen to occupy the same
  slot.
- **Coordinate.** Paper 1's outcome is `post_norm`. Paper 2's is `A`, which
  rescales the normalized margin by the item's adversary extent
  (`PREREGISTRATION_v2.md` section 3.2). Section 8.2 already carries the SESOI
  across those two coordinates by arguing they are on the same scale; that
  argument does not extend to their per-item dispersion, which is exactly what
  is measured here.

So what follows is a **prior over the magnitude of a one-sentence-insertion
effect's item-level variability** in this signal space, on this tile, with this
scoring. It is not a measurement of `sigma` for `Delta-A`, and a report that used
it as one would be overstating it.

## 1. Headline

Under `pmi` (primary, per D98 and D109), across the seven models of the
confirmatory family:

```
sigma_analogue   {lo:.4f}  to  {hi:.4f}
```

Against the adopted confirmatory set of n = {N_ADOPTED} `size`-tile items with
finite `beta_c`, which covers `sigma <= {SIGMA_COVERED}`:

```
models whose analogue sigma exceeds {SIGMA_COVERED}   {n_exceed} of {len(pmi)}    (pmi)
```

{md_table(pmi, MAIN, f)}
Realized power is the normal approximation
`power = Phi(delta * sqrt(n) / sigma - z_(alpha/2))`, the same approximation
`PREREGISTRATION_v2.md` section 8.2 inverts, used here so the two numbers sit on
the same footing as the preregistered curve. A noncentral-t calculation would
differ slightly and would give slightly lower power. `n required` is
`{N_CONST:,.0f} * sigma^2`, section 8.2's constant at `delta = 0.05`.

**Neither number is adopted here.** Both are reported. Whether n = {N_ADOPTED}
is accepted with its stated power, or a larger draw is made, is the author's
decision and is not taken in this session.

## 2. Constants, from the preregistration rather than retyped

```
alpha              = 0.05 / 21 = {ALPHA:.6f}   two-sided, 21-test confirmatory family (section 8.1)
z_(alpha/2)        = {Z_HALF_ALPHA:.4f}                    section 8.2 quotes 3.038
z_(0.20)           = {Z_BETA:.4f}                    section 8.2 quotes 0.842
(z + z)^2          = {(Z_HALF_ALPHA + Z_BETA) ** 2:.4f}                    section 8.2 quotes 15.05
delta              = {DELTA}                       SESOI, Paper 1's D74
n = C * sigma^2,  C = {N_CONST:,.2f}         section 8.2 quotes 6020
n adopted          = {N_ADOPTED}                        PREREGISTRATION_v2.3 section 3
sigma covered      = {SIGMA_COVERED}                     by n = {N_ADOPTED} at 80% power
```

The z values are recomputed from the normal quantile rather than read off
section 8.2's rounded figures, and they agree with them to the digits section
8.2 prints.

## 3. What was filtered, and how much each filter removed

Format V only (`format == "V"`; D103 retires format L), `size` tile only (P2-D3),
Paper 1's scoring-tie filter `n_tied == 1`, and rows with a non-empty
`unscored_reason` dropped. Nothing else is dropped.

{md_table(att.sort_values(["model", "prompt_form"]), ATT, f)}
Two things to note in that table rather than leave implicit:

- **The format filter removes nothing.** Both files carry Format V rows only.
  Paper 1's format-L runs are not in these two artifacts, so D103's retirement
  costs no rows here. The filter is applied anyway, because a report that
  claimed Format V without filtering on it would be claiming something it had
  not checked.
- **The `unscored_reason` filter removes nothing, and the column is not null.**
  `unscored_reason` is the empty string on all {len(df):,} rows of both files,
  never null. The brief's "non-null" was read as "non-empty", because a null
  test would have dropped every row.

## 4. Pairing bookkeeping, `pmi`, template

Per item, `post_norm` is averaged within condition across the two option-order
permutations, then differenced. Items must survive filtering in both conditions.

{md_table(pmi.assign(rule="pmi"), BOOK, f)}
## 5. All three scoring rules

D109 requires every finding recomputed under all three rules with
rule-dependence stated in the sentence that makes the claim. Here it is.

{md_table(tmpl, MAIN, f)}
## 6. The `prompt_form` split, disclosed rather than collapsed

`notebooks/results_3/choices_llm_t26.parquet` carries a `prompt_form` column the
brief did not name: `B2` and `B4` were each run under `raw` and `template`, and
`CTRL` under `template` only. That is 60,000 rows rather than the 36,000 the
model-by-rule-by-condition-by-item-by-permutation grid implies, and it was the
one thing in the data that did not match the brief's description.

It was not resolved by choosing. `template` is primary because that is the
filter Paper 1's own analysis code applies to this same file
(`src/divergence_curve.py:139` and `src/frontier_position.py:129` both do
`d = d[d["prompt_form"] == "template"]`), which is the code path that produced
Paper 1's reported frontier and divergence numbers. The ladder file has no such
column and its prompts are the templated rendering, so `template` is also the
form that puts all seven models in one frame. The `raw` rows are reported below
rather than dropped silently or averaged in.

{md_table(raw, MAIN, f)}
## 7. Does the analogue exceed 0.134

Stated plainly, per model, `pmi`:

```
"""
    for r in pmi.itertuples():
        txt += (f"{r.model:6s} sigma = {r.sd_d:.4f}   "
                f"{'EXCEEDS' if r.exceeds else 'within'} 0.134   "
                f"power at n = 108: {r.power_108:.4f}   "
                f"n required: {r.n_required:,.0f}\n")
    ex_all = T[T["prompt_form"] == "template"]
    txt += f"""```

{"Every model's analogue sigma exceeds 0.134 under pmi." if n_exceed == len(pmi) else f"{n_exceed} of {len(pmi)} models exceed 0.134 under pmi."} Across all three rules, {int(ex_all["exceeds"].sum())} of {len(ex_all)} model-by-rule cells exceed it.

This is a **disclosed finding about the adopted set's power** under this
analogue, and that is where it stops. It is not a trigger to redraw, and no
redraw is proposed. No item set was touched, selected, or sized in this session,
and `docs/P2/DECISIONS.md`, `src/p2_decisions.py` and the preregistration files
were not edited.

The honest reading is narrow: **if** `Delta-A` turns out to have per-item
dispersion of the same magnitude as a one-sentence insertion's effect on
`post_norm`, then n = 108 detects a 0.05 effect at the power printed above, and
the n that would reach 80% power is the last column. Section 8.2 already stated
that its own 400-item target was a curve over an unmeasured `sigma`; this
replaces the curve with a prior from a structurally analogous manipulation, not
with a measurement.

## 8. What surprised me, as numbers

- **The insertion effect's mean is small and its dispersion is not.** Mean `d_i`
  under `pmi` ranges {tmpl[tmpl.rule == "pmi"]["mean_d"].min():+.4f} to {tmpl[tmpl.rule == "pmi"]["mean_d"].max():+.4f}, while `sigma` ranges {lo:.4f} to {hi:.4f}. A
  one-sentence insertion moves individual items a lot and the average almost not
  at all. If `Delta-A` behaves the same way, the confirmatory tests are
  dispersion-limited rather than effect-limited.
- **`sigma` is rule-dependent.** Range across the three rules, per model:
{"".join(f"  `{m}`: {g['sd_d'].min():.4f} to {g['sd_d'].max():.4f}" + chr(10) for m, g in ex_all.groupby("model"))}
  D109's rule-dependence requirement bites on this figure. A single headline
  `sigma` would be a `pmi` figure, and must be labelled as one.
- **Ties cost permutations but no items.** The `n_tied == 1` filter removes
  {int(att["drop_tied"].sum())} of the {int(att["drop_tile"].sum() + att["kept"].sum() + att["drop_tied"].sum() - att["drop_tile"].sum()):,} `size`-tile Format V rows across all cells, and every one of
  those removals leaves the item's other permutation standing: {int(ex_all["cells_one_perm"].sum())} item-condition
  cells in the template set are averaged over one permutation instead of two,
  and {int(ex_all["lost_unpaired"].sum())} items are lost to unpairing. Every cell keeps all {int(pmi["n_items"].max())} `size`-tile
  items. I expected item attrition and there is none.

## 9. What I could not do

- **`sigma` of `Delta-A` itself.** No Paper 2 data exists. Section 8.2 says so
  and that has not changed. This is the substitute, with the caveat in section 0.
- **The item set here is all {int(pmi["n_items"].max())} `size`-tile items in the frozen 1,000, not the
  108-item finite-`beta_c` subset the adopted confirmatory set uses, and not the
  125-item conflict subset Paper 1's own frontier analyses used
  (`src/frontier_position.py`, `size_conflict_items`). `sigma` was not
  recomputed on either subset. Restricting the item set to compute a `sigma` is
  item-set selection, which this session is prohibited from doing; the brief
  specified the `size` tile and that is what was used. Whether the analogue
  `sigma` differs on the finite-`beta_c` subset is open and is the obvious next
  measurement.

## 10. Chain of custody

```
sha256  notebooks/results_2/choices_llm.parquet
        {p1.artifact_hash(LADDER)}
sha256  notebooks/results_3/choices_llm_t26.parquet
        {p1.artifact_hash(T26)}
P1_ROOT {p1.P1_ROOT}
rows    {len(df):,}  ({len(df[df.source == 'ladder']):,} ladder + {len(df[df.source == 't26']):,} t26)
```

Hashes via `p1.artifact_hash`. Paper 1 gitignores `data/**` and `notebooks/**`
outputs, so these files cannot be pinned by commit and the hash is the available
substitute.

`docs/P2/DECISIONS.md`, `src/p2_decisions.py`, the `PREREGISTRATION_v2*.md`
files, `src/framings.py`, `tests/test_framings.py`,
`data/reference/framings_p2.json` and `docs/P2/README.md` were not modified.
"""
    os.makedirs("reports", exist_ok=True)
    with open(REPORT, "w") as fh:
        fh.write(txt)
    print(f"wrote {REPORT}")
    print(T.to_string(index=False))
    return T


def demo():
    """One runnable check on the two pieces of non-trivial arithmetic."""
    # The power formula and the sample-size formula must be inverses at 80%.
    for s in (0.10, 0.134, 0.25):
        assert abs(realized_power(s, required_n(s)) - POWER) < 1e-9, s
    # n = 108 covers sigma = 0.134 at 80% power, the claim in the brief.
    assert abs(required_n(SIGMA_COVERED) - N_ADOPTED) < 1.5, required_n(SIGMA_COVERED)
    # Section 8.2's own table: sigma 0.10 -> 61 items, 0.20 -> 241.
    assert round(required_n(0.10)) == 60 or round(required_n(0.10)) == 61
    assert abs(required_n(0.20) - 241) < 2
    # per_cell on a hand-built frame: two items, perms averaged, one unpaired.
    g = pd.DataFrame(dict(
        item_id=[1, 1, 1, 1, 2, 2, 2, 2, 3, 3],
        condition=["cond4"] * 2 + ["cond5"] * 2 + ["cond4"] * 2 + ["cond5"] * 2
                  + ["cond4"] * 2,
        post_norm=[0.0, 0.2, 0.4, 0.4, 0.5, 0.5, 0.1, 0.1, 0.9, 0.9]))
    r = per_cell(g)
    assert r["n_items"] == 2 and r["lost_unpaired"] == 1, r
    assert abs(r["mean_d"] - ((0.40 - 0.10) + (0.10 - 0.50)) / 2) < 1e-12, r
    assert abs(r["sd_d"] - float(np.std([0.30, -0.40], ddof=1))) < 1e-12, r
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(0 if main() is not None else 1)
