#!/bin/bash

# Enable exit on error
set -e

# Function to print error message and exit
error_exit() {
    echo "Error on line $1: $2"
    exit 1
}

# Trap the error signal and call error_exit function
trap 'error_exit $LINENO "$BASH_COMMAND"' ERR

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Check if an argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <file_path> [start_line] [end_line] [-m|--model <model>] [-t|--temperature <temperature>] [-c|--chat_id <chat_id>]"
    exit 1
fi

file="$1"
start_line=${2:-1}
end_line=${3:-$(wc -l < "$file")}

# Set defaults
model="gpt-4o"
temperature=0.5
CHAT_ID=-1002232572864

# Parse optional arguments
shift 3
while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--model)
            model="$2"
            shift 2
            ;;
        -t|--temperature)
            temperature="$2"
            shift 2
            ;;
        -c|--chat_id)
            CHAT_ID="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Processing file: $file from line $start_line to $end_line"

# Extract the specified range of lines from the file
temp_file_lines=$(mktemp)
sed -n "${start_line},${end_line}p" "$file" > "$temp_file_lines"

# echo $(cat ${temp_file_lines})

while IFS= read -r url; do
    echo "Processing video URL: $url"
    result=$(bun ${SCRIPT_DIR}/video_to_hashnode.ts "${url}")
    hx $result
    # sh $SCRIPT_DIR/video_to_hashnode.sh "$url" -m "$model" -t "$temperature" -c "$CHAT_ID"
done < "$temp_file_lines"

rm -f $temp_file_lines
