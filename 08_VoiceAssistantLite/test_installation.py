def test_imports():
    import importlib

    modules = [
        "config",
        "stt_service",
        "tts_service",
        "faq_matcher",
        "logger",
        "cli",
        "main",
    ]
    for m in modules:
        importlib.import_module(m)

    # External deps
    import speech_recognition  # noqa: F401
    import pyttsx3  # noqa: F401
    import rapidfuzz  # noqa: F401


