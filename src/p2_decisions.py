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
                         ("P2-D22", P2D22_TEXT)):
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
                            ("P2-D22", P2D22_REJECTED)):
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
          + ", all present in the log")
    print(f"constants match {os.path.relpath(LOG)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
