import os
import sys
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any

# Support package and script modes
try:
    from .gpt_parser import parse_query, brief_insight
    from .converter import convert
    from .currency_data import CURRENCIES
except Exception:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gpt_parser import parse_query, brief_insight  # type: ignore
    from converter import convert  # type: ignore
    from currency_data import CURRENCIES  # type: ignore


@dataclass
class OpenAIAgent:
    """Agent that uses OpenAI for NL parsing and optional insights."""

    def parse(self, text: str) -> Optional[Tuple[float, str, str]]:
        return parse_query(text)

    def insight(self, base: str, target: str) -> Optional[str]:
        return brief_insight(base, target)


@dataclass
class ExchangeRateHostAgent:
    """Agent encapsulating exchangerate.host conversions with cache fallback."""

    def convert(self, amount: float, from_code: str, to_code: str) -> Tuple[Optional[float], Optional[float], Dict[str, Any]]:
        return convert(amount, from_code, to_code)


@dataclass
class CurrencyResolverAgent:
    """Resolves informal names/countries to ISO currency codes.

    Strategy:
    1) Local dataset fuzzy-ish match (lowercase contains match)
    2) Fallback to OpenAI to propose a 3-letter code if enabled
    """

    def resolve(self, text: str) -> Optional[str]:
        t = text.strip().lower()
        t_clean = t.replace(".", "").strip()
        known_codes = {c["code"].lower() for c in CURRENCIES}

        # Prefer local dataset resolution first (names, countries, exact code present in dataset)
        for item in CURRENCIES:
            code = item["code"].upper()
            code_l = code.lower()
            names = [n.lower() for n in item.get("names", [])]
            countries = [c.lower() for c in item.get("country", [])]
            if (
                t == code_l or t_clean == code_l or
                any(t in n or t_clean in n for n in names) or
                any(t in c or t_clean in c for c in countries)
            ):
                return code

        # If 3 letters and actually a known ISO code from dataset, accept
        if len(t_clean) == 3 and t_clean.isalpha() and t_clean in known_codes:
            return t_clean.upper()

        # OpenAI fallback via parser: ask it for to_currency in a dummy prompt
        parsed = parse_query(f"Convert 1 XXX to {text}")
        if parsed:
            _, _, to_code = parsed
            return to_code
        return None


