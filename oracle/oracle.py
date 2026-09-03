"""oracle/oracle.py - HIDDEN system. The model never sees this file.

The hidden "proposed solvent" is structurally amine_MDEA (N-methyldiethanolamine,
tertiary, no N-H, bicarbonate route) -- its real, already-verified GFN2-xTB numbers
from this session's authoring work, wrapped behind a black-box interface instead of
disclosed directly. problem.md states BOTH governing equations (carbamate, for an
amine with an available N-H bond, and base-catalyzed bicarbonate, for one with none)
but does not say which applies to the proposed solvent -- the model must call
"classify" to learn whether it has an N-H bond, then pick the matching equation
itself.

Only the difference E(cation) - E(neutral) is ever returned by "probe" (never an
absolute energy) -- exactly the piece needed for the bicarbonate-route reaction
energy, since the bicarbonate anion, CO2, and H2O are all species the solver can
build and compute independently (they do not depend on the proposed solvent's
identity).

Public entry point: handle_query(mode, parameters) (query_oracle is an alias).
"""
from __future__ import annotations
import hashlib

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from ase import Atoms
from ase.optimize import BFGS
from tblite.ase import TBLite

# === Hidden identity: structurally amine_MDEA (tertiary, no N-H) ===
_NEUTRAL_SMILES = "OCCN(C)CCO"
_CATION_SMILES = "OCC[NH+](C)CCO"

_ENVIRONMENTS = ("vacuum", "water")
_EV2HA = 1.0 / 27.211386245988


def _smiles_to_atoms(smiles, seed=42, tries=5):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    ok = -1
    for i in range(tries):
        ok = AllChem.EmbedMolecule(mol, randomSeed=seed + i, useRandomCoords=True)
        if ok == 0:
            break
    if ok != 0:
        raise RuntimeError(f"embed failed: {smiles}")
    AllChem.MMFFOptimizeMolecule(mol, maxIters=2000)
    conf = mol.GetConformer()
    symbols = [a.GetSymbol() for a in mol.GetAtoms()]
    positions = [list(conf.GetAtomPosition(i)) for i in range(mol.GetNumAtoms())]
    charge = Chem.GetFormalCharge(mol)
    return Atoms(symbols, positions=positions), charge


def _energy(smiles, environment):
    atoms, charge = _smiles_to_atoms(smiles)
    calc = TBLite(method="GFN2-xTB", charge=charge, uhf=0, verbosity=0)
    atoms.calc = calc
    atoms.get_potential_energy()
    if environment == "water":
        calc._xtb.add("alpb-solvation", "water")
        calc.results = {}
    BFGS(atoms, logfile=None).run(fmax=0.03, steps=500)
    return float(atoms.get_potential_energy())  # eV


def _cation_minus_neutral(environment):
    e_cation = _energy(_CATION_SMILES, environment)
    e_neutral = _energy(_NEUTRAL_SMILES, environment)
    return (e_cation - e_neutral) * _EV2HA  # Hartree


# === Budget enforcement ===
_BUDGET = 30
_used = 0

_NOISE_SALT = "co2-solvent-identity-v2"


def _seed_key(mode: str, parameters: dict) -> str:
    items = sorted((str(k), repr(v)) for k, v in parameters.items() if k != "replicate_id")
    return mode + "|" + ";".join(f"{k}={v}" for k, v in items)


def _rng_for(replicate_id, key: str):
    if replicate_id is None:
        return None
    digest = hashlib.sha256(f"{_NOISE_SALT}:{int(replicate_id)}:{key}".encode("utf-8")).digest()
    return np.random.default_rng(int.from_bytes(digest[:8], "little") % (2 ** 32))


def _noise(replicate_id, key: str, sigma: float):
    rng = _rng_for(replicate_id, key)
    return 0.0 if rng is None else float(rng.normal(0.0, sigma))


def handle_query(mode: str, parameters: dict | None = None):
    """The PUBLIC interface the model can call (RLS contract)."""
    global _used
    parameters = parameters or {}

    if mode == "help":
        return {
            "description": "an instrument for one unidentified proposed CO2-capture solvent -- "
                            "'classify' reports its structural class, 'probe' reports how much "
                            "its own protonated cation differs energetically from its own "
                            "neutral form, never an absolute energy",
            "modes": {
                "classify": "{} -> {has_nh_bond: bool} (free, does not spend budget)",
                "probe": "{environment: 'vacuum'|'water', replicate_id?: int} -> "
                         "{observation: {energy_hartree: float}, unit: str}",
            },
            "budget_remaining": _BUDGET - _used,
        }

    if mode == "classify":
        return {"has_nh_bond": False}

    if mode != "probe":
        return {"error": f"unknown mode {mode!r}"}

    environment = parameters.get("environment")
    if environment not in _ENVIRONMENTS:
        return {"error": f"environment must be one of {_ENVIRONMENTS}, got {environment!r}"}

    rid = parameters.get("replicate_id")
    if rid is not None:
        try:
            int(rid)
        except (TypeError, ValueError):
            return {"error": f"replicate_id must be an integer, got {rid!r}"}

    _used += 1
    if _used > _BUDGET:
        return {"error": "budget exceeded"}

    e_ha = _cation_minus_neutral(environment)
    key = _seed_key(mode, parameters)
    e_obs = e_ha + _noise(rid, key, sigma=1e-6)

    return {"observation": {"energy_hartree": e_obs}, "unit": "Hartree"}


# Alias for the skill's tooling.
query_oracle = handle_query
