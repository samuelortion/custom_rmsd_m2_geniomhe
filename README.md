# Coarse-grained RMSD vs common metrics

![](img/website_image.png)

## Folder explanation

In the `data` folder, you can find the following folders:
- **NATIVE**: native `.pdb` structures from a community challenge RNA-Puzzles (@rna_puzzles) (22 non-redundant RNAs)
- **PREDS**: predicted `.pdb` structures from different models.
- **SCORES**: metrics computed between the native structures and the predicted ones. It comprises the `RMSD`, `MCQ` and `TM-Score`

In the `src` folder, you have a `utils.py` method that shows you how to superimpose a set of points using:

```
python -m src.utils
```

It should output the following image:

![](img/align_atoms.png)

Feel free to use the functions in the file and include it in your code. 

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