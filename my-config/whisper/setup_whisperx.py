#!/usr/bin/env python3
"""
Setup script for WhisperX dictation with virtual environment support.
Works cross-platform: Linux, Windows, macOS.
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
    
    # Simple GPU detection
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
    venv_path = Path("venv_whisperx")
    
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

def get_venv_activate_script(venv_path):
    """Get activation command for the virtual environment"""
    system = platform.system().lower()
    if system == "windows":
        return str(venv_path / "Scripts" / "activate.bat")
    else:
        return f"source {venv_path / 'bin' / 'activate'}"

def install_dependencies(venv_python, has_gpu):
    """Install WhisperX and dependencies"""
    print("Installing dependencies...")
    
    # Upgrade pip first
    run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install basic dependencies
    deps = ["numpy"]
    
    # Try to install pyaudio, skip if it fails (Nix might provide it)
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
    
    # Install PyTorch with CUDA support
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
            "torch", "torchaudio"
        ]
        run_command(torch_cmd)
    
    # Install WhisperX from regular PyPI (not CUDA index)
    print("Installing WhisperX...")
    whisperx_cmd = [str(venv_python), "-m", "pip", "install", "whisperx"]
    run_command(whisperx_cmd)
    
    print("✅ Dependencies installed successfully!")

def create_run_script(venv_path, system):
    """Create platform-specific run script"""
    venv_python = get_venv_python(venv_path)
    script_path = Path("dictate_whisperx.py")
    
    if system == "windows":
        # Create batch file for Windows
        batch_content = f'''@echo off
"{venv_python}" "{script_path}" %*
'''
        with open("run_whisperx.bat", "w") as f:
            f.write(batch_content)
        print("✅ Created run_whisperx.bat")
        
    else:
        # Create shell script for Unix-like systems
        shell_content = f'''#!/bin/bash
"{venv_python}" "{script_path}" "$@"
'''
        with open("run_whisperx.sh", "w") as f:
            f.write(shell_content)
        os.chmod("run_whisperx.sh", 0o755)
        print("✅ Created run_whisperx.sh")

def test_installation(venv_python):
    """Test that WhisperX imports correctly"""
    print("Testing installation...")
    
    # Test core components
    test_cmd = [
        str(venv_python), "-c", 
        "import whisperx, torch; print('✅ WhisperX and PyTorch imported successfully!')"
    ]
    
    try:
        run_command(test_cmd)
        
        # Test pyaudio separately (might fail in Nix)
        try:
            pyaudio_cmd = [str(venv_python), "-c", "import pyaudio; print('✅ PyAudio available')"]
            run_command(pyaudio_cmd)
        except:
            print("⚠️  PyAudio not available - you'll need system audio support")
            print("   On Linux with Nix: this is provided by the runtime environment")
        
        return True
    except:
        print("❌ Installation test failed")
        return False

def main():
    print("WhisperX Virtual Environment Setup")
    print("=" * 40)
    
    # Detect system
    system, has_gpu = detect_platform()
    print(f"Platform: {system}")
    print(f"GPU detected: {'Yes' if has_gpu else 'No'}")
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
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
        print("\nTo use WhisperX dictation:")
        
        if system == "windows":
            print("  run_whisperx.bat")
        else:
            print("  ./run_whisperx.sh")
            
        print(f"\nOr activate the venv manually:")
        print(f"  {get_venv_activate_script(venv_path)}")
        print(f"  python dictate_whisperx.py")
        
    else:
        print("❌ Setup completed but testing failed. Check the error messages above.")

if __name__ == "__main__":
    main()