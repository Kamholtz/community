#!/usr/bin/env python3
"""
Setup script for faster-whisper dictation with minimal dependencies.
Lighter weight alternative to WhisperX setup.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, check=True, shell=False):
    """Run command with error handling"""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(cmd, check=check, shell=shell, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def detect_platform():
    """Detect platform and capabilities"""
    system = platform.system().lower()
    has_gpu = False
    
    # GPU detection
    try:
        if system == "linux":
            result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
            has_gpu = result.returncode == 0
        elif system == "windows":
            result = subprocess.run(["nvidia-smi.exe"], capture_output=True, text=True)
            has_gpu = result.returncode == 0
    except FileNotFoundError:
        pass
    
    return system, has_gpu

def setup_venv():
    """Create and setup virtual environment"""
    venv_path = Path("venv_faster_whisper")
    
    if venv_path.exists():
        print(f"Virtual environment already exists at {venv_path}")
        response = input("Recreate it? (y/N): ").lower().strip()
        if response == 'y':
            shutil.rmtree(venv_path)
        else:
            return venv_path
    
    print(f"Creating virtual environment at {venv_path}...")
    run_command([sys.executable, "-m", "venv", str(venv_path)])
    
    return venv_path

def get_venv_python(venv_path):
    """Get path to Python executable in venv"""
    system = platform.system().lower()
    if system == "windows":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"

def install_dependencies(venv_python, has_gpu):
    """Install faster-whisper and minimal dependencies"""
    print("Installing dependencies...")
    
    # Upgrade pip first
    run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install basic dependencies
    deps = ["numpy"]
    
    # Install pyaudio (try pre-built, fallback to system)
    print("Installing pyaudio...")
    try:
        run_command([str(venv_python), "-m", "pip", "install", "pyaudio"], check=True)
    except:
        print("⚠️  pyaudio installation failed, checking if available from system...")
        try:
            run_command([str(venv_python), "-c", "import pyaudio; print('✅ pyaudio available from system')"])
        except:
            print("❌ pyaudio not available. You may need to install system audio libraries.")
    
    run_command([str(venv_python), "-m", "pip", "install"] + deps)
    
    # Install PyTorch (required by faster-whisper)
    if has_gpu:
        print("Installing PyTorch with CUDA support...")
        torch_cmd = [
            str(venv_python), "-m", "pip", "install", 
            "torch", "torchaudio",
            "--index-url", "https://download.pytorch.org/whl/cu118"
        ]
        run_command(torch_cmd)
    else:
        print("Installing CPU-only PyTorch...")
        torch_cmd = [
            str(venv_python), "-m", "pip", "install", 
            "torch", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cpu"
        ]
        run_command(torch_cmd)
    
    # Install faster-whisper
    print("Installing faster-whisper...")
    faster_whisper_cmd = [str(venv_python), "-m", "pip", "install", "faster-whisper"]
    run_command(faster_whisper_cmd)
    
    print("✅ Dependencies installed successfully!")

def create_run_script(venv_path, system):
    """Create platform-specific run script for faster-whisper"""
    venv_python = get_venv_python(venv_path)
    script_path = Path("dictate_faster_whisper.py")
    
    if system == "windows":
        # Create batch file for Windows
        batch_content = f'''@echo off
"{venv_python}" "{script_path}" %*
'''
        with open("run_faster_whisper.bat", "w") as f:
            f.write(batch_content)
        print("✅ Created run_faster_whisper.bat")
        
    else:
        # Create shell script for Unix-like systems
        shell_content = f'''#!/bin/bash
"{venv_python}" "{script_path}" "$@"
'''
        with open("run_faster_whisper.sh", "w") as f:
            f.write(shell_content)
        os.chmod("run_faster_whisper.sh", 0o755)
        print("✅ Created run_faster_whisper.sh")

def test_installation(venv_python):
    """Test that faster-whisper imports correctly"""
    print("Testing installation...")
    
    # Test core components
    test_cmd = [
        str(venv_python), "-c", 
        "import faster_whisper, torch, numpy; print('✅ faster-whisper, PyTorch, and NumPy imported successfully!')"
    ]
    
    try:
        run_command(test_cmd)
        
        # Test pyaudio separately
        try:
            pyaudio_cmd = [str(venv_python), "-c", "import pyaudio; print('✅ PyAudio available')"]
            run_command(pyaudio_cmd)
        except:
            print("⚠️  PyAudio not available - you'll need system audio support")
        
        # Test model loading (quick check)
        model_test_cmd = [
            str(venv_python), "-c", 
            "from faster_whisper import WhisperModel; print('✅ WhisperModel can be imported')"
        ]
        run_command(model_test_cmd)
        
        return True
    except:
        print("❌ Installation test failed")
        return False

def main():
    print("Faster-whisper Virtual Environment Setup")
    print("=" * 45)
    
    # Detect system
    system, has_gpu = detect_platform()
    print(f"Platform: {system}")
    print(f"GPU detected: {'Yes' if has_gpu else 'No'}")
    print()
    
    # Check Python version
    if sys.version_info < (3,8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Setup virtual environment
    venv_path = setup_venv()
    venv_python = get_venv_python(venv_path)
    
    # Install dependencies
    install_dependencies(venv_python, has_gpu)
    
    # Create run script
    create_run_script(venv_path, system)
    
    # Test installation
    if test_installation(venv_python):
        print("\n🎉 Setup completed successfully!")
        print("\nTo use faster-whisper dictation:")
        
        if system == "windows":
            print("  run_faster_whisper.bat")
        else:
            print("  ./run_faster_whisper.sh")
            
        print(f"\nOr activate the venv manually and run:")
        if system == "windows":
            print(f"  {venv_path}\\Scripts\\activate.bat")
        else:
            print(f"  source {venv_path}/bin/activate")
        print(f"  python dictate_faster_whisper.py")
        
        print(f"\nAvailable models: tiny.en, base.en, small.en, medium.en, large-v3")
        print(f"Usage: ./run_faster_whisper.sh --model medium.en")
        
    else:
        print("❌ Setup completed but testing failed. Check the error messages above.")

if __name__ == "__main__":
    main()