#!/bin/bash
set -euo pipefail

# Configuration
BACKEND=${1:-"faster-whisper"}
MODEL=${2:-"small.en"}

echo "Starting WhisperX Docker Container"
echo "=================================="
echo "Backend: $BACKEND"
echo "Model: $MODEL"

# Function to check prerequisites
check_prerequisites() {
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed"
        exit 1
    fi
    
    # Check X11 forwarding setup (Linux)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -z "${DISPLAY:-}" ]; then
            echo "❌ DISPLAY variable not set"
            echo "Run: export DISPLAY=:0"
            exit 1
        fi
        
        # Allow X11 connections (temporary)
        xhost +local:docker 2>/dev/null || echo "⚠️  xhost not available, X11 forwarding may not work"
    fi
}

# Function to detect GPU support
check_gpu_support() {
    if command -v nvidia-smi &> /dev/null && docker run --rm --gpus all nvidia/cuda:11.8-runtime-ubuntu22.04 nvidia-smi &> /dev/null 2>&1; then
        echo "✅ GPU support detected"
        return 0
    else
        echo "⚠️  No GPU support, running on CPU"
        return 1
    fi
}

# Function to run container
run_container() {
    local backend=$1
    local model=$2
    local gpu_args=""
    
    # Set GPU arguments if available
    if check_gpu_support; then
        gpu_args="--gpus all"
    fi
    
    # Determine image tag
    local image_tag="whisper-dictate:$backend"
    
    # Check if image exists
    if ! docker image inspect "$image_tag" &> /dev/null; then
        echo "❌ Image $image_tag not found"
        echo "Run: ./docker-build.sh"
        exit 1
    fi
    
    echo "Starting container..."
    
    # Platform-specific volume mounts
    local volume_args=""
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        volume_args="-v /tmp/.X11-unix:/tmp/.X11-unix:rw"
        volume_args="$volume_args -v ${XDG_RUNTIME_DIR}/pulse:${XDG_RUNTIME_DIR}/pulse:rw"
        volume_args="$volume_args --device /dev/snd:/dev/snd"
    fi
    
    # Environment variables
    local env_args="-e DISPLAY=${DISPLAY:-:0}"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        env_args="$env_args -e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native"
    fi
    
    # Run the container
    docker run \
        --rm \
        -it \
        $gpu_args \
        $volume_args \
        $env_args \
        --network host \
        --name "whisper-$backend-$$" \
        "$image_tag" \
        python3 "dictate_$backend.py" --model "$model"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [BACKEND] [MODEL]"
    echo ""
    echo "BACKEND options:"
    echo "  faster-whisper  Lightweight, fast (default)"
    echo "  whisperx        Best accuracy, word alignment"
    echo ""
    echo "MODEL options:"
    echo "  tiny.en         Fastest, basic accuracy"
    echo "  small.en        Good balance (default)"
    echo "  base.en         Better accuracy"
    echo "  medium.en       High accuracy"
    echo "  large-v3        Best accuracy"
    echo ""
    echo "Examples:"
    echo "  $0                              # Run faster-whisper with small.en"
    echo "  $0 whisperx                     # Run WhisperX with small.en"
    echo "  $0 faster-whisper medium.en     # Run faster-whisper with medium.en"
    echo "  $0 whisperx large-v3            # Run WhisperX with large-v3"
}

# Handle help flag
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    show_usage
    exit 0
fi

# Validate backend
if [[ "$BACKEND" != "faster-whisper" ]] && [[ "$BACKEND" != "whisperx" ]]; then
    echo "❌ Invalid backend: $BACKEND"
    echo ""
    show_usage
    exit 1
fi

# Main execution
check_prerequisites
run_container "$BACKEND" "$MODEL"