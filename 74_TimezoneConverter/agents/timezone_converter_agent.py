import os
import json
import re
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from config import MODEL_PROVIDER, MODEL_NAME, GEMINI_API_KEY, DEFAULT_SOURCE_TIMEZONE, DEFAULT_TARGET_TIMEZONE

load_dotenv()

class TimezoneConverterAgent:
    def __init__(self):
        self.model_provider = MODEL_PROVIDER
        self.model_name = MODEL_NAME
        self.gemini_api_key = GEMINI_API_KEY
        self.system_prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'system_prompt.txt')

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        try:
            return json.loads(text)
        except Exception:
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1 and end > start:
                snippet = text[start:end+1]
                try:
                    return json.loads(snippet)
                except Exception:
                    return None
            return None

    def _llm_parse(self, prompt: str) -> Dict[str, Any]:
        try:
            with open(self.system_prompt_path, 'r', encoding='utf-8') as f:
                system_prompt = f.read()
        except Exception:
            system_prompt = "You extract time and timezones and reply only JSON."
        user_prompt = system_prompt + "\nUser query:" + prompt.strip()
        if self.model_provider == "gemini" and self.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                model = genai.GenerativeModel(self.model_name)
                resp = model.generate_content(user_prompt)
                text = (getattr(resp, 'text', None) or '').strip()
                data = self._extract_json(text)
                if data:
                    return data
                return {"error": "LLM did not return valid JSON."}
            except Exception as e:
                return {"error": f"Gemini LLM parsing failed: {e}"}
        return {"error": "Only Gemini LLM supported in this agent config."}

    def _fallback_parse(self, user_str: str) -> Dict[str, Any]:
        s = user_str.strip()
        # Try to capture patterns like: 3 PM PST to IST, 22:00 UTC to CET, 12 noon Chicago in London time
        time_patterns = [
            r"(?P<h>\d{1,2}):(?P<m>\d{2})\s*(?P<ampm>[ap]m)?",
            r"(?P<h>\d{1,2})\s*(?P<ampm>[ap]m)",
            r"(?P<noon>noon)",
        ]
        found_time = None
        for pat in time_patterns:
            m = re.search(pat, s, flags=re.IGNORECASE)
            if m:
                if m.groupdict().get('noon'):
                    found_time = "12:00 PM"
                else:
                    h = m.groupdict().get('h')
                    mnt = m.groupdict().get('m') or '00'
                    ampm = m.groupdict().get('ampm')
                    if ampm:
                        found_time = f"{int(h):d}:{int(mnt):02d} {ampm.upper()}"
                    else:
                        # assume 24h if no am/pm and hour>12 else ambiguous; default 24h
                        found_time = f"{int(h):02d}:{int(mnt):02d}"
                break
        # Source/target extraction via 'to' or 'in'
        source = None
        target = None
        # prefer "X to Y"
        m_to = re.search(r"\bto\b\s+([\w\-/ ]+)\s*$", s, flags=re.IGNORECASE)
        if m_to:
            target = m_to.group(1).strip()
            # source heuristics: words before 'to', last timezone-y token
            before_to = s[:m_to.start()].strip()
            # try 'in <place>' first
            m_in = re.search(r"\bin\b\s+([\w\-/ ]+)$", before_to, flags=re.IGNORECASE)
            if m_in:
                source = m_in.group(1).strip()
            else:
                # fallback: last word-like segment
                toks = re.split(r"\s+", before_to)
                if len(toks) >= 1:
                    source = toks[-1]
        else:
            # pattern: "time in X in Y" or "time in X, Y"
            m_in_all = re.findall(r"\bin\b\s+([\w\-/ ]+)", s, flags=re.IGNORECASE)
            if len(m_in_all) >= 2:
                source, target = m_in_all[-2].strip(), m_in_all[-1].strip()
            elif len(m_in_all) == 1:
                source = m_in_all[0].strip()
        return {
            "input_time": found_time,
            "input_date": None,
            "source_timezone": source,
            "target_timezone": target,
            "note": "fallback"
        }

    def parse_user_input(self, user_str: str) -> Dict[str, Any]:
        parsed = self._llm_parse(user_str)
        if 'error' in parsed:
            # fallback to heuristic parser
            h = self._fallback_parse(user_str)
            if not h.get('input_time'):
                raise ValueError(parsed['error'])
            return h
        return parsed

    def perform_timezone_conversion(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        from utils.timezone_utils import resolve_timezone_name, get_timezone_info
        from datetime import datetime
        import pytz
        
        input_time = parsed.get("input_time")
        input_date = parsed.get("input_date")
        source_tz = resolve_timezone_name(parsed.get("source_timezone") or DEFAULT_SOURCE_TIMEZONE)
        target_tz = resolve_timezone_name(parsed.get("target_timezone") or DEFAULT_TARGET_TIMEZONE)
        if not input_time or not source_tz or not target_tz:
            return {"error": "Time or timezone not specified clearly. Please include a time and valid locations."}
        if not input_date:
            dt = datetime.now()
            input_date = dt.strftime("%Y-%m-%d")
        dt_str = f"{input_date} {input_time}"
        try:
            naive_dt = None
            for fmt in ("%Y-%m-%d %I:%M %p", "%Y-%m-%d %H:%M", "%Y-%m-%d %I %p", "%Y-%m-%d %H"):
                try:
                    naive_dt = datetime.strptime(dt_str, fmt)
                    break
                except Exception:
                    continue
            if naive_dt is None:
                raise Exception("Could not parse date/time.")
            src_tz_obj = pytz.timezone(source_tz)
            tgt_tz_obj = pytz.timezone(target_tz)
            src_dt = src_tz_obj.localize(naive_dt, is_dst=None)
            tgt_dt = src_dt.astimezone(tgt_tz_obj)
            out = {
                "converted_time": tgt_dt.strftime("%I:%M %p"),
                "converted_date": tgt_dt.strftime("%Y-%m-%d"),
                "converted_day_diff": (tgt_dt.date() - src_dt.date()).days,
                "source_info": get_timezone_info(source_tz),
                "target_info": get_timezone_info(target_tz),
                "input":{"dt":dt_str, "tz":source_tz},
                "raw":parsed
            }
            return out
        except Exception as e:
            return {"error": str(e)}

    def format_output(self, conversion_result: Dict[str, Any]) -> str:
        if 'error' in conversion_result:
            return f"❗ {conversion_result['error']}\nTry format: 'Convert 3 PM PST to IST'"
        time = conversion_result["converted_time"]
        date = conversion_result["converted_date"]
        day_diff = conversion_result["converted_day_diff"]
        src = conversion_result["source_info"]
        tgt = conversion_result["target_info"]
        lines = []
        if day_diff == 0:
            day_note = ""
        elif day_diff == 1:
            day_note = " (Next Day)"
        elif day_diff == -1:
            day_note = " (Previous Day)"
        else:
            day_note = f" ({'+' if day_diff>0 else ''}{day_diff} days)"
        lines.append(f"🕒 {time}{day_note} — {tgt.get('zone','?')} ({tgt.get('long_name','?')})")
        lines.append(f"🗓 Date: {date}")
        lines.append(f"🧭 Source Timezone: {src.get('long_name','?')}")
        lines.append(f"🌍 Target Timezone: {tgt.get('long_name','?')}")
        return '\n'.join(lines)

    def handle_error(self, error: Exception) -> str:
        return f"Sorry, I couldn't process your request. Error: {error}"

    def log_conversion(self, user_input: str, result: dict):
        import json, datetime
        filepath = os.path.join(os.path.dirname(__file__), '..', 'log.txt')
        try:
            with open(filepath, 'a', encoding='utf-8') as logf:
                now = datetime.datetime.now().isoformat()
                logf.write(f"{now} | {user_input} | {json.dumps(result, ensure_ascii=False)}\n")
        except Exception:
            pass
