"""Power for Arm B's sign-based confirmatory instrument (P2-D6).

v2.0 section 8.2 sizes Arm B from `n = 15.05 * sigma^2 / delta^2`, which is the
power curve for a MEAN. P2-D6 makes the confirmatory instrument a tie rate plus a
sign test, so that curve no longer governs the primary analysis and this one does.

The change is not cosmetic. A sign test's power is an exact binomial function of
the effective sample size and the alternative proportion, and `sigma` enters
nowhere. What it needs instead is the TIE RATE, the share of items whose `ΔA` is
exactly zero, which is also unmeasured. One unknown is exchanged for another, and
the exchange is stated rather than presented as a saving:

  sigma       unbounded above, estimated with error, and the estimate itself
              needs data.
  tie rate    bounded in [0, 1], observed exactly once F1 or F2 is scored rather
              than estimated, and its effect on power is monotone.

The subtlety that matters most is in the other direction and is recorded here so
it is not discovered later: **a high tie rate is itself the outcome H-B predicts.**
Items where the model does not move contribute no sign, so the state of the world
in which the null is true is also the state in which the sign test has least
power. That is why the tie rate is reported as a primary quantity in its own
right rather than treated as attrition: "no movement" is answered by the tie rate
directly, and the sign test answers only "among items that moved, did they move
toward the adversary optimum".

Run: python3 src/sign_power.py          (writes results/T5_sign_power.json)
     python3 src/sign_power.py --demo   (self-check on the binomial power pair)
"""
import json
import os
import sys

import numpy as np
from scipy.stats import binom

ALPHA = 0.05 / 21          # v2.0 section 8.1, unchanged by P2-D6
N_CONFIRMATORY = 108       # v2.3 section 3 / P2-D4: size tile, finite beta_c
TIE_RATES = (0.0, 0.15, 0.30, 0.50, 0.70)
P_GRID = (0.55, 0.60, 0.65, 0.70, 0.75, 0.80)
OUT = "results/T5_sign_power.json"


def power(n_eff, p1, alpha=ALPHA):
    """Exact two-sided sign-test power against p0 = 0.5. No sigma enters."""
    if n_eff < 1:
        return 0.0
    lo = binom.ppf(alpha / 2, n_eff, 0.5)
    hi = binom.isf(alpha / 2, n_eff, 0.5)
    return float(binom.cdf(lo - 1, n_eff, p1) + binom.sf(hi, n_eff, p1))


def detectable(n_eff, target=0.80, alpha=ALPHA):
    """Smallest p1 > 0.5 reaching `target` power. None if unreachable."""
    for p in np.arange(0.501, 1.0, 0.001):
        if power(n_eff, float(p), alpha) >= target:
            return float(round(p, 3))
    return None


def main():
    rows = []
    for tr in TIE_RATES:
        n_eff = int(round(N_CONFIRMATORY * (1 - tr)))
        rows.append({
            "tie_rate": tr, "n_effective": n_eff,
            "power_at": {str(p): power(n_eff, p) for p in P_GRID},
            "detectable_p1_at_80_power": detectable(n_eff),
        })
    out = {
        "instrument": "P2-D6: tie rate reported directly, plus an exact two-sided "
                      "sign test against p0 = 0.5 on the items that moved",
        "alpha": ALPHA, "alpha_source": "v2.0 section 8.1, 21-test family, unchanged",
        "n_confirmatory_items": N_CONFIRMATORY,
        "n_source": "v2.3 section 3 / P2-D4: size tile of items_final.parquet, "
                    "finite beta_c",
        "sigma_enters": False,
        "sigma_note": "A sign test's power is exact-binomial in (n_eff, p1). "
                      "v2.0 section 8.2's n = 15.05 * sigma^2 / delta^2 sizes a "
                      "MEAN and no longer governs the confirmatory analysis. "
                      "sigma remains needed for the mean, which P2-D6 keeps as a "
                      "reported descriptive quantity.",
        "unknown_exchanged": "sigma for the tie rate. The tie rate is bounded in "
                             "[0, 1], observed exactly rather than estimated, and "
                             "monotone in its effect on power. It is not knowable "
                             "before F1 or F2 is scored.",
        "power_is_lowest_where_the_null_is_true":
            "A high tie rate is the outcome H-B predicts, and ties carry no sign, "
            "so the sign test has least power exactly where the null holds. This "
            "is why the tie rate is a primary reported quantity and not attrition: "
            "'no movement' is answered by the tie rate, and the sign test answers "
            "only 'among items that moved, did they move toward the adversary "
            "optimum'.",
        "sesoi": "NOT SET. D74's delta = 0.05 is a SESOI on mean ΔA and does not "
                 "translate to a proportion without a distributional assumption. "
                 "None is invented here. The confirmatory test is against "
                 "p0 = 0.5, which is well posed with no SESOI; the SESOI would "
                 "enter only for power, and realized power is reported at the "
                 "observed n_eff instead.",
        "rows": rows,
    }
    os.makedirs("results", exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=2)
    print(f"alpha = {ALPHA:.6f} two-sided, n = {N_CONFIRMATORY}, sigma-free\n")
    print(f"{'tie rate':>9s} {'n_eff':>6s} " + " ".join(f"p1={p:.2f}" for p in P_GRID)
          + "   p1 at 80% power")
    for r in rows:
        print(f"{r['tie_rate']:9.0%} {r['n_effective']:6d} "
              + " ".join(f"{r['power_at'][str(p)]:7.3f}" for p in P_GRID)
              + f"   {r['detectable_p1_at_80_power']}")
    print(f"\nwritten: {OUT}")
    return 0


def demo():
    """Power and its inverse must agree, and the null must sit at alpha."""
    for n in (108, 76, 54):
        p = detectable(n)
        assert power(n, p) >= 0.80, f"detectable({n}) = {p} does not reach 0.80"
        assert power(n, p - 0.002) < 0.80, f"detectable({n}) is not the smallest"
        assert power(n, 0.5) <= ALPHA + 1e-12, \
            f"size at p0 = 0.5 is {power(n, 0.5):.6f}, above alpha {ALPHA:.6f}"
        assert power(n, 0.99) > power(n, 0.7) > power(n, 0.55), "power not monotone"
    assert power(0, 0.9) == 0.0, "zero effective n must give zero power"
    print("ok: power/inverse agree, size <= alpha at p0 = 0.5, monotone in p1, "
          "n_eff = 0 gives zero power")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else main())
