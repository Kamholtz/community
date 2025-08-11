#!/bin/bash
set -e

echo "=== Direct Run: Real-time VAD + Faster-Whisper Transcription ==="
echo "Target: RTX 3050 Ti Mobile GPU"
echo

# Create models directory if it doesn't exist
mkdir -p models

# Run directly as current user with all necessary flags
docker run --rm --gpus all \
  --device /dev/snd \
  --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
  -e DISPLAY=$DISPLAY \
  -e PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v /run/user/$(id -u)/pulse:/run/user/$(id -u)/pulse:ro \
  -v $(pwd)/models:/home/transcriber/models \
  -e HF_HOME=/home/transcriber/models \
  --user $(id -u):$(id -g) \
  --network host \
  --workdir /home/transcriber \
  realtime-transcription:latest \
  python /app/realtime_transcription.py

echo
echo "To stop: Press Ctrl+C"