# Optimized PyTorch image for RTX 3050 Ti Mobile with pre-installed ML dependencies
FROM nvcr.io/nvidia/pytorch:25.06-py3

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PULSE_RUNTIME_PATH=/run/user/1000/pulse

# Test PyTorch CUDA setup (nvidia-smi only available at runtime with --gpus)
RUN echo "Testing PyTorch CUDA compatibility for RTX 3050 Ti Mobile..." && \
    python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA build available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print('GPU detection will be tested at runtime with --gpus flag')" && \
    echo "PyTorch CUDA build test passed!"

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

# Install whisper-mic dependencies (PyTorch already included)
RUN pip install \
    sounddevice \
    pyaudio \
    faster-whisper \
    speechrecognition \
    pynput \
    click \
    attrs \
    more-itertools \
    transformers \
    ffmpeg-python \
    pydub \
    rich \
    pydantic \
    importlib-metadata \
    openai-whisper

# Create app directory
WORKDIR /app

# Create directories for models and config
RUN mkdir -p /app/models /app/config

# Copy whisper-mic repository
COPY whisper-mic-repo/ /app/whisper-mic-repo/

# Install whisper-mic package
RUN pip install -e /app/whisper-mic-repo/

# Copy run script, enhanced wrapper, and debug tools
COPY whisper-mic/run_whisper_mic.sh /app/
COPY whisper-mic/whisper_mic_wrapper.py /app/
COPY whisper-mic/debug_performance.py /app/

# Make scripts executable
RUN chmod +x /app/*.sh /app/*.py

# Create user for running the application (NGC image may have existing UID 1000)
RUN groupadd -f audio || true
RUN id -u transcriber >/dev/null 2>&1 || useradd -m -u 1001 transcriber
RUN usermod -aG audio transcriber 2>/dev/null || true

# Set ownership
RUN chown -R transcriber /app 2>/dev/null || chown -R 1001 /app

# Switch to non-root user
USER transcriber

# Set environment variables for whisper-mic (optimized for responsiveness)
ENV MODEL_SIZE=tiny
ENV DEVICE=auto
ENV ENGLISH_ONLY=true
ENV USE_FASTER=true
ENV ENERGY_THRESHOLD=300
ENV PAUSE_THRESHOLD=0.8
ENV PHRASE_TIME_LIMIT=2

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python3 -c "import torch; print('GPU available:', torch.cuda.is_available())" || exit 1

# Default command with optimized settings for fast, responsive transcription using enhanced wrapper
CMD ["python3", "/app/whisper_mic_wrapper.py", "--loop", "--dictate", "--faster", "--model", "tiny", "--english", "--energy", "300", "--pause", "0.8", "--dynamic_energy", "--hallucinate_threshold", "400"]