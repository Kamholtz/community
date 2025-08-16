#!/bin/bash

# Docker run script for whisper-mic
# Based on faster_whisper_vad setup for microphone access

echo "Starting whisper-mic in Docker container..."

# Get current user ID and group ID for proper permissions
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

# Set default environment variables  
export MODEL_SIZE=${MODEL_SIZE:-small}
export DEVICE=${DEVICE:-auto}
export ENGLISH_ONLY=${ENGLISH_ONLY:-true}
export USE_FASTER=${USE_FASTER:-true}
export ENERGY_THRESHOLD=${ENERGY_THRESHOLD:-400}
export PAUSE_THRESHOLD=${PAUSE_THRESHOLD:-1.2}

# Build and run the container
docker compose up --build whisper-mic