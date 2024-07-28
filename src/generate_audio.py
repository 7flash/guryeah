import os
import sys
import argparse
import requests
import random
import logging

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/{}"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
}

data = {"model_id": "eleven_multilingual_v2", "voice_settings": {}}

def main():
    parser = argparse.ArgumentParser(description="Text to Speech converter.")
    parser.add_argument("input_file", help="Path to the input text file.")
    parser.add_argument("output_file", help="Path to the output mp3 file.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    api_key = os.getenv("XI_API_KEY")
    if not api_key:
        logger.error("XI_API_KEY is missing in environment variables.")
        sys.exit(1)
    headers["xi-api-key"] = api_key

    voice_id = os.getenv("VOICE_ID")
    if not voice_id:
        logger.error("VOICE_ID is missing in environment variables.")
        sys.exit(1)

    stability = os.getenv("STABILITY", 1.0)
    data["voice_settings"]["stability"] = float(stability)

    similarity_boost = os.getenv("SIMILARITY_BOOST", round(random.uniform(0, 1), 2))
    data["voice_settings"]["similarity_boost"] = float(similarity_boost)

    style = os.getenv("STYLE", round(random.uniform(0, 1), 2))
    data["voice_settings"]["style"] = float(style)

    speaker_boost = os.getenv("SPEAKER_BOOST", True)
    data["voice_settings"]["use_speaker_boost"] = speaker_boost

    print(data)

    if not os.path.isfile(args.input_file):
        logger.error(f"Input file {args.input_file} does not exist.")
        sys.exit(1)

    with open(args.input_file, "r") as f:
        data["text"] = f.read()

    try:
        response = requests.post(url.format(voice_id), json=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}, Response: {response.text}")
        sys.exit(1)

    with open(args.output_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    logger.info(f"Successfully converted text to speech. Output saved to {args.output_file}.")

    # Save details for sending with audio
    details_file = f"{args.output_file}.details.txt"
    with open(details_file, "w") as f:
        f.write(f"stability: {stability}\n")
        f.write(f"similarity_boost: {similarity_boost}\n")
        f.write(f"style: {style}\n")
        f.write(f"speaker_boost: {speaker_boost}\n")
        f.write(f"text: {data['text']}\n")

    logger.info(f"Details saved to {details_file}")

if __name__ == "__main__":
    main()
