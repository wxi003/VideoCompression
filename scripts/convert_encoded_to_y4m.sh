#!/bin/bash

# Set paths
base_dir=~/compression_experiments
output_dir="$base_dir/y4m/codec"
mkdir -p "$output_dir"

# Loop through codecs
for codec in h264 h265; do
    input_dir="$base_dir/$codec/animation"

    echo "Processing $codec videos in $input_dir..."

    for mp4_file in "$input_dir"/*.mp4; do
        [ -e "$mp4_file" ] || continue  # Skip if no files found

        filename=$(basename "$mp4_file" .mp4)
        out_y4m="$output_dir/${filename}.y4m"

        if [ -f "$out_y4m" ]; then
            if head -n 1 "$out_y4m" | grep -q "YUV4MPEG2"; then
                echo "Skipping $filename (already converted and valid)"
                continue
            else
                echo "Corrupted Y4M found for $filename, reconverting..."
            fi
        else
            echo "Converting $filename to Y4M..."
        fi

        ffmpeg -y -i "$mp4_file" -pix_fmt yuv420p -fps_mode passthrough "$out_y4m"
    done
done

echo "All encoded MP4s processed!"
