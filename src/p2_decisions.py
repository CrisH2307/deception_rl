"""Verbatim Paper 2 decision text, in one place, asserted at import.

Paper 1's D100: verification must bind an artifact to the decision that governs
it, not only to itself. This is Paper 2's equivalent. The source is
`docs/P2/DECISIONS.md`; every string below is quoted from it verbatim, and any
script producing an artifact derived from one of these decisions imports the
constant and asserts against it, so a drift fails at import rather than entering
the stimulus silently.

**Never edit a constant here to make a caller pass.** `docs/P2/DECISIONS.md` is
the source; if they disagree, that is the bug this module exists to surface.

Not named `decisions.py`. Paper 1's frozen `decisions.py` is imported by bare
name from Paper 1's `src/`, which `src/p1.py` puts on `sys.path`, and a Paper 2
file of that name shadows it for any Paper 2 module importing `decisions` before
`p1` has run. Measured 2026-09-09: a decoy was returned in place of Paper 1's,
carrying a drifted `D64_COND5_INSERT` and a no-op `assert_verbatim`, and the
import raised nothing. See `docs/P2/DECISIONS.md`.

Run: python3 src/p2_decisions.py     (checks the constants against the log)
"""
import os
import sys

import p1  # noqa: F401  puts Paper 1's src on sys.path; must precede the import below

# Paper 1's frozen helper, by import. A second copy would be the duplication bug
# this module exists to prevent.
from decisions import assert_verbatim                            # noqa: E402

LOG = os.path.join(os.path.dirname(__file__), "..", "docs/P2/DECISIONS.md")


# --------------------------------------------------------- P2-D1, the variant
P2D1_TEXT = (
    "`F0` is Paper 1's Format V `base` rendering only. Paper 1's `c5` variant, the D64\n"
    "condition-5 insert, is not carried into Paper 2. A Paper 2 rendering is\n"
    "(item x permutation x framing) and not x variant. `F0`'s replication target is\n"
    "Paper 1's condition 4."
)
P2D1_VARIANT = "base"
# The alternatives offered and not chosen, verbatim as the log heads them. A
# decision record that keeps only the chosen option cannot be audited, so these
# are bound the same way the decision text is.
P2D1_REJECTED = ("Cross variant by framing.", "`c5` as the `F0` base.")

# ------------------------------------------------------------- P2-D2, the slot
P2D2_TEXT = (
    "The `F1` and `F2` framing block goes in Paper 1's `{extra}` slot, after the option\n"
    "menu and immediately before `Which do you send?`. That is the position D64's\n"
    "condition-5 insert occupies, and D104's PMI neutral prompt already excludes the\n"
    "slot, so the scoring normalisation is identical under `F0`, `F1` and `F2`."
)
P2D2_SLOT_ANCHOR = "\n\nWhich do you send?"
P2D2_REJECTED = ("After the audience paragraph, before the menu.",)

# ------------------------------------------ P2-D3, Arm B's unit of analysis
P2D3_TEXT = (
    "Arm B's confirmatory analysis is per tile, on the `size` tile alone. Pooling across\n"
    "tiles with tile as a stratum is rejected. This preserves `PREREGISTRATION_v2.md`\n"
    "section 2 unchanged: the confirmatory set is `size`-tile items with finite\n"
    "`beta_c`, and `manmade`, `moves` and `hold` stay secondary."
)
P2D3_TILE = "size"
P2D3_POOLED = False
P2D3_REJECTED = ("Pooled across tiles with tile as a stratum.",)

# ------------------------------------------------ P2-D4, the confirmatory items
P2D4_TEXT = (
    "Arm B's confirmatory analysis set is the `size` tile of Paper 1's frozen\n"
    "`items_final.parquet`, restricted to items with finite `beta_c`: 108 items. No new\n"
    "item draw is authorized. Redraw variant (a), uniform enlargement of all four tiles,\n"
    "is rejected outright. Redraw variant (b), enlarging the `size` tile only, is neither\n"
    "adopted nor rejected: its size depends on `sigma` for `\u0394A`, which is unmeasured."
)
# P1 gitignores data/**, so the frozen input cannot be pinned by commit from P2.
# The hash is the substitute, and it is what makes P2-D4 mechanically checkable:
# an Arm B run against any other item file fails here rather than in the results.
P2D4_ITEMS_SHA256 = "ec79b071dcfabd6094f9a91a2278cce0a6008ffd304c9935bd96850437218289"
P2D4_N_CONFIRMATORY = 108
P2D4_REJECTED = ("Redraw variant (a), uniform ~871 per tile, 3,487 total.",
                 "Redraw variant (b), enlarging `size` only.")


# ------------------------------------------------- what P2-D1 makes structural
P2_FRAMING_IDS = ("F0", "F1", "F2")
P2_RENDERING_AXES = ("item", "permutation", "framing")
P2_F0_REPLICATION_TARGET = "Paper 1 condition 4 (Format V, base variant)"


def bind_armb(tile, items_sha256, pooled):
    """Assert an Arm B caller's own behaviour against P2-D3 and P2-D4.

    Takes what the caller actually did, not what it meant to do: the tile it
    filtered to, the sha256 of the item file it loaded, and whether it pooled.
    A pooled run, a run on a second tile, or a run against a redrawn item file
    fails at import rather than in the results table.

    `sigma` for the primary measure is unmeasured, so P2-D4 leaves a `size`-tile
    enlargement open (PREREGISTRATION_v2.3 section 6). If one is ever authorized,
    the hash here changes and this function is where that lands.
    """
    checks = (("P2-D3 confirmatory tile", tile, P2D3_TILE),
              ("P2-D3 pooling", bool(pooled), P2D3_POOLED),
              ("P2-D4 item file sha256", items_sha256, P2D4_ITEMS_SHA256))
    for label, actual, expected in checks:
        try:
            assert_verbatim(label, str(actual), str(expected))
        except AssertionError as e:
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None


def bind(variant, anchor, framing_ids, axes):
    """Assert a caller's own behaviour against P2-D1 and P2-D2. Call at import.

    Takes the caller's values rather than reading the constants back, so this is
    a check and not a tautology: `src/framings.py` passes the variant string it
    actually renders with and the anchor it actually splices at.
    """
    checks = (("P2-D1 rendering variant", variant, P2D1_VARIANT),
              ("P2-D2 slot anchor", anchor, P2D2_SLOT_ANCHOR),
              ("P2-D1 framing ids", tuple(framing_ids), P2_FRAMING_IDS),
              ("P2-D1 rendering axes (no variant axis)", tuple(axes),
               P2_RENDERING_AXES))
    for label, actual, expected in checks:
        try:
            assert_verbatim(label, actual, expected)
        except AssertionError as e:
            # Paper 1's helper signs off with Paper 1's rule file. Pointing a
            # Paper 2 failure at Paper 1's rules is the wrong-source read this
            # module exists to prevent, so the governing path is restated.
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None


def check_log(path=LOG):
    """The constants above are quoted from the log. Verify they still are.

    Not called at import: it reads a file by relative path, and a binding that
    can fail on the working directory is a binding that gets deleted. The test
    suite calls it.
    """
    text = open(path).read()
    for label, const in (("P2-D1", P2D1_TEXT), ("P2-D2", P2D2_TEXT),
                         ("P2-D3", P2D3_TEXT), ("P2-D4", P2D4_TEXT)):
        quoted = "\n".join("> " + ln for ln in const.split("\n"))
        if quoted not in text:
            raise AssertionError(
                f"D100: {label}'s decision text is not quoted verbatim in {path}.\n"
                f"  in code:\n{quoted}\n"
                "Fix whichever one drifted. The log is the source.")
    for label, rejected in (("P2-D1", P2D1_REJECTED), ("P2-D2", P2D2_REJECTED),
                            ("P2-D3", P2D3_REJECTED), ("P2-D4", P2D4_REJECTED)):
        for alt in rejected:
            if f"**{alt}**" not in text:
                raise AssertionError(
                    f"D100: {label} lists a rejected alternative the log does "
                    f"not head: {alt!r}. An alternative dropped from the log is "
                    "a decision that can no longer be audited.")
    return True


def main():
    check_log()
    print(f"P2-D1 variant   {P2D1_VARIANT!r}")
    print(f"P2-D2 anchor    {P2D2_SLOT_ANCHOR!r}")
    print(f"framing ids     {P2_FRAMING_IDS}")
    print(f"rendering axes  {P2_RENDERING_AXES}")
    print(f"F0 target       {P2_F0_REPLICATION_TARGET}")
    print(f"Arm B tile      {P2D3_TILE!r}, pooled={P2D3_POOLED}, "
          f"n={P2D4_N_CONFIRMATORY}")
    print(f"item file       sha256 {P2D4_ITEMS_SHA256[:16]}...")
    print(f"rejected        {len(P2D1_REJECTED)} on P2-D1, "
          f"{len(P2D2_REJECTED)} on P2-D2, {len(P2D3_REJECTED)} on P2-D3, "
          f"{len(P2D4_REJECTED)} on P2-D4, all present in the log")
    print(f"constants match {os.path.relpath(LOG)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
