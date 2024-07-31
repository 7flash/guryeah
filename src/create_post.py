import os
import sys
import subprocess
import re
import unidecode

hashnode_domain = os.getenv('HASHNODE_DOMAIN')

if not hashnode_domain:
    print("HASHNODE_DOMAIN environment variable not set.")
    sys.exit(1)

def get_video_metadata(video_id):
    try:
        # Use yt-dlp to get the video title and channel name with a custom delimiter
        delimiter = '|||'
        video_url = f"https://youtube.com/watch?v={video_id}"
        result = subprocess.run(['yt-dlp', '--no-warnings', '--print', f'%(title)s{delimiter}%(uploader)s', video_url], capture_output=True, text=True)
        result.check_returncode()
        title, channel = result.stdout.strip().split(delimiter)
        return title, channel
    except subprocess.CalledProcessError as e:
        print(f"Error fetching video metadata: {e}")
        sys.exit(1)

def generate_slug(title, video_id, max_length=50):
    # Transliterate to ASCII
    title = unidecode.unidecode(title)
    # Convert title to lowercase, replace spaces with hyphens, and remove non-alphanumeric characters
    slug = re.sub(r'[^a-z0-9-]', '', re.sub(r'\s+', '-', title.lower()))
    # Ensure the slug ends with the video ID and respects max URL length
    if len(slug) + len(video_id) + 1 > max_length:
        slug = slug[:max_length - len(video_id) - 1]
    slug = f"{slug}-{video_id}"
    return slug

def create_markdown_file(file_path):
    # Extract the video ID from the filename (assuming the format is "$id-blogpost.md")
    filename = os.path.basename(file_path)
    video_id = filename.rsplit('-', 1)[0]

    # Get the video title and channel name using yt-dlp
    title, channel = get_video_metadata(video_id)

    # Remove semicolons from title
    title = title.replace(":", "")

    # Generate the slug from the title
    slug = generate_slug(title, video_id)

    # Read the content from the input file
    with open(file_path, 'r') as file:
        content = file.read()

    # Define the frontmatter fields
    frontmatter = {
        "title": title.replace(':', '\\:').replace('"', '\\"'),
        "slug": slug,
        "tags": ["podcast", "video", "youtube"],
        "cover": "",
        "domain": hashnode_domain,
        "saveAsDraft": True,
        "enableToc": True,
        "seriesSlug": generate_slug(channel, "").rstrip('-')
    }

    # Create the output filename
    output_filename = os.path.join(os.path.dirname(file_path), f"{video_id}-hashnode.md")

    # Open the output file for writing
    with open(output_filename, 'w') as file:
        # Write the frontmatter
        file.write("---\n")
        for key, value in frontmatter.items():
            if isinstance(value, list):
                file.write(f"{key}: {', '.join(value)}\n")
            else:
                file.write(f"{key}: {value}\n")
        file.write("---\n\n")
                
        # Write the content
        file.write(content)

        # Write the "Watch" link
        file.write(f"> Watch: https://youtube.com/watch?v={video_id}\n\n")

    print(f"Markdown file '{output_filename}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]

    if not os.path.isfile(input_file_path):
        print(f"Error: File '{input_file_path}' not found.")
        sys.exit(1)

    create_markdown_file(input_file_path)
