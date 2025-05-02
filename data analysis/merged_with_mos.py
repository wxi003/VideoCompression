import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load the merged encoding log and MOS score sheet
merged_df = pd.read_excel("/mnt/data/Merged_Encoding_Log.xlsx")
mos_df = pd.read_excel("/mnt/data/MOS.xlsx")

# Normalize vid and filename to make them easier to match
# For example: extract "Animation_1080P-05f8" from "Animation_1080P-05f8_crf_10_ss_00_t_20.0"
merged_df["vid"] = merged_df["filename"].apply(lambda x: "_".join(x.split("_")[:2]) if isinstance(x, str) else None)
mos_df["vid"] = mos_df["vid"].astype(str)

# Merge on vid
merged_with_mos = pd.merge(merged_df, mos_df, on="vid", how="inner")

# Prepare plots for comparison
figures = {}

for metric in metrics:
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=merged_with_mos, x='MOS full', y=metric)
    plt.title(f'MOS vs. {metric.upper()}')
    plt.xlabel('MOS (Mean Opinion Score)')
    plt.ylabel(metric.upper())
    plt.grid(True)
    fig_path = f"/mnt/data/MOS_vs_{metric.upper()}.png"
    plt.savefig(fig_path)
    figures[metric] = fig_path
    plt.close()

figures
