import sys
import os
import math

# Check if the correct number of arguments are provided
if len(sys.argv) != 4:
    print("Usage: python3 script.py <file> <min_chapters> <max_chapter_size>")
    sys.exit(1)

# Variables
file = sys.argv[1]
min_chapters = int(sys.argv[2])
max_chapter_size = int(sys.argv[3])

# Check if the file exists
if not os.path.isfile(file):
    print("File {} not found!".format(file))
    sys.exit(1)

# Create a new file name
new_file = file.replace('.txt', '-with-chapters.txt')

# Open the file
with open(file, 'r') as f:
    lines = f.readlines()

total_lines = len(lines)

# Calculate the number of chapters
num_chapters = max(min_chapters, math.ceil(total_lines / max_chapter_size))

# Ensure the number of chapters is a multiple of 6
if num_chapters % 6 != 0:
    num_chapters = ((num_chapters // 6) + 1) * 6

# Calculate the number of lines per chapter
lines_per_chapter = math.ceil(total_lines / num_chapters)

# Write to the new file
with open(new_file, 'w') as f:
    chapter = 1
    f.write("//.chapter-{}\n".format(chapter))
    for i, line in enumerate(lines, start=1):
        f.write(line)
        if i % lines_per_chapter == 0 and chapter < num_chapters and i < total_lines:
            chapter += 1
            f.write("//.chapter-{}\n".format(chapter))

    # Ensure the last chapter marker is added if not already
    if chapter < num_chapters and i < total_lines:
        f.write("//.chapter-{}\n".format(chapter + 1))
    else:
        f.write("//.end")
