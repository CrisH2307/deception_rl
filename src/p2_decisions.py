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
import math
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


# --------------------------------------------- P2-D5, the level confound
P2D5_TEXT = (
    "`o*_infinity` is Paper 1's `o_fit` on 452 of 460 divergent items, so Arm B's target\n"
    "sits on Paper 1's salience pole and the LEVEL of `A` is confounded with salience.\n"
    "The confound is real, permanent, and not repaired by any item set. No change is made\n"
    "to the item set, the coordinate, or the analysis set. Instead: no claim that a model\n"
    "carries adversary-relevant content may rest on `A` under a single framing. Every such\n"
    "claim is made on a framing contrast and on excess over the marginal null, never on\n"
    "raw `A`. A model at `A = 1` under F0 is reporting salience, not adversary awareness,\n"
    "and a point mass at `A = 0` is likewise not evidence of Bayes-optimal behaviour."
)
P2D5_REJECTED = ("Restrict the primary analysis to items with F0 headroom.",
                 "Add a second coordinate not confounded with salience at the level.")

# ------------------------------- P2-D6, the confirmatory statistic for Arm B
P2D6_TEXT = (
    "Arm B's confirmatory instrument is (i) the tie rate, the share of analysis-set items\n"
    "with `ΔA` exactly zero, reported directly as a primary quantity, and (ii) an exact\n"
    "two-sided sign test on the remaining items, on the count with `ΔA > 0` against\n"
    "`p0 = 0.5`, at `alpha = 0.05/21`. Mean `ΔA` is demoted to a reported descriptive\n"
    "quantity. The median of per-item `ΔA` and the value computed from the means are both\n"
    "retained. The `size`-tile analysis set, the 21-test family and `alpha` are unchanged."
)
P2D6_REJECTED = ("Accept the mean, state the mixture as a limitation.",
                 "Restrict to pole-to-pole transitions.",
                 "A bounded transform of `ΔA`.")
P2D6_ALPHA = 0.05 / 21          # unchanged from v2.0 section 8.1
P2D6_P0 = 0.5                   # the sign test's null; needs no SESOI
P2D6_MEAN_IS_CONFIRMATORY = False


def bind_armb_statistic(statistic, alpha, p0, mean_is_confirmatory):
    """Assert an Arm B confirmatory run against P2-D6. Call at import.

    Takes what the caller actually computes. A run that puts its confirmatory
    claim on mean `ΔA`, or that moves `alpha` or the sign test's null, fails here
    rather than in the results table. `sign` and `tie_rate` are the two halves of
    the instrument and either is an admissible primary statistic; nothing else is.
    """
    allowed = ("sign", "tie_rate")
    if statistic not in allowed:
        raise AssertionError(
            f"P2-D6: confirmatory statistic {statistic!r} is not one of {allowed}. "
            "Mean `ΔA` is descriptive under P2-D6 and cannot carry a confirmatory "
            "claim; see docs/P2/DECISIONS.md and PREREGISTRATION_v2.4.md section 2.")
    checks = (("P2-D6 alpha", alpha, P2D6_ALPHA),
              ("P2-D6 sign-test null", p0, P2D6_P0),
              ("P2-D6 mean is confirmatory", bool(mean_is_confirmatory),
               P2D6_MEAN_IS_CONFIRMATORY))
    for label, actual, expected in checks:
        try:
            assert_verbatim(label, str(actual), str(expected))
        except AssertionError as e:
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None


# ------------------------------------- P2-D7, the declined redraw variant (b)
P2D7_TEXT = (
    "Redraw variant (b), enlarging the `size` tile, is declined. `PREREGISTRATION_v2.3.md`\n"
    "section 6 gated it on `sigma` for `ΔA`; `v2.4` section 3.2 removed `sigma` from the\n"
    "confirmatory power curve but moved the gate rather than clearing it, since sizing an\n"
    "enlargement now requires a target tie rate, which is equally unmeasured. There is no\n"
    "new quantity to authorize an enlargement on. Arm B runs on Paper 1's frozen 1,000,\n"
    "`size`-tile analysis set, `n = 108`, with realized power reported rather than assumed."
)
P2D7_REJECTED = ("Authorize an enlargement sized against the `sigma` analogue.",
                 "Leave it open pending a tie-rate estimate.")
# P2-D4 left this open; P2-D7 closes it. Any enlargement would change
# P2D4_ITEMS_SHA256, so `bind_armb` is already where a violation lands.
P2D7_ENLARGEMENT_AUTHORIZED = False

# --------------------------------------- P2-D8, the tie rate's reference
P2D8_TEXT = (
    "The Arm B tie rate is calibrated against Paper 1's condition-4-versus-condition-5\n"
    "same-option rate, which is perturbation-matched to the framing contrast in slot, in\n"
    "kind and in which factor varies. The permutation-to-permutation rate is rejected as\n"
    "the primary reference and retained as a bound, because it varies option order rather\n"
    "than text and sits 0.18 to 0.57 below the `c5` rate on every model. The reference\n"
    "values are tabulated in `PREREGISTRATION_v2.5.md` section 2.2 and T7 uses them rather\n"
    "than recomputing them. The statistic is the framing same-option rate minus the model's\n"
    "`c5` rate, with a cluster bootstrap over items, 10,000 resamples, seed 20260910, at\n"
    "`1 - alpha` with `alpha = 0.05/21`. The tie rate does not enter the 21-test family: it\n"
    "forms a second family of 21 corrected separately, because rejecting H-B requires the\n"
    "conjunction of both halves and a conjunction's error is bounded by the smaller of its\n"
    "parts. A tie rate indistinguishable from the reference does not support H-B; the cell\n"
    "is reported inconclusive and its sign test carries no claim."
)
P2D8_REJECTED = ("Calibrate against the permutation-to-permutation rate.",
                 "Merge the tie rate into the 21-test family, giving 42 tests at `0.05/42`.",
                 "Report the tie rate with an interval and no reference.")
# The tabulated reference, size tile, pmi/template. T7 reads these; it does not
# recompute them, and a recomputation that disagrees fails at `bind_armb_tie`.
P2D8_C5_REFERENCE = {"CTRL": 0.7037037037037037, "B2": 0.8037383177570093,
                     "B4": 0.6296296296296297, "L1": 0.8611111111111112,
                     "L2": 0.8518518518518519, "L3": 0.8101851851851852,
                     "L4": 0.7407407407407407}
P2D8_BOOT_N = 10_000
P2D8_BOOT_SEED = 20260910
P2D8_TIE_IN_MAIN_FAMILY = False


def bind_armb_tie(reference, boot_n, boot_seed, tie_in_main_family):
    """Assert an Arm B tie-rate run against P2-D8. Call at import.

    The reference is tabulated in the preregistration precisely so T7 does not
    recompute it; passing a recomputed table that differs fails here rather than
    silently recalibrating the comparison mid-analysis.
    """
    for model, want in P2D8_C5_REFERENCE.items():
        got = reference.get(model)
        if got is None or abs(float(got) - want) > 5e-4:
            raise AssertionError(
                f"P2-D8: c5 reference for {model} is {got!r}, preregistered "
                f"{want:.4f}. The table in PREREGISTRATION_v2.5.md section 2.2 is "
                "the source; T7 uses it rather than recomputing it.")
    checks = (("P2-D8 bootstrap resamples", boot_n, P2D8_BOOT_N),
              ("P2-D8 bootstrap seed", boot_seed, P2D8_BOOT_SEED),
              ("P2-D8 tie rate in the main family", bool(tie_in_main_family),
               P2D8_TIE_IN_MAIN_FAMILY))
    for label, actual, expected in checks:
        try:
            assert_verbatim(label, str(actual), str(expected))
        except AssertionError as e:
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None



# --------------------------------- P2-D9, the c5 reference's status
P2D9_TEXT = (
    "Paper 1's `c5` insert is an ACTIVE comparator, not a no-manipulation baseline. On the\n"
    "`size`-tile confirmatory set the insert changes the chosen option on 0.1389 to 0.3704\n"
    "of matched rendering pairs, and the cluster bootstrap interval excludes the no-effect\n"
    "rate on all seven models at `alpha = 0.05/21`. The no-effect rate is exactly 1.0\n"
    "because Paper 1's chooser is an argmax over teacher-forced log-probabilities with no\n"
    "sampling anywhere in the scoring path. A framing rate indistinguishable from `R_m`\n"
    "therefore reads as \"the framing moved choices about as much as a known-effective\n"
    "content insertion in the same slot did\", not as \"the framing moved nothing\". That\n"
    "reading is still not support for H-B, because the comparison is blind to direction."
)
P2D9_REJECTED = ("Leave the reference's status unstated and read it in T7.",
                 "Treat `c5` as a baseline on the strength of its small mean effect.",
                 "Recompute the reference under a null perturbation to measure the "
                 "no-effect rate.")
P2D9_C5_IS_ACTIVE = True
# Emitted by `src/c5_effect.py` into `results/T5_c5_effect.json`, size tile.
P2D9_C5_CHANGE_RATE_RANGE = (0.1388888888888889, 0.37037037037037035)
P2D9_NO_EFFECT_SAME_OPTION_RATE = 1.0

# ------------------------- P2-D10, which rate is primary for H-B's no-movement half
P2D10_TEXT = (
    "Arm B's primary no-movement statistic is the SAME-OPTION rate, not the tie rate. The\n"
    "same-option rate is what P2-D8's reference calibrates, and a statistic with no null\n"
    "cannot carry half of a confirmatory conjunction. The tie rate governs the sign test's\n"
    "denominator, because ties are mechanically what the sign test drops, and it is\n"
    "reported beside the same-option rate with its exact interval and its realized power.\n"
    "The gap between them is non-negative, since same option implies `ΔA = 0`, and is\n"
    "reported per cell as the coordinate's blind spot: choice movement between two options\n"
    "that share an `A`. `PREREGISTRATION_v2.4.md` section 2.4's label of the tie rate as\n"
    "primary is superseded, and `v2.5` section 2.3 already ran the comparison on the\n"
    "same-option rate, so this decision makes the two documents agree rather than changing\n"
    "what either computes."
)
P2D10_REJECTED = ("Keep the tie rate primary and calibrate it directly.",
                  "Run both as co-primary and require agreement.",
                  "Report the gap only as an aggregate limitation.")
P2D10_PRIMARY_RATE = "same_option"
P2D10_SIGN_TEST_DENOMINATOR = "non_tie"

# --------------------------- P2-D11, the joint detection statement a null must carry
P2D11_TEXT = (
    "Every reported Arm B null carries both detection limits in one statement. The\n"
    "reference comparison cannot resolve a same-option-rate gap below roughly 0.15, which\n"
    "requires a framing to change choices on 1.45 to 2.13 times as many pairs as `c5` does\n"
    "before the movement half can fire. At that boundary the sign test's effective `n` is\n"
    "at most 32 to 58, so its power reaches 0.80 only at `p1` between 0.746 and 0.822. The\n"
    "two limits compose rather than trade off, because a framing weak enough to sit near\n"
    "the first boundary leaves the second with that effective `n`. `n = 108` against `v2.0`\n"
    "section 8.2's benchmark of 400 is a third shortfall and it does not disappear because\n"
    "P2-D6 changed the statistic. A null licenses only that the framing did not move\n"
    "choices detectably more than `c5` did, at this `n`, on this tile, on this coordinate."
)
P2D11_REJECTED = ("Cross-reference the two sections from the results report.",
                  "Compute the joint ceiling in T7 from the observed tie rate.")
P2D11_N_BENCHMARK = 400
# (min, max) over the seven models, from `results/T5_detection_ceiling.json`.
P2D11_CEILING = {"half_width": (0.1412037037037037, 0.16666666666666669),
                 "change_rate_multiple_of_c5": (1.4500000000000002,
                                                2.133333333333334),
                 "n_eff_max": (32, 58),
                 "p1_at_80_power": (0.746, 0.822)}


def bind_armb_rates(primary_rate, sign_denominator, c5_is_active):
    """Assert an Arm B run against P2-D9 and P2-D10. Call at import.

    Takes what the caller actually used. A script that computes its verdict from
    the tie rate, or that writes the baseline reading of an indistinguishable
    cell, fails here rather than in the results table.
    """
    checks = (("P2-D10 primary no-movement rate", primary_rate, P2D10_PRIMARY_RATE),
              ("P2-D10 sign test denominator", sign_denominator,
               P2D10_SIGN_TEST_DENOMINATOR),
              ("P2-D9 c5 reference is active", bool(c5_is_active),
               P2D9_C5_IS_ACTIVE))
    for label, actual, expected in checks:
        try:
            assert_verbatim(label, str(actual), str(expected))
        except AssertionError as e:
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None



# ------------------------- P2-D12, three quantities, none gating another
P2D12_TEXT = (
    "Arm B reports three quantities and none of them gates another. (a) INERTNESS: the\n"
    "same-option change rate against zero, per model, on the full confirmatory `n`, with\n"
    "P2-D8's cluster bootstrap. Zero is the exact null, because Paper 1's scorer is\n"
    "deterministic (P2-D9), so this establishes whether the framing moved anything at all,\n"
    "which is the question the `c5` reference was introduced for. (b) MAGNITUDE CONTEXT:\n"
    "the same-option rate against `R_m`, with the bootstrap half-width stated. Reported and\n"
    "descriptive; it gates nothing and spends no `alpha`. (c) DIRECTION: the exact\n"
    "two-sided sign test on items with `ΔA != 0` against `p0 = 0.5`, unchanged. H-B's\n"
    "no-movement half resolves on (a) with (b) as context, never on (b). The gate in\n"
    "`PREREGISTRATION_v2.5.md` section 2.3 and `v2.6` section 1.4 is superseded, and with\n"
    "it P2-D11's ceiling."
)
P2D12_REJECTED = ("Keep the `c5` comparison as the gate.",
                  "Gate on inertness and drop the `c5` comparison entirely.",
                  "Adopt `c5`'s own `ΔA` sign proportion as `p0`.")
P2D12_QUANTITIES = ("inertness", "magnitude_context", "direction")
P2D12_C5_GATES = False           # (b) is descriptive; this is the whole decision
P2D12_INERTNESS_NULL = 0.0       # exact, per P2-D9's deterministic scorer
# Emitted by `src/inertness_ceiling.py`. A count of moving items, not a rate: the
# bootstrap's lower bound is zero exactly when a resample can contain no mover.
P2D12_INERTNESS_FLOOR_ITEMS = 7


def bind_armb_quantities(inertness_null, c5_gates, sign_p0, quantities):
    """Assert an Arm B run against P2-D12. Call at import.

    The check that matters is `c5_gates`. A script that resolves H-B's
    no-movement half on the reference comparison rather than on inertness is the
    superseded design, and it must fail here rather than produce a table that
    looks like the current one.
    """
    checks = (("P2-D12 inertness null", float(inertness_null),
               P2D12_INERTNESS_NULL),
              ("P2-D12 c5 comparison gates", bool(c5_gates), P2D12_C5_GATES),
              ("P2-D6 sign-test null, unchanged by P2-D12", float(sign_p0),
               P2D6_P0),
              ("P2-D12 reported quantities", tuple(quantities), P2D12_QUANTITIES))
    for label, actual, expected in checks:
        try:
            assert_verbatim(label, str(actual), str(expected))
        except AssertionError as e:
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None



# ------------------ P2-D13, the inertness floor is numerical, not statistical
P2D13_TEXT = (
    "Quantity (a)'s floor is a numerical noise floor, not a statistical threshold. Under\n"
    "P2-D9 the scorer is deterministic, so under the strict null every item has `ΔA = 0`,\n"
    "every bootstrap resample returns exactly zero, the lower bound never clears, and Type\n"
    "I error is exactly 0 rather than `alpha`. A single changed option establishes\n"
    "deductively that the framing moved something, so P2-D12's derivation of 7 from\n"
    "bootstrap arithmetic guarded no statistical quantity and is withdrawn. The hazard is\n"
    "floating-point nondeterminism flipping a near-tie argmax across runs and hardware.\n"
    "The floor is provisionally 7 items and is revised to T7's `F0`-versus-`cond4`\n"
    "disagreement count if that count exceeds 7. The revision is upward-only by\n"
    "construction, the rule being a maximum, and it is triggered by a measurement\n"
    "`T7.md` step 2 already performs for the environment-equivalence check. P2-D8's\n"
    "bootstrap is retained unchanged in quantity (b), where two estimated population rates\n"
    "are compared in the interior of the parameter space."
)
P2D13_REJECTED = ("Keep the bootstrap floor of 7 on its original derivation.",
                  "Lower the floor to a single changed item.",
                  "Scale the `F0` disagreement count upward to allow for F1's longer "
                  "prompts.")
P2D13_PROVISIONAL_FLOOR = 7           # same value as P2-D12; different justification
P2D13_REVISION_IS_UPWARD_ONLY = True
P2D13_FLOOR_IS_STATISTICAL = False    # the whole content of this decision

# ---------------------- P2-D14, p0 = 0.5 retained, its Type II cost disclosed
P2D14_TEXT = (
    "`p0 = 0.5` is retained and is stated as conservative against Type I and costly in\n"
    "Type II. The word \"chance\" is withdrawn from the licenses box: `PREREGISTRATION_v2.7.md`\n"
    "section 2.1 measures the content-neutral sign proportion at 0.2453 to 0.5000, at or\n"
    "below 0.5 on all seven models and below it at the corrected `alpha` on one, so 0.5 is\n"
    "not the neutral baseline. A null on (c) therefore does NOT distinguish \"no directional\n"
    "effect\" from \"a directional effect that did not clear the gap between 0.5 and the\n"
    "measured content-neutral baseline\". The per-model gap is 0.0000 to 0.2547 and is\n"
    "reported with the verdict, so a reader can size the cost rather than being told it\n"
    "exists."
)
P2D14_REJECTED = ("Recalibrate `p0` to the measured content-neutral baseline.",
                  "Keep the word \"chance\" and note the diagnostic separately.")
# 0.5 minus the measured content-neutral sign proportion, from
# results/T5_armb_floor.json. Reported with every (c) verdict.
P2D14_TYPE_II_GAP = {"CTRL": 0.2547169811320755, "B2": 0.0,
                     "B4": 0.012500000000000011, "L1": 0.09259259259259256,
                     "L2": 0.03125, "L3": 0.24285714285714283,
                     "L4": 0.20909090909090908}

# ------------------- P2-D15, sign(delta-A) is admissible cross-family under D111
P2D15_TEXT = (
    "`sign(ΔA)` is ADMISSIBLE for the cross-family control under Paper 1's D111. D111\n"
    "restricts cross-family comparison to choice-based statistics and bans raw PMI\n"
    "magnitudes, because the control's tokenizer differs by construction and\n"
    "log-probability magnitudes stop being commensurable. The operational test is whether\n"
    "the statistic changes when the tokenizer changes but the chosen options do not.\n"
    "`A(o) = (marg_norm(o) - marg_norm(o*_0)) / ext_i` with `ext_i > 0` a per-item\n"
    "constant, so `sign(ΔA)` is an ordinal comparison of two options on frozen, model-free\n"
    "item geometry, selected by the model's choice and nothing else. It is computed within\n"
    "a model and reported as a rate, which is what D111 permits. The ruling extends to\n"
    "nothing that reads a model's scores rather than its choice: `logp_sum_chosen`,\n"
    "`logp_neutral_chosen` and any PMI value remain inadmissible across families. The\n"
    "conclusion is reported both ways regardless: on the six ladder models alone the\n"
    "neutral sign proportion runs 0.2571 to 0.5000, still at or below 0.5 on every one."
)
P2D15_REJECTED = ("Rule it inadmissible because `A` is a magnitude coordinate.",
                  "Drop the control from the diagnostic without ruling.")
P2D15_SIGN_IS_ADMISSIBLE = True
# Named in the decision text so the ruling cannot be read as relaxing D111.
P2D15_STILL_INADMISSIBLE = ("logp_sum_chosen", "logp_neutral_chosen", "pmi")


# ------------------- P2-D16, a tied rendering is excluded pairwise
P2D16_TEXT = (
    "A rendering whose argmax is tied carries no chosen option, so it carries neither a\n"
    "same-option verdict nor an `A` value, and it is excluded. The exclusion is PAIRWISE and\n"
    "at the level of the rendering pair, the (item, permutation) unit at which a framing\n"
    "contrast is formed: the pair leaves both the numerator and the denominator of every\n"
    "quantity whenever either of its two renderings is tied, and the item's other permutation\n"
    "is retained. A tied rendering is never imputed as a non-mover, and the item is never\n"
    "dropped whole. The rule is symmetric across the arms: it applies whether the tie falls\n"
    "on `F0`, `F1` or `F2`, so a tied `F0` rendering leaves both the `F1` and the `F2`\n"
    "contrast while a tied `F1` rendering leaves only the `F1` contrast. A tied `F0`\n"
    "rendering is also outside the `F0`-versus-`cond4` disagreement count that sets P2-D13's\n"
    "floor, which is already Paper 1's `n_tied == 1` filter on both sides, so it neither\n"
    "raises nor lowers the floor. This is Paper 1's `n_tied == 1` filter applied at the\n"
    "contrast rather than at the rendering, and it is what `src/c5_effect.py` and\n"
    "`src/inertness_ceiling.py` already do to produce P2-D8's reference values. Every cell\n"
    "reports its attrition: rendering pairs excluded for a tie, and items left with one\n"
    "surviving pair or with none."
)
P2D16_REJECTED = ("Count the tie as a non-mover.",
                  "Exclude the whole item.",
                  "Break the tie with a deterministic rule and score the rendering.")
# The unit the exclusion happens at, before any aggregation. Same shape as the
# pivot index in `c5_movement` and `c5_delta_A`, which is the point: the rule is
# what produced P2-D8's reference values, not a new handling for F1 and F2.
P2D16_EXCLUSION_UNIT = ("item_id", "permutation_id")
P2D16_IMPUTE_TIE_AS_NON_MOVER = False   # the whole content of the decision
P2D16_DROPS_WHOLE_ITEM = False
P2D16_ATTRITION_IS_REPORTED = True
# What a cell reports beside its three quantities. A denominator that is not 108
# cannot be recovered from a rate, and P2-D13's floor is an absolute count.
P2D16_ATTRITION_FIELDS = ("pairs_excluded_for_a_tie", "items_with_one_surviving_pair",
                          "items_with_no_surviving_pair", "item_denominator")


def bind_tie_exclusion(unit, imputed_as_non_mover, dropped_whole_item,
                       attrition_fields):
    """Assert an Arm B run's tie handling against P2-D16. Call at import.

    Takes what the caller actually did. The check that matters is
    `imputed_as_non_mover`: a run that counts a tied rendering as "same option"
    adds pairs to quantity (a)'s denominator that cannot reach its numerator, on
    a boundary null where one item is deductive evidence, and it does so in the
    direction that confirms H-B's no-movement half.
    """
    missing = [f for f in P2D16_ATTRITION_FIELDS if f not in tuple(attrition_fields)]
    if missing:
        raise AssertionError(
            f"P2-D16: the cell does not report {missing}. Attrition that is not "
            "reported is attrition a reader cannot size, and the item "
            "denominator is not recoverable from the rate. "
            "docs/P2/DECISIONS.md is the source.")
    checks = (("P2-D16 exclusion unit", tuple(unit), P2D16_EXCLUSION_UNIT),
              ("P2-D16 tie imputed as non-mover", bool(imputed_as_non_mover),
               P2D16_IMPUTE_TIE_AS_NON_MOVER),
              ("P2-D16 whole item dropped", bool(dropped_whole_item),
               P2D16_DROPS_WHOLE_ITEM))
    for label, actual, expected in checks:
        try:
            assert_verbatim(label, str(actual), str(expected))
        except AssertionError as e:
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None


def bind_armb_floor(floor_used, f0_disagreement_items, floor_is_statistical):
    """Assert T7's inertness floor against P2-D13. Call where the floor is set.

    Takes the floor the run actually used and the disagreement count it was
    derived from, so a run that kept the provisional floor against a larger
    measured noise floor fails here rather than reporting a movement verdict the
    environment could have produced on its own.
    """
    if int(f0_disagreement_items) < 0:
        raise AssertionError(
            f"P2-D13: disagreement count cannot be negative, got "
            f"{int(f0_disagreement_items)}. A negative count would pass the "
            "maximum silently, since max(7, -1) is 7.")
    want = max(P2D13_PROVISIONAL_FLOOR, int(f0_disagreement_items))
    if int(floor_used) != want:
        raise AssertionError(
            f"P2-D13: floor = max({P2D13_PROVISIONAL_FLOOR}, "
            f"{int(f0_disagreement_items)}) = {want}; the run used "
            f"{int(floor_used)}. The revision is upward-only and the rule is a "
            "maximum. docs/P2/DECISIONS.md is the source.")
    try:
        assert_verbatim("P2-D13 floor is statistical",
                        str(bool(floor_is_statistical)),
                        str(P2D13_FLOOR_IS_STATISTICAL))
    except AssertionError as e:
        raise AssertionError(
            str(e).replace(".claude/rules/30-data-decisions.md",
                           "docs/P2/DECISIONS.md")) from None


# ------------------- P2-D17, P2-D18: WITHDRAWN, numbers retired
# Two entries written by a parallel session on 2026-09-12 and recorded as author
# rulings with premises the author did not write. Withdrawn; never decisions. The
# numbers are retired rather than reused, because copies of the withdrawn text
# exist outside this repository and a reused number could not be told apart from
# them. Named here so a caller importing `P2D17_*` fails loudly instead of
# finding nothing and moving on.
P2D17_WITHDRAWN = True
P2D18_WITHDRAWN = True
P2D17_TEXT = P2D18_TEXT = None


# ------------------- P2-D19, the A-tie tolerance is Paper 1's EPS
P2D19_TEXT = (
    "Two options count as `A`-tied when `|A(x) - A(y)| <= EPS` with `EPS = 1e-12`, which is\n"
    "Paper 1's `src/tiebreak.py` constant, inherited and not chosen. The tolerance governs\n"
    "every figure reporting what the `A` coordinate can resolve, and the PRIMARY figure is\n"
    "per option pair: on the `size` confirmatory set 84 of 1,620 unordered option pairs are\n"
    "`A`-tied, which is 0.0519, against 101 of 3,024 on the divergence set, 0.0334, a factor\n"
    "of 1.55. Exact float equality gives 50 pairs. The per-item figure, 73 of 108 items or\n"
    "0.6759, counts items containing AT LEAST ONE tied pair and is inflated by option count:\n"
    "a `size` item has six options and therefore fifteen chances to contain one. It is\n"
    "reported beside the per-pair figure, with its base named, and never alone. Arm B's blind\n"
    "spot is narrower than either, because `ΔA = 0` despite a changed option requires the\n"
    "`F0`-chosen and the `F1`-chosen option SPECIFICALLY to be tied, not their item to\n"
    "contain a tied pair among fifteen, so it is bounded near the per-pair rate. Every gap\n"
    "the tolerance absorbs is at or below 2.23e-14 and the smallest gap it does not absorb is\n"
    "1.97e-03, eleven orders larger, so every tolerance strictly inside that interval\n"
    "classifies identically and these are properties of the geometry rather than of the\n"
    "constant. The consequence is stated as a limitation of the coordinate and never as a\n"
    "property of a model. The exact-equality figures stay in\n"
    "`results/T5_tie_reference.json` unchanged, because `v2.5` section 3 and `v2.6` section\n"
    "2.2 cite them and a superseded document must still reproduce."
)
P2D19_REJECTED = ("Keep exact float equality.",
                  "Choose a tolerance fitted to the observed gap.",
                  "Record the finding as a range and let the reader choose.",
                  "Lead with the per-item figure.")
# Not a literal: imported from Paper 1 so a drift in P1's constant fails here.
from tiebreak import EPS as P2D19_EPS                      # noqa: E402,F401
# The confirmatory-set figures, emitted by `tie_reference.a_invisibility`.
# PRIMARY base first: the pair. The item counts are kept because the log quotes
# them, and `bind_a_tie_tolerance` refuses to check one without the other.
P2D19_A_TIED_PAIRS, P2D19_TOTAL_PAIRS = 84, 1620
P2D19_A_TIED_ITEMS = 73
P2D19_EXACT_EQUALITY_PAIRS, P2D19_EXACT_EQUALITY_ITEMS = 50, 48
# (A-tied pairs, unordered pairs) pooled over the divergence set, for the
# comparison the decision text makes. `size` is the worst tile on both bases.
P2D19_DIVERGENCE_PAIRS, P2D19_DIVERGENCE_TOTAL_PAIRS = 101, 3024
# (largest gap the tolerance absorbs, smallest gap above it). The decision stands
# on this interval being empty, not on the value of EPS.
P2D19_GAP = (2.229433e-14, 1.973765183412878e-03)


def bind_a_tie_tolerance(eps, a_tied_items, a_tied_pairs, total_pairs,
                         next_gap_above_eps):
    """Assert an A-resolution figure against P2-D19. Call where the figure is made.

    Takes what the caller actually computed. Three things are checked and they
    fail for different reasons: an `eps` that is not Paper 1's means the tolerance
    was chosen; a `next_gap_above_eps` near `eps` means the tolerance no longer
    sits in a gap, so it has become a threshold whether or not anyone chose it;
    and `total_pairs` is required so the per-pair rate, which is the decision's
    primary figure, cannot be omitted while the inflated per-item count passes.
    """
    if float(eps) != float(P2D19_EPS):
        raise AssertionError(
            f"P2-D19: the A-tie tolerance is Paper 1's tiebreak EPS = {P2D19_EPS:g}, "
            f"inherited and not chosen; the run used {float(eps):g}. "
            "docs/P2/DECISIONS.md is the source.")
    if not float(next_gap_above_eps) > float(eps) * 1e6:
        raise AssertionError(
            f"P2-D19: the smallest gap above eps is {float(next_gap_above_eps):.3g}, "
            f"within six orders of {float(eps):g}. The tolerance sat in an empty "
            f"interval of eleven orders ({P2D19_GAP[0]:.3g} to {P2D19_GAP[1]:.3g}) "
            "when it was adopted; it no longer does, so it is now a chosen "
            "threshold and P2-D19 must be revisited rather than kept.")
    for label, actual, expected in (
            ("P2-D19 A-tied option pairs", int(a_tied_pairs), P2D19_A_TIED_PAIRS),
            ("P2-D19 unordered option pairs", int(total_pairs), P2D19_TOTAL_PAIRS),
            ("P2-D19 items with an A-tied pair", int(a_tied_items),
             P2D19_A_TIED_ITEMS)):
        try:
            assert_verbatim(label, str(actual), str(expected))
        except AssertionError as e:
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None


# ------------------- P2-D20, quantity (c)'s unit is the item
P2D20_TEXT = (
    "Quantity (c)'s unit is the ITEM. This is not a choice between three readings in\n"
    "circulation; it is the unit both governing documents already state, restored. P2-D12's\n"
    "decision text says \"the exact two-sided sign test on items with `ΔA != 0`\" and `v2.0`\n"
    "section 3.2 says `A` is computed per rendering and \"averaged within item across the\n"
    "two\" Format V permutations. An item's value is therefore the mean of its SURVIVING\n"
    "pair `ΔA`s, which equals the difference of its within-item mean `A`s, and the item\n"
    "enters the sign test when `|mean ΔA| > EPS` under P2-D19's tolerance. Three\n"
    "consequences are fixed here because no reading covered them. An item with one\n"
    "surviving pair contributes that pair's sign, per P2-D16: it contributes what it has,\n"
    "and is neither imputed nor dropped. An item whose two pairs DISAGREE in sign\n"
    "contributes the sign of their mean. An item whose two pairs cancel to within `EPS`\n"
    "contributes nothing and is counted as a tie, which is the same event as a pair-level\n"
    "tie and is reported as one. `inertness_ceiling.c5_delta_A`'s pair count and\n"
    "`inertness_ceiling.main`'s `round(108 x (1 - tie_rate))` are both superseded for (c):\n"
    "the first counts the wrong unit, the second applies an item scale to a 216-pair rate\n"
    "and yields neither unit. Both keep emitting unchanged, because `v2.7` sections 2.1 and\n"
    "3.2 publish them and a superseded document must still reproduce."
)
P2D20_REJECTED = (
    "Adopt the rendering pair, and amend P2-D12 and v2.0 section 3.2 to match the code.",
    "Keep `round(108 x (1 - tie_rate))`.",
    "Exclude items whose two permutations disagree in sign.",
    "Break a sign disagreement by permutation 0.")
P2D20_UNIT = "item"
P2D20_SIGN_DISAGREEMENT = "sign of the within-item mean"
P2D20_ONE_PAIR_ITEM_CONTRIBUTES = True     # P2-D16's precedent, not a new rule
P2D20_CANCELLING_ITEM_IS_A_TIE = True
# Recomputed 2026-09-13 from frozen P1 rows by `inertness_ceiling.c5_delta_A`, on
# the c5 contrast, confirmatory set. Not transcribed from v2.7.
P2D20_C5_N_EFF_ITEM = {"CTRL": 41, "B2": 36, "B4": 63, "L1": 27, "L2": 31,
                       "L3": 33, "L4": 43}
# The two superseded readings, recomputed and confirmed to still reproduce what
# v2.7 published. Kept so a caller quoting one of them can be told which it has.
P2D20_C5_N_EFF_PAIR_EXACT = {"CTRL": 53, "B2": 42, "B4": 80, "L1": 27, "L2": 32,
                             "L3": 35, "L4": 55}
P2D20_C5_N_EFF_RESCALED = {"CTRL": 26, "B2": 21, "B4": 40, "L1": 14, "L2": 16,
                           "L3": 17, "L4": 28}
# Items whose two permutations disagree in sign, and the subset that cancel to
# within EPS and so become ties. The case the unit exists to rule on.
P2D20_C5_SIGN_DISAGREEMENT = {"CTRL": 1, "B2": 6, "B4": 5, "L1": 0, "L2": 0,
                              "L3": 1, "L4": 4}
P2D20_C5_SIGN_DISAGREEMENT_CANCELLING = {"CTRL": 1, "B2": 0, "B4": 1, "L1": 0,
                                         "L2": 0, "L3": 0, "L4": 0}


def bind_quantity_c_unit(unit, sign_disagreement_rule, one_pair_item_contributes,
                         cancelling_item_is_a_tie, zero_test_eps):
    """Assert a quantity (c) run's unit against P2-D20. Call where n_eff is formed.

    The check that matters is `unit`. A run that counts rendering pairs reports an
    `n_eff` roughly a third larger than the item unit gives, and one that rescales
    a 216-pair rate to 108 reports one roughly a third smaller; both are wrong in
    a direction a reader cannot see from the number. `zero_test_eps` is checked
    because the unit and the tolerance move `n_eff` separately and a run that
    fixes one and not the other is still not reporting P2-D20's quantity.
    """
    checks = (("P2-D20 unit", str(unit), P2D20_UNIT),
              ("P2-D20 sign disagreement rule", str(sign_disagreement_rule),
               P2D20_SIGN_DISAGREEMENT),
              ("P2-D20 one-pair item contributes",
               str(bool(one_pair_item_contributes)),
               str(P2D20_ONE_PAIR_ITEM_CONTRIBUTES)),
              ("P2-D20 cancelling item is a tie",
               str(bool(cancelling_item_is_a_tie)),
               str(P2D20_CANCELLING_ITEM_IS_A_TIE)))
    for label, actual, expected in checks:
        try:
            assert_verbatim(label, actual, str(expected))
        except AssertionError as e:
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None
    if float(zero_test_eps) != float(P2D19_EPS):
        raise AssertionError(
            f"P2-D20: the item-level zero test uses P2-D19's EPS = {P2D19_EPS:g}; "
            f"the run used {float(zero_test_eps):g}. The unit and the tolerance "
            "move n_eff separately and both have to be right.")


# ------------------- P2-D21, the "all seven" claim is withdrawn; p0 = 0.5 stands
P2D21_TEXT = (
    "The claim that the `c5` neutral sign proportion is \"at or below 0.5 on all seven\n"
    "models\" is WITHDRAWN. At P2-D20's item unit it is 0.1951 to 0.5556, above 0.5 on\n"
    "`B2`, and the six-ladder-model restatement in P2-D15 fails for the same reason,\n"
    "because the exception is a ladder model and not the control. `p0 = 0.5` is\n"
    "RETAINED, and not on the withdrawn claim. It is retained on the structural ground\n"
    "P2-D12 and P2-D14 both stated first and independently of any measurement: moving\n"
    "`p0` recalibrates a preregistered test against a different manipulation, on a\n"
    "coordinate Paper 1 never used. The empirical claim is stated directly and not as a\n"
    "tally: the neutral baseline does not drift toward the salience pole, the per-model\n"
    "proportion runs 0.1951 to 0.5556, only `CTRL` resolves at the corrected `alpha` and\n"
    "it resolves downward, and `B2` sits at the null, since 0.5556 on `n_eff` 36 carries\n"
    "`p = 0.6177` and a 95% exact interval of [0.3810, 0.7206]. Two clauses that reverse\n"
    "on `B2` are withdrawn\n"
    "rather than patched. P2-D14's \"it would make a positive F1 result easier to obtain\"\n"
    "is true on six models and false on `B2`, where recalibration would raise `p0`. And\n"
    "P2-D14's Type II gap, `0.5` minus the proportion, is `-0.0556` on `B2`: a negative\n"
    "gap is not a smaller cost but a different quantity, a Type I exposure the licence\n"
    "box has no sentence for, so a `B2` (c) result significant against `p0 = 0.5` but at\n"
    "or below 0.5556 is reported with that exposure named. `v2.7` section 5 preregistered\n"
    "\"a proportion above 0.5 would have been a reason to keep a direction-matched\n"
    "reference and to reconsider `p0`\"; the antecedent has fired on one model and is\n"
    "discharged here by reconsidering and retaining, not by reading the antecedent away.\n"
    "Every figure at the pair unit keeps emitting unchanged, because `v2.7` section 2.1\n"
    "and `v2.8` section 2.2 publish it and a superseded document must still reproduce."
)
P2D21_REJECTED = (
    "Move `p0` to the measured content-neutral baseline, per model.",
    "Patch the wording to \"six of seven\" and leave the mechanism unexamined.",
    "Move `p0` on `B2` alone, where the baseline sits above it.",
    "Withdraw the diagnostic, on the ground that it no longer says one thing.")
# p0 does NOT move. The whole content of this decision on that question.
P2D21_P0 = 0.5
P2D21_P0_MOVED = False
# The two universally quantified sentences this decision withdraws. Both are
# FALSE at P2-D20's item unit and both are recorded as False rather than deleted,
# so a caller that re-asserts either fails here.
P2D21_ALL_SEVEN_CLAIM_HOLDS = False
P2D21_SIX_LADDER_CLAIM_HOLDS = False
# The models whose item-unit neutral baseline sits ABOVE p0. On these the Type II
# gap is negative and the exposure is Type I, which P2-D14's licence box has no
# sentence for.
P2D21_NEUTRAL_ABOVE_P0 = ("B2",)
# Recomputed 2026-09-13 by `inertness_ceiling._item_reading` on the c5 contrast,
# size confirmatory set, at P2-D20's item unit. Not transcribed from v2.7 or v2.8,
# both of which publish the PAIR unit.
P2D21_C5_SIGN_PROPORTION_ITEM = {
    "CTRL": 0.1951219512195122, "B2": 0.5555555555555556,
    "B4": 0.4603174603174603, "L1": 0.4074074074074074,
    "L2": 0.4838709677419355, "L3": 0.24242424242424243,
    "L4": 0.3023255813953488}
# 0.5 minus the above. SIGNED: negative on B2. P2D14_TYPE_II_GAP is the pair-unit
# reading and is kept unchanged beside this, because v2.8 section 2.2 publishes it.
P2D21_TYPE_II_GAP_ITEM = {
    "CTRL": 0.3048780487804878, "B2": -0.05555555555555558,
    "B4": 0.039682539682539675, "L1": 0.09259259259259256,
    "L2": 0.016129032258064502, "L3": 0.25757575757575757,
    "L4": 0.19767441860465118}
# Only CTRL departs from 0.5 at the corrected alpha, and it departs DOWNWARD.
# True at the pair unit and still true at the item unit, which is why the
# conclusion survives the wording that does not.
P2D21_SIGNIFICANT_AT_CORRECTED_ALPHA = ("CTRL",)


def bind_neutral_baseline(p0, all_seven_holds, six_ladder_holds, above_p0,
                          gap_item):
    """Assert a run's neutral-baseline claims against P2-D21. Call where cited.

    The check that matters is `all_seven_holds`. The sentence "at or below 0.5 on
    all seven models" is what P2-D12 and P2-D14 rested on and it is false at
    P2-D20's unit, so a run that re-asserts it is citing a withdrawn claim and
    must fail here rather than reproduce it. `six_ladder_holds` is checked
    separately because P2-D15's fallback restatement fails for a different
    reason: the exception is a ladder model, not the control, so the fallback
    breaks where the admissibility ruling it exists to make optional does not.
    `gap_item` is checked for SIGN, because P2-D14 describes the gap as a cost
    and a negative one is a Type I exposure instead.
    """
    checks = (("P2-D21 p0, unmoved", float(p0), P2D21_P0),
              ("P2-D21 \"at or below 0.5 on all seven models\"",
               bool(all_seven_holds), P2D21_ALL_SEVEN_CLAIM_HOLDS),
              ("P2-D21 P2-D15's six-ladder restatement",
               bool(six_ladder_holds), P2D21_SIX_LADDER_CLAIM_HOLDS),
              ("P2-D21 models with a baseline above p0",
               tuple(above_p0), P2D21_NEUTRAL_ABOVE_P0))
    for label, actual, expected in checks:
        try:
            assert_verbatim(label, str(actual), str(expected))
        except AssertionError as e:
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None
    for m, want in P2D21_TYPE_II_GAP_ITEM.items():
        got = float(gap_item[m])
        if abs(got - want) > 1e-12:
            raise AssertionError(
                f"P2-D21 states an item-unit Type II gap of {want} for {m}; this "
                f"run gives {got}. docs/P2/DECISIONS.md is the source.")
        if (got < 0) != (m in P2D21_NEUTRAL_ABOVE_P0):
            raise AssertionError(
                f"P2-D21: {m}'s item-unit gap has sign {got:+.4f}, which "
                f"disagrees with the recorded set of models whose baseline sits "
                f"above p0, {P2D21_NEUTRAL_ABOVE_P0}. A negative gap is a Type I "
                "exposure and not a Type II cost, so the set has to be right.")


# ------------------- P2-D22, how the neutral-baseline claim is stated, and where B2 sits
P2D22_TEXT = (
    "The neutral-baseline claim is stated directly and never as a tally. \"At or below 0.5\n"
    "on six of seven models\" is NOT the replacement for the withdrawn \"all seven\": it keeps\n"
    "universality as the frame and leaves a reader an exception they cannot resolve. The\n"
    "claim is: the content-neutral baseline does not drift toward the salience pole. It is\n"
    "stated with the per-model distribution, 0.1951 to 0.5556 at P2-D20's item unit, with\n"
    "the fact that only `CTRL` resolves at the corrected `alpha` and resolves downward, and\n"
    "with `B2` at the null. `B2` IS AT THE NULL, and that is a measured claim rather than a\n"
    "concession: across five aggregations of the same frozen rows its point estimate is\n"
    "exactly 0.5000 under three and 0.5556 under two, `p` is 1.0000 under three and 0.6177\n"
    "under two, every 95% exact interval contains 0.5, two votes of 36 return the item-unit\n"
    "estimate to 0.5000, and `B2` is the only model whose point estimate changes side\n"
    "between the pair unit and the item unit. It is therefore described as a model sitting\n"
    "at the null whose point estimate falls either side depending on aggregation, and never\n"
    "as a model that drifts upward. Separately, \"conservative\" is WITHDRAWN as a\n"
    "justification for `p0 = 0.5` everywhere it is offered as one, because\n"
    "conservativeness is a per-model property and the design is not conservative on `B2` at\n"
    "the point estimate. `p0 = 0.5` stands on the structural ground, on the ordering\n"
    "hazard, and on a single fixed null being the point of having one. Superseded\n"
    "documents keep their wording and their emitted strings unchanged, because `v2.7`,\n"
    "`v2.8` and the artifact fields they publish must still reproduce; this governs live\n"
    "prose, live briefs and every figure emitted at P2-D20's unit."
)
P2D22_REJECTED = (
    "Restate the claim as \"at or below 0.5 on six of seven models\".",
    "Keep \"conservative\" for the six models whose gap is positive and qualify it.",
    "Describe `B2` as a small upward departure that does not reach significance.",
    "Edit the superseded documents so one sentence holds everywhere.")
P2D22_TALLY_FRAME_PERMITTED = False
P2D22_CONSERVATIVE_JUSTIFIES_P0 = False
# B2's position, measured across five aggregations named before they were computed.
# A pair/exact (v2.7 2.1), B pair/EPS, C item/mean/EPS (P2-D20, adopted),
# D item/mean/exact, E item/majority-of-pair-signs. E and the others are NOT
# candidate units: P2-D20 fixed the unit and this is a robustness probe on where
# B2 sits, not a reopening of it.
P2D22_B2_AGGREGATIONS = {"A": (21, 42), "B": (21, 42), "C": (20, 36),
                         "D": (20, 36), "E": (15, 30)}
P2D22_B2_EXACTLY_HALF_UNDER = ("A", "B", "E")
P2D22_B2_ABOVE_HALF_UNDER = ("C", "D")
P2D22_B2_AT_THE_NULL = True
# The only model whose point estimate changes side between the pair and item units.
P2D22_CHANGES_SIDE_BETWEEN_UNITS = ("B2",)


def bind_neutral_claim_wording(tally_frame_used, conservative_justifies_p0,
                               b2_described_as_drifting):
    """Assert how a live statement of the neutral-baseline claim is framed. P2-D22.

    Three separate failures. A tally frame keeps universality and hands the reader
    an unresolved exception. "Conservative" as p0's justification asserts a
    per-model property of the design that does not hold on B2. And describing B2
    as an upward departure reports a direction the data does not carry: its point
    estimate is exactly 0.5000 under three of five aggregations of the same rows.
    """
    checks = (("P2-D22 tally frame used", bool(tally_frame_used),
               P2D22_TALLY_FRAME_PERMITTED),
              ("P2-D22 conservative justifies p0",
               bool(conservative_justifies_p0), P2D22_CONSERVATIVE_JUSTIFIES_P0),
              ("P2-D22 B2 described as drifting",
               bool(b2_described_as_drifting), False))
    for label, actual, expected in checks:
        try:
            assert_verbatim(label, str(actual), str(expected))
        except AssertionError as e:
            raise AssertionError(
                str(e).replace(".claude/rules/30-data-decisions.md",
                               "docs/P2/DECISIONS.md")) from None
    half = tuple(k for k, (p, n) in P2D22_B2_AGGREGATIONS.items() if p * 2 == n)
    if half != P2D22_B2_EXACTLY_HALF_UNDER:
        raise AssertionError(
            f"P2-D22: B2 is exactly 0.5 under {half}, and the decision records "
            f"{P2D22_B2_EXACTLY_HALF_UNDER}. The at-the-null reading rests on that "
            "set, so it is not a presentational detail.")


# ------------------- P2-D23, the ext_i floor does not reach the confirmatory set
P2D23_TEXT = (
    "The `ext_i >= 0.02` floor is RETAINED and does NOT apply to Arm B's confirmatory\n"
    "set. The confirmatory `n` stays 108. The floor is Paper 1's, carried into `v2.0`\n"
    "section 3.2 as the guard on a MEAN OF PER-ITEM RATIOS: Paper 1's governing source is\n"
    "the comment beside `span > 0.02` in `src/frontier_position.py`, which scopes the\n"
    "pathology to exactly that form, and `v2.0` section 3.2 imports it in exactly those\n"
    "words. `v2.0` section 7.2 then wrote the exclusion against \"the confirmatory Arm B\n"
    "analysis\", which at `v2.0` WAS the mean and median of per-item `A`. P2-D6 replaced\n"
    "the mean with a sign test and P2-D12 fixed the three quantities, and none of the\n"
    "three has the ratio form the floor guards. (a) and (b) read chosen options only and\n"
    "never touch `A` or `ext_i`. (c) is a sign test, and `ext_i` is a strictly positive\n"
    "PER-ITEM constant, so both renderings of an item share it and\n"
    "`sign(mean ΔA) = sign(sum of raw margin differences)`, which no denominator can\n"
    "change. The floor therefore removes no item from the confirmatory set. It REMAINS IN\n"
    "FORCE, unamended, on every quantity that is a mean or median of per-item `A`, on\n"
    "`v2.0` section 4.3's `ΔA`-against-`ext_i` correlation, and on the `ΔA` null `v2.x`\n"
    "reported before P2-D6; all of those are reported rather than confirmatory. The floor\n"
    "is not withdrawn and its value is not changed: what is ruled is its reach."
)
P2D23_REJECTED = (
    "Apply the floor to the confirmatory set as `v2.0` section 7.2 reads literally.",
    "Withdraw the floor, since no confirmatory quantity needs it.",
    "Lower the floor to a value the confirmatory set clears.")
P2D23_FLOOR = 0.02
P2D23_APPLIES_TO_CONFIRMATORY = False
P2D23_CONFIRMATORY_N = 108
# Paper 1's governing source. Not a separate entry in P1's decision log; the
# comment beside this expression is the record, and it scopes the pathology to a
# mean of per-item ratios. Asserted present so a change to P1 fails here.
P2D23_P1_SOURCE = "src/frontier_position.py"
P2D23_P1_EXPRESSION = "span > 0.02"
# Recomputed 2026-09-13 on the size confirmatory set. The instruction carried
# 0.00134 and 0.02; both were treated as unverified and both reproduce.
P2D23_MIN_EXT_CONFIRMATORY = 0.001340028643
P2D23_MAX_EXT_CONFIRMATORY = 0.5123189453
# The quantities the floor DOES govern. None is confirmatory after P2-D6.
P2D23_GOVERNS = ("mean of per-item A", "median of per-item A",
                 "v2.0 section 4.3's per-item dA against ext_i correlation",
                 "the dA null reported before P2-D6")


def bind_ext_floor(min_ext_confirmatory, n_confirmatory, quantities_reading_ext):
    """Assert an Arm B run's ext_i handling against P2-D23. Call where (c) is formed.

    The check that matters is `min_ext_confirmatory > 0`, and it is checked for a
    reason rather than as a range. P2-D23's whole argument is that
    `sign(mean ΔA) = sign(sum of raw margin differences)` because `ext_i` is a
    strictly positive per-item constant shared by both of an item's renderings. At
    `ext_i = 0` that identity does not hold, the sign is undefined rather than
    large, and the floor would reach the confirmatory set after all. A small
    `ext_i` is not the hazard; a zero or negative one is.

    `quantities_reading_ext` is the run's list of confirmatory quantities that read
    `ext_i`. It must be empty. A run that adds an `A`-magnitude quantity to the
    confirmatory family has changed what the floor reaches, and this is where that
    surfaces instead of in the reported `n`.
    """
    if not float(min_ext_confirmatory) > 0.0:
        raise AssertionError(
            f"P2-D23: min ext_i on the confirmatory set is "
            f"{float(min_ext_confirmatory)!r}, not strictly positive. The ruling "
            "rests on sign(mean dA) = sign(sum of raw margin differences), which "
            "needs a strictly positive per-item denominator. At zero the sign is "
            "undefined and the floor reaches the confirmatory set. "
            "docs/P2/DECISIONS.md is the source.")
    if tuple(quantities_reading_ext):
        raise AssertionError(
            f"P2-D23: confirmatory quantities reading ext_i: "
            f"{tuple(quantities_reading_ext)}. P2-D23 rules the floor out of the "
            "confirmatory set because none of (a), (b), (c) has the ratio form. A "
            "confirmatory quantity that reads ext_i reopens that ruling.")
    try:
        assert_verbatim("P2-D23 confirmatory n", str(int(n_confirmatory)),
                        str(P2D23_CONFIRMATORY_N))
    except AssertionError as e:
        raise AssertionError(
            str(e).replace(".claude/rules/30-data-decisions.md",
                           "docs/P2/DECISIONS.md")) from None


def check_p1_ext_floor_source(p1_root=None):
    """Chain of custody: P1's floor is a literal in a comment-scoped expression.

    P1's decision log has no entry for it, so the expression IS the record. If P1
    ever changes it, P2-D23's premise moves and this is where that is caught.
    """
    import os as _os
    root = p1_root or _os.environ.get(
        "P1_ROOT", "/Users/crishuynh/Documents/SoftwareProject/deception")
    path = _os.path.join(root, P2D23_P1_SOURCE)
    if not _os.path.exists(path):
        raise AssertionError(f"P2-D23: {path} missing; P1's floor cannot be verified.")
    if P2D23_P1_EXPRESSION not in open(path).read():
        raise AssertionError(
            f"P2-D23: {P2D23_P1_EXPRESSION!r} is no longer in {P2D23_P1_SOURCE}. "
            f"P2-D23 records the floor as {P2D23_FLOOR} carried from there, and "
            "P1's decision log has no separate entry for it, so that expression is "
            "the governing record. It moved.")
    return True


# ------------------- P2-D24, the five downward departures license no direction claim
P2D24_TEXT = (
    "The five downward departures license NO claim about direction. Quantity (c) is\n"
    "reported as computed, nothing is withheld, and the five cells that resolve at the\n"
    "corrected `alpha` are reported as what they are: a sign proportion below `p0 = 0.5`\n"
    "on `CTRL`/F1, `L3`/F1, `L4`/F1, `L3`/F2 and `L4`/F2. No sentence reads that as\n"
    "movement away from `o*_infinity`, as evidence about adversary tracking, or as a\n"
    "property of a model. A direction claim needs three premises and none holds. First,\n"
    "P2-D5's second conjunct names a quantity the confirmatory family does not contain:\n"
    "`A_null(m, F) = sum_o p_{m,F}(o) A_i(o)` is `v2.0` section 3.3's object, and neither\n"
    "a same-option rate nor `p0 = 0.5` is that object. Second, a content-neutral insert\n"
    "departs downward too, on the one model whose own diagnostic resolves at the corrected\n"
    "`alpha`, which is `CTRL` and only `CTRL`, so downward departure is not established as\n"
    "a property of adversary content rather than of inserted text. Third, on three of the\n"
    "five resolving cells the coordinate discards the switches it cannot see at 1.81 to\n"
    "4.09 times P2-D19's per-pair bound, and nothing establishes that the discarded\n"
    "switches carry the direction of the retained ones. The ruling does not depend on how\n"
    "P2-D5's blocker is later ruled: under all three readings in circulation the second\n"
    "and third premises still fail, so the blocker stays open and stays the author's. What\n"
    "IS licensed is movement. Quantity (a) reads chosen options only, carries no claim\n"
    "about adversary-relevant content, and clears P2-D13's floor of 7 on all 14 cells at\n"
    "30 to 77 items of 108 against an exact null of zero. Quantity (b) resolves on three\n"
    "cells, all in the direction of the framing moving choices more than `c5` does, and on\n"
    "eleven it does not. Both are reported per cell, never as one magnitude word."
)
P2D24_REJECTED = (
    "H-B's null half is refuted by (a), and the paper reports movement without direction.",
    "Read the five departures against the measured neutral baseline, and state the "
    "concentration as a limitation on the affected cells.",
    "Withhold quantity (c)'s numbers until P2-D5's blocker is ruled.")
P2D24_DIRECTION_CLAIM_LICENSED = False
P2D24_MOVEMENT_CLAIM_LICENSED = True
# The five (c) cells resolving at the corrected alpha, all below p0. Recomputed
# 2026-09-14 from results/T7_armb_quantities.json, not transcribed.
P2D24_RESOLVING_CELLS = ("CTRL|F1", "L3|F1", "L4|F1", "L3|F2", "L4|F2")
P2D24_RESOLVING_ALL_DOWNWARD = True
# Premise 2. The c5 neutral diagnostic at P2-D20's item unit resolves at the
# corrected alpha on CTRL alone (P2-D21's adopted text says so; the instruction
# that prompted this ruling named L3 as well and L3's p is 0.004551, above alpha).
P2D24_NEUTRAL_RESOLVES_ON = ("CTRL",)
# Premise 3. Resolving cells whose switches concentrate on A-tied option pairs.
P2D24_CONCENTRATED_RESOLVING_CELLS = ("CTRL|F1", "L3|F1", "L3|F2")
P2D24_CONCENTRATION_RATIO_RESOLVING = (1.81, 4.09)
# Premise 1. v2.0 section 3.3's A_null and section 4.4's dA_null are preregistered.
# Using either to license a direction claim on (c) would be post-hoc, because no
# rule maps a level excess onto a sign proportion. That is premise 1's substance
# and it is untouched.
# FACTUAL CORRECTION, 2026-09-15, not a ruling. This said "have never been
# computed", true when P2-D24 was written and false once `src/t7_control.py`
# computed both under P2-D25. Computing them was preregistered work, exactly as
# P2-D24 said it would be, so the fact changing is the entry working rather than
# failing. Nothing about what they may LICENSE moves with it.
P2D24_MARGINAL_NULL_COMPUTED = True
P2D24_MARGINAL_NULL_COMPUTED_BY = "src/t7_control.py, under P2-D25"
P2D24_MARGINAL_NULL_SPEC = ("v2.0 section 3.3 (A_null), v2.0 section 4.4 (dA_null)")


def bind_direction_claim(direction_claim_made, neutral_resolves_on,
                         excess_over_marginal_null_quantities,
                         discarded_switch_direction_established):
    """Assert the premises a direction claim on quantity (c) would need. P2-D24.

    Per the binding-form note in `docs/P2/DECISIONS.md`: this asserts the premises
    that would make a direction claim well formed, not a range any proportion,
    `p` value or concentration ratio happens to occupy. Every one of those numbers
    may move on a re-run without touching the ruling; what the ruling rests on is
    that three specific things are NOT established, and each assert fires when one
    of them becomes established rather than when a value drifts.

    `neutral_resolves_on` is the set of models whose `c5` item-unit sign diagnostic
    resolves at the corrected `alpha`. Reading an F1 or F2 proportion against a
    neutral figure needs a neutral figure that resolves, and it resolves on `CTRL`
    alone, on none of the four `L3` or `L4` resolving cells. If a later run resolves
    it on a second model, the second premise has moved and P2-D24 is re-read rather
    than assumed.

    `excess_over_marginal_null_quantities` is the run's list of confirmatory
    quantities that are an excess over the marginal null. It must be empty. P2-D5's
    second conjunct names exactly that quantity and P2-D12's three do not contain
    one; a run that adds one has changed what the conjunct reaches, which is the
    first premise moving.

    `discarded_switch_direction_established` says whether the run establishes the
    direction of the switches the `A` coordinate discards. It must be false. The
    premise a direction claim needs on a cell whose coordinate discards switches is
    that the discarded ones carry the direction of the retained ones; that is
    selection rather than measurement error, and nothing in the design establishes
    it.
    """
    if bool(direction_claim_made) != P2D24_DIRECTION_CLAIM_LICENSED:
        raise AssertionError(
            "P2-D24: this caller reports a direction claim on quantity (c). None is "
            "licensed: the three premises such a claim needs are asserted below and "
            "none holds. The numbers are not blocked, the reading is. "
            "docs/P2/DECISIONS.md is the source.")
    if tuple(excess_over_marginal_null_quantities):
        raise AssertionError(
            f"P2-D24 premise 1: confirmatory quantities that are an excess over the "
            f"marginal null: {tuple(excess_over_marginal_null_quantities)}. P2-D24 "
            "rules no direction claim partly because P2-D12's three quantities "
            f"contain none, and {P2D24_MARGINAL_NULL_SPEC} specify the object they "
            "would have to be. A run that adds one has moved the premise, and the "
            "ruling is re-read rather than inherited.")
    if tuple(neutral_resolves_on) != P2D24_NEUTRAL_RESOLVES_ON:
        raise AssertionError(
            f"P2-D24 premise 2: the c5 neutral diagnostic resolves on "
            f"{tuple(neutral_resolves_on)}, and P2-D24 rests on it resolving on "
            f"{P2D24_NEUTRAL_RESOLVES_ON}. Reading an F1 or F2 proportion against a "
            "neutral figure needs a neutral figure that resolves; on one model of "
            "seven it does not reach four of the five resolving cells. If that has "
            "changed, the reading P2-D24 rejected may now be available and the "
            "ruling is re-read, not patched.")
    if discarded_switch_direction_established:
        raise AssertionError(
            "P2-D24 premise 3: this run claims the direction of the switches the A "
            "coordinate discards is established. P2-D24 rests on it not being: on "
            f"{P2D24_CONCENTRATED_RESOLVING_CELLS} the discard runs "
            f"{P2D24_CONCENTRATION_RATIO_RESOLVING[0]} to "
            f"{P2D24_CONCENTRATION_RATIO_RESOLVING[1]} times P2-D19's per-pair "
            "bound, which is selection and not measurement error. If the direction "
            "is now established, say by what, and re-read the ruling.")


# ------------------- P2-D25, what the two marginal-null quantities may be used for
P2D25_TEXT = (
    "`A_null(m, F)` and `ΔA_null(m, F)` are computed as `v2.0` sections 3.3 and 4.4\n"
    "specify them, and they are DESCRIPTIVE. Neither enters the confirmatory family,\n"
    "which stays at 21 tests at `alpha = 0.05/21`. Neither was ever a test: `A_null` is\n"
    "a reference point in section 3.3's table and `ΔA_null` is a conjunct on section 4's\n"
    "criterion, and section 10 lists neither. For `ΔA_null` this restates rather than\n"
    "extends P2-D23, which already placed the `ΔA` null among the reported quantities and\n"
    "left the `ext_i >= 0.02` floor in force on it; `A_null` has the same ratio form and\n"
    "inherits the same floor, on its mean and on its median, under `v2.0` section 3.2's\n"
    "two aggregates. NO mapping from either onto quantity (c) is authorized and none may\n"
    "be written: (c) is a sign proportion, both are levels in `A` units, no preregistered\n"
    "rule connects them, and a rule written now would be written with all fourteen of\n"
    "(c)'s cells already published, so writing it blind to `A_null` would not make it\n"
    "blind. NO successor to section 4.4's cap is authorized, and the cap needs none. It\n"
    "caps mean `ΔA`, which P2-D6 demoted rather than deleted, so it follows its quantity\n"
    "down to descriptive and is applied unchanged to the quantity it was written for.\n"
    "P2-D6's mixture finding reaches both sides of that comparison, since `ΔA_null` is\n"
    "built from `mean_i A_i(o)`, and the cap is reported with that defect named. Arm B's\n"
    "confirmatory family therefore carries no defence against the generic-shift\n"
    "hypothesis and cannot acquire one. That is the finding and it is stated as one.\n"
    "`TV(m, F)` on the `beta_c = infinity` control set IS authorized and is descriptive,\n"
    "on section 4.4's first paragraph, whose ground is that any change in the choice\n"
    "distribution on adversary-robust items is prompt sensitivity. That ground is\n"
    "independent of the cap, of mean `ΔA` and of `A`, so P2-D6 and P2-D12 do not reach it\n"
    "and it survives them intact and unamended. The control base is the `size` tile's 142\n"
    "adversary-robust items, which is the base P2-D4 names and the only one whose option\n"
    "arity matches the set the cap reweights; the 540-item figure across all four tiles is\n"
    "reported beside it with its base named, never alone. Both quantities are marginals\n"
    "over CANONICAL option ids, so neither can adjudicate a menu-POSITION hypothesis, and\n"
    "the (4,5) signature is not evidence for one: `chosen_option` is a canonical id, Paper\n"
    "1's Format V permutes the menu per item and per permutation, and canonical options 4\n"
    "and 5 fall in all six menu positions at near-uniform rates under both permutations.\n"
    "The hypothesis these quantities bear on is a shift in preference over canonical option\n"
    "CONTENT at the ends of the tile's ordinal scale, and they bear on it descriptively, at\n"
    "the level, never at the sign. The ruling holds whichever way P2-D5's blocker is later\n"
    "ruled, because nothing it authorizes is an excess quantity in the confirmatory family\n"
    "and nothing it authorizes reaches quantity (c)."
)
P2D25_REJECTED = (
    "Admit `A_null` and `ΔA_null` to the confirmatory family.",
    "Write a successor cap mapping the control-set reweighting onto quantity (c)'s sign "
    "proportion.",
    "Leave the cap orphaned and compute neither quantity.",
    "Compute a marginal over rendered menu positions, so the (4,5) signature can be "
    "tested against a position-shaped cap.")
# Question 1. Neither was ever a test: A_null is one of v2.0 section 3.3's four
# REFERENCES and dA_null is the second conjunct of section 4's criterion, which is
# a condition on a test and spends no alpha. The family is unchanged.
P2D25_IN_CONFIRMATORY_FAMILY = False
P2D25_CONFIRMATORY_FAMILY_SIZE = 21
# Question 2. None. A level in A units and a sign proportion, with no preregistered
# rule between them, and every cell of (c) already published.
P2D25_MAPPING_TO_QUANTITY_C = None
# Question 4. None. The cap's object, mean dA, still exists at descriptive standing
# under P2-D6, so the cap applies to it unchanged and no successor is needed.
P2D25_SUCCESSOR_CAP_AUTHORIZED = False
P2D25_CAP_APPLIES_TO = "mean dA, descriptive under P2-D6"
# v2.0 section 4.4's first paragraph, which is not the cap and did not expire with
# it: any change in the choice distribution on beta_c = infinity items is prompt
# sensitivity. Nothing in P2-D6 or P2-D12 reaches it.
P2D25_CONTROL_TV_AUTHORIZED = True
P2D25_CONTROL_TILE = "size"
P2D25_CONTROL_N = 142              # P2-D4's consequences: the size tile's robust items
P2D25_CONTROL_N_ALL_TILES = 540    # T7.md's SCOPE sentence; a different base, reported beside
P2D25_CONFIRMATORY_ARITY = 6       # |O| on the size tile; the reweighting's shared support
# Question 3. Both marginals are over canonical option ids (v2.0 section 3.3 in
# those words). A canonical id is not a menu position: P1's Format V permutes the
# menu per item and per permutation_id, and on the size tile canonical options 4
# and 5 fall in all six menu positions at near-uniform rates under both. So the
# (4,5) signature is not evidence for a menu-position shift, and no preregistered
# quantity is a marginal over rendered positions.
P2D25_MARGINAL_SUPPORT = "canonical_option_id"
P2D25_MENU_POSITION_ADJUDICABLE = False
P2D25_CANONICAL_TAIL_IDS = (4, 5)
# P2-D23 leaves the ext_i floor in force on every mean or median of per-item A and
# on "the dA null reported before P2-D6". Both quantities here have that form.
P2D25_EXT_FLOOR_IN_FORCE = True


def bind_marginal_null_use(in_confirmatory_family, confirmatory_family_size, alpha,
                           mapping_to_quantity_c, successor_cap,
                           control_arity, confirmatory_arity,
                           hypothesis_support, ext_floor_applied):
    """Assert the premises that make a use of A_null or dA_null well formed. P2-D25.

    Per the binding-form note in `docs/P2/DECISIONS.md`: every premise below is a
    thing that must be TRUE for a use to mean anything, not a range a value
    occupies. No value of A_null, dA_null or TV appears here, and none can make
    this pass or fail. That is deliberate: the ruling was made before any of them
    existed, and it must not become re-readable only once they do.

    `in_confirmatory_family`, `confirmatory_family_size` and `alpha`: neither
    quantity is a test. `A_null` is one of `v2.0` section 3.3's four references and
    `dA_null` is the second conjunct of section 4's criterion; section 8.1's family
    is seven models by three contrasts and section 10 lists neither. Admitting one
    moves `alpha` for 21 tests that are already published at 0.05/21.

    `mapping_to_quantity_c`: must be None. (c) is a sign proportion against
    `p0 = 0.5`; both quantities are levels in `A` units. No preregistered rule
    connects them, and a rule written now is written with all fourteen of (c)'s
    cells published, so a session blind to `A_null` is still not blind.

    `successor_cap`: must be None. The cap's object still exists. P2-D6 demoted
    mean `dA` and did not delete it, so section 4.4's cap applies to it unchanged
    at descriptive standing. A successor would be a new quantity, chosen now.

    `control_arity` and `confirmatory_arity`: the premise that makes the
    reweighting a well formed sum. `dA_null` sums `p^ctrl(o) * mean_i A_i(o)` over
    one option index, so the control marginal and the confirmatory `A` values must
    live on the same option-id support. P2-D3 rejected pooling for the adjacent
    reason: a marginal over canonical option ids does not pool across
    `|O| in {3, 3, 4, 6}`.

    `hypothesis_support`: must be `canonical_option_id`. A marginal over canonical
    ids cannot express a preference over menu POSITIONS, because P1's Format V
    permutes the menu per item and per permutation. A caller that names the cap as
    adjudicating a position hypothesis has mistaken which index the cap runs on.

    `ext_floor_applied`: P2-D23 leaves the `ext_i >= 0.02` floor in force on every
    mean or median of per-item `A` and on the `dA` null. Both quantities have that
    ratio form, so a run that reports them without the floor is reporting a
    quantity P2-D23 governs while skipping the guard P2-D23 kept.
    """
    if bool(in_confirmatory_family) != P2D25_IN_CONFIRMATORY_FAMILY:
        raise AssertionError(
            "P2-D25: this caller puts A_null or dA_null in the confirmatory family. "
            "Neither was ever a test: v2.0 section 3.3 lists A_null among four "
            "REFERENCES and section 4.4 states dA_null as a CONJUNCT on section 4's "
            "criterion, which spends no alpha, and section 10 lists neither. "
            "docs/P2/DECISIONS.md is the source.")
    if int(confirmatory_family_size) != P2D25_CONFIRMATORY_FAMILY_SIZE:
        raise AssertionError(
            f"P2-D25: the confirmatory family is {int(confirmatory_family_size)} "
            f"tests and P2-D25 rests on it staying "
            f"{P2D25_CONFIRMATORY_FAMILY_SIZE}. Admitting a marginal-null quantity "
            "moves alpha for tests whose cells are already published, which is the "
            "ordering hazard P2-D12, P2-D21 and P2-D24 each declined.")
    if abs(float(alpha) - P2D6_ALPHA) > 1e-12:
        raise AssertionError(
            f"P2-D25: alpha is {float(alpha)!r} and P2-D6 fixes {P2D6_ALPHA!r}. "
            "Nothing P2-D25 authorizes changes the family or its correction.")
    if mapping_to_quantity_c is not None:
        raise AssertionError(
            f"P2-D25: this caller declares a mapping from a marginal-null level onto "
            f"quantity (c): {mapping_to_quantity_c!r}. None is authorized. (c) is a "
            "sign proportion and both quantities are levels in A units; no "
            "preregistered rule connects them, and P2-D24 already rules that use "
            "post-hoc. Writing the mapping blind to A_null does not preregister it, "
            "because every cell of (c) is already published.")
    if successor_cap is not None:
        raise AssertionError(
            f"P2-D25: this caller claims a successor to v2.0 section 4.4's cap: "
            f"{successor_cap!r}. None is authorized and none is needed. The cap's "
            f"object is {P2D25_CAP_APPLIES_TO}: P2-D6 demoted mean dA rather than "
            "deleting it, so the cap applies to it unchanged. What the design lacks "
            "is a defence for quantity (c), and section 5.1 of v2.16 says why none "
            "can be written now.")
    if int(control_arity) != int(confirmatory_arity):
        raise AssertionError(
            f"P2-D25: the control marginal is on |O| = {int(control_arity)} and the "
            f"set the cap reweights is on |O| = {int(confirmatory_arity)}. dA_null "
            "sums p^ctrl(o) * mean_i A_i(o) over ONE option index, so the two must "
            "share an option-id support or the sum is not defined. P2-D3 rejected "
            "pooling for the adjacent reason. The control base is the size tile's "
            f"{P2D25_CONTROL_N} adversary-robust items, not the "
            f"{P2D25_CONTROL_N_ALL_TILES} pooled across tiles.")
    if hypothesis_support != P2D25_MARGINAL_SUPPORT:
        raise AssertionError(
            f"P2-D25: this caller reads the cap as adjudicating a hypothesis stated "
            f"over {hypothesis_support!r}, and both marginals are over "
            f"{P2D25_MARGINAL_SUPPORT!r}. A marginal over canonical option ids "
            "cannot express a preference over menu positions: P1's Format V permutes "
            "the menu per item and per permutation, and canonical options "
            f"{P2D25_CANONICAL_TAIL_IDS} fall in every menu position at near-uniform "
            "rates. Menu position is not adjudicable by any preregistered quantity.")
    if not ext_floor_applied:
        raise AssertionError(
            "P2-D25: this run reports A_null or dA_null without the ext_i floor. "
            f"P2-D23 leaves the {P2D23_FLOOR} floor IN FORCE on every mean or median "
            "of per-item A and on the dA null, and both quantities have that ratio "
            "form through A_i(o). The floor does not reach the confirmatory set and "
            "does reach these.")


# ------------------- the scope registry (DECISIONS.md, case 4: the expired scope)
# A decision that scopes itself to another decision's QUANTITY names that decision
# here. Superseding a quantity then surfaces every dependent scope, because the
# dependents are enumerable rather than discoverable.
#
# Neither provenance nor verbatim binding reaches this failure: the citation is
# clean and the bound text is still true of the thing it originally described.
# Only enumeration does.
#
# An entry here is not an error to fix. It is a question to answer, and the
# failure mode is nobody noticing there is one. `ruled_by` is None until answered.
#
# `defends_against` was added on 2026-09-14 by the second recorded instance, the
# orphaned attribution cap. The first version of this registry recorded WHAT a
# passage was scoped to and not WHAT IT WAS FOR, so an expiry surfaced as a
# sentence needing a ruling and never as a hypothesis left undefended. It is None
# for a passage that is a convention or a threshold, and a string for a passage
# that is a defence. `undefended()` is the louder half of the audit.
SCOPE_REGISTRY = (
    {"passage": "v2.0 section 7.2, the ext_i >= 0.02 exclusion",
     "scoped_to": "mean and median of per-item A",
     "quantity_owned_by": "P2-D6",
     "replaced_by": "P2-D6 (mean demoted to descriptive)",
     "defends_against": None,
     "ruled_by": "P2-D23"},
    {"passage": "v2.0 section 8.2, SESOI = 0.05",
     "scoped_to": "mean dA",
     "quantity_owned_by": "P2-D6",
     "replaced_by": "P2-D6 (mean demoted to descriptive)",
     "defends_against": None,
     "ruled_by": "PREREGISTRATION_v2.4.md section 3.1"},
    {"passage": "v2.5 section 2.3 and v2.6 section 1.4, the magnitude gate",
     "scoped_to": "the c5 comparison as a gate",
     "quantity_owned_by": "P2-D8",
     "replaced_by": "P2-D12 (gate removed)",
     "defends_against": None,
     "ruled_by": "P2-D12"},
    {"passage": "v2.7 section 2.1's diagnostic and section 3.2's n_eff table",
     "scoped_to": "n_eff at the rendering pair",
     "quantity_owned_by": "P2-D12",
     "replaced_by": "P2-D20 (unit moved to the item)",
     "defends_against": None,
     "ruled_by": "P2-D20, P2-D21"},
    # UNRULED. Surfaced by the registry's first run, 2026-09-14. v2.0 section 4
    # required BOTH that the interval on mean dA exclude zero AND that observed
    # mean dA exceed dA_null. P2-D6 retires the first conjunct by demoting the
    # mean. It does not name the second, and P2-D12's three quantities contain no
    # excess-over-the-marginal-null quantity. P2-D5 is adopted and binds the same
    # conjunct independently, on exactly the claim Arm B exists to make.
    {"passage": "v2.0 section 4.4's attribution cap dA_null(m, F), v2.0 section 4's "
                "movement criterion, and P2-D5's second conjunct, 'excess over the "
                "marginal null'",
     "scoped_to": "observed mean dA against dA_null(m, F)",
     "quantity_owned_by": "P2-D6",
     "replaced_by": "P2-D6 (mean demoted), P2-D12 (three quantities fixed, none "
                    "an excess over the marginal null)",
     # THE SECOND RECORDED INSTANCE, and the one that cost something. v2.0
     # section 4.4 labels it "Attribution cap, preregistered" and states what it
     # is for in its own words: "Movement that a generic prompt-induced shift in
     # option preference already explains is reported as prompt sensitivity and
     # named as such." No successor was written. Neither of the cap's inputs
     # exists: TV(m, F) on the beta_c = infinity control set is T7 step 4 and has
     # not been run, and dA_null(m, F) has never been computed. BOTH WERE COMPUTED
     # on 2026-09-15 by src/t7_control.py under P2-D25, descriptively; this comment
     # records the state while the entry was open.
     "defends_against": "the hypothesis that the movement is a generic "
                        "prompt-induced shift in option preference rather than "
                        "adversary tracking",
     # P2-D25 answered the cap half on 2026-09-14: both quantities are
     # descriptive, no mapping onto quantity (c) is authorized, and no successor
     # cap is authorized because the cap's object, mean dA, still exists at
     # descriptive standing. `ruled_by` stayed None then ON PURPOSE, because the
     # passage also covers P2-D5's second conjunct, which was the author's and was
     # still open. P2-D26 closed that half on 2026-09-15; see below.
     "partly_ruled_by": "P2-D25 (v2.0 section 4.4's cap and section 4's movement "
                        "criterion; P2-D5's second conjunct stays the author's)",
     # DISCHARGED by P2-D26. The conjunct is not satisfied and it is not still
     # pending: no adversary-tracking claim is available on the confirmatory set at
     # all, so the conjunct gates nothing there. `defends_against` goes with it, for
     # the same reason and NOT because the defence was restored: the generic-shift
     # hypothesis mattered because a tracking claim had to rule it out, and there is
     # no such claim left to protect.
     "ruled_by": "P2-D25 (the cap and the criterion), P2-D26 (P2-D5's conjunct, "
                 "discharged structurally)"},
)


def scope_audit(registry=SCOPE_REGISTRY):
    """Preregistration passages scoped to a quantity a later decision replaced.

    Returns the UNRULED ones. An empty list means every dependent scope of every
    superseded quantity has been answered, not that none exists: the registry is
    maintained, because no parser can tell a scope from a mention.
    """
    return [r for r in registry if not r["ruled_by"]]


def undefended(registry=SCOPE_REGISTRY):
    """Unruled scopes that were DEFENCES. The louder half of `scope_audit`.

    A convention whose scope expires needs a ruling. A defence whose scope expires
    leaves a hypothesis undefended, and the design stops being able to rule that
    hypothesis out while nothing in the reading says so. The two are the same
    failure and they are not the same cost, so they are separated here.

    This distinction is what the registry's first version lacked. It listed the
    orphaned attribution cap correctly, as its one unruled entry, and the entry
    read as a sentence needing a ruling because no field said the sentence was a
    defence. See `docs/P2/DECISIONS.md`, the two instances recorded together.
    """
    return [r for r in scope_audit(registry) if r.get("defends_against")]


# ------------------- P2-D26, P2-D5's blocker is discharged as permanently blocking
P2D26_TEXT = (
    "P2-D5's blocker is DISCHARGED as permanently blocking, on a structural ground, and\n"
    "not pending further measurement. On the `size` confirmatory set `o*_infinity` equals\n"
    "`o_fit` on all 108 items: of the 8 divergent items where the two differ, 3 are on\n"
    "`manmade` and 5 on `moves`, and none is on `size`. The adversary-aware optimum and\n"
    "the salience pole are therefore the SAME OPTION throughout the confirmatory set, and\n"
    "`v2.0` section 3.3's four references collapse to three there. **No Arm B quantity\n"
    "computed on that set can support a claim about adversary tracking**, because the\n"
    "coordinate cannot distinguish adversary-aware behaviour from salience-driven\n"
    "behaviour when the two targets are one point, and no successor measure on `size` can\n"
    "either. This is not a caveat to attach to a result. It is why the direction question\n"
    "was never answerable on this set, and it explains P2-D24 from the other side: P2-D24\n"
    "found that the design licenses nothing about direction, and this says why. The tile\n"
    "is not revisitable: Paper 1's D49 and D108 fixed `size` on measured grounds before\n"
    "any of this was known, and the 8 separating items sit on tiles those decisions\n"
    "excluded. The confirmatory confound is stated as **108 of 108** and never as 452 of\n"
    "460, which is a divergence-set figure and understates the confirmatory case."
)
P2D26_REJECTED = (
    "Discharge the blocker as satisfied, by treating a framing contrast as an excess.",
    "Hold the blocker open pending a successor measure on `size`.",
    "Revisit the tile so the 8 separating items enter the confirmatory set.")
P2D26_BLOCKER_DISCHARGED = True
P2D26_DISCHARGE_IS_STRUCTURAL = True      # not pending measurement
P2D26_ADVERSARY_TRACKING_CLAIM_AVAILABLE = False
P2D26_TILE_REVISITABLE = False
# The premise the discharge rests on, and the one thing that could undo it.
P2D26_CONFIRMATORY_COINCIDENCE = (108, 108)   # o*_infinity == o_fit, size tile
P2D26_DIVERGENCE_COINCIDENCE = (452, 460)     # divergence set; NOT the confirmatory figure
P2D26_SEPARATING_ITEMS_BY_TILE = {"hold": 0, "manmade": 3, "moves": 5, "size": 0}
P2D26_CONFOUND_FIGURE_FOR_CONFIRMATORY = "108 of 108"


def bind_adversary_tracking_claim(tracking_claim_made, coincidence_count,
                                  confirmatory_n, confound_figure_cited):
    """Assert the premise P2-D26's discharge rests on. Call where Arm B reports.

    Per the binding-form note in `docs/P2/DECISIONS.md`, this asserts the premise
    that makes the discharge well founded, not a range any statistic occupies. The
    premise is that the adversary-aware optimum and the salience pole are the SAME
    option on every confirmatory item. If an item set ever separates them, the
    coordinate can distinguish the two behaviours again, this assert fires, and
    P2-D26 is re-read rather than assumed. A partial coincidence is not a weaker
    version of the discharge; it is a different case the ruling does not cover.
    """
    if bool(tracking_claim_made) != P2D26_ADVERSARY_TRACKING_CLAIM_AVAILABLE:
        raise AssertionError(
            "P2-D26: this caller reports a claim about adversary tracking. None is "
            "available on the confirmatory set: the adversary-aware optimum and the "
            "salience pole are the same option on all 108 items, so no quantity "
            "computed there can separate the two behaviours. "
            "docs/P2/DECISIONS.md is the source.")
    want_c, want_n = P2D26_CONFIRMATORY_COINCIDENCE
    if (int(coincidence_count), int(confirmatory_n)) != (want_c, want_n):
        raise AssertionError(
            f"P2-D26: the discharge rests on o*_infinity == o_fit on ALL "
            f"{want_n} confirmatory items; this run gives {int(coincidence_count)} "
            f"of {int(confirmatory_n)}. If the two targets separate anywhere in the "
            "set, the coordinate can tell the two behaviours apart on those items "
            "and P2-D26 does not cover that case.")
    if "452" in str(confound_figure_cited):
        raise AssertionError(
            f"P2-D26: the confirmatory confound is cited as "
            f"{confound_figure_cited!r}. 452 of 460 is a DIVERGENCE-set figure and "
            f"understates the confirmatory case, which is "
            f"{P2D26_CONFOUND_FIGURE_FOR_CONFIRMATORY}.")


# ------------- P2-D27, a change rate on the control set: new, exploratory, side by side
P2D27_TEXT = (
    "A change rate on the `beta_c = infinity` control set is NOT preregistered work under\n"
    "T7 step 4. Step 4 names movement and its role and names no instrument and no unit, and\n"
    "it was written on 2026-09-09, before P2-D12 made quantity (a) a change rate, so its\n"
    "word \"movement\" cannot carry (a)'s instrument. The preregistration that operationalizes\n"
    "step 4 is `v2.0` section 4.4, and it names one control measure, `TV`. P2-D12 scopes (a)\n"
    "to the confirmatory `n`. P2-D25 authorized `TV` and is SILENT on a change rate: it\n"
    "neither declined nor authorized one, and `steps_not_run` in\n"
    "`results/T7_control_marginal_null.json` records the computing session's reading of that\n"
    "silence under its own instruction, not a ruling. The control change rate is therefore a\n"
    "NEW quantity. It is AUTHORIZED NOW, as EXPLORATORY under `v2.0` section 10 and\n"
    "descriptive, because its instrument is fixed by existing decisions and by matching (a)\n"
    "cell for cell, and leaves no choice that could be fitted to its value:\n"
    "`c5_effect.c5_movement` with `col = \"framing\"` and `base = \"F0\"`, per model, for `F1`\n"
    "and `F2`, on the `size` tile's 142 adversary-robust items only, with P2-D16's pairwise\n"
    "exclusion, and with P2-D8's cluster bootstrap interval emitted as (a) emits it and\n"
    "carrying no inferential role, as P2-D13 left it in (a). The rate is reported with its\n"
    "item count beside it, as (a) is. P2-D13's floor is not applied and no verdict flag is\n"
    "emitted, because the floor exists for (a)'s inertness verdict and no verdict on the\n"
    "control is authorized. It does not enter the confirmatory family, which stays 21 tests\n"
    "at `alpha = 0.05/21`. The comparison it licenses is SIDE BY SIDE, per cell, in the same\n"
    "units, and nothing beyond: no difference, ratio, attributable share or test of (a)\n"
    "against the control rate is authorized. Each would be a new quantity written with (a)\n"
    "published and with the control's `TV`, which bounds its rate from below, in view, so it\n"
    "would be post-hoc; each would need a rule transferring a rate across two disjoint item\n"
    "sets that differ by construction, which no version writes; and a share of (a) read as\n"
    "adversary-attributable is a claim about adversary content on the confirmatory set, which\n"
    "P2-D26 makes unavailable."
)
P2D27_REJECTED = (
    "Rule the control change rate preregistered under T7 step 4.",
    "Leave it uncomputed and state the control in `TV` only.",
    "Authorize the rate together with a difference, ratio or attributable share against "
    "quantity (a).",
    "Apply P2-D13's floor to the control and emit a verdict flag.",
    "Report the change rate on the 540-item all-tile base beside the 142.")
# The answer to the question asked. Step 4 names no instrument; v2.0 section 4.4
# names TV; P2-D12 is scoped to the confirmatory n; P2-D25 never mentions a rate.
P2D27_PREREGISTERED = False
P2D27_P2D25_ADDRESSED = False      # silence: neither declined nor authorized
P2D27_AUTHORIZED = True
P2D27_STANDING = "exploratory"     # v2.0 section 10: requested after the data
P2D27_IN_CONFIRMATORY_FAMILY = False
# Quantity (a)'s own instrument and contrast, so the side-by-side is like for like.
P2D27_INSTRUMENT = ("c5_effect", "c5_movement")
P2D27_CONTRAST = ("framing", "F0")
P2D27_ARMS = ("F1", "F2")          # (a)'s two contrasts; (a) has no F2-F1 cell
P2D27_CONTROL_TILE = P2D25_CONTROL_TILE
P2D27_CONTROL_N = P2D25_CONTROL_N  # 142, the tile, arity and menus (a) is on
P2D27_ALL_TILES_AUTHORIZED = False
P2D27_FLOOR_APPLIED = False
# Exactly what is emitted per cell: (a)'s a_inertness block in t7_armb, minus its
# verdict flags (`interval_excludes_zero`, `clears_the_floor`), its floor and null,
# and its `tv_option_marginal`, since the control TV of record is P2-D25's.
P2D27_FIELDS = ("change_rate_renderings", "change_rate_item_mean", "n_changed_pairs",
                "n_pairs", "ci_lo", "ci_hi", "alpha", "n_items_with_a_changed_pair",
                "item_denominator")
P2D27_COMPARISON = "side_by_side"
P2D27_DERIVED_AUTHORIZED = ()      # no difference, ratio, share or test


def bind_control_change_rate(instrument, contrast, arms, control_beta_c, control_tiles,
                             reads_A, in_confirmatory_family, alpha, emitted_fields,
                             derived_quantities, floor_applied):
    """Assert the premises that make a control change rate well formed. P2-D27.

    Call before emitting anything. Per the binding-form note in
    `docs/P2/DECISIONS.md`, every check is a premise the ruling rests on, and no
    value of the rate appears here: the ruling was made before any existed, and it
    must not become re-readable only once one does.

    `instrument`, `contrast`, `arms`: the rate is placed beside quantity (a), so it
    must BE (a)'s instrument on (a)'s contrasts. A different function, base or arm
    set makes the side-by-side compare two instruments rather than two item sets.

    `control_beta_c`, `control_tiles`: every item has `beta_c = infinity`, so
    `o*_0 = o*_infinity` and nothing adversary-relevant can move there (`v2.0`
    section 4.4), and every item is on the `size` tile, so the menus and arity are
    (a)'s. The count is P2-D25's base.

    `reads_A`: must be False. `A` is undefined on the control set (`v2.0` section
    3.2), and the rate's standing outside P2-D26 rests on reading chosen options
    only.

    `emitted_fields`, `derived_quantities`, `floor_applied`: the ruling authorizes a
    descriptive rate with its item count, side by side with (a). A verdict flag, a
    floor, or any difference, ratio, share or test against (a) is a quantity no
    version writes, chosen with (a) published and the control's TV in view.
    """
    got = (getattr(instrument, "__module__", None), getattr(instrument, "__name__", None))
    if got != P2D27_INSTRUMENT:
        raise AssertionError(
            f"P2-D27: the control rate is formed by {got!r}. It must be quantity (a)'s "
            f"own instrument, {'.'.join(P2D27_INSTRUMENT)}, or the side-by-side "
            "compares two instruments and not two item sets. "
            "docs/P2/DECISIONS.md is the source.")
    if tuple(contrast) != P2D27_CONTRAST or tuple(arms) != P2D27_ARMS:
        raise AssertionError(
            f"P2-D27: contrast {tuple(contrast)!r} with arms {tuple(arms)!r}. Quantity "
            f"(a) is {P2D27_CONTRAST!r} against {P2D27_ARMS!r}; any other contrast has "
            "no (a) cell to sit beside.")
    beta = [float(b) for b in control_beta_c]
    if any(math.isfinite(b) for b in beta):
        raise AssertionError(
            "P2-D27: an item in the control set has finite beta_c. The control's "
            "reading as prompt sensitivity rests on o*_0 = o*_infinity on EVERY item, "
            "and on an item with finite beta_c the adversary does move the optimum.")
    tiles = set(control_tiles)
    if tiles != {P2D27_CONTROL_TILE} or len(beta) != P2D27_CONTROL_N:
        raise AssertionError(
            f"P2-D27: the control base is {len(beta)} items on {sorted(tiles)!r}. The "
            f"side-by-side needs (a)'s tile, arity and menus: the "
            f"{P2D27_CONTROL_N} adversary-robust items of '{P2D27_CONTROL_TILE}'. "
            "A base mixing arities is comparable to (a) in neither direction.")
    if bool(reads_A):
        raise AssertionError(
            "P2-D27: this run reads A on the control set. A is undefined there "
            "(v2.0 section 3.2), and the rate stands outside P2-D26 only because it "
            "reads chosen options and nothing else.")
    if bool(in_confirmatory_family) != P2D27_IN_CONFIRMATORY_FAMILY:
        raise AssertionError(
            "P2-D27: the control rate is placed in the confirmatory family. It was "
            "requested after the data and is exploratory under v2.0 section 10; the "
            "family stays 21 tests.")
    if abs(float(alpha) - P2D6_ALPHA) > 1e-12:
        raise AssertionError(
            f"P2-D27: the interval's alpha is {float(alpha)!r}. It is emitted as (a) "
            f"emits it, at {P2D6_ALPHA!r}, and carries no inferential role.")
    fields = set(emitted_fields)
    if fields != set(P2D27_FIELDS):
        raise AssertionError(
            f"P2-D27: emitted fields differ from the ruling's. Extra "
            f"{sorted(fields - set(P2D27_FIELDS))!r}, missing "
            f"{sorted(set(P2D27_FIELDS) - fields)!r}. A verdict flag or floor is a "
            "verdict no decision authorizes on the control; a second TV duplicates "
            "P2-D25's; the item count must sit beside the rate as it does for (a).")
    if tuple(derived_quantities) != P2D27_DERIVED_AUTHORIZED:
        raise AssertionError(
            f"P2-D27: derived quantities {tuple(derived_quantities)!r}. None is "
            "authorized: each is written with (a) published, needs an unwritten rule "
            "transferring a rate across disjoint item sets, and a share of (a) read "
            "as adversary-attributable is what P2-D26 makes unavailable.")
    if bool(floor_applied) != P2D27_FLOOR_APPLIED:
        raise AssertionError(
            "P2-D27: P2-D13's floor is applied to the control. It is the convention "
            "for (a)'s inertness verdict on the confirmatory set, and no verdict on "
            "the control is authorized.")


# ------------- P2-D28, tolerance-determined divergent items: kept, and disclosed
P2D28_TEXT = (
    "Spec section 6.2's tie-broken argmax stays the definition of divergence, and the pool\n"
    "items whose `beta_c` is set by D51's band stay in `D(infinity)`. They are 136 pool items,\n"
    "and all 136 are divergent only by tie-break: the tie-broken winner never leads `o*_0`\n"
    "beyond the band at any `beta`, and no other rival does either. They are disclosed beside\n"
    "the pool existence rate, never omitted, with four facts: the count; that every one has\n"
    "`beta_c` between 17.35 and 23.45, above the reporting grid's endpoint of 8, so `|D(8)|`\n"
    "and every grid-rate figure are unaffected and only `|D(infinity)|` includes them; that\n"
    "none of the 2,748 separating items is among them; and that the frozen 1,000 contains\n"
    "none, so no confirmatory claim is touched."
)
P2D28_REJECTED = (
    "Exclude the tolerance-determined items from the divergence set.",
    "Report the pool existence rate without the disclosure.")
P2D28_EXCLUDED = False                      # spec 6.2's tie-broken argmax is the definition
P2D28_N_TOLERANCE_DETERMINED = 136
P2D28_N_DIVERGENT_ONLY_BY_TIE_BREAK = 136   # not 99: v2.22 section 2 corrects v2.21 section 8
P2D28_N_SEPARATING_AMONG = 0
P2D28_N_FROZEN = 0
P2D28_DISCLOSURE_FIELDS = ("n_tolerance_determined", "n_divergent_only_by_tie_break",
                           "tolerance_determined_beta_c_range",
                           "n_separating_tolerance_determined")


def bind_tolerance_determined_disclosure(record):
    """Assert P2-D28's premises from `results/T1_crossing_tolerance.json` and return
    the fields every pool existence-rate statement carries beside it.

    Premises, not ranges: the items are still counted in D(infinity) (the pool's
    divergent count is its finite-beta_c count); every one lies above the grid
    endpoint, which is WHY |D(8)| is unaffected; none separates; the frozen base has
    none, which is WHY no confirmatory claim is touched.
    """
    pool, frozen = record["bases"]["pool_200000"], record["bases"]["frozen_1000"]
    if P2D28_EXCLUDED or pool["n_divergent"] != pool["n_finite_beta_c"]:
        raise AssertionError("P2-D28: tolerance-determined items stay in D(infinity); "
                             "a caller excluding them redefines divergence after the data.")
    if not pool["tolerance_determined_all_above_grid_endpoint"]:
        raise AssertionError("P2-D28: a tolerance-determined beta_c reached the grid; "
                             "'|D(8)| is unaffected' no longer holds.")
    if pool["n_separating_tolerance_determined"] != P2D28_N_SEPARATING_AMONG:
        raise AssertionError("P2-D28: a separating item is tolerance-determined; the "
                             "2,748 sentence needs the author.")
    if frozen["n_tolerance_determined"] != P2D28_N_FROZEN:
        raise AssertionError("P2-D28: the frozen 1,000 carries a tolerance-determined "
                             "item; 'no confirmatory claim is touched' no longer holds.")
    got = (pool["n_tolerance_determined"], pool["n_divergent_only_by_tie_break"])
    if got != (P2D28_N_TOLERANCE_DETERMINED, P2D28_N_DIVERGENT_ONLY_BY_TIE_BREAK):
        raise AssertionError(f"P2-D28: counts {got} are not the ruled "
                             f"{(P2D28_N_TOLERANCE_DETERMINED, P2D28_N_DIVERGENT_ONLY_BY_TIE_BREAK)}.")
    return {k: pool[k] for k in P2D28_DISCLOSURE_FIELDS}


# ------------- P2-D29, the closed form's parallel case read at EPS_TIE
P2D29_TEXT = (
    "`adversary._crossings` treats a rival as never overtaking when the coefficient of `x`\n"
    "in its crossing equation has magnitude at most `PARALLEL_TOL = 1e-12`, which is\n"
    "`EPS_TIE`, the spec's inherited absolute tie tolerance, not a new constant. The test\n"
    "is on the coefficient of `x` alone, because spec section 6.3's degenerate case is that\n"
    "coefficient being zero, in both its parallel and its identical form. On the 200,000\n"
    "pool every root pair whose curves are identical or only converge has that coefficient\n"
    "at most 3.5e-17, and every pair that crosses strictly has it at least 7.3e-8, so every\n"
    "tolerance inside that interval classifies identically. With it, the closed form\n"
    "disagrees with bisection on exactly the 136 tolerance-determined items of P2-D28 and on\n"
    "no other item. That residual is the cross-check's expected state, because the closed\n"
    "form tests strict crossing and cannot see a tie-break flip, and it is asserted as an\n"
    "invariant."
)
P2D29_REJECTED = (
    "Both-coefficients rule, as `v2.21` section 7 proposed.",
    "Keep the exact `den != 0` test and report the disagreement as unresolved.")
P2D29_PARALLEL_TOL = 1e-12                  # spec 8.2's EPS_TIE, inherited
P2D29_TESTED_COEFFICIENT = "den"            # the coefficient of x, spec 6.3


def bind_parallel_tol(parallel_tol, record):
    """Assert the closed form's tolerance against P2-D29, from the caller's own value.

    The premise is the empty gap, on both bases, and the residual invariant: after the
    fix the cross-check disagrees on exactly the tolerance-determined set. A geometry
    that puts a coefficient inside the gap fails here, not in a cross-check count.
    """
    if parallel_tol != P2D29_PARALLEL_TOL or record["parallel_tol"] != P2D29_PARALLEL_TOL:
        raise AssertionError(f"P2-D29: parallel_tol is {parallel_tol!r}, ruled "
                             f"{P2D29_PARALLEL_TOL!r}.")
    for name, base in record["bases"].items():
        lo, hi = base["coefficients"]["den_gap"]
        if not lo < parallel_tol < hi:
            raise AssertionError(f"P2-D29: {name}: {parallel_tol} is not inside the "
                                 f"empty gap ({lo}, {hi}); the tolerance became a choice.")
        if not base["cross_check_adopted_parallel_tol"]["residual_equals_tol_set"]:
            raise AssertionError(f"P2-D29: {name}: the cross-check disagrees off the "
                                 "tolerance-determined set. That is a bug, not a residual.")
    return True


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
                         ("P2-D3", P2D3_TEXT), ("P2-D4", P2D4_TEXT),
                         ("P2-D5", P2D5_TEXT), ("P2-D6", P2D6_TEXT),
                         ("P2-D7", P2D7_TEXT), ("P2-D8", P2D8_TEXT),
                         ("P2-D9", P2D9_TEXT), ("P2-D10", P2D10_TEXT),
                         ("P2-D11", P2D11_TEXT), ("P2-D12", P2D12_TEXT),
                         ("P2-D13", P2D13_TEXT), ("P2-D14", P2D14_TEXT),
                         ("P2-D15", P2D15_TEXT), ("P2-D16", P2D16_TEXT),
                         ("P2-D19", P2D19_TEXT),
                         ("P2-D20", P2D20_TEXT),
                         ("P2-D21", P2D21_TEXT),
                         ("P2-D22", P2D22_TEXT),
                         ("P2-D23", P2D23_TEXT),
                         ("P2-D24", P2D24_TEXT),
                         ("P2-D25", P2D25_TEXT),
                         ("P2-D26", P2D26_TEXT),
                         ("P2-D27", P2D27_TEXT),
                         ("P2-D28", P2D28_TEXT),
                         ("P2-D29", P2D29_TEXT)):
        quoted = "\n".join("> " + ln for ln in const.split("\n"))
        if quoted not in text:
            raise AssertionError(
                f"D100: {label}'s decision text is not quoted verbatim in {path}.\n"
                f"  in code:\n{quoted}\n"
                "Fix whichever one drifted. The log is the source.")
    for label, rejected in (("P2-D1", P2D1_REJECTED), ("P2-D2", P2D2_REJECTED),
                            ("P2-D3", P2D3_REJECTED), ("P2-D4", P2D4_REJECTED),
                            ("P2-D5", P2D5_REJECTED), ("P2-D6", P2D6_REJECTED),
                            ("P2-D7", P2D7_REJECTED), ("P2-D8", P2D8_REJECTED),
                            ("P2-D9", P2D9_REJECTED), ("P2-D10", P2D10_REJECTED),
                            ("P2-D11", P2D11_REJECTED),
                            ("P2-D12", P2D12_REJECTED),
                            ("P2-D13", P2D13_REJECTED),
                            ("P2-D14", P2D14_REJECTED),
                            ("P2-D15", P2D15_REJECTED),
                            ("P2-D16", P2D16_REJECTED),
                            ("P2-D19", P2D19_REJECTED),
                            ("P2-D20", P2D20_REJECTED),
                            ("P2-D21", P2D21_REJECTED),
                            ("P2-D22", P2D22_REJECTED),
                            ("P2-D23", P2D23_REJECTED),
                            ("P2-D24", P2D24_REJECTED),
                            ("P2-D25", P2D25_REJECTED),
                            ("P2-D26", P2D26_REJECTED),
                            ("P2-D27", P2D27_REJECTED),
                            ("P2-D28", P2D28_REJECTED),
                            ("P2-D29", P2D29_REJECTED)):
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
    print(f"Arm B statistic tie rate + sign test vs p0={P2D6_P0}, "
          f"alpha={P2D6_ALPHA:.6f}; mean is confirmatory="
          f"{P2D6_MEAN_IS_CONFIRMATORY}")
    print(f"level confound  P2-D5: raw single-framing A carries no claim")
    print(f"tie reference   P2-D8: c5 same-option, {len(P2D8_C5_REFERENCE)} models, "
          f"boot seed {P2D8_BOOT_SEED}; in main family={P2D8_TIE_IN_MAIN_FAMILY}")
    print(f"redraw (b)      P2-D7: declined, enlargement authorized="
          f"{P2D7_ENLARGEMENT_AUTHORIZED}")
    print(f"c5 status       P2-D9: active={P2D9_C5_IS_ACTIVE}, change rate "
          f"{P2D9_C5_CHANGE_RATE_RANGE[0]:.4f} to "
          f"{P2D9_C5_CHANGE_RATE_RANGE[1]:.4f} against a no-effect rate of "
          f"{P2D9_NO_EFFECT_SAME_OPTION_RATE}")
    print(f"primary rate    P2-D10: {P2D10_PRIMARY_RATE!r}; sign test denominator "
          f"{P2D10_SIGN_TEST_DENOMINATOR!r}")
    print(f"quantities      P2-D12: {P2D12_QUANTITIES}; c5 gates="
          f"{P2D12_C5_GATES}; inertness null={P2D12_INERTNESS_NULL}, floor "
          f"{P2D12_INERTNESS_FLOOR_ITEMS} of {P2D4_N_CONFIRMATORY} items")
    print(f"inertness floor P2-D13: provisional {P2D13_PROVISIONAL_FLOOR}, "
          f"floor = max({P2D13_PROVISIONAL_FLOOR}, F0 disagreement items); "
          f"statistical={P2D13_FLOOR_IS_STATISTICAL}, "
          f"upward only={P2D13_REVISION_IS_UPWARD_ONLY}")
    print(f"type II cost    P2-D14: p0={P2D6_P0} kept; gap to the neutral baseline "
          f"{min(P2D14_TYPE_II_GAP.values()):.4f} to "
          f"{max(P2D14_TYPE_II_GAP.values()):.4f}")
    print(f"tie handling    P2-D16: excluded at {P2D16_EXCLUSION_UNIT}; "
          f"imputed as non-mover={P2D16_IMPUTE_TIE_AS_NON_MOVER}, whole item "
          f"dropped={P2D16_DROPS_WHOLE_ITEM}, attrition reported="
          f"{P2D16_ATTRITION_IS_REPORTED}")
    print(f"A-tie tolerance P2-D19: eps={P2D19_EPS:g} (P1 tiebreak.EPS); PRIMARY "
          f"per-pair {P2D19_A_TIED_PAIRS}/{P2D19_TOTAL_PAIRS}="
          f"{P2D19_A_TIED_PAIRS / P2D19_TOTAL_PAIRS:.4f} vs "
          f"{P2D19_DIVERGENCE_PAIRS}/{P2D19_DIVERGENCE_TOTAL_PAIRS}="
          f"{P2D19_DIVERGENCE_PAIRS / P2D19_DIVERGENCE_TOTAL_PAIRS:.4f} pooled "
          f"(x{(P2D19_A_TIED_PAIRS / P2D19_TOTAL_PAIRS) / (P2D19_DIVERGENCE_PAIRS / P2D19_DIVERGENCE_TOTAL_PAIRS):.2f})")
    print(f"                secondary per-item {P2D19_A_TIED_ITEMS} of "
          f"{P2D4_N_CONFIRMATORY} items carry ANY tied pair, inflated by option "
          f"count; exact equality gives {P2D19_EXACT_EQUALITY_PAIRS} pairs on "
          f"{P2D19_EXACT_EQUALITY_ITEMS} items; empty gap {P2D19_GAP[0]:.3g} to "
          f"{P2D19_GAP[1]:.3g}")
    print(f"quantity (c)    P2-D20: unit={P2D20_UNIT}; sign disagreement -> "
          f"{P2D20_SIGN_DISAGREEMENT}; one-pair item contributes="
          f"{P2D20_ONE_PAIR_ITEM_CONTRIBUTES}, cancelling item is a tie="
          f"{P2D20_CANCELLING_ITEM_IS_A_TIE}")
    print("                c5 n_eff item " + " ".join(
        f"{m}={n}" for m, n in P2D20_C5_N_EFF_ITEM.items()))
    print("                superseded: pair " + " ".join(
        str(n) for n in P2D20_C5_N_EFF_PAIR_EXACT.values()) + "; rescaled "
        + " ".join(str(n) for n in P2D20_C5_N_EFF_RESCALED.values()))
    print(f"neutral baseline P2-D21: p0={P2D21_P0} UNMOVED (moved={P2D21_P0_MOVED}); "
          f"\"at or below 0.5 on all seven models\" holds="
          f"{P2D21_ALL_SEVEN_CLAIM_HOLDS}, P2-D15's six-ladder restatement "
          f"holds={P2D21_SIX_LADDER_CLAIM_HOLDS}")
    print("                item-unit proportion " + " ".join(
        f"{m}={v:.4f}" for m, v in P2D21_C5_SIGN_PROPORTION_ITEM.items()))
    print("                signed Type II gap  " + " ".join(
        f"{m}={v:+.4f}" for m, v in P2D21_TYPE_II_GAP_ITEM.items()))
    print(f"                baseline ABOVE p0 on {P2D21_NEUTRAL_ABOVE_P0} "
          f"(Type I exposure, not a Type II cost); departs at the corrected "
          f"alpha only on {P2D21_SIGNIFICANT_AT_CORRECTED_ALPHA}, downward")
    print(f"claim wording    P2-D22: tally frame permitted="
          f"{P2D22_TALLY_FRAME_PERMITTED}, 'conservative' justifies p0="
          f"{P2D22_CONSERVATIVE_JUSTIFIES_P0}; B2 at the null="
          f"{P2D22_B2_AT_THE_NULL}, exactly 0.5 under "
          f"{P2D22_B2_EXACTLY_HALF_UNDER} and above under "
          f"{P2D22_B2_ABOVE_HALF_UNDER}")
    print(f"ext_i floor      P2-D23: floor={P2D23_FLOOR} RETAINED, applies to the "
          f"confirmatory set={P2D23_APPLIES_TO_CONFIRMATORY}; n stays "
          f"{P2D23_CONFIRMATORY_N}; min ext_i {P2D23_MIN_EXT_CONFIRMATORY:.6g} > 0")
    print("                governs " + "; ".join(P2D23_GOVERNS))
    _open, _und = scope_audit(), undefended()
    print(f"scope registry   {len(SCOPE_REGISTRY)} scoped passages, {len(_open)} UNRULED, "
          f"{len(_und)} of them DEFENCES")
    for _r in _open:
        print(f"                UNRULED: {_r['passage']}")
        print(f"                         scoped to {_r['scoped_to']}, replaced by "
              f"{_r['replaced_by']}")
        if _r.get("defends_against"):
            print(f"                         UNDEFENDED: {_r['defends_against']}")
    print(f"P2-D5 blocker   P2-D26: DISCHARGED structurally; adversary-tracking "
          f"claim available={P2D26_ADVERSARY_TRACKING_CLAIM_AVAILABLE}; "
          f"o*_inf == o_fit on {P2D26_CONFIRMATORY_COINCIDENCE[0]} of "
          f"{P2D26_CONFIRMATORY_COINCIDENCE[1]} confirmatory items; confound is "
          f"{P2D26_CONFOUND_FIGURE_FOR_CONFIRMATORY}, never 452 of 460")
    print(f"WITHDRAWN       P2-D17, P2-D18: never decisions, numbers retired")
    print(f"D111 on CTRL    P2-D15: sign(delta-A) admissible="
          f"{P2D15_SIGN_IS_ADMISSIBLE}; still inadmissible "
          f"{P2D15_STILL_INADMISSIBLE}")
    print(f"SUPERSEDED      P2-D11: framing must move "
          f"{P2D11_CEILING['change_rate_multiple_of_c5'][0]:.2f} to "
          f"{P2D11_CEILING['change_rate_multiple_of_c5'][1]:.2f} x c5; n_eff then "
          f"<= {P2D11_CEILING['n_eff_max'][0]}-{P2D11_CEILING['n_eff_max'][1]}, "
          f"p1 at 80% power {P2D11_CEILING['p1_at_80_power'][0]:.3f}-"
          f"{P2D11_CEILING['p1_at_80_power'][1]:.3f}")
    print("rejected        " + ", ".join(
        f"{len(r)} on P2-D{i}" for i, r in enumerate(
            (P2D1_REJECTED, P2D2_REJECTED, P2D3_REJECTED, P2D4_REJECTED,
             P2D5_REJECTED, P2D6_REJECTED, P2D7_REJECTED,
             P2D8_REJECTED, P2D9_REJECTED, P2D10_REJECTED,
             P2D11_REJECTED, P2D12_REJECTED, P2D13_REJECTED,
             P2D14_REJECTED, P2D15_REJECTED, P2D16_REJECTED), start=1))
          + f", {len(P2D19_REJECTED)} on P2-D19, {len(P2D20_REJECTED)} on P2-D20"
          + f", {len(P2D21_REJECTED)} on P2-D21, {len(P2D22_REJECTED)} on P2-D22"
          + f", {len(P2D23_REJECTED)} on P2-D23"
          + f", {len(P2D24_REJECTED)} on P2-D24"
          + f", {len(P2D25_REJECTED)} on P2-D25"
          + ", all present in the log")
    print(f"direction       P2-D24: licensed={P2D24_DIRECTION_CLAIM_LICENSED}; "
          f"movement licensed={P2D24_MOVEMENT_CLAIM_LICENSED}; resolving cells "
          f"{P2D24_RESOLVING_CELLS}, all downward="
          f"{P2D24_RESOLVING_ALL_DOWNWARD}; neutral resolves on "
          f"{P2D24_NEUTRAL_RESOLVES_ON}; marginal null computed="
          f"{P2D24_MARGINAL_NULL_COMPUTED}")
    print(f"marginal nulls  P2-D25: A_null and dA_null DESCRIPTIVE "
          f"(in confirmatory family={P2D25_IN_CONFIRMATORY_FAMILY}, family stays "
          f"{P2D25_CONFIRMATORY_FAMILY_SIZE} at alpha={P2D6_ALPHA:.6f}); mapping "
          f"onto quantity (c)={P2D25_MAPPING_TO_QUANTITY_C}; successor cap "
          f"authorized={P2D25_SUCCESSOR_CAP_AUTHORIZED}, the cap applies to "
          f"{P2D25_CAP_APPLIES_TO}")
    print(f"                control TV authorized={P2D25_CONTROL_TV_AUTHORIZED} on "
          f"the {P2D25_CONTROL_TILE} tile's {P2D25_CONTROL_N} robust items "
          f"(|O|={P2D25_CONFIRMATORY_ARITY}); {P2D25_CONTROL_N_ALL_TILES} pooled is "
          f"a different base and is reported beside it")
    print(f"                marginal support {P2D25_MARGINAL_SUPPORT!r}; menu "
          f"position adjudicable={P2D25_MENU_POSITION_ADJUDICABLE}; canonical "
          f"{P2D25_CANONICAL_TAIL_IDS} are NOT the end of the rendered menu; ext_i "
          f"floor in force={P2D25_EXT_FLOOR_IN_FORCE}")
    print(f"constants match {os.path.relpath(LOG)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
