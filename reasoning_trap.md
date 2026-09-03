Five stacked traps, all verified with real GFN2-xTB numbers.

**Trap 1 (decisive, solvation):** tblite is gas-phase by default. The prompt only says the
amines are dissolved in water, with no explicit computational instruction, and the oracle's
own `environment` parameter must also be set to `"water"`. Naive vacuum treatment (both sides)
makes every capture reaction endothermic and flips which candidate looks best.

**Trap 2 (decisive, direction):** the prompt asks for the LEAST energy to REGENERATE, not the
most favorable capture. Regeneration reverses capture, so regeneration energy = -capture
energy: the answer is the candidate with the LEAST exothermic capture, not the most. A solver
that computes capture correctly and reports the most-negative candidate has it backwards.

**Trap 3 (decisive, equation recall):** neither governing equation is stated. The solver must
know that a primary/secondary amine forms a carbamate (2 Amine + CO2 -> Carbamate(-) +
AmineH(+)) while a tertiary (no-N-H) amine forms bicarbonate instead (Amine + CO2 + H2O ->
AmineH(+) + HCO3(-), 1:1). Wrong stoichiometry breaks the whole calculation, not just the
hidden candidate's.

**Trap 4 (side, mechanism discovery):** the hidden solvent's N-H status is undisclosed, and
`classify` isn't even named - the solver must call `help` first, discover `classify` exists,
then call it. Never competitive for the win, but skipping it leaves no defensible route at all.

**Trap 5 (side, site selection):** HPEEDA is bifunctional - one primary N-H site (carbamate),
one already-tertiary site (protonation) - and requires identifying which nitrogen reacts where.

**Also in play:** Piperazine was removed after independent verification (100-conformer
searches, three blind solvers) could not reliably separate it from the hidden winner (within
~0.1-0.9 kcal/mol) - not decidable at this level of theory. The winner is hidden behind an
oracle rather than disclosed by name to avoid a structural label leak.
