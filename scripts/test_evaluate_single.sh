#!/bin/bash

# === Configuration ===
base_dir=~/compression_experiments
original_y4m="$base_dir/y4m/original/Animation_1080P-05f8_crf_10_ss_00_t_20.0.y4m"
encoded_mp4="$base_dir/h264/animation/Animation_1080P-05f8_crf_10_ss_00_t_20.0_libx264_1000k_fast_keyint120.mp4"
encoded_y4m="$base_dir/y4m/codec/Animation_1080P-05f8_crf_10_ss_00_t_20.0_libx264_1000k_fast_keyint120.y4m"
log_file="$base_dir/evaluation_log_test.csv"
model_path=~/vmaf_models/vmaf_v0.6.1.json

# === Parse metadata from filename ===
filename=$(basename "$encoded_y4m" .y4m)
codec="h264"
bitrate=$(echo "$filename" | sed -E 's/.*_([0-9]+k)_.*/\1/')
preset=$(echo "$filename" | sed -E 's/.*_([a-z]+)_keyint.*/\1/')
keyint=$(echo "$filename" | grep -o 'keyint[0-9]\+' | sed 's/keyint//')

# === Init log file ===
if [ ! -f "$log_file" ]; then
    echo "filename,codec,bitrate,preset,keyint,vmaf,psnr" > "$log_file"
fi

# === Convert MP4 to Y4M if missing ===
if [ ! -f "$encoded_y4m" ]; then
    echo "Converting encoded MP4 to Y4M..."
    ffmpeg -y -i "$encoded_mp4" -pix_fmt yuv420p -fps_mode passthrough "$encoded_y4m"
fi

# === Run VMAF ===
echo "Running VMAF..."
vmaf --reference "$original_y4m" \
     --distorted "$encoded_y4m" \
     --model path="$model_path" \
     --json --output result.json

vmaf_score=$(jq '.pooled_metrics.vmaf.mean' result.json)

# === Run PSNR using FFmpeg ===
echo "Running PSNR (FFmpeg)..."
psnr_output=$(ffmpeg -i "$encoded_mp4" -i "$base_dir/original/animation/$(basename "$original_y4m" .y4m).mp4" \
    -lavfi psnr="stats_file=psnr.log" -f null - 2>&1)
psnr_score=$(echo "$psnr_output" | grep "average:" | awk -F'average:' '{print $2}' | awk '{print $1}')

# === Record result ===
echo "$filename,$codec,$bitrate,$preset,$keyint,$vmaf_score,$psnr_score" >> "$log_file"
echo "Test entry recorded in: $log_file"
