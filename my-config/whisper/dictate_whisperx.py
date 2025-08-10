#!/usr/bin/env python3
"""
WhisperX-based real-time dictation with proper word boundary handling.
"""

import argparse
import subprocess
import sys
import time
import tempfile
import os
import threading
from queue import Queue, Empty
import wave
import io

try:
    import whisperx
    import torch
    import pyaudio
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install: pip install whisperx torch pyaudio")
    sys.exit(1)


class WhisperXDictation:
    def __init__(self, model_size="small.en", device="auto", compute_type="float16"):
        self.model_size = model_size
        self.device = device if device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
        self.compute_type = compute_type if self.device == "cuda" else "float32"
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_duration = 5.0  # seconds
        self.overlap_duration = 1.0  # seconds
        
        # Threading
        self.audio_queue = Queue()
        self.running = False
        
        print(f"Using device: {self.device}, compute_type: {self.compute_type}")
        
    def load_model(self):
        """Load WhisperX model and alignment model"""
        print(f"Loading WhisperX model: {self.model_size}")
        self.model = whisperx.load_model(
            self.model_size, 
            self.device,
            compute_type=self.compute_type
        )
        
        # Load alignment model
        print("Loading alignment model...")
        self.align_model, self.align_metadata = whisperx.load_align_model(
            language_code="en", 
            device=self.device
        )
        
    def paste_text(self, text):
        """Paste text using xdotool/xclip on Linux"""
        try:
            # Copy to clipboard
            subprocess.run(['xclip', '-selection', 'clipboard'], 
                         input=text.encode(), check=True)
            time.sleep(0.05)
            # Paste
            subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+v'], 
                         check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to paste: {e}")
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """PyAudio callback - puts audio data in queue"""
        if status:
            print(f"Audio callback status: {status}")
        self.audio_queue.put(in_data)
        return (None, pyaudio.paContinue)
    
    def capture_audio_continuous(self):
        """Continuous audio capture using PyAudio"""
        p = pyaudio.PyAudio()
        
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=1024,
            stream_callback=self.audio_callback
        )
        
        stream.start_stream()
        print("Audio capture started...")
        
        try:
            while self.running:
                time.sleep(0.1)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
    
    def process_audio_chunks(self):
        """Process audio chunks with WhisperX"""
        audio_buffer = b''
        chunk_size = int(self.sample_rate * self.chunk_duration * 2)  # 2 bytes per sample
        overlap_size = int(self.sample_rate * self.overlap_duration * 2)
        last_transcript = ""
        
        print(f"Processing chunks: {self.chunk_duration}s duration, {self.overlap_duration}s overlap")
        
        while self.running:
            try:
                # Collect audio data
                while len(audio_buffer) < chunk_size and self.running:
                    try:
                        data = self.audio_queue.get(timeout=0.1)
                        audio_buffer += data
                    except Empty:
                        continue
                
                if len(audio_buffer) < chunk_size:
                    continue
                
                # Extract chunk for processing
                chunk_data = audio_buffer[:chunk_size]
                # Keep overlap for next iteration
                audio_buffer = audio_buffer[chunk_size - overlap_size:]
                
                # Convert to audio array
                audio_array = self.bytes_to_audio_array(chunk_data)
                
                if len(audio_array) == 0:
                    continue
                
                # Transcribe with WhisperX
                try:
                    result = self.model.transcribe(audio_array, batch_size=16)
                    
                    if result and "segments" in result and len(result["segments"]) > 0:
                        # Align the results for word-level timestamps
                        result = whisperx.align(
                            result["segments"], 
                            self.align_model, 
                            self.align_metadata, 
                            audio_array, 
                            self.device, 
                            return_char_alignments=False
                        )
                        
                        # Extract text
                        transcript = " ".join([seg["text"].strip() for seg in result["segments"]])
                        transcript = transcript.strip()
                        
                        if transcript and transcript != last_transcript:
                            # Simple approach: paste new transcript if it's different
                            if len(transcript) > len(last_transcript) and transcript.startswith(last_transcript):
                                # Extract only new words
                                new_text = transcript[len(last_transcript):].strip()
                                if new_text:
                                    print(f"New: '{new_text}'")
                                    self.paste_text(new_text + " ")
                            elif transcript != last_transcript:
                                # Completely new transcript
                                print(f"Full: '{transcript}'")
                                self.paste_text(transcript + " ")
                            
                            last_transcript = transcript
                            
                except Exception as e:
                    print(f"Transcription error: {e}")
                    continue
                    
            except Exception as e:
                print(f"Processing error: {e}")
                continue
    
    def bytes_to_audio_array(self, audio_bytes):
        """Convert audio bytes to numpy array for WhisperX"""
        import numpy as np
        
        # Convert bytes to int16 array
        audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
        
        # Convert to float32 and normalize
        audio_array = audio_data.astype(np.float32) / 32768.0
        
        return audio_array
    
    def run(self):
        """Main run loop"""
        try:
            self.load_model()
            self.running = True
            
            # Start audio capture thread
            audio_thread = threading.Thread(target=self.capture_audio_continuous)
            audio_thread.daemon = True
            audio_thread.start()
            
            print("WhisperX dictation started! Speak now (Ctrl+C to stop)")
            
            # Process audio in main thread
            self.process_audio_chunks()
            
        except KeyboardInterrupt:
            print("\nStopping dictation...")
        finally:
            self.running = False


def main():
    parser = argparse.ArgumentParser(description="WhisperX Real-time Dictation")
    parser.add_argument("--model", default="small.en", 
                       help="WhisperX model size (tiny.en, base.en, small.en, medium.en, large-v3)")
    parser.add_argument("--device", default="auto", 
                       help="Device to use (auto, cuda, cpu)")
    parser.add_argument("--compute-type", default="float16",
                       help="Compute type (float16, float32)")
    
    args = parser.parse_args()
    
    dictation = WhisperXDictation(
        model_size=args.model,
        device=args.device,
        compute_type=args.compute_type
    )
    
    dictation.run()


if __name__ == "__main__":
    main()