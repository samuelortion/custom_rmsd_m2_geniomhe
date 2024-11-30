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

def correlation(identifier, metrics):
    other_df = pd.read_csv(os.path.join(SCORES, f"{identifier}.csv"))
    other_df.reset_index(drop=True, inplace=True)
    other_df.rename(columns={"Unnamed: 0": "model"}, inplace=True)
    cg_rmsd_df = pd.read_csv(os.path.join("tmp/", f"{identifier}.csv"))
    cg_rmsd_df["model"] = cg_rmsd_df["model"].map(lambda x: f"normalized_{x}")
    df = pd.merge(cg_rmsd_df, other_df, on="model")
    cg_rmsd = df["scores"]
    other = df[metrics]
    cg_rmsd_values = [
        cg_rmsd for cg_rmsd, rmsd in zip(cg_rmsd.values, other.values)
        if not pd.isna(cg_rmsd) and not pd.isna(rmsd)
    ]
    other_values = [
        rmsd for cg_rmsd, rmsd in zip(cg_rmsd.values, other.values)
        if not pd.isna(cg_rmsd) and not pd.isna(rmsd)
    ]
    try:
        score = pearsonr(cg_rmsd_values, other_values)
    except Exception as e:
        print(e)
        return pd.NA
    return score.statistic
    


def main():
    native_structures = os.listdir(NATIVE)
    score_metrics = ["RMSD", "MCQ", "TM-score"]
    score_values = {metric: [] for metric in score_metrics}
    for native_structure in native_structures:
        identifier = native_structure.replace(".pdb", "")
        for metrics in score_metrics:
            score = correlation(identifier, metrics)
            if not pd.isna(score):
                score_values[metrics].append(score)
    correlation_scores = [np.mean(score_values[metric]) for metric in score_metrics]
    print("Correlation Scores:")
    for metric, score in zip(score_metrics, correlation_scores):
        print(f"{metric}: {score}")

if __name__ == "__main__":
    main()
