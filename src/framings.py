"""T3 -- the three P2 framings, F0 / F1 / F2, over P1's frozen Format V rendering.

Authoring only. No model is run and no item is drawn here.

`F0` is P1's rendering, not a copy of it: every prompt below is produced by
calling `render_items.render(..., fmt="V", variant="base")` in P1's own tree, so
the shared content cannot drift. `F1` and `F2` are that string with one constant
block spliced into P1's `{extra}` slot, the position D64's condition-5 insert
occupies. Nothing else moves.

Two author decisions govern this module, neither derivable from the spec or the
preregistration. Both were put to the author and answered on 2026-09-09, before
any framing text was written. They are recorded in `docs/P2/DECISIONS.md` with
the alternatives that were offered and not chosen, quoted verbatim in
`src/p2_decisions.py`, and asserted here at import by `dec.bind`:

  1. `F0` is P1's `base` variant only. The `c5` variant is not carried into P2,
     so a rendering is (item x permutation x framing) and not x variant.
  2. The framing block goes in the `{extra}` slot, after the menu and before the
     question. P1 put its own one-sentence addition about the listener there
     (D64), and D104's PMI neutral prompt already excludes that slot, so scoring
     normalisation is identical across the three framings.

Run: python3 src/framings.py
"""
import hashlib
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd

import adversary
import p1
import p2_decisions as dec

import render_items                                             # noqa: E402
from decisions import D64_COND5_INSERT, assert_verbatim         # noqa: E402

OUT_JSON = "data/reference/framings_p2.json"
OUT_REPORT = "reports/T3_framings.md"

# The splice point. P1's BASE ends `"{options}\n{extra}Which do you send?"` and
# `variant="base"` sets `extra` to a bare newline, so every F0 prompt ends with
# this exact string. Derived from P1's template, never typed independently.
ANCHOR = "\n\nWhich do you send?"

# The two values P2-D1 and P2-D2 govern, declared here and checked against
# `docs/P2/DECISIONS.md` by `dec.bind` below. Changing either without changing
# the decision log fails at import.
VARIANT = "base"                                    # P2-D1
RENDERING_AXES = ("item", "permutation", "framing")  # P2-D1: no variant axis
assert render_items.BASE.endswith("{options}\n{extra}Which do you send?")
assert render_items.BASE.format(left="", right="", tm="", tc="", options="x",
                                extra="\n").endswith("x" + ANCHOR)

# D64 is quoted here only to fix the shape F1 and F2 imitate: two to four hard
# wrapped lines in the `{extra}` slot, no blank line inside the block. If P1's
# constant drifts, this assertion is the tripwire.
assert_verbatim("D64 shape reference", D64_COND5_INSERT.count("\n"), 1)

# --------------------------------------------------------------- the framings
#
# Sentences 1 and 2 are shared by F1 and F2 verbatim. Sentence 3 is the only
# thing that differs, and it is the mechanism statement. F1's sentence 3 is
# neutral filler: it restates two facts the prompt has already given (the
# Scientist knows the pair, the other person does not) and adds no new fact, so
# the F1/F2 contrast is mechanism and not length.
#
# Every word is checked against four lists by `leak_check`: the four banned
# words in T3, P1's `BANNED`, P1's `GAME_TERMS`, and P1's `TILE_TERMS`. Note
# `means` is a P1 game term, which is why sentence 1 does not say "the means by
# which".
_PRESENCE = (
    "A third person also sees both lists and already knows the pair. After you "
    "send\nyour description, that person will speak to the other person, and "
    "wants them\nto name a different pair. ")

F1_BLOCK = _PRESENCE + (
    "They know the pair, and the other person still\ndoes not know what it is.")

F2_BLOCK = _PRESENCE + (
    "They will argue for whichever wrong pair your\ndescription makes look "
    "most likely.")

FRAMINGS = {"F0": "", "F1": F1_BLOCK, "F2": F2_BLOCK}

# D100, Paper 2 side. Binds this module to `docs/P2/DECISIONS.md` P2-D1 and
# P2-D2. A drift in the variant, the splice position, the framing set or the
# rendering axes fails here, before any prompt can be built from it.
dec.bind(VARIANT, ANCHOR, tuple(FRAMINGS), RENDERING_AXES)

# T3's four banned words, on top of P1's own lists.
T3_BANNED = [r"\bmargin\w*\b", r"\bmaximi[sz]\w*\b", r"\boptimal\w*\b",
             r"\bbayes\w*\b"]


def render(words, it, perm, framing, tiles):
    """One prompt. `it` is a row of P1's `items_final`, `perm` an option order.

    `framing` in {"F0", "F1", "F2"}. F0 is P1's frozen Format V base rendering,
    byte for byte, produced by P1's own renderer; F1 and F2 splice a constant
    block into the `{extra}` slot.
    """
    base = render_items.render(words, it["means"], it["clues"],
                               it["target_means"], it["target_clue"],
                               tiles[it["tile"]]["options"], perm, "V", VARIANT)
    return splice(base, FRAMINGS[framing])


def splice(base, block):
    """`base` with `block` inserted into the `{extra}` slot. Identity if empty."""
    if not block:
        return base
    head, sep, tail = base.rpartition(ANCHOR)
    if not sep:
        raise ValueError("anchor absent: the P1 template has changed")
    return head + "\n\n" + block + sep + tail


def unsplice(text, block):
    """Inverse of `splice`. Returns the F0 prompt, or raises.

    This is the leak check that matters. `block` is a module constant, so a
    prompt that survives removal of that exact string carries no item-specific
    framing content: anything item-dependent inside the block would make the
    removal fail on some item.
    """
    if not block:
        return text
    marker = "\n\n" + block
    head, sep, tail = text.rpartition(marker)
    if not sep:
        raise ValueError("block not found verbatim")
    if marker in head:
        raise ValueError("block occurs more than once")
    return head + tail


# ------------------------------------------------------------------ the check
def leak_check(tiles, words):
    """(rows, n_violations). Every rule is a hard failure, none is advisory."""
    rows = []
    blocks = {k: v for k, v in FRAMINGS.items() if v}
    flat = " ".join(blocks.values())

    def add(name, n):
        rows.append([name, n, "PASS" if n == 0 else "FAIL"])

    add("T3 banned words (margin / maximize / optimal / Bayesian)",
        sum(len(re.findall(p, flat, re.I)) for p in T3_BANNED))
    add("P1 BANNED (correct / best / optimal / right answer)",
        sum(len(re.findall(p, flat, re.I)) for p in render_items.BANNED))
    add(f"P1 GAME_TERMS ({len(render_items.GAME_TERMS)} patterns)",
        sum(len(re.findall(p, flat, re.I)) for p in render_items.GAME_TERMS))
    add("P1 TILE_TERMS (size / manmade / moves / hold)",
        sum(len(re.findall(p, flat, re.I))
            for pats in render_items.TILE_TERMS.values() for p in pats))
    add("no option string appears in any block",
        sum(1 for t in tiles.values() for o in t["options"]
            if o.lower() in flat.lower()))
    add("no pool concept name appears in any block",
        len({w for w in words if re.search(rf"\b{re.escape(w)}\b", flat, re.I)}))
    add("block is a single paragraph, no blank line",
        sum(b.count("\n\n") for b in blocks.values()))
    add("every line wraps at or under 79 characters",
        sum(1 for b in blocks.values() for ln in b.split("\n") if len(ln) > 79))
    add("F1 and F2 share sentences 1 and 2 verbatim",
        0 if F1_BLOCK.startswith(_PRESENCE) and F2_BLOCK.startswith(_PRESENCE)
        else 1)
    return rows, sum(r[1] for r in rows)


def _opt_name(tiles, tile, o):
    return tiles[tile]["options"][int(o)]


def _pair_name(words, it, h):
    """Flat hypothesis id h = m * C + c, back to the two concept words."""
    return (f"{words[it['means'][h // int(it['C'])]]} + "
            f"{words[it['clues'][h % int(it['C'])]]}")


# ------------------------------------------------------------------- the run
def md(rows, headers, aligns=None):
    aligns = aligns or ["---"] * len(headers)
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "|" + "|".join(aligns) + "|"]
                     + ["| " + " | ".join(str(x) for x in r) + " |" for r in rows])


def main():
    pool = pd.read_csv(p1.POOL)
    words = pool["Word"].values
    tiles = {t["id"]: t for t in json.load(open(p1.TILES))["tiles"]}
    items = p1.load_items().set_index("item_id")
    frozen = pd.read_parquet(os.path.join(
        p1.P1_ROOT, "data/processed/items_rendered.parquet"))
    V = frozen[(frozen["format"] == "V") & (frozen["variant"] == "base")]

    buf = []
    w = buf.append
    w("# T3: prompt conditions F0 / F1 / F2\n")
    w(f"Generated by `python3 src/framings.py`. Spec `{adversary.SPEC_VERSION}`, "
      "`docs/spec/adversary-game-v1.md`. Deterministic, no seed: the "
      "permutations are read from P1's frozen renderings rather than redrawn.\n")

    # ---------------- 1. the three templates ----------------
    w("\n## 1. The three framings\n")
    w("`F0` is P1's Format V `base` rendering, produced by calling "
      "`render_items.render` in P1's tree. `F1` and `F2` are that string with "
      "one constant block spliced into the `{extra}` slot, the position D64's "
      "condition-5 insert occupies, immediately before `Which do you send?`.\n")
    for k in ("F0", "F1", "F2"):
        b = FRAMINGS[k]
        w(f"\n**{k}** " + ("(no block; identical to P1)\n" if not b else "\n"))
        if b:
            w("```\n" + b + "\n```\n")

    # ---------------- 2. F0 diff ----------------
    w("\n## 2. `F0` against Paper 1, byte for byte\n")
    bad, n = [], 0
    for _, r in V.iterrows():
        it = items.loc[r["item_id"]]
        got = render(words, it, tuple(r["option_order"]), "F0", tiles)
        n += 1
        if got != r["text"]:
            bad.append(int(r["item_id"]))
    w(f"Regenerated all **{n:,}** Format V `base` renderings in "
      "`items_rendered.parquet` and compared to the frozen text.\n")
    w(f"```\nrenderings compared   {n:,}\nbyte-level mismatches "
      f"{len(bad):,}\n```\n")
    if bad:
        w(f"MISMATCHING item ids: {bad[:20]}\n")
        open(OUT_REPORT, "w").write("\n".join(buf))
        sys.exit(f"STOP: F0 is not byte-identical to Paper 1 on {len(bad)} renderings")
    w("**Zero content drift.** `F0` is Paper 1's prompt, not a reproduction of "
      "it.\n")
    w("\nAnd the framings are additive: removing the constant block from every "
      "`F1` and `F2` prompt returns the `F0` prompt exactly.\n")
    back = 0
    for _, r in V.iterrows():
        it = items.loc[r["item_id"]]
        f0 = render(words, it, tuple(r["option_order"]), "F0", tiles)
        for k in ("F1", "F2"):
            t = render(words, it, tuple(r["option_order"]), k, tiles)
            back += int(unsplice(t, FRAMINGS[k]) != f0)
    w(f"```\nF1/F2 prompts round-tripped   {2*n:,}\nfailures to recover F0        "
      f"{back:,}\n```\n")
    if back:
        open(OUT_REPORT, "w").write("\n".join(buf))
        sys.exit("STOP: framing block is not item-invariant")

    # ---------------- 3. length parity ----------------
    w("\n## 3. Length parity, `F1` against `F2`\n")
    w("Sentences 1 and 2 are shared verbatim. Only sentence 3 differs.\n")
    s1 = _PRESENCE.strip()
    t1 = F1_BLOCK[len(_PRESENCE):]
    t2 = F2_BLOCK[len(_PRESENCE):]
    rows = [["shared, sentences 1-2", len(s1.replace("\n", " ")),
             len(s1.split()), "both"],
            ["`F1` sentence 3 (neutral filler)", len(t1.replace("\n", " ")),
             len(t1.split()), "F1 only"],
            ["`F2` sentence 3 (mechanism)", len(t2.replace("\n", " ")),
             len(t2.split()), "F2 only"]]
    w(md(rows, ["segment", "chars", "words", "in"],
         ["---", "---:", "---:", "---"]))
    dc = len(t2.replace("\n", " ")) - len(t1.replace("\n", " "))
    dw = len(t2.split()) - len(t1.split())
    w(f"\n**Differing-sentence delta: `F2` minus `F1` = {dw:+d} words, "
      f"{dc:+d} characters.**\n")
    w("\nWhole-block and whole-prompt deltas, which are what a model sees:\n")
    rows = [[f"`{k}` block", len(FRAMINGS[k].replace("\n", " ")),
             len(FRAMINGS[k].split())] for k in ("F1", "F2")]
    w(md(rows, ["block", "chars", "words"], ["---", "---:", "---:"]))
    lens = {}
    for k in ("F0", "F1", "F2"):
        c = [len(render(words, items.loc[r["item_id"]],
                         tuple(r["option_order"]), k, tiles))
             for _, r in V.iterrows()]
        lens[k] = c
    rows = []
    for t in tiles:
        ids = set(V[V["item_id"].isin(items[items["tile"] == t].index)]["item_id"])
        sel = [i for i, (_, r) in enumerate(V.iterrows()) if r["item_id"] in ids]
        rows.append([f"`{t}`", len(tiles[t]["options"]),
                     int(np.median([lens['F0'][i] for i in sel])),
                     int(np.median([lens['F1'][i] for i in sel])),
                     int(np.median([lens['F2'][i] for i in sel])),
                     f"{np.median([lens['F2'][i] for i in sel]) - np.median([lens['F1'][i] for i in sel]):+.0f}"])
    w("\n" + md(rows, ["tile", "\\|O\\|", "F0 median chars", "F1", "F2",
                       "F2 - F1"],
                ["---", "---:", "---:", "---:", "---:", "---:"]))
    pct = 100.0 * dc / len(F2_BLOCK.replace("\n", " "))
    w(f"\nThe `F2` block is {pct:.1f}% longer than `F1`'s, and "
      f"{100.0*dc/np.median(lens['F1']):.2f}% of a median `F1` prompt. "
      "Preregistration section 4.5 cell 4 takes this number as the input to its "
      "length-artifact diagnosis; it is small enough that a length explanation "
      "for an `F1`-only effect would have to survive the `TV(m, F1)` check in "
      "the same paragraph, not rest on the word count.\n")
    w("\nOne register difference is stated rather than engineered away: `F2`'s "
      "sentence 3 contains the word `wrong` and `F1`'s does not. It cannot be "
      "removed, because naming the wrong-answer set is what the mechanism "
      "statement is. The shared sentence 2, `wants them to name a different "
      "pair`, carries the same content in both framings.\n")

    # ---------------- 4. leak check ----------------
    w("\n## 4. Leak check\n")
    w("The framing must be computable from the task setup alone: no reference "
      "to `h*` beyond what P1's prompt already states, none to the margin, and "
      "none to which signal to send. Implemented in `leak_check` and re-run by "
      "`tests/test_framings.py`.\n")
    rows, nviol = leak_check(tiles, words)
    w(md([[r[0], r[1], f"**{r[2]}**"] for r in rows],
         ["check", "violations", "result"], ["---", "---:", "---"]))
    w(f"\nPlus the structural check in section 2: **{back}** of {2*n:,} `F1` and "
      "`F2` prompts fail to return `F0` when the constant block is removed. "
      "That is the check that actually rules out per-item framing content, "
      "because a block carrying anything item-specific could not be a module "
      "constant and would fail the removal on some item.\n")
    if nviol:
        open(OUT_REPORT, "w").write("\n".join(buf))
        sys.exit(f"STOP: {nviol} leak-check violations")

    # ---------------- 5. adversarial review cases ----------------
    w("\n## 5. Adversarial review cases\n")
    w("Three per framing. Each is a wording a careless author would write, the "
      "quantity it resolves to, and a real item on which that quantity is "
      "named. The adopted wording resolves to nothing on any of them: it is a "
      "module constant and section 2 shows it is byte-identical across all "
      f"{n:,} renderings.\n")

    size = items[items["tile"] == "size"].copy()
    conflict = size[size["conflict"]].sort_values("fit_cost", ascending=False)
    batch = adversary.build_batch(size.reset_index())
    o_inf = adversary.optimal_option(batch, math.inf)
    d_star = adversary.best_response_batch(batch)
    ix = {int(i): k for k, i in enumerate(batch.item_id)}

    picks = list(conflict.index[:3]) + list(conflict.index[3:6]) + \
        list(conflict.index[6:9])
    cases = [
        ("F0", "Send the description that fits your pair most closely.",
         "o_fit", "Names a signal outright. On a conflict item `o_fit` is not "
         "P1's oracle, so the sentence resolves to a specific option and to the "
         "one P1 measures models for over-choosing."),
        ("F0", "Send the description that makes your pair stand out furthest "
         "from every other pairing.",
         "o_inf", "The margin rule in words, which T3 item 3 forbids and which "
         "under `F0` has no adversary to justify it. It would hand `F0` the "
         "`beta -> infinity` answer."),
        ("F0", "Send the description the other person is most likely to read "
         "as your pair.",
         "o_bayes", "States the `F0` answer directly: `o_bayes` is "
         "`argmax_o L(h*|o)`."),
        ("F1", "A third person also sees both lists and already knows the pair, "
         "and will argue for whichever other pairing your description fits "
         "next best.",
         "d_star", "Withholding the mechanism is the entire purpose of `F1`. "
         "This states R1 and makes `F1` a second copy of `F2`, destroying the "
         "load-bearing contrast."),
        ("F1", "A third person also sees both lists and already knows the pair "
         "is the two objects you were told, and will name something else.",
         "h_star", "Re-states `h*` inside the framing. The block would have to "
         "be item-specific and would fail section 2's removal check."),
        ("F1", "A third person will argue against you, so leave as much room as "
         "you can between your pair and the nearest rival.",
         "o_inf", "An instruction about the margin, therefore about which "
         "signal to send, smuggled into the framing that is supposed to say "
         "only that an adversary exists."),
        ("F2", "They will argue for whichever wrong pair your description makes "
         "look most likely, so send the description whose lead over the next "
         "pairing is largest.",
         "o_inf", "Sentence 3 as adopted is fine; the trailing clause is not. "
         "It turns a description of the adversary into an instruction naming "
         "`o*_infinity`."),
        ("F2", "They will argue for the pairing that comes second under your "
         "description, which on this item is the one you can see coming.",
         "d_star", "Item-specific by construction. A block that names the "
         "runner-up cannot be constant, and section 2's round trip fails."),
        ("F2", "They will argue for whichever wrong pair looks most likely, so "
         "avoid descriptions under which two pairings look alike.",
         "o_inf", "The margin rule restated as advice. `F2` may describe what "
         "the adversary does; it may not tell the Scientist what to do about "
         "it."),
    ]
    rows = []
    for (fr, careless, quant, why), iid in zip(cases, picks):
        it = items.loc[iid]
        k = ix[int(iid)]
        if quant == "o_fit":
            named = f"`{_opt_name(tiles, 'size', it['o_fit'])}`"
        elif quant == "o_bayes":
            named = f"`{_opt_name(tiles, 'size', it['o_bayes'])}`"
        elif quant == "o_inf":
            named = f"`{_opt_name(tiles, 'size', o_inf[k])}`"
        elif quant == "d_star":
            named = ("`" + _pair_name(words, it,
                     d_star[k, int(it['o_bayes'])]) + "`")
        else:
            named = f"`{words[it['target_means']]} + {words[it['target_clue']]}`"
        others = {"o_fit": _opt_name(tiles, "size", it["o_fit"]),
                  "o_bayes": _opt_name(tiles, "size", it["o_bayes"]),
                  "o_inf": _opt_name(tiles, "size", o_inf[k])}
        rows.append([fr, int(iid), f"`{quant}`", named,
                     " / ".join(f"`{v}`" for v in dict.fromkeys(
                         others[q][len("about the size of "):]
                         for q in ("o_fit", "o_bayes", "o_inf")))])
        w(f"\n**{fr}, item {iid}.** Careless wording:\n")
        w("> " + careless + "\n")
        w(f"Resolves to `{quant}` = {named} on this item. {why}\n")
        w(f"On this item `o_fit` / `o_bayes` / `o*_infinity` are "
          + " / ".join(f"`{others[q][len('about the size of '):]}`"
                       for q in ("o_fit", "o_bayes", "o_inf"))
          + ", so the careless wording selects among them rather than "
            "describing the game.\n")
        w(f"Adopted `{fr}`: "
          + ("no block. P1's prompt is unchanged, and section 2 shows it is "
             "byte-identical to the frozen rendering for this item."
             if fr == "F0" else
             f"the block `sha256:{hashlib.sha256(FRAMINGS[fr].encode()).hexdigest()[:12]}`, "
             "the same string on this item as on every other one.") + "\n")
    w("\n**Summary of what each careless wording would have named:**\n")
    w(md(rows, ["framing", "item", "quantity",
                "option or pairing it names",
                "the item's `o_fit` / `o_bayes` / `o*_inf`"],
         ["---", "---:", "---", "---", "---"]))
    w("\nThe last column is abbreviated: every `size` option reads "
      "`about the size of X` and only `X` is shown. Where it lists more than "
      "one value the three oracles disagree on that item, which is why a "
      "careless wording naming any of them would be naming a specific and "
      "different option.\n")
    w("\nThe adopted `F1` and `F2` blocks name none of these. They contain no "
      "option string, no pool concept name and no tile term (section 4), and "
      "they are one constant string across every item (section 2). `F2`'s "
      "sentence 3 states the adversary's rule, `d*(o) = argmax_{h != h*} "
      "L(h|o)` from spec section 4, which is a property of the game and not of "
      "the item: it is the same sentence whatever `h*`, `o` and `d*` turn out "
      "to be.\n")

    # ---------------- 6. response format ----------------
    w("\n## 6. Response format\n")
    w("Unchanged across framings. Every prompt ends with the same "
      f"`{ANCHOR!r}` and the option menu is P1's, so the scored strings are the "
      "option texts verbatim under Format V and parsing is untouched "
      "(preregistration section 7.2). D104's PMI neutral prompt is built from "
      "the menu and the question only, and the framing block sits outside it, "
      "exactly as D104 holds the condition-5 insert outside it: the "
      "normalisation denominator is identical under `F0`, `F1` and `F2`.\n")
    w("\nNo chain-of-thought scaffolding, hint or worked example is added, and "
      "no shared byte is changed, so P1's zero-shot forced choice is what all "
      "three framings measure.\n")

    # ---------------- 7. custody ----------------
    w("\n## 7. Chain of custody\n")
    payload = {
        "schema_version": 1,
        "generated_by": "src/framings.py",
        "spec_version": adversary.SPEC_VERSION,
        "format": "V",
        "p1_variant": "base",
        "governing_record": "docs/P2/DECISIONS.md, P2-D1 (variant) and P2-D2 "
                            "(insertion slot). Bound at import by "
                            "src/p2_decisions.py. This file is a deliverable, "
                            "not the record: read the log.",
        "p1_variant_note": dec.P2D1_TEXT.replace("\n", " "),
        "f0_replication_target": dec.P2_F0_REPLICATION_TARGET,
        "rendering_axes": list(dec.P2_RENDERING_AXES),
        "insertion_slot": dec.P2D2_TEXT.replace("\n", " "),
        "base_template": render_items.BASE,
        "framings": FRAMINGS,
    }
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
    rows = [[f"`{k}` block", "n/a (empty)" if not v else
             hashlib.sha256(v.encode()).hexdigest()[:16]]
            for k, v in FRAMINGS.items()]
    rows.append(["P1 `BASE` template",
                 hashlib.sha256(render_items.BASE.encode()).hexdigest()[:16]])
    for nm, path in (("items_final.parquet", p1.ITEMS_FINAL),
                     ("items_rendered.parquet",
                      os.path.join(p1.P1_ROOT,
                                   "data/processed/items_rendered.parquet"))):
        rows.append([f"P1 `{nm}`", p1.artifact_hash(path)[:16]])
    w(md(rows, ["artifact", "sha256 (first 16)"], ["---", "---"]))
    w(f"\nFrozen framings: `{OUT_JSON}`. Test suite: "
      "`tests/test_framings.py`.\n")

    open(OUT_REPORT, "w").write("\n".join(buf))
    print(f"wrote {OUT_REPORT}, {OUT_JSON}")
    print(f"F0 byte mismatches vs P1: {len(bad)} of {n:,}")
    print(f"F1/F2 round-trip failures: {back} of {2*n:,}")
    print(f"leak-check violations: {nviol}")
    print(f"F2 - F1 differing sentence: {dw:+d} words, {dc:+d} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
