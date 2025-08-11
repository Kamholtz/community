#!/bin/bash
set -e

echo "=== Real-time VAD + Faster-Whisper Transcription ==="
echo "Target: RTX 3050 Ti Mobile GPU"
echo

# Set current user ID for proper file permissions
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

echo "Running as user: $USER_ID:$GROUP_ID"

# Ensure models directory exists and is writable
mkdir -p models config
chmod 755 models config 2>/dev/null || echo "Note: Could not change permissions for models/config directories"

# Check X11 forwarding setup
if [ -z "$DISPLAY" ]; then
    echo "⚠️  Warning: DISPLAY not set, X11 forwarding may not work for typing"
    echo "   Set DISPLAY=:0 or run 'export DISPLAY=:0'"
fi

# Check if PulseAudio is running
if ! pgrep -x pulseaudio >/dev/null; then
    echo "⚠️  Warning: PulseAudio not running, audio may not work"
    echo "   Start PulseAudio with: pulseaudio --start"
fi

# Run the container with proper permissions and GPU access
echo "Starting real-time transcription container..."
docker compose up --build