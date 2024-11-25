"""
Comparison of Coarse-Grained RMSD metrics
with RMSD, MQ and TM metrics
"""

import os
import pandas as pd

from CustomCGRMSD import CustomCGRMSD

NATIVE = os.path.join("data", "NATIVE")
PREDS = os.path.join("data", "PREDS")
SCORES = os.path.join("data", "GC_RMSD")

native_filenames = os.listdir(NATIVE)

my_rmsd = CustomCGRMSD()


for native_filename in native_filenames:
    identifier = native_filename.replace(".pdb", "")
    predicted_structures = os.listdir(os.path.join(PREDS, identifier))
    native_path = os.path.join(NATIVE, native_filename)
    scores = []
    for predicted_filename in predicted_structures:
        predicted_path = os.path.join(PREDS, identifier, predicted_filename)
        try:
            score = my_rmsd.predict(native_path, predicted_path)
        except Exception as e:
            print(e)
            score = pd.NA

        scores.append(score)
    os.makedirs("tmp", exist_ok=True)
    df = pd.DataFrame(dict(model=predicted_structures, scores=scores))
    df.to_csv(os.path.join("tmp", f"{identifier}.csv"))
