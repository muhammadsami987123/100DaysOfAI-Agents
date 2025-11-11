
from setuptools import setup, find_packages

setup(
    name="offline-gpt-jarvis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "vosk",
        "pyttsx3",
        "tinydb",
        "gpt4all",
        "speechrecognition",
        "pyaudio"
    ],
    entry_points={
        "console_scripts": [
            "jarvis=offline_jarvis:main",
        ],
    },
)
