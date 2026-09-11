"""Arm B's detection limits under P2-D12's restructure, and the diagnostics behind it.

P2-D8 made the `c5` comparison a GATE: the movement half of H-B's conjunction
fired only if the framing's same-option rate sat more than a bootstrap half-width
below `R_m`. `results/T5_detection_ceiling.json` measured what that cost, and the
cost was the design: `L1` had to move 2.13 times what `c5` moves before anything
fired, and the effective `n` for the sign test was bounded at 32 to 58.

P2-D9 is what makes the gate unnecessary. Paper 1's scorer is deterministic, so
the no-effect same-option rate is exactly 1.0 and the inertness question the
reference was introduced for ("did F1 move anything, or are T3's templates too
weak") is answered by the change rate against **zero**, at full `n`. The `c5`
comparison is retained as magnitude context and gates nothing.

This file emits three things.

  1. THE INERTNESS FLOOR.  How many of the 108 items must carry a changed
     rendering before the cluster bootstrap's lower bound clears zero. It is a
     count, not a rate, because the bootstrap's lower bound is zero exactly when
     a resample can contain no moving item.

  2. THE SIGN TEST'S POSITION, unbounded by the gate.  Effective `n` is now
     whatever the observed tie rate gives. Since no tie rate is observable before
     T7 runs, `c5`'s own tie rate is reported as an analogue, with the same
     caveat `reports/T5_sigma_prior.md` section 0 attaches to its own: a
     structurally matched manipulation, not a measurement of the quantity.

  3. TWO DIAGNOSTICS that bear on whether the gate bought anything.

     `c5`'s own `ΔA` sign proportion answers the one thing a magnitude gate might
     have been reaching for: whether a content-neutral insertion drifts toward
     `o*_infinity`, which is P1's salience pole on 452 of 460 divergent items. If
     it did, a positive F1 sign test would be explicable without adversary
     tracking. Measured, it does not: the proportion is at or below 0.5 on all
     seven models. **This is reported, and it is NOT adopted as a null.** Moving
     `p0` off 0.5 would recalibrate a preregistered test against a different
     manipulation, and P2-D6 fixed `p0 = 0.5`.

     `c5`'s tie rate minus its same-option rate is P2-D10's blind spot, measured
     on a real manipulation rather than bounded from the geometry.

Run: python3 src/inertness_ceiling.py          (writes results/T5_inertness_ceiling.json)
     python3 src/inertness_ceiling.py --demo   (self-check on the floor)
"""
import json
import os
import sys

import numpy as np
from scipy.stats import binomtest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2_decisions as P2D  # noqa: E402
import sign_power as SP     # noqa: E402
import tie_reference as TR  # noqa: E402

OUT = "results/T5_inertness_ceiling.json"
N = SP.N_CONFIRMATORY
P_GRID = (0.60, 0.65, 0.70, 0.75, 0.80, 0.90)


def inertness_floor(n=N, alpha=SP.ALPHA):
    """Smallest number of moving items whose bootstrap lower bound clears zero.

    The item-level mean of a resample is zero exactly when the resample contains
    no moving item, so the lower bound at `alpha/2` is positive as soon as
    `((n - k) / n) ** n < alpha / 2`. Solved by search and then checked against
    the real bootstrap, because an analytic floor that the implementation does
    not reproduce is worth nothing.
    """
    for k in range(1, n + 1):
        if ((n - k) / n) ** n < alpha / 2:
            return k
    return None


def check_floor(k, n=N, both_permutations=True):
    """Run P2-D8's actual bootstrap on a `k`-mover configuration."""
    v = np.zeros(n)
    v[:k] = 1.0 if both_permutations else 0.5
    r = TR.cluster_bootstrap_diff(np.arange(n), v, np.zeros(n))
    return {"k": k, "item_mean": r["difference"], "lo": r["lo"],
            "clears_zero": bool(r["lo"] > 0)}


def c5_delta_A(ch, A, keep):
    """`c5`'s own tie rate, blind spot and `ΔA` sign proportion, per model."""
    out = {}
    for m in TR.LADDER:
        g = ch[(ch["model"] == m) & (ch["prompt_form"] == TR.FORM)
               & (ch["rule"] == TR.RULE) & (ch["item_id"].isin(keep))
               & ch["permutation_id"].notna()]
        w = g.pivot_table(index=["item_id", "permutation_id"], columns="condition",
                          values="chosen_option", aggfunc="first")
        w = w.loc[w.notna().all(axis=1)]
        it = w.index.get_level_values("item_id").values.astype(int)
        c4, c5 = w["cond4"].values, w["cond5"].values
        d = np.array([A[i][int(b)] - A[i][int(a)] for i, a, b in zip(it, c4, c5)])
        nz = d != 0
        n_eff, pos = int(nz.sum()), int((d[nz] > 0).sum())
        same = float((c4 == c5).mean())
        tie = float(1 - nz.mean())
        out[m] = {
            "same_option_rate": same, "tie_rate": tie,
            "blind_spot": tie - same,
            "n_eff": n_eff, "n_positive": pos,
            "sign_proportion": pos / n_eff if n_eff else float("nan"),
            "p_two_sided": binomtest(pos, n_eff, 0.5).pvalue if n_eff else float("nan"),
            "significant_at_corrected_alpha":
                bool(n_eff and binomtest(pos, n_eff, 0.5).pvalue < SP.ALPHA),
        }
    return out


def main():
    df, cols, A, ids, sets = TR.item_sets()
    ch = TR.load_choices()
    keep = set(int(i) for i in ids[sets["size_tile_confirmatory"]])
    k = inertness_floor()
    checks = [check_floor(j) for j in (k - 2, k - 1, k, k + 1)]
    half = [check_floor(k, both_permutations=False)]
    c5 = c5_delta_A(ch, A, keep)
    eff = json.load(open("results/T5_c5_effect.json"))["sets"]["size_tile_confirmatory"]

    rows = {}
    for m, R in P2D.P2D8_C5_REFERENCE.items():
        moved = eff[m]["n_items_with_a_changed_pair"]
        n_eff = int(round(N * (1 - c5[m]["tie_rate"])))
        rows[m] = {
            "c5_items_moved_of_108": moved,
            "inertness_floor_items": k,
            "floor_as_multiple_of_c5": k / moved,
            "c5_change_rate": 1 - R,
            "c5_tie_rate_analogue": c5[m]["tie_rate"],
            "n_eff_at_a_c5_like_tie_rate": n_eff,
            "sign_power_at": {str(p): SP.power(n_eff, p) for p in P_GRID},
            "p1_at_80_power": SP.detectable(n_eff),
        }

    out = {
        "purpose": "Arm B's detection limits under P2-D12: inertness against "
                   "zero at full n, c5 as context, sign test ungated. Replaces "
                   "the ceiling in results/T5_detection_ceiling.json, which "
                   "measured the superseded gated design and is kept because "
                   "PREREGISTRATION_v2.6.md section 3.3 reports it.",
        "n_confirmatory": N, "alpha": SP.ALPHA,
        "quantity_a_inertness": {
            "null": 0.0,
            "why_zero_is_the_null":
                "P2-D9: P1's chooser is an argmax over teacher-forced "
                "log-probabilities with no sampling, so an identical prompt "
                "returns an identical choice and a manipulation that changes no "
                "choice is inert exactly. No reference manipulation is needed to "
                "establish that, which is why the c5 comparison no longer gates.",
            "instrument": "P2-D8's cluster bootstrap, items, 10,000 resamples, "
                          "seed 20260910, at 1 - alpha, against 0 rather than R_m",
            "floor_items_of_108": k,
            "floor_share": k / N,
            "floor_checks_both_permutations_moving": checks,
            "floor_check_one_permutation_moving": half,
            "floor_is_a_count_not_a_rate":
                "The item-level mean of a resample is zero exactly when the "
                "resample contains no moving item, so the floor depends on how "
                "many items moved and not on how far. A mover that changes one "
                "of its two renderings counts the same as one that changes both.",
            "full_n": N,
        },
        "quantity_b_magnitude_context": {
            "role": "DESCRIPTIVE. Reported with the bootstrap half-width. Gates "
                    "nothing and spends no alpha.",
            "reference": P2D.P2D8_C5_REFERENCE,
            "half_width_range": list(P2D.P2D11_CEILING["half_width"]),
            "resolution_note":
                "A same-option-rate gap below roughly 0.15 is still unresolvable. "
                "Under P2-D12 that limits what the CONTEXT can say, not whether "
                "the movement half fires.",
        },
        "quantity_c_direction": {
            "instrument": "P2-D6 exact two-sided sign test, p0 = 0.5, unchanged",
            "effective_n": "108 * (1 - tie rate), with no lower bound imposed by "
                           "quantity (b). Under the superseded gate it was capped "
                           "at 32 to 58.",
            "tie_rate_is_not_knowable_before_T7": True,
            "c5_tie_rate_analogue_caveat":
                "c5's tie rate is a structurally matched manipulation's tie rate, "
                "not a measurement of F1's. Same caveat as reports/"
                "T5_sigma_prior.md section 0. It sizes nothing and is reported so "
                "the sign test's likely position is visible rather than assumed.",
        },
        "diagnostic_c5_direction": {
            "question": "Does a content-neutral insertion drift toward "
                        "o*_infinity, which is P1's salience pole? If it did, a "
                        "positive F1 sign test would be explicable without "
                        "adversary tracking.",
            "answer": "No. The sign proportion is at or below 0.5 on all seven "
                      "models, so p0 = 0.5 is conservative for detecting movement "
                      "toward o*_infinity.",
            "not_adopted_as_a_null":
                "P2-D6 fixes p0 = 0.5. Moving it to c5's proportion would "
                "recalibrate a preregistered test against a different "
                "manipulation. This is a reported diagnostic and nothing else.",
            "per_model": c5,
        },
        "diagnostic_blind_spot_measured": {
            "definition": "tie rate minus same-option rate on the c5 contrast, "
                          "which is P2-D10's gap measured on a real manipulation "
                          "rather than bounded from the geometry",
            "range": [min(v["blind_spot"] for v in c5.values()),
                      max(v["blind_spot"] for v in c5.values())],
            "per_model": {m: v["blind_spot"] for m, v in c5.items()},
        },
        "per_model": rows,
        "a_null_licenses":
            "That the framing changed the chosen option on fewer than "
            f"{k} of {N} items, which at this n is indistinguishable from a "
            "manipulation that changes nothing. Because the no-effect rate is "
            "exactly 1.0 and not estimated, this is a statement about the "
            "framing, not about measurement noise.",
        "a_null_does_not_license":
            "That models are insensitive to adversary structure. A framing can "
            "move choices without moving them toward o*_infinity, which is what "
            "quantity (c) separates, and quantity (c)'s power is set by the "
            "observed tie rate. It also does not license any claim about "
            "magnitude: quantity (b)'s resolution is roughly 0.15 on the "
            "same-option rate, so a framing that moves choices materially less "
            "than c5 does is not distinguishable from one that moves them as "
            "much. The A coordinate additionally cannot see a switch between two "
            "A-tied options, measured at 0.0000 to 0.0509 on the c5 contrast.",
    }
    # P2-D12 is the source; this script must reproduce it. A run that gated on
    # the c5 comparison, or that used a floor the log does not state, fails here.
    P2D.bind_armb_quantities(out["quantity_a_inertness"]["null"],
                             c5_gates=False, sign_p0=0.5,
                             quantities=P2D.P2D12_QUANTITIES)
    assert k == P2D.P2D12_INERTNESS_FLOOR_ITEMS, (
        f"P2-D12 states an inertness floor of {P2D.P2D12_INERTNESS_FLOOR_ITEMS} "
        f"items; this run gives {k}. docs/P2/DECISIONS.md is the source.")

    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)

    print(f"n = {N}, alpha = {SP.ALPHA:.6f}\n")
    print(f"(a) inertness floor: {k} of {N} items must carry a changed rendering")
    for c in checks + half:
        print(f"      k={c['k']:2d} item mean {c['item_mean']:.4f}  "
              f"lo {c['lo']:.6f}  {'clears 0' if c['clears_zero'] else 'does not'}")
    print(f"\n  {'model':6s} {'c5 moved':>9s} {'floor/c5':>9s} {'c5 tie':>7s} "
          f"{'n_eff':>6s} " + " ".join(f"p1={p:.2f}" for p in P_GRID) + "   p1@80%")
    for m, v in rows.items():
        print(f"  {m:6s} {v['c5_items_moved_of_108']:9d} "
              f"{v['floor_as_multiple_of_c5']:9.2f} "
              f"{v['c5_tie_rate_analogue']:7.4f} "
              f"{v['n_eff_at_a_c5_like_tie_rate']:6d} "
              + " ".join(f"{v['sign_power_at'][str(p)]:7.3f}" for p in P_GRID)
              + f"   {v['p1_at_80_power']}")
    print("\ndiagnostic: c5's own delta-A sign proportion (reported, not adopted as p0)")
    for m, v in c5.items():
        print(f"  {m:6s} n_eff={v['n_eff']:3d}  prop={v['sign_proportion']:.4f}  "
              f"p={v['p_two_sided']:.4f}  "
              f"{'below 0.5 at the corrected alpha' if v['significant_at_corrected_alpha'] else ''}")
    b = out["diagnostic_blind_spot_measured"]["range"]
    print(f"\ndiagnostic: P2-D10 blind spot on the c5 contrast, "
          f"{b[0]:.4f} to {b[1]:.4f}")
    print(f"\nwritten: {OUT}")
    return 0


def demo():
    """The floor must be the smallest `k` the real bootstrap accepts, and it must
    be far below what the superseded gate required. If it were not, P2-D12 would
    be restructuring the design for nothing."""
    k = inertness_floor()
    assert check_floor(k)["clears_zero"], f"floor {k} does not clear zero"
    assert not check_floor(k - 1)["clears_zero"], f"{k} is not the smallest"
    assert check_floor(k, both_permutations=False)["clears_zero"], \
        "the floor must not depend on how far a mover moves, only on how many moved"
    eff = json.load(open("results/T5_c5_effect.json"))["sets"]["size_tile_confirmatory"]
    worst = max(k / v["n_items_with_a_changed_pair"] for v in eff.values())
    gated = P2D.P2D11_CEILING["change_rate_multiple_of_c5"][0]
    assert worst < gated, (
        f"the inertness floor is {worst:.2f}x c5 at worst and the superseded gate "
        f"was {gated:.2f}x at best; P2-D12 buys nothing")
    print(f"ok: floor is {k} of {N} items, {worst:.2f}x c5 at worst, against the "
          f"superseded gate's {gated:.2f}x at best")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
