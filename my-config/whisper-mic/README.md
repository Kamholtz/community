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

## Troubleshooting

### Docker Issues
- If audio doesn't work, ensure PulseAudio is running: `systemctl --user status pulseaudio`
- For GPU issues, verify Docker has NVIDIA runtime: `docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi`

### Local Installation Issues
- Ensure your microphone is working and accessible
- The script will download the tiny whisper model on first run
- For audio device issues, run: `whisper_mic --list_devices` to see available microphones
- For library conflicts, use the Docker setup instead

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