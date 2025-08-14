import argparse
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

try:
    from langdetect import detect
except Exception:  # pragma: no cover
    detect = None  # type: ignore

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover
    sr = None  # type: ignore

try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None  # type: ignore

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


console = Console()


@dataclass
class ParsedCommand:
    action: Optional[str] = None  # create | open | delete | show
    target_type: Optional[str] = None  # file | folder | unknown
    name: Optional[str] = None  # e.g., notes.txt or data
    explicit_path: Optional[str] = None  # e.g., C:\Users\.. or ~/Desktop
    base_dir_key: Optional[str] = None  # desktop | downloads | documents | pictures | music | videos


class SpeechOutput:
    def __init__(self, enable_voice: bool = True, rate: int = 175):
        self.enable_voice = enable_voice and (pyttsx3 is not None)
        self.engine = None
        if self.enable_voice:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", rate)
            except Exception:
                self.enable_voice = False

    def say(self, text: str) -> None:
        if not self.enable_voice or not self.engine:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            pass


class SpeechInput:
    def __init__(self, language_hint: Optional[str] = None):
        self.language_hint = language_hint
        self.available = sr is not None
        if self.available:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.dynamic_energy_threshold = True
            except Exception:
                self.available = False

    def listen_once(self) -> Optional[str]:
        if not self.available:
            return None
        try:
            with sr.Microphone() as source:
                with console.status("🎤 Listening...", spinner="dots"):
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            # Prefer Google's free recognizer for demo purposes
            lang = self.language_hint or "en-US"
            try:
                text = self.recognizer.recognize_google(audio, language=lang)
                return text
            except Exception:
                # Fallback to Sphinx if available
                try:
                    text = self.recognizer.recognize_sphinx(audio)
                    return text
                except Exception:
                    return None
        except Exception:
            return None


class CommandParser:
    def __init__(self):
        # Canonical directories mapping (synonyms → canonical key)
        self.dir_aliases = self._build_dir_aliases()
        # Action and type aliases
        self.action_aliases = self._build_action_aliases()
        self.type_aliases = self._build_type_aliases()
        # Prepositions / connectors
        self.prep_in = {"in", "inside", "under", "on", "پر", "میں", "کے اندر", "के अंदर", "में", "पर"}
        self.prep_from = {"from", "سے", "से"}
        self.named_tokens = {"named", "نام کی", "नाम का"}

    @staticmethod
    def _normalize_spoken_punctuation(text: str) -> str:
        s = text
        # Normalize common spoken punctuation to symbols
        s = re.sub(r"\b(dot|point)\b", ".", s, flags=re.IGNORECASE)
        s = re.sub(r"\b(slash)\b", "/", s, flags=re.IGNORECASE)
        s = re.sub(r"\b(back\\s*slash)\b", "\\\\", s, flags=re.IGNORECASE)
        s = re.sub(r"\b(underscore)\b", "_", s, flags=re.IGNORECASE)
        s = re.sub(r"\b(dash|hyphen)\b", "-", s, flags=re.IGNORECASE)
        # Collapse spaces around inserted punctuation
        s = re.sub(r"\s*\.(\s*)", ".", s)
        s = re.sub(r"\s*/(\s*)", "/", s)
        s = re.sub(r"\s*-(\s*)", "-", s)
        s = re.sub(r"\s*_(\s*)", "_", s)
        return s

    @staticmethod
    def _build_dir_aliases():
        return {
            # Desktop
            "desktop": "desktop",
            "ڈیسک ٹاپ": "desktop",
            "डेस्कटॉप": "desktop",
            "desktop folder": "desktop",
            "desktop directory": "desktop",
            # Downloads
            "downloads": "downloads",
            "ڈاؤن لوڈز": "downloads",
            "डाउनलोड्स": "downloads",
            "download": "downloads",
            "डाउनलोड": "downloads",
            "ڈاؤن لوڈ": "downloads",
            "downloads folder": "downloads",
            "downloads directory": "downloads",
            "download folder": "downloads",
            "download directory": "downloads",
            "डाउनलोड फोल्डर": "downloads",
            "डाउनलोड फ़ोल्डर": "downloads",
            "डाउनलोड डायरेक्टरी": "downloads",
            # Documents
            "documents": "documents",
            "docs": "documents",
            "دستاویزات": "documents",
            "ڈاکومنٹس": "documents",
            "डॉक्यूमेंट्स": "documents",
            "मेरे डॉक्यूमेंट्स": "documents",
            "documents folder": "documents",
            "documents directory": "documents",
            # Pictures
            "pictures": "pictures",
            "photos": "pictures",
            "تصاویر": "pictures",
            "फोटो": "pictures",
            # Music
            "music": "music",
            "گانے": "music",
            "میوزک": "music",
            "संगीत": "music",
            # Videos
            "videos": "videos",
            "video": "videos",
            "ویڈیوز": "videos",
            "वीडियो": "videos",
        }

    @staticmethod
    def _build_action_aliases():
        return {
            # create
            "create": "create",
            "make": "create",
            "mkdir": "create",
            "new": "create",
            "make a": "create",
            "make new": "create",
            "made": "create",
            "you made": "create",
            "you make": "create",
            "please make": "create",
            "please create": "create",
            "build": "create",
            "generate": "create",
            "بناؤ": "create",
            "بناو": "create",
            "بنا دو": "create",
            "بنادو": "create",
            "تیار": "create",
            "بنائیں": "create",
            "बनाओ": "create",
            "बनाइए": "create",
            "बना दो": "create",
            "बना दीजिए": "create",
            # open
            "open": "open",
            "launch": "open",
            "کھولو": "open",
            "کھولیں": "open",
            "کھول دو": "open",
            "खोलो": "open",
            "ओपन": "open",
            # delete
            "delete": "delete",
            "remove": "delete",
            "erase": "delete",
            "del": "delete",
            "ڈلیٹ": "delete",
            "حذف": "delete",
            "مٹا": "delete",
            "ہٹا": "delete",
            "हटाओ": "delete",
            "मिटाओ": "delete",
            "मिटा दो": "delete",
            "हटा दो": "delete",
            # show/list
            "show": "show",
            "list": "show",
            "display": "show",
            "دکھاؤ": "show",
            "dikhao": "show",
            "दिखाओ": "show",
        }

    @staticmethod
    def _build_type_aliases():
        return {
            # file
            "file": "file",
            "فائل": "file",
            "फ़ाइल": "file",
            # folder
            "folder": "folder",
            "directory": "folder",
            "dir": "folder",
            "فولڈر": "folder",
            "ڈائریکٹری": "folder",
            "फ़ोल्डर": "folder",
            "डायरेक्टरी": "folder",
        }

    def detect_language(self, text: str) -> Optional[str]:
        if not text:
            return None
        if detect is None:
            return None
        try:
            return detect(text)
        except Exception:
            return None

    def _find_known_dir(self, lowered: str) -> Optional[str]:
        # Return the last mentioned known directory alias to respect phrases like "inside X"
        found: Optional[str] = None
        for alias, key in self.dir_aliases.items():
            if alias in lowered:
                found = key
        return found

    @staticmethod
    def _looks_like_path(token: str) -> bool:
        if not token:
            return False
        token = token.strip().strip('"\'')
        return (
            re.match(r"^[a-zA-Z]:\\", token) is not None  # Windows drive
            or token.startswith("~/")
            or token.startswith("~\\")
            or token.startswith("/")
            or token.startswith(".\\")
            or token.startswith("./")
            or ("\\" in token or "/" in token)
        )

    def _extract_explicit_path(self, text: str) -> Optional[str]:
        # Look for quoted paths first
        quoted = re.findall(r"[\"']([^\"']+)[\"']", text)
        for q in quoted:
            if self._looks_like_path(q):
                return q
        # Then search for path-like tokens
        tokens = re.split(r"\s+", text)
        for tok in tokens:
            if self._looks_like_path(tok):
                return tok
        return None

    def _extract_name(self, lowered: str) -> Optional[str]:
        # 0) Normalize spoken punctuation before name detection
        lowered = self._normalize_spoken_punctuation(lowered)
        # 0.5) Direct patterns: "file|folder named|called <name>"
        m = re.search(r"\b(file|folder|directory|dir)\s+(named|called)\s+([\w .\-]+)\b", lowered)
        if m:
            return self._clean_candidate_name(m.group(3).strip())
        # 0.55) English: "(file|folder) name is <name>" or simply "name is <name>"
        m = re.search(r"\b(file|folder|directory|dir)\s+name\s+is\s+([\w .\-]+)\b", lowered)
        if m:
            return self._clean_candidate_name(m.group(2).strip())
        m = re.search(r"\bname\s+is\s+([\w .\-]+)\b", lowered)
        if m:
            return self._clean_candidate_name(m.group(1).strip())
        # 0.6) Urdu/Hindi: "جس کا نام X ہو" / "जिसका नाम X हो"
        m = re.search(r"جس کا نام\s+([\w .\-]+)\s+ہو", lowered)
        if m:
            return self._clean_candidate_name(m.group(1).strip())
        m = re.search(r"जिसका नाम\s+([\w .\-]+)\s+हो", lowered)
        if m:
            return self._clean_candidate_name(m.group(1).strip())
        # 0.65) Urdu/Hindi: "نام ہے X" / "नाम है X" and "نام X ہے" / "नाम X है|हो"
        m = re.search(r"نام\s+ہے\s+([\w .\-]+)", lowered)
        if m:
            return self._clean_candidate_name(m.group(1).strip())
        m = re.search(r"نام\s+([\w .\-]+)\s+(ہے|ہو)", lowered)
        if m:
            return self._clean_candidate_name(m.group(1).strip())
        m = re.search(r"नाम\s+है\s+([\w .\-]+)", lowered)
        if m:
            return self._clean_candidate_name(m.group(1).strip())
        m = re.search(r"नाम\s+([\w .\-]+)\s+(है|हो)", lowered)
        if m:
            return self._clean_candidate_name(m.group(1).strip())
        # 1) Patterns with noun before the type: "<name> folder", "<name> file"
        m = re.search(r"\b([\w .\-]+?)\s+(folder|फ़ोल्डर|فولڈر|file|फ़ाइल|فائل)\b", lowered)
        if m:
            candidate = m.group(1).strip()
            if candidate:
                return self._clean_candidate_name(candidate)
        # 2) Urdu/Hindi patterns: "<name> نام کی فائل", "<name> नाम का folder"
        m = re.search(r"([\w .\-]+)\s+(نام کی|नाम का)\s+(فائل|फ़ाइल|folder|फ़ोल्डर|فولڈر)", lowered)
        if m:
            candidate = m.group(1).strip()
            return self._clean_candidate_name(candidate)
        # 3) English patterns: "file <name>", "folder <name>"
        m = re.search(r"\b(file|folder|directory|dir)\s+([\w .\-]+)\b", lowered)
        if m:
            return self._clean_candidate_name(m.group(2).strip())
        # 4) Generic filename with extension
        m = re.search(r"\b([\w .\-]+\.[a-z0-9]{1,8})\b", lowered)
        if m:
            return self._clean_candidate_name(m.group(1).strip())
        # 5) After word 'named'
        m = re.search(r"\bnamed\s+([\w .\-]+)\b", lowered)
        if m:
            return self._clean_candidate_name(m.group(1).strip())
        # 6) Simple pattern "make a file <name>" or "create file <name>"
        m = re.search(r"\b(make|create|made|generate|build)\b\s+(a\s+)?\b(file|folder|directory|dir)\b\s+([\w .\-]+)\b", lowered)
        if m:
            return self._clean_candidate_name(m.group(4).strip())
        return None

    @staticmethod
    def _clean_candidate_name(name: str) -> str:
        cleaned = name.strip().strip('"\'')
        # Remove common fillers at boundaries
        fillers = {
            "a", "an", "the", "please", "kindly", "me", "for", "for", "for me",
            "my", "your", "you", "named", "called", "name", "is",
            # action verbs at boundaries we don't want as names
            "make", "create", "made", "build", "generate",
            # types at edges
            "file", "folder", "directory", "dir"
        }
        tokens = [t for t in re.split(r"\s+", cleaned) if t]
        # Trim leading fillers
        while tokens and tokens[0] in fillers:
            tokens.pop(0)
        # Trim trailing fillers
        while tokens and tokens[-1] in fillers:
            tokens.pop()
        cleaned = " ".join(tokens).strip()
        return cleaned

    def parse(self, text: str) -> ParsedCommand:
        if not text:
            return ParsedCommand()
        normalized = self._normalize_spoken_punctuation(text)
        lowered = normalized.strip().lower()
        # Heuristic: if a probable filename with extension exists anywhere, capture it
        ext_match = re.search(r"\b([\w]+(?:[ _\-][\w]+)*\.[a-z0-9]{1,8})\b", normalized, flags=re.IGNORECASE)
        probable_name = ext_match.group(1).strip() if ext_match else None

        # Find action
        action = None
        for token, act in self.action_aliases.items():
            if f" {token} " in f" {lowered} ":
                action = act
        # Find target type
        target_type = None
        for token, typ in self.type_aliases.items():
            if f" {token} " in f" {lowered} ":
                target_type = typ

        # Explicit path or known base dir
        explicit_path = self._extract_explicit_path(text)
        base_dir_key = self._find_known_dir(lowered)

        # Extract name
        name = self._extract_name(lowered)
        if not name and probable_name:
            name = probable_name

        # Infer type from name if missing
        if not target_type and name:
            target_type = "file" if "." in name else "folder"

        return ParsedCommand(
            action=action,
            target_type=target_type,
            name=name,
            explicit_path=explicit_path,
            base_dir_key=base_dir_key,
        )


class JarvisFileManager:
    def __init__(self, log_path: Path, tts: SpeechOutput, speak_errors: bool = True):
        self.tts = tts
        self.speak_errors = speak_errors
        self.created_index_path = Path(__file__).parent / "created_items.json"
        self._setup_logging(log_path)

    def _setup_logging(self, log_path: Path) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(log_path, encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )
        logging.info("JarvisFileManager started")

    @staticmethod
    def _known_base_dirs() -> dict:
        home = Path.home()
        return {
            "desktop": home / "Desktop",
            "downloads": home / "Downloads",
            "documents": home / "Documents",
            "pictures": home / "Pictures",
            "music": home / "Music",
            "videos": home / "Videos",
        }

    def _resolve_base_dir(self, key: Optional[str]) -> Path:
        base_map = self._known_base_dirs()
        if key and key in base_map:
            return base_map[key]
        # Default to Desktop
        return base_map["desktop"]

    @staticmethod
    def _sanitize_name(name: str) -> str:
        return name.strip().strip('"\'')

    def _resolve_target_path(self, cmd: ParsedCommand) -> Tuple[Path, bool]:
        # Returns (path, is_explicit)
        if cmd.explicit_path:
            p = Path(os.path.expanduser(cmd.explicit_path)).resolve()
            return p, True
        base_dir = self._resolve_base_dir(cmd.base_dir_key)
        if cmd.name:
            return (base_dir / self._sanitize_name(cmd.name)).resolve(), False
        return base_dir.resolve(), False

    @staticmethod
    def _generate_default_name(target_type: str, base_dir: Path) -> str:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        if target_type == "file":
            name = f"new_file_{timestamp}.txt"
            # Ensure uniqueness
            idx = 1
            candidate = base_dir / name
            while candidate.exists():
                candidate = base_dir / f"new_file_{timestamp}_{idx}.txt"
                idx += 1
            return candidate.name
        else:
            name = f"New Folder {timestamp}"
            idx = 1
            candidate = base_dir / name
            while candidate.exists():
                candidate = base_dir / f"New Folder {timestamp} ({idx})"
                idx += 1
            return candidate.name

    def _record_created(self, path: Path, kind: str) -> None:
        items = []
        if self.created_index_path.exists():
            try:
                items = json.loads(self.created_index_path.read_text(encoding="utf-8"))
            except Exception:
                items = []
        items.append({
            "path": str(path),
            "type": kind,
            "timestamp": int(time.time()),
        })
        self.created_index_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    def _succeed(self, message: str) -> None:
        console.print(f"[bold green]✔ {message}[/bold green]")
        logging.info(message)
        self.tts.say(message)

    def _fail(self, message: str) -> None:
        console.print(f"[bold red]✘ {message}[/bold red]")
        logging.error(message)
        if self.speak_errors:
            self.tts.say(message)

    def create(self, cmd: ParsedCommand) -> None:
        if not cmd.target_type:
            cmd.target_type = "file" if (cmd.name and "." in cmd.name) else "folder"
        # If user didn't specify a name at all, generate a default inside the base directory
        if not cmd.name:
            base_dir = self._resolve_base_dir(cmd.base_dir_key)
            default_name = self._generate_default_name(cmd.target_type, base_dir)
            cmd.name = default_name
        # Ensure we preserve exact spoken name including extensions
        path, _ = self._resolve_target_path(cmd)

        try:
            if cmd.target_type == "file":
                with console.status(f"✅ Creating file in {path.parent}...", spinner="dots"):
                    if path.exists():
                        self._fail(f"Error: File already exists at {path}")
                        return
                    if not path.parent.exists():
                        self._fail("Error: Directory not found")
                        return
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.touch()
                self._record_created(path, "file")
                self._succeed(f"File created at {path}")
            else:
                with console.status(f"✅ Creating folder in {path.parent}...", spinner="dots"):
                    if path.exists():
                        self._fail(f"Error: Folder already exists at {path}")
                        return
                    if not path.parent.exists():
                        self._fail("Error: Directory not found")
                        return
                    # If user gave no explicit name phrases but type is folder and
                    # the extracted name is actually the word 'make' or other action, fallback to New Folder
                    folder_name = path.name.strip()
                    confusing_names = {"make", "create", "made", "build", "generate"}
                    if folder_name.lower() in confusing_names:
                        base_dir = path.parent
                        fallback_name = self._generate_default_name("folder", base_dir)
                        path = (base_dir / fallback_name).resolve()
                    path.mkdir(parents=True, exist_ok=False)
                self._record_created(path, "folder")
                self._succeed(f"Folder created at {path}")
        except Exception as e:
            self._fail(f"Error: {e}")

    def open(self, cmd: ParsedCommand) -> None:
        path, _ = self._resolve_target_path(cmd)
        if not path.exists():
            self._fail(f"Error: Path not found: {path}")
            return
        try:
            with console.status("🔄 Opening...", spinner="dots"):
                if sys.platform.startswith("win"):
                    os.startfile(str(path))  # type: ignore[attr-defined]
                elif sys.platform == "darwin":
                    os.system(f"open '{path}'")
                else:
                    os.system(f"xdg-open '{path}'")
            self._succeed(f"Opened {path}")
        except Exception as e:
            self._fail(f"Error: {e}")

    def delete(self, cmd: ParsedCommand) -> None:
        import shutil

        path, _ = self._resolve_target_path(cmd)
        if not path.exists():
            self._fail(f"Error: Path not found: {path}")
            return
        try:
            with console.status("🗑️ Deleting...", spinner="dots"):
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
            self._succeed(f"{'Folder' if path.is_dir() else 'File'} deleted: {path}")
        except Exception as e:
            self._fail(f"Error: {e}")

    def show_created(self) -> None:
        items = []
        if self.created_index_path.exists():
            try:
                items = json.loads(self.created_index_path.read_text(encoding="utf-8"))
            except Exception:
                items = []
        if not items:
            console.print("[bold yellow]No created items recorded yet.[/bold yellow]")
            return
        table = Table(title="Created Items", show_header=True, header_style="bold magenta")
        table.add_column("#", justify="right", style="cyan", no_wrap=True)
        table.add_column("Type", style="green")
        table.add_column("Path", style="white")
        table.add_column("Timestamp", style="yellow")
        for idx, it in enumerate(items, start=1):
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(it.get("timestamp", 0)))
            table.add_row(str(idx), it.get("type", "?"), it.get("path", ""), ts)
        console.print(table)


def run_cli():
    parser = argparse.ArgumentParser(description="Day 14 – CLI-Based JarvisFileManager")
    parser.add_argument("--log", default=str(Path(__file__).parent / "logs.txt"), help="Path to logs file")
    parser.add_argument("--no-voice", action="store_true", help="Disable text-to-speech output")
    parser.add_argument("--speak-errors", action="store_true", help="Speak back errors as well")
    parser.add_argument("--lang", default="auto", help="Language hint for STT (e.g., en-US, hi-IN, ur-PK)")
    parser.add_argument("--text", help="Provide a text command instead of voice input")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    tts = SpeechOutput(enable_voice=not args.no_voice)
    manager = JarvisFileManager(log_path=Path(args.log), tts=tts, speak_errors=args.speak_errors)
    parser_engine = CommandParser()

    # Header panel
    console.print(Panel.fit(Text("JarvisFileManager – Voice-controlled File Manager (EN/HI/UR)", style="bold white"), style="cyan"))

    def process_text(text: str) -> None:
        with console.status("🧠 Understanding your command...", spinner="dots"):
            if not text:
                manager._fail("Could not understand the command.")
                return
            console.print(f"[bold blue]🗣 Command:[/bold blue] {text}")
            # Try robust language detection; if short text, keep previous or hint
            detected_lang = parser_engine.detect_language(text)
            lang = detected_lang or "auto"
            console.print(f"[dim]Detected language: {lang}[/dim]")
            cmd = parser_engine.parse(text)
        if not cmd.action:
            # special case: show created files
            if re.search(r"\b(show|list|display)\b.*\b(created|made|بنائی|بنائے|बनाई|बनाए)\b", text.lower()):
                manager.show_created()
                return
            # Try forgiving detection if user says e.g., "you made a file ..."
            if re.search(r"\b(you\s+made|you\s+make|please\s+make|please\s+create|build|generate)\b", text.lower()):
                cmd.action = "create"
            elif re.search(r"\b(open|launch)\b", text.lower()):
                cmd.action = "open"
            elif re.search(r"\b(delete|remove|erase|del|हटाओ|मिटाओ|ڈلیٹ|حذف)\b", text.lower()):
                cmd.action = "delete"
            elif re.search(r"\b(show|list|display)\b", text.lower()):
                cmd.action = "show"
            else:
                manager._fail("Sorry, I couldn't detect the action (create/open/delete/show).")
                return
        if cmd.action == "create":
            manager.create(cmd)
        elif cmd.action == "open":
            manager.open(cmd)
        elif cmd.action == "delete":
            manager.delete(cmd)
        elif cmd.action == "show":
            # If no explicit "created" keyword, show base dir contents as a bonus
            if re.search(r"\b(created|بنائی|बनाई)\b", text.lower()):
                manager.show_created()
            else:
                base = manager._resolve_base_dir(cmd.base_dir_key)
                if base.exists():
                    with console.status("🔄 Processing...", spinner="dots"):
                        entries = list(base.iterdir())[:50]
                        table = Table(title=f"Listing: {base}")
                        table.add_column("Name", style="white")
                        table.add_column("Type", style="green")
                        for p in entries:
                            table.add_row(p.name, "folder" if p.is_dir() else "file")
                    console.print(table)
                else:
                    manager._fail(f"Error: Directory not found: {base}")
        else:
            manager._fail("Unsupported action.")

    if args.text:
        process_text(args.text)
        return

    language_hint = None
    if args.lang and args.lang != "auto":
        language_hint = args.lang
    listener = SpeechInput(language_hint=language_hint)
    if not listener.available:
        console.print("[bold yellow]Voice input unavailable. Use --text to pass a command.[/bold yellow]")
        return

    try:
        while True:
            text = listener.listen_once()
            process_text(text or "")
            if args.once:
                break
            console.print("[dim]Say another command or press Ctrl+C to exit.[/dim]\n")
    except KeyboardInterrupt:
        console.print("[bold cyan]\nGoodbye![/bold cyan]")


if __name__ == "__main__":
    run_cli()


