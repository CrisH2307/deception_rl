"""The adversary game: V_beta, best response, beta_c, divergence set, margin.

Implements the function contracts of `docs/spec/adversary-game-v1.md` section 9
(spec v3). Everything is computed in log space over float64, vectorised over
items; the section 9 scalar contracts are thin wrappers on the batch core, so
there is one implementation of each quantity, not two.

The listener posterior is P1's, imported through `p1.fit_grid`:

    L(h|o) = [f(o,h) / sum_o' f(o',h)] / sum_h' [f(o,h') / sum_o' f(o',h')]

`f(o,h)` is not a likelihood until it is normalised over `o`; the inner
normalisation is what makes Bayes well-posed (spec v3 section 2).

Run: python3 src/adversary.py     (self-check on the frozen P1 item set)
"""
import math
import os
import sys
from dataclasses import dataclass

import numpy as np
from scipy.special import logsumexp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1  # noqa: E402
from p1 import lex_obayes, TAU_MAIN  # noqa: E402  (P1's frozen D51 tie-break)

EPS_BETA = 1e-9    # spec section 8.2, bisection tolerance on beta
EPS_TIE = 1e-12    # spec section 8.2, absolute tie tolerance
BETA_GRID = (0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0)   # spec section 8.2


# --------------------------------------------------------------------- batch
@dataclass
class ItemBatch:
    """`n` items sharing one tile, in the form every function below needs.

    log_posterior : (n, |H|, |O|)  log L(h|o), normalised over h
    h_star        : (n,)           flat index of h* in H (h = m * C + c)
    fit           : (n, |H|, |O|)  f(o, h), kept for the tie-break rule
    item_id       : (n,)
    """
    tile: str
    log_posterior: np.ndarray
    h_star: np.ndarray
    fit: np.ndarray
    item_id: np.ndarray

    def __len__(self):
        return len(self.h_star)

    @property
    def n_options(self):
        return self.log_posterior.shape[2]

    @property
    def rows(self):
        return np.arange(len(self))

    @property
    def log_l_star(self):
        """(n, |O|) log L(h*|o)."""
        return self.log_posterior[self.rows, self.h_star, :]

    @property
    def fit_star(self):
        """(n, |O|) f(o, h*), the second key of the tie-break."""
        return self.fit[self.rows, self.h_star, :]

    @property
    def _log_rivals(self):
        """(n, |H|, |O|) log L(h|o) with h* masked out."""
        m = self.log_posterior.copy()
        m[self.rows, self.h_star, :] = -np.inf
        return m

    @property
    def log_m(self):
        """(n, |O|) log M(o) = max_{h != h*} log L(h|o)."""
        return self._log_rivals.max(axis=1)


def build_batch(df, chunk=None):
    """ItemBatch (or a generator of them, if `chunk` is set) from a P1 item table.

    The table must be single-tile; call once per tile. Rows keep their order, so
    `item_id` lines up with the input frame.
    """
    tile = df["tile"].iloc[0]
    if (df["tile"] != tile).any():
        raise ValueError("build_batch takes one tile at a time; |O| differs across tiles")
    if chunk is None:
        return _build(df, tile)
    return (_build(df.iloc[s:s + chunk], tile) for s in range(0, len(df), chunk))


def _build(df, tile):
    means = np.stack(df["means"].values).astype(int)
    clues = np.stack(df["clues"].values).astype(int)
    G = p1.fit_grid(tile, means, clues)                   # (n, |H|, |O|) f(o,h)
    if not (G > 0).all():
        raise AssertionError(                             # spec test 7, P1's D29
            f"{int((G <= 0).sum())} non-positive fits. Exponential fit is "
            "strictly positive, so this is a bug, not a case to patch.")
    log_f = np.log(G)
    log_lik = log_f - logsumexp(log_f, axis=2, keepdims=True)      # P(o|h)
    log_post = log_lik - logsumexp(log_lik, axis=1, keepdims=True)  # P(h|o)
    C = clues.shape[1]
    h_star = (df["target_means_pos"].values.astype(int) * C
              + df["target_clue_pos"].values.astype(int))
    return ItemBatch(tile, log_post, h_star, G, df["item_id"].values)


# ------------------------------------------------------------------ the game
def log_v_beta(batch, beta, tau=1.0):
    """(n, |O|) log V_beta(o), the adversary-worst-case correct-accusation
    log-probability. `beta = inf` returns -inf (V_inf = 0 exactly); use
    `optimal_option` for the limiting argmax, which is argmax margin."""
    _check(beta, tau)
    if beta == math.inf:
        return np.full(batch.log_l_star.shape, -np.inf)
    c = batch.log_l_star / tau                                    # log C_o
    b = batch.log_m / tau                                         # log B_o
    z = logsumexp(batch.log_posterior / tau, axis=1)               # log Z_tau
    # log A_o = log(Z_tau - M^{1/tau}); the sum over the 99 non-decoy
    # hypotheses, each strictly positive, so A_o > 0 and log1p is well posed.
    with np.errstate(divide="ignore"):
        log_a = z + np.log1p(-np.exp(np.minimum(b - z, 0.0)))
    if not np.isfinite(log_a).all():
        raise AssertionError(
            f"{int((~np.isfinite(log_a)).sum())} degenerate A_o (a single rival "
            "holds all posterior mass to float64 precision). Surfaced, not clipped.")
    return c - np.logaddexp(log_a, b + beta / tau)


def margin_batch(batch):
    """(n, |O|) margin(o) = log L(h*|o) - max_{h != h*} log L(h|o)."""
    return batch.log_l_star - batch.log_m


def best_response_batch(batch):
    """(n, |O|) d*(o) = argmax_{h != h*} L(h|o), as flat hypothesis ids.

    Independent of beta and tau by R1. Ties broken by max f(o,h) among the tied
    hypotheses, then by hypothesis index h = m * C + c (spec section 6.2).

    Exact ties among rivals are common on the low-|O| tiles (28% of
    option-cells in the frozen set reach the index level, tie sets up to 24),
    because distinct concept pairs falling in the same bins have bit-identical
    fit vectors. The tie set is resolved deterministically by the item's own
    frozen means/clues order, and every downstream quantity depends on the tied
    hypotheses only through M(o) = L(d*|o), which is identical across the set.
    """
    lg = np.exp(batch._log_rivals)                                # (n,|H|,|O|)
    tied = lg >= lg.max(axis=1, keepdims=True) - EPS_TIE          # eps_tie is
    return np.where(tied, batch.fit, -np.inf).argmax(axis=1)      # absolute on L


def _select(score, fit_star):
    """P1's frozen D51 lexicographic argmax, applied to `score` (n, |O|).

    `score` is rescaled to a max of exactly 1 per row before the call. D51's
    tolerance is relative, so this is an exact reformulation, not a clamp; it is
    what keeps the comparison meaningful once exp(-beta/tau) has driven every
    option's absolute V_beta toward zero at large beta.
    """
    rel = np.exp(score - score.max(axis=1, keepdims=True))
    return lex_obayes(rel, fit_star, TAU_MAIN)[0]


def optimal_option(batch, beta, tau=1.0):
    """(n,) argmax_o V_beta(o) under the spec's tie-break.

    At `beta = inf` this is argmax_o margin(o) (spec section 5.2), reached by a
    separate code path, never by a large finite beta.
    """
    _check(beta, tau)
    score = margin_batch(batch) / tau if beta == math.inf else log_v_beta(batch, beta, tau)
    return _select(score, batch.fit_star)


def _abc(batch, tau):
    """(A_o, B_o, C_o) of spec section 6.3, rescaled per row by 1/max_o C_o.

    V_beta(o) = C_o / (A_o + B_o x) with x = exp(beta/tau); the crossing
    equation is homogeneous in a common row scale, so rescaling C leaves every
    root unchanged and keeps the arithmetic away from underflow at small tau.
    """
    c = np.exp(batch.log_l_star / tau - (batch.log_l_star / tau).max(axis=1, keepdims=True))
    z = np.exp(logsumexp(batch.log_posterior / tau, axis=1))
    b = np.exp(batch.log_m / tau)
    return z - b, b, c


def _crossings(batch, tau):
    """(n, |O|) the x >= 1 at which each rival overtakes o*_0, else inf.

    Closed form of spec section 6.3: the pairwise equality is linear in
    x = exp(beta/tau), so each rival has at most one root.
    """
    a, b, c = _abc(batch, tau)
    o0 = optimal_option(batch, 0.0, tau)
    r = batch.rows
    a0, b0, c0 = a[r, o0, None], b[r, o0, None], c[r, o0, None]
    num = c * a0 - c0 * a
    den = c0 * b - c * b0
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.where(den != 0, num / den, np.inf)
    x[r, o0] = np.inf                                   # o*_0 never overtakes itself
    return np.where(np.isfinite(x) & (x >= 1.0), x, np.inf)


def beta_critical_batch(batch, tau=1.0):
    """(n,) beta_c, by bisection to EPS_BETA. inf for adversary-robust items.

    Robustness and the bracket come from the closed form of section 6.3 (exact,
    and it settles margin ties that the beta -> inf argmax alone would miss);
    the returned value is bisected on the monotone indicator, per T1. The two
    are cross-checked in `tests/test_adversary.py`.
    """
    _check(0.0, tau)
    x = _crossings(batch, tau).min(axis=1)
    beta_c = np.where(np.isfinite(x), tau * np.log(x), np.inf)
    live = np.isfinite(beta_c)
    if not live.any():
        return beta_c

    o0 = optimal_option(batch, 0.0, tau)

    def diverged(bet):
        lv = log_v_beta(batch, 0.0, tau) if np.all(bet == 0) else _lv_at(batch, bet, tau)
        best = lv[batch.rows, o0].copy()
        lv = lv.copy()
        lv[batch.rows, o0] = -np.inf
        return lv.max(axis=1) > best

    lo = np.zeros(len(batch))
    hi = np.maximum(beta_c * 2.0, 1.0)                  # closed-form bracket
    hi = np.where(live, hi, 1.0)
    for _ in range(64):
        need = live & ~diverged(hi)
        if not need.any():
            break
        hi = np.where(need, hi * 2.0, hi)
    else:
        raise AssertionError("bisection bracket did not close in 64 doublings")

    span = np.where(live, hi, 0.0)
    for _ in range(int(np.ceil(np.log2(max(span.max(), 1.0) / EPS_BETA))) + 2):
        mid = 0.5 * (lo + hi)
        d = diverged(mid)
        hi = np.where(live & d, mid, hi)
        lo = np.where(live & ~d, mid, lo)
    return np.where(live, hi, np.inf)


def _lv_at(batch, beta_vec, tau):
    """log V_beta with a per-item beta (bisection carries one beta per item)."""
    c = batch.log_l_star / tau
    b = batch.log_m / tau
    z = logsumexp(batch.log_posterior / tau, axis=1)
    with np.errstate(divide="ignore"):
        log_a = z + np.log1p(-np.exp(np.minimum(b - z, 0.0)))
    return c - np.logaddexp(log_a, b + beta_vec[:, None] / tau)


def _check(beta, tau):
    if beta < 0:
        raise ValueError(f"beta must be >= 0, got {beta}")
    if tau <= 0:
        raise ValueError(f"tau must be > 0, got {tau}")


# ------------------------------------------- section 9 contracts (scalar API)
def _one(item):
    """An ItemBatch of length 1 from a single item record (a pandas row / dict)."""
    import pandas as pd
    return build_batch(pd.DataFrame([dict(item)]))


def v_beta(item, o, beta, tau=1.0):
    """Scientist utility V_beta(o) for one item and option (spec sections 3, 5).

    Returns a probability in [0, 1]; 0.0 at beta = inf, which is the exact
    limit, not a truncation. The limiting *argmax* is argmax margin, not the
    argmax of this value; see `optimal_option`.
    """
    return float(np.exp(log_v_beta(_one(item), beta, tau)[0, o]))


def adversary_best_response(item, o):
    """d*(o) = argmax_{h != h*} L(h|o) (spec section 4, R1). Takes no beta/tau."""
    return int(best_response_batch(_one(item))[0, o])


def beta_critical(item, tau=1.0):
    """beta_c(i) (spec section 6.1). math.inf for adversary-robust items."""
    return float(beta_critical_batch(_one(item), tau)[0])


def divergence_set(items, beta, tau=1.0):
    """D(beta) = { i : beta_c(i) <= beta } (spec section 7).

    Empty at beta == 0 unconditionally (spec section 7.1): a boundary-tied item
    may have beta_c == 0 and is still excluded, because o*_0 is the argmax at
    beta = 0 for every item by the tie-break rule.
    """
    if beta == 0:
        return []
    import pandas as pd
    df = items if isinstance(items, pd.DataFrame) else pd.DataFrame(list(items))
    out = []
    for tile, sub in df.groupby("tile", sort=False):
        b = build_batch(sub.reset_index(drop=True))
        out.extend(np.asarray(b.item_id)[beta_critical_batch(b, tau) <= beta + EPS_BETA])
    return out


def margin(item, o):
    """margin(o) = log L(h*|o) - max_{h != h*} log L(h|o) (spec section 5.2)."""
    return float(margin_batch(_one(item))[0, o])


def main():
    df = p1.load_items()
    bad = 0
    for tile, sub in df.groupby("tile", sort=False):
        sub = sub.reset_index(drop=True)
        b = build_batch(sub)
        bad += int((optimal_option(b, 0.0) != sub["o_bayes"].values).sum())
    print(f"beta=0 vs frozen P1 o_bayes: {bad} disagreements over {len(df)} items")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
