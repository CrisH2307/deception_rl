# P2 Foundation: The Adversary Effect and the RL Scientist

Deception Papers Roadmap, Paper 2. Literature survey, formal core, design skeleton,
and open decisions. Prepared 2026-09-08.

---

## 0. Research brief

**Topic.** Signal selection under a constrained channel when an informed adversary
shares the audience, and whether a learned policy recovers the adversary-aware
optimum that language models miss.

**RQ1 (normative).** Does the presence of an informed, responsive adversary change
*which* signal is optimal, and by how much, in the P1 task structure?

**RQ2 (descriptive).** Do LLMs shift their signal choice toward the adversary-aware
optimum when the adversary is made explicit in the task framing?

**RQ3 (constructive).** Can a reinforcement-learned Scientist policy recover the
adversary-aware optimum, and does a policy trained against one adversary transfer
to another?

**Angle.** P1 established that item-sensitivity is not alignment, because models sat
outside the salience–Bayes interval on the far side of salience. P2 asks whether
*game structure* is a second axis models are blind to: not just "are they hitting the
right target," but "do they notice the target moved." The claimed convergence is that
the adversary-augmented objective nests P1's objective exactly as a limiting case,
which makes P2 a strict extension rather than a new task.

**Reader.** ACL/EMNLP or AAMAS reviewer familiar with LLM social-deduction agents
but not with information design; secondarily an economics-adjacent reader who knows
Bayesian persuasion but not LLM evaluation.

---

## 1. Method note

Retrieval ran serially, not via parallel sub-agents (chat environment). Sources:
Semantic Scholar Graph API, arXiv API (metadata verified directly against the
official endpoint, so existence is confirmed for every arXiv entry), and web search
for the economics literature which is not on arXiv. Every reference below passed
existence verification. Claims are held to abstract-level detail; no method details
or numbers are asserted beyond what the abstracts state.

Coverage: seven sub-directions, each with three or more verified works. The one thin
area is human speaker behaviour under an adversarial audience, where no directly
relevant work was retrieved, marked as such in §5.

---

## 2. The formal core

This is the part that makes P2 a strict extension of P1 rather than a new paper
that happens to reuse the same board game.

### 2.1 Setup (P1, restated)

- Hypothesis space `H` of candidate solutions, `|H| = n`, true state `h* ∈ H`.
- Prior `π` over `H`.
- Signal space `S`: the Scientist's tile-marker configurations.
- Literal listener posterior `L(h | s) ∝ π(h) · fit(s, h)`, with `fit` the P1
  min-aggregation exponential-decay function (no free parameters).
- **P1 oracle:** `s*₀ = argmax_{s∈S} L(h* | s)`.

### 2.2 Adding the adversary

The Murderer knows `h*`, observes `s`, and speaks on an *unconstrained* channel while
the Scientist cannot speak at all. Model that asymmetry as a single persuasion budget
`β ≥ 0` applied to one nominated decoy `d ≠ h*`.

Honest investigators score hypotheses as `u(h) = log L(h | s) + β · 1[h = d]` and
choose by quantal response with temperature `τ`:

```
P(choose h) = exp(u(h)/τ) / Σ_{h'} exp(u(h')/τ)
```

Scientist utility is the adversary-worst-case probability of a correct accusation:

```
V_β(s) = min_{d ≠ h*} P(choose h* | s, d)
```

**Result 1 (adversary best response).** Promoting hypothesis `d` inflates the
softmax denominator by `L(d|s)^{1/τ} (e^{β/τ} − 1)`, which is increasing in
`L(d|s)`. So the adversary's best response is always to promote the *strongest
surviving rival*:

```
d*(s) = argmax_{h ≠ h*} L(h | s)
```

This is the formal statement of the intuition every DMHK player has: the Murderer
does not invent a story, they amplify the second-best reading of the Scientist's own
clue.

**Result 2 (the β continuum).** Substituting `d*(s)`:

```
V_β(s) = L(h*|s)^{1/τ} / [ Σ_h L(h|s)^{1/τ} + max_{h≠h*} L(h|s)^{1/τ} (e^{β/τ} − 1) ]
```

- At `β = 0` the second term vanishes and `argmax_s V_0(s) = argmax_s L(h*|s) = s*₀`.
  **P1's oracle is the β = 0 case exactly.**
- As `β → ∞`, `V_β(s) ≈ e^{−β/τ} · [ L(h*|s) / max_{h≠h*} L(h|s) ]^{1/τ}`, and the
  `e^{−β/τ}` factor is constant in `s`, so

```
argmax_s V_∞(s) = argmax_s margin(s),
  where margin(s) = log L(h*|s) − max_{h≠h*} log L(h|s)
```

**The adversary effect, stated precisely: the objective moves from max-posterior to
max-margin, continuously, indexed by β.**

### 2.3 The measurement instrument this buys

For each item `i`, the argmax of `V_β` is piecewise constant in `β`. Define:

- **Critical budget** `β_c(i)` = the smallest `β` at which `argmax_s V_β(i)` first
  differs from `s*₀(i)`. Computable exactly by enumeration over `S`.
- **Divergence set** `D(β) = { i : β_c(i) ≤ β }`.
- Items with `β_c = ∞` are **adversary-robust**: the same signal is optimal at every
  adversary strength. These are the built-in control items.

`β_c` is to P2 what `fit_cost` was to P1: an item-level, parameter-free scalar to
stratify on. The whole existing P1 stratification pipeline transfers.

**Why this matters for the LLM arm.** Outside `D(β)` the two oracles predict the same
signal, so a model that ignores the adversary is indistinguishable from one that
handles it. All discriminating power lives inside `D(β)`. This is the same logical
move P1 made by requiring a reference for the quantity of interest, applied one level
up.

---

## 3. Taxonomy of prior work

Six branches. Each is scored on the two axes that matter for P2: whether the setting
has a **computable optimum** (can you say how far from best a policy is, or only who
won), and whether the adversary is **responsive** (does it react to the signal, or is
it a fixed obstacle).

| Branch | Computable optimum | Responsive adversary | Semantic signals |
|---|---|---|---|
| B1 LLM social-deduction agents | no | yes | yes (free-form) |
| B2 Codenames and clue games | partial | no | yes (constrained) |
| B3 RSA / computational pragmatics | yes | no | yes |
| B4 Information design, competing senders | yes | yes | no (abstract) |
| B5 RL for LLM speakers, self-play | no | yes | yes (free-form) |
| B6 ZSC, robust and Byzantine MARL | partial | yes | no |

**No existing branch has all three.** P2's slot is the intersection of B2's constrained
semantic channel, B4's responsive competing sender, and B3's exact solvability, with
B5's training machinery as the method. That intersection is empty in the retrieved
literature.

### B1, LLM agents in social deduction games

The most crowded branch and the one P2 must differentiate hardest from.

Xu et al. (2023, arXiv:2310.18940) power LLM Werewolf agents with RL, having the LLM
generate diverse action candidates and an RL policy select among them, explicitly to
counter what they call intrinsic bias in LLM action choice inherited from training
data. This is the closest published statement of P1's finding, though diagnosed by win rate
rather than against an oracle. Rahimirad et al. (2025, arXiv:2506.17788) go the other
way in Avalon, externalising belief inference to a structured probabilistic model and
leaving language handling to the LLM, and report the first language agent to beat
human players in a controlled study; their framing that large reasoning models degrade
sharply when distilled to smaller real-time variants is directly relevant to Cris's
Qwen3 0.6B–8B ladder. Kopparapu et al. (2022, arXiv:2201.01816) predate the LLM wave
with Hidden Agenda, showing RL agents in a two-team social deduction environment learn
partnering and voting *without* natural-language communication, which is the honest
null P2's RL arm has to beat. Brandizzi et al. (2021, arXiv:2106.05018) study emergent
communication in Werewolf under the RLupus framework. Evaluation-side entries include
MINDGAMES (Wang et al. 2026, arXiv:2605.29512), a live arena spanning Colonel Blotto,
Iterated Prisoner's Dilemma, Codenames and Secret Mafia with 944 submitted agents,
whose finding that failure-heavy environments reward robustness to opponent errors as
much as strategic ability is a direct warning about win-rate-only evaluation in exactly
P2's setting. Also in this branch: DVM (Zhang et al. 2025, arXiv:2501.06695) on
controllable SDG agents, CaM-Wolf (Zhang et al. 2026, arXiv:2607.26393) on causal-aware
multimodal SDG agents, MafiaScope (Karpov, 2026, arXiv:2607.10645) on time-resolved
belief probing, QUACK (Yuan et al. 2026, arXiv:2605.27068) which argues explicitly that
outcome-only scoring cannot separate real reasoning from luck, and Kao et al. (2025,
arXiv:2601.13709) measuring LLM deception quality against human baselines.

**Reading:** the branch has converged on the diagnosis (outcome metrics are not enough)
without having a setting where a better metric is available. P1 and P2 supply one.

### B2, Codenames and constrained clue games

The nearest structural analogue, and the branch that shows the adversary effect in its
*static* form.

Stephenson et al. (2024, arXiv:2412.11373) propose Codenames as an LLM benchmark,
evaluating several frontier models across board setups and reporting that different
models exhibit distinct emergent behaviours and excel at different roles, and that LLM
agents generalise to a wider range of teammates than prior embedding-based
techniques. Bills, Archibald and Blaylock (2024, arXiv:2412.12409) is the most
methodologically adjacent work found:
they model partner uncertainty as a prior over language models combined with the
cognitive hierarchy, and use Bayesian inference over partner type to maximise expected
heuristic value. That is level-k reasoning about the *teammate*; P2's adversary is
level-k reasoning about an *opponent inside the audience*, and no retrieved work
combines the two. Siu (2022, arXiv:2212.14104) formulates Codenames as a Markov
decision process and applies SAC, PPO and A2C, reporting that none of them converge on
the full environment. The contrast with P2 is a property of Codenames itself rather
than of any one agent: the assassin is a fixed board tile, identified before the clue
is given, so a spymaster routes around a hazard whose location is known and static.
P2's adversary observes the signal first and only then picks which rival to promote,
so the ambiguity a signal leaves cannot be routed around in advance. Koyyalagunta
et al. (2021, arXiv:2105.05885) established the embedding-and-graph baseline
family. Hakimov et al. (2025, arXiv:2502.11707) use Codenames for ad-hoc
concept forming in LLMs. Shaikh et al. (2023, arXiv:2306.02475, ACL) and White et al.
(2024, arXiv:2408.04900) both attack cross-cultural common ground, the latter with an
RSA extension (RSA+C3), showing the branch already accepts RSA-style speaker models as
the right normative frame. Archibald and Brosnahan (2024, arXiv:2403.00823) study
adapting to unknown teammates. Pincus and Traum (2016, LREC) is the pre-neural anchor
for automatic clue quality.

**Reading:** Codenames' assassin is a fixed obstacle known in advance. DMHK's Murderer
picks their target *after* seeing the clue. That single change turns a constrained
optimisation into a game, and no Codenames work makes it.

### B3, RSA and computational pragmatics

Supplies the listener model and the normative vocabulary. White, Mu and Goodman (2020,
arXiv:2006.00418) amortise pragmatic reasoning into a speaker to avoid RSA's inference
cost, which is the technique P2's RL arm effectively repeats under an adversarial
utility. Zarrieß and Schlangen (2019, arXiv:1906.05518) handle pragmatic reference for
objects of unknown category. Newman, Cohn-Gordon and Potts (2019, arXiv:1909.07290)
argue for communication-based evaluation of NLG over n-gram overlap, which is the
generic form of P1's argument. Estienne et al. (2025, arXiv:2507.14063, EMNLP) extend
RSA to multi-turn collaborative dialogue.

**Reading:** every retrieved RSA variant assumes a cooperative or at worst
uninformative listener. An RSA speaker facing an informed saboteur in the audience is
not in the retrieved literature. `[unconfirmed: no work retrieved for adversarial RSA]`

### B4, Information design with competing senders

The theory branch that already contains P2's normative result in abstract form.

Kamenica and Gentzkow (2011, *AER* 101(6):2590–2615) established Bayesian persuasion
via concavification. Gentzkow and Kamenica (2017, *Review of Economic Studies*
84(1):300–322) study competition in persuasion and show the effect of competition on
information revelation is *ambiguous in general*, identifying a condition on the
information environment that is necessary and sufficient for equilibrium outcomes to
be no less informative than the collusive outcome; their companion (2017, *GEB*
104:411–429) extends this to rich signal spaces. Ravindran and Cui (arXiv:2008.08517)
treat the zero-sum case specifically and find that most zero-sum sender preferences
result in full revelation, the closest theoretical statement to DMHK's Scientist-vs-
Murderer structure, and a result P2 should either recover or explain away, since
DMHK's Scientist manifestly *cannot* fully reveal. Hossain et al. (2024,
arXiv:2402.04971) give the computational picture: finding equilibria in multi-sender
persuasion is PPAD-hard and even a single sender's best response is NP-hard, which is
precisely why a small exactly-solvable instance like P1's is valuable. Banerjee et al.
(2025, arXiv:2504.10459) study the price of competitive disclosure. On the robustness
side, Babichenko, Talgam-Cohen and Xu (arXiv:2105.13870) take an adversarial approach
to a sender ignorant of receiver utility, and Sapiro-Gheiler (arXiv:2109.11536) handles
maxmin preferences over receiver types.

**Reading:** the economics is mature, abstract, and computationally forbidding in
general. P2's contribution to this branch is an instance that is semantic, small
enough to solve exactly, and populated by real language models.

### B5, RL for LLM speakers and self-play

The method branch, and the source of P2's closest competitor.

**Zheng et al. (2025/2026, arXiv:2510.09087), "The Stackelberg Speaker."** This is the
single most important paper for P2's positioning. It formalises turn-based SDG dialogue
as a Stackelberg competition where the current player leads and strategically
influences the follower's response, then trains agents via RL to optimise utterances
for persuasive impact across three SDGs. This is "adversary effect plus RL speaker" as
a headline. P2 must differentiate on the axis it can win: the Stackelberg Speaker
optimises free-form utterances in settings with no ground-truth optimal message, so it
can report win rates and baseline comparisons but not distance from optimal. P1's task
has an exact oracle, and §2 shows the adversarial version does too. **The
differentiator is not the idea, it is the measurability.** Frame P2 as the audit
instrument that work of this kind currently lacks.

Sarkar et al. (2025, arXiv:2502.06060) train LMs for social deduction in an Among Us
environment with no human demonstrations, decomposing communication into listening
(predict environment information from discussion) and speaking (reward messages by
their influence on other agents), doubling win rates over standard RL. Their
influence-based speaker reward is the natural baseline for P2's RL arm, and the
contrast is sharp: their reward is *measured* influence on other agents, P2's is
*computed* against an oracle. SPIRAL (Liu et al. 2025/2026, arXiv:2506.24119) provides
the self-play infrastructure argument, showing multi-turn zero-sum self-play with
role-conditioned advantage estimation transfers reasoning gains across Qwen and Llama
families, directly relevant given Cris's existing Qwen3 ladder. GameTalk (Conchello
Vendrell et al. 2026, arXiv:2601.16276) trains LLMs for strategic conversation.

### B6, Zero-shot coordination and robust MARL

Supplies the transfer question in RQ3. Hu et al. (2020, arXiv:2003.02979) introduced
Other-Play for zero-shot coordination, showing self-play policies encode arbitrary
conventions that break with novel partners. Treutlein et al. (2021, arXiv:2106.06613)
formalise ZSC and its open problems. Cui et al. (2022, arXiv:2207.07166) apply k-level
reasoning to ZSC in Hanabi, the closest cognitive-hierarchy analogue on the RL side.
Wolski et al. (2026, arXiv:2608.03644) introduce cross-implementation cross-play,
varying implementation details rather than only random seeds, and find for Other-Play
that the standard single-implementation evaluation is in fact a reasonable proxy for
the more thorough scheme. Their finding is reassuring rather than damning; what P2's
transfer experiment should take from it is that they ran the check. On
adversaries inside a cooperative team: Li et al. (2023, arXiv:2305.12872) cast
Byzantine-robust cooperative MARL as a Bayesian game where any agent may act
worst-case, which is the MARL-native statement of DMHK's hidden-traitor structure;
Mguni et al. (2025, arXiv:2508.08800) add adversarial budget constraints, a device
close to P2's `β`. Yuan et al. (2023, arXiv:2305.05116) study communication-robust
MARL under noisy or adversarial channels.

---

## 4. Cross-branch synthesis

Three tensions the branches leave unresolved, all of which P2 can address.

**T1: everyone diagnoses outcome metrics, nobody replaces them.** QUACK and MINDGAMES
independently argue that win rate confounds strategic ability with robustness to
opponent error, and MINDGAMES documents a concrete error-survival confound in Secret
Mafia. Neither offers a reference optimum, because their settings do not admit one.
P1 built the reference; §2 shows it survives the addition of an adversary. This is the
cleanest contribution claim available to P2 and it does not depend on any model result.

**T2: the adversary is either fixed or unmeasurable.** Codenames has a fixed assassin
and computable clue quality (B2). SDG work has a strategic adversary and no computable
quality (B1, B5). Information design has both but no language (B4). The three
literatures do not cite each other much, and the gap sits precisely where they fail to
meet.

**T3: zero-sum theory predicts full revelation; DMHK cannot revenue that.** Ravindran
and Cui find most zero-sum competing-sender preferences yield fully revealing
equilibria. DMHK's Scientist obviously cannot fully reveal, the channel is too narrow.
The resolution is that the channel constraint, not the preference structure, is the
binding force, which is a point P2 can make cleanly and which the economics literature
does not study because abstract signal spaces are assumed rich. This is a genuine
theoretical contribution, small but real.

---

## 5. Where P2 sits

| Work | Responsive adversary | Exact optimum | Constrained semantic channel | LLM eval | RL |
|---|---|---|---|---|---|
| Stackelberg Speaker (2510.09087) | yes | no | no | yes | yes |
| Sarkar et al. (2502.06060) | yes | no | no | yes | yes |
| Siu Codenames DRL (2212.14104) | no | partial | yes | no | yes |
| Stephenson et al. (2412.11373) | no | partial | yes | yes | no |
| Bills et al. (2412.12409) | no | yes | yes | no | no |
| Hossain et al. (2402.04971) | yes | yes | no | no | no |
| **P2** | **yes** | **yes** | **yes** | **yes** | **yes** |

The row is not empty by luck. It is empty because exact optima require small tractable
instances, and small tractable instances are usually not semantic. P1 already paid the
cost of building one (SPoSE space, parameter-free fit function, exact Bayesian oracle
over 1,000 stratified items). P2 gets the adversarial extension nearly free, §2 adds
one scalar and reuses every artifact.

**Known gap, stated honestly:** no retrieved work studies whether *human* speakers
shift toward margin-maximising signals when told an adversary is in the audience.
`[unconfirmed: no work retrieved in this direction]` This is either an opportunity or
a warning that the effect has not been shown in humans either.

---

## 6. Design skeleton

Three arms, ordered by risk. Arm A cannot fail; Arm B is the headline; Arm C is the
contribution that makes it a method paper rather than an evaluation paper.

### Arm A, Normative (computation only, no models)

Compute `β_c(i)` for every item. Report the distribution of `β_c`, the growth of
`|D(β)|` in `β`, and what item properties predict a low `β_c`. Characterise how far
`s*_∞` sits from `s*_0` in posterior terms, the price of robustness.

Output: the adversary effect exists in this task, quantified, with no model in the
loop. **This result is guaranteed and it alone justifies the paper's setup section.**

### Arm B, Descriptive (LLM evaluation)

Same Qwen3 ladder and cross-family control as P1, three framings:

1. **F0, no adversary.** P1 replication, sanity check on artifact reuse.
2. **F1, adversary present.** The Murderer is described; their mechanism is not.
3. **F2, adversary mechanics stated.** The Murderer promotes the strongest rival.

Primary measure, restricted to `D(β)`: signed movement of the choice distribution from
`s*_0` toward `s*_∞`, against P1's existing reference set (salience, marginal null,
Bayes). Secondary: does F2 help where F1 does not, which separates "cannot represent
the adversary" from "was not told to."

Prediction from P1: little or no movement, and any movement uncorrelated with the
correct direction. If that holds, the headline is **game structure is a second axis of
misalignment: models do not merely miss the target, they do not notice it moved.**

### Arm C, Constructive (the RL Scientist)

Where RL earns its keep. Three candidate justifications; recommend the second:

- **C1 multi-round.** Scientist revises markers after failed accusations. Sequential,
  genuinely RL, but requires new game machinery and breaks P1's one-shot artifacts.
- **C2 unknown adversary (recommended).** The Murderer is not a best-responder but a
  learned, LLM, or human-like policy. The optimum is no longer computable in closed
  form, so it must be learned, and self-play between Scientist and Murderer is a
  two-player zero-sum game whose analytic minimax *is* computable from §2. **RL
  correctness can be verified against ground truth, which almost no MARL paper can
  do.** This is the strongest single result available in P2.
- **C3 scale.** Full 1,118-concept vocabulary where enumeration is infeasible. Weakest
  motivation; the interesting failure is not computational.

Policy class, cheapest first, per the project's cheap-first principle:

1. **Feature-scorer policy.** Linear or shallow scorer over oracle-computable features
   (posterior on `h*`, margin, rival gap, posterior entropy, salience). Trained by
   REINFORCE. Near-zero compute, and the learned weights *are* the result: they say
   directly how much margin versus posterior the policy weighs, and can be read against
   the analytic optimum.
2. **GRPO on Qwen3-0.6B/1.7B** with the same reward, only to answer the separate
   question of whether an LLM can be *trained* into the behaviour it does not exhibit
   zero-shot.

Transfer experiment (RQ3): train against the best-response adversary, evaluate against
an LLM adversary and a fixed-heuristic adversary. Run the cross-play check Wolski et al.
ran rather than assuming the standard evaluation generalises. Their result was that it
does hold up for Other-Play, and the reason that is informative is that they tested it.

---

## 7. Risks and kill criteria

| Risk | Detection | Response |
|---|---|---|
| `D(β)` is nearly empty at plausible `β` | Arm A, before any model runs | Adversary effect is not present in this signal space. Redesign `S` or increase `|H|`. **Run Arm A first for exactly this reason.** |
| Stackelberg Speaker is judged to scoop P2 | Reviewer response | Lead every framing with measurability, not with the adversary idea. Cite it as motivation, not as related work buried in §2. |
| RL beats the oracle | Arm C | Means the oracle is misspecified, not that RL is good. Treat as a bug. |
| Reusing P1 items invites a same-data objection | Design time | Re-stratify on `β_c` rather than `fit_cost`, and pre-register the reuse. |
| Three arms is two papers | Now | See Decision 1. |
| Human arm inherits P1's unresolved two-strategy split | Now | See Decision 3. |

---

## 8. Open decisions

Numbered for direct reply. Recommended default given in each.

**D1, Scope.** One paper with Arms A+B+C, or split (P2a = A+B, P2b = C)?
*Recommend A+B+C in one paper.* The phenomenon–failure–fix arc is what makes it a
contribution rather than another evaluation; splitting leaves P2a as an eval paper in a
crowded branch. But this is the biggest cost decision and it is yours.

**D2, Artifact reuse.** Reuse P1's frozen 1,000 items exactly, or redraw stratified
on `β_c` from the same 200,000-candidate pool?
*Recommend redraw from the same pool.* Keeps the vocabulary, fit function, and Format V
renderings frozen, changes only the stratification variable to the one that carries
P2's discriminating power. Preserves the direct P1 comparison since both come from the
same pool.

**D3, Human arm.** In or out for P2?
*Recommend out, with a one-paragraph note deferring it.* P1's human arm is unresolved
(the two-strategy split), and stacking an unresolved instrument under a new
manipulation compounds the problem. Arms A+B+C stand without humans.

**D4, RL policy class.** Feature-scorer only, or feature-scorer plus GRPO on Qwen3
small?
*Recommend feature-scorer first, GRPO as a stretch goal gated on Arm A and B results.*
Cheap-first, and the feature weights are more interpretable than a fine-tuned model.

**D5, Adversary's power (the one I need your ruling on most).** In real DMHK the
Murderer *chooses* the crime, so they select `h*` adversarially before the Scientist
signals. §2 models a weaker adversary who only promotes a decoy after the fact. Which
game are we studying?
- (a) **Decoy-only** (as in §2). Scientist faces a fixed `h*`, adversary responds to
  the signal. Nests P1 exactly, exactly solvable, cheapest.
- (b) **State-choosing.** Adversary picks `h*` to be maximally hard to signal, *then*
  promotes a decoy. Closer to the real game, strictly harder, and it changes the item
  distribution rather than the objective, which would break the P1 comparison.
- (c) **Both**, with (b) as a bounded extension section.
*Recommend (a) for the main result, (c) if Arm A finishes early.* Note that (b) is
plausibly its own paper.

---

## 9. Prompt-plan decomposition (shape only, pending D1–D5)

Once the decisions land, the work splits into independently promptable tasks. The
dependency structure is what matters, these are the natural parallel boundaries:

**Wave 0 (blocking, sequential):**
- T0: freeze the adversary game specification and the `β_c` computation contract.

**Wave 1 (fully parallel, no cross-dependencies):**
- T1: implement `V_β`, `β_c`, and `D(β)` over frozen P1 artifacts; run-time asserts.
- T2: item redraw and `β_c` stratification (depends on D2).
- T3: prompt-condition authoring for F0/F1/F2 with the Format V renderer.
- T4: related-work section covering B1, B2, B5 with the Stackelberg Speaker
  differentiation argument written explicitly.
- T5: preregistration v2 draft with predictions and kill criteria.

**Wave 2 (parallel, depends on Wave 1):**
- T6: Arm A analysis and figures.
- T7: Arm B model runs across the ladder and three framings.
- T8: RL environment and feature-scorer policy (depends on T1).

**Wave 3:**
- T9: transfer and adversary-swap experiments.
- T10: `verify_paper.py` extension recomputing P2's headline numbers.

Each task gets a self-contained prompt carrying its own context, contract, and
acceptance test, so they can be run in separate agent sessions without shared state.

---

## 10. Verified references

**Correction note (2026-09-09, T4).** Three descriptions in section 3 were corrected
after independent verification against the source abstracts: Stephenson et al.
(2412.11373), Siu (2212.14104) and Wolski et al. (2608.03644). The references were
always real; the descriptions were not. The Wolski et al. lesson in section 6 was
rewritten to match. Details are recorded in `docs/P2/related-work.md` section 11.2.

Every entry below was confirmed against the arXiv API or, for the economics entries,
against publisher records via web search.

**B1, LLM social deduction**
- Xu, Yu, Fang, Wang, Wu. Language Agents with Reinforcement Learning for Strategic Play in the Werewolf Game. arXiv:2310.18940
- Rahimirad, Gergerli, Romero, Qian, Olson, Stepputtis, Campbell. Bayesian Social Deduction with Graph-Informed Language Models. arXiv:2506.17788
- Kopparapu, Duéñez-Guzmán, Matyas, Vezhnevets, Agapiou, McKee, Everett, Marecki, Leibo, Graepel. Hidden Agenda: a Social Deduction Game with Diverse Learned Equilibria. arXiv:2201.01816
- Brandizzi, Grossi, Iocchi. RLupus: Cooperation through emergent communication in The Werewolf social deduction game. arXiv:2106.05018
- Wang et al. MINDGAMES: A Live Arena for Evaluating Social and Strategic Reasoning in Multi-Agent LLMs. arXiv:2605.29512
- Zhang, Lan, Chen et al. DVM: Towards Controllable LLM Agents in Social Deduction Games. arXiv:2501.06695
- Zhang, Yao, He et al. CaM-Wolf: Causal-Aware Multimodal Agents for Social Deduction Games. arXiv:2607.26393
- Karpov. MafiaScope: Non-Invasive, Time-Resolved Belief Probing for LLM Agents in Social Deduction Games. arXiv:2607.10645
- Yuan, Song, Li et al. QUACK: Questioning, Understanding, and Auditing Communicated Knowledge in Multimodal Social Deduction Agents. arXiv:2605.27068
- Kao, Vats, Davis. Hidden in Plain Text: Measuring LLM Deception Quality Against Human Baselines Using Social Deduction Games. arXiv:2601.13709

**B2, Codenames and clue games**
- Stephenson, Sidji, Ronval. Codenames as a Benchmark for Large Language Models. arXiv:2412.11373
- Bills, Archibald, Blaylock. Improving Cooperation in Language Games with Bayesian Inference and the Cognitive Hierarchy. arXiv:2412.12409
- Siu. Towards automating Codenames spymasters with deep reinforcement learning. arXiv:2212.14104
- Koyyalagunta, Sun, Draelos et al. Playing Codenames with Language Graphs and Word Embeddings. arXiv:2105.05885
- Hakimov, Pfennigschmidt, Schlangen. Ad-hoc Concept Forming in the Game Codenames as a Means for Evaluating Large Language Models. arXiv:2502.11707
- Shaikh, Ziems, Held et al. Modeling Cross-Cultural Pragmatic Inference with Codenames Duet. arXiv:2306.02475 (ACL)
- White, Pandey, Pan et al. Communicate to Play: Pragmatic Reasoning for Efficient Cross-Cultural Communication in Codenames. arXiv:2408.04900
- Archibald, Brosnahan. Adapting to Teammates in a Cooperative Language Game. arXiv:2403.00823
- Pincus, Traum. Towards Automatic Identification of Effective Clues for Team Word-Guessing Games. LREC 2016

**B3, RSA and pragmatics**
- White, Mu, Goodman. Learning to refer informatively by amortizing pragmatic reasoning. arXiv:2006.00418
- Zarrieß, Schlangen. Know What You Don't Know: Modeling a Pragmatic Speaker that Refers to Objects of Unknown Categories. arXiv:1906.05518 (ACL)
- Newman, Cohn-Gordon, Potts. Communication-based Evaluation for Natural Language Generation. arXiv:1909.07290
- Estienne, Ben Zenou, Naderi et al. Collaborative Rational Speech Act: Pragmatic Reasoning for Multi-Turn Dialog. arXiv:2507.14063 (EMNLP)

**B4, Information design and competing senders**
- Kamenica, Gentzkow. Bayesian Persuasion. *American Economic Review* 101(6):2590–2615, 2011
- Gentzkow, Kamenica. Competition in Persuasion. *Review of Economic Studies* 84(1):300–322, 2017
- Gentzkow, Kamenica. Bayesian persuasion with multiple senders and rich signal spaces. *Games and Economic Behavior* 104:411–429, 2017
- Ravindran, Cui. Competing Persuaders in Zero-Sum Games. arXiv:2008.08517
- Hossain, Wang, Lin, Chen, Parkes, Xu. Multi-Sender Persuasion: A Computational Perspective. arXiv:2402.04971
- Banerjee, Munagala, Shen et al. The Price of Competitive Information Disclosure. arXiv:2504.10459
- Babichenko, Talgam-Cohen, Xu. Regret-Minimizing Bayesian Persuasion. arXiv:2105.13870
- Sapiro-Gheiler. Persuasion with Ambiguous Receiver Preferences. arXiv:2109.11536

**B5, RL for LLM speakers and self-play**
- Zheng, Ye, Zhao, Wang. The Stackelberg Speaker: Optimizing Persuasive Communication in Social Deduction Games. arXiv:2510.09087
- Sarkar, Xia, Liu, Sadigh. Training Language Models for Social Deduction with Multi-Agent Reinforcement Learning. arXiv:2502.06060
- Liu, Guertler, Yu et al. SPIRAL: Self-Play on Zero-Sum Games Incentivizes Reasoning via Multi-Agent Multi-Turn Reinforcement Learning. arXiv:2506.24119
- Conchello Vendrell, Ruiz Luyten, van der Schaar. GameTalk: Training LLMs for Strategic Conversation. arXiv:2601.16276

**B6, ZSC and robust MARL**
- Hu, Lerer, Peysakhovich, Foerster. "Other-Play" for Zero-Shot Coordination. arXiv:2003.02979
- Treutlein, Dennis, Oesterheld et al. A New Formalism, Method and Open Issues for Zero-Shot Coordination. arXiv:2106.06613
- Cui, Hu, Pineda et al. K-level Reasoning for Zero-Shot Coordination in Hanabi. arXiv:2207.07166
- Wolski, Hoernle, Forkel et al. Is Inter-Seed Cross-Play Enough? arXiv:2608.03644
- Li, Guo, Xiu et al. Byzantine Robust Cooperative Multi-Agent Reinforcement Learning as a Bayesian Game. arXiv:2305.12872
- Mguni, Sun, Chen et al. Fault Tolerant Multi-Agent Learning with Adversarial Budget Constraints. arXiv:2508.08800
- Yuan, Chen, Zhang et al. Communication-Robust Multi-Agent Learning by Adaptable Auxiliary Multi-Agent Adversary Generation. arXiv:2305.05116

**Evaluation and strategic reasoning context**
- Zhang, Mao, Ge et al. LLM as a Mastermind: A Survey of Strategic Reasoning with Large Language Models. arXiv:2404.01230
- Zheng, Zhou, Wang. Beyond Nash Equilibrium: Bounded Rationality of LLMs and humans in Strategic Decision-making. arXiv:2506.09390
- He, Wu, Jia et al. HI-TOM: A Benchmark for Evaluating Higher-Order Theory of Mind Reasoning in LLMs. arXiv:2310.16755
- Street, Siy, Keeling et al. LLMs achieve adult human performance on higher-order theory of mind tasks. arXiv:2405.18870

**P1**
- Huynh. Consistency Without Alignment: Item-Sensitive Language Models Indistinguishable From Random. arXiv:2609.00576
