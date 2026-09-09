# Adversary Game Specification v3.1

Status: frozen on author sign-off (2026-09-08, amended 2026-09-08 and twice on
2026-09-09).
Produced by T0.
Every downstream Paper 2 task cites this document by path and version. If executing
a task shows an assumption here is wrong or underspecified, stop and report it here
rather than patching around it locally. File path is unchanged from v1
(`docs/spec/adversary-game-v1.md`); only the content inside is versioned. See
Section 11 for the full v1 -> v2 -> v3 -> v3.1 changelog.

Paper 1: Huynh, "Consistency Without Alignment: Item-Sensitive Language Models
Indistinguishable From Random," arXiv:2609.00576. Codebase at
`/Users/crishuynh/Documents/SoftwareProject/deception` (referred to below as P1).
This repository (`deception_RL`) is referred to below as P2.

---

## 1. Notation inherited from Paper 1

P1's paper (`paper/paper.tex`, section "Definitions") and code (`src/fit.py`,
`src/oracle.py`) fix the following symbols. This spec inherits them rather than
introducing new ones.

| Symbol | Meaning | Source |
|---|---|---|
| `h`, `h*` | a hypothesis; the true target hypothesis (a Means x Clue concept pair) | P1 |
| `H` | hypothesis space, `|H| = 100` (`M = C = 10`) | introduced here; P1 never names the set, only its size |
| `O`, `o` | the option set for an item's tile; a chosen option | P1 |
| `f(o, h)` | pair fit, min-aggregation exponential decay, no free parameters | P1 (`src/fit.py`) |
| `pi(h)` | prior over `H`; uniform in every P1 artifact | P1 |
| `P(h* \| o)` | P1's literal-listener posterior mass on the truth; see Section 2 for the exact form (corrected in v3) | P1 (`src/score_items.py`, `src/oracle.py`) |
| `o_fit` | `argmax_o f(o, h*)` | P1 |
| `o_bayes` | `argmax_o P(h* \| o)`, ties broken by max fit among tied options | P1 |

`O`/`o` is now also what `docs/P2/prompt-plan.md` and the task briefs (T1-T9) use
directly (amended in v2; see Section 11). There is no remaining `s`/`o` aliasing to
track.

**Generalization needed for P2.** P1 only ever writes the posterior evaluated at
the true hypothesis, `P(h*|o)`. The adversary needs the posterior mass at other
hypotheses too (to find the strongest rival). This spec writes the general form
`L(h|o)`, defined in Section 2, so `P(h*|o) = L(h*|o)` is the P1 special case at
`h = h*`. This is a generalization, not a competing symbol: P1 never defined
`L(h|o)` for `h != h*`. P1's code, however, already computes the full vector as
an intermediate (`grid_stats` normalises over the whole hypothesis grid before
selecting `h*`), so the generalization reads a quantity P1 computes rather than
introducing a new one.

**Log convention.** `log` denotes the natural logarithm throughout, matching P1's
code (`torch.log_softmax` in `src/score_llm.py`; `fit` is defined via `exp(...)`).

---

## 2. Formal setup (P1, restated with inherited notation)

- Hypothesis space `H`, `|H| = 100`, true hypothesis `h* in H`, uniform prior
  `pi(h) = 1/100`.
- Option set `O` is **one item's tile's option set** (P1's `o`; P2's "signal"),
  small and enumerable. Exact counts, verified against
  `data/reference/tiles.json` in the P1 repo (the earlier "2 to 7" range in v1 of
  this spec was not checked against the actual file and is corrected here):

  | tile | `\|O\|` | options |
  |---|---|---|
  | `manmade` | 3 | naturally occurring / partly manufactured / manufactured |
  | `moves` | 3 | stays still / sometimes moves / moves |
  | `hold` | 4 | very hard to hold / hard to hold / easy to hold / very easy to hold |
  | `size` | 6 | six anchor-object size bins |

  This four-way range (3, 3, 4, 6) is a real, built-in gradient in `|O|` across
  otherwise identical machinery. Section 7.2 uses it directly.
- Literal listener posterior. **Corrected in v3; v1 and v2 stated this wrongly.**
  `f(o,h)` is a *fit*, not a likelihood: it is not normalised over anything. It
  becomes the conditional likelihood `P(o|h)` only after being normalised over
  the option set, and that inner normalisation is what makes Bayes well-posed.
  P1 does exactly this, in two steps (`src/oracle.py::likelihood`, which sums
  over the option axis, then `src/score_items.py::grid_stats`, which sums the
  result over hypotheses):

  ```
  P(o | h)  = f(o,h) / sum_{o'} f(o',h)                      (normalise over o)
  L(h | o)  = pi(h) P(o|h) / sum_{h'} pi(h') P(o|h')
            = [ f(o,h) / sum_{o'} f(o',h) ]
              / sum_{h'} [ f(o,h') / sum_{o'} f(o',h') ]      (uniform prior cancels)
  ```

  v1 and v2 wrote `L(h|o) = f(o,h) / sum_{h'} f(o,h')`, dropping the inner
  normalisation. The per-hypothesis normalisers `1 / sum_{o'} f(o',h)` differ
  across `h` and therefore do **not** cancel; they reweight every rival
  hypothesis. This is a correction to a misreading of P1, not a P2 design
  choice: the object being specified was always meant to be P1's posterior.

  **Measured cost of the error, on the frozen 1,000-item set**: taking
  `argmax_o` of the v2 formula disagrees with P1's frozen `o_bayes` on
  **50 of 1,000 items** (70 without the tie-break of Section 6.2); the corrected
  formula disagrees on **0 of 1,000**. Acceptance test 1 (Section 10) is
  therefore satisfiable only under the corrected definition.
- **P1's oracle:** `o_bayes(i) = argmax_{o in O} L(h*|o)` for item `i`, ties broken
  by max `f(o,h*)` among options tied on `L(h*|o)` (P1's existing convention,
  `paper.tex` sec. "Oracle").

P2 writes this oracle as `o*_0 = argmax_o L(h*|o)`. It is the same object as P1's
`o_bayes`, renamed only to carry the beta index into the adversary game below.

### 2.1 Joint (multi-tile) construction: conditional, not built

P2's main analysis is defined over **per-tile `O` only**, exactly as in Section 2:
one item, one tile, `|O| in {3,3,4,6}`. This subsection exists because a joint
(multi-tile) construction was considered for the main result and rejected; it is
recorded here, fully specified, so a later task can build it without re-deriving
this reasoning, but **it is not part of the primary design and no code should be
written against it without a separate author decision** gated on Section 7.2.

**What "joint" would mean.** An item's Scientist marks all four tiles at once
instead of one: an option becomes a 4-tuple `(o_manmade, o_moves, o_hold, o_size)`,
giving `3*3*4*6 = 216` joint options. The joint likelihood multiplies per-tile
fits and renormalizes over the fixed 100-hypothesis space:

```
f_joint(o1,o2,o3,o4, h) = f_manmade(o1,h) * f_moves(o2,h) * f_hold(o3,h) * f_size(o4,h)
L_joint(h | o1,o2,o3,o4) = f_joint(o1,o2,o3,o4, h) / sum_{h'} f_joint(o1,o2,o3,o4, h')
```

**Why it is not the main construction, resolved against D39.** P1's actual design
decision, quoted verbatim from `tasks/TASK_14_item_generator.md` in the P1 repo:

> **D39. One tile per item.** The Scientist sees the target, the table, and a
> single tile. This removes the conditional-independence assumption Task 11
> needed to multiply likelihoods across tiles correlated at up to `|r| = 0.63`,
> and removes a joint-optimisation confound where tile-by-tile greedy choice
> differs from jointly optimal choice. The oracle becomes assumption-free. Items
> are cheap, so the cost is volume only.
>
> Multi-tile is a **secondary condition**, built only if time permits. It is not
> part of the primary design.

This resolves cleanly, not ambiguously: **D39 does not forbid the joint
condition. It explicitly anticipates it as an optional secondary condition**,
and gives the reason single-tile is primary (the conditional-independence
assumption across tiles correlated up to `|r|=0.63`, and a separate
greedy-vs-joint-optimum confound). Neither P1's frozen 200k-candidate pool
(`items_candidate.parquet`, produced by `generate_items.py`, whose own docstring
states "One tile per item (D39)") nor the frozen 1,000-item set
(`items_final.parquet`) contains a single joint item; both are one-tile-per-item
by construction. `src/oracle.py` does compute a 216-option "all four jointly" row
(`run_items()`), but that is a Task-11 diagnostic table computed on freshly
random-drawn concepts each call, never wired to the frozen pool or the frozen
item set. (A separate, older code comment in `src/items_report.py` cites "D39 in
the earlier numbering" for an unrelated point about not pooling standard errors
across tiles; that is a decision-numbering artifact from before a renumbering
pass, not a second definition of D39. `tasks/TASK_14_item_generator.md`'s text,
quoted above, is the authoritative source.)

**Verified, not asserted (per the constraint that this task not patch around a
real break silently): the joint construction breaks neither the tau=1 identity
nor the single-crossing/monotonicity proof.** Both Section 5.1's identity
(`sum_h L(h|o)=1` implies `V_0(o)=L(h*|o)` at tau=1) and Section 6.3's proof
(pairwise `V_beta` crossings are roots of a linear equation in `x=exp(beta/tau)`)
use only the fact that `L(.|o)` is *some* normalized distribution over `H` for
each fixed `o`. Both hold for `L_joint` exactly as they hold for the per-tile
`L`, regardless of how `O` or `L(.|o)` are built. So the joint construction is
mathematically safe if it is ever built; the reason it is not the main result is
the pool/artifact incompatibility above and the reintroduced independence
assumption, not a broken proof.

**If Section 7.2's gate disambiguation ever motivates building this**: it
requires new item-generation code (reusing the frozen vocabulary, fit function,
and tiles, but combining across tiles in a way `generate_items.py` does not),
it is a conditional exploratory arm, not a redraw from "the same pool" in D2's
sense, and any result from it must state the reintroduced conditional-
independence assumption as a limitation in the same sentence as the result, not
in a footnote.

---

## 3. Adding the adversary

The adversary knows `h*`, observes `o`, and promotes one decoy `d != h*` with
persuasion budget `beta >= 0`. Honest investigators score

```
u(h) = log L(h|o) + beta * 1[h = d]
```

and choose by quantal response at fixed temperature `tau`:

```
P(choose h | o, d) = exp(u(h)/tau) / sum_{h'} exp(u(h')/tau)
```

Scientist utility is the adversary-worst-case probability of a correct accusation:

```
V_beta(o) = min_{d != h*} P(choose h* | o, d)
```

`tau` is fixed at 1 and is **not a free parameter of this game** (Section 8.1
explains why). `beta` is the one new free parameter P2 introduces.

---

## 4. Derivation of R1 (adversary best response)

Claim: `d*(o) = argmax_{h != h*} L(h|o)`, independent of `beta` and `tau`.

**Derivation.** Write `L_h = L(h|o)` for brevity, fixed `o`. Substituting `u`:

```
P(choose h | o, d) = L_h^{1/tau} * exp(beta/tau * 1[h=d]) / Z(d)

Z(d) = sum_{h'} L_{h'}^{1/tau} * exp(beta/tau * 1[h'=d])
     = sum_{h' != d} L_{h'}^{1/tau}  +  L_d^{1/tau} * exp(beta/tau)
     = sum_{h'} L_{h'}^{1/tau}  +  L_d^{1/tau} * (exp(beta/tau) - 1)
```

(added and subtracted the `h'=d` term to get from the first sum to the second).
For `h = h*` (and `d != h*`, so `1[h*=d] = 0`):

```
P(h* | o, d) = L_{h*}^{1/tau} / [ sum_{h'} L_{h'}^{1/tau} + L_d^{1/tau}(exp(beta/tau)-1) ]
```

For `beta >= 0`, `exp(beta/tau) - 1 >= 0`. `P(h*|o,d)` is therefore a strictly
decreasing function of `L_d^{1/tau}`, hence of `L_d`. The adversary minimizes
`P(h*|o,d)` over `d != h*` by maximizing `L_d`, i.e.

```
d*(o) = argmax_{h != h*} L(h|o)
```

**Verified. R1 holds exactly, for every `tau > 0` and `beta >= 0`.** It does not
depend on `beta`: the identity of the best-response decoy is fixed by `o` alone.
This is used in Section 6.

---

## 5. Derivation of R2 (the beta continuum) and the tau resolution

Substituting `d*(o)` into `V_beta(o) = P(h*|o, d*(o))`, and writing
`M(o) = L(d*(o)|o) = max_{h != h*} L(h|o)`:

```
V_beta(o) = L(h*|o)^{1/tau} / [ sum_{h'} L(h'|o)^{1/tau} + M(o)^{1/tau} (exp(beta/tau)-1) ]
```

**This is the exact form. Verified**, by the substitution above.

### 5.1 The beta = 0 case, and why tau must be fixed at 1

At `beta = 0`, `exp(beta/tau) - 1 = 0` and

```
V_0(o) = L(h*|o)^{1/tau} / sum_{h'} L(h'|o)^{1/tau}
```

The prompt-plan's R2 claims `argmax_o V_0(o) = o*_0` (P1's oracle) **exactly**,
for the full `tau` sweep the plan proposes (`tau in {0.5, 1, 2}`). This is **false
for `tau != 1`, and the plan's own draft derivation implicitly assumed `tau = 1`
without stating it.** Re-derivation:

`L(.|o)` is a probability distribution over `H` for every `o`: `sum_h L(h|o) = 1`.

**Shown, not asserted (v3).** Under the corrected Section 2 definition, write
`w(o,h) = f(o,h) / sum_{o'} f(o',h)` for the inner (over-`o`) normalisation.
Then `L(h|o) = w(o,h) / sum_{h'} w(o,h')`, and summing over `h` at fixed `o`:

```
sum_h L(h|o) = sum_h w(o,h) / sum_{h'} w(o,h')
             = [ sum_h w(o,h) ] / [ sum_{h'} w(o,h') ]
             = 1
```

The denominator does not depend on `h`, so it factors out of the sum and the
numerator is literally the same sum. This holds for every `o`, for any strictly
positive `f`, and in particular it does **not** depend on which normalisation
convention Section 2 uses: the v1/v2 formula was normalised over `h` too, which
is exactly why the v1/v2 error left this identity, and everything resting on it,
intact. `f(o,h) > 0` everywhere (P1's D29, acceptance test 7), so no denominator
vanishes.

**Consequence.** The `tau = 1` identity below, R2's `beta = 0` clause, R1
(Section 4), the single-crossing proof (Section 6.3) and the monotone nesting of
`D(.)` (Section 7.1) all use `L(.|o)` *only* through the facts that it is
normalised over `h` and strictly positive. Each therefore survives the v3
correction unchanged. This was verified, not assumed: see Section 11's v3 entry
for the re-derivation and the numbers.

Two cases:

- **`tau = 1`.** `V_0(o) = L(h*|o)^1 / sum_h L(h|o)^1 = L(h*|o) / 1 = L(h*|o)`.
  This is an identity, not an approximation: the denominator is the L1 norm of a
  probability vector, which is 1 by definition, for every `o`. Therefore
  `argmax_o V_0(o) = argmax_o L(h*|o) = o*_0` **exactly, and only for this reason**.
- **`tau != 1`.** The denominator `sum_h L(h|o)^{1/tau}` is the `1/tau`-power sum
  of a probability vector, i.e. proportional to an `l_{1/tau}` norm. This quantity
  is **not** constant in `o` (unlike the `tau=1` case, where it collapses to the
  constant 1): it depends on the *shape* of the distribution `L(.|o)`, not only on
  `L(h*|o)`. Two options with the same `L(h*|o)` but differently peaked rival
  distributions will have different `l_{1/tau}` norms, so `V_0` reorders them
  relative to `L(h*|o)` alone. There is no general argument that
  `argmax_o V_0(o) = argmax_o L(h*|o)` at `tau != 1`, and a direct construction
  (two options with equal `f(o,h*)` and equal `sum_h f(o,h)` but different
  within-option fit dispersion across rivals) produces a counterexample. **R2's
  beta=0 clause, as stated in the prompt-plan, is wrong for general tau.**

**Resolution (author decision, 2026-09-08): `tau` is fixed at 1 and is not a
parameter of Paper 2.** Justification, restated from the derivation above: P1's
oracle `o_bayes = argmax_o L(h*|o)` is the optimal option for a `tau=1`
quantal-response listener, and *only* for that listener, because only at `tau=1`
does `V_0(o)` collapse to `L(h*|o)` identically (the L1-norm-equals-1 identity).
The listener model is a frozen P1 artifact; P2 holds it fixed and varies only the
game (`beta`). A `tau` sweep in the main analysis would silently modify a frozen
listener and confound two mechanisms that both push the optimum toward margin
(temperature sharpening and adversary pressure), which is exactly the kind of
silent artifact modification `CLAUDE.md` forbids.

**Consequence for downstream tasks.** Every occurrence of `tau` in the function
contracts below is `tau = 1`, fixed, not swept, in the main analysis (Arms A, B,
C and the preregistration). An appendix robustness check is permitted under the
following protocol, stated here so it is preregistered rather than decided after
seeing data:

> Recompute Arm B's primary measure at `tau in {0.5, 2}`, using as the
> no-adversary reference the **tau-local optimum** `argmax_o V_0(o)` evaluated at
> that `tau` (not `o*_0`). Report only whether Arm B's qualitative conclusion
> survives. State explicitly that oracle-nesting holds at `tau = 1` only, and that
> at `tau < 1` the tau-local reference already embeds rival suppression (sharper
> quantal response concentrates `V_0` toward options that also suppress the
> strongest rival, which is a step in the same direction as the adversary
> mechanism itself), so a movement effect found there is not attributable to
> `beta` alone.

### 5.2 The beta -> infinity case

As `beta -> infinity`, `exp(beta/tau) - 1 ~ exp(beta/tau)`, which dominates the
`o`-dependent but `beta`-independent term `sum_h L(h|o)^{1/tau}` in the
denominator (the latter is bounded; the former grows without bound). So

```
V_beta(o) ~ exp(-beta/tau) * [ L(h*|o) / M(o) ]^{1/tau}       as beta -> infinity
```

**Verified** by dropping the subdominant term and simplifying. `exp(-beta/tau)` is
constant in `o`. `x -> x^{1/tau}` is strictly increasing for any `tau > 0`, so it
preserves argmax over `o` **for every tau**, unlike the beta=0 case:

```
argmax_o V_beta(o)  ->  argmax_o [ L(h*|o) / M(o) ]  =  argmax_o margin(o)
                         as beta -> infinity, for every tau > 0

margin(o) := log L(h*|o) - max_{h != h*} log L(h|o) = log L(h*|o) - log M(o)
```

**R2's beta -> infinity clause is verified and holds for every tau > 0.** Only the
beta=0 clause required the tau=1 fix.

---

## 6. beta_c, tie-breaking, and why bisection is valid

### 6.1 Definition

For item `i`, `beta_c(i)` is the infimum of `beta` at which
`argmax_o V_beta(o)` first differs from `o*_0`. If no such `beta` exists,
`beta_c(i) = infinity` (adversary-robust item).

### 6.2 Tie-breaking

Ties in `argmax_o V_beta(o)` are broken **exactly as P1 breaks ties in
`o_bayes`**: first by max `V_beta(o)` (already the primary criterion), then by
max `f(o, h*)` among options tied on `V_beta`, then, if still tied, by the
option's index in the tile's `options` list (`tiles.json`), P1's existing
canonical order.

**Citation corrected in v3.** The rule that actually produced the frozen
`o_bayes` is P1's **D51**, implemented in `src/tiebreak.py::lex_obayes` and
applied at `TAU_MAIN = 1e-9`, a *relative* tolerance:

```
tied   = post >= post.max() * (1 - 1e-9) - 1e-12
o_bayes = argmax of f(o,h*) over the tied set          (ties -> lowest index)
```

v1 and v2 cited `TIE_EPS = 1e-12` from `src/oracle.py` as this tolerance. That
constant is a Task-11 diagnostic threshold used for counting ties in the oracle
report; it is not the rule applied to the frozen artifact. Downstream code must
reuse `lex_obayes` by import rather than reimplementing either tolerance.

The two tolerances were checked against each other on the frozen 1,000-item set:
**both reproduce `o_bayes` on 1,000 of 1,000 items, and the tie sets they induce
are identical on every item**, so no result in Paper 1 or Paper 2 turns on the
difference. D51 is nevertheless the rule of record, because it is the one the
artifact was built with. The tie-break matters on 17 of the 1,000 items: a plain
`argmax` disagrees with `o_bayes` on exactly that many.

`eps_tie = 1e-12` (Section 8.2) remains the absolute tolerance for comparing
`f(o,h)` and `L(h|o)` values, for instance in `adversary_best_response` and in
acceptance test 6. It is D51's relative `TAU_MAIN` that governs option
selection.

### 6.3 Proof that argmax_o V_beta(o) is piecewise constant in beta

Fix item `i` and `o in O`. Write `x = exp(beta/tau)` (a strictly increasing
bijection of `beta in [0, infinity)` onto `x in [1, infinity)`), and

```
C_o = L(h*|o)^{1/tau}                    (constant in beta)
A_o = sum_h L(h|o)^{1/tau} - M(o)^{1/tau}  (constant in beta; >= 0)
B_o = M(o)^{1/tau}                        (constant in beta; > 0)
```

so that `V_beta(o) = C_o / (A_o + B_o x)`, a strictly decreasing function of `x`
(hence of `beta`) for fixed `o`, since `A_o, B_o, C_o > 0`.

**Claim: for any two options `o, o'`, `V_beta(o) = V_beta(o')` has at most one
solution `x >= 1`.** Setting the two ratios equal and clearing denominators:

```
C_o (A_{o'} + B_{o'} x) = C_{o'} (A_o + B_o x)
x * (C_o B_{o'} - C_{o'} B_o) = C_{o'} A_o - C_o A_{o'}
```

This is **linear in `x`**. It has at most one root (none, if the coefficient of
`x` is zero and the two curves are not identical; the whole line, in the
degenerate case they are identical, which is not a crossing). A strictly
decreasing function of `x` can therefore cross another strictly decreasing
function of `x` **at most once**, for `x >= 1`.

**Consequence 1 (well-posedness).** At `beta = 0` (`x = 1`), `o*_0` is defined as
the argmax, so `V_0(o*_0) >= V_0(o')` for every rival `o'`. Because each pairwise
comparison `V_beta(o*_0)` vs. `V_beta(o')` can flip **at most once**, and it
starts non-negative (`o*_0` on top or tied), the flip, if it happens, is a single,
permanent transition from "`o*_0` weakly ahead" to "`o'` strictly ahead" at
`x*_{o'} = beta*_{o'}`. Hence for every rival `o'` there is at most one crossing
`beta*_{o'} = tau * log(x*_{o'})` (only counted if `x*_{o'} >= 1`, i.e.
`beta*_{o'} >= 0`).

```
beta_c(i) = min_{o' != o*_0} beta*_{o'}          (infinity if the set is empty)
```

**Consequence 2 (monotonicity of D(beta)).** Since each pairwise dominance
`o*_0` vs. `o'` flips at most once and only in the losing direction (never back),
the set of rivals beating `o*_0` only grows as `beta` increases. So once
`argmax_o V_beta(o) != o*_0` at some `beta`, it remains `!= o*_0` for all larger
`beta` (a *possibly different* rival may take over from the one that first
overtook `o*_0`, but `o*_0` itself never regains the argmax). This is exactly:
`i in D(beta) => i in D(beta') for beta' > beta`, i.e. `D(.)` is monotonically
nested. **This is what makes bisection on `beta` valid**: the indicator
`1[argmax_o V_beta(o) != o*_0]` is monotone non-decreasing in `beta`, so standard
bisection on that indicator converges to `beta_c(i)`.

**Note for T1.** The pairwise crossing equation above is linear and gives a
closed form for each `beta*_{o'}`. Implementations may compute `beta_c` directly
from this closed form (exact, no iteration) or via bisection to the tolerance in
Section 8.2; if via bisection, the closed form is a strong correctness check
(compare bisection output to the closed-form root on a test sample) since a
mismatch beyond tolerance indicates an implementation bug rather than numerical
noise.

---

## 7. Divergence set and robust set

```
D(beta) = { i : beta_c(i) <= beta }     for beta > 0
D(0)    = {}                             by convention (Section 7.1)
```

Adversary-robust set: `{ i : beta_c(i) = infinity }`, i.e. `o*_0` is also the
margin-maximizer (Section 5.2), so no finite persuasion budget changes the
optimal option. By Section 6.3, `D(.)` is monotonically nested in `beta`, for
`beta > 0`.

### 7.1 The beta=0 boundary (correctness fix, v2)

**Bug in v1, found by the author.** `beta_c(i)` is an infimum. If `o*_0` and some
rival `o'` are exactly tied at `beta=0` (P1 counts this case explicitly:
`boundary_exact` columns in `concept_tile_bins.csv`, fit `= 1.0` on both options
adjacent to a bin boundary) and `o'` strictly overtakes `o*_0` for every
`beta > 0`, Section 6.3's crossing is at `x* = 1`, i.e. `beta*_{o'} = 0`, so the
formula as originally stated gives `beta_c(i) = 0` and puts `i` in `D(0)`. But
`o*_0` is the argmax at `beta=0` **by the tie-break rule** (Section 6.2), which
is a fact about the definition, not a limit: nothing has diverged at exactly
`beta=0`, for any item, ever. `D(0)` must be empty by construction, and the raw
infimum formula does not guarantee that on its own.

**Fix.** `beta_c(i)` keeps its Section 6.1 definition unchanged (infimum over
`beta >= 0`; a boundary-tied item can legitimately have `beta_c(i) = 0`, which
correctly reports "maximally fragile: any positive budget flips this item," and
is a meaningful number to keep reporting, e.g. in Section 6's distribution
characterization). What changes is `D`: **`D(0) := {}` by fiat, for every item,
regardless of the value of `beta_c`; `D(beta) = {i : beta_c(i) <= beta}` only for
`beta > 0`.** This is consistent with, not a patch around, Section 6.2's
tie-break rule: that rule is exactly what makes `argmax_o V_0(o) = o*_0` true
for every item without exception, so the `beta=0` slice of the divergence curve
has nothing in it, by definition, independent of how close any crossing is to
zero. Section 6.3's monotonicity proof is unaffected for `beta > 0` (it never
relied on the value at exactly `beta=0`).

**Consequence for reporting.** A `beta_c(i) = 0` item appears in `D(beta)` for
every `beta > 0` (correctly, since the rival does overtake immediately) but is
excluded from `D(0)` specifically. `|D(beta)|` curves (Section 6, T6 Step 5) must
treat `beta=0` as a fixed, separate anchor point (always `|D(0)|=0`) rather than
extrapolating the curve's limit as `beta -> 0+` back onto it.

### 7.2 Gate disambiguation protocol (for T6 Step 1)

Section 2's `|O| in {3,3,4,6}` gradient is a built-in confound for T6's kill
gate: a small `|O|` mechanically shrinks the reachable range of `V_beta(o)`
across options, which can shrink `|D(beta)|` for reasons that have nothing to do
with whether the adversary effect exists. T6 Step 1 must report divergence
**per tile**, not only pooled, so a near-empty pooled divergence set can be told
apart from a structural `|O|`-driven artifact. This is stated now, before any
model or Arm A number is seen, so it is a preregistered interpretation rule
rather than a post-hoc justification (per `CLAUDE.md`: "no tuning toward a
desired result").

**Procedure.** At `beta = 8` (the largest finite value in the accepted reporting
grid, Section 8.2), compute the per-tile divergence rate
`r_t = |D_t(8)| / n_t` for `t in {manmade(3), moves(3), hold(4), size(6)}`
(subscript is the tile; `n_t` is that tile's item count in the frozen set),
ordered by `|O|` ascending: `manmade, moves, hold, size`.

**Interpretation, stated numerically so it is preregistered:**

- **Structural / inconclusive**: `r_size` exceeds both `r_manmade` and `r_moves`
  by at least 10 percentage points (absolute), i.e.
  `r_size - min(r_manmade, r_moves) >= 0.10`. Read: the option-space size is a
  plausible binding constraint on the pooled result. The pooled kill-gate
  outcome is reported as **inconclusive, not a clean negative**. The joint
  condition (Section 2.1) becomes a justified, author-gated follow-up, not an
  automatic next step.
- **Clean negative**: `max_t r_t` across all four tiles, **including `size`**,
  is still below T5's preregistered kill threshold. Read: even the tile with
  the most room to diverge does not clear the bar, so `|O|` is not the limiting
  factor and the adversary effect is genuinely absent in this signal space.
  Report and stop per T6 Step 1's existing instruction; Arms B and C do not
  run; the joint condition would not rescue this result and is not justified by
  it.
- **Neither condition met** (e.g. `size` is not the top tile, or the gap is
  present but under 10 points): report all four `r_t` values and the pooled
  figure plainly, state explicitly that neither the structural nor the
  clean-negative criterion was met, and stop for author review before Wave 2
  opens, per T6's existing "if it fails, STOP... report to the author" pattern.
  Do not resolve this case by picking whichever reading is more convenient.

**`|O|` is not the dominant driver (factual note added in v3.1; the rule above
is unchanged).** T1's implementation measured the existence rate
`|D(infinity)| / N` per tile over the full 200,000-candidate pool:

| tile | `\|O\|` | `\|D(infinity)\| / N` |
|---|---|---|
| `manmade` | 3 | 0.0387 |
| `moves` | 3 | 0.1790 |
| `hold` | 4 | 0.1775 |
| `size` | 6 | 0.3338 |

Two facts follow, and they are recorded here because this section's framing
assumes the opposite. The rates are **not monotone in `|O|`**: `moves` at
`|O| = 3` exceeds `hold` at `|O| = 4`. And the spread *within* `|O| = 3` is
`0.1403`, larger than the 3-to-4 step and comparable to the 4-to-6 step. Two
tiles with identical option counts differ by fourteen points, so option count
explains less of the between-tile variance than within-`|O|` variation does. A
plausible alternative driver is each tile's rating spread relative to its bin
width, which is not `|O|`.

**No rule changes on this note, deliberately.** The pooled existence rate passes
K1 (0.1823, preregistration section 7.1), so this section's disambiguation
criteria cannot fire, and amending an inert rule after seeing pool data buys
nothing and costs the preregistration its standing. The mechanism question moves
to T6 Step 4 as **exploratory**, not confirmatory, and no replacement rule is
proposed here.

**Flagged for author confirmation**: the `10 percentage point` threshold is this
task's proposed operationalization of "clearly above," not a value carried over
from any existing document (none was given). If a different threshold or
statistic (e.g. a formal rank-correlation test across the four tiles, which is
possible but low-powered with only four points) is wanted, only this
subsection changes.

---

## 8. Chosen values

### 8.1 tau

**tau = 1, fixed, not swept in the main analysis.** See Section 5.1 for the full
justification and the appendix-only sweep protocol. P1 used a pure argmax
listener with no temperature or softmax anywhere in its decision rule (`src/fit.py`:
"no temperature, no softmax, no fitted decay rate"; P1's oracle is a hard argmax
over the exact posterior, not a quantal response). Per the instruction to inherit
`tau` only if P1 fixed a listener sharpness: **P1 did not use a quantal-response
listener at all, so this is the "choose fresh" case** — but "fresh" resolved to
`tau = 1` specifically, because that is the unique value at which the new
quantal-response listener's `beta=0` optimum coincides with P1's frozen argmax
oracle (Section 5.1). This is not an arbitrary fresh choice; it is forced by the
requirement that the adversary game nest P1 exactly at `beta=0`.

### 8.2 beta reporting grid and tolerances

`docs/P2/prompt-plan.md`'s stated grid, `beta in {0, 0.25, 0.5, 1, 2, 4, }`, is
truncated in the source document (trailing comma, nothing after). This spec
completes it as:

```
beta reporting grid: {0, 0.25, 0.5, 1, 2, 4, 8}, plus infinity as a labeled
                      limiting case (Section 5.2), reported separately, never
                      dropped from plots (per CLAUDE.md, "no silent clipping").
```

**Flagged for author confirmation**: the endpoint `8` and the spacing are this
task's completion of a truncated list, not a value carried over from an existing
document. If a different top value or spacing is wanted, only this line changes;
nothing else in this spec depends on the specific grid.

`beta_c(i)` itself is computed exactly (Section 6.3's closed form or bisection to
tolerance), never read off this grid; the grid is for reporting `|D(beta)|` curves
only.

- **Tie tolerance** `eps_tie = 1e-12`, absolute, on any two compared values of
  `f(o,h)` or `L(h|o)` or `V_beta(o)`. Used for hypothesis-level comparisons
  (`adversary_best_response`) and acceptance test 6. **Option selection does not
  use it**: that is governed by D51's relative `TAU_MAIN = 1e-9`
  (`src/tiebreak.py`), which is the rule the frozen `o_bayes` was built with.
  See Section 6.2; the v1/v2 claim that `eps_tie` "matches P1's `TIE_EPS`" was
  a miscitation, corrected in v3.
- **Bisection tolerance** `eps_beta = 1e-9`, absolute, on `beta`, if bisection is
  used instead of (or as a check against) the closed form in Section 6.3.
- **Float precision**: float64 throughout. Compute `log L(h|o)` and related
  quantities in log-space (`CLAUDE.md`: "Log space throughout for probability
  math"); do not exponentiate large arguments directly. The `beta -> infinity`
  limit (Section 5.2) is a **separate code path** returning `argmax_o margin(o)`
  directly, never approximated by substituting a large finite `beta` into the
  finite-`beta` formula (which would overflow `exp(beta/tau)` for `tau=1` at
  `beta` well below double-precision range, and is exactly the kind of numerical
  convenience `CLAUDE.md` forbids: "no silent clipping, clamping, or
  regularization... numerical convenience that changes results is a bug").
- **Infinity representation**: `math.inf` / `np.inf` (IEEE-754) for `beta_c` and
  for `V_beta` limits where applicable. Any tabular/serialized output (parquet,
  CSV, JSON) must additionally carry an explicit boolean `is_robust` column
  alongside the raw `beta_c` value, because not every downstream reader or file
  format round-trips IEEE infinity losslessly (matches P1's convention of
  explicit manifest columns over implicit sentinel values).

### 8.3 No new free parameters beyond beta

`tau` is fixed, not a free parameter (Section 8.1). `beta` is the only new free
parameter this game introduces relative to P1. This is a deliberate, minimal
deviation from P1's zero-free-parameter design philosophy (`src/fit.py`,
`paper.tex`: shifting or softmax were explicitly rejected in P1 for reintroducing
a free parameter). Recorded here per the constraint: "If you find yourself
needing a third [parameter], stop and report it as a design problem." No third
parameter was needed.

---

## 9. Function-signature contracts

Contracts only, no implementations, per T0's constraint. `item` is whatever
in-memory or on-disk record type downstream tasks use to carry `h*`, `H`, `O`,
and the tile's fit data for one item; its concrete shape is a T1 decision, not a
T0 decision, since T0 must not write implementation code.

```python
import math
from typing import Any, Hashable, Sequence

HypothesisId = Hashable
SignalId = Hashable  # an "option" o in P1's terms; see Section 1 correspondence


def v_beta(item: Any, o: SignalId, beta: float, tau: float = 1.0) -> float:
    """Scientist utility V_beta(o) for one item and option, under a
    best-responding adversary (Section 3, 5).

    Computes V_beta(o) = P(choose h* | o, d*(o)) where d*(o) is the adversary's
    best response (adversary_best_response, below). Must use the closed form of
    Section 5 (via log L(h|o), log-space arithmetic per Section 8.2), not a
    direct simulation of the softmax over d in a loop.

    `tau` defaults to 1.0 (Section 8.1). **tau != 1.0 must raise unless the
    caller passes an explicit opt-in flag** (v3.1; implementations add a
    keyword-only `appendix: bool = False` to every contract taking `tau`). The
    prohibition on silent tau drift in Arm A/B/C main results is therefore
    mechanical rather than advisory. Measured justification, to be carried in
    the implementation's error message so the guard is not removed later: at
    `tau in {0.5, 2}` the `beta = 0` argmax disagrees with P1's frozen oracle on
    **127 of 2,000 item-tau cells**. Only Section 5.1's appendix robustness
    protocol may opt in, and it must use the tau-local reference.

    For beta == math.inf, use the separate limiting-case path (Section 5.2,
    8.2), not this formula evaluated at a large finite beta.

    Returns a probability in [0, 1]. Raises on beta < 0 or tau <= 0.
    """
    raise NotImplementedError


def adversary_best_response(item: Any, o: SignalId) -> HypothesisId:
    """d*(o) = argmax_{h != h*} L(h|o) (Section 4, R1).

    Independent of beta and tau (R1 holds for every beta >= 0, tau > 0): this
    function takes neither as an argument, by construction. Ties broken by the
    canonical order in Section 6.2 (max f(o,h) among tied L(h|o), then tile
    option/hypothesis index order).
    """
    raise NotImplementedError


def beta_critical(item: Any, tau: float = 1.0) -> float:
    """beta_c(i): infimum of beta at which argmax_o V_beta(o) first differs
    from o*_0 (Section 6.1). May return math.inf for adversary-robust items
    (Section 7).

    Must be computed to the tolerance in Section 8.2 (eps_beta = 1e-9) by
    bisection on the monotone indicator 1[argmax_o V_beta(o) != o*_0], valid per
    Section 6.3's monotonicity proof. The argmax in that indicator is the
    tie-broken argmax of Section 6.2, not a strict comparison of V_beta values;
    a strict comparison does not converge on the option pairs whose curves are
    equal to float64 (v3 item 5).

    **The bisected value is the value of record** (v3.1). Cross-check against the
    closed-form pairwise crossing of Section 6.3, which is exact, but do not
    return it: consistency with `optimal_option` and `divergence_set`, which the
    bisected value has by construction, beats exactness against a criterion no
    other function uses. Any artifact carrying `beta_c` (T2's manifest, T6's
    gate record) carries the bisected value.

    Expect the two to differ by up to ~1e-6 in beta, in either direction: the
    closed form solves V_o = V_o' exactly, while bisection fires when the options
    separate by one D51 band. That difference is the expected behaviour of the
    two definitions, not noise and not a bug, and it is orders of magnitude below
    any plausible stratification bin edge. What *would* be a bug: the two
    disagreeing on which items are adversary-robust, or a closed-form root at
    which the top two options are not equal to float64.
    """
    raise NotImplementedError


def divergence_set(items: Sequence[Any], beta: float, tau: float = 1.0) -> list:
    """D(beta) = { i : beta_c(i) <= beta } over a collection of items (Section 7).

    Returns item identifiers (not the items themselves). Must be consistent with
    beta_critical: item i is included iff beta_critical(item_i, tau) <= beta,
    with the same eps_beta tolerance applied at the boundary. Consistency is
    structural, not incidental: beta_critical bisects on the same tie-broken
    argmax that every other function here uses (v3 item 5).

    Special case, Section 7.1: at beta == 0 this MUST return an empty list
    unconditionally, regardless of any item's beta_critical value (a
    boundary-tied item can have beta_critical == 0 and must still be excluded
    from divergence_set(items, 0, tau)). Do not implement this by special-casing
    "beta_critical <= 0" as a comparison; implement it as an explicit
    "if beta == 0: return []" branch, so the exclusion holds even if a future
    change to beta_critical's tolerance handling would otherwise leak a
    boundary-tied item through the general comparison.
    """
    raise NotImplementedError


def margin(item: Any, o: SignalId) -> float:
    """margin(o) = log L(h*|o) - max_{h != h*} log L(h|o) (Section 5.2).

    Computed in log-space directly (do not compute L(h|o) in linear space and
    then take its log). argmax_o margin(o) is the beta -> infinity limit of
    argmax_o V_beta(o), for every tau > 0 (Section 5.2); this is what the
    beta = math.inf path of v_beta and downstream tasks must return.
    """
    raise NotImplementedError
```

---

## 10. Acceptance tests

Other tasks may run these against any implementation of Section 9's contracts.

1. **P1 oracle equivalence.** At `beta = 0, tau = 1`, `argmax_o v_beta(item, o, 0,
   1.0)` over every option must equal P1's frozen `o_bayes` for every item in P1's
   1,000-item set (`data/processed/items_final.parquet` in the P1 repo), including
   tie-break agreement. **Confirmed to exist for v2**: this file is present
   (1,000 rows, 38 columns) and carries an `o_bayes` integer column per item,
   alongside `o_fit`, `fit_cost`, `conflict`, `boundary_exact`, and `tile`
   (needed for Section 7.2's per-tile breakdown). Expected disagreement count:
   zero. If nonzero, that is the finding to report (per T1's brief); do not
   adjust the implementation to force agreement without first checking whether
   the P1 artifact or the new code is wrong.
2. **Large-beta / margin equivalence.** For every item, the `beta = math.inf` path
   of `v_beta`'s implied argmax (or `divergence_set`/`beta_critical` consumers
   using that path) equals `argmax_o margin(item, o)` exactly (not
   approximately): both are computed by the same closed form (Section 5.2), so
   they must match bit-for-bit modulo tie-break, not merely within tolerance.
3. **D(beta) monotonicity.** For a sample of items and the reporting grid
   (Section 8.2), `i in D(beta)` implies `i in D(beta')` for every `beta' > beta`
   on the grid, and also across the closed-form crossing points directly (not
   only at grid points).
4. **Adversary best response is beta/tau-independent.** `adversary_best_response`
   returns the same hypothesis id regardless of the `beta` and `tau` used
   elsewhere in a test run (it takes neither argument, so this is a signature-
   level guarantee, but test that no implementation smuggles a hidden
   beta/tau-dependence into how `item` is prepared).
5. **V_beta is strictly decreasing in beta.** For a sample of item/option pairs
   and an increasing sequence of finite `beta` values, `v_beta` output is
   strictly decreasing (Section 6.3, `A_o, B_o, C_o > 0`), to within `eps_tie`.
6. **Single crossing.** For a sample of item/option-pair combinations, scanning
   `v_beta(item, o, beta, tau) - v_beta(item, o2, beta, tau)` over a fine grid of
   `beta in [0, 50]` shows at most one sign change, matching the closed-form
   root count of Section 6.3 (0 or 1). **Must treat any difference smaller than
   `eps_tie` (Section 8.2) as zero, not as a sign, before counting changes.**
   Verified numerically against real P1 data during this spec's authoring
   (60 items sampled from `items_final.parquet`, 4,000-point beta grid): a naive
   sign scan without the `eps_tie` floor reports spurious multiple crossings for
   option pairs whose `V_beta` values are nearly equal across a wide beta range
   (dense clusters of sign flips a hundredth of a beta-unit apart are the
   signature of this, not a real second root); applying `eps_tie` as a floor
   before comparing signs reduces the violation count to exactly zero, matching
   the proof. An implementation of this test that skips the `eps_tie` floor will
   report false failures, not a spec problem.
7. **Zero-denominator audit (inherited from P1's D29).** `f(o,h) > 0` for every
   `o, h` in every item (fit is strictly positive by construction, `src/fit.py`),
   so `sum_h f(o,h) > 0` always and `L(h|o)` is never a division by zero. Reuse
   P1's audit methodology (`src/oracle.py`, Step 3) rather than writing a new one.
8. **Tie-break determinism.** Permuting the iteration order of `O` or `H` in an
   implementation's internals must not change any returned id (`o*_0`, `d*(o)`,
   or the option returned as `argmax_o V_beta(o)` at a tie), since Section 6.2's
   tie-break is a total order, not an artifact of iteration order.
9. **`D(0)` is empty (Section 7.1, v2).** `divergence_set(items, beta=0, tau=1)`
   returns `[]` for every item set, including one deliberately constructed (or
   drawn from P1's `boundary_exact` items) to contain a `beta_c(i) = 0`
   boundary-tied item. This must hold even though `beta_critical` on that same
   item correctly returns `0.0`, not `math.inf` or a small positive number: the
   two functions are allowed, by Section 7.1, to disagree at exactly `beta=0`.

---

## 11. Version history

### v1 (2026-09-08)

Open items recorded for the author, not part of the citable spec above:

1. **tau.** P1 has no quantal-response listener at all (pure argmax). Resolved
   2026-09-08: tau fixed at 1, not swept in the main analysis. Full reasoning in
   Section 5.1; appendix-only sweep protocol specified there.
2. **Zero-free-parameter philosophy.** P1's design explicitly rejects introducing
   any temperature/softmax parameter anywhere (`src/fit.py`, `paper.tex`). P2
   necessarily introduces `beta` as a new free parameter to model persuasion
   budget; with `tau` fixed, `beta` is the only one. Flagged, not treated as a
   problem to solve, since D1-D5 in `docs/P2/foundation.md` already anticipate an
   adversary parameter.
3. **Notation.** P1's paper and code call the Scientist's choice an "option"
   (`O`/`o`), not a "signal" (`S`/`s`). This spec inherits `O`/`o`. The task
   briefs (T1-T9) and `prompt-plan.md` used `s`/`S` in prose at the time; resolved
   in v2 below rather than left as a standing aliasing note.
4. **beta reporting grid.** `prompt-plan.md`'s grid list is truncated
   (`{0, 0.25, 0.5, 1, 2, 4, }`). Completed here as `{0, 0.25, 0.5, 1, 2, 4, 8}` +
   infinity (Section 8.2). Confirmed by author for v2; not re-flagged below.

### v2 (2026-09-08)

Three changes, all author-directed, plus the closure of two v1 open items above:

1. **Option space defined (was undefined in v1).** Section 2 now states `O` is
   per-tile (author decision: per-tile is the main result), with exact counts
   `{3,3,4,6}` verified against `tiles.json` (v1's "2 to 7" range was wrong,
   never checked against the file). Section 2.1 fully specifies the joint
   (multi-tile, 216-option) alternative as a conditional, not-built, exploratory
   construction, resolved against P1's `D39` (quoted verbatim: multi-tile is
   explicitly an allowed **secondary condition**, "not part of the primary
   design," so it is not forbidden, only correctly demoted). Verified, per the
   constraint not to patch around a real break silently: the joint construction
   would not have broken either the tau=1 identity (Section 5.1) or the
   single-crossing/monotonicity proof (Section 6.3), since both are agnostic to
   how `O`/`L(.|o)` are built. The reason it is not primary is artifact
   incompatibility (no joint item exists in the frozen 200k pool or the frozen
   1,000-item set; `oracle.py`'s 216-option row is an unrelated Task-11
   diagnostic on fresh random draws) and the reintroduced cross-tile
   independence assumption D39 names, not a math failure.
2. **Gate disambiguation protocol added (Section 7.2), and `docs/P2/tasks/T6.md`
   patched.** The `{3,3,4,6}` option-count gradient is a built-in confound for
   T6's kill gate: a small `|O|` mechanically caps how large `|D(beta)|` can get,
   independent of whether an adversary effect exists. T6 Step 1 now reports
   divergence per tile, ordered by `|O|`, with a numeric interpretation rule
   (structural/inconclusive vs. clean negative vs. neither) preregistered now,
   before any Arm A number exists. The `10`-percentage-point threshold used
   there is flagged as this task's proposed operationalization, not a
   carried-over value.
3. **beta=0 tie-boundary bug fixed (Section 7.1).** `beta_c(i)` is an infimum
   and can legitimately equal `0` for an item whose `o*_0` is exactly tied with
   a rival at `beta=0` (P1's `boundary_exact` case is a live instance of this).
   The v1 spec's `D(beta) = {i : beta_c(i) <= beta}` would have put such an item
   in `D(0)`, contradicting the fact that `o*_0` is the argmax at `beta=0` by
   the tie-break rule, for every item, without exception. Fixed by defining
   `D(0) := {}` by convention (not derived from `beta_c`), leaving `beta_c`
   itself, and `D(beta)` for `beta > 0`, unchanged. Added as acceptance test 9.
4. **Notation unified.** `s -> o` and `S -> O` applied across
   `docs/P2/prompt-plan.md` and `docs/P2/tasks/T1.md` through `T9.md` (verified:
   `T1.md`-`T5.md` and `T9.md` had no actual signal-notation tokens to change,
   only unrelated possessives like "Paper 1's"; `T6.md`, `T7.md`, `T8.md`, and
   `prompt-plan.md` did). `docs/P2/tasks/T0.md` itself was left unedited, since
   the instruction named `T1.md` through `T9.md` specifically and `T0.md` is a
   completed, historical brief; `prompt-plan.md`'s embedded copy of the T0
   prompt *was* edited, since `prompt-plan.md` was named as a whole file. This
   creates a small, disclosed inconsistency between `tasks/T0.md` and
   `prompt-plan.md`'s T0 section (old `s`/`S` in the former, new `o`/`O` in the
   latter) — flag if that split was not intended. The Section 1 correspondence
   note and the old item 3 above are superseded and removed from the citable
   spec; there is no remaining aliasing to track.

### v3 (2026-09-09, this amendment)

Author-directed, following a T1 stop-and-report. T1 could not satisfy acceptance
test 1 as written and stopped rather than implementing around it.

1. **The listener posterior was wrong in v1 and v2 (Sections 1, 2).** The spec
   defined `L(h|o) = f(o,h) / sum_{h'} f(o,h')`, omitting the normalisation of
   `f` over the option set. P1 normalises first
   (`src/oracle.py::likelihood`, summing over the option axis, giving `P(o|h)`)
   and only then applies Bayes over hypotheses
   (`src/score_items.py::grid_stats`). Corrected in Section 2, with the
   two-step form written out. Measured on the frozen 1,000-item set: the v2
   formula gives **50 disagreements** with P1's `o_bayes` (70 with a plain
   argmax); the corrected formula gives **0**.

2. **v2's explanation of the 57/60 sample was wrong (recorded so it is not
   re-derived).** v2 attributed its three sample disagreements to
   `items_final.parquet`'s `o_bayes` coming from "TASK_14's resample-averaged,
   dual-gate fit computation." It does not. `score_items.py` computes `o_bayes`
   from the plain single-pass fit matrix `F0 = fit_matrix(d["v"], d["iv"])`;
   the 40 resampled draws feed only the separate `resample_stability` gate, and
   the Gaussian family feeds only `family_agree`. Neither touches `o_bayes`.
   The actual cause was the missing inner normalisation, in the spec, not in
   the artifact. **Nothing is wrong with `items_final.parquet`.**

3. **Tie-break citation corrected (Section 6.2).** The frozen rule is D51,
   `src/tiebreak.py::lex_obayes` at `TAU_MAIN = 1e-9` relative, not
   `oracle.py`'s `TIE_EPS = 1e-12`, which is a Task-11 diagnostic. Both
   reproduce `o_bayes` 1,000/1,000 with identical tie sets, so no result turns
   on it; D51 is the rule of record because it built the artifact.

4. **R1, R2, Section 6.3 and Section 7.1 re-verified under the corrected `L`.**
   Re-derived (Section 5.1 now shows `sum_h L(h|o) = 1` rather than asserting
   it) and re-run numerically against all 1,000 frozen items by
   `tests/test_adversary.py` in the P2 repo. Every one survives, because each
   uses `L(.|o)` only as a strictly positive distribution over `H`:

   | claim | how re-verified | result |
   |---|---|---|
   | `sum_h L(h\|o) = 1` | direct, all items x options | max deviation `1.8e-15` |
   | R1, `d*(o) = argmax_{h != h*} L(h\|o)` | brute force over every `d != h*`, at `tau in {0.5,1,2}` x `beta in {0.25,1,4}` | exact match, no beta/tau dependence |
   | R2 at `beta=0`, `tau=1`: `V_0(o) = L(h*\|o)` | direct | max deviation `1.8e-15` |
   | R2 at `beta=0` reproduces `o_bayes` | vs. frozen artifact | **0 / 1000** |
   | R2 as `beta -> inf` equals `argmax margin` | `beta = inf` path vs. `beta = 500` in log space | exact match |
   | Section 6.3 single crossing | 4,000-point beta grid, `eps_tie` floor | 0 violations |
   | Section 6.3 closed form vs. bisection | both computed independently | root exact to `8.9e-16` relative |
   | Section 7.1 monotone nesting of `D(.)` | reporting grid and crossing points | 0 violations |
   | Section 7.1 `D(0) = {}` | incl. `boundary_exact` items | holds |

   The `tau != 1` failure is also now a positive test rather than a remark:
   `argmax_o V_0(o)` at `tau in {0.5, 2}` disagrees with the `tau = 1` oracle on
   **127** of 2,000 item-tau cells, which is the concrete reason Section 8.1
   fixes `tau = 1`.

5. **Two numerical facts found by T1, recorded for downstream tasks.**

   - **`beta_c` must be bisected on the tie-broken argmax, not on a strict
     `V_beta(o') > V_beta(o*_0)`.** On the 200k candidate pool there are option
     pairs whose `V_beta` curves are equal to float64 across the whole range
     (roughly 3 items per 2,000 on the `size` tile). A strict comparison never
     fires on those and bisection cannot converge; Section 6.1's definition
     already says "argmax", which is the tie-broken argmax of Section 6.2, so
     the tie-aware indicator is the faithful reading and it also keeps
     `divergence_set` consistent with `beta_critical` as Section 9 requires.
     Consequence, expected and not an error: the bisected `beta_c` differs from
     the exact closed-form root by up to `2.2e-6` in `beta`, in both
     directions, because the selector flips when the two options separate by
     one D51 band rather than at exact equality. Both values are correct
     answers to different questions; `beta_critical` returns the bisected one.
   - **Rival ties are common and reach the index level.** Distinct concept
     pairs falling in the same bins have bit-identical fit vectors, so
     `argmax_{h != h*} L(h|o)` is tied for 28% of option-cells in the frozen
     set (tie sets up to 24 hypotheses). The tie is resolved deterministically
     by the item's own frozen means/clues order. `adversary_best_response`'s
     returned *identity* is therefore not invariant under reordering an item's
     concept lists, while `M(o) = L(d*(o)|o)` is; every downstream quantity
     (`V_beta`, `beta_c`, `margin`, `D(beta)`) depends on the tie set only
     through `M(o)`, so nothing downstream is affected. Flagged rather than
     resolved: if a permutation-invariant `d*` id is ever wanted, the canonical
     key would be the concept-pool ids, not the within-item positions, and that
     would be a spec change.

### v3.1 (2026-09-09, this amendment)

Author-directed, after a review of the T1 delivery. Four changes, none of which
alters a decision rule. Two proposed amendments were **withdrawn without
adoption** and are recorded below because a withdrawn amendment is part of the
record.

1. **Section 7.2: factual note, rule unchanged.** T1's per-tile existence rates
   over the pool show the rates are not monotone in `|O|` (`moves` at `|O|=3`
   exceeds `hold` at `|O|=4`) and that the within-`|O|=3` spread of `0.1403`
   exceeds the 3-to-4 step. Option count is therefore not the dominant driver of
   between-tile variance, which is what this section's framing assumed. The note
   is recorded; **the disambiguation criteria are unchanged**, because the pooled
   existence rate passes K1 and the criteria cannot fire. The mechanism question
   moves to T6 Step 4 as exploratory.

   **Withdrawn, not adopted:** a proposed rescue rule under which a failing
   pooled rate would not kill when the per-tile rates are monotone in `|O|` and
   the largest-`|O|` tile clears the threshold. Withdrawn for two reasons. It was
   proposed after T1's benchmark had incidentally computed the per-tile rates, so
   adopting it would have been choosing a gate rule after seeing the gate
   statistic. And its monotonicity condition is already false on the pool, so it
   would not have fired even if adopted.

2. **Section 9, `beta_critical`: the bisected value is the value of record.** A
   proposal to make the closed form primary was **withdrawn**: consistency with
   `optimal_option` and `divergence_set` beats exactness against a criterion
   nothing else uses, and the `~1e-6` difference is far below any stratification
   bin edge.

3. **Section 9, every contract taking `tau`: the guard is mechanical.**
   `tau != 1.0` must raise unless an explicit keyword-only `appendix` flag is
   passed. Section 5.1's prohibition was prose that nothing enforced. The
   measured justification (`127 / 2,000` item-tau cells disagree with the frozen
   oracle at `tau in {0.5, 2}`) is carried in the implementation's error message
   so the guard is not quietly removed.

4. **Chain of custody made checkable.** The implementation carries
   `SPEC_VERSION` and the test suite asserts it equals this document's header
   version, so a spec bump without a corresponding code review fails the suite.
   P1 gitignores `data/**`, so the frozen inputs cannot be pinned by commit from
   P2; T1's report records their sha256 instead:

   | artifact | sha256 |
   |---|---|
   | `items_final.parquet` | `ec79b071dcfabd6094f9a91a2278cce0a6008ffd304c9935bd96850437218289` |
   | `items_candidate.parquet` | `ac7d13189b26a58c963e3f3ac5c1d7d4330fcd304e95bd454b2c7e66a4b42774` |

**Where the K1 disclosure lives.** T1's benchmark computed K1's statistic as a
byproduct (pooled `|D(infinity)|/N = 0.1823`, `|D(8)|/N = 0.1795`, outcome 2,
pass). That is a preregistration matter, not a spec matter, and the dated
disclosure is in `docs/P2/PREREGISTRATION_v2.md`'s revision record. It is noted
here only so a reader of this section is not left to discover it elsewhere.

**Verified for the v2 amendment**: `data/processed/items_final.parquet` exists in
the P1 repo, 1,000 rows, and carries an `o_bayes` column (acceptance test 1,
Section 10). No change needed there.

**Numeric re-verification, the v2 amendment. Its conclusion about the 57/60 was
wrong; see v3 item 2. Kept as written for the record.** Re-ran the mathematical claims
(not the not-yet-written contracts, which have nothing to execute) against 60
real items sampled from `items_final.parquet`, computing `L(h|o)` directly from
`fit.py` and the raw property ratings: the `tau=1` identity (Section 5.1) held
exactly on all 60; the `beta -> infinity`/`margin` equivalence (Section 5.2)
held exactly on all 60; the single-crossing property (Section 6.3) held on all
60 once compared with the `eps_tie` floor (see the amended acceptance test 6
above; a naive scan without it reports false violations from near-equal option
pairs). Computed `argmax_o L(h*|o)` agreed with P1's stored `o_bayes` on 57/60;
the disagreements are consistent with `items_final.parquet`'s `o_bayes` coming
from `TASK_14`'s resample-averaged, dual-gate (exponential/Gaussian agreement)
fit computation rather than a single direct pass over the raw ratings, which
this quick check did not replicate. This is not evidence against the spec's
math (the three invariant properties above were exact); it is a reminder for
T1, already implicit in Section 9's "reuse by import" instruction: reproduce
P1's stored `o_bayes` by importing whatever P1 code path actually produced
`items_final.parquet`, not by recomputing fit from raw ratings independently.

> **Superseded by v3.** The resample/dual-gate attribution above is false:
> `o_bayes` is computed from the plain single-pass fit matrix, and the
> resampling feeds only `resample_stability`. The real cause was the missing
> inner normalisation in the v1/v2 Section 2, which v3 corrects. The closing
> instruction, reproduce `o_bayes` by importing P1's own code path, was the
> right instruction for the wrong reason, and T1 followed it: at full scale the
> corrected definition disagrees on 0 of 1,000 items, not 3 of 60.
