#!/bin/bash

# Get script directory
SCRIPT_DIR="$(dirname "$0")"

# Check if wrapper exists and use it, otherwise fall back to original
if [[ -f "$SCRIPT_DIR/whisper_mic_wrapper.py" ]]; then
    echo "Using enhanced wrapper with timestamps and microphone detection..."
    # Run enhanced wrapper with timestamps and microphone detection
    "$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/whisper_mic_wrapper.py" --loop --dictate --faster --model tiny --english
else
    echo "Using original whisper_mic CLI..."
    # Run whisper_mic using venv python directly
    # The --faster flag enables faster_whisper implementation
    # The --model tiny flag uses the smallest model for fastest startup
    "$SCRIPT_DIR/venv/bin/python" -m whisper_mic.cli --loop --dictate --faster --model tiny --english
fi
