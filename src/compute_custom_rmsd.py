"""
Comparison of Coarse-Grained RMSD metrics
with RMSD, MQ and TM metrics
"""

import os

import pandas as pd
from CustomCGRMSD import CustomCGRMSD

NATIVE = "data/NATIVE"
PREDS = "data/PREDS"

native_filenames = os.listdir(NATIVE)

my_rmsd = CustomCGRMSD()

for native_filename in native_filenames:
    identifier = native_filename.replace(".pdb", "")
    predicted_structures = os.listdir(os.path.join(PREDS, identifier))
    native_path = os.path.join(NATIVE, native_filename)
    for predicted_filename in predicted_structures:
        predicted_path = os.path.join(PREDS, predicted_filename)
        score = my_rmsd.predict(native_path, predicted_path)
