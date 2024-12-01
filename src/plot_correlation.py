import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from compute_our_custom_rmsd import SELECTIONS

correlation_scores = pd.read_csv("correlation_scores.csv")
for metrics in ["RMSD", "MCQ", "TM-score"]:
    correlation_scores[metrics] = correlation_scores[metrics].apply(eval).apply(np.array)


fig, axs = plt.subplots(3, 1, figsize=(10, 15))

for j, metric in enumerate(["RMSD", "MCQ", "TM-score"]):
    for i, selection in enumerate(SELECTIONS):
        axs[j].boxplot(correlation_scores[metric].values[i], positions=[i], widths=0.6, patch_artist=True)
        axs[j].set_title(metric)
        axs[j].set_xticks(range(len(SELECTIONS)))
        axs[j].set_ylabel("Pearson ρ")
axs[j].set_xticklabels([str(", ".join(selection)) for selection in SELECTIONS], rotation=45)

plt.show()
