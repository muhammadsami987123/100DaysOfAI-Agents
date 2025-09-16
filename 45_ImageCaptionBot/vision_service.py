from __future__ import annotations

import base64
from typing import Literal, Optional, Dict, Any, List

from openai import OpenAI


LanguageCode = Literal["en", "ur", "hi"]
StyleCode = Literal["descriptive", "creative", "alt"]
LengthCode = Literal["short", "medium", "long"]


class VisionCaptioner:
    def __init__(self, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def _build_system_prompt(self, language: LanguageCode, style: StyleCode, length: LengthCode, hashtags: bool) -> str:
        base = (
            "You are an expert image captioning assistant. Respond with a single, concise caption. "
            "Be accurate and context-aware. Avoid speculation."
        )
        if style == "alt":
            base += " Write it as high-quality accessibility alt-text, neutral and descriptive."
        elif style == "creative":
            base += " Make it short, catchy, and social-media friendly."
        else:
            base += " Keep it clear, vivid, and factual."

        if length == "short":
            base += " Aim for 4–12 words."
        elif length == "medium":
            base += " Aim for a single sentence, up to 18 words."
        else:
            base += " Aim for up to two concise sentences."

        if hashtags:
            base += " Optionally append 1–3 relevant hashtags at the end."

        if language == "ur":
            base += " Respond in Urdu."
        elif language == "hi":
            base += " Respond in Hindi."
        else:
            base += " Respond in English."
        return base

    def generate_caption(
        self,
        image_bytes: bytes,
        mime_type: str,
        language: LanguageCode = "en",
        style: StyleCode = "descriptive",
        length: LengthCode = "short",
        hashtags: bool = False,
    ) -> str:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        sys_prompt = self._build_system_prompt(language, style, length, hashtags)

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": sys_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Caption this image."},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64}"}},
                    ],
                },
            ],
            max_tokens=120,
            temperature=0.7 if style == "creative" else 0.3,
        )

        caption: Optional[str] = resp.choices[0].message.content if resp and resp.choices else None
        return (caption or "").strip()

    def generate_platform_captions(
        self,
        image_bytes: bytes,
        mime_type: str,
        language: LanguageCode,
        tone: Literal["professional", "funny", "emotional"],
        variations: int = 10,
        temperature: float = 0.9,
    ) -> Dict[str, List[str]]:
        b64 = base64.b64encode(image_bytes).decode("utf-8")

        system = (
            "You are a senior social media strategist and captioning expert. "
            "Given an image, generate platform-tailored, concise, context-aware captions. "
            "Respect platform tone expectations. Avoid generic filler. Vary structure and vocabulary."
        )

        lang_line = " Respond in English."
        if language == "ur":
            lang_line = " Respond in Urdu."
        elif language == "hi":
            lang_line = " Respond in Hindi."

        tone_map = {
            "professional": "Maintain a professional, clear, confident tone.",
            "funny": "Use light humor, wordplay, or witty phrasing (keep tasteful).",
            "emotional": "Evoke feeling with warm, human language; avoid melodrama.",
        }

        platform_instructions = (
            "Return JSON ONLY with keys: instagram, twitter, facebook, linkedin, tiktok. "
            f"Each key maps to an array of {variations} JSON objects. Each object must contain 'caption' (string) and 'hashtags' (array of strings, e.g., ['#tag1', '#tag2']). "
            "Generate captions with diverse phrasing and content. The captions should be unique and tailored for each platform. Critically, ensure **no duplication of text or ideas** across platforms or within variations for the same platform.\n"
            "Instagram: trendy, playful, visual. Length: 50-100 words. Include 5-10 relevant hashtags. Call to action: encourage likes, shares, or saves.\n"
            "Twitter: short, sharp, conversational. Length: <280 characters. Include 2-4 relevant hashtags. Call to action: retweet, reply, or click.\n"
            "Facebook: warm, community-oriented. Length: 100-150 words. Include 3-5 relevant hashtags. Encourage comments and engagement.\n"
            "LinkedIn: professional, insightful, educational. Length: 120-180 words. Limit hashtags to 2-3. Focus on expertise and networking.\n"
            "TikTok: very short, fun, energetic, trending. Length: 20-50 words. Use 5-8 popular trending hashtags."
        )

        messages = [
            {"role": "system", "content": system + lang_line + " " + tone_map[tone]},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": platform_instructions},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64}"}},
                ],
            },
        ]

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            max_tokens=800,
            temperature=min(1.5, temperature * 1.2), # Slightly increase temperature for more creativity
            presence_penalty=1.0, # Increase to discourage repeating topics
            frequency_penalty=0.7, # Increase to discourage repeating words/phrases
        )

        content = resp.choices[0].message.content if resp and resp.choices else "{}"
        try:
            import json

            data: Dict[str, Any] = json.loads(content or "{}")
        except Exception:
            data = {}

        def pick_structured_captions(data_obj: Dict[str, Any], keys: List[str]) -> List[Dict[str, Any]]:
            for k in keys:
                if k in data_obj and isinstance(data_obj[k], list):
                    return [
                        {"caption": str(item.get("caption", "")).strip(), "hashtags": [str(h).strip() for h in item.get("hashtags", []) if str(h).strip()]}
                        for item in data_obj[k] if isinstance(item, dict) and item.get("caption")
                    ]
                lk = k.lower()
                for candidate in list(data_obj.keys()):
                    if candidate.lower() == lk and isinstance(data_obj[candidate], list):
                        return [
                            {"caption": str(item.get("caption", "")).strip(), "hashtags": [str(h).strip() for h in item.get("hashtags", []) if str(h).strip()]}
                            for item in data_obj[candidate] if isinstance(item, dict) and item.get("caption")
                        ]
            return []

        out: Dict[str, List[Dict[str, Any]]] = {
            "instagram": pick_structured_captions(data, ["instagram", "ig"])[: variations],
            "linkedin": pick_structured_captions(data, ["linkedin", "li"])[: variations],
            "facebook": pick_structured_captions(data, ["facebook", "fb"])[: variations],
            "twitter": pick_structured_captions(data, ["twitter", "x", "x_twitter"])[: variations],
            "whatsapp": pick_structured_captions(data, ["whatsapp", "wa", "whats_app"])[: variations],
            "tiktok": pick_structured_captions(data, ["tiktok", "tt"])[: variations],
        }

        # if nothing parsed but there are values, distribute round-robin
        all_values: List[str] = []
        if isinstance(data, dict):
            for v in data.values():
                if isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict) and "caption" in item and item["caption"]:
                            all_values.append({"caption": item["caption"], "hashtags": [str(h).strip() for h in item.get("hashtags", []) if str(h).strip()]})
                elif isinstance(v, str) and v.strip():
                    all_values.append({"caption": v.strip(), "hashtags": []})
                elif isinstance(v, dict) and "caption" in v and v["caption"].strip():
                    all_values.append({"caption": v["caption"].strip(), "hashtags": [str(h).strip() for h in v.get("hashtags", []) if str(h).strip()]})
        if all(len(v) == 0 for v in out.values()) and all_values:
            platforms = ["instagram", "linkedin", "facebook", "twitter", "whatsapp", "tiktok"]
            for i, cap_obj in enumerate(all_values[: variations * len(platforms)]):
                p = platforms[i % len(platforms)]
                out[p].append(cap_obj) # cap_obj is already a dict with caption and hashtags
                out[p] = out[p][: variations]

        # Absolute fallback: if still empty, generate a single generic caption
        if sum(len(v) for v in out.values()) == 0:
            try:
                generic = self.generate_caption(
                    image_bytes,
                    mime_type,
                    language=language,
                    style="creative",  # more engaging
                    length="short",
                    hashtags=False,
                )
            except Exception:
                generic = ""
            if generic:
                for key in out.keys():
                    out[key] = [{"caption": generic, "hashtags": []}]
        return out


