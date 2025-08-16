#!/bin/bash

# Get script directory
SCRIPT_DIR="$(dirname "$0")"

# Run whisper_mic using venv python directly
# The --faster flag enables faster_whisper implementation
# The --model tiny flag uses the smallest model for fastest startup
"$SCRIPT_DIR/venv/bin/python" -m whisper_mic.cli --loop --dictate --faster --model tiny --englishj
