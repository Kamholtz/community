#!/usr/bin/env python3
"""
Performance debugging script for whisper-mic
Tests various configurations to find optimal settings
"""

import click
import torch
import speech_recognition as sr
import time
import datetime
from typing import Optional

try:
    from whisper_mic import WhisperMic
except ImportError:
    print("ERROR: whisper_mic not installed")
    exit(1)


def print_timestamped(message):
    """Print message with timestamp"""
    timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
    print(f"[{timestamp}] {message}")


@click.command()
@click.option("--test-models", is_flag=True, help="Test startup time for different models")
@click.option("--test-energy", is_flag=True, help="Test different energy thresholds")
@click.option("--test-audio", is_flag=True, help="Test audio device responsiveness")
def main(test_models, test_energy, test_audio):
    """Debug whisper-mic performance issues"""
    
    print_timestamped("=== Whisper-Mic Performance Debug Tool ===")
    
    # System info
    print_timestamped(f"PyTorch version: {torch.__version__}")
    print_timestamped(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print_timestamped(f"CUDA device: {torch.cuda.get_device_name(0)}")
    
    # Test microphones
    print_timestamped("Testing microphone detection...")
    try:
        mic_list = sr.Microphone.list_microphone_names()
        print_timestamped(f"Found {len(mic_list)} microphones:")
        for i, name in enumerate(mic_list):
            print_timestamped(f"  [{i}] {name}")
    except Exception as e:
        print_timestamped(f"Microphone detection error: {e}")
    
    if test_models:
        print_timestamped("\n=== Testing Model Startup Times ===")
        models = ["tiny", "base", "small"]
        
        for model in models:
            print_timestamped(f"Testing {model} model...")
            start_time = time.time()
            
            try:
                mic = WhisperMic(
                    model=model,
                    english=True,
                    implementation="faster_whisper",
                    device="cuda" if torch.cuda.is_available() else "cpu"
                )
                load_time = time.time() - start_time
                print_timestamped(f"  {model} model loaded in {load_time:.2f}s")
                
                # Test a quick transcription
                print_timestamped(f"  Testing {model} transcription speed...")
                # Note: This would require actual audio input
                
            except Exception as e:
                print_timestamped(f"  {model} model failed: {e}")
    
    if test_energy:
        print_timestamped("\n=== Testing Energy Thresholds ===")
        thresholds = [100, 300, 500, 800]
        
        for threshold in thresholds:
            print_timestamped(f"Testing energy threshold: {threshold}")
            try:
                mic = WhisperMic(
                    model="tiny",
                    english=True,
                    implementation="faster_whisper",
                    energy=threshold,
                    device="cuda" if torch.cuda.is_available() else "cpu"
                )
                print_timestamped(f"  Energy {threshold}: OK")
            except Exception as e:
                print_timestamped(f"  Energy {threshold}: ERROR - {e}")
    
    if test_audio:
        print_timestamped("\n=== Testing Audio Responsiveness ===")
        try:
            print_timestamped("Testing audio input detection...")
            r = sr.Recognizer()
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True
            
            with sr.Microphone() as source:
                print_timestamped("Adjusting for ambient noise...")
                start_adjust = time.time()
                r.adjust_for_ambient_noise(source, duration=1)
                adjust_time = time.time() - start_adjust
                print_timestamped(f"Ambient noise adjustment took {adjust_time:.2f}s")
                print_timestamped(f"Energy threshold after adjustment: {r.energy_threshold}")
                
        except Exception as e:
            print_timestamped(f"Audio test error: {e}")
    
    print_timestamped("=== Performance Debug Complete ===")


if __name__ == "__main__":
    main()