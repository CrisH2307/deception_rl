# Paper 2: Adversary Effect and the RL Scientist

## Files

| File | What it is |
|---|---|
| `foundation.md` | Literature survey, formal core, positioning, verified references |
| `prompt-plan.md` | Full plan, dependency graph, locked decisions, all ten task briefs |
| `tasks/T0.md` ... `tasks/T9.md` | Individual task briefs, one per session |
| `DECISIONS.md` | Author decisions not derivable from the spec or the preregistration, with the alternatives not chosen. Bound at import by `src/p2_decisions.py` |
| `KAGGLE_T7.md` | How to upload, run and resume T7's scoring on Kaggle, and what to bring back |

The spec at `../spec/adversary-game-v1.md` is produced by T0 and does not exist yet.

## Locked decisions

| ID | Decision |
|---|---|
| D1 | One paper, Arms A + B + C |
| D2 | Redraw items from the same 200k pool, stratified on `beta_c` |
| D3 | No human arm |
| D4 | Feature-scorer RL first; GRPO gated on Arm A and B results |
| D5 | Decoy-only adversary (responds to the signal, does not choose `h*`) |

Decisions taken during a task, rather than locked before Wave 1, live in
`DECISIONS.md` under `P2-D<n>` ids. They are bound to the code that implements them
the way Paper 1's D100 binds its own: verbatim constant, asserted at import.

## Order of execution

```
T0  blocking, single session, author reviews output before Wave 1
 |
 +-- T1  oracle implementation      \
 +-- T2  item redraw                 |
 +-- T3  prompt conditions           |  Wave 1, parallel, separate worktrees
 +-- T4  related work                |
 +-- T5  preregistration            /
      |
      +-- T6  Arm A, CONTAINS THE KILL GATE, run alone
            |
            +-- T7  Arm B model runs   \  Wave 2, only after the gate passes
            +-- T8  RL Scientist       /
                  |
                  +-- T9  verification bundle
```

## Two gates the author owns

1. **After T0**, read the spec before releasing Wave 1. Five sessions build on it.
2. **After T6 Step 1**, read the divergence-set number before releasing inference or
   training budget. A failed gate means Arms B and C do not run.

## Usage

```
/p2-task T0
```

One task per session. `/clear` between tasks.

## Placeholders

Task briefs contain `<<FILL>>` markers for repo-specific paths. Replace them before
the first run, or the agent will ask.
