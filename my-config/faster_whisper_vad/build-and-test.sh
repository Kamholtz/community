#!/bin/bash
set -e

echo "=== Building and Testing Real-time Transcription Container ==="
echo "Target: RTX 3050 Ti Mobile GPU"
echo

# Check if nvidia-docker is available
if ! docker info | grep -i nvidia > /dev/null 2>&1; then
    echo "⚠️  Warning: NVIDIA Docker runtime not detected"
    echo "   Make sure nvidia-docker2 is installed and Docker daemon is configured"
fi

# Check host GPU
echo "1. Host GPU Check:"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits
    echo
else
    echo "❌ nvidia-smi not found on host"
    exit 1
fi

# Build the container
echo "2. Building Container:"
echo "   Using NGC PyTorch image optimized for RTX 30-series..."
docker build -t realtime-transcription:latest .

if [ $? -eq 0 ]; then
    echo "✅ Container build successful"
else
    echo "❌ Container build failed"
    exit 1
fi

echo

# Test GPU compatibility inside container
echo "3. Testing GPU Compatibility in Container:"
docker run --rm --gpus all \
    -v $(pwd):/app/src \
    realtime-transcription:latest \
    python /app/src/test-gpu.py

if [ $? -eq 0 ]; then
    echo
    echo "🎉 Build and GPU compatibility test completed successfully!"
    echo
    echo "Next steps:"
    echo "   1. Run: docker-compose up"
    echo "   2. Or: docker run --rm --gpus all --device /dev/snd \\"
    echo "          -e DISPLAY=\$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \\"
    echo "          realtime-transcription:latest"
else
    echo
    echo "❌ GPU compatibility test failed in container"
    echo "Check the error messages above for troubleshooting"
    exit 1
fi