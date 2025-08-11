#!/bin/bash
set -e

echo "=== Fixed Run: Real-time VAD + Faster-Whisper Transcription ==="
echo "Target: RTX 3050 Ti Mobile GPU"
echo

# Set up X11 permissions for Docker
echo "Setting up X11 access for container..."
xhost +local:docker

# Check if DISPLAY is set
if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
    echo "Set DISPLAY to :0"
fi

echo "DISPLAY is set to: $DISPLAY"

# Run with proper X11 setup and English language enforcement
docker run --rm --gpus all \
  --device /dev/snd \
  --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -e XAUTHORITY=/tmp/.docker.xauth \
  -v $HOME/.Xauthority:/tmp/.docker.xauth:rw \
  --network host \
  -e MODEL_SIZE=small.en \
  realtime-transcription:latest

echo
echo "Cleaning up X11 permissions..."
xhost -local:docker

echo "Note: Used small.en model for English-only transcription"