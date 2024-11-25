"""
    Since we have also a inputs.py script to do the same things, this draft will be probably removed
"""

import numpy as np

ATOM_LIST = [
    "P",
    "O5'",
    "C5'",
    "C4'",
    "C3'",
    "C2'",
    "C1'",
    "O1'",
    "O3'"
]

def readPDB(file_name, atom):
    atoms_dict = {
        'x' : [],
        'y' : [],
        'z' : []
    }

    file = open(file_name, 'r')

    for line in file.readlines():
        column_1 = line[0:6].replace(" ","")
        atom_name = line[12:16].replace(" ","")
        residue_name = line[17:20]
        x_coordinate = line[30:38]
        y_coordinate = line[38:46]
        z_coordinate = line[46:54]
        chain_identifier = line[21:22]
        if column_1 == "ATOM" :
            if atom_name == atom:
                atoms_dict['x'].append(float(x_coordinate))
                atoms_dict['y'].append(float(y_coordinate))
                atoms_dict['z'].append(float(z_coordinate))

    file.close()
    print(atoms_dict)
    atoms_ndarray = np.array([[atoms_dict[j] for j in ['x', 'y', 'z']]])

    return(atoms_ndarray)

if __name__ == "__main__":
    atom = "C3'"
    atom2 = "P"
    pdb_name_nat = r"data\\NATIVE\\rp03.pdb"
    pdb_name_pred = r"data\\PREDS\\rp03\\3drna_rp03_1.pdb"
    
    pdb_name_nat11 = r"data\\NATIVE\\rp11.pdb"
    pdb_name_pred11 = r"data\\PREDS\\rp11\\rnacomposer_rp11.pdb"
    coords_nat_C3 = readPDB(pdb_name_nat,atom)
    coords_pred_C3 = readPDB(pdb_name_pred,atom)
    coords_nat_C311 = readPDB(pdb_name_nat11,atom2)
    coords_pred_C311 = readPDB(pdb_name_pred11,atom2)
    # print(coords_nat_C3)
    print(coords_nat_C3.shape, coords_pred_C3.shape)
    print(coords_nat_C311.shape, coords_pred_C311.shape)