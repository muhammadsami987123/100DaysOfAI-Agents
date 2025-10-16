# 🎤 PodcastIdeaBot - Day 73 of #100DaysOfAI-Agents

<div align="center">

![PodcastIdeaBot](https://img.shields.io/badge/PodcastIdeaBot-Day%2074-teal?style=for-the-badge&logo=podcastaddict&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange?style=for-the-badge&logo=openai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-blue?style=for-the-badge&logo=fastapi&logoColor=white)

**Plan and script podcast episodes on any topic – instantly and professionally!**

[🚀 Quick Start](#-quick-start) • [🎧 Features](#-features) • [🪄 Script Generation](#-generate-full-scripts) • [🎛️ API](#-api-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## 🎯 What is PodcastIdeaBot?

PodcastIdeaBot is an AI-powered agent that quickly turns any topic into structured, creative, and recording-ready podcast episode ideas—plus, you can generate a full professional script for your show with just a click.

Great for seasoned hosts, new podcasters, educators, or anyone wanting to ideate and script audio content efficiently.

### 🌟 Key Highlights
- **🎬 Generate Full Scripts**: Get a complete, broadcast-ready episode script in seconds
- **🧭 Professional Structure**: Episode title, outline, suggested guest, takeaways, target audience, and unique creative twist
- **⚡ Modern Interface**: Responsive web UI with card outputs and interactive features
- **🛠️ Dual Generation**: Ideation cards or instant scripts from the topic bar

---

## 🚀 Features

### 💡 Core Functionality
- **AI-Powered Ideation**: High-quality episode concepts powered by OpenAI or Gemini (configurable)
- **Single-Click Script Writing**: Instantly create podcast-ready scripts for any topic
- **Dynamic Guest Suggestions**: Context-aware guest type recommendations
- **Copy & Export Tools**: Fast export and copy for any card or script

### 🎨 Professional Episode Elements
- **Catchy Titles**: Natural language, podcast-ready titles
- **Structured Outlines**: 3-6 segment breakdowns for realistic episode flow
- **Key Takeaways**: Audience-facing insights listed per episode
- **Audience Targeting**: Clear positioning info for each episode
- **Unique Twists**: Creative segment or formatting suggestions

### 🖥️ Web Interface Highlights
- **Modern Card Layout**: Responsive, beautiful UI across all devices
- **Script Modal/Panel**: Generate and review full scripts without losing context
- **Accessible & Fast**: Keyboard friendly, rapid feedback
- **Mobile Responsive**: Looks great everywhere!

---

## ⚡ Quick Start

### 📋 Prerequisites
- **Python 3.8+**
- **OpenAI or Gemini API Key** (for LLM-powered mode, else fallback is local)
- **Internet connection** (for true AI mode)

### ☑️ Installation

```bash
# 1. Clone repo
$ git clone <repository-url>
$ cd 73_PodcastIdeaBot

# 2. Create & activate virtual environment (recommended)
$ python -m venv venv
$ venv\Scripts\activate  # Windows
$ source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Set up your API key(s) in .env (see below)
```

### 🔑 API Setup (.env)

```
OPENAI_API_KEY=sk-...   # For GPT-4, if desired
GEMINI_API_KEY=...      # For Gemini, if desired
LLM_MODEL=gemini        # Or 'openai' (default: gemini, fallback is local logic)
```

### 🚦 Run the App

```bash
uvicorn app:app --reload
# Open http://localhost:8000 in your browser
```

---

## 🎧 How to Use

1. Enter your episode topic and, optionally, a type of guest (or leave blank for smart suggestions).
2. Choose the number of ideas you want.
3. **Click Generate:** See podcast-ready episode ideas with all structural elements.
4. **Card Tools:** Copy, expand outline, or instantly generate a script for any card.
5. **OR, use the top 'Generate Script' button'** to instantly write a full professional podcast script for your topic.
6. Copy or export outputs as desired!

---

## 🖥️ Screenshots (UI Examples)

> _Add your screenshots here—web interface, instant script, card layout, etc._

---

## 🏗️ Project Structure

```
73_PodcastIdeaBot/
├── agent.py         # Core logic for podcast idea and script generation
├── app.py           # FastAPI app with endpoints
├── config.py        # API keys and model config
├── requirements.txt # Requirements
├── utils/
│   └── llm_service.py # LLM selection, JSON parsing
├── template/
│   └── index.html   # Beautiful frontend with Tailwind CSS
└── README.md
```

---

## 🦾 Technical Stack
| Component              | Technology         | Notes                          |
|-----------------------|--------------------|-------------------------------|
| **Backend**           | Python 3.8+        | Core business logic           |
| **LLM Engine**        | Gemini / OpenAI    | Google Gemini (default) or OpenAI GPT-4/4o |
| **Web Framework**     | FastAPI            | RESTful backend, async        |
| **Frontend**          | Jinja2, TailwindCSS, Vanilla JS | Modern, animated, responsive |
| **Deployment**        | Uvicorn            | Dev server, can use Gunicorn  |
| **Env Config**        | python-dotenv      | Manage keys and model select  |

---

## 🎛️ API Documentation

### 🤖 `/generate` (POST)
- **Purpose:** Return a list of idea dicts based on topic, guest_type, count
- **Body:** `{ topic (str), guest_type (str, optional), count (int, 1-5) }`
- **Returns:** `{ ideas: [ { title, outline, takeaways, audience, guest_type, twist } ] }`

### 📝 `/generate_script` (POST)
- **Purpose:** Generate a full script from an idea object (or from topic/guest)
- **Body:** `{ idea: { title, outline?, guest_type?, takeaways?, audience?, twist? } }`
- **Returns:** `{ script: "..." }`

---

## 🧪 Testing

```bash
# Run quick installation test (if available):
python test_installation.py
```

---

## 💡 Tips & Best Practices
- **Try with and without a guest type:** The auto-guest feature is smart.
- **Use the script button** from the top, or from idea cards, for flexible workflow.
- **Use the copy tools** for fast export to your podcast planner/editor.
- **Switch LLM models** with the `LLM_MODEL` config as needed.

---

## 🤝 Contributing

We welcome improvements! Please:
- Fork the repository
- Use a feature branch
- Write tests where possible
- Update this README with new features
- Open a Pull Request 💡

--

## 📞 Support & Community
- Use GitHub Issues for questions and feedback
- Share your podcast plans and feedback!
- Part of #100DaysOfAI-Agents by Muhammad Sami Asghar Mughal

---

<div align="center">

## 🎉 Ready to Plan Your Next Podcast?
**Modern podcast episode ideation and script writing, powered by AI.**

---

_Made with ❤️ by the #100DaysOfAI-Agents community (Day 73 of 100)_

</div>


