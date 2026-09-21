# PREREGISTRATION v2.19

**Paper 2: the adversary effect and the RL Scientist**

Version 2.19 · written 2026-09-21 · amends `PREREGISTRATION_v2.md` (v2.0) and follows
`v2.1` through `v2.18`.

**Status.** New file per Paper 1's **D148**. `v2.0` through `v2.18` are not edited. This
version rules one question, **before the number exists**: whether a change rate on the
142-item `beta_c = infinity` control set, formed with quantity (a)'s own instrument, is
preregistered work under T7 step 4 or a new quantity. It records **P2-D27**.

**Decided by an agent session acting on an author instruction**, per the countermeasure in
`v2.10` section 2.4. The session is not the author. It wrote this document and P2-D27 from
the instruction quoted in section 1.

**This session computed no statistic.** It ran no analysis `main()`, did not call
`c5_movement` on the control set, and read nothing on `data/raw_t7/`. Section 8 discloses
what it knew and the one thing it knows about the uncomputed rate.

**What is unchanged.** `p0` is 0.5. The confirmatory family is 21 tests at
`alpha = 0.05/21`. The confirmatory `n` is 108. No statistic, unit, tolerance, null, floor
or family moves. P2-D5, P2-D6, P2-D12, P2-D24, P2-D25 and P2-D26 are not reopened.

| # | ruling | where |
|---|---|---|
| 1 | The control change rate is NOT preregistered under T7 step 4. It is a new quantity. | §3 |
| 2 | P2-D25 is silent on it: it neither declined nor authorized one. | §4 |
| 3 | It is authorized now, exploratory under `v2.0` section 10, fully specified. | §5 |
| 4 | The comparison with (a) is side by side and nothing beyond. | §6 |

---

## 1. The instruction

Quoted in the parts that bear on the ruling.

> You rule. **You compute nothing.**
>
> Quantity (a) is a change rate: the share of rendering pairs whose chosen option differs
> between a framing and `F0`, on the 108 confirmatory items, formed by
> `c5_effect.c5_movement` with P2-D16's pairwise exclusion and P2-D8's cluster bootstrap.
> The 142-item `beta_c = infinity` control on the `size` tile is reported in **TV** under
> P2-D25, in `results/T7_control_marginal_null.json`. The two are in different units, so a
> reader cannot compare them, and the control is what bounds what (a) means.
>
> **Rule: is a change rate on the 142-item control set, formed with quantity (a)'s own
> instrument, preregistered work under T7 step 4, or is it a new quantity P2-D25 did not
> authorize?**
>
> The author's read is that it is preregistered. **Evaluate that, do not adopt it.** Rule it
> on the record.
>
> It is not adversary-relevant in any way P2-D26 blocks: `A` is undefined on the control set
> and (a)'s instrument never reads `A`. Say whether you agree with that too, rather than
> taking it.
>
> ## THE HARD LINE: compute nothing
>
> Verify the record by reading. Do not compute the control change rate, do not run
> `c5_movement` or any analysis `main()` on the control set, do not touch `data/raw_t7/`
> for any aggregate. You have already seen quantity (a)'s values and the control's TV
> values, because they are on `main`; **record that ordering disclosure explicitly** in
> your entry, the way P2-D23 recorded what was known before its ruling. The control change
> rate itself must not be known when you rule.

and the required content: preregistered or new, with the textual ground; if authorized, a
complete specification covering the pair unit and P2-D16's exclusion, P2-D8's bootstrap,
P2-D13's floor, the item-level count and the framings; what the comparison licenses; the
standing and the fate of the 21-test family; and, if not authorized, the outline sentence.

**Constraints, all followed.** Do not reopen P2-D5, P2-D6, P2-D12, P2-D24, P2-D25 or
P2-D26. Do not edit `docs/P2/RESULTS_OUTLINE.md` or anything in `results/`. Treat every
claim in the instruction as unverified. No em dashes.

---

## 2. Every claim in the instruction, checked against the record

| carried | checked against | verdict |
|---|---|---|
| local `main` at `17a7f41` or later | `git log --oneline -1 main`; `HEAD` equals it and is an ancestor | **holds**, both at `17a7f41` |
| (a) is formed by `c5_effect.c5_movement` with P2-D16's pairwise exclusion | `t7_armb.compute` calls `CE.c5_movement(kept, m, keep, "framing", BASE, arm)`; exclusion is `tie_reference.pair_frame`'s pivot and `notna` | **holds** |
| ...and with P2-D8's cluster bootstrap | `c5_movement` calls `TR.cluster_bootstrap_diff` and `t7_armb` emits `ci_lo`, `ci_hi`; but P2-D13's consequences say "The bootstrap loses its role in (a) and keeps it unchanged ... in (b)" | **holds of the computation, loose of the role.** The interval is emitted for (a) and carries no inferential role there. The control rate inherits exactly that status (§5) |
| (a) is on the 108 confirmatory items | `P2D23_CONFIRMATORY_N`, `t7_armb` `keep` from `size_tile_confirmatory` | **holds** |
| the control is 142 items on `size`, reported in `TV` under P2-D25, in `results/T7_control_marginal_null.json` | `control_bases.primary`: `tile` `size`, `n_items` 142, `arity` 6; `P2D25_CONTROL_TV_AUTHORIZED` | **holds** |
| `steps_not_run` records a change rate as not computed "under P2-D25" | the field reads "NOT COMPUTED ... P2-D25 does not authorize it: v2.0 section 4.4's control measure is TV and TV is what is computed. Compute no quantity P2-D25 did not authorize." The phrase "under P2-D25" is the results outline's, section 4 | **loose.** The artifact records non-authorization under the computing session's own instruction, not a ruling by P2-D25. §4 |
| T7 step 4 names "movement", "NO movement", "caps how much of the divergence-set effect you can attribute" | `docs/P2/tasks/T7.md` step 4, verbatim | **holds.** It names neither an instrument nor a unit |
| `A` is undefined on the control set | `v2.0` section 3.2: `ext_i > 0` iff `beta_c < infinity`; `T7.md` note 1 takes the domain from `isfinite(beta_c)` | **holds** |
| (a)'s instrument never reads `A` | `c5_movement` and `pair_frame` read `chosen_option` only; P2-D23's first verified claim; `tests/test_p2d27_control_change_rate.py` runs it on a frame with no geometry | **holds** |
| the control change rate is not adversary-relevant in any way P2-D26 blocks | P2-D26's text scopes to quantities "computed on that set", the confirmatory set | **holds, refined.** P2-D26 does not reach the control set at all. What it does reach is a derived share of (a) (§6) |
| P2-D17 and P2-D18 are retired; P2-D26 is the highest live number | `DECISIONS.md` | **holds**; this entry is P2-D27 |

---

## 3. Preregistered or new: NEW

**The author's read, stated in its strongest form.** After P2-D12, "movement" in Arm B means
quantity (a): P2-D12 says H-B's no-movement half "resolves on (a)". So T7 step 4's "there
should be NO movement there" names (a)'s instrument applied to the control, and the rate is
preregistered by step 4.

**It does not survive the record, on three independent grounds.**

**3.1 Step 4 predates the instrument it would need.** The sentence "caps how much of the
divergence-set effect you can attribute" entered `docs/P2/tasks/T7.md` in commit `13bb803`,
dated 2026-09-09. P2-D12 was decided on 2026-09-10, in commit `3233c02`. Until P2-D12,
Arm B's movement measure was mean `ΔA`, which cannot run on the control set. So on the day
step 4 was written, "movement" could not have meant a change rate. Reading it that way
reads a later decision's vocabulary back into an earlier sentence. The log records scope
expiry as a quantity moving out from under a sentence; this is the same failure pointed the
other way, a sentence extended to a quantity that did not exist when it was written.

**3.2 The preregistration that operationalizes step 4 names a different instrument, and
names one.** `v2.0` section 4.4: "Because `A` is undefined on the control set, the control
measure is the total variation distance between the model's marginal over canonical option
ids under `F1` (or `F2`) and under `F0`". The measure is singular and its reason is given.
T7's brief is a task list; the preregistration is where instruments are fixed. Where the two
differ in specificity, the preregistration governs what was preregistered.

**3.3 P2-D12's quantity is scoped to the confirmatory set.** "(a) INERTNESS: the same-option
change rate against zero, per model, on the full confirmatory `n`". P2-D8, P2-D13 and P2-D16
bind "any Arm B confirmatory analysis script" or name the confirmatory contrasts. None names
the control set.

**What the author's read gets right, and why this version authorizes rather than
declines.** `v2.0` section 4.4's **reason** for a separate control measure was that the
confirmatory measure needed `A`. P2-D12 replaced the confirmatory measure with one that
reads chosen options only, so that reason no longer excludes running (a)'s instrument on the
control. The rate is therefore admissible, and it is motivated by the record: `c5_effect.tv`'s
docstring, written before T7 ran, already says that "a high change rate with `tv` near zero
is churn", and `v2.17` section 7.1 applied that to the control. That is a reason to authorize
it now. It is not preregistration.

---

## 4. What P2-D25 said about a control change rate: nothing

P2-D25's decision text, its four rejected alternatives, `v2.16` in full and `P2D25_TEXT`
contain no mention of a change rate or a same-option rate on the control set. It did not
decline one, which would appear as a rejected alternative or a "NO" in the decision text,
as the successor cap and the mapping onto (c) do. It did not authorize one. It **did not
address** one.

`steps_not_run.step_4_control_change_rate` reflects **a conservative reading of that
silence** by the `v2.17` computing session, whose instruction said "Compute no quantity
P2-D25 did not authorize". `v2.17` section 3.6 lists it as "deliberately not computed" for
that reason and section 7.1 flags it as a gap the author may want to close. That was the
correct application of the computing session's instruction, and it is not a ruling in
P2-D25's text. The results outline's "not computed, under P2-D25" compresses the two into
one and should be re-cited to P2-D27.

The distinction matters because it decides what was needed now. Had P2-D25 declined the
rate, authorizing it would reopen P2-D25, which the instruction forbids. Because P2-D25 was
silent, authorizing it reopens nothing.

`tests/test_p2d27_control_change_rate.py::test_p2d25_is_silent_on_a_change_rate` asserts the
silence, so an edit that made P2-D25 address the rate would fail there and send a reader
back to this ruling.

---

## 5. Authorized now: the complete specification

**Standing.** EXPLORATORY under `v2.0` section 10, whose list of exploratory quantities ends
"and anything suggested by looking at the data". The rate was requested after (a) and the
control `TV` were published, so it belongs there, whatever its record-based motivation. It is
descriptive, it is labelled exploratory wherever it appears, and it is never written in
confirmatory language.

**The family.** It does not enter the confirmatory family. The family stays 21 tests at
`alpha = 0.05/21`. It does not enter P2-D8's second family either, which is the tie-rate
family and is not reopened. No `alpha` is spent.

**Every choice, fixed.**

| element | fixed as | why |
|---|---|---|
| instrument | `c5_effect.c5_movement`, unmodified | (a)'s own; any other instrument makes the side-by-side compare instruments |
| contrast | `col = "framing"`, `base = "F0"` | (a)'s |
| arms | `F1` and `F2`, one cell each per model | (a)'s fourteen cells; (a) has no `F2`-versus-`F1` cell |
| models | `tie_reference.LADDER`, all seven | (a)'s; `CTRL` is admissible under D111 because the rate reads chosen options only (P2-D15's mechanism) |
| item set | `t7_control.geometry()["robust_by_tile"]["size"]`: `~isfinite(beta_c)` and `tile == "size"`, 142 items | P2-D25's base; (a)'s tile, arity and menus |
| the 540-item base | **not computed** | mixes arities 3, 3, 4 and 6, whose chance switching rates differ, so it is comparable to (a) in neither direction; P2-D25's 540 was a requirement on `TV` and does not travel |
| choice rows | `t7_armb.load_t7()`'s `kept`: Format V, `rule == "pmi"`, `n_tied == 1`, empty `unscored_reason` | (a)'s |
| pair unit and exclusion | the (item, permutation) rendering pair, P2-D16's pairwise exclusion, as `pair_frame` applies it; attrition reported per cell by `t7_armb.attrition` with `P2D16_ATTRITION_FIELDS` | (a)'s |
| interval | emitted as `c5_movement` computes it: P2-D8's cluster bootstrap over items, 10,000 resamples, seed 20260910, `alpha = 0.05/21` | emitted as (a) emits it, and like (a)'s it carries no inferential role under a deterministic scorer (P2-D13) |
| P2-D13's floor | **not applied**, no `clears_the_floor` | the floor is the numerical convention for (a)'s inertness verdict on the confirmatory set; the control's expectation is its own, step 4's "NO movement", and `v2.17` already reports it failed on `TV`; a floor verdict on the rate would be a second verdict on the same expectation in a new instrument chosen after the first was seen |
| verdict flags | **none**: no `interval_excludes_zero`, no `excludes_no_effect`, no `null` field | no verdict on the control is authorized |
| item-level count | **reported**: `n_items_with_a_changed_pair`, beside the rate, with `item_denominator` | (a) reports one, and a side-by-side needs both |
| `tv_option_marginal` | **not emitted** | the control `TV` of record is P2-D25's, in `results/T7_control_marginal_null.json`; a second figure for the same cell would be formed on pair-surviving renderings and could differ from it |
| derived quantities | **none** | §6 |

**Emitted per cell, exactly `P2D27_FIELDS`, named as (a)'s `a_inertness` block names them:**
`change_rate_renderings` (from `mv["change_rate"]`), `change_rate_item_mean`,
`n_changed_pairs` (from `mv["n_changed"]`), `n_pairs`, `ci_lo`, `ci_hi`, `alpha`,
`n_items_with_a_changed_pair`, `item_denominator` (from `mv["n_items"]`). Beside them, an
`attrition_P2D16` block from `t7_armb.attrition`. The artifact also carries
`"standing": "exploratory (v2.0 section 10), P2-D27"` and the side-by-side licence of §6 as a
field.

**Where it goes.** A NEW artifact, `results/T7_control_change_rate.json`, with a report at
`reports/T7_control_change_rate.md`. It is emitted by a function in `src/t7_control.py`
invoked by a `--change-rate` flag and not by `main()`, so
`results/T7_control_marginal_null.json` is not rewritten and every existing `results/*.json`
stays byte-identical. The side-by-side is formed where it is read, by citing (a)'s key and
the control's key for the same cell; (a)'s values are not copied into the new artifact,
because a copied number is a number that can drift.

**The exact binding call**, made before anything is emitted:

```python
import c5_effect as CE, p2_decisions as P2D, t7_armb as T7, t7_control as TC
import tie_reference as TR

G = TC.geometry()
ctrl = G["robust_by_tile"]["size"]
keep = set(int(i) for i in G["ids"][ctrl])
kept, raw = T7.load_t7()

P2D.bind_control_change_rate(
    instrument=CE.c5_movement, contrast=("framing", "F0"), arms=("F1", "F2"),
    control_beta_c=G["cols"]["beta_c"][ctrl], control_tiles=G["tiles"][ctrl],
    reads_A=False, in_confirmatory_family=False, alpha=P2D.P2D6_ALPHA,
    emitted_fields=P2D.P2D27_FIELDS, derived_quantities=(), floor_applied=False)
P2D.bind_tie_exclusion(P2D.P2D16_EXCLUSION_UNIT, imputed_as_non_mover=False,
                       dropped_whole_item=False,
                       attrition_fields=P2D.P2D16_ATTRITION_FIELDS)

for arm in P2D.P2D27_ARMS:
    for m in TR.LADDER:
        mv = CE.c5_movement(kept, m, keep, "framing", "F0", arm)
        # emit P2D27_FIELDS from mv, and T7.attrition(raw, kept, m, keep, arm)
```

---

## 6. What the comparison licenses: side by side, and nothing beyond

**Licensed.** Per cell, the control change rate and its item count beside (a)'s, in the same
units, from the same instrument, with both denominators named. The sentence it supports is
flat: on items where the adversary cannot move the optimum, the same framing changes the
chosen option at this rate. By `v2.0` section 4.4's first paragraph that movement is prompt
sensitivity.

**Not licensed, each as a new quantity.** A difference (a) minus control, a ratio, an
"attributable share" of (a), and any test of (a) against the control rate. None is specified
anywhere in the record, so each would be written now. Three reasons, each sufficient.

1. **Post-hoc by ordering.** (a) is published on all fourteen cells, and the control's `TV`,
   which bounds the control rate from below (§8), is published too. A derived quantity
   written now is written with one end known and the other bounded, which is the ordering
   hazard P2-D12, P2-D21, P2-D24 and P2-D25 each declined.
2. **No transfer rule, and the sets differ by construction.** The 108 and the 142 are
   disjoint, and they differ in exactly the property the control exists to vary: `beta_c` is
   finite on one and infinite on the other. A difference or share treats the control rate as
   an estimate of prompt sensitivity **on the confirmatory items**, which needs a rule
   transferring a rate across item sets. No version writes one. `v2.16` section 5.4 already
   states the limit: the control "can show that generic movement exists. It cannot
   adjudicate whether the confirmatory movement is that movement." A share would be that
   adjudication. P2-D8's cluster bootstrap cannot supply one either: `cluster_bootstrap_diff`
   resamples one item set with two paired values per item, and these are two item sets.
3. **P2-D26.** A share of (a) read as the part the adversary explains is a claim about
   adversary content on the confirmatory set. P2-D26 makes every such claim unavailable,
   because the adversary-aware optimum and the salience pole are one option on all 108
   items, and no successor measure on `size` lifts that.

Writing any of them now would be post-hoc under reason 1 regardless of reasons 2 and 3.

---

## 7. The outline sentences

The outline session updates `docs/P2/RESULTS_OUTLINE.md` after this ruling is merged. This
session does not edit it. Two sentences.

**Until the rate is computed**, the "Needed and absent" entry under section 4 reads:

> A change rate on the 142-item control set, in quantity (a)'s units and from its
> instrument, is authorized by P2-D27 as exploratory and descriptive and is not yet
> computed. P2-D25 did not address it; it neither declined nor authorized one.

**Wherever the control and (a) appear together, whether or not the rate has been
computed:**

> The control change rate and quantity (a) are reported side by side in the same units and
> are not comparable as an attribution: they are taken on disjoint item sets that differ by
> construction in whether the adversary can move the optimum, no preregistered rule
> transfers a rate from one to the other, and no difference, ratio or share of the two is
> reported.

Until the rate exists, the outline's section 4.6 keeps the control in `TV` and the second
sentence's first clause is replaced by "The control is reported in `TV` and quantity (a) as
a change rate, so the two are not in the same units; even once the control change rate is
computed, they".

---

## 8. Ordering, disclosed

**What this session knew when it ruled**, because it is on `main` and the instruction
required reading it: all fourteen cells of quantities (a), (b) and (c), including (a) at 30
to 77 items of 108; the control `TV` on the 142, 0.0176 to 0.2782, and on the 540; the
attribution cap; `A_null` and the excess; P2-D26 and the results outline.

**What it read beyond the documents**: the key list, `control_bases` and `steps_not_run` of
`results/T7_control_marginal_null.json`, the key list of `results/T5_c5_effect.json`'s
`sets`, and `CTRL|F1`'s control rendering counts, 284 in each arm. Frozen model-free
geometry was read by the new test, to count the control base; no model choice was read.

**What it did not know: the control change rate on any cell.**

**What it does know about that rate, and why the ruling is therefore not fully blind.** For
paired renderings, the total variation distance between the two empirical marginals is at
most the share of pairs whose choice differs: each changed pair moves at most one unit of
mass. `t7_control` forms `TV` from each arm's surviving renderings separately, so on every
cell where those renderings are the ones that also survive P2-D16's pairing (as on `CTRL|F1`,
284 and 284), the control's rendering-level change rate is **at least** that cell's `TV`.
The session did not compute an upper bound, a value or an item-level figure.

**Why it does not matter to the ruling.** Nothing the ruling authorizes reads the value. No
derived quantity is authorized, so there is nothing for a known lower bound to be fitted
into. No verdict is attached, so there is no threshold for it to be fitted against. Every
choice in §5 is fixed by matching (a), not by the rate.

**What this session wanted a number for.** Whether the control rate would sit near (a)'s or
far below it. Near would make a share look like the natural summary; far would make the
side-by-side look like support for (a). Both are the pull toward a derived quantity chosen
with its value in view, which is why §6 forbids every one.

---

## 9. Alternatives offered and not chosen

Listed in full in P2-D27. In brief:

1. **Rule the control change rate preregistered under T7 step 4.** §3.
2. **Leave it uncomputed and state the control in `TV` only.** Leaves the outline with two
   numbers a reader cannot compare and leaves `v2.17` section 7.1's churn gap open, while
   buying no protection the side-by-side restriction does not.
3. **Authorize the rate together with a difference, ratio or attributable share against quantity (a).** §6.
4. **Apply P2-D13's floor to the control and emit a verdict flag.** §5, the floor row.
5. **Report the change rate on the 540-item all-tile base beside the 142.** §5, the
   540-item row.

---

## 10. What this version changes

- `docs/P2/DECISIONS.md` gains **P2-D27** and three standing-check rows.
- `src/p2_decisions.py` gains `P2D27_TEXT`, `P2D27_REJECTED`, the constants above and
  `bind_control_change_rate`, and `check_log` covers P2-D27 in both loops.
- `tests/test_p2d27_control_change_rate.py` is added.
- **No `results/*.json` changes**, verified by hashing every file before and after. No
  superseded preregistration version is edited. `docs/P2/RESULTS_OUTLINE.md` is not edited.
  No statistic is computed. `p0` is 0.5. The confirmatory family is 21 tests at
  `alpha = 0.05/21`. The confirmatory `n` is 108.
