#!/bin/bash

echo "🤖 VoiceNoteAgent - Installation Script"
echo "======================================"
echo

# Check Python installation
echo "📋 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "💡 Please install Python 3.7+ from https://python.org"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "🔧 Installing dependencies for $MACHINE..."
echo

# Install system dependencies
if [ "$MACHINE" = "Linux" ]; then
    echo "📦 Installing system dependencies (Linux)..."
    sudo apt-get update
    sudo apt-get install -y python3-pyaudio portaudio19-dev python3-dev
    sudo apt-get install -y espeak
elif [ "$MACHINE" = "Mac" ]; then
    echo "📦 Installing system dependencies (macOS)..."
    if command -v brew &> /dev/null; then
        brew install portaudio
        brew install espeak
    else
        echo "⚠️  Homebrew not found. Please install portaudio manually:"
        echo "   brew install portaudio"
        echo "   brew install espeak"
    fi
fi

echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo
echo "✅ Installation completed!"
echo
echo "🚀 To start VoiceNoteAgent, run:"
echo "   python3 main.py"
echo
echo "🧪 To run tests, use:"
echo "   python3 test_agent.py"
echo
echo "🔍 To check system, use:"
echo "   python3 config.py check"
echo 