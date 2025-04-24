#!/bin/bash

# === Configuration ===
base_dir=~/compression_experiments
codec_dir="$base_dir/y4m/codec"
original_dir="$base_dir/original/animation"
log_file="$base_dir/evaluation_log.csv"
model_path=~/vmaf_models/vmaf_v0.6.1.json

# === Init log file ===
if [ ! -f "$log_file" ]; then
    echo "filename,codec,bitrate,preset,keyint,vmaf,psnr" > "$log_file"
fi

# === Loop over all .y4m files ===
for encoded_y4m in "$codec_dir"/*.y4m; do
    filename=$(basename "$encoded_y4m" .y4m)

    # Skip already logged
    if grep -q "$filename" "$log_file"; then
        echo "Already evaluated: $filename"
        continue
    fi

    # === Extract metadata ===
    base_name=$(echo "$filename" | sed -E 's/_libx(264|265)_.*//')
    codec=$(echo "$filename" | grep -o 'libx264\|libx265' | sed 's/libx/h/')
    bitrate=$(echo "$filename" | sed -E 's/.*_([0-9]+k)_.*/\1/')
    preset=$(echo "$filename" | sed -E 's/.*_([a-z]+)_keyint.*/\1/')
    keyint=$(echo "$filename" | grep -o 'keyint[0-9]\+' | sed 's/keyint//')

    # === Resolve paths ===
    original_y4m="$base_dir/y4m/original/${base_name}.y4m"
    encoded_mp4="$base_dir/$codec/animation/${filename}.mp4"
    original_mp4="$original_dir/${base_name}.mp4"

    # === Check paths ===
    if [ ! -f "$original_y4m" ]; then
        echo "Missing files for $original_y4m, skipping."
        continue
    fi
    
    if [ ! -f "$encoded_mp4" ]; then
        echo "Missing files for $encoded_mp4, skipping."
        continue
    fi	

    # === Run VMAF ===
    echo "Running VMAF for $filename..."
    vmaf --reference "$original_y4m" \
         --distorted "$encoded_y4m" \
         --model path="$model_path" \
         --json --output result.json

    vmaf_score=$(jq '.pooled_metrics.vmaf.mean' result.json)

    # === Run PSNR ===
    echo "Running PSNR for $filename..."
    psnr_output=$(ffmpeg -i "$encoded_mp4" -i "$original_mp4" \
        -lavfi psnr="stats_file=psnr.log" -f null - 2>&1)
    psnr_score=$(echo "$psnr_output" | grep "average:" | awk -F'average:' '{print $2}' | awk '{print $1}')

    # === Save ===
    echo "$filename,$codec,$bitrate,$preset,$keyint,$vmaf_score,$psnr_score" >> "$log_file"
    echo "Logged $filename"

    # Optional cleanup:
    rm -f "$encoded_y4m"
done
