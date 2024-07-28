## Technical Details

### Step 1: Extracting the Transcript

The first step involves extracting the transcript from the YouTube video. This is achieved using the `get_transcript.py` script. If the transcript is disabled, the script terminates the process.

### Step 2: Splitting the Transcript into Chapters

Once the transcript is available, it is split into chapters using the `add_chapters.py` script. The number of chapters is determined based on a minimum and maximum chapter size.

### Step 3: Creating Sections with Overlap

The transcript chapters are then divided into overlapping sections to ensure no important parts are cut off. Sections are created with a defined size and overlap.

### Step 4: Generating QA Pairs

For each section, a series of question-answer pairs are generated using GPT-4o. These QA pairs are extracted directly from the transcript without any paraphrasing or interpretation.

### Step 5: Summarizing and Highlighting

Using the generated QA pairs, the script creates summaries for each section, focusing on verbatim quotes without adding any external comments or questions.

### Step 6: Coherent Paragraph Generation

The highlighted summaries are then transformed into coherent paragraphs, formatted with markdown. Transitions between sections are facilitated using italicized comments to maintain flow and readability.

### Step 7: Extracting Core Insights

The script then extracts a single core insight (formatted to fit a viral, Instagram-like style) from each paragraph. These insights are designed to be engaging and shareable.

### Step 8: Merging Insights and Paragraphs

The insights and paragraphs are then merged to form the complete document. Each section starts with an insight followed by the corresponding paragraph.

### Step 9: Creating and Formatting the Hashnode Post

Finally, the complete content is formatted into a markdown file compatible with Hashnode. The script automatically creates a post on Hashnode and saves a copy of the file locally.

### Additional Notes

- Environment variables such as `MODEL`, `TEMPERATURE`, and file paths are defined at the beginning of the script.
- The script ensures files are concatenated in sequence, and sections fit together naturally.
- Logging statements have been commented out but can be activated for debugging.
