#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <number_of_videos> <number_of_tabs>"
    exit 1
fi

# Read the arguments
total_videos=$1
total_tabs=$2

# Calculate the number of videos per tab
videos_per_tab=$((total_videos / total_tabs))
remainder=$((total_videos % total_tabs))

# Initialize start and end indices
start=1

# Create the output file
output_file="config.txt"
> "$output_file"

# Generate the configuration lines
for (( i=1; i<=total_tabs; i++ )); do
    end=$((start + videos_per_tab - 1))
    
    # Distribute the remainder videos
    if [ "$remainder" -gt 0 ]; then
        end=$((end + 1))
        remainder=$((remainder - 1))
    fi
    
    # Write the line to the output file
    echo "${start}-to-${end}: sh ./src/process_all.sh ./data/playlist_july24-podcast.txt ${start} ${end}" >> "$output_file"
    
    # Update the start index for the next tab
    start=$((end + 1))
done

echo "Configuration written to $output_file"
