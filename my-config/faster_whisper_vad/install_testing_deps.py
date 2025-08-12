"""
Install dependencies for VAD testing framework.
"""

import subprocess
import sys
import importlib

def install_package(package):
    """Install a Python package using pip."""
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def check_and_install_dependencies():
    """Check and install all required dependencies for VAD testing."""
    
    dependencies = {
        'sounddevice': 'sounddevice',
        'soundfile': 'soundfile', 
        'numpy': 'numpy',
        'fuzzywuzzy': 'fuzzywuzzy[speedup]',  # Include speedup
        'jellyfish': 'jellyfish',
        'pathlib': None,  # Built-in, skip
        'json': None,     # Built-in, skip
        'datetime': None, # Built-in, skip
    }
    
    print("🔍 Checking dependencies for VAD testing framework...")
    
    missing_deps = []
    
    for module_name, pip_name in dependencies.items():
        if pip_name is None:
            continue  # Skip built-in modules
            
        try:
            importlib.import_module(module_name.split('.')[0])
            print(f"✅ {module_name} is already installed")
        except ImportError:
            print(f"❌ {module_name} is missing")
            missing_deps.append(pip_name)
    
    if missing_deps:
        print(f"\n📦 Installing {len(missing_deps)} missing packages...")
        
        failed_installs = []
        for package in missing_deps:
            if not install_package(package):
                failed_installs.append(package)
        
        if failed_installs:
            print(f"\n⚠️  Some packages failed to install: {failed_installs}")
            print("You may need to install them manually:")
            for package in failed_installs:
                print(f"  pip install {package}")
        else:
            print(f"\n🎉 All dependencies installed successfully!")
    else:
        print("\n🎉 All dependencies are already installed!")
    
    # Test imports
    print("\n🧪 Testing imports...")
    test_results = {}
    
    test_modules = [
        ('sounddevice', 'sd'),
        ('soundfile', 'sf'),
        ('numpy', 'np'),
        ('fuzzywuzzy.fuzz', 'fuzz'),
        ('jellyfish', 'jellyfish'),
        ('difflib', 'difflib'),
    ]
    
    for module, alias in test_modules:
        try:
            if alias == 'sd':
                import sounddevice as sd
                print(f"✅ sounddevice - version: {sd.__version__ if hasattr(sd, '__version__') else 'unknown'}")
            elif alias == 'sf':
                import soundfile as sf  
                print(f"✅ soundfile - version: {sf.__version__ if hasattr(sf, '__version__') else 'unknown'}")
            elif alias == 'np':
                import numpy as np
                print(f"✅ numpy - version: {np.__version__}")
            elif alias == 'fuzz':
                from fuzzywuzzy import fuzz
                print(f"✅ fuzzywuzzy imported successfully")
            elif alias == 'jellyfish':
                import jellyfish
                print(f"✅ jellyfish - functions: {len(dir(jellyfish))} available")
            elif alias == 'difflib':
                import difflib
                print(f"✅ difflib (built-in) imported successfully")
                
            test_results[module] = True
            
        except ImportError as e:
            print(f"❌ Failed to import {module}: {e}")
            test_results[module] = False
    
    # Show audio devices (if sounddevice works)
    if test_results.get('sounddevice', False):
        try:
            import sounddevice as sd
            print(f"\n🎧 Available audio devices:")
            devices = sd.query_devices()
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    print(f"  {i}: {device['name']} (input channels: {device['max_input_channels']})")
        except Exception as e:
            print(f"⚠️  Could not list audio devices: {e}")
    
    return all(test_results.values())

def main():
    """Main installation function."""
    print("🛠️  VAD Testing Dependencies Installer")
    print("=" * 50)
    
    success = check_and_install_dependencies()
    
    if success:
        print("\n✅ Setup complete! You can now run the VAD testing framework:")
        print("   python vad_tester.py")
    else:
        print("\n❌ Some dependencies failed to install. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())