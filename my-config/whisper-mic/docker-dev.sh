#!/bin/bash

# Docker development shell script for whisper-mic
# Based on faster_whisper_vad setup for microphone access

echo "Starting whisper-mic development container with shell access..."

# Get current user ID and group ID for proper permissions
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

# Run the development container with shell access
docker compose --profile dev run --rm whisper-mic-dev