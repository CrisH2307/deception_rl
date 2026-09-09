"""Throughput benchmark for the T1 core over P1's frozen 200k candidate pool.

Run: python3 src/bench_adversary.py [n_per_tile]
"""
import sys
import time

import numpy as np

sys.path.insert(0, "src")
import adversary as adv  # noqa: E402
import p1  # noqa: E402

CHUNK = 5_000


def main(n=None):
    df = p1.load_items(p1.ITEMS_CANDIDATE)
    rows = []
    grand_n = grand_t = 0
    for tile in ("manmade", "moves", "hold", "size"):
        sub = df[df["tile"] == tile].reset_index(drop=True)
        if n:
            sub = sub.iloc[:n].reset_index(drop=True)
        t0 = time.perf_counter()
        out, peak = [], 0.0
        for b in adv.build_batch(sub, chunk=CHUNK):
            out.append(adv.beta_critical_batch(b))
            peak = max(peak, b.log_posterior.nbytes + b.fit.nbytes)
        bc = np.concatenate(out)
        dt = time.perf_counter() - t0
        grand_n += len(sub); grand_t += dt
        rows.append((tile, adv.tile_k(tile), len(sub), dt, len(sub) / dt,
                     peak / 2**20, float(np.isinf(bc).mean()),
                     float(np.median(bc[np.isfinite(bc)])) if np.isfinite(bc).any() else float("nan")))
    print(f"{'tile':8s} {'|O|':>3} {'items':>7} {'sec':>7} {'items/s':>9} "
          f"{'peak MiB':>9} {'robust':>8} {'median beta_c':>14}")
    for t, k, ni, dt, rate, mb, rob, med in rows:
        print(f"{t:8s} {k:>3} {ni:>7,} {dt:>7.2f} {rate:>9,.0f} {mb:>9.1f} "
              f"{100*rob:>7.1f}% {med:>14.4f}")
    print(f"{'TOTAL':8s} {'':>3} {grand_n:>7,} {grand_t:>7.2f} "
          f"{grand_n/grand_t:>9,.0f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else None))
