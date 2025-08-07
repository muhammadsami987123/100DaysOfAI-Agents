import sys
from transcript import fetch_transcript, filter_transcript_by_time, filter_transcript_by_channel_or_date
from translation import detect_language, translate_text
from summarizer import generate_summary
from utils import print_colored, save_to_file, copy_to_clipboard, parse_time, show_loading
import utils
import threading

def run_cli():
    print("YouTube InsightFetcher Agent\n==============================")
    url_or_id = input("Enter YouTube video URL or ID: ").strip()
    channel = input("(Optional) Filter by channel name (leave blank to skip): ").strip()
    date = input("(Optional) Filter by video date (YYYY-MM-DD, leave blank to skip): ").strip()
    mode = input("Do you want to extract insights from the full video or a specific time range? (Type: full / range): ").strip().lower()
    start_time = end_time = None
    if mode == "range":
        start_time = input("Start time (e.g., 02:00): ").strip()
        end_time = input("End time (e.g., 10:00): ").strip()
    output_lang = input("Enter your preferred output language (e.g., English, Urdu, Hindi, etc.): ").strip()

    transcript = fetch_transcript(url_or_id)
    if channel or date:
        transcript = filter_transcript_by_channel_or_date(transcript, channel, date)
    transcript = filter_transcript_by_time(transcript, start_time, end_time)
    text = " ".join([entry['text'] for entry in transcript])
    if not text.strip():
        print_colored("No transcript text found in the selected range.", "red")
        sys.exit(1)
    transcript_lang = detect_language(text) or "unknown"
    print_colored(f"Detected transcript language: {transcript_lang}", "cyan")
    if transcript_lang != output_lang:
        # Show loading animation in a separate thread
        loading = True
        def loading_anim():
            while loading:
                show_loading("Translating transcript", duration=1)
        t = threading.Thread(target=loading_anim)
        t.start()
        try:
            text = translate_text(text, transcript_lang, output_lang)
        finally:
            loading = False
            t.join()
        print_colored("Translation complete!", "green")
    insights = generate_summary(text, output_lang)
    print_colored("\n===== Key Actionable Takeaways =====", "cyan", bright=True)
    for t in insights.get("takeaways", []):
        sentiment = t.get('sentiment', 'Unknown')
        print(f"- {t.get('text', str(t))} [{sentiment}]")
    print_colored("\n===== Memorable Quotes =====", "magenta", bright=True)
    for q in insights.get("quotes", []):
        print(f"- {q}")
    print_colored("\n===== Important Statistics/Data Points =====", "blue", bright=True)
    for s in insights.get("statistics", []):
        print(f"- {s}")
    output = utils.format_output(insights)
    if input("Do you want to save this summary to a file in the 'summaries' folder? (yes/no): ").strip().lower() == "yes":
        save_to_file(output)
    if input("Do you want to copy the output to clipboard? (yes/no): ").strip().lower() == "yes":
        copy_to_clipboard(output)
