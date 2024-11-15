import numpy as np
from Bio import PDB
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

def load_atoms(filename: str, selected_atoms: list[str] = NUCLEOTIDE_ATOMS) -> np.ndarray:
    parser = PDBParser(PERMISSIVE=1)
    structure_id = None
    structure = parser.get_structure(structure_id, filename)
    model = structure[0]
    coordinates = []
    for chain in model:
        for residue in chain:
            for atom in residue:
                if atom.get_name() in selected_atoms:
                    coordinates.append(atom.get_coord())
    return np.array(coordinates)



if __name__ == "__main__":
    atoms = load_atoms("data/NATIVE/rp03.pdb", "C3'")
