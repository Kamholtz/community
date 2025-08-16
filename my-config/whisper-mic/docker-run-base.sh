#!/bin/bash

# Docker run script with base model for better accuracy

echo "Starting whisper-mic with BASE model (better accuracy)..."

# Get current user ID and group ID for proper permissions
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

# Use base model for better accuracy
export MODEL_SIZE=base
export DEVICE=${DEVICE:-auto}
export ENGLISH_ONLY=${ENGLISH_ONLY:-true}
export USE_FASTER=${USE_FASTER:-true}
export ENERGY_THRESHOLD=${ENERGY_THRESHOLD:-400}
export PAUSE_THRESHOLD=${PAUSE_THRESHOLD:-1.2}

# Build and run the container
docker compose up --build whisper-mic