#!/usr/bin/env python3
"""
Quick Test Audio Recorder
Creates standardized test audio for VAD system evaluation.
"""

import time
import sys
import os

def record_with_sounddevice():
    """Record using sounddevice library (requires installation)."""
    try:
        import sounddevice as sd
        import soundfile as sf
        
        # Recording parameters
        duration = 30  # seconds
        samplerate = 16000  # Hz
        channels = 1
        
        print("🎙️  Recording Test Audio")
        print("=" * 40)
        print("Instructions:")
        print("• Say: 'the quick brown fox jumps over the lazy dog'")
        print("• Repeat exactly 3 times")
        print("• Leave 2-3 second pauses between repetitions")
        print("• Speak clearly and at normal volume")
        print("• Recording will stop automatically after 30 seconds")
        print("• Press Ctrl+C to stop early if needed")
        print()
        
        # Countdown
        for i in range(3, 0, -1):
            print(f"Recording starts in {i}...")
            time.sleep(1)
        
        print("🔴 Recording started! (30 seconds - press Ctrl+C to stop early)")
        print("Speak now...")
        
        # Record audio
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
        sd.wait()  # Wait for recording to complete
        
        # Save to file
        output_file = 'test_audio/quick_fox_test.wav'
        os.makedirs('test_audio', exist_ok=True)
        sf.write(output_file, audio, samplerate)
        
        print("✅ Recording complete!")
        print(f"📁 Saved as: {output_file}")
        print()
        
        # Test playback
        try:
            print("🔊 Playing back recording...")
            sd.play(audio, samplerate)
            sd.wait()
        except Exception as e:
            print(f"⚠️  Could not play back: {e}")
        
        return output_file
        
    except ImportError:
        print("❌ sounddevice not available")
        return None
    except Exception as e:
        print(f"❌ Recording failed: {e}")
        return None

def record_with_system_tools():
    """Record using system tools (Linux/macOS)."""
    import subprocess
    import platform
    
    os_name = platform.system().lower()
    output_file = 'test_audio/quick_fox_test.wav'
    os.makedirs('test_audio', exist_ok=True)
    
    print("🎙️  Recording Test Audio with System Tools")
    print("=" * 50)
    
    # Show available devices first
    if "linux" in os_name:
        try:
            print("🎤 Available audio devices:")
            result = subprocess.run(['arecord', '-l'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if 'card' in line:
                        print(f"   {line}")
            
            # Show default device
            result = subprocess.run(['arecord', '-L'], capture_output=True, text=True)
            if result.returncode == 0 and 'default' in result.stdout:
                default_line = [l for l in result.stdout.split('\n') if l.strip().startswith('default')][0]
                print(f"📍 Default device: {default_line}")
        except:
            print("⚠️  Could not list audio devices")
    
    print()
    print("Instructions:")
    print("• Say: 'the quick brown fox jumps over the lazy dog'")
    print("• Repeat exactly 3 times")
    print("• Leave 2-3 second pauses between repetitions")
    print()
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"Recording starts in {i}...")
        time.sleep(1)
    
    try:
        if "linux" in os_name:
            # Try arecord first
            cmd = ['arecord', '-f', 'cd', '-t', 'wav', '-d', '30', output_file]
            print("🔴 Recording with arecord (using default device)...")
            subprocess.run(cmd, check=True)
            
        elif "darwin" in os_name:  # macOS
            # Try sox
            cmd = ['sox', '-t', 'coreaudio', 'default', output_file, 'trim', '0', '30']
            print("🔴 Recording with sox...")
            subprocess.run(cmd, check=True)
            
        else:
            print("❌ Unsupported OS for system recording")
            return None
            
        print("✅ Recording complete!")
        print(f"📁 Saved as: {output_file}")
        return output_file
        
    except subprocess.CalledProcessError as e:
        print(f"❌ System recording failed: {e}")
        return None
    except FileNotFoundError as e:
        print(f"❌ Recording tool not found: {e}")
        print("Try installing: arecord (Linux) or sox (macOS)")
        return None

def main():
    """Main recording function."""
    
    print("🎯 VAD Test Audio Recorder")
    print("=" * 30)
    print()
    
    # Try sounddevice first (most reliable)
    output_file = record_with_sounddevice()
    
    # Fallback to system tools
    if output_file is None:
        output_file = record_with_system_tools()
    
    if output_file:
        print()
        print("🚀 Next Steps:")
        print("1. Test the recording:")
        print(f"   python simple_vad_test.py {output_file}")
        print("2. Or test with the full system:")
        print("   # Modify faster_whisper_vad.py to use file input")
        print("3. Compare results with optimized parameters")
        print()
        
        # Quick file info
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"📊 File info: {output_file}")
            print(f"   Size: {size:,} bytes (~{size/1024:.1f} KB)")
            print(f"   Expected: ~800 KB for 30s at 16kHz")
    else:
        print()
        print("❌ Recording failed with all methods")
        print()
        print("💡 Alternative options:")
        print("1. Use online recorder: https://online-voice-recorder.com/")
        print("2. Use phone to record and transfer file")
        print("3. Use Audacity or other audio software")
        print("4. Check the RECORDING_GUIDE.md for more options")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Recording cancelled")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")