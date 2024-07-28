#!/bin/bash

if ! command -v yt-dlp &> /dev/null; then
    echo "yt-dlp is not installed. Please install it first."
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Please provide a YouTube playlist URL."
    exit 1
fi

playlist_url="$1"

# https://www.youtube.com/playlist?list=PL1ksgbct81C4ZDRr3zRp41Zj6RLtM1iNa
DATA_FOLDER=$HOME/Documents/march23-galaxynews/data
PLAYLIST_ID=$(echo $playlist_url | sed -n 's/.*list=\([^&]*\).*/\1/p')

# Extract playlist title
playlist_title=$(yt-dlp --get-title --print playlist_title --no-warnings --flat-playlist "$playlist_url" 2>/dev/null | head -n 1)

# Sanitize playlist title to be a valid filename
playlist_title=$(echo "$playlist_title" | tr -cd '[:alnum:]._-' | tr ' ' '_')

output_file=$DATA_FOLDER/playlist_${playlist_title}.txt

> $output_file
yt-dlp -i --get-id "$playlist_url" | sed 's~^~https://www.youtube.com/watch?v=~' > "$output_file"

# Check if the operation was successful
if [ $? -eq 0 ]; then
    echo "Video links have been saved to $output_file"
else
    echo "An error occurred while processing the playlist."
    exit 1
fi
