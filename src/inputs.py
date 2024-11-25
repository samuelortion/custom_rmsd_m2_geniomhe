import os
import numpy as np
from Bio.PDB.PDBParser import PDBParser

NUCLEOTIDE_ATOMS = ["P",
            "O5'",
            "C5'",
            "C4'",
            "C3'",
            "C2'",
            "C1'",
            "O1'",
            "O3'"]

def load_atoms(filename: str, selected_atoms: list[str] | str = NUCLEOTIDE_ATOMS) -> np.ndarray:
    """
    Load the (x, y, z) coordinates of atoms from a PDB file

    Args
    ----
        filename:
            path to the PDB file
        selected_atoms:
            either a list of residue names to keep or "all", if no filter has to be applied

    Results
    -------
        a matrix (N, 3) [[x,y,z], ...] with atom coordinates
    """
    parser = PDBParser(PERMISSIVE=1)
    structure_id = None
    structure = parser.get_structure(structure_id, filename)
    model = structure[0]
    coordinates = []
    for chain in model:
        for residue in chain:
            for atom in residue:
                if selected_atoms == "all" or atom.get_name() in selected_atoms:
                    coordinates.append(atom.get_coord())
    return np.array(coordinates)



if __name__ == "__main__":
    atoms = load_atoms(os.path.join("data","NATIVE","rp03.pdb"), "C3'")
