# SUBMISSION-CHECK V3.6

# Feedback - co2-solvent-identity

FIX | submission-check 2026-09-03 (draft check) | evidence: MANIFEST.md

## The problem

All four gates pass (TASK-SHAPE REAL-INVERSE, TOOL-NECESSITY PASS, SUFFICIENCY SUFFICIENT). One
required file is missing and this review cannot substitute for it.

## Fix these

- **Write `solution/solution.md`.** Your own step-by-step account of why `amine_Proposed` is
  correct, in your own scientific voice - `raw_solution_content.md` is a local-only draft and never
  ships. `publish.py` refuses without this file, and no reviewer's re-derivation replaces it.

## Worth doing, not blocking

- The solvation trap (h#1: does the solver add implicit water solvation, since tblite defaults to
  gas-phase and the prompt never says so explicitly) is well-reasoned but untested against a real
  run population. This is expected and not a defect - it is exactly what the 16-run evaluation is
  for - but if the runs come back showing models mostly cluster on the vacuum near-miss
  (`amine_NH3`) rather than a defensible-but-wrong alternative reading, re-check Guard 1 (shortcut
  cluster = trap working; alternative-reading cluster = ambiguity) before trusting the stump rate.

## Before you resubmit

- [ ] Write `solution/solution.md`.
- [ ] Create the task in RL Studio, publish via `publish.py`.
- [ ] Run `submission-check` again after the 16 real Taiga runs land - this draft check's SUFFICIENT
      verdict is capped at MEDIUM specifically because no run population exists yet.
