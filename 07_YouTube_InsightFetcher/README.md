# 📺 YouTube InsightFetcher - Day 7 of #100DaysOfAI-Agents

> **📝 Note**: This is a CLI-based agent for extracting deep insights from YouTube videos, with full multilingual support and AI-powered translation/summarization.

A powerful command-line agent that fetches, translates, and summarizes YouTube video transcripts into actionable takeaways, memorable quotes, and key statistics — in any language you choose. Perfect for researchers, content creators, and anyone who wants to distill the essence of a video without watching the whole thing.

---

## 🎯 Purpose

YouTube InsightFetcher lets you:
- Instantly extract the most important points, quotes, and stats from any YouTube video (with transcript)
- Translate the content into your preferred language (e.g., Urdu, Hindi, Arabic, etc.) using AI
- Save or copy the summary for later use
- Focus on the full video or a specific time range

---

## 🔧 Key Features

- **🌐 Multilingual Support**: Translate and summarize in any language
- **🤖 AI Summarization**: Uses OpenAI for rich, structured summaries
- **📋 Actionable Takeaways**: With sentiment (Positive/Negative/Neutral)
- **💬 Memorable Quotes**: Verbatim extraction
- **📊 Key Statistics**: Pulls out important data points
- **⏱️ Time Range Selection**: Summarize the whole video or a specific segment
- **📁 Organized Saving**: Summaries saved in a dedicated `summaries/` folder
- **📋 Clipboard Copy**: Instantly copy output for sharing
- **🎨 Beautiful CLI Output**: Colored, readable, and user-friendly
- **🛠️ Modular Python Codebase**: Easy to extend and maintain

---

## 🛠️ Tech Stack

- **Python 3.7+**
- **youtube-transcript-api** - Fetch YouTube transcripts
- **openai** - AI-powered translation and summarization
- **langdetect** - Language detection
- **colorama** - Colored CLI output
- **pyperclip** - Clipboard support

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.7 or higher**
- **OpenAI API key**

### Installation
1. **Clone or download the YouTube InsightFetcher files**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your OpenAI API key:**
   - Windows (PowerShell):
     ```powershell
     $env:OPENAI_API_KEY="your-api-key-here"
     ```
   - macOS/Linux:
     ```bash
     export OPENAI_API_KEY="your-api-key-here"
     ```
   - Or add to a `.env` file:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

---

## 📖 Usage Guide

### Running the Agent
```bash
python main.py
```

### CLI Flow Example
```
YouTube InsightFetcher Agent
==============================
Enter YouTube video URL or ID: https://www.youtube.com/watch?v=dQw4w9WgXcQ
(Optional) Filter by channel name (leave blank to skip):
(Optional) Filter by video date (YYYY-MM-DD, leave blank to skip):
Do you want to extract insights from the full video or a specific time range? (Type: full / range): full
Enter your preferred output language (e.g., English, Urdu, Hindi, etc.): Urdu

Detected transcript language: en
Translating transcript... |
Translation complete!

===== Key Actionable Takeaways =====
- Example takeaway 1 [Positive]
- Example takeaway 2 [Neutral]

===== Memorable Quotes =====
- "Example quote"

===== Important Statistics/Data Points =====
- 42% of viewers ...

Do you want to save this summary to a file in the 'summaries' folder? (yes/no): yes
Enter filename to save (with .txt or .md extension): summary.md
Saved to summaries/summary.md
Do you want to copy the output to clipboard? (yes/no): yes
Output copied to clipboard.
```

---

## 📁 File Structure

```
07_YouTube_InsightFetcher/
├── main.py           # CLI entry point
├── cli.py            # User interaction and orchestration
├── transcript.py     # Transcript fetching and filtering
├── translation.py    # Language detection and translation
├── summarizer.py     # Summarization logic
├── utils.py          # Utility functions (saving, clipboard, loading, etc.)
├── config.py         # Environment/config management
├── requirements.txt  # Python dependencies
├── summaries/        # (auto-created) Saved summaries
└── README.md         # This file
```

---

## 🔧 Configuration

- **API Key**: Set `OPENAI_API_KEY` as an environment variable or in a `.env` file
- **Output Folder**: Summaries are saved in `summaries/` (auto-created)
- **Clipboard**: Uses `pyperclip` (may require xclip/xsel on Linux)

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Transcript not available | Some videos do not have transcripts. Try another video. |
| OpenAI API key error | Ensure your `OPENAI_API_KEY` is set before running. |
| Clipboard not working | Install `xclip`/`xsel` on Linux, check permissions. |
| Time range input | Use `mm:ss` or `hh:mm:ss` format. |
| Translation errors | Check your API key and internet connection. |

---

## 🔮 Future Enhancements

- Real channel/date filtering using YouTube Data API
- More advanced error handling and validation
- Web UI version
- Support for more translation providers
- Auto-detect and summarize playlists

---

## 🙏 Acknowledgments

- **youtube-transcript-api** for transcript extraction
- **OpenAI** for language and summarization
- **colorama** and **pyperclip** for CLI polish

---

**🎉 Ready to extract insights from any YouTube video!**

Run `python main.py` to get started.
