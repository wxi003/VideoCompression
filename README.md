# CS 4490 Thesis: Comparative Analysis of Modern Video Codecs: H.264, H.265, and AV1 Using Objective and Perceptual Metrics

This repository contains the full source files, data, scripts, and final report for the CS4490Z undergraduate thesis project at Western University (2025), authored by Xi Wang. The project compares the performance of three modern video codecs—**H.264**, **H.265**, and **AV1**—using both **objective** and **perceptual** quality metrics.

---

## Abstract

With video streaming accounting for over 80% of global internet traffic, efficient video compression is crucial. This thesis investigates codec efficiency, video quality, and encoding speed across various bitrate and preset combinations using:

- **Objective Metrics**: PSNR  
- **Perceptual Metric**: VMAF, KID, MOS  
---

## Research Goals

- Compare AV1, H.264, and H.265 in terms of visual quality, file size, and compression time.
- Evaluate metric correlation with user-perceived quality (MOS).
- Identify optimal codec-bitrate-preset trade-offs for streaming applications.

---

## Repo Structure

```plaintext
.
├── report/
│   └── CS4490_Thesis_Final_Report.pdf      # Final report (22 pages, includes figures)
├── data files/
│   ├── original_videos_MOS.xlsx            # Mean Opinion Score data from UGC dataset
│   ├── encoding_log.xlsx                   # Compression metadata
│   ├── evaluation_log.csv                  # VMAF and PSNR scores
│   └── kid_scores_50_frames.csv            # KID metrics for compressed vs. original frames
├── scripts/
│   ├── convert_encoded_to_y4m.sh
│   ├── evaluate_codec_y4m.sh
│   ├── extract_frames_commands.sh
│   ├── extract_compressed_frames_commands.sh
│   └── updated_batch_kid_evaluation.py
├── data analysis/
│   ├── Average_Compression_Time_By_Codec.png
│   ├── Bitrate_vs_VideoQuality.png
│   ├── Compression_Time_vs_VideoQuality.png
│   ├── File_Size_vs_VideoQuality.png
│   ├── MOS_vs_KID_MEAN.png
│   ├── MOS_vs_PSNR.png
│   ├── MOS_vs_VMAF.png
│   ├── data_analysis.py
│   ├── merged_with_mos.py
└── README.md
