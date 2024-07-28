#!/bin/bash

# Check if the directory argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Directory containing the Markdown files
DIRECTORY="$1"

# Check if the directory exists
if [ ! -d "$DIRECTORY" ]; then
    echo "Error: Directory $DIRECTORY does not exist."
    exit 1
fi

# Iterate over all Markdown files in the directory
for FILE in "$DIRECTORY"/*.md; do
    if [[ -f "$FILE" ]]; then
        echo "Processing file: $FILE"
        
        # Extract the frontmatter
        FRONTMATTER=$(sed -n '/^---$/,/^---$/p' "$FILE")

        # Check if the frontmatter contains saveAsDraft: false
        if echo "$FRONTMATTER" | grep -iq "saveAsDraft: true"; then
            # Delete the file
            rm "$FILE"
            echo "Deleted: $FILE"
        else
            echo "No matching frontmatter found in: $FILE"
        fi
    else
        echo "No Markdown files found in directory: $DIRECTORY"
    fi
done
