"""P2-D3 and P2-D4 are tripwires, not comments. Test that they fire.

Separate file from `tests/test_framings.py`, which is T3's and governs P2-D1 and
P2-D2. `dec.check_log` covers all four decisions and is already asserted there;
what is new here is the Arm B bind's negative case and the one number P2-D4
states, which is checkable against the frozen artifact rather than trusted.

Run: python3 tests/test_armb_binding.py
"""
import sys

import numpy as np

sys.path.insert(0, "src")

import adversary as adv  # noqa: E402
import p1  # noqa: E402
import p2_decisions as dec  # noqa: E402


def test_bind_armb_accepts_the_governed_values():
    """The decision as adopted: `size` tile, P1's frozen items, not pooled."""
    dec.bind_armb(dec.P2D3_TILE, p1.artifact_hash(p1.ITEMS_FINAL), pooled=False)


def test_bind_armb_rejects_drift():
    """Perturb each governed value in turn; the check must fail on every one.

    The pooled case is the one that matters most: P2-D3 rejected pooling on
    D108, and a later session that pools for the extra `n` is exactly the drift
    this bind exists to stop.
    """
    good_hash = p1.artifact_hash(p1.ITEMS_FINAL)
    drifted = [
        ("pooled", ("size", good_hash, True)),
        ("tile", ("manmade", good_hash, False)),
        ("tile", ("moves", good_hash, False)),
        ("tile", ("", good_hash, False)),
        ("item file", ("size", "0" * 64, False)),
        ("item file", ("size", good_hash[:-1] + "0", False)),
    ]
    for what, args in drifted:
        try:
            dec.bind_armb(*args)
        except AssertionError:
            continue
        raise AssertionError(f"bind_armb accepted a drifted {what}: {args}")


def test_confirmatory_n_matches_the_frozen_artifact():
    """P2-D4 states n = 108. Recompute it rather than trusting the number.

    A decision that names a count and a hash but never checks the count against
    the artifact the hash pins is half a binding: the hash would still match
    after a change to what `finite beta_c` means.
    """
    df = p1.load_items(tile=dec.P2D3_TILE)
    bc = adv.beta_critical_batch(adv.build_batch(df))
    n = int(np.isfinite(bc).sum())
    assert n == dec.P2D4_N_CONFIRMATORY, (
        f"P2-D4 states n = {dec.P2D4_N_CONFIRMATORY} `size`-tile items with "
        f"finite beta_c; the frozen artifact gives {n}. The log is the source: "
        "fix whichever drifted, do not edit the constant to pass.")
    assert len(df) == 250, len(df)


def test_sigma_ceiling_the_adopted_set_covers():
    """The limitation PREREGISTRATION_v2.3 section 3.3 states, recomputed.

    n = 15.05 * sigma^2 / delta^2 at delta = 0.05 gives n = 6020 * sigma^2, so
    108 items cover sigma <= 0.134 and section 8.2's 400 covers sigma <= 0.25.
    Asserted so the stated limitation cannot drift from the arithmetic behind it.
    """
    n_coef = (3.038 + 0.842) ** 2 / 0.05 ** 2
    assert abs(n_coef - 6020) < 20, n_coef
    assert abs((dec.P2D4_N_CONFIRMATORY / n_coef) ** 0.5 - 0.134) < 0.001
    assert abs((377 / n_coef) ** 0.5 - 0.250) < 0.001


def test_p2d6_rejects_a_mean_based_confirmatory_claim():
    """P2-D6 demotes mean `ΔA`. A run that puts a confirmatory claim on it must
    fail at the binding, not in the results table."""
    dec.bind_armb_statistic("sign", dec.P2D6_ALPHA, dec.P2D6_P0, False)
    dec.bind_armb_statistic("tie_rate", dec.P2D6_ALPHA, dec.P2D6_P0, False)
    for bad in ("mean", "mean_delta_A", "value_from_means"):
        try:
            dec.bind_armb_statistic(bad, dec.P2D6_ALPHA, dec.P2D6_P0, False)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"P2-D6 accepted {bad!r} as confirmatory")
    for kwargs in ((0.05, dec.P2D6_P0, False),          # alpha drift
                   (dec.P2D6_ALPHA, 0.6, False),        # sign-test null drift
                   (dec.P2D6_ALPHA, dec.P2D6_P0, True)):  # mean promoted back
        try:
            dec.bind_armb_statistic("sign", *kwargs)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"P2-D6 accepted drift {kwargs}")


def test_sign_power_is_sigma_free_and_matches_the_prereg():
    """P2-D6's power curve must not depend on `sigma`, and the figures quoted in
    PREREGISTRATION_v2.4 section 3.2 must come from the script that emits them."""
    import sign_power as sp
    assert sp.ALPHA == dec.P2D6_ALPHA, "sign_power alpha drifted from P2-D6"
    assert sp.N_CONFIRMATORY == dec.P2D4_N_CONFIRMATORY, "n drifted from P2-D4"
    # the three figures the preregistration quotes, recomputed here
    for n_eff, p1, want in ((108, 0.70, 0.858), (76, 0.70, 0.670), (54, 0.75, 0.740)):
        got = sp.power(n_eff, p1)
        assert abs(got - want) < 5e-4, f"power({n_eff}, {p1}) = {got:.4f}, prereg says {want}"
    assert sp.detectable(108) == 0.691, "detectable p1 at n=108 drifted"


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"ok  {name}")
            except AssertionError as e:
                fails += 1
                print(f"FAIL {name}\n     {e}")
    sys.exit(1 if fails else 0)
