from youtube_transcript_api import YouTubeTranscriptApi

def fetch_transcript(video_url, lang="en"):
    video_id = video_url.split("v=")[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
    text_data = []
    for entry in transcript:
        text_data.append({
            "start": entry["start"],
            "end": entry["start"] + entry["duration"],
            "text": entry["text"].strip()
        })
    return text_data

def combine_transcript_text(transcript_entries):
    return " ".join([e["text"] for e in transcript_entries if e["text"].strip()])
