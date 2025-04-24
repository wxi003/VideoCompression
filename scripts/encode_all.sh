#!/bin/bash

input_dir=~/compression_experiments/original/animation
output_base=~/compression_experiments
log_file=~/compression_experiments/encoding_log.csv

# Initialize CSV file
echo "filename,codec,bitrate,preset,keyint,output_file_size_bytes,compression_time_seconds" > "$log_file"

bitrates=(500k 1000k 2000k 4000k)
presets=(ultrafast fast medium slow veryslow)
keyints=(30 60 120)
codecs=("libx264" "libx265" "libaom-av1")

for filepath in "$input_dir"/*.mp4; do
    filename=$(basename "$filepath" .mp4)

    for codec in "${codecs[@]}"; do
        case $codec in
            libx264) out_dir="$output_base/h264/animation" ;;
            libx265) out_dir="$output_base/h265/animation" ;;
            libaom-av1) out_dir="$output_base/av1/animation" ;;
        esac
        mkdir -p "$out_dir"

        for bitrate in "${bitrates[@]}"; do
            for preset in "${presets[@]}"; do
                for keyint in "${keyints[@]}"; do
                    out_name="${filename}_${codec}_${bitrate}_${preset}_keyint${keyint}.mp4"
                    out_path="${out_dir}/${out_name}"

                    # Measure encoding time
                    start_time=$(date +%s.%N)
                    ffmpeg -y -i "$filepath" -c:v "$codec" -b:v "$bitrate" -preset "$preset" -g "$keyint" -an "$out_path"
                    end_time=$(date +%s.%N)
                    elapsed=$(echo "$end_time - $start_time" | bc)

                    # Get file size
                    file_size=$(stat -c%s "$out_path")

                    # Log info to CSV
                    echo "$filename,$codec,$bitrate,$preset,$keyint,$file_size,$elapsed" >> "$log_file"
                done
            done
        done
    done
done
