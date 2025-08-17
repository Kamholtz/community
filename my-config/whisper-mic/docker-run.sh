#!/bin/bash

# Docker run script for whisper-mic
# Based on faster_whisper_vad setup for microphone access

echo "Starting whisper-mic in Docker container..."

# Get current user ID and group ID for proper permissions
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

# Set default environment variables (optimized for fast, responsive transcription)
export MODEL_SIZE=${MODEL_SIZE:-tiny}
export DEVICE=${DEVICE:-auto}
export ENGLISH_ONLY=${ENGLISH_ONLY:-true}
export USE_FASTER=${USE_FASTER:-true}
export ENERGY_THRESHOLD=${ENERGY_THRESHOLD:-300}
export PAUSE_THRESHOLD=${PAUSE_THRESHOLD:-0.8}

# Build and run the container
docker compose up --build whisper-mic