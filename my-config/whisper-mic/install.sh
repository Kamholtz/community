#!/bin/bash

echo "Setting up whisper-mic for live transcription..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Install requirements
echo "Installing dependencies..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Install whisper-mic package
echo "Installing whisper-mic package..."
./venv/bin/pip install -e ../whisper-mic-repo/

echo "Installation complete!"
echo "Run ./run_whisper_mic.sh to start live transcription"