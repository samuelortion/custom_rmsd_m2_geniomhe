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
    # Initialize the PDB parser
    parser = PDBParser(PERMISSIVE=1) # 'PERMISSIVE' allows parsing of incomplete files

    # Parse the structure from the PDB file
    structure_id = None
    structure = parser.get_structure(structure_id, filename)
    model = structure[0]

    coordinates = [] # a list to store the coordinates of selected atoms

    # Iterate through all chains, residues, and atoms in the model
    for chain in model:
        for residue in chain:
            for atom in residue:
                # If there are no filter or if actual atom is in the selected list, append its coordinates
                if selected_atoms == "all" or atom.get_name() in selected_atoms:
                    coordinates.append(atom.get_coord())
        # Convert the list of coordinates into a NumPy array and return
        return np.array(coordinates)

# Example usage: load all C3' atoms from a specific PDB file
if __name__ == "__main__":
    atoms = load_atoms(os.path.join("data","NATIVE","rp03.pdb"), "C3'")
