# SUBMISSION-CHECK V3.6

# Submission Check - co2-solvent-identity (draft check, entry point 3)

Generated: 2026-09-03 | submission-check draft check (Phase 0 + Phase 0b only, no trajectories)
Outputs: MANIFEST.md (this file)

**Supersedes the prior `co2-solvent-identity_submission_check/MANIFEST.md`**, which reviewed an
earlier, structurally different design of this task (a FORWARD, no-oracle, 5-disclosed-candidate
version, disclosed winner amine_Piperazine). The task was redesigned to the current INVERSE,
oracle-hidden-candidate shape after that review ran. This report reviews the CURRENT files only.

**Conflict-of-interest disclosure, binding on every verdict below.** This review was performed in
the same session, by the same agent, that authored `problem.md`, `oracle/oracle.py`,
`solution/main.py` and `solution/shortcut.py`, and that ran the authoring-time calibration gate
(`capture_golden` / `verify` / `shortcut` / `determinism` / `sandbox_run` / `lint`) earlier in this
session. There is no independent party in this loop. Per Hard rule 20 this review does not re-run
or re-derive the solver itself - but the golden WAS confirmed by direct execution earlier in this
same session (not by an independent party before this skill was invoked, which is the assumption
Hard rule 20 ordinarily relies on). E1 below is therefore **author-observed-and-reproduced, not
independently-confirmed** - the single biggest reason SUFFICIENCY's band is not higher than MEDIUM,
on top of the entry-point-3 cap that would apply regardless.

## Gate summary

| gate | verdict | confidence | basis | reviewer must check |
|---|---|---|---|---|
| MATERIALS | INCOMPLETE | CERTAIN | file listing (mechanical) - `solution/solution.md` and `task_info.md` absent; neither blocks verification | - |
| TASK-SHAPE | REAL-INVERSE | HIGH | panels 3/3, unanimous - probed oracle surface (single `probe` mode, environment+replicate_id settings only, never a candidate answer); ledger E1 | - |
| TOOL-NECESSITY | PASS (main.py only - no runs to corroborate) | CERTAIN | main.py read AND actually executed this session: real RDKit+ASE+tblite calls on every candidate's answer path; `return max(capture, key=capture.get)` is a genuine computed argmax, not a literal (E1, sandbox_run 3.1 min real wall-clock) | - |
| SUFFICIENCY | SUFFICIENT | MEDIUM (capped) | panels 3/3, unanimous, no ratchet - battery E1-E8 complete for the enumerable half; **capped at MEDIUM per this skill's own draft-check rule** - the run-derived half of H (reading histogram, pass-quality forensics, computed-gold-then-rejected) is `NOT RUN - no trajectories (draft check)`, regardless of panel unanimity | see note below |

`DISCRIMINATION: N/A - no trajectories exist yet (draft check); cannot compute a stump rate.` This is
not a clean bill - it says the task is fair, not that it is hard. The next real evidence on
difficulty is the 16 runs themselves.

**Why MEDIUM, not HIGH, despite 3/3 unanimous panels citing a strong textual/domain pin:** this
skill's own entry-point-3 rule states the cap explicitly and says not to argue it away - a pre-run
review proves "no unpinned choice was found among the enumerated ones," never "the task is fair,"
because only the real run population can discover an axis nobody enumerated (here, specifically:
whether real models actually make the "dissolved in water -> add implicit solvation" inference
rather than defaulting to tblite's gas-phase default). All three panels independently flagged this
same gap and applied the same cap without being asked to.

**`reviewer must check` for SUFFICIENCY:** nothing is contested (P=3/3, not 2/3), so there is no
owner-question to name. The note exists because a MEDIUM band from a capped arm still owes the
reader an explanation, per this skill's own rule for a MEDIUM produced by a degraded/missing-artifact
arm rather than genuine disagreement.

---

## Glossary (kept per policy - never delete to save space)

- **H** - the Hidden decisions: every choice the solver must make that moves the graded answer
  (here: a categorical choice among 6 candidate labels) by enough to change which label is correct.
- **A** - the Available information: the PROMPT + what the ORACLE actually returns when probed (this
  task has no mounted files, and no source paper is load-bearing - HPEEDA's real-world origin as "a
  2026 AIChE Journal molecule" is flavor text, never something the solver must cite) + the DOMAIN /
  CHEMICAL REASONING the solver can legitimately apply.
- **PINNED** - something specific and quotable in A determines the choice, or the science settles it
  (domain-reasoning pin).
- **UNPINNED** - nothing in A determines it; the solver must guess, and a defensible guess changes
  the answer.
- **H \ A** - the unpinned members of H; this is the defect list.

## Gate detail

### MATERIALS: INCOMPLETE

| # | Row | Status |
|---|---|---|
| 1 | Task prompt (`problem.md`) | PRESENT |
| 2 | Writer's solution | **MISSING - REQUIRED.** `solution/solution.md` does not exist yet; only the skill's own draft, `raw_solution_content.md`, exists (never ships, never counts). Consequence: no free corroboration for this review's re-derivation and no statement of the intended mechanism in the writer's own words - partially mitigated here because the author-agent directly executed and reproduced the golden this session (E1), but that is a weaker substitute than an independent writer account. **Not optional - write it before this ships** (`publish.py` refuses without it). |
| 3 | Grading guidance (`grader/grading_guide.md`) | PRESENT |
| 4 | Trajectories | N/A (draft check, pre-runs) |
| 6 | Expected answer (`golden/expected.json`, `golden/golden_answer.md`) | PRESENT, both forms present and consistent - `amine_Proposed` |
| 7 | Oracle source (`oracle/oracle.py`) | PRESENT - Python oracle, this file IS the instrument (no native sibling; `oracle_native_source` is N/A by the schema's own rule for a Python oracle) |
| 8 | Reference solver (`solution/main.py`) | PRESENT |
| 9 | Source paper | N/A - none implied; HPEEDA's cited real-world origin is context, not a disambiguator the solver needs |
| 10 | `task_files/` / mounted data | N/A - nothing needs mounting beyond the oracle callable |
| 11 | `qa_reports/` | ABSENT - expected, no runs exist yet |
| 12 | `task_info.md` | MISSING (optional) - not a defect; TOOL-NECESSITY falls back to inferring the mandated tool from `main.py`/`config.yaml` (`simulator: tblite`), which is unambiguous here anyway |

**Two decisions, never collapsed.** Flagged: row 2 (required, genuinely missing) and row 12
(optional, informational only). Blocks: **neither blocks verification** - this review re-derives
everything it needs directly from `problem.md`, `oracle/oracle.py`, `solution/main.py`, and this
session's real executions of all three. Row 2 is still a real gap that must close before publish.

---

### TASK-SHAPE: REAL-INVERSE

Unanimous across 3 independent panels. The oracle exposes exactly one measurement mode
(`probe`, parametrized only by `environment` and `replicate_id` - both probe SETTINGS, never a
candidate answer) plus one free descriptive mode (`help`). No mode returns a boolean, score, rank,
verdict, or the hidden solvent's identity/formula/geometry/absolute energy - only a single noisy
relative energy (cation minus neutral) that, by itself, is not the graded answer. Reaching the
graded label requires the solver to independently build and relax CO2, H2O and the bicarbonate
anion with its own tblite calls, combine that with the oracle's reading to get the hidden
candidate's own capture energy, compare against five separately-computed disclosed-candidate
capture energies, and apply the regeneration-is-the-reverse-reaction sign logic - genuine inference
across a measurement -> config gap, not arithmetic on a vended ingredient. The golden is a real
computed argmax (`return max(capture, key=capture.get)`), reproduced 3/3 times by direct execution
this session (E1), never a literal or a read of `golden/expected.json`. No source paper is
load-bearing, so the identifiability test is vacuously satisfied.

---

### TOOL-NECESSITY: PASS (main.py only - no runs to corroborate)

`solution/main.py` was read AND, unusually for this skill's normal posture, was already directly
executed multiple times earlier in this same authoring session (capture_golden, verify, determinism
x3, sandbox_run) - real RDKit (`Chem`/`AllChem`, multi-conformer MMFF pre-relaxation) + ASE
(`Atoms`, `BFGS`) + `tblite.ase.TBLite` (`method="GFN2-xTB"`) calls on every one of the six
candidates' answer paths, with explicit ALPB water solvation added for the graded (water)
environment. The hidden candidate's capture energy combines 10 independent oracle `probe` calls
with independently-relaxed CO2/H2O/bicarbonate energies computed by the same tool. `solve()`
returns `max(capture, key=capture.get)` - traced the data path: this consumes every one of the six
computed dictionary entries, none of which is a literal, a lookup, or a copy of
`golden/expected.json`. `config.yaml`'s `simulator: tblite` matches. `shortcut.py` is the identical
computation with `solvate` forced off everywhere (tblite's actual gas-phase default) - a
naive-parameter shortcut, not a different or absent tool.

No trajectories exist for the N/N audit (draft check) - reported as such, not scored.

---

### SUFFICIENCY: SUFFICIENT | conf MEDIUM (capped) -- basis: panels 3/3, unanimous, battery
E1-E8 complete for the enumerable half, ratchet did not fire

**A = the PROMPT + what the oracle actually returns when probed + the DOMAIN/chemistry reasoning
the solver can legitimately apply.** (No mounted files, no load-bearing paper - both vacuously
satisfied/absent on this task.)

#### The H/A ledger

| # | h (number-moving choice) | Pinned by | Tested how | Decisive? | Verdict |
|---|---|---|---|---|---|
| 1 | solvation: vacuum vs water, applied to every species incl. the oracle probes | domain reasoning - "dissolved in water" stated for every candidate incl. the hidden one; NO explicit computational instruction to add solvation | 3 independent panels, unanimous; E2/E2b show a full winner-identity flip (amine_Proposed/water vs amine_NH3/vacuum) | YES - flips the graded label entirely | PINNED (domain reasoning), but **reviewer-asserted, not run-demonstrated** |
| 2 | regeneration direction: least-exothermic capture wins, not most | explicit text - "Regeneration reverses capture: heating releases the captured CO2... requires the least energy to regenerate" | 3 panels, unanimous; standard Hess's-law sign logic (regen energy = -capture energy) | YES - co-decisive with #1 | PINNED (explicit) |
| 3 | HPEEDA site assignment (which nitrogen is the carbamate site vs the protonation site) | explicit text names the ambiguity and requires resolving it; the correct resolution itself is domain reasoning | E2: HPEEDA's capture energy (-17.453) sits far from both the winner (-11.316) and runner-up (-14.468, a 5.99 kcal/mol gap) - not close enough for a site-assignment error to plausibly swing the winner | NO - side issue, never competitive for the win either way | PINNED (side issue), non-load-bearing |

**Every row has a quotable "Pinned by" span or an explicit domain-reasoning chain. No empty cells.**

#### Deducibility rationale for h#1 (the decisive item)

- **Fact of the matter in the science, or the author's private construction?** Fact of the matter:
  gas-phase electronic energies for a reaction that creates real separated ionic charge from neutral
  reactants are dominated by an unscreened Coulombic penalty with no physical relevance to a process
  the prompt states happens in aqueous solution. Standard graduate physical chemistry, not specific
  to this task's authoring.
- **The argument a scientist would make:** "the prompt states these amines - including the hidden
  one - are dissolved in water; tblite defaults to gas-phase; a bare vacuum calculation of an
  ion-forming reaction in a system explicitly described as aqueous is unphysical, so I must add
  implicit solvation on every species to get a chemically meaningful comparison." This predicts the
  answer; it does not retrofit it.
- **Pre-registration test:** yes - follows directly from reading "dissolved in water" before knowing
  any answer.
- **Empirical check:** **NOT RUN - no transcripts (draft check).** All three panels are
  reviewer-assertions, not run-population evidence, and all three said so unprompted. This is the
  entry-point-3 ceiling: HIGH is unreachable here regardless of how clean the reasoning chain looks,
  because CERTAIN/HIGH both require either a deterministic computation with no judgment step, or
  P=3/3 AND E complete AND R=no - and E is genuinely incomplete (the run-derived half of H cannot
  exist yet).
- **Direction:** the reasoning points AT the correct answer, not away from it (E6) - a plain reading
  of "dissolved in water" lands on water, which is also the physically correct choice. No textual cue
  anywhere points toward vacuum.
- **VERDICT: PINNED** (by domain reasoning), capped in confidence, not in verdict.

#### Guard-arm check (SUFFICIENCY != EASY)

Not rated easy - `DISCRIMINATION` is explicitly N/A pending real runs. A model that skips the
explicit-but-unstated "add solvation" step, or that mishandles the regeneration-direction sign, gets
this wrong exactly as intended. Sufficiency says a fair path exists and is quotable/derivable; it
says nothing about how many of 16 runs will find it.

#### Evidence ledger (E1-E8)

```
E1 golden reproduced:   main.py -> amine_Proposed, reproduced 3/3 in a determinism check this
                         session (identical every run); matches golden/expected.json.
                         (author-observed-and-reproduced this session, NOT independently confirmed
                         by a separate party - see the COI disclosure at the top of this file.)
E2 all-candidate stats (water-solvated capture energy, kcal/mol, real tblite GFN2-xTB numbers):
                         amine_Proposed -11.316 | amine_NH3 -14.468 | amine_MEA -17.258 |
                         amine_HPEEDA -17.453 | amine_DEA -18.512 | amine_EDA -20.782
E2b all-candidate stats (vacuum, naive, same units):
                         amine_DEA 89.922 | amine_HPEEDA 91.957 | amine_Proposed 105.951 |
                         amine_EDA 108.662 | amine_MEA 110.762 | amine_NH3 139.427
E3 invariance-equivalent: toggling solvation MOVES the winner identity outright (Proposed/water vs
                         NH3/vacuum), not just a number - maximally sensitive to this one choice.
E4 estimator power:     2 defensible environment readings exist for this disclosed-aqueous system;
                         1 of 2 (water) reaches amine_Proposed, the other reaches the documented
                         near-miss amine_NH3.
E5 margin:               categorical answer, tolerance 0/exact-match; the h#1 risk if left unpinned
                         is a FULL LABEL FLIP - equivalent to the "sign flip = infinite margin"
                         archetype, not a partial-credit zone.
E6 counter-signal:      no textual cue anywhere points toward vacuum; "dissolved in water" (the only
                         environment cue given, repeated for every candidate incl. the hidden one)
                         points toward the correct answer.
E7 claimed-tell test:   grading_guide.md's stated tell ("shortcut.py skips implicit water solvation
                         ... and lands on 'amine_NH3'") tested by direct execution this session:
                         HOLDS (shortcut.py printed amine_NH3 exactly as documented).
E8 answer-contract check: exact-match, case-insensitive, against one of six disclosed labels; the
                         submitted sentinel format is unambiguous and matches golden_answer.md.
```

#### Panels (k=3, independent, ledger-citing)

All three panels ruled TASK-SHAPE=REAL-INVERSE and SUFFICIENCY=SUFFICIENT unanimously, each
independently building its own H/A ledger and citing E1-E8. No dissent, no ratchet-firing new
evidence, no ledger item left uncited. One panel was explicitly instructed to hunt for a reason the
solvation pin might not hold and for an HPEEDA-driven side effect on the winner; it found none and
independently confirmed E2's 5.99 kcal/mol margin between HPEEDA and the runner-up as sufficient
insulation. Another was instructed to scrutinize the regeneration-direction wording specifically for
sign-trap risk; it independently derived the same Hess's-law reading from the literal text and
confirmed PINNED (explicit).

**SUFFICIENCY: SUFFICIENT.**

---

## Recommendations

1. **Write `solution/solution.md`** (the writer's own step-by-step account) before this ships -
   `publish.py` refuses without it, and it is the one thing this review cannot substitute for, COI
   disclosure notwithstanding.
2. **This report's ceiling is real:** nothing here can substitute for the 16-run Taiga evaluation.
   `SUFFICIENT | conf MEDIUM` means "no unpinned choice was found among the enumerated ones, and the
   reasoning chain for the decisive one is genuinely strong" - not a certification that the task is
   fair, and not a prediction of the stump rate.
3. If real runs come back clustering on the vacuum near-miss (`amine_NH3`) at a rate that looks like
   ambiguity rather than the trap working, re-run this gate's Guard 1 check (defensible-alternative-
   reading vs shortcut-cluster) against the actual transcripts before concluding the task is unfair -
   the guard arm applies with equal force in either direction.
