import argparse
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_url):
    video_id = video_url.split("watch?v=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('en', 'en-US', 'ru', 'id'))
    for line in transcript:
        print(line['text'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get YouTube video transcript')
    parser.add_argument('url', help='YouTube video URL')
    args = parser.parse_args()
    get_transcript(args.url)
