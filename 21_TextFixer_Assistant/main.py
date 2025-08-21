from __future__ import annotations

import sys
from typing import Optional

from config import CONFIG
from correction_service import get_correction_provider
from hotkey_listener import TextFixerHotkey


_PROVIDER = None


def correct_text(text: str) -> str:
    global _PROVIDER
    if _PROVIDER is None:
        _PROVIDER = get_correction_provider()
    return _PROVIDER.correct(text, language=CONFIG.language, style=CONFIG.style)


def main(argv: Optional[list[str]] = None) -> int:
    fixer = TextFixerHotkey(on_text=correct_text)
    fixer.start()
    try:
        fixer.join()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


