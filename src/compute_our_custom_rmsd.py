import inputs
from compute_custom_rmsd import compute_rmsd
from CustomCGRMSD import CustomCGRMSD

SELECTIONS = [
    "all",
    ["P"],
    ["C5'"],
    ["O5'"],
    inputs.NUCLEOTIDE_ATOMS
]

def main():
    for i, selection in enumerate(SELECTIONS):
        inputs.NUCLEOTIDE_ATOMS = selection
        cg_rmsd = CustomCGRMSD(selected_atoms=selection)
        compute_rmsd(cg_rmsd, tmp_dir=f"tmp/{i}")

if __name__ == "__main__":
    main()
