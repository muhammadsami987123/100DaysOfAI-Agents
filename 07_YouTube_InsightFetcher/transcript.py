import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def extract_video_id(url_or_id):
    patterns = [
        r"(?:v=|youtu.be/|youtube.com/embed/)([\w-]{11})",
        r"^([\w-]{11})$"
    ]
    for pat in patterns:
        m = re.search(pat, url_or_id)
        if m:
            return m.group(1)
    return None

def fetch_transcript(url_or_id):
    video_id = extract_video_id(url_or_id)
    if not video_id:
        raise ValueError("Invalid YouTube URL or ID.")
    try:
        transcript_obj = YouTubeTranscriptApi().fetch(video_id)
        transcript = [
            {'text': snippet.text, 'start': snippet.start, 'duration': snippet.duration}
            for snippet in transcript_obj
        ]
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound):
        raise RuntimeError("Transcript is not available for this video.")
    except Exception as e:
        raise RuntimeError(f"Error fetching transcript: {e}")

def filter_transcript_by_time(transcript, start_time=None, end_time=None):
    def time_to_seconds(t):
        if not t:
            return None
        parts = [int(p) for p in t.split(":")]
        if len(parts) == 2:
            return parts[0]*60 + parts[1]
        elif len(parts) == 3:
            return parts[0]*3600 + parts[1]*60 + parts[2]
        return None
    s = time_to_seconds(start_time)
    e = time_to_seconds(end_time)
    filtered = []
    for entry in transcript:
        if (s is not None and entry['start'] < s):
            continue
        if (e is not None and entry['start'] > e):
            continue
        filtered.append(entry)
    return filtered

def filter_transcript_by_channel_or_date(transcript, channel, date):
    # Placeholder: Actual implementation would require YouTube Data API
    # For now, just return transcript as-is
    return transcript
