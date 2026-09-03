"""solution/shortcut.py - the naive path this task is designed to catch.

Skill-local only, NOT uploaded. Same robust multi-conformer geometry search, same
oracle-querying and regeneration = -capture sign logic as main.py -- the one and only
naive step is skipping implicit water solvation (tblite's actual default), even
though the system is explicitly aqueous, on BOTH the disclosed side and the oracle
probes (queried with environment="vacuum"). Verified with real numbers: naive vacuum
treatment makes every capture reaction endothermic, and the least energy to
regenerate under that (wrong) treatment goes to whichever candidate had the WORST
(most endothermic) naive capture energy -- amine_NH3, not amine_Proposed.
"""
from __future__ import annotations

from rdkit import Chem
from rdkit.Chem import AllChem
from ase import Atoms
from ase.optimize import BFGS
from tblite.ase import TBLite

EV2KCAL = 23.060548
HA2KCAL = 627.5094740631

CARBAMATE = {
    "amine_NH3": ("N", "[NH4+]", "[NH2]C(=O)[O-]"),
    "amine_MEA": ("NCCO", "OCC[NH3+]", "OCC[NH]C(=O)[O-]"),
    "amine_EDA": ("NCCN", "[NH3+]CCN", "[O-]C(=O)NCCN"),
    "amine_HPEEDA": ("NCCN(CC)CC(O)C", "NCC[NH+](CC)CC(O)C", "[O-]C(=O)NCCN(CC)CC(O)C"),
    "amine_DEA": ("OCCNCCO", "OCC[NH2+]CCO", "OCCN(CCO)C(=O)[O-]"),
}
BICARBONATE_ANION = "OC(=O)[O-]"
CO2_SMILES = "O=C=O"
H2O_SMILES = "O"

N_CONFS = 40
N_RELAX = 8
N_REPLICATES = 10


def _relax_vacuum(atoms, charge, fmax=0.01, steps=800):
    atoms.calc = TBLite(method="GFN2-xTB", charge=charge, uhf=0, verbosity=0)
    BFGS(atoms, logfile=None).run(fmax=fmax, steps=steps)
    return float(atoms.get_potential_energy())


def _true_minimum_energy(smiles, charge, n_confs=N_CONFS, n_relax=N_RELAX, seed=42):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)

    if mol.GetNumAtoms() <= 3:
        AllChem.EmbedMolecule(mol, randomSeed=seed, useRandomCoords=True)
        AllChem.MMFFOptimizeMolecule(mol, maxIters=2000)
        conf = mol.GetConformer()
        symbols = [a.GetSymbol() for a in mol.GetAtoms()]
        positions = [list(conf.GetAtomPosition(i)) for i in range(mol.GetNumAtoms())]
        atoms = Atoms(symbols, positions=positions)
        return _relax_vacuum(atoms, charge)

    cids = AllChem.EmbedMultipleConfs(mol, numConfs=n_confs, randomSeed=seed,
                                       useRandomCoords=True, pruneRmsThresh=0.2)
    mmff_energies = []
    for cid in cids:
        props = AllChem.MMFFGetMoleculeProperties(mol)
        ff = AllChem.MMFFGetMoleculeForceField(mol, props, confId=cid)
        if ff is None:
            continue
        ff.Minimize(maxIts=2000)
        mmff_energies.append((ff.CalcEnergy(), cid))
    mmff_energies.sort(key=lambda x: x[0])

    symbols = [a.GetSymbol() for a in mol.GetAtoms()]
    best_e = None
    for _, cid in mmff_energies[:n_relax]:
        conf = mol.GetConformer(cid)
        positions = [list(conf.GetAtomPosition(i)) for i in range(mol.GetNumAtoms())]
        atoms = Atoms(symbols, positions=positions)
        e = _relax_vacuum(atoms, charge)
        if best_e is None or e < best_e:
            best_e = e
    return best_e


def naive_solve(query_oracle):
    query_oracle("help", {})

    e_co2 = _true_minimum_energy(CO2_SMILES, 0)
    e_h2o = _true_minimum_energy(H2O_SMILES, 0)
    e_bicarb = _true_minimum_energy(BICARBONATE_ANION, -1)

    capture = {}
    for name, (neu, cat, an) in CARBAMATE.items():
        e_n = _true_minimum_energy(neu, 0)
        e_c = _true_minimum_energy(cat, 1)
        e_a = _true_minimum_energy(an, -1)
        capture[name] = (e_c + e_a - 2 * e_n - e_co2) * EV2KCAL

    classification = query_oracle("classify", {})
    if classification["has_nh_bond"]:
        raise NotImplementedError("carbamate route for the proposed solvent is not implemented")
    diffs = []
    for rid in range(N_REPLICATES):
        r = query_oracle("probe", {"environment": "vacuum", "replicate_id": rid})
        diffs.append(r["observation"]["energy_hartree"])
    diff_ha = sum(diffs) / len(diffs)
    e_co2_ha = e_co2 * (1.0 / 27.211386245988)
    e_h2o_ha = e_h2o * (1.0 / 27.211386245988)
    e_bicarb_ha = e_bicarb * (1.0 / 27.211386245988)
    dE_proposed_kcal = (diff_ha + e_bicarb_ha - e_co2_ha - e_h2o_ha) * HA2KCAL
    capture["amine_Proposed"] = dE_proposed_kcal

    return max(capture, key=capture.get)


def main():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "oracle"))
    import oracle  # type: ignore[import-not-found]  # noqa: E402

    answer = naive_solve(oracle.handle_query)
    print(f"EVERGLADES_SUBMIT_ANSWER: {answer}")
    print(answer)


if __name__ == "__main__":
    main()
