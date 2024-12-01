# Coarse-grained RMSD vs common metrics

![](img/website_image.png)

Instructions: <https://evryrna.github.io/m2_geniomhe_project_presentation/>

## Folder explanation

In the `data` folder, you can find the following folders:

- **NATIVE**: native `.pdb` structures from a community challenge RNA-Puzzles (@rna_puzzles) (22 non-redundant RNAs)
- **PREDS**: predicted `.pdb` structures from different models.
- **SCORES**: metrics computed between the native structures and the predicted ones. It comprises the `RMSD`, `MCQ` and `TM-Score`

In the `src` folder, you can find the following scripts:

- `compute_custom_rmsd.py`: script to compute the custom Coarse-grained RMSD
- `correlation.py`: script to compute the correlation between the custom Coarse-grained RMSD and the other metrics
- `CustomCGRMSD.py`: class to compute the custom Coarse-grained RMSD with the required API
- `inputs.py`: method to load atom positions from the differents `.pdb` files folders using BioPython
- `metrics.py`: method to compute the Root Mean Square deviation between two set of points

## Installation

You might need `numpy`, `scipy`, `matplotlib` and `biopython` to run this project:

```bash
pip install numpy scipy matplotlib biopython
```

## Usage

Our project is divided in two main part, which need to be launch in two time. All our scripts can be find in the `src` folder.

First, we have the computation of our custom Coarse-grained RMSD.

- You will need to run the `compute_custom_rmsd.py` script. This will create a `tmp` folder to stock a `.csv` file per RNA provided in the `data` following the same structure that the files provided in **SCORES** folder, with our `CG-RMSD` for all predicted models.

This code used the `CustomCGRMSD` class and its method present in the `CustomCGRMSD.py` script. Our `inputs.py` method is used by the `CustomCGRMSD.predict` method in order to read the differents `pdb` files from `data` **NATIVE** and **PREDS** folders. Our `metrics.py` method is used also by the `CustomCGRMSD.predict` method to compute the Root Mean Square deviation between two set of points. We used also the `compute_rssd` method from the `utils.py` provided.

Then, we have the computation of the correlation between our `CG-RMSD` score and the other metrics.

- You will need to run the `correlation.py` script. This will print in your terminal the correlation calculated from the generated files in `tmp` folder by running the previous step, and the provided files in `data` **SCORES** folder.

### CustomCGRMSD class API

```python
from CustomCGRMSD import CustomCGRMSD

# Create an instance of the class
cgrmsd = CustomCGRMSD() 
# You can specify the set of atoms to load from the pdb files
cgrmsd = CustomCGRMSD(selected_atoms=["C1'", "C2'", "C3'", "C4'", "C5'", "P", "O5'"])

# Compute the custom Coarse-grained RMSD
cgrmsd.predict('data/NATIVE/1a60.pdb', 'data/PREDS/1a60.pdb')
```
