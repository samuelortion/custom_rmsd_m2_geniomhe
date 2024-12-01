"""
Helper function to compute the CG-RMSD between native and predicted structures
"""

import os
import pandas as pd

from CustomCGRMSD import CustomCGRMSD

NATIVE = os.path.join("data", "NATIVE")
PREDS = os.path.join("data", "PREDS")
SCORES = os.path.join("data", "GC_RMSD")

def compute_rmsd(cg_rmsd, tmp_dir="tmp"):
    native_filenames = os.listdir(NATIVE)

    for native_filename in native_filenames:
        identifier = native_filename.replace(".pdb", "")
        predicted_structures = os.listdir(os.path.join(PREDS, identifier))
        native_path = os.path.join(NATIVE, native_filename)

        scores = [] # list to store scores for each predicted structure

        # Loop over each predicted structure to calculate its CG-RMSD with the native structure
        for predicted_filename in predicted_structures:
            predicted_path = os.path.join(PREDS, identifier, predicted_filename)
            # Attempt to predict the CG-RMSD score between the native and predicted structures
            # If an error occurs during the prediction, print the error message and assign NaN as the score
            try:
                score = cg_rmsd.predict(native_path, predicted_path)
            except Exception as e:
                print(e)
                score = pd.NA

            scores.append(score)
        
        # Ensure that the "tmp" directory exists to store the output CSV files
        os.makedirs(tmp_dir, exist_ok=True)
        # Create a DataFrame from the predicted filenames and their corresponding RMSD scores
        df = pd.DataFrame(dict(model=predicted_structures, scores=scores))
        df.to_csv(os.path.join(tmp_dir, f"{identifier}.csv"), index=False)

def main():
    cg_rmsd = CustomCGRMSD()
    compute_rmsd(cg_rmsd)


if __name__ == "__main__":
    main()