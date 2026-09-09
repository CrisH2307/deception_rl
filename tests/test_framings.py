"""T3 acceptance tests for the F0 / F1 / F2 framings.

Real tests against the frozen Paper 1 artifacts. Three things must hold, each a
separate failure mode: F0 is Paper 1's prompt rather than a copy of it, the
framing block is item-invariant, and nothing in the block can be read off the
item.

Run: python3 tests/test_framings.py
"""
import json
import functools
import os
import re
import sys

import pandas as pd

sys.path.insert(0, "src")

import framings as fr        # noqa: E402
import p1                    # noqa: E402
import p2_decisions as dec   # noqa: E402

# Import order is load-bearing and is the hazard itself: `decisions` and
# `render_items` live in Paper 1's tree, which only reaches `sys.path` once
# `p1` has been imported. Alphabetising these two above `p1` raises
# ModuleNotFoundError today, and would silently resolve to a Paper 2 file of the
# same name if one existed. `test_p2_binding_module_does_not_shadow_paper1`.
import decisions             # noqa: E402
import render_items          # noqa: E402

RENDERED = os.path.join(p1.P1_ROOT, "data/processed/items_rendered.parquet")


@functools.lru_cache(maxsize=1)
def ctx():
    """(words, tiles, items, V). V is P1's 2,000 frozen Format V base rows."""
    words = pd.read_csv(p1.POOL)["Word"].values
    tiles = {t["id"]: t for t in json.load(open(p1.TILES))["tiles"]}
    items = p1.load_items().set_index("item_id")
    V = pd.read_parquet(RENDERED)
    V = V[(V["format"] == "V") & (V["variant"] == "base")].reset_index(drop=True)
    return words, tiles, items, V


def prompts(framing, n=None):
    words, tiles, items, V = ctx()
    for _, r in (V if n is None else V.iloc[:n]).iterrows():
        yield r, fr.render(words, items.loc[r["item_id"]],
                           tuple(r["option_order"]), framing, tiles)


def shared():
    """Sentences 1-2, verbatim in both blocks. Not `commonprefix`: both third
    sentences begin "They ", so the common prefix runs past the sentence end."""
    assert os.path.commonprefix([fr.F1_BLOCK, fr.F2_BLOCK]).startswith(fr._PRESENCE)
    return fr._PRESENCE


def test_f0_is_paper1_byte_for_byte():
    """The whole point of F0. Zero content drift on every frozen rendering."""
    bad = [int(r["item_id"]) for r, t in prompts("F0") if t != r["text"]]
    assert bad == [], f"{len(bad)} renderings drifted, first: {bad[:5]}"


def test_f1_f2_are_f0_plus_a_constant_block():
    """Item-invariance. A block carrying item content could not round-trip."""
    for framing in ("F1", "F2"):
        for (r, t), (_, f0) in zip(prompts(framing), prompts("F0")):
            assert fr.unsplice(t, fr.FRAMINGS[framing]) == f0, r["item_id"]


def test_block_sits_in_the_d64_slot():
    """Immediately before the question, where P1 put the condition-5 insert."""
    for framing in ("F1", "F2"):
        for _, t in prompts(framing, n=40):
            assert t.endswith(fr.FRAMINGS[framing] + fr.ANCHOR)


def test_response_format_is_unchanged():
    """Same final question, same verbatim option menu, so parsing is fixed."""
    _, tiles, _, _ = ctx()
    for framing in ("F0", "F1", "F2"):
        for r, t in prompts(framing, n=60):
            assert t.endswith("Which do you send?")
            assert t.count("Which do you send?") == 1
            for o in tiles[r["tile"]]["options"]:
                assert o in t, (framing, r["item_id"], o)


def test_leak_check_passes():
    words, tiles, _, _ = ctx()
    rows, n = fr.leak_check(tiles, words)
    assert n == 0, [r for r in rows if r[1]]


def test_t3_banned_words_absent():
    """margin / maximize / optimal / Bayesian, T3's anti-requirement."""
    for pattern in fr.T3_BANNED:
        for k, b in fr.FRAMINGS.items():
            assert not re.search(pattern, b, re.I), (k, pattern)


def test_p1_word_lists_absent():
    """P1's own BANNED, GAME_TERMS and TILE_TERMS, imported not copied."""
    flat = " ".join(fr.FRAMINGS.values())
    pats = (list(render_items.BANNED) + list(render_items.GAME_TERMS)
            + [p for ps in render_items.TILE_TERMS.values() for p in ps])
    assert [p for p in pats if re.search(p, flat, re.I)] == []


def test_f1_and_f2_differ_only_in_the_final_sentence():
    """The load-bearing contrast is mechanism, not wording drift."""
    s = shared()
    assert s.rstrip().endswith("name a different pair.")
    assert fr.F1_BLOCK[len(s):].count(".") == 1
    assert fr.F2_BLOCK[len(s):].count(".") == 1


def test_length_parity():
    """Not a tuned threshold: a whole extra rendered line would be a confound."""
    s = shared()
    t1, t2 = fr.F1_BLOCK[len(s):], fr.F2_BLOCK[len(s):]
    assert abs(len(t2) - len(t1)) < 79, (len(t1), len(t2))
    assert abs(len(t2.split()) - len(t1.split())) <= 3


def test_unsplice_rejects_a_block_that_is_not_there():
    """The round-trip check is only evidence if its negative case fails."""
    _, _, items, V = ctx()
    words, tiles = ctx()[0], ctx()[1]
    r = V.iloc[0]
    f0 = fr.render(words, items.loc[r["item_id"]], tuple(r["option_order"]),
                   "F0", tiles)
    for framing in ("F1", "F2"):
        try:
            fr.unsplice(f0, fr.FRAMINGS[framing])
        except ValueError:
            continue
        raise AssertionError(f"unsplice accepted an F0 prompt as {framing}")
    f1 = fr.render(words, items.loc[r["item_id"]], tuple(r["option_order"]),
                   "F1", tiles)
    try:
        fr.unsplice(f1, fr.F2_BLOCK)
    except ValueError:
        return
    raise AssertionError("unsplice removed the F2 block from an F1 prompt")


def test_frozen_json_matches_the_module():
    """The artifact and the code cannot drift apart silently."""
    d = json.load(open("data/reference/framings_p2.json"))
    assert d["framings"] == fr.FRAMINGS
    assert d["base_template"] == render_items.BASE
    assert d["p1_variant"] == "base"
    assert d["format"] == "V"


# ------------------------------------------------- D100, the Paper 2 bindings
def test_p2_decision_log_quotes_the_constants():
    """`docs/P2/DECISIONS.md` is the source. The constants must still match it,
    including the alternatives that were offered and not chosen."""
    assert dec.check_log("docs/P2/DECISIONS.md")


def test_p2_binding_rejects_drift():
    """The bind is only a tripwire if its negative case fires. Perturb each of
    the four governed values in turn and require the import-time check to fail."""
    good = (fr.VARIANT, fr.ANCHOR, tuple(fr.FRAMINGS), fr.RENDERING_AXES)
    dec.bind(*good)                                          # the live values pass
    drifted = [
        ("variant", ("c5", good[1], good[2], good[3])),
        ("variant", ("", good[1], good[2], good[3])),
        ("slot anchor", (good[0], "\n\nWhich do you send", good[2], good[3])),
        ("slot anchor", (good[0], "\nWhich do you send?", good[2], good[3])),
        ("framing ids", (good[0], good[1], ("F0", "F1"), good[3])),
        ("framing ids", (good[0], good[1], ("F0", "F1", "F2", "F3"), good[3])),
        ("rendering axes", (good[0], good[1], good[2],
                            ("item", "permutation", "variant", "framing"))),
    ]
    for what, args in drifted:
        try:
            dec.bind(*args)
        except AssertionError:
            continue
        raise AssertionError(f"bind accepted a drifted {what}: {args}")


def test_framings_renders_with_the_governed_variant():
    """P2-D1 is structural, not a comment: the value reaching P1's renderer is
    the one the log governs, and there is no variant axis."""
    assert fr.VARIANT == dec.P2D1_VARIANT == "base"
    assert "variant" not in fr.RENDERING_AXES
    assert fr.RENDERING_AXES == dec.P2_RENDERING_AXES
    words, tiles, items, V = ctx()
    r = V.iloc[0]
    seen = {}
    real = render_items.render

    def spy(*a, **kw):
        seen["variant"] = a[-1] if len(a) >= 9 else kw.get("variant")
        return real(*a, **kw)

    render_items.render = spy
    try:
        fr.render(words, items.loc[r["item_id"]], tuple(r["option_order"]),
                  "F1", tiles)
    finally:
        render_items.render = real
    assert seen["variant"] == dec.P2D1_VARIANT, seen


def test_p2_binding_module_does_not_shadow_paper1():
    """`src/p2_decisions.py` is not called `decisions.py` for a reason. A bare
    `import decisions` must still reach Paper 1's frozen module: a Paper 2 file
    of that name silently replaces it, no-op `assert_verbatim` included."""
    assert os.path.realpath(decisions.__file__).startswith(
        os.path.realpath(p1.P1_ROOT)), decisions.__file__
    assert decisions.assert_verbatim is dec.assert_verbatim
    assert not os.path.exists("src/decisions.py"), (
        "src/decisions.py shadows Paper 1's frozen module; see docs/P2/DECISIONS.md")


if __name__ == "__main__":
    ok = True
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"ok  {name}")
            except AssertionError as e:
                ok = False
                print(f"FAIL {name}: {e}")
    sys.exit(0 if ok else 1)
