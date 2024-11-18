"""
Compute the correlation coefficients between 
Coarse-Grained RMSD and other metrics
"""

from scipy.stats import pearsonr
import numpy as np
import pandas as pd
import os

NATIVE = "data/NATIVE"
SCORES = "data/SCORES"

def correlation(identifier):
    cg_rmsd_df = pd.read_csv(os.path.join("tmp/", f"{identifier}.csv"))
    other_df = pd.read_csv(os.path.join(SCORES, f"{identifier}.csv"), index_col=0)
    cg_rmsd_df = cg_rmsd_df.set_index('model')
    cg_rmsd_df = cg_rmsd_df.reindex(index=other_df.index)
    cg_rmsd = cg_rmsd_df["scores"]
    rmsd = other_df["RMSD"]
    cg_rmsd_values = [
        cg_rmsd for cg_rmsd, rmsd in zip(cg_rmsd.values, rmsd.values)
        if not pd.isna(cg_rmsd) and not pd.isna(rmsd)
    ]
    rmsd_values = [
        rmsd for cg_rmsd, rmsd in zip(cg_rmsd.values, rmsd.values)
        if not pd.isna(cg_rmsd) and not pd.isna(rmsd)
    ]
    assert len(cg_rmsd_values) == len(rmsd_values)
    return pearsonr(cg_rmsd.values, rmsd.values)


def main():
    native_structures = os.listdir(NATIVE)
    correlation_scores = []
    for native_structure in native_structures:
        identifier = native_structure.replace(".pdb", "")
        score = correlation(identifier)
        if score.statistic != np.nan:
            print(score.statistic)
            correlation_scores.append(score.statistic)
    print(sum(correlation_scores) / len(correlation_scores))


if __name__ == "__main__":
    main()
