"""
Compute the correlation coefficients between 
Coarse-Grained RMSD and other metrics
"""

from scipy.stats import pearsonr
import numpy as np
import pandas as pd
import os

NATIVE = os.path.join("data", "NATIVE")
SCORES = os.path.join("data", "SCORES")

def correlation(identifier):
    """
    Function that computes correlation coefficients
    between Coarse-Grained RMSD (CGRMDS) and other metrics

    Args
    ----
        identifier: str
            unique to each structure, use to locate associated `.csv` file
    
    Returns
    -------
        A tuple containing the pearson correlation coefficient and the p-value
    """
    cg_rmsd_df = pd.read_csv(os.path.join("tmp", f"{identifier}.csv"))
    other_df = pd.read_csv(os.path.join(SCORES, f"{identifier}.csv"), index_col=0)

    print("\n cg_rmsd_df : \n", cg_rmsd_df)
    print("\n other_df : \n", other_df)

    # Set the index of cg_rmsd_df to be the 'model' column (assumed column in the CSV)
    cg_rmsd_df = cg_rmsd_df.set_index('model')
    print("\n cg_rmsd_df after set_index : \n", cg_rmsd_df)
    # Rename the index by adding "normalized_" to the beginning of each value
    cg_rmsd_df.index = cg_rmsd_df.index.map(lambda x: f"normalized_{x}")
    print("\n cg_rmsd_df.index : \n", cg_rmsd_df.index)
    print("\n cg_rmsd_df agter the map : \n", cg_rmsd_df)
    # Align the indices of cg_rmsd_df to match the other_df based on their indices
    cg_rmsd_df = cg_rmsd_df.reindex(index=other_df.index)

    print("\n other_df.index : \n", other_df.index)
    print("\n cg_rmsd_df after reindex : \n", cg_rmsd_df)

    cg_rmsd = cg_rmsd_df["scores"]
    rmsd = other_df["RMSD"]

    print("\n cg_rmsd : \n",cg_rmsd)
    print("\n rmsd : \n", rmsd)
    print("\n is na in cg_rmsd : \n", cg_rmsd.isna().any())
    print("is na in rmsd : \n",rmsd.isna().any())

    # Filter out pairs of values where either cg_rmsd or rmsd is NaN (missing values)
    cg_rmsd_values = [
        cg_rmsd for cg_rmsd, rmsd in zip(cg_rmsd.values, rmsd.values)
        if not pd.isna(cg_rmsd) and not pd.isna(rmsd)
    ]
    rmsd_values = [
        rmsd for cg_rmsd, rmsd in zip(cg_rmsd.values, rmsd.values)
        if not pd.isna(cg_rmsd) and not pd.isna(rmsd)
    ]
    print("\n cg_rmsd_value : \n", cg_rmsd_values)
    print("\n rmsd_values : \n", rmsd_values)

    assert len(cg_rmsd_values) == len(rmsd_values)
    return pearsonr(cg_rmsd_values, rmsd_values)


def main():
    native_structures = os.listdir(NATIVE)
    correlation_scores = [] # List to store correlation scores for each native structure
    for native_structure in native_structures:
        identifier = native_structure.replace(".pdb", "")
        score = correlation(identifier)
        # Check if the Pearson correlation coefficient is a valid number (not NaN)
        if score.statistic != np.nan:
            print("score : ",score.statistic)
            correlation_scores.append(score.statistic)
    # Compute and print the average correlation score for all structures
    print("\n correlation_scores : \n", correlation_scores)
    print("average correlation score : ",sum(correlation_scores) / len(correlation_scores))


if __name__ == "__main__":
    main()
