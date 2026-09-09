# Related work and positioning (Paper 2 draft)

Produced by T4. Derives from `docs/P2/foundation.md` sections 3, 5 and 10, and uses
the notation frozen in `docs/spec/adversary-game-v1.md` v2 (`o` for an option/signal,
`L(h|o)` for the literal-listener posterior, `beta` for the adversary's persuasion
budget, `beta_c(i)` for an item's critical budget, `D(beta)` for the divergence set).

Every reference cited below was verified independently during T4 against the arXiv
API or a publisher record. Section 11 records the verification outcome, including
three places where `foundation.md` section 3 states more than its sources support.
Section 11 is working material and is not part of the paper prose.

---

## 0. The nearest prior work, addressed first

The single closest published work to this paper is Zheng, Ye, Zhao and Wang's
Stackelberg Speaker (arXiv:2510.09087). It formalizes turn-based dialogue in social
deduction games as a Stackelberg competition, with the current speaker as a leader who
strategically shapes the follower's response, and trains agents by reinforcement
learning to optimize utterances for persuasive impact across three games. Read at the
level of a one-line summary, that is an adversary-aware speaker trained with RL, which
is also a one-line summary of this paper.

The difference is not the idea, it is what can be measured. The Stackelberg Speaker
optimizes free-form natural-language utterances in settings that admit no ground-truth
optimal message. Its evaluation is therefore necessarily relative: win rates and
comparisons against baselines and ablations. There is no quantity in that setting
corresponding to "how far from the best possible utterance was this one," because the
best possible utterance is not defined, let alone computable.

This paper's task is built so that the quantity exists. The signal space `O` is small
and enumerable, the listener is a parameter-free literal Bayesian model inherited
frozen from Paper 1, and the adversary's best response is solved in closed form
(`docs/spec/adversary-game-v1.md`, Section 4). The consequence is that for every item
and every adversary strength `beta` there is an exactly computable optimal signal,
that the argmax is piecewise constant in `beta`, and that the budget at which it first
moves, `beta_c(i)`, is an exact per-item scalar. A policy's distance from optimal is a
number, not a comparison.

So the contribution claimed here is measurability, not the observation that adversaries
change what a speaker should say. The Stackelberg Speaker is prior work this paper
builds on and takes as motivation. What this paper adds is the instrument that work of
that kind currently has no way to construct: an audit setting where the correct answer
is known at every adversary strength, so a model can be scored against it rather than
against another model.

---

## 1. Two axes, and a taxonomy

Prior work is organized here into six branches, each scored on the two properties that
determine whether this paper's question can even be asked in that setting. The first is
whether the setting has a **computable optimum**: can one report how far a policy is
from best, or only who won. The second is whether the adversary is **responsive**: does
it react to the signal that was sent, or is it a fixed obstacle fixed before the signal
is chosen.

| Branch | Computable optimum | Responsive adversary | Semantic signals |
|---|---|---|---|
| B1 LLM social-deduction agents | no | yes | yes (free-form) |
| B2 Codenames and clue games | partial | no | yes (constrained) |
| B3 RSA and computational pragmatics | yes | no | yes |
| B4 Information design, competing senders | yes | yes | no (abstract) |
| B5 RL for LLM speakers, self-play | no | yes | yes (free-form) |
| B6 Zero-shot coordination, robust MARL | partial | yes | no (abstract) |

No branch has all three. The slot this paper occupies is the intersection of B2's
constrained semantic channel, B4's responsive competing sender, and B3's exact
solvability, with B5's training machinery as the method. That intersection is empty in
the literature surveyed here.

---

## 2. B1: LLM agents in social deduction games

This is the most crowded branch, and the branch whose own critiques supply this paper's
motivation.

Xu et al. (arXiv:2310.18940) power LLM Werewolf agents with reinforcement learning:
the LLM performs deductive reasoning and proposes a diverse set of action candidates,
and an RL policy selects among them. The stated purpose is to mitigate what they call
intrinsic bias in LLM action choice, inherited from training data and producing
suboptimal play. That is close to Paper 1's finding, arrived at from the other
direction: Xu et al. diagnose the bias by win rate against opponents, Paper 1 diagnoses
it by distance from an oracle. Rahimirad et al. (arXiv:2506.17788) go the opposite way
in Avalon, externalizing belief inference to a structured probabilistic model and
leaving language handling to the LLM, and report the first language agent to defeat
human players in a controlled study, with a 67% win rate. Their observation that large
reasoning models degrade sharply when distilled to smaller real-time variants bears
directly on the Qwen3 ladder used in Arm B. Kopparapu et al. (arXiv:2201.01816) predate
the LLM wave with Hidden Agenda, a two-team social deduction environment in which RL
agents learn partnering and voting without natural-language communication at all. That
result is the honest null for this paper's Arm C: coordination behaviour can emerge
with no linguistic channel, so a language-based policy has to be shown to beat it
rather than assumed to. Brandizzi et al. (arXiv:2106.05018) study emergent
communication in Werewolf under the RLupus framework.

The evaluation-side entries in this branch are the important ones here, because they
diagnose precisely the problem this paper's setup solves.

MINDGAMES (Wang et al., arXiv:2605.29512) is a live multi-game arena that ran a
competition cycle assessing 944 submitted agents from 76 teams across Colonel Blotto,
Iterated Prisoner's Dilemma, Codenames and Secret Mafia. Its analysis reports that
leaderboard validity differs sharply across environments, that brittle rule adherence
is a major bottleneck, and, most relevant here, that failure-heavy environments can
reward robustness to opponent errors as much as strategic ability, with Secret Mafia
exhibiting a pronounced error-survival confound in that cycle. Secret Mafia is the
environment structurally closest to the game this paper abstracts from. The warning is
therefore direct: in exactly this family of settings, outcome scoring can rank an agent
highly for surviving other agents' mistakes.

QUACK (Yuan et al., arXiv:2605.27068) makes the complementary argument. Its position is
that environments scored only by game outcomes make it impossible to tell whether an
agent's language is grounded in what it perceived and did, or to identify the failure
modes behind its behaviour. Its statement-verification pipeline reconstructs each
agent's ground-truth trajectory from engine logs and checks every discussion claim
against it, finding that even the strongest frontier model evaluated hallucinates 15.1%
of its verifiable spatial claims and that 11.5% of accusations are strictly
unsupported. Related entries include DVM (Zhang et al., arXiv:2501.06695) on
controllable agents, CaM-Wolf (Zhang et al., arXiv:2607.26393) on causal-aware
multimodal agents, MafiaScope (Karpov, arXiv:2607.10645) on time-resolved belief
probing, and Kao et al. (arXiv:2601.13709) on measuring deception quality against human
baselines.

MINDGAMES and QUACK are allies, not competitors. Both argue that outcome-only scoring
cannot separate strategic ability from luck or from robustness to opponent error.
Neither supplies a reference optimum, because their settings do not admit one: QUACK's
answer is to audit claims against a ground-truth trajectory, which verifies grounding
rather than optimality. This paper's answer is the other half. Where they check whether
what an agent said was true of the world, this paper checks whether what an agent said
was the best thing it could have said, against a listener and an adversary whose
behaviour is solved rather than sampled.

---

## 3. B2: Codenames and constrained clue games

Codenames is the nearest structural analogue: a sender picks one signal from a
constrained space to point a receiver at a target set, and the quality of a clue is at
least partly computable. It is also where the difference this paper turns on shows most
clearly.

Stephenson et al. (arXiv:2412.11373) propose Codenames as an LLM benchmark, evaluating
several frontier models across board setups and reporting that different models exhibit
distinct emergent behaviours and excel at different roles, and that LLM agents
generalize to a wider range of teammates than prior embedding-based techniques. Bills,
Archibald and Blaylock (arXiv:2412.12409) are the most methodologically adjacent work
found: they model coarse semantic uncertainty as a prior over language models and
pragmatic uncertainty via the cognitive hierarchy, combine them into a single prior over
partner types, and use Bayesian inference over that prior to maximize the expected value
of a heuristic. That is level-k reasoning about a *teammate*. The adversary here is
level-k reasoning about an *opponent inside the audience*, and no retrieved work
combines the two. Siu (arXiv:2212.14104) formulates Codenames as a Markov decision
process and applies SAC, PPO and A2C, reporting that none of them converge on the full
environment. Koyyalagunta et al. (arXiv:2105.05885) established the embedding-and-graph
baseline family, Hakimov et al. (arXiv:2502.11707) use Codenames for ad-hoc concept
forming, Archibald and Brosnahan (arXiv:2403.00823) study adaptation to unknown
teammates, and Shaikh et al. (arXiv:2306.02475) and White et al. (arXiv:2408.04900) both
address cross-cultural common ground, the latter with an RSA extension, which shows the
branch already accepts RSA-style speaker models as the right normative frame. Pincus and
Traum (LREC 2016) is the pre-neural anchor for automatic clue quality.

The structural point is the assassin. In Codenames the assassin is a fixed board tile,
identified before the clue is given, and a spymaster's problem is to route around a
hazard whose location is known and static. Every treatment in this branch inherits that
structure, whether the assassin enters as a hand-specified penalty in an RL reward or as
a term in a heuristic. The adversary in this paper is not a location, it is a player: it
observes the signal and only then selects which rival hypothesis to promote. Formally
its best response is `d*(o) = argmax_{h != h*} L(h|o)`, the strongest surviving rival
under the signal actually sent (`docs/spec/adversary-game-v1.md`, Section 4). A fixed
hazard can be avoided by construction. A responsive one cannot, because whatever
residual ambiguity a signal leaves is exactly what the adversary will occupy. That
single change turns a constrained optimization into a game, and it is why the optimal
signal moves from maximizing the posterior on the truth to maximizing the margin over
the best rival, continuously in `beta`. No Codenames work makes that change.

---

## 4. B3: RSA and computational pragmatics

This branch supplies the listener model and the normative vocabulary. White, Mu and
Goodman (arXiv:2006.00418) amortize the cost of RSA computation into a speaker by
directly optimizing for successful communication with an internal listener model, which
is structurally what this paper's Arm C does under an adversarial utility rather than a
cooperative one. Zarrieß and Schlangen (arXiv:1906.05518) model a pragmatic speaker
referring to objects of unknown categories. Newman, Cohn-Gordon and Potts
(arXiv:1909.07290) argue for communication-based evaluation of natural language
generation in place of n-gram overlap, which is the general form of Paper 1's argument
that a signal should be scored by what it does to a listener. Estienne et al.
(arXiv:2507.14063) extend RSA to multi-turn collaborative dialogue.

Every RSA variant retrieved assumes a listener who is cooperative, or at worst
uninformative. An RSA speaker facing an informed saboteur inside the audience does not
appear in the literature surveyed here. That is a statement about what was retrieved,
not a proof of absence, and it is worth being explicit that the absence is the reason
this paper defines its adversary inside the listener's scoring rule rather than as a
separate channel: `u(h) = log L(h|o) + beta * 1[h = d]` keeps the literal listener
frozen from Paper 1 and adds exactly one parameter.

---

## 5. B4: Information design with competing senders

The economics of this problem is mature, and it already contains this paper's normative
result in abstract form.

Kamenica and Gentzkow (*American Economic Review* 101(6):2590-2615, 2011) established
Bayesian persuasion, deriving conditions under which a sender who commits to a signal
structure strictly benefits from persuading a receiver whose action affects them both.
Gentzkow and Kamenica (*Review of Economic Studies* 84(1):300-322, 2017) study
competition in persuasion and show that the effect of competition on information
revelation is ambiguous in general, identifying a condition on the information
environment that is necessary and sufficient for equilibrium outcomes to be no less
informative than the collusive one. Their companion paper (*Games and Economic
Behavior* 104:411-429, 2017) extends the analysis to multiple senders with rich signal
spaces, showing that adding senders cannot decrease the amount of information revealed.
Ravindran and Cui (arXiv:2008.08517) treat the zero-sum case directly, characterizing
when all equilibria are fully revealing and finding that most zero-sum sender
preferences result in full revelation. That is the closest theoretical statement to this
paper's Scientist-against-Murderer structure, and it is a result this paper must either
recover or explain away, because the Scientist here manifestly cannot fully reveal.
The resolution is that the binding force in this task is the channel constraint rather
than the preference structure: `|O|` is between three and six options per tile, so full
revelation is not in the signal space at all, whereas the competing-sender results
assume signal spaces rich enough to support it. Banerjee et al. (arXiv:2504.10459)
study the price of competitive information disclosure. On the robustness side,
Babichenko, Talgam-Cohen and Xu (arXiv:2105.13870) treat a sender ignorant of receiver
utility, and Sapiro-Gheiler (arXiv:2109.11536) handles maxmin preferences over receiver
types.

Hossain et al. (arXiv:2402.04971) supply the computational picture and, with it, the
argument for why this paper's instance is worth building. They prove that finding an
equilibrium in multi-sender persuasion is PPAD-hard, and that even computing a single
sender's best response is NP-hard, which is why their own approach turns to
approximating local equilibria with a differentiable network. The hardness is not an
obstacle this paper overcomes: it is the reason a small, exactly solvable, semantic
instance has value. General multi-sender persuasion cannot be solved, so the field
approximates. A restricted instance that *can* be solved exactly, and that is populated
by real language models rather than abstract agents, gives a place to check what the
approximations are approximating. This paper's contribution to this branch is that
instance.

---

## 6. B5: RL for LLM speakers and self-play

This is the method branch and, as set out in Section 0, the source of this paper's
closest competitor.

The Stackelberg Speaker (Zheng et al., arXiv:2510.09087) is treated in full above. Its
relationship to this paper is best stated as division of labour rather than
competition. It demonstrates that adversary-aware speaker training works in a realistic
free-form setting, and reports that its agents outperform baselines across three games.
It cannot report by how much they fall short of optimal, because its setting has no
optimum to fall short of. This paper does not attempt the free-form setting. It builds
the constrained one in which the missing number exists, which is the complementary and
much smaller claim.

Sarkar et al. (arXiv:2502.06060) train language models for social deduction in an
embodied Among Us environment with no human demonstrations, decomposing communication
into listening, trained by predicting environment information from discussion, and
speaking, trained by rewarding messages according to their influence on other agents.
They report doubled win rates over standard RL. Their influence-based speaker reward is
the natural baseline for this paper's Arm C, and the contrast is sharp and worth
stating explicitly: their reward is *measured* influence on a population of other
agents, which is well defined but relative to whichever agents happen to be in the
population. This paper's reward is *computed* against a solved adversary and a frozen
listener. The first is available in any environment and tells you what worked against
these opponents. The second is available only in a solvable environment and tells you
what was best, full stop. SPIRAL (Liu et al., arXiv:2506.24119) supplies the
infrastructure argument, showing that multi-turn zero-sum self-play with
role-conditioned advantage estimation produces reasoning gains that transfer across
Qwen and Llama families, which is directly relevant given this program's existing Qwen3
ladder. GameTalk (Conchello Vendrell et al., arXiv:2601.16276) trains LLMs for strategic
conversation.

---

## 7. B6: Zero-shot coordination and robust MARL

This branch supplies the transfer question in RQ3, where a policy trained against the
best-responding adversary is evaluated against adversaries it was not trained on.

Hu et al. (arXiv:2003.02979) introduced Other-Play for zero-shot coordination, showing
that self-play policies encode arbitrary conventions that break with novel partners.
Treutlein et al. (arXiv:2106.06613) formalize zero-shot coordination and its open
problems. Cui et al. (arXiv:2207.07166) apply k-level reasoning to zero-shot
coordination in Hanabi, the closest cognitive-hierarchy analogue on the RL side. Wolski
et al. (arXiv:2608.03644) provide the methodological caution that this paper's transfer
experiment should absorb, and it is worth stating their result accurately: they
introduce cross-implementation cross-play, varying implementation details rather than
only random seeds, and find for Other-Play that the standard single-implementation
evaluation is in fact a reasonable proxy for the more thorough scheme. Their finding is
reassuring rather than damning, but the reason it is reassuring is that they checked,
and the check is what this paper's adversary-swap experiment should imitate.

On adversaries inside a cooperative team, Li et al. (arXiv:2305.12872) cast
Byzantine-robust cooperative MARL as a Bayesian game in which any agent may act
worst-case, represented as nature-dictated types, which is the MARL-native statement of
the hidden-traitor structure this paper abstracts. Mguni et al. (arXiv:2508.08800) add
adversarial budget constraints, a device close in spirit to `beta`. Yuan et al.
(arXiv:2305.05116) study communication-robust MARL under adversarial channels.

The gap this branch leaves is the same one as elsewhere. These settings have responsive
adversaries and no exact optimum for a *signal*: robustness is demonstrated by
performance under perturbation, not by distance from a best response that was computed.

---

## 8. The human-behaviour gap

One direction is deliberately not claimed here, and the precise shape of what is missing
matters, because it is easy to overstate.

Speech-production research on how speakers adapt to listeners frames the listener as
someone to help. Hazan and Baker (*Journal of the Acoustical Society of America*
130(4):2139-2152, 2011) show that speech produced with communicative intent to counter
genuinely adverse listening conditions differs acoustically from clear speech read
under imagined difficulty, and that the modifications are tailored to the condition.
Buz, Tanenhaus and Jaeger (*Journal of Memory and Language* 89:68-86, 2016) show that
feedback from an interlocutor changes speakers' subsequent pronunciations, with
hyper-articulation of a target increasing when partners occasionally misunderstand.
Gessa et al. (*Psychonomic Bulletin and Review*, 2026, doi:10.3758/s13423-026-02942-3)
show that speakers attend to non-verbal visual cues of listening effort and adjust their
communicative behaviour accordingly. In all of this work the audience is cooperative:
the speaker's problem is to reduce the listener's difficulty.

Experimental economics has studied competitive context effects on senders, but measures
a different dependent variable: honesty rate under misaligned incentives. Rode
(*Games and Economic Behavior* 68(1):325-338, 2010) runs a communication game in
cooperative and competitive contexts. Sutter (*Economic Journal* 119(534):47-60, 2009)
shows sophisticated deception through telling the truth in a sender-receiver
experiment, where a true message is chosen in the expectation that the receiver will
not follow it. Gneezy (*American Economic Review* 95(1):384-394, 2005) shows that under
conflictive preferences the probability of lying increases in the sender's gain and
decreases in the receiver's loss. Cai and Wang (*Games and Economic Behavior*
56(1):7-36, 2006) test Crawford-Sobel information transmission and find systematic
overcommunication relative to the most informative equilibrium. In all of this work the
question is whether the sender tells the truth.

Neither literature asks the question this paper asks: which signal a *truthful* sender
picks when a hostile co-speaker will exploit whatever ambiguity the signal leaves. The
sender here never lies. The choice is between true signals that differ in how much
residual ambiguity they leave for someone else to occupy. Pinker, Nowak and Lee
(*Proceedings of the National Academy of Sciences* 105(3):833-838, 2008) is the closest
bridge, proposing a game-theoretic account of indirect speech in which plausible
deniability protects a speaker against an uncooperative listener, and it is genuinely
about a mixture of cooperation and conflict in communication. But it concerns semantic
indirectness, the choice between saying a thing and implying it, not signal selection
against a computable optimum.

The claim being made is therefore narrow, and it is not that nobody studies adversarial
communication. It is that the specific question of margin-maximizing signal choice by a
truthful sender under a responsive adversary has not been posed as a normative question
with a computable answer, in either the speech-production or the experimental-economics
literature retrieved here. Paper 2 does not include a human arm, so this paper makes no
claim about what human speakers do. The gap is recorded as an opening for later work,
and as a caution: the effect has not been demonstrated in humans either.

---

## 9. Where this paper sits

Columns are defined as follows. *Responsive adversary*: a second party observes the
signal and then acts to defeat it. *Exact optimum*: the setting admits a computable
best signal against its own specified listener model, so distance from best is a
number. *Constrained semantic channel*: the signal space is meaning-bearing and small
enough to enumerate. *LLM eval*: language models are evaluated in the setting. *RL*: a
policy is trained.

| Work | Responsive adversary | Exact optimum | Constrained semantic channel | LLM eval | RL |
|---|---|---|---|---|---|
| Stackelberg Speaker (arXiv:2510.09087) | yes | no | no | yes | yes |
| Sarkar et al. (arXiv:2502.06060) | yes | no | no | yes | yes |
| Siu, Codenames DRL (arXiv:2212.14104) | no | partial | yes | no | yes |
| Stephenson et al. (arXiv:2412.11373) | no | partial | yes | yes | no |
| Bills et al. (arXiv:2412.12409) | no | yes | yes | no | no |
| Hossain et al. (arXiv:2402.04971) | yes | yes | no | no | no |
| **This paper** | **yes** | **yes** | **yes** | **yes** | **yes** |

The bottom row is not empty by luck. Exact optima require small tractable instances,
and small tractable instances are usually not semantic: the two properties pull against
each other, which is why the table's filled rows each give one of them up. Paper 1
(arXiv:2609.00576) already paid the cost of building an instance that has both, with a
human-derived similarity space, a parameter-free fit function and an exact Bayesian
oracle over a stratified item set. This paper gets the adversarial extension at low
marginal cost, because the adversary adds exactly one parameter to a frozen listener
and the resulting objective nests Paper 1's exactly at `beta = 0`
(`docs/spec/adversary-game-v1.md`, Section 5.1). The whole existing stratification
pipeline transfers, with `beta_c` in the role `fit_cost` played in Paper 1.

Three tensions across the branches summarize the position. First, everyone diagnoses
outcome metrics and nobody replaces them: MINDGAMES and QUACK independently argue that
outcome scoring confounds strategic ability with luck or with robustness to opponent
error, and neither offers a reference optimum, because their settings do not admit one.
Second, the adversary is either fixed or unmeasurable: Codenames has a fixed assassin
and partly computable clue quality, social deduction work has a strategic adversary and
no computable signal quality, information design has both but no language. Third,
zero-sum competing-sender theory predicts full revelation while this task's sender
cannot fully reveal, and the resolution, that the channel constraint rather than the
preference structure binds, is a small theoretical point that the economics literature
does not study because it assumes rich signal spaces.

---

## 10. References cited

**B1, LLM social deduction**
- Xu, Yu, Fang, Wang, Wu. Language Agents with Reinforcement Learning for Strategic Play in the Werewolf Game. arXiv:2310.18940
- Rahimirad, Gergerli, Romero, Qian, Olson, Stepputtis, Campbell. Bayesian Social Deduction with Graph-Informed Language Models. arXiv:2506.17788
- Kopparapu, Duéñez-Guzmán, Matyas, Vezhnevets, Agapiou, McKee, Everett, Marecki, Leibo, Graepel. Hidden Agenda: a Social Deduction Game with Diverse Learned Equilibria. arXiv:2201.01816
- Brandizzi, Grossi, Iocchi. RLupus: Cooperation through emergent communication in The Werewolf social deduction game. arXiv:2106.05018
- Wang et al. MINDGAMES: A Live Arena for Evaluating Social and Strategic Reasoning in Multi-Agent LLMs. arXiv:2605.29512
- Zhang et al. DVM: Towards Controllable LLM Agents in Social Deduction Games. arXiv:2501.06695
- Zhang et al. CaM-Wolf: Causal-Aware Multimodal Agents for Social Deduction Games. arXiv:2607.26393
- Karpov. MafiaScope: Non-Invasive, Time-Resolved Belief Probing for LLM Agents in Social Deduction Games. arXiv:2607.10645
- Yuan et al. QUACK: Questioning, Understanding, and Auditing Communicated Knowledge in Multimodal Social Deduction Agents. arXiv:2605.27068
- Kao, Vats, Davis. Hidden in Plain Text: Measuring LLM Deception Quality Against Human Baselines Using Social Deduction Games. arXiv:2601.13709

**B2, Codenames and clue games**
- Stephenson, Sidji, Ronval. Codenames as a Benchmark for Large Language Models. arXiv:2412.11373
- Bills, Archibald, Blaylock. Improving Cooperation in Language Games with Bayesian Inference and the Cognitive Hierarchy. arXiv:2412.12409
- Siu. Towards automating Codenames spymasters with deep reinforcement learning. arXiv:2212.14104
- Koyyalagunta, Sun, Draelos, Rudin. Playing Codenames with Language Graphs and Word Embeddings. arXiv:2105.05885
- Hakimov, Pfennigschmidt, Schlangen. Ad-hoc Concept Forming in the Game Codenames as a Means for Evaluating Large Language Models. arXiv:2502.11707
- Shaikh, Ziems, Held et al. Modeling Cross-Cultural Pragmatic Inference with Codenames Duet. arXiv:2306.02475
- White, Pandey, Pan et al. Communicate to Play: Pragmatic Reasoning for Efficient Cross-Cultural Communication in Codenames. arXiv:2408.04900
- Archibald, Brosnahan. Adapting to Teammates in a Cooperative Language Game. arXiv:2403.00823
- Pincus, Traum. Towards Automatic Identification of Effective Clues for Team Word-Guessing Games. LREC 2016

**B3, RSA and pragmatics**
- White, Mu, Goodman. Learning to refer informatively by amortizing pragmatic reasoning. arXiv:2006.00418
- Zarrieß, Schlangen. Know What You Don't Know: Modeling a Pragmatic Speaker that Refers to Objects of Unknown Categories. arXiv:1906.05518
- Newman, Cohn-Gordon, Potts. Communication-based Evaluation for Natural Language Generation. arXiv:1909.07290
- Estienne, Ben Zenou, Naderi et al. Collaborative Rational Speech Act: Pragmatic Reasoning for Multi-Turn Dialog. arXiv:2507.14063

**B4, Information design and competing senders**
- Kamenica, Gentzkow. Bayesian Persuasion. *American Economic Review* 101(6):2590-2615, 2011
- Gentzkow, Kamenica. Competition in Persuasion. *Review of Economic Studies* 84(1):300-322, 2017
- Gentzkow, Kamenica. Bayesian persuasion with multiple senders and rich signal spaces. *Games and Economic Behavior* 104:411-429, 2017
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
- Wolski, Hoernle, Forkel et al. Is Inter-Seed Cross-Play Enough? Evaluating the Robustness of Zero-Shot Coordination Algorithms to Implementation Details. arXiv:2608.03644
- Li, Guo, Xiu et al. Byzantine Robust Cooperative Multi-Agent Reinforcement Learning as a Bayesian Game. arXiv:2305.12872
- Mguni, Sun, Chen et al. Fault Tolerant Multi-Agent Learning with Adversarial Budget Constraints. arXiv:2508.08800
- Yuan, Chen, Zhang et al. Communication-Robust Multi-Agent Learning by Adaptable Auxiliary Multi-Agent Adversary Generation. arXiv:2305.05116

**Human speech production and experimental economics**
- Hazan, Baker. Acoustic-phonetic characteristics of speech produced with communicative intent to counter adverse listening conditions. *Journal of the Acoustical Society of America* 130(4):2139-2152, 2011
- Buz, Tanenhaus, Jaeger. Dynamically adapted context-specific hyper-articulation: Feedback from interlocutors affects speakers' subsequent pronunciations. *Journal of Memory and Language* 89:68-86, 2016
- Gessa, Valzolgher, Giovanelli et al. Will I speak louder if I see you struggling to understand? Speech modifications in response to non-verbal visual cues of listening effort. *Psychonomic Bulletin and Review*, 2026, doi:10.3758/s13423-026-02942-3
- Rode. Truth and trust in communication: Experiments on the effect of a competitive context. *Games and Economic Behavior* 68(1):325-338, 2010
- Sutter. Deception Through Telling the Truth?! Experimental Evidence From Individuals and Teams. *Economic Journal* 119(534):47-60, 2009
- Gneezy. Deception: The Role of Consequences. *American Economic Review* 95(1):384-394, 2005
- Cai, Wang. Overcommunication in strategic information transmission games. *Games and Economic Behavior* 56(1):7-36, 2006
- Pinker, Nowak, Lee. The logic of indirect speech. *Proceedings of the National Academy of Sciences* 105(3):833-838, 2008

**Paper 1**
- Huynh. Consistency Without Alignment: Item-Sensitive Language Models Indistinguishable From Random. arXiv:2609.00576

---

## 11. Verification appendix (not paper prose)

### 11.1 References that could not be confirmed

None. Every reference cited in Sections 0 through 10 was verified during T4.

Method. All 43 arXiv entries were queried directly against the arXiv API
(`export.arxiv.org/api/query?id_list=...`), and each returned a matching title and
author list. The eight non-arXiv entries named in the T4 brief, which are not in
`foundation.md` section 10 and so had not previously been verified, were checked
against publisher and index records: Hazan and Baker 2011 (JASA 130(4):2139-2152,
PubMed 21973368), Buz, Tanenhaus and Jaeger 2016 (JML 89:68-86, ScienceDirect
S0749596X15001631), Gessa et al. 2026 (Psychonomic Bulletin and Review, DOI
10.3758/s13423-026-02942-3, resolving via doi.org, PMC13269471), Rode 2010 (GEB
68(1):325-338, ScienceDirect S0899825609001249), Sutter 2009 (Economic Journal
119(534):47-60, DOI 10.1111/j.1468-0297.2008.02205.x), Gneezy 2005 (AER 95(1):384-394,
DOI 10.1257/0002828053828662), Cai and Wang 2006 (GEB 56(1):7-36, RePEc
gamebe:v:56:y:2006:i:1:p:7-36), Pinker, Nowak and Lee 2008 (PNAS 105(3):833-838, DOI
10.1073/pnas.0707192105). The three Kamenica and Gentzkow entries already in section 10
were re-checked against publisher records because they are quoted in the prose.
Pincus and Traum (LREC 2016) is carried from `foundation.md` section 10 on its prior
verification and is cited by name only, with no claim attached.

Note on author naming: arXiv lists the first author of arXiv:2510.09087 as "Zhang
Zheng", cited here as Zheng et al. following `foundation.md` and the T4 brief.

### 11.2 Corrections to `foundation.md` section 3

Three characterizations in `foundation.md` section 3 are not supported by the abstracts
of the works they describe. The reference entries themselves are correct in every case;
what fails is the description. This draft uses the corrected versions, and
`foundation.md` should be amended.

1. **Stephenson et al. (arXiv:2412.11373).** `foundation.md` states they "report a
   Spearman correlation of 0.821 between codemaster riskiness (average clue number) and
   loss rate, an empirical trace of the posterior-versus-margin trade-off." The
   abstract contains no such correlation. The number may appear in the body, but it was
   not verified here, so the claim is not repeated. This matters beyond bookkeeping:
   that correlation was the only cited empirical evidence that the posterior-versus-
   margin trade-off has already been observed in a neighbouring task, and it is
   currently unsupported.

2. **Siu (arXiv:2212.14104).** `foundation.md` states he "trains Codenames spymasters
   with deep RL, with a reward of -25 for hitting the assassin." The abstract reports
   that SAC, PPO and A2C all fail to converge on the Codenames environment, and states
   no reward values. The reward figure was not verified. This draft describes the work
   as an MDP formulation with non-convergent RL baselines, and makes the fixed-assassin
   argument from the rules of Codenames itself, which does not depend on any paper's
   reward shaping.

3. **Wolski et al. (arXiv:2608.03644).** `foundation.md` states they "question whether
   inter-seed cross-play is even an adequate ZSC evaluation, a caution P2's transfer
   experiment should absorb." The abstract reports the opposite conclusion: their
   findings are "encouraging" and suggest that for Other-Play, standard ZSC evaluation
   is a reasonable proxy for cross-implementation cross-play. The methodological lesson
   for this paper survives, but it is "run the check" rather than "the standard
   evaluation is inadequate", and this draft states it that way.

### 11.3 Bracketed markers removed

`foundation.md` carries two `[unconfirmed: ...]` markers, in section 3 branch B3 and in
section 5. Per the T4 anti-requirements these do not appear in prose. Both are stated
here as plain claims about what the survey retrieved: Section 4 for adversarial RSA,
Section 8 for the human-behaviour gap.
