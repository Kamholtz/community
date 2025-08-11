# Optimized PyTorch image for RTX 3050 Ti Mobile with pre-installed ML dependencies
FROM nvcr.io/nvidia/pytorch:25.06-py3

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PULSE_RUNTIME_PATH=/run/user/1000/pulse

# Test GPU compatibility early in build process
RUN echo "Testing GPU compatibility for RTX 3050 Ti Mobile..." && \
    nvidia-smi && \
    python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'GPU device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')" && \
    echo "GPU compatibility test passed!"

# Install system dependencies (Python/PyTorch already included in base image)
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    pulseaudio \
    pulseaudio-utils \
    xdotool \
    xclip \
    wtype \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install only the additional transcription dependencies (PyTorch already included)
RUN pip install \
    sounddevice \
    webrtcvad \
    faster-whisper \
    keyboard \
    pyyaml

# Create app directory
WORKDIR /app

# Create directories for models and config
RUN mkdir -p /app/models /app/config

# Copy application files
COPY faster_whisper_vad.py /app/
COPY install.sh /app/

# Create enhanced version with config support
COPY realtime_transcription.py /app/
COPY config.yaml /app/config/

# Make scripts executable
RUN chmod +x /app/*.py /app/install.sh

# Create user for running the application
RUN useradd -m -u 1000 -g audio transcriber
RUN usermod -aG audio,pulse-access transcriber

# Set ownership
RUN chown -R transcriber:audio /app

# Switch to non-root user
USER transcriber

# Set environment variables for the application
ENV MODEL_SIZE=small
ENV DEVICE=auto
ENV VAD_AGGRESSIVENESS=2
ENV PARTIAL_INTERVAL=0.9
ENV START_GATE_MS=200
ENV END_GATE_MS=400
ENV PAD_MS=250

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python3 -c "import torch; print('GPU available:', torch.cuda.is_available())" || exit 1

# Default command
CMD ["python3", "realtime_transcription.py"]