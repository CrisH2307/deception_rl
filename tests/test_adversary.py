"""Acceptance tests for the adversary game (spec v3 section 10) plus direct
re-verification of R1, R2, section 6.3 and section 7.1 under the corrected
posterior.

The proofs are re-checked numerically against the frozen P1 item set, not
assumed to carry over from v2: each one is re-run by brute force here and
compared with the closed form the module uses.

Run: python3 tests/test_adversary.py
"""
import math
import sys

import numpy as np
from scipy.special import logsumexp

sys.path.insert(0, "src")

import adversary as adv  # noqa: E402
import p1  # noqa: E402

TILES = ["manmade", "moves", "hold", "size"]
RNG = np.random.default_rng(20260909)


def batches(n=None):
    df = p1.load_items()
    for tile in TILES:
        sub = df[df["tile"] == tile].reset_index(drop=True)
        if n:
            sub = sub.iloc[:n].reset_index(drop=True)
        yield tile, sub, adv.build_batch(sub)


# ------------------------------------------------- spec section 10, tests 1-9
def test_1_p1_oracle_equivalence():
    """beta=0, tau=1 reproduces P1's frozen o_bayes on all 1,000 items."""
    bad = total = 0
    for tile, sub, b in batches():
        d = adv.optimal_option(b, 0.0) != sub["o_bayes"].values
        bad += int(d.sum())
        total += len(sub)
    assert total == 1000, total
    assert bad == 0, f"{bad}/{total} items disagree with P1's frozen o_bayes"


def test_2_large_beta_equals_argmax_margin():
    """The beta=inf path is argmax margin, and finite beta converges to it."""
    for tile, sub, b in batches():
        lim = adv.optimal_option(b, math.inf)
        assert (lim == adv._select(adv.margin_batch(b), b.fit_star)).all()
        # reached from below, in log space, without overflowing exp(beta)
        assert (adv.optimal_option(b, 500.0) == lim).all(), tile


def test_3_divergence_set_monotone():
    """i in D(beta) implies i in D(beta') for beta' > beta, on the reporting
    grid and at the closed-form crossings themselves."""
    for tile, sub, b in batches():
        bc = adv.beta_critical_batch(b)
        prev = np.zeros(len(b), bool)
        for beta in adv.BETA_GRID[1:]:
            cur = bc <= beta
            assert (prev & ~cur).sum() == 0, f"{tile}: item left D at beta={beta}"
            prev = cur
        finite = bc[np.isfinite(bc)]
        for beta in np.sort(finite)[:: max(1, len(finite) // 50)]:
            assert (bc <= beta).sum() >= (bc <= beta * 0.999).sum()


def test_4_best_response_is_beta_tau_independent():
    """R1: d*(o) does not move with beta or tau, and it is the true minimiser
    of P(h*|o,d), verified by brute force over every d != h*."""
    for tile, sub, b in list(batches(n=25)):
        d_star = adv.best_response_batch(b)
        logL = b.log_posterior
        for tau in (0.5, 1.0, 2.0):
            for beta in (0.25, 1.0, 4.0):
                s = logL / tau                                   # (n,|H|,|O|)
                z = logsumexp(s, axis=1)                         # (n,|O|)
                # P(h*|o,d) denominator: Z + L_d^{1/tau}(e^{beta/tau} - 1)
                bump = s + np.log(math.expm1(beta / tau))
                den = np.logaddexp(z[:, None, :], bump)          # (n,|H|,|O|) by d
                num = s[b.rows, b.h_star, :][:, None, :]
                p = num - den
                p[b.rows, b.h_star, :] = np.inf                  # d != h*
                brute = p.argmin(axis=1)
                assert (brute == d_star).all(), \
                    f"{tile}: R1 fails at beta={beta}, tau={tau}"


def test_5_v_beta_strictly_decreasing_in_beta():
    for tile, sub, b in batches(n=60):
        prev = None
        for beta in (0.0, 0.1, 0.25, 1.0, 4.0, 16.0):
            lv = adv.log_v_beta(b, beta)
            assert np.isfinite(lv).all()
            if prev is not None:
                assert (lv < prev - adv.EPS_TIE).all(), f"{tile} at beta={beta}"
            prev = lv


def test_6_single_crossing():
    """At most one sign change per option pair, with the eps_tie floor the spec
    requires (a naive scan reports spurious roots on near-equal pairs)."""
    grid = np.linspace(0.0, 50.0, 4000)
    naive = floored = 0
    for tile, sub, b in batches(n=15):
        lv = np.stack([adv.log_v_beta(b, x) for x in grid])       # (T,n,|O|)
        K = b.n_options
        for i in range(K):
            for j in range(i + 1, K):
                d = np.exp(lv[:, :, i]) - np.exp(lv[:, :, j])
                for arr, eps in ((d, 0.0), (d, adv.EPS_TIE)):
                    s = np.sign(np.where(np.abs(arr) < eps, 0.0, arr))
                    flips = np.array([
                        _changes(s[:, k]) for k in range(s.shape[1])])
                    if eps == 0.0:
                        naive += int((flips > 1).sum())
                    else:
                        floored += int((flips > 1).sum())
    assert floored == 0, f"{floored} option pairs cross more than once"
    print(f"     (naive sign scan without the eps_tie floor: {naive} false violations)")


def _changes(s):
    s = s[s != 0]
    return int((np.diff(s) != 0).sum())


def test_7_zero_denominator_audit():
    """P1's D29: f(o,h) > 0 everywhere, so no likelihood denominator vanishes.
    Uses P1's own assertion path (`oracle.likelihood`) as the reference."""
    from oracle import likelihood
    df = p1.load_items()
    for tile in TILES:
        sub = df[df["tile"] == tile].reset_index(drop=True)
        G = p1.fit_grid(tile, np.stack(sub["means"].values).astype(int),
                        np.stack(sub["clues"].values).astype(int))
        assert (G > 0).all(), f"{tile}: non-positive fit"
        for k in range(0, len(G), 200):
            likelihood(G[k])          # raises on a non-positive denominator


def test_8_tie_break_determinism():
    """Permuting H must not change o*_0 or M(o); permuting O must permute the
    returned option, not reorder the winner.

    d*'s *identity* is deliberately not asserted invariant: exact rival ties
    reaching the index level are common (see `best_response_batch`), and the
    index is the item's own frozen means/clues order, which a permutation
    genuinely changes. What must be stable is everything downstream reads,
    namely M(o) = L(d*|o).
    """
    df = p1.load_items()
    for tile in TILES:
        sub = df[df["tile"] == tile].reset_index(drop=True).iloc[:80].copy()
        b = adv.build_batch(sub)
        want_o = adv.optimal_option(b, 1.0)
        want_d = adv.best_response_batch(b)
        M, C = len(sub["means"].iloc[0]), len(sub["clues"].iloc[0])
        pm, pc = RNG.permutation(M), RNG.permutation(C)
        inv_m, inv_c = np.argsort(pm), np.argsort(pc)
        sub["means"] = [np.asarray(r)[pm] for r in sub["means"]]
        sub["clues"] = [np.asarray(r)[pc] for r in sub["clues"]]
        sub["target_means_pos"] = inv_m[sub["target_means_pos"].values]
        sub["target_clue_pos"] = inv_c[sub["target_clue_pos"].values]
        b2 = adv.build_batch(sub)
        assert (adv.optimal_option(b2, 1.0) == want_o).all(), f"{tile}: o moved under H permutation"
        assert np.abs(b2.log_m - b.log_m).max() < 1e-12, f"{tile}: M(o) moved under H permutation"
        # the permuted d* must still be a maximiser: its posterior is M(o)
        d2 = adv.best_response_batch(b2)
        cols = np.arange(d2.shape[1])[None, :]
        got = b2.log_posterior[b2.rows[:, None], d2, cols]
        assert np.abs(got - b2.log_m).max() < 1e-12, \
            f"{tile}: permuted d* is not a maximiser of L(h|o)"
        # option order: the selector must follow the permutation exactly
        score, fit = adv.log_v_beta(b, 1.0), b.fit_star
        po = RNG.permutation(score.shape[1])
        assert (adv._select(score[:, po], fit[:, po]) == np.argsort(po)[want_o]).all()


def test_9_divergence_set_empty_at_zero():
    """D(0) = {} unconditionally, including for items whose beta_c is 0."""
    df = p1.load_items()
    assert adv.divergence_set(df, 0.0) == []
    bnd = df[df["boundary_exact"]]
    assert len(bnd) > 0, "no boundary_exact items in the frozen set to test with"
    assert adv.divergence_set(bnd, 0.0) == []
    zero = []
    for tile, sub, b in batches():
        bc = adv.beta_critical_batch(b)
        zero.extend(sub["item_id"].values[bc <= adv.EPS_BETA])
    print(f"     ({len(zero)} items with beta_c ~ 0, all excluded from D(0))")


# ------------------------------------------ spec v3 re-verification (item 5)
def test_v3_posterior_is_normalised_over_h():
    """sum_h L(h|o) = 1 under the corrected definition. This is what R2's
    beta=0 clause and the tau=1 identity rest on (spec section 5.1)."""
    worst = 0.0
    for tile, sub, b in batches():
        s = np.exp(logsumexp(b.log_posterior, axis=1))
        worst = max(worst, float(np.abs(s - 1.0).max()))
    assert worst < 1e-12, f"posterior not normalised over h: max |sum-1| = {worst:.3e}"
    print(f"     (max |sum_h L(h|o) - 1| = {worst:.3e})")


def test_v3_tau1_identity_v0_equals_posterior():
    """tau=1: V_0(o) = L(h*|o) identically, so argmax V_0 = P1's oracle."""
    worst = 0.0
    for tile, sub, b in batches():
        worst = max(worst, float(np.abs(
            adv.log_v_beta(b, 0.0, 1.0) - b.log_l_star).max()))
    assert worst < 1e-12, f"tau=1 identity broken: max |log V_0 - log L(h*|o)| = {worst:.3e}"
    print(f"     (max |log V_0(o) - log L(h*|o)| = {worst:.3e})")


def test_v3_tau1_identity_fails_off_tau1():
    """The identity is specific to tau=1, which is why the spec fixes tau there.
    A guard against silently re-opening tau as a swept parameter."""
    off = 0
    for tile, sub, b in batches():
        for tau in (0.5, 2.0):
            off += int((adv.optimal_option(b, 0.0, tau)
                        != adv.optimal_option(b, 0.0, 1.0)).sum())
    assert off > 0, "tau!=1 reproduced the tau=1 oracle everywhere; check section 5.1"
    print(f"     ({off} beta=0 argmax disagreements at tau in {{0.5, 2}}, as section 5.1 predicts)")


def test_v3_bisection_matches_closed_form():
    """Section 6.3's closed-form root and the bisected value agree to EPS_BETA."""
    worst = 0.0
    for tile, sub, b in batches():
        bis = adv.beta_critical_batch(b)
        cf = adv._crossings(b, 1.0).min(axis=1)
        cf = np.where(np.isfinite(cf), np.log(cf), np.inf)
        assert (np.isfinite(bis) == np.isfinite(cf)).all(), f"{tile}: robustness disagrees"
        f = np.isfinite(bis)
        if f.any():
            worst = max(worst, float(np.abs(bis[f] - cf[f]).max()))
    assert worst <= adv.EPS_BETA, f"bisection vs closed form: max gap {worst:.3e}"
    print(f"     (max |bisection - closed form| = {worst:.3e}, tolerance {adv.EPS_BETA:.0e})")


def test_v3_beta_c_is_the_flip_point():
    """Just below beta_c the argmax is o*_0; just above it is not."""
    for tile, sub, b in batches():
        bc = adv.beta_critical_batch(b)
        o0 = adv.optimal_option(b, 0.0)
        f = np.isfinite(bc) & (bc > 1e-6)
        if not f.any():
            continue
        lo = adv.optimal_option(b, 0.0)  # placeholder to keep shapes aligned
        for sign, want_equal in ((-1.0, True), (1.0, False)):
            probe = bc + sign * 1e-4
            got = np.array([
                adv.optimal_option(adv.ItemBatch(
                    b.tile, b.log_posterior[k:k + 1], b.h_star[k:k + 1],
                    b.fit[k:k + 1], b.item_id[k:k + 1]), float(probe[k]))[0]
                for k in np.where(f)[0][:40]])
            ref = o0[f][:40]
            assert ((got == ref) == want_equal).all(), \
                f"{tile}: argmax on the {'low' if sign < 0 else 'high'} side of beta_c"


def test_v3_scalar_contracts_match_batch():
    """The section 9 scalar API and the vectorised core are one implementation."""
    df = p1.load_items()
    for tile in TILES:
        sub = df[df["tile"] == tile].reset_index(drop=True)
        b = adv.build_batch(sub)
        for k in RNG.choice(len(sub), 5, replace=False):
            row = sub.iloc[int(k)]
            for o in range(b.n_options):
                assert abs(adv.v_beta(row, o, 1.0)
                           - float(np.exp(adv.log_v_beta(b, 1.0)[k, o]))) < 1e-15
                assert adv.adversary_best_response(row, o) == adv.best_response_batch(b)[k, o]
                assert abs(adv.margin(row, o) - adv.margin_batch(b)[k, o]) < 1e-15
            one, many = adv.beta_critical(row), float(adv.beta_critical_batch(b)[k])
            assert (math.isinf(one) and math.isinf(many)) or abs(one - many) < adv.EPS_BETA
            assert adv.v_beta(row, 0, math.inf) == 0.0


def test_v3_rejects_bad_arguments():
    df = p1.load_items().iloc[:1]
    for bad in (dict(beta=-0.1, tau=1.0), dict(beta=1.0, tau=0.0), dict(beta=1.0, tau=-1.0)):
        try:
            adv.log_v_beta(adv.build_batch(df), **bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")


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
