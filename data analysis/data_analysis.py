import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the merged encoding log
file_path = "/mnt/data/Merged_Encoding_Log.xlsx"
df = pd.read_excel(file_path)

# Convert bitrate from "500k" to integer in kbps
df["bitrate_kbps"] = df["bitrate"].str.replace("k", "").astype(float)

# Filter valid rows for plotting
df_vmaf = df.dropna(subset=["vmaf"])
df_psnr = df.dropna(subset=["psnr"])
df_kid = df.dropna(subset=["kid_mean"])

# 1. Bitrate vs. Video Quality (VMAF/PSNR/KID) for each codec
fig, axes = plt.subplots(3, 1, figsize=(10, 18))

sns.lineplot(data=df_vmaf, x="bitrate_kbps", y="vmaf", hue="codec", marker="o", ax=axes[0])
axes[0].set_title("Bitrate vs. VMAF by Codec")
axes[0].set_xlabel("Bitrate (kbps)")
axes[0].set_ylabel("VMAF")

sns.lineplot(data=df_psnr, x="bitrate_kbps", y="psnr", hue="codec", marker="o", ax=axes[1])
axes[1].set_title("Bitrate vs. PSNR by Codec")
axes[1].set_xlabel("Bitrate (kbps)")
axes[1].set_ylabel("PSNR (dB)")

sns.lineplot(data=df_kid, x="bitrate_kbps", y="kid_mean", hue="codec", marker="o", ax=axes[2])
axes[2].set_title("Bitrate vs. KID Mean by Codec")
axes[2].set_xlabel("Bitrate (kbps)")
axes[2].set_ylabel("KID Mean")

plt.tight_layout()
plt.show()

# 2. Compression Time vs. Video Quality
fig, axes = plt.subplots(3, 1, figsize=(10, 18))

sns.scatterplot(data=df_vmaf, x="compression_time_seconds", y="vmaf", hue="codec", ax=axes[0])
axes[0].set_title("Compression Time vs. VMAF")
axes[0].set_xlabel("Compression Time (s)")
axes[0].set_ylabel("VMAF")

sns.scatterplot(data=df_psnr, x="compression_time_seconds", y="psnr", hue="codec", ax=axes[1])
axes[1].set_title("Compression Time vs. PSNR")
axes[1].set_xlabel("Compression Time (s)")
axes[1].set_ylabel("PSNR (dB)")

sns.scatterplot(data=df_kid, x="compression_time_seconds", y="kid_mean", hue="codec", ax=axes[2])
axes[2].set_title("Compression Time vs. KID Mean")
axes[2].set_xlabel("Compression Time (s)")
axes[2].set_ylabel("KID Mean")

plt.tight_layout()
plt.show()

# 3. File Size vs. Video Quality
fig, axes = plt.subplots(3, 1, figsize=(10, 18))

sns.scatterplot(data=df_vmaf, x="output_file_size_bytes", y="vmaf", hue="codec", ax=axes[0])
axes[0].set_title("File Size vs. VMAF")
axes[0].set_xlabel("File Size (bytes)")
axes[0].set_ylabel("VMAF")

sns.scatterplot(data=df_psnr, x="output_file_size_bytes", y="psnr", hue="codec", ax=axes[1])
axes[1].set_title("File Size vs. PSNR")
axes[1].set_xlabel("File Size (bytes)")
axes[1].set_ylabel("PSNR (dB)")

sns.scatterplot(data=df_kid, x="output_file_size_bytes", y="kid_mean", hue="codec", ax=axes[2])
axes[2].set_title("File Size vs. KID Mean")
axes[2].set_xlabel("File Size (bytes)")
axes[2].set_ylabel("KID Mean")

plt.tight_layout()
plt.show()
