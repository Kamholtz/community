#!/bin/bash

# Optimized settings to reduce over-punctuation and word cutting

echo "Starting whisper-mic with OPTIMIZED settings (reduced punctuation, better word capture)..."

# Get current user ID and group ID for proper permissions
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

# Optimized settings for cleaner transcription
export MODEL_SIZE=base  # Better accuracy than small
export DEVICE=${DEVICE:-auto}
export ENGLISH_ONLY=${ENGLISH_ONLY:-true}
export USE_FASTER=${USE_FASTER:-true}

# Aggressive settings to capture complete phrases
export ENERGY_THRESHOLD=500        # Higher = waits for clearer speech
export PAUSE_THRESHOLD=1.5         # Longer = captures complete thoughts
export PHRASE_TIME_LIMIT=10        # Max 10 seconds per phrase
export HALLUCINATE_THRESHOLD=600   # Reduces false detections

echo "Settings: base model, energy=500, pause=1.5s, phrase_limit=10s"
echo "These settings prioritize complete phrases over quick response"

# Build and run with optimized command
docker compose down 2>/dev/null
docker compose up --build whisper-mic