#!/usr/bin/env python3
"""
GPU compatibility test for RTX 3050 Ti Mobile
Tests CUDA availability and faster-whisper model loading
"""

import sys
import torch
from faster_whisper import WhisperModel

def test_gpu_compatibility():
    """Test GPU setup for RTX 3050 Ti Mobile."""
    print("=== GPU Compatibility Test for RTX 3050 Ti Mobile ===\n")
    
    # Basic PyTorch CUDA test
    print("1. PyTorch CUDA Test:")
    print(f"   PyTorch version: {torch.__version__}")
    print(f"   CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"   CUDA version: {torch.version.cuda}")
        print(f"   GPU count: {torch.cuda.device_count()}")
        print(f"   GPU device: {torch.cuda.get_device_name(0)}")
        
        # Memory info
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"   GPU memory: {gpu_mem:.1f} GB")
        
        # Test tensor operations
        try:
            x = torch.randn(1000, 1000).cuda()
            y = torch.mm(x, x)
            print("   CUDA tensor operations: ✅ Working")
        except Exception as e:
            print(f"   CUDA tensor operations: ❌ Failed - {e}")
            return False
    else:
        print("   ❌ CUDA not available")
        return False
    
    print("\n2. Faster-Whisper Model Test:")
    try:
        # Test model loading with CUDA
        print("   Loading tiny model with CUDA...")
        model = WhisperModel("tiny", device="cuda", compute_type="float16")
        print("   Model loading: ✅ Success")
        
        # Test transcription with dummy audio
        import numpy as np
        dummy_audio = np.random.randn(16000).astype(np.float32)  # 1 second of audio
        segments, info = model.transcribe(dummy_audio, beam_size=1)
        segments_list = list(segments)
        print(f"   Transcription test: ✅ Success (detected language: {info.language})")
        
    except Exception as e:
        print(f"   Faster-Whisper test: ❌ Failed - {e}")
        return False
    
    print("\n3. Audio Dependencies Test:")
    try:
        import sounddevice as sd
        import webrtcvad
        print("   sounddevice: ✅ Available")
        print("   webrtcvad: ✅ Available")
        
        # Test audio device enumeration
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        print(f"   Audio input devices found: {len(input_devices)}")
        
    except Exception as e:
        print(f"   Audio dependencies: ❌ Failed - {e}")
        return False
    
    print("\n🎉 All tests passed! RTX 3050 Ti Mobile setup is compatible.")
    return True

if __name__ == "__main__":
    success = test_gpu_compatibility()
    sys.exit(0 if success else 1)