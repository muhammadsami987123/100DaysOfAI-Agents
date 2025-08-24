"""
Setup script for MoodMusicAgent
"""
from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "MoodMusicAgent - Emotion-Based Music Player"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="mood-music-agent",
    version="1.0.0",
    author="100 Days of AI Agents",
    author_email="",
    description="An intelligent agent that plays music based on the user's current mood or emotion",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/100DaysOfAI-Agents",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "voice": [
            "speech_recognition>=3.10.0",
            "pyttsx3>=2.90",
            "pyaudio>=0.2.11",
        ],
        "spotify": [
            "spotipy>=2.23.0",
        ],
        "youtube": [
            "youtube_search_python>=1.6.6",
            "pafy>=0.5.5",
            "yt_dlp>=2023.12.30",
        ],
    },
    entry_points={
        "console_scripts": [
            "moodmusicagent=main:main",
            "moodmusic-demo=demo:run_full_demo",
            "moodmusic-test=test_installation:run_all_tests",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.bat", "*.sh"],
    },
    keywords=[
        "music",
        "mood",
        "emotion",
        "ai",
        "agent",
        "music-player",
        "voice-interface",
        "sentiment-analysis",
        "spotify",
        "youtube",
        "local-music",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/100DaysOfAI-Agents/issues",
        "Source": "https://github.com/yourusername/100DaysOfAI-Agents",
        "Documentation": "https://github.com/yourusername/100DaysOfAI-Agents/blob/main/24_MoodMusicAgent/README.md",
    },
)
