"""
Compute the correlation coefficients between 
Coarse-Grained RMSD and other metrics
"""

from scipy.stats import pearsonr
import numpy as np
import pandas as pd
import os
from compute_our_custom_rmsd import SELECTIONS

NATIVE = os.path.join("data", "NATIVE")
SCORES = os.path.join("data", "SCORES")

def correlation(identifier: str, metrics: str, tmp_dir: str = "tmp") -> float:
    """
    Compute the Pearson correlation coefficient
    between the CG-RMSD and another metric (e.g., RMSD, MCQ, or TM-score).

    Parameters
    ----------
        identifier: The identifier of the structure (usually the filename without extension)
        metrics: The name of the metric (e.g., 'RMSD', 'MCQ', 'TM-score') to correlate with CG-RMSD
    
    Returns
    --------
        float: The Pearson correlation coefficient between CG-RMSD and the given metric
    """
    # Load the other metric's data
    other_df = pd.read_csv(os.path.join(SCORES, f"{identifier}.csv"))
    # Reset the index of the DataFrame, dropping the old index, and modifying the DataFrame in place
    # This ensures that the index starts from 0 and is continuous (no leftover index from previous operations)
    other_df.reset_index(drop=True, inplace=True)
    # Rename the column 'Unnamed: 0' (the default name of the index column when reading CSVs) to 'model'
    # This allows us to have a proper column name for the 'model' in the DataFrame
    other_df.rename(columns={"Unnamed: 0": "model"}, inplace=True)

    # Load the CG-RMSD data from the "tmp/" folder and modify the 'model' column values
    # We use a lambda function to prefix each model name with 'normalized_' for consistency
    # This step ensures that the model names in cg_rmsd_df match the format used in the other_df for merging
    cg_rmsd_df = pd.read_csv(os.path.join(tmp_dir, f"{identifier}.csv"))
    cg_rmsd_df["model"] = cg_rmsd_df["model"].map(lambda x: f"normalized_{x}")

    # Merge CG-RMSD data with the other metric data on the model column
    df = pd.merge(cg_rmsd_df, other_df, on="model")

    cg_rmsd = df["scores"]
    other = df[metrics]

    # Filter out NaN values from both CG-RMSD and the other metric
    cg_rmsd_values = [
        cg_rmsd for cg_rmsd, rmsd in zip(cg_rmsd.values, other.values)
        if not pd.isna(cg_rmsd) and not pd.isna(rmsd)
    ]
    other_values = [
        rmsd for cg_rmsd, rmsd in zip(cg_rmsd.values, other.values)
        if not pd.isna(cg_rmsd) and not pd.isna(rmsd)
    ]

    # Try to compute the Pearson correlation coefficient
    try:
        score = pearsonr(cg_rmsd_values, other_values)
    except Exception as e:
        print(e)
        return pd.NA
    return score.statistic
    

def correlation_coefficients(tmp_dir: str):
    """
    Main function to compute correlation scores 
    between CG-RMSD stored in `tmp_dir` and other metrics (RMSD, MCQ, TM-score) 
    for all structures.
    """
    native_structures = os.listdir(NATIVE)
    score_metrics = ["RMSD", "MCQ", "TM-score"]
    score_values: dict[str, list] = {metric: [] for metric in score_metrics} # dictionary to hold score values for each metric

    for native_structure in native_structures:
        identifier = native_structure.replace(".pdb", "")
        # For each metric, calculate the correlation with CG-RMSD
        for metrics in score_metrics:
            score = correlation(identifier, metrics)
            if not pd.isna(score):
                score_values[metrics].append(score)

    # Calculate the mean correlation score for each metric
    # correlation_scores = [np.mean(score_values[metric]) for metric in score_metrics]
    # return correlation_scores
    return score_values


def main():
    data = {}
    data["selection"] = SELECTIONS
    data.update({metric: [] for metric in ["RMSD", "MCQ", "TM-score"]})
    for i, selection in enumerate(SELECTIONS):
        correlations = correlation_coefficients(f"tmp/{i}")
        for metric in ["RMSD", "MCQ", "TM-score"]:
            data[metric].append(correlations[metric])
    df = pd.DataFrame(data)
    df.to_csv("correlation_scores.csv", index=False)

if __name__ == "__main__":
    main()
