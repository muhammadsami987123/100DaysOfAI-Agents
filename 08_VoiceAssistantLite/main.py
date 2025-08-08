from __future__ import annotations

from cli import VoiceAssistantCLI


def main() -> None:
    app = VoiceAssistantCLI()
    app.loop()


if __name__ == "__main__":
    main()


