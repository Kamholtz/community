#!/usr/bin/env python3
"""
Faster-whisper based real-time dictation with minimal dependencies.
Uses faster-whisper directly without WhisperX word alignment.
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
import platform

try:
    from faster_whisper import WhisperModel
    import pyaudio
    import numpy as np
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install: pip install faster-whisper pyaudio numpy")
    sys.exit(1)


class FasterWhisperDictation:
    def __init__(self, model_size="small.en", device="auto", compute_type="auto"):
        self.model_size = model_size
        self.device = device if device != "auto" else ("cuda" if self._has_cuda() else "cpu")
        
        # Auto-select compute type based on device
        if compute_type == "auto":
            if self.device == "cuda":
                self.compute_type = "float16"
            else:
                self.compute_type = "int8"  # Better for CPU
        else:
            self.compute_type = compute_type
        
        # Audio settings optimized for faster processing
        self.sample_rate = 16000
        self.chunk_duration = 3.0  # Shorter chunks for faster response
        self.overlap_duration = 0.5  # Minimal overlap
        
        # Threading
        self.audio_queue = Queue()
        self.running = False
        
        print(f"Using device: {self.device}, compute_type: {self.compute_type}")
        
    def _has_cuda(self):
        """Check if CUDA is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            # Try nvidia-smi as fallback
            try:
                subprocess.run(["nvidia-smi"], check=True, capture_output=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
        
    def load_model(self):
        """Load faster-whisper model"""
        print(f"Loading faster-whisper model: {self.model_size}")
        self.model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
            download_root=os.path.expanduser("~/.cache/huggingface/hub")
        )
        print("Model loaded successfully!")
        
    def paste_text(self, text):
        """Paste text using platform-specific methods"""
        system = platform.system().lower()
        
        try:
            if system == "linux":
                # Linux: xdotool + xclip
                subprocess.run(['xclip', '-selection', 'clipboard'], 
                             input=text.encode(), check=True)
                time.sleep(0.05)
                subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+v'], 
                             check=True)
            elif system == "windows":
                # Windows: Use PowerShell for clipboard
                subprocess.run(['powershell', '-command', f'Set-Clipboard "{text}"'], 
                             check=True, shell=True)
                time.sleep(0.05)
                # Use VBScript for key sending
                subprocess.run(['powershell', '-command', 
                              'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("^v")'], 
                             check=True, shell=True)
            elif system == "darwin":
                # macOS: pbcopy + osascript
                subprocess.run(['pbcopy'], input=text.encode(), check=True)
                time.sleep(0.05)
                subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke "v" using command down'], 
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
        
        # Find the best input device
        device_index = None
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                device_index = i
                break
        
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=1024,
            stream_callback=self.audio_callback
        )
        
        stream.start_stream()
        print(f"Audio capture started (device: {device_index})...")
        
        try:
            while self.running:
                time.sleep(0.1)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
    
    def process_audio_chunks(self):
        """Process audio chunks with faster-whisper"""
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
                
                # Transcribe with faster-whisper
                try:
                    segments, info = self.model.transcribe(
                        audio_array, 
                        language="en",
                        beam_size=1,  # Faster beam search
                        best_of=1,    # Single candidate for speed
                        temperature=0.0,  # Deterministic
                        condition_on_previous_text=False  # Independent chunks
                    )
                    
                    # Extract text from segments
                    transcript_parts = []
                    for segment in segments:
                        transcript_parts.append(segment.text.strip())
                    
                    if transcript_parts:
                        transcript = " ".join(transcript_parts).strip()
                        
                        if transcript and transcript != last_transcript:
                            # Simple incremental approach
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
        """Convert audio bytes to numpy array for faster-whisper"""
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
            
            print("Faster-whisper dictation started! Speak now (Ctrl+C to stop)")
            
            # Process audio in main thread
            self.process_audio_chunks()
            
        except KeyboardInterrupt:
            print("\nStopping dictation...")
        finally:
            self.running = False


def main():
    parser = argparse.ArgumentParser(description="Faster-whisper Real-time Dictation")
    parser.add_argument("--model", default="small.en", 
                       help="Model size (tiny.en, base.en, small.en, medium.en, large-v3)")
    parser.add_argument("--device", default="auto", 
                       help="Device to use (auto, cuda, cpu)")
    parser.add_argument("--compute-type", default="auto",
                       help="Compute type (auto, float16, float32, int8)")
    
    args = parser.parse_args()
    
    dictation = FasterWhisperDictation(
        model_size=args.model,
        device=args.device,
        compute_type=args.compute_type
    )
    
    dictation.run()


if __name__ == "__main__":
    main()