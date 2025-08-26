# Day 26: FocusTimerAgent – Desktop Pomodoro App (GUI + TTS)

A polished desktop Pomodoro timer with a modern Tkinter UI, second-level controls, voice alerts (TTS), notifications, and an optional AI coach.

## Features

- Start, pause, resume, stop timer
- Custom work/short-break/long-break durations
- Automatic long break after cycles
- Spoken reminders (TTS) you can mute/unmute
- Status and daily history persisted to JSON
- Optional OpenAI "coach" for short motivational tips

## Quick Start (GUI)

### Installation (Windows)
```bash
cd 26_FocusTimerAgent
install.bat
```

### Start GUI
```bash
start.bat  # choose "Start GUI"
```

## Using the App

- Work/Break/Long: set minutes and seconds using the spin boxes (GUI)
- Presets: choose from the dropdown (Custom/Pomodoro/Long Focus/Quick) and click Reset to apply
- Cycles/Long: after this number of focus sessions, the next break becomes a long break
- Voice toggle: enable/disable TTS prompts
- Controls: Start, Pause, Resume, Stop

Alerts used:
- Start focus: "Time to focus."
- Short break: "Break time! You've earned it."
- Long break: "Take a longer break now."
- End break: "Let's get back to work."

Session History:
- Bottom panel lists completed focus sessions per day
- Stored in `data/history.json`

## CLI (optional)
```bash
# Start with defaults (25/5, long 20, 4 cycles)
python -m 26_FocusTimerAgent.main start

# Start with custom durations (in minutes)
python -m 26_FocusTimerAgent.main start --work 25 --break 5 --long 20 --cycles 4

# Controls
python -m 26_FocusTimerAgent.main pause
python -m 26_FocusTimerAgent.main resume
python -m 26_FocusTimerAgent.main stop
python -m 26_FocusTimerAgent.main mute
python -m 26_FocusTimerAgent.main unmute

# Status and history
python -m 26_FocusTimerAgent.main status
python -m 26_FocusTimerAgent.main history

# Ask the coach (requires OPENAI_API_KEY)
python -m 26_FocusTimerAgent.main coach --context "struggling" --mood "tired" --minutes-left 7
```

### Commands Reference (quick)
```text
GUI           start.bat  -> choose "Start GUI"

CLI           python -m 26_FocusTimerAgent.main <command> [options]
  start       --work <min> --break <min> --long <min> --cycles <n> [--mute]
  pause       pause current session
  resume      resume current session
  stop        stop and set mode to idle
  status      print current mode/remaining time/cycle/voice status
  history     print completed focus sessions per day
  mute        disable TTS (can still re-enable in GUI)
  unmute      enable TTS
  coach       ask OpenAI coach for a short tip
```

## OpenAI Coach (optional)

Set environment variables (use `.env` in `26_FocusTimerAgent` if you prefer):
```env
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o-mini
```
Call the coach from CLI for a brief motivational tip:
```bash
python -m 26_FocusTimerAgent.main coach --context "mid-session" --mood "energized" --minutes-left 12
```

## Voice Reminders (TTS)

Phrases used:
- Start focus: "Time to focus."
- Short break: "Break time! You've earned it."
- Long break: "Take a longer break now."
- End of break: "Let's get back to work."

Mute or unmute anytime with the CLI commands.

## Folder Structure

```text
26_FocusTimerAgent/
  ai_agent.py              # OpenAI coach (optional)
  config.py                # Defaults and paths (JSON storage)
  gui_app.py               # Tkinter GUI entrypoint
  main.py                  # CLI entrypoint
  timer.py                 # CLI timer engine
  tts_service.py           # TTS wrapper and phrases
  requirements.txt
  install.bat              # Setup venv + deps (prefers root venv)
  start.bat                # Launcher (GUI + CLI)
  build-windows.bat        # PyInstaller onefile build
  data/
    state.json             # CLI state (when using CLI)
    history.json           # Daily session counts
```

## Build a Standalone EXE (Windows)

```bash
cd 26_FocusTimerAgent
build-windows.bat
```

The executable `FocusTimerAgent.exe` will be in `dist/`.

## Troubleshooting & FAQ

- The EXE doesn’t open
  - Run from terminal to see the message: `dist\FocusTimerAgent.exe`
  - If it mentions missing modules, rebuild with `build-windows.bat` (it adds hidden-imports)
  - If it says `Local module not found: config.py`, rebuild; the builder now bundles config/tts

- No sound or TTS
  - Check Windows volume and output device
  - TTS requires `pyttsx3`; reinstall deps via `install.bat`
  - On some systems you must install Microsoft SAPI5 voices; try “English (United States)” voice pack

- Notifications not showing
  - On some systems, OS notification permission is required; the app falls back to a popup

- Using my existing repo venv
  - `install.bat` and `start.bat` prefer `..\venv` and fall back to a local `venv`

- Resetting presets
  - Choose a preset then click Reset to apply values without starting

- Build errors (PyInstaller)
  - `ModuleNotFoundError: win32com`: `pip install pywin32`, then rebuild
  - `ImportError: No module named 'pyttsx3.drivers.sapi5'`: ensure `pyttsx3` is installed; our builder adds hidden-imports
  - Antivirus blocks EXE: whitelist `dist/FocusTimerAgent.exe` or run from a signed path

- CLI import error: `attempted relative import with no known parent package`
  - Use `python -m 26_FocusTimerAgent.main ...` from the repo root, or run `python main.py ...` from inside the folder (we added fallbacks)

- Where are logs/data saved?
  - History: `26_FocusTimerAgent/data/history.json`
  - CLI state: `26_FocusTimerAgent/data/state.json`

- How do minutes/seconds work in GUI?
  - Set exact minutes and seconds in the spin boxes; presets fill these automatically; progress bar updates with second precision

## Notes

- TTS uses `pyttsx3` which works offline on Windows/macOS/Linux.
- If TTS fails to initialize, the app still runs silently.
- To enable the coach, set `OPENAI_API_KEY` (optional `OPENAI_MODEL`, defaults to `gpt-4o-mini`). You can create a `.env` file in this folder.


