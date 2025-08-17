#!/usr/bin/env python3
"""
Enhanced whisper-mic wrapper with timestamps and microphone detection
"""

import click
import torch
import speech_recognition as sr
import time
import datetime
import subprocess
import sys
from typing import Optional

try:
    from whisper_mic import WhisperMic
except ImportError:
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ERROR: whisper_mic not installed")
    sys.exit(1)


def print_timestamped(message):
    """Print message with timestamp"""
    timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
    print(f"[{timestamp}] {message}")


def detect_and_show_microphone():
    """Detect and display available microphones and the one being used"""
    print_timestamped("Detecting available microphones...")
    
    try:
        # Get list of available microphones
        mic_list = sr.Microphone.list_microphone_names()
        
        print_timestamped(f"Found {len(mic_list)} microphone(s):")
        for i, mic_name in enumerate(mic_list):
            print_timestamped(f"  [{i}] {mic_name}")
        
        # Test which microphone will be used by default
        try:
            # Create a microphone instance to see which one gets selected
            mic = sr.Microphone()
            default_mic = mic_list[mic.device_index] if mic.device_index < len(mic_list) else "Unknown"
            print_timestamped(f"Default microphone: [{mic.device_index}] {default_mic}")
            return mic.device_index, default_mic
        except Exception as e:
            print_timestamped(f"Could not determine default microphone: {e}")
            return None, "Unknown"
            
    except Exception as e:
        print_timestamped(f"Error detecting microphones: {e}")
        return None, "Unknown"


@click.command()
@click.option("--model", default="base", help="Model to use", type=click.Choice(["tiny","base", "small","medium","large","large-v2","large-v3"]))
@click.option("--device", default=("cuda" if torch.cuda.is_available() else "cpu"), help="Device to use", type=click.Choice(["cpu","cuda","mps"]))
@click.option("--english", default=False, help="Whether to use English model", is_flag=True, type=bool)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True, type=bool)
@click.option("--energy", default=300, help="Energy level for mic to detect", type=int)
@click.option("--dynamic_energy", default=False, is_flag=True, help="Flag to enable dynamic energy", type=bool)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
@click.option("--save_file", default=False, help="Flag to save file", is_flag=True, type=bool)
@click.option("--loop", default=False, help="Flag to loop", is_flag=True, type=bool)
@click.option("--dictate", default=False, help="Flag to dictate (implies loop)", is_flag=True, type=bool)
@click.option("--mic_index", default=None, help="Mic index to use", type=int)
@click.option("--list_devices", default=False, help="Flag to list devices", is_flag=True, type=bool)
@click.option("--faster", default=False, help="Use faster_whisper implementation", is_flag=True, type=bool)
@click.option("--hallucinate_threshold", default=400, help="Raise this to reduce hallucinations.  Lower this to activate more often.", is_flag=False, type=int)
def main(model: str, english: bool, verbose: bool, energy: int, pause: float, dynamic_energy: bool, 
         save_file: bool, device: str, loop: bool, dictate: bool, mic_index: Optional[int], 
         list_devices: bool, faster: bool, hallucinate_threshold: int) -> None:
    
    # Print startup information with timestamp
    print_timestamped("=== Whisper-Mic Enhanced Wrapper Starting ===")
    print_timestamped(f"Model: {model}, Device: {device}, Faster: {faster}")
    print_timestamped(f"Energy threshold: {energy}, Pause: {pause}s")
    
    if list_devices:
        detect_and_show_microphone()
        return
    
    # Always show microphone information
    mic_index_detected, mic_name = detect_and_show_microphone()
    
    # Use detected mic if none specified
    if mic_index is None and mic_index_detected is not None:
        mic_index = mic_index_detected
        print_timestamped(f"Using detected default microphone: [{mic_index}] {mic_name}")
    elif mic_index is not None:
        print_timestamped(f"Using specified microphone index: {mic_index}")
    
    print_timestamped("Initializing Whisper-Mic...")
    start_init = time.time()
    
    try:
        mic = WhisperMic(
            model=model, 
            english=english, 
            verbose=verbose, 
            energy=energy, 
            pause=pause, 
            dynamic_energy=dynamic_energy, 
            save_file=save_file, 
            device=device,
            mic_index=mic_index,
            implementation=("faster_whisper" if faster else "whisper"),
            hallucinate_threshold=hallucinate_threshold
        )
        
        init_time = time.time() - start_init
        print_timestamped(f"Whisper-Mic initialized in {init_time:.2f}s")
        
    except Exception as e:
        print_timestamped(f"ERROR: Failed to initialize Whisper-Mic: {e}")
        sys.exit(1)

    if not loop and not dictate:
        print_timestamped("Starting single transcription...")
        try:
            start_transcribe = time.time()
            result = mic.listen()
            transcribe_time = time.time() - start_transcribe
            print_timestamped(f"Transcription completed in {transcribe_time:.2f}s")
            print_timestamped(f"Result: {result}")
        except KeyboardInterrupt:
            print_timestamped("Operation interrupted by user")
        except Exception as e:
            print_timestamped(f"ERROR during transcription: {e}")
        finally:
            if save_file:
                mic.file.close()
    else:
        print_timestamped("Starting continuous transcription loop...")
        if dictate:
            print_timestamped("Dictation mode enabled - text will be typed into focused window")
        print_timestamped(f"Audio settings - Energy: {energy}, Pause: {pause}s, Dynamic energy: {dynamic_energy}")
        print_timestamped("Listening for speech... (Ctrl+C to stop)")
        
        try:
            # Add a custom listen loop with better logging
            mic.listen_loop(dictate=dictate, phrase_time_limit=2)
        except KeyboardInterrupt:
            print_timestamped("Continuous transcription stopped by user")
        except Exception as e:
            print_timestamped(f"ERROR during continuous transcription: {e}")
        finally:
            if save_file:
                mic.file.close()
    
    print_timestamped("=== Whisper-Mic Enhanced Wrapper Finished ===")


if __name__ == "__main__":
    main()