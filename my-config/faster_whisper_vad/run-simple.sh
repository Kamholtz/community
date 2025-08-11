#!/bin/bash
set -e

echo "=== Simple Run: Real-time VAD + Faster-Whisper Transcription ==="
echo "Target: RTX 3050 Ti Mobile GPU"
echo "Models will be downloaded inside container (not persistent)"
echo

# Run with minimal setup - models download inside container
docker run --rm --gpus all \
  --device /dev/snd \
  --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --network host \
  realtime-transcription:latest

echo
echo "Note: Models are downloaded inside container and not preserved"
echo "For persistent models, use the docker-compose setup"