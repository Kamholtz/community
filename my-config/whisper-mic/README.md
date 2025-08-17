# Whisper-Mic Live Transcription Setup

This repository contains a setup for using [whisper-mic](https://github.com/mallorbc/whisper_mic) for live speech transcription that types directly into your focused application.

## Quick Setup

### Option 1: Docker (Recommended)

1. **Run with Docker:**
   ```bash
   ./docker-run.sh
   ```

2. **Development mode with shell access:**
   ```bash
   ./docker-dev.sh
   ```

### Option 2: Local Installation

1. **Install dependencies:**
   ```bash
   ./install.sh
   ```

2. **Run live transcription:**
   ```bash
   ./run_whisper_mic.sh
   ```

## What It Does

- Listens continuously to your microphone (tested with Anker work microphone)
- Uses faster-whisper for efficient GPU-accelerated transcription on RTX 3050 mobile
- Types transcribed speech directly into your currently focused application
- Uses the tiny model for fastest startup and response times
- **NEW**: Shows timestamps for transcription timing analysis
- **NEW**: Displays detected microphones and which one is being used

## Manual Installation

If the install script doesn't work, you can install manually:

```bash
# Create virtual environment
python3 -m venv venv

# Install dependencies
./venv/bin/pip install -r requirements.txt

# Install whisper-mic
./venv/bin/pip install -e ../whisper-mic-repo/
```

## Usage

The run script uses these optimal settings:
- `--loop --dictate`: Continuous transcription that types into focused app
- `--faster`: Uses faster-whisper implementation for better performance
- `--model tiny`: Small model for fastest response
- `--english`: English-only transcription

## Docker Advantages

The Docker setup solves common issues:
- ✅ All dependencies pre-installed with correct versions
- ✅ GPU acceleration with CUDA support for RTX 3050 mobile
- ✅ Proper audio device access via PulseAudio and ALSA
- ✅ No conflicts with system libraries
- ✅ Consistent environment across different systems
- ✅ Enhanced wrapper with timestamps and microphone detection

## Troubleshooting

### Docker Issues
- If audio doesn't work, ensure PulseAudio is running: `systemctl --user status pulseaudio`
- For GPU issues, verify Docker has NVIDIA runtime: `docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi`

### Local Installation Issues
- Ensure your microphone is working and accessible
- The script will download the tiny whisper model on first run
- For audio device issues, run: `whisper_mic --list_devices` to see available microphones
- For library conflicts, use the Docker setup instead

## Enhanced Features

The Docker container now includes an enhanced wrapper (`whisper_mic_wrapper.py`) that provides:

### Timestamps
- All output includes timestamps in `[HH:MM:SS.mmm]` format
- Shows initialization time, transcription duration, and other timing metrics
- Helpful for analyzing transcription performance and latency

### Microphone Detection
- Automatically detects and displays all available microphones at startup
- Shows which microphone is being used (default or specified)
- Use `--list_devices` flag to see all available audio devices

### Example Output
```
[14:23:15.123] === Whisper-Mic Enhanced Wrapper Starting ===
[14:23:15.124] Model: tiny, Device: cuda, Faster: true
[14:23:15.125] Energy threshold: 300, Pause: 0.8s
[14:23:15.126] Detecting available microphones...
[14:23:15.234] Found 3 microphone(s):
[14:23:15.235]   [0] Default
[14:23:15.236]   [1] Anker PowerConf C200
[14:23:15.237]   [2] Built-in Audio
[14:23:15.238] Default microphone: [1] Anker PowerConf C200
[14:23:15.239] Initializing Whisper-Mic...
[14:23:16.123] Whisper-Mic initialized in 0.88s
[14:23:16.124] Starting continuous transcription loop...
[14:23:16.125] Audio settings - Energy: 300, Pause: 0.8s, Dynamic energy: true
[14:23:16.126] Listening for speech... (Ctrl+C to stop)
```

### Performance Optimizations

The setup has been optimized for responsiveness:

- **Model**: Uses `tiny` model by default (fastest startup and processing)
- **Energy threshold**: Set to 300 (more sensitive to speech)
- **Pause threshold**: Reduced to 0.8s (faster response)
- **Dynamic energy**: Enabled (adapts to ambient noise)
- **Phrase time limit**: Set to 2s (processes chunks quickly)

### Debug Performance Issues

If experiencing slow startup or responsiveness issues:

1. **Run performance debug tool**:
   ```bash
   # In development container
   python3 /app/debug_performance.py --test-models --test-energy --test-audio
   ```

2. **Check GPU acceleration**:
   ```bash
   # Should show "CUDA available: True"
   python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"
   ```

3. **Test different configurations**:
   ```bash
   # Ultra-fast but less accurate
   python3 /app/whisper_mic_wrapper.py --model tiny --energy 200 --pause 0.5
   
   # More accurate but slower
   python3 /app/whisper_mic_wrapper.py --model base --energy 400 --pause 1.0
   ```

## Command Reference

Available whisper_mic flags:
- `--model`: Model size (tiny, base, small, medium, large)
- `--faster`: Use faster-whisper implementation
- `--english`: English-only transcription
- `--loop`: Continuous listening
- `--dictate`: Type output into focused application
- `--mic_index`: Specify microphone device
- `--list_devices`: Show available audio devices


 the following is the CLI do python file from the whisper mice project going all of the relevant CLI commands


```python
#!/usr/bin/env python3

import click
import torch
import speech_recognition as sr
from typing import Optional

from whisper_mic import WhisperMic

@click.command()
@click.option("--model", default="base", help="Model to use", type=click.Choice(["tiny","base", "small","medium","large","large-v2","large-v3"]))
@click.option("--device", default=("cuda" if torch.cuda.is_available() else "cpu"), help="Device to use", type=click.Choice(["cpu","cuda","mps"]))
@click.option("--english", default=False, help="Whether to use English model",is_flag=True, type=bool)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True,type=bool)
@click.option("--energy", default=300, help="Energy level for mic to detect", type=int)
@click.option("--dynamic_energy", default=False,is_flag=True, help="Flag to enable dynamic energy", type=bool)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
@click.option("--save_file",default=False, help="Flag to save file", is_flag=True,type=bool)
@click.option("--loop", default=False, help="Flag to loop", is_flag=True,type=bool)
@click.option("--dictate", default=False, help="Flag to dictate (implies loop)", is_flag=True,type=bool)
@click.option("--mic_index", default=None, help="Mic index to use", type=int)
@click.option("--list_devices",default=False, help="Flag to list devices", is_flag=True,type=bool)
@click.option("--faster",default=False, help="Use faster_whisper implementation", is_flag=True,type=bool)
@click.option("--hallucinate_threshold",default=400, help="Raise this to reduce hallucinations.  Lower this to activate more often.", is_flag=False,type=int)
def main(model: str, english: bool, verbose: bool, energy:  int, pause: float, dynamic_energy: bool, save_file: bool, device: str, loop: bool, dictate: bool,mic_index:Optional[int],list_devices: bool,faster: bool,hallucinate_threshold:int) -> None:
    if list_devices:
        print("Possible devices: ",sr.Microphone.list_microphone_names())
        return
    mic = WhisperMic(model=model, english=english, verbose=verbose, energy=energy, pause=pause, dynamic_energy=dynamic_energy, save_file=save_file, device=device,mic_index=mic_index,implementation=("faster_whisper" if faster else "whisper"),hallucinate_threshold=hallucinate_threshold)

    if not loop:
        try:
            result = mic.listen()
            print("You said: " + result)
        except KeyboardInterrupt:
            print("Operation interrupted successfully")
        finally:
            if save_file:
                mic.file.close()
    else:
        try:
            mic.listen_loop(dictate=dictate,phrase_time_limit=2)
        except KeyboardInterrupt:
            print("Operation interrupted successfully")
        finally:
            if save_file:
                mic.file.close()

if __name__ == "__main__":
    main()
```