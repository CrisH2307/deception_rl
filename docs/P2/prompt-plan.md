# P2 Prompt Plan: Adversary Effect and the RL Scientist

Decisions locked (all defaults):

| ID | Decision |
|---|---|
| D1 | One paper, Arms A + B + C |
| D2 | Redraw items from the same 200k pool, stratified on `β_c` |
| D3 | No human arm |
| D4 | Feature-scorer RL first; GRPO gated on Arm A and B results |
| D5 | Decoy-only adversary (adversary responds to the signal, does not choose `h*`) |

Every prompt below is self-contained. Each carries its own context block, so it can
be pasted into a fresh agent session with no shared state. Placeholders written as
`<<FILL>>` must be replaced with your repo specifics before pasting.

## Dependency graph

```
T0  (blocking, single session)
 |
 +-- T1  oracle implementation      \
 +-- T2  item redraw + stratification|
 +-- T3  prompt conditions F0/F1/F2  |  Wave 1, fully parallel
 +-- T4  related work + positioning  |
 +-- T5  preregistration v2         /
      |
      +-- T6  Arm A analysis        \
      +-- T7  Arm B model runs       |  Wave 2, parallel
      +-- T8  RL scientist          /
            |
            +-- T9  verification + repro bundle
```

**Do not start Wave 2 until T6's precondition is checked.** If Arm A shows the
divergence set is near-empty at plausible `β`, the adversary effect does not exist in
this signal space and Arms B and C are wasted compute. That check is the first thing
T6 does and it is a kill gate.

## Two spec parameters you should know about before T0 runs

1. **Listener temperature `τ`.** The margin result is a `τ → ` limit statement, but
   `β_c` values depend on `τ`. Default in T0: `τ = 1`, with `τ ∈ {0.5, 1, 2}` as a
   robustness sweep reported in an appendix. If P1 used a different listener
   sharpness, T0 must inherit it rather than pick fresh.
2. **`β` grid.** Default: `β ∈ {0, 0.25, 0.5, 1, 2, 4, }` on the log-odds scale,
   with `β_c` computed exactly by bisection rather than read off the grid. The grid is
   for reporting; `β_c` is continuous.

---

## T0, Freeze the adversary game specification (BLOCKING)

```
You are working on Paper 2 of a research program on signal selection under a
constrained channel. Paper 1 (arXiv:2609.00576, "Consistency Without Alignment") is
finished and its artifacts are frozen.

BACKGROUND YOU NEED

Paper 1 setup: a Forensic Scientist must choose one signal o from a small enumerable
signal space O to point Investigators at a true hypothesis h* inside a candidate set
H. A literal Bayesian listener forms L(h|o) proportional to prior(h) * fit(o,h),
where fit is a parameter-free min-aggregation exponential-decay function over a
human-derived similarity space. Paper 1's oracle is o*_0 = argmax_o L(h*|o).

Paper 2 adds an adversary. The adversary knows h*, observes o, and promotes one decoy
d != h* with persuasion budget beta >= 0. Honest investigators score
u(h) = log L(h|o) + beta * 1[h == d] and choose by quantal response with temperature
tau. The Scientist's utility is the adversary-worst-case correct-accusation
probability, V_beta(o) = min over d != h* of P(choose h* | o, d).

Two results have been derived on paper and MUST be re-derived and verified by you,
not assumed:
  R1. The adversary's best response is d*(o) = argmax over h != h* of L(h|o),
      because promoting d inflates the softmax denominator by
      L(d|o)^(1/tau) * (exp(beta/tau) - 1), which is increasing in L(d|o).
  R2. argmax_o V_0(o) = o*_0 exactly (Paper 1's oracle), and as beta -> infinity,
      argmax_o V_beta(o) -> argmax_o margin(o), where
      margin(o) = log L(h*|o) - max over h != h* of log L(h|o).

YOUR TASK

Produce a specification document at <<REPO>>/docs/spec/adversary-game-v1.md that is
the single source of truth every downstream task cites. It must contain:

1. Formal setup, notation matched to Paper 1's existing notation. Read Paper 1's
   codebase and paper source at <<PATH_TO_P1>> first and inherit its symbols. Do not
   introduce new notation where an existing symbol exists.
2. Full derivation of R1 and R2 with every step shown. If either is wrong, say so
   loudly and stop; do not patch silently.
3. The definition of beta_c(i): the infimum of beta at which argmax_o V_beta differs
   from o*_0 for item i. State the tie-breaking rule for argmax ties (default:
   lexicographic on a canonical signal ordering, stated explicitly) and prove or
   argue that argmax_o V_beta(i) is piecewise constant in beta so bisection is valid.
4. Definition of the divergence set D(beta) = { i : beta_c(i) <= beta } and the
   adversary-robust set { i : beta_c(i) = infinity }.
5. Chosen values: tau default and sweep, beta reporting grid, numerical tolerances,
   float precision, and how infinities are represented.
6. Function-signature contracts for downstream tasks, given as Python type stubs
   with docstrings but NO implementations:
     - v_beta(item, o, beta, tau) -> float
     - adversary_best_response(item, o) -> hypothesis_id
     - beta_critical(item, tau) -> float  # may return math.inf
     - divergence_set(items, beta, tau) -> list[item_id]
     - margin(item, o) -> float
7. A list of at least six acceptance tests other tasks can run against any
   implementation, including: beta=0 reproduces Paper 1's oracle on the frozen P1
   item set exactly; large-beta argmax equals argmax margin; beta_c is monotone in
   the sense that i in D(beta) implies i in D(beta') for beta' > beta.

CONSTRAINTS
- Inherit tau from Paper 1 if Paper 1 fixed a listener sharpness. Only choose fresh
  if Paper 1 used a pure argmax listener; say which case applies.
- No new free parameters beyond tau and beta. If you find yourself needing a third,
  stop and report it as a design problem.
- Do not write implementation code. Contracts only.

DELIVERABLE
The spec file, plus a short summary of anything in Paper 1 that does not transfer
cleanly and needs a decision from the author.
```

---

## T1, Implement the adversary oracle (Wave 1)

```
You are implementing the numerical core of Paper 2 in an existing research codebase.

INPUTS
- Specification: <<REPO>>/docs/spec/adversary-game-v1.md. Read it fully first. It is
  authoritative. If the spec is ambiguous, stop and report rather than guessing.
- Paper 1 codebase at <<REPO>>. The fit function, similarity space, prior, and
  Bayesian oracle already exist and are frozen. Find them; do not reimplement them.

TASK
Implement exactly the function contracts listed in section 6 of the spec:
v_beta, adversary_best_response, beta_critical, divergence_set, margin.

REQUIREMENTS
1. beta_critical uses exact bisection to a tolerance stated in the spec, not a grid
   lookup. Return math.inf for adversary-robust items.
2. Vectorize over items. The pipeline will run over 200k candidates in T2, so a
   pure-Python per-item loop is not acceptable. Benchmark and report throughput.
3. Reuse Paper 1's fit function by import. If you find yourself copying its code,
   stop: that is a duplication bug that will silently diverge.
4. Write the acceptance tests from section 7 of the spec as real tests, not
   assertions in a notebook. The beta=0 equivalence test must run against the actual
   frozen Paper 1 item set and pass with zero disagreements. If it does not pass,
   that is the finding; report it and stop.
5. Numerical hygiene: log-space throughout, no exponentiation of large arguments,
   explicit handling of the beta -> infinity limit as a separate code path rather
   than a large float.

ANTI-REQUIREMENTS
- Do not tune anything to make results look better.
- Do not silently clip, clamp, or regularize. If a value is degenerate, surface it.
- Do not add caching that changes results.

DELIVERABLE
Module + test suite + a short benchmark note. Report the beta=0 equivalence test
result as a single number: how many of Paper 1's items disagree. The expected answer
is zero.
```

---

## T2, Item redraw and beta_c stratification (Wave 1)

```
You are designing the item sample for Paper 2 of a research program.

CONTEXT
Paper 1 drew 1,000 items from a pool of roughly 200,000 candidates, stratified on a
scalar called fit_cost. Paper 2 needs a fresh draw from the SAME pool, stratified
instead on beta_c, the critical adversary budget at which the optimal signal flips.
Items with beta_c = infinity are adversary-robust and serve as built-in controls.

Rationale for redrawing rather than reusing: outside the divergence set the
no-adversary and adversary-aware oracles predict the same signal, so those items
carry no discriminating power for the model experiment. Stratifying on beta_c
concentrates the sample where the manipulation can be detected. Both draws come from
the same pool, so the Paper 1 comparison is preserved.

INPUTS
- Spec: <<REPO>>/docs/spec/adversary-game-v1.md
- Pool construction code from Paper 1 at <<PATH_TO_POOL>>. The pool, vocabulary, fit
  function, and rendering format are FROZEN. You change only the stratification
  variable.
- beta_c values come from T1's beta_critical(). Write your code against the contract
  in spec section 6. Do NOT write your own beta_c implementation; if T1 is not ready,
  stub the call and mark the stub clearly.

TASK
1. Characterize the beta_c distribution over the full pool: shape, mass at infinity,
   relationship to fit_cost (are these the same variable in disguise? if the
   correlation is above ~0.8, that is a finding and it weakens the redraw rationale,
   so report it prominently).
2. Design the stratification: bin edges over finite beta_c, quota for the
   beta_c = infinity control stratum, target n per cell. Justify bin edges against
   the distribution rather than picking round numbers.
3. Implement the sampler with explicit seed discipline matching Paper 1's convention.
   The draw must be exactly reproducible from the seed.
4. Produce the frozen item file plus a manifest recording seed, pool hash, bin edges,
   per-cell counts, and the spec version.
5. Report overlap with Paper 1's 1,000 items. Some overlap is fine and expected;
   quantify it so it can be stated in the paper.

ANTI-REQUIREMENTS
- Do not modify the pool, vocabulary, fit function, or rendering format.
- Do not drop items because they look inconvenient. If items must be excluded, the
  exclusion rule is stated before you look at beta_c values, not after.

DELIVERABLE
Sampler code, frozen item file, manifest, and a one-page characterization of the
beta_c distribution including the fit_cost correlation.
```

---

## T3, Prompt conditions F0 / F1 / F2 (Wave 1)

```
You are authoring the model-facing task presentations for Paper 2.

CONTEXT
Paper 1 presented a forced-choice signalling task to language models using a fixed
rendering called Format V. Paper 2 keeps the same task and the same rendering but
adds three framings that differ ONLY in how the adversary is described:

  F0  No adversary. Replicates Paper 1 exactly. Sanity check that artifact reuse
      did not change model behaviour.
  F1  Adversary present. The task states that one participant in the audience
      already knows the answer and wants the others to guess wrong. The mechanism
      by which they do this is NOT described.
  F2  Adversary mechanics stated. As F1, plus an explicit statement that the
      adversary will argue for whichever wrong answer your signal makes look most
      plausible.

The F1 versus F2 contrast is the load-bearing one. It separates "the model cannot
represent an adversarial audience" from "the model was never told how the adversary
works." Design them so that contrast is clean.

INPUTS
- Format V renderer and Paper 1 prompt templates at <<PATH_TO_PROMPTS>>.
- Spec: <<REPO>>/docs/spec/adversary-game-v1.md, section on the adversary model.

TASK
1. Write the three framings. F0 must be byte-identical to Paper 1's prompt where the
   content is shared; diff it and confirm.
2. Hold everything constant across F1 and F2 except the mechanism sentence. Same
   length category, same position in the prompt, same register. Report the word-count
   delta; if F2 is much longer than F1, add neutral filler to F1 rather than letting
   length confound the comparison.
3. Do NOT let the framing leak the answer. Verify: the adversary description must be
   computable from the task setup alone and must not reference the true hypothesis,
   the margin, or which signal is optimal. Write an automated check for this.
4. Produce a small set of adversarial-review cases: for each framing, three items
   where a careless wording would leak the answer, and show your wording does not.
5. Keep the response format identical across framings so parsing is unchanged.

ANTI-REQUIREMENTS
- Do not add chain-of-thought scaffolding, hints, or worked examples. Paper 1's
  finding is about zero-shot choice; changing the scaffolding breaks comparability.
- Do not use the words "margin", "maximize", "optimal", or "Bayesian" anywhere in
  any framing.

DELIVERABLE
Three prompt templates, the leak check, the length-parity report, and the F0 diff
against Paper 1 showing zero content drift.
```

---

## T4, Related work and positioning (Wave 1)

```
You are drafting the related-work section for Paper 2 of a research program.

CONTEXT
Paper 2 studies how the optimal signal changes when an informed adversary shares the
audience, and whether language models track that change. Paper 1 established that
models are item-sensitive but sit outside the salience-Bayes interval on the far side
of salience.

THE POSITIONING PROBLEM YOU MUST SOLVE
arXiv:2510.09087, "The Stackelberg Speaker: Optimizing Persuasive Communication in
Social Deduction Games" (Zheng, Ye, Zhao, Wang), formalizes turn-based social
deduction dialogue as a Stackelberg competition and trains an RL speaker for
persuasive impact. On the surface this is "adversary effect plus RL speaker", which
is Paper 2's headline. You must write related work so that a reviewer who knows this
paper does not conclude Paper 2 is derivative.

The real differentiator: the Stackelberg Speaker optimizes free-form utterances in a
setting with no ground-truth optimal message, so it can report win rates and baseline
comparisons but cannot report distance from optimal. Paper 2's task has an exactly
computable optimum at every adversary strength. The contribution is measurability,
not the idea that adversaries matter.

Do not bury this. Address it early and directly. A reviewer should finish the related
work section already knowing why the comparison is not fatal.

INPUTS
- The verified reference list at <<PATH>>/P2-foundation.md, sections 3, 5 and 10.
  Every entry there has passed existence verification. Do not add references you have
  not verified yourself against arXiv or a publisher record.

TASK
Write related work organized by the taxonomy in foundation section 3 (six branches),
with a comparison table matching foundation section 5. Required coverage:
- LLM social deduction agents, including the evaluation critiques (MINDGAMES's
  error-survival confound, QUACK's argument that outcome scoring cannot separate
  reasoning from luck). These are your allies: they diagnose the problem Paper 2
  solves.
- Codenames and constrained clue games, with the specific point that the assassin is
  a FIXED obstacle known in advance whereas this paper's adversary picks its target
  after seeing the signal.
- Information design with competing senders (Kamenica and Gentzkow 2011; Gentzkow and
  Kamenica 2017 REStud and GEB; Ravindran and Cui on the zero-sum case; Hossain et
  al. on PPAD-hardness). The hardness results are the reason a small exactly-solvable
  semantic instance is worth having.
- RL for LLM speakers, where the Stackelberg Speaker discussion lives.
- The human-behaviour gap, stated PRECISELY as follows and not more strongly:
  speech-production work frames the listener as someone to help (Hazan and Baker
  2011; Buz et al. 2016; Gessa et al. 2026); experimental economics has studied
  competitive context effects on senders but measures honesty rate under misaligned
  incentives (Rode 2010 GEB 68(1):325-338; Sutter 2009; Gneezy 2005; Cai and Wang
  2006). Neither asks which signal a TRUTHFUL sender picks when a hostile co-speaker
  will exploit residual ambiguity. Pinker, Nowak and Lee (2008 PNAS) is the closest
  bridge but concerns semantic indirectness, not signal selection against a
  computable optimum.

ANTI-REQUIREMENTS
- Do not claim novelty broader than the evidence supports. The claim is NOT "nobody
  studies adversarial communication." It is the narrow claim spelled out above.
- Do not cite anything you have not verified. One fewer reference beats one invented
  reference.
- No bracketed placeholder markers in the prose.

DELIVERABLE
Related-work draft plus the comparison table, and a separate list of any reference
whose existence you could not confirm (these get deleted, not flagged in the text).
```

---

## T5, Preregistration v2 (Wave 1)

```
You are writing the preregistration for Paper 2, following the convention established
for Paper 1 at <<PATH_TO_PREREG_V1>>. Read that first and match its structure.

CONTEXT
Three arms:
  A (normative)    Compute beta_c over the item set. No models. Characterize the
                   divergence set and the price of robustness.
  B (descriptive)  Language models across a size ladder plus a cross-family control,
                   three framings F0/F1/F2, measuring signed movement from the
                   no-adversary optimum toward the adversary-aware optimum, computed
                   only inside the divergence set.
  C (constructive) A reinforcement-learned Scientist policy under the adversarial
                   reward, verified against the analytically computable minimax.

TASK
Write the preregistration. It must contain, before any data is seen:

1. Directional predictions for every arm, with the reasoning. Paper 1's result
   implies the Arm B prediction is little or no movement, and any movement
   uncorrelated with the correct direction. State that as the prediction, not as a
   hope.
2. The primary measure for Arm B, stated as a formula, restricted to the divergence
   set, with the reference set (salience, marginal null, Bayes oracle, adversary
   oracle) named explicitly.
3. What distinguishes F1 from F2 and what each outcome pattern would mean. Fill in
   all four cells: no movement in either, movement in F2 only, movement in both,
   movement in F1 only (which would be strange and needs an explanation prepared).
4. KILL CRITERIA, stated numerically:
   - If the divergence set is below a stated fraction of items at the largest
     plausible beta, the adversary effect is absent in this signal space and Arms B
     and C do not run. State the fraction now.
   - If beta_c correlates with fit_cost above a stated threshold, the redraw
     rationale collapses and the design needs revisiting. State the threshold now.
   - If the RL policy outperforms the analytic optimum, that is an oracle
     misspecification bug, not a result. State that explicitly.
5. Multiple-comparison discipline across the model ladder, framings, and beta grid.
   Match Paper 1's convention.
6. Everything that is exploratory, listed as exploratory.

ANTI-REQUIREMENTS
- No outcome-contingent analysis choices.
- Do not write "we expect to find" for anything you would also accept the opposite of.

DELIVERABLE
Preregistration document, versioned, with a timestamp and a statement of what data
had been observed at the time of writing (should be: none beyond the beta_c
distribution needed to set bin edges, which is disclosed).
```

---

## T6, Arm A analysis (Wave 2, RUN FIRST, contains the kill gate)

```
You are running the normative arm of Paper 2. No language models are involved. This
arm cannot fail to produce a result, and it gates the other two arms.

INPUTS
- Spec: <<REPO>>/docs/spec/adversary-game-v1.md
- Oracle implementation from T1
- Frozen item set and manifest from T2
- Preregistration from T5, including the kill criteria

TASK, IN THIS ORDER

STEP 1, THE KILL GATE. Compute |D(beta)| / n at the largest beta in the reporting
grid. Compare against the preregistered threshold. If it fails, STOP, write up the
negative result, and report to the author that Arms B and C must not run. Do not
proceed past this step without an explicit pass.

STEP 2. Characterize beta_c: distribution over finite values, mass at infinity,
and growth of |D(beta)| in beta. Report the correlation with fit_cost against the
preregistered threshold.

STEP 3. The price of robustness. For each item in the divergence set, compute
L(h*|o*_0) - L(h*|o*_infinity): how much posterior mass on the truth the Scientist
gives up to buy margin. Report the distribution. This number is the paper's answer to
"how much does the adversary actually cost."

STEP 4. What predicts a low beta_c? Regress or otherwise relate beta_c to item
properties available in the manifest. This is exploratory unless preregistered; label
it as such.

STEP 5. Figures. At minimum: |D(beta)| versus beta; the beta_c distribution with the
infinity mass shown honestly rather than dropped; the price-of-robustness
distribution.

ANTI-REQUIREMENTS
- Do not run any language model in this task.
- Do not drop the beta_c = infinity items from plots because they are inconvenient to
  display. Show the mass.
- Every number that will appear in the paper must be emitted by a script into a
  results file, not read off a plot.

DELIVERABLE
Results file, figures, and a plain-language statement of whether the kill gate
passed, with the number.
```

---

## T7, Arm B model runs and analysis (Wave 2)

```
You are running the language-model arm of Paper 2.

PRECONDITION
T6's kill gate must have passed. Confirm this before spending any inference budget.
If you cannot confirm it, stop.

INPUTS
- Prompt templates F0/F1/F2 from T3
- Frozen item set from T2
- Oracle values (o*_0, o*_infinity, divergence set membership, beta_c) from T1/T6
- Paper 1's model ladder and inference harness at <<PATH_TO_HARNESS>>. Reuse it.
  Same models, same decoding settings, same parsing, same seeds convention.

TASK
1. Run the ladder across all three framings. Record raw outputs; never overwrite them.
2. F0 sanity check FIRST: does F0 reproduce Paper 1's reported result on the overlapping
   items? If not, artifact reuse has changed something and everything downstream is
   suspect. Report the comparison before analyzing F1/F2.
3. Primary analysis, restricted to the divergence set: signed movement of the choice
   distribution from o*_0 toward o*_infinity, F1 minus F0 and F2 minus F0, per model,
   with the preregistered uncertainty treatment.
4. Control analysis on the beta_c = infinity items: there should be NO movement there,
   because the optimal signal does not change. Movement there is a prompt-sensitivity
   artifact, not adversary awareness, and it caps how much of the divergence-set effect
   you can attribute. Report it as such.
5. Place every model against the full reference set from Paper 1 (salience, marginal
   null, Bayes) plus the new adversary oracle. The point is where models sit on the
   interval, not whether they beat a baseline.
6. Size-ladder analysis: does adversary sensitivity appear at any scale?

ANTI-REQUIREMENTS
- Do not retry, resample, or filter outputs to improve parse rates beyond the
  preregistered parsing rule. Report parse failures as data.
- Do not report win rates or accuracy as the headline. The headline is position
  relative to the references.
- If a model's behaviour is indistinguishable from the marginal null, say so plainly.

DELIVERABLE
Raw outputs, results file, figures, and an explicit statement of the F0 replication
result and the beta_c = infinity control result.
```

---

## T8, The RL Scientist (Wave 2)

```
You are building the reinforcement-learning arm of Paper 2. This arm exists to answer
a question the other two cannot: can a policy recover the adversary-aware optimum,
and does it transfer?

PRECONDITION
T6's kill gate must have passed.

WHY RL IS JUSTIFIED HERE, so you build the right thing
Against a best-responding adversary the optimum is computable, so RL would be
pointless. The justification is that the adversary is NOT assumed to be a best
responder. Scientist and adversary are co-trained in self-play, which is a two-player
zero-sum game whose analytic minimax IS computable from the spec. That means RL
correctness can be verified against ground truth, which almost no multi-agent RL work
can do. That verification is the arm's headline result, not the win rate.

INPUTS
- Spec: <<REPO>>/docs/spec/adversary-game-v1.md
- Oracle implementation from T1
- Frozen item set from T2

TASK
1. Build the environment: state is an item, Scientist action is a signal in O,
   adversary action is a decoy in H \ {h*}, reward is the correct-accusation outcome
   under the quantal-response listener. Verify the environment against the oracle:
   for a best-responding adversary and a max-V_beta Scientist, empirical reward must
   match V_beta analytically to within sampling error. Do this before any training.
2. Policy class: a low-dimensional scorer over oracle-computable features (posterior
   on h*, margin, rival gap, posterior entropy, salience), trained by REINFORCE.
   Start here, not with a fine-tuned language model. The learned weights are the
   result: they say directly how much margin versus posterior the policy weighs, and
   can be read against the analytic optimum at each beta.
3. Self-play: co-train Scientist and adversary. Report convergence toward the
   analytic minimax as the central verification. If it does not converge, diagnose
   whether the failure is the algorithm or the environment, and check the environment
   first.
4. Transfer: train against the best-response adversary, evaluate against (a) a
   fixed-heuristic adversary, (b) a language-model adversary. Report degradation.
   Absorb the caution from arXiv:2608.03644 that cross-play evaluation is itself
   fragile; state what your evaluation can and cannot conclude.
5. Ablation: does a policy trained at beta = 0 transfer to beta > 0? The prediction is
   no, and a clean negative here is a good result because it shows the adversary
   effect must be trained in rather than emerging.

GATED STRETCH GOAL, do not start without author sign-off
GRPO on a small instruct model with the same reward, to answer whether a language
model can be trained into behaviour it does not show zero-shot. Cost-gated.

ANTI-REQUIREMENTS
- If the RL policy beats the analytic optimum, that is a bug in the oracle or the
  environment. Treat it as a bug, find it, and report it. Do not publish it.
- Do not tune reward shaping to make learning curves look better. Report the reward
  as specified.
- Do not report only final performance. Report the learned feature weights; they are
  more informative than the score.

DELIVERABLE
Environment, policy code, the environment-versus-oracle verification result, the
self-play convergence result against analytic minimax, transfer numbers, the beta = 0
ablation, and the learned weight trajectories.
```

---

## T9, Verification and reproducibility bundle (Wave 3)

```
You are extending the verification tooling for Paper 2, following the convention
established for Paper 1 at <<PATH_TO_VERIFY_SCRIPT>>. Read that first.

CONTEXT
Paper 1 shipped a script that recomputes every headline number in the paper from
frozen artifacts, so that a reader can check the claims without trusting the prose.
Paper 2 must do the same.

TASK
1. Extend the verification script to recompute every number that appears in Paper 2's
   abstract, results tables, and figure captions, from the frozen artifacts and the
   committed seeds.
2. Every number in the paper source must be either produced by the script or flagged
   as unverified. Produce the list of unverified numbers; the target is empty.
3. Verify the chain of custody: item file hash matches manifest, manifest cites the
   spec version, spec version matches the one T1 implemented against. A mismatch
   anywhere is a hard failure.
4. Re-run the T1 acceptance tests as part of the bundle, including the beta = 0
   equivalence to Paper 1's oracle.
5. Package: artifacts, seeds, environment pin, and a single command that reproduces
   the paper's numbers end to end. Time it and report the wall-clock cost.

ANTI-REQUIREMENTS
- Do not hardcode expected values. The script recomputes; it does not assert against
  numbers copied from the draft.
- If a number in the draft does not reproduce, that is a finding about the draft. Fix
  the draft, not the script.

DELIVERABLE
Extended verification script, the unverified-numbers list, the chain-of-custody
report, and the reproduction command with its runtime.
```

---

## Notes on running these in parallel

- **T0 must complete before anything else.** Every Wave 1 prompt cites the spec file
  by path. If you paste Wave 1 tasks before T0 exists, they will invent their own
  definitions and diverge.
- T2 depends on T1's `beta_critical` contract but not its implementation. It can start
  immediately against the stub. Reconcile when T1 lands.
- T4 and T5 have no code dependencies and can start the moment T0 is written.
- T6 is the gate. Do not authorize T7 or T8 inference or training budget until T6
  reports a pass with a number.
- If any task reports that a spec assumption is wrong, stop the wave and fix T0. A
  spec change mid-wave is cheaper than reconciling three divergent implementations.
