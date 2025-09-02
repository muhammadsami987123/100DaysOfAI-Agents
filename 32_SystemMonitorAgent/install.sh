#!/bin/bash

echo "Installing SystemMonitorAgent..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    echo "Please install pip3 and try again"
    exit 1
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo
echo "Installation completed successfully!"
echo
echo "Usage examples:"
echo "  python3 main.py                    # Monitor with default 5s interval"
echo "  python3 main.py -i 2              # Monitor with 2s interval"
echo "  python3 main.py --export json     # Export current stats"
echo "  python3 main.py --suggest         # Get AI optimization suggestions"
echo "  python3 main.py --health          # Get AI health assessment"
echo
echo "For AI features, set OPENAI_API_KEY environment variable:"
echo "  export OPENAI_API_KEY='your-api-key-here'"
echo
