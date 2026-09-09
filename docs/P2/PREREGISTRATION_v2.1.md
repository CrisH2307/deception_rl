# PREREGISTRATION v2.1

**Paper 2: the adversary effect and the RL Scientist**

Version 2.1 · written 2026-09-09 · amends `PREREGISTRATION_v2.md` (v2.0).

Written as a separate file per Paper 1's **D148**: v2.0 is never edited in place, and
the two are read together. This amendment **changes no kill criterion, no threshold,
no hypothesis and no analysis rule.** It is a disclosure of ordering, plus two
documentation corrections. If it appears to conflict with v2.0, v2.0's rules stand
and this file is the record of why they were left alone.

---

## 1. Disclosure: K1's statistic was computed as a byproduct of T1

T1's benchmark, run on 2026-09-09, computed K1's gate statistic over the full
200,000-candidate pool as an incidental byproduct of benchmarking `beta_critical`.
The number therefore exists before T6 has run. It is disclosed here in full, with the
ordering that determines whether the preregistration's standing survives it.

### 1.1 What was fixed, and when, relative to the number

1. **K1's statistic and threshold were both fixed before any pool figure existed.**
   The kill decision is `|D(infinity)| / N < 0.10` (v2.0 §7.1). The threshold `0.10`
   was fixed in v2.0 as written, with no P2 measurement in view; v2.0's header
   records that no data of any kind existed at the time of writing.

2. **The statistic change was pre-data.** K1's decision moved from the grid rate
   `|D(8)| / N` to the existence rate `|D(infinity)| / N` in response to T5's first
   delivery, **prior to T1's benchmark**. That amendment is already recorded in
   v2.0's own revision record, and it was a correctness fix: the original wording
   would have killed a real effect whenever the `beta_c` distribution sat above the
   reporting grid's endpoint. It did not relax the threshold and did not change the
   direction of the test.

3. **A later proposed amendment was withdrawn without adoption.** On 2026-09-09,
   **after** T1's benchmark had incidentally computed the per-tile rates, a
   pooled-versus-per-tile rescue rule was proposed: a failing pooled rate would not
   kill when the per-tile rates were monotone in `|O|` and the largest-`|O|` tile
   cleared the threshold. It was **withdrawn and not adopted**, for two independent
   reasons, either of which is sufficient:

   - It was proposed after the gate statistic existed. Adopting a gate rule at that
     point is choosing the rule after seeing the number, which `CLAUDE.md` forbids
     and which no post-hoc justification repairs.
   - Its monotonicity condition is **already false** on the pool (`moves` at
     `|O| = 3` gives 0.1790, above `hold` at `|O| = 4` with 0.1775), so it would not
     have fired even if adopted.

   A withdrawn amendment is part of the record, which is why it is written down here
   rather than left unmentioned.

### 1.2 The number

Computed by T1's `beta_critical` over the full unstratified 200,000-candidate pool,
the item base v2.0 §7.1 and T6 Step 1 both specify. Deterministic: no seed enters
`beta_critical`.

```
pooled existence rate   |D(infinity)| / N = 0.1823   (36,464 / 200,000)
pooled grid rate        |D(8)| / N        = 0.1795
```

Per-tile existence rate `|D(infinity)| / N`, ordered by `|O|` ascending:

| tile | `\|O\|` | `\|D(infinity)\| / N` | `\|D(8)\| / N` |
|---|---|---|---|
| `manmade` | 3 | 0.0387 | 0.0385 |
| `moves` | 3 | 0.1790 | 0.1773 |
| `hold` | 4 | 0.1775 | 0.1746 |
| `size` | 6 | 0.3338 | 0.3273 |

Both pooled rates are at or above `0.10`, so this is **v2.0 §7.1 outcome 2, PASS**:
the effect exists and the reporting grid reaches it. No grid extension is triggered.

### 1.3 What T6 Step 1 is now

T6 Step 1 **still runs and still reports the gate**, through the **unamended** v2.0
§7.1 rule. Its status is a **reproduction check on T1's implementation**, not a fresh
gate: the quantity, the item base and the code are the same, so a discrepancy between
T6's number and the one above is evidence of a bug in one of the two runs and must be
resolved before Wave 2 opens. T6 emits the machine-readable gate record v2.0 §7.1
requires, and T7 and T8 read that record, not this file.

This does not make T1 an Arm A result. Arm A is T6 Steps 2 through 5 on T2's frozen
item set. T1 measured one pooled statistic on the pool; it did not characterise the
`beta_c` distribution, the divergence curve, or anything Arm A reports.

---

## 2. Documentation corrections, no rules changed

1. **Spec version.** v2.0's "Authoritative documents" paragraph cites
   `docs/spec/adversary-game-v1.md` at **content version v2**. The current content
   version is **v3.1**. The intervening amendments corrected the listener posterior
   (v3 §2, a misreading of P1 that put `L(h|o)` on the wrong normalisation),
   recited the tie-break to P1's D51 rule (v3 §6.2), fixed `beta_critical`'s value of
   record and made the `tau = 1` guard mechanical (v3.1 §9). None of them changes a
   quantity this document thresholds. The spec still wins wherever the two state the
   same formula.

2. **`|O|` is not the dominant driver of between-tile variance.** v2.0 §7.1 restates
   spec §7.2's disambiguation protocol, which orders tiles by `|O|` on the assumption
   that option count is the binding structural constraint. The pool data above does
   not support that: the rates are not monotone in `|O|`, and the spread within
   `|O| = 3` (0.1403) exceeds the 3-to-4 step. A plausible alternative driver is each
   tile's rating spread relative to its bin width.

   **No rule changes on this.** The disambiguation criteria cannot fire once the
   pooled existence rate passes, and amending an inert rule after seeing data costs
   the preregistration its standing for nothing. The mechanism question is assigned
   to **T6 Step 4 as exploratory**, not confirmatory, with no preregistered
   prediction and no threshold. Spec v3.1 §7.2 carries the same note.

---

## 3. What this amendment does not do

- It does not change K1, K2, any threshold, any hypothesis, or any exclusion rule.
- It does not adopt the withdrawn rescue rule, in any form.
- It does not license reading T1's pooled figure as an Arm A finding.
- It does not relieve T6 of running Step 1 and emitting the gate record.
