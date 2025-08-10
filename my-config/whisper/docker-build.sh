#!/bin/bash
set -euo pipefail

echo "Building WhisperX Docker Images"
echo "==============================="

# Function to check if Docker is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed or not in PATH"
        echo "Please install Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo "❌ Docker daemon is not running"
        echo "Please start Docker daemon"
        exit 1
    fi
}

# Function to check for NVIDIA Docker support  
check_nvidia_docker() {
    if command -v nvidia-smi &> /dev/null; then
        echo "✅ NVIDIA GPU detected"
        if command -v nvidia-docker &> /dev/null || docker info 2>/dev/null | grep -q nvidia; then
            echo "✅ NVIDIA Docker runtime available"
            return 0
        else
            echo "⚠️  NVIDIA Docker runtime not available"
            echo "   Containers will use CPU-only PyTorch"
            return 1
        fi
    else
        echo "⚠️  No NVIDIA GPU detected, building CPU-only versions"
        return 1
    fi
}

# Function to build images
build_image() {
    local dockerfile=$1
    local tag=$2
    local description=$3
    
    echo ""
    echo "Building $description..."
    echo "Dockerfile: $dockerfile"
    echo "Tag: $tag"
    
    if docker build -f "$dockerfile" -t "$tag" .; then
        echo "✅ Successfully built $tag"
    else
        echo "❌ Failed to build $tag"
        exit 1
    fi
}

# Main execution
echo "Checking prerequisites..."
check_docker

# Check for NVIDIA support
if check_nvidia_docker; then
    GPU_SUPPORT=true
else
    GPU_SUPPORT=false
fi

echo ""
echo "Building Docker images..."

# Build faster-whisper image
build_image "Dockerfile.faster-whisper" "whisper-dictate:faster-whisper" "Faster-whisper backend"

# Build WhisperX image  
build_image "Dockerfile.whisperx" "whisper-dictate:whisperx" "WhisperX backend"

echo ""
echo "🎉 Build completed successfully!"
echo ""
echo "Available images:"
echo "  - whisper-dictate:faster-whisper (lightweight, fast)"
echo "  - whisper-dictate:whisperx (best accuracy, word alignment)"
echo ""
echo "Usage:"
echo "  ./docker-run.sh faster-whisper"
echo "  ./docker-run.sh whisperx"
echo "  docker-compose --profile faster-whisper up"
echo "  docker-compose --profile whisperx up"

if [ "$GPU_SUPPORT" = false ]; then
    echo ""
    echo "⚠️  Note: Images built without GPU support"
    echo "   For GPU acceleration, install NVIDIA Docker support"
fi