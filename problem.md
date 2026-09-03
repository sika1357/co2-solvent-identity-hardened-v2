A plant scrubs CO2 from flue gas with diethanolamine (DEA), dissolved in water, and is comparing it to four other disclosed amines plus one proposed solvent whose structure is confidential.

Disclosed candidates:
ammonia, SMILES N
monoethanolamine (MEA), SMILES NCCO
ethylenediamine (EDA), SMILES NCCN
N-(2-hydroxypropyl)-N-ethylethylenediamine (HPEEDA), SMILES NCCN(CC)CC(O)C
diethanolamine (DEA), SMILES OCCNCCO

Each disclosed amine has an available N-H bond; HPEEDA has two chemically distinct nitrogens, use whichever is the actual reactive site.

The proposed solvent's structure is hidden, including whether it has an available N-H bond; query it with query_oracle(mode, parameters) -- call query_oracle("help", {}) first to learn the available modes and the remaining budget. query_oracle("probe", {"environment": "vacuum" or "water", "replicate_id": <int>}) returns a noisy Hartree energy difference, the proposed solvent's cation minus its neutral form; replicate_id is required, each reading independently noisy, budget 30 calls total.

Regeneration reverses capture. Determine which of the six candidates requires the least energy to regenerate, using each candidate's own applicable equation.

Write a Python script that uses tblite (GFN2-xTB) for every calculation.

Submit exactly one of these six labels, case insensitive, via submit_answer: amine_NH3, amine_MEA, amine_DEA, amine_EDA, amine_HPEEDA, amine_Proposed. The last non-empty line printed to stdout must be exactly EVERGLADES_SUBMIT_ANSWER: <label>.
