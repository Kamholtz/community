"""
Complete VAD Testing Framework Setup Script

This script sets up the complete VAD testing environment including:
1. Dependencies installation
2. Test audio recording
3. Parameter optimization
4. Performance visualization
5. Report generation
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install all required dependencies."""
    
    dependencies = [
        'sounddevice',
        'soundfile', 
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'fuzzywuzzy[speedup]',
        'jellyfish',
        'scipy'  # Often required by other packages
    ]
    
    print(f"📦 Installing {len(dependencies)} packages...")
    
    for package in dependencies:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  ✅ {package}")
        except subprocess.CalledProcessError:
            print(f"  ❌ {package} failed")
    
    print("✅ Dependency installation complete!")

def create_directories():
    """Create necessary directories for VAD testing."""
    
    dirs = [
        'test_audio',
        'test_results', 
        'reports',
        'temp'
    ]
    
    for dirname in dirs:
        Path(dirname).mkdir(exist_ok=True)
        print(f"📁 Created directory: {dirname}")
    
    print("✅ Directory structure ready!")

def test_audio_devices():
    """Test that audio input devices are available."""
    
    try:
        import sounddevice as sd
        
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        
        print(f"🎤 Found {len(input_devices)} audio input devices:")
        for i, device in enumerate(input_devices):
            print(f"  {i}: {device['name']}")
        
        if not input_devices:
            print("⚠️  No audio input devices found!")
            print("   Make sure a microphone is connected")
            return False
        
        # Test default input device
        try:
            default_device = sd.default.device[0]
            if default_device is not None:
                print(f"✅ Default input device: {devices[default_device]['name']}")
                return True
        except Exception:
            pass
        
        print("⚠️  No default input device set")
        return True  # Still OK, just no default
        
    except ImportError:
        print("❌ sounddevice not available - audio testing skipped")
        return False
    except Exception as e:
        print(f"❌ Audio device test failed: {e}")
        return False

def create_quick_start_script():
    """Create a quick start script for easy VAD testing."""
    
    script_content = '''#!/usr/bin/env python3
"""
Quick Start VAD Testing Script

This script provides an easy way to get started with VAD testing.
"""

from vad_tester import AudioRecorder, VADTester, TranscriptionEvaluator
from vad_dashboard import VADDashboard
import sys

def main():
    print("🚀 Quick Start VAD Testing")
    print("=" * 30)
    
    print("\\nWhat would you like to do?")
    print("1. Record test audio")
    print("2. Run quick parameter test") 
    print("3. Generate dashboard from existing results")
    print("4. Full testing workflow")
    
    choice = input("\\nSelect option (1-4): ").strip()
    
    if choice == "1":
        recorder = AudioRecorder()
        filename = input("Audio filename (default: quick_test.wav): ").strip()
        if not filename:
            filename = "quick_test.wav"
        if not filename.endswith('.wav'):
            filename += '.wav'
        
        recorder.record_test_audio(filename, duration=20)
        print(f"✅ Recording complete: {filename}")
        
    elif choice == "2":
        audio_file = input("Path to audio file: ").strip()
        if not audio_file:
            print("❌ Audio file required")
            return
        
        tester = VADTester()
        results = tester.parameter_sweep(audio_file, quick_test=True)
        best = tester.find_optimal_parameters(results)
        tester.save_results(results)
        
        print("✅ Quick test complete!")
        
    elif choice == "3":
        dashboard = VADDashboard()
        try:
            dashboard.create_full_dashboard()
            print("✅ Dashboard generated!")
        except Exception as e:
            print(f"❌ Dashboard generation failed: {e}")
            
    elif choice == "4":
        print("🔄 Running full workflow...")
        
        # Step 1: Record audio
        recorder = AudioRecorder()
        audio_file = recorder.record_test_audio("workflow_test.wav", duration=25)
        
        # Step 2: Run tests
        tester = VADTester()
        print("\\n🧪 Running parameter tests...")
        results = tester.parameter_sweep(audio_file, quick_test=True)
        
        # Step 3: Find best parameters
        best = tester.find_optimal_parameters(results)
        results_file = tester.save_results(results)
        
        # Step 4: Generate dashboard
        dashboard = VADDashboard()
        try:
            outputs = dashboard.create_full_dashboard()
            print("\\n🎉 Complete workflow finished!")
            print(f"Results: {results_file}")
            print("Dashboard files:")
            for name, path in outputs.items():
                print(f"  {name}: {path}")
        except Exception as e:
            print(f"⚠️  Dashboard generation failed: {e}")
            
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
'''
    
    with open('quick_start_vad.py', 'w') as f:
        f.write(script_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        os.chmod('quick_start_vad.py', 0o755)
    
    print("📄 Created quick_start_vad.py")

def create_usage_guide():
    """Create a comprehensive usage guide."""
    
    guide_content = '''# VAD Testing Framework Usage Guide

This guide explains how to use the complete VAD (Voice Activity Detection) testing framework.

## Overview

The VAD testing framework consists of several components:

- `vad_tester.py`: Core testing framework with audio recording and evaluation
- `vad_integration.py`: Integration with your actual VAD transcription system  
- `vad_dashboard.py`: Visualization and reporting tools
- `install_testing_deps.py`: Dependency installer
- `quick_start_vad.py`: Quick start script for common tasks

## Quick Start

1. **Install dependencies:**
   ```bash
   python install_testing_deps.py
   ```

2. **Record test audio:**
   ```bash
   python quick_start_vad.py
   # Choose option 1 and follow prompts
   ```

3. **Run parameter optimization:**
   ```bash
   python quick_start_vad.py  
   # Choose option 2 and provide audio file path
   ```

4. **Generate performance dashboard:**
   ```bash
   python quick_start_vad.py
   # Choose option 3
   ```

## Detailed Usage

### Recording Test Audio

The framework supports recording standardized test audio:

```python
from vad_tester import AudioRecorder

recorder = AudioRecorder()

# Record single file
recorder.record_test_audio("my_test.wav", duration=30)

# Record full test suite
recordings = recorder.create_test_suite()
```

**Test Scenarios Include:**
- Normal pace speech
- Fast speech
- Slow speech  
- Natural conversation

### Running Parameter Tests

Test different VAD parameter combinations:

```python
from vad_tester import VADTester

tester = VADTester()

# Quick test (3 parameter combinations)
results = tester.parameter_sweep("test_audio.wav", quick_test=True)

# Full test (dozens of combinations) 
results = tester.parameter_sweep("test_audio.wav", quick_test=False)

# Find optimal parameters
best_config = tester.find_optimal_parameters(results)
```

### Evaluation Metrics

The framework uses multiple metrics to evaluate performance:

- **Overall Score** (0-100): Composite performance score
- **Key Words Detected**: Fraction of important words correctly transcribed
- **Sequence Similarity**: How well the structure matches expected text
- **Word Accuracy**: Word-level accuracy similar to WER
- **Fuzzy Matching**: Various string similarity measures
- **Repetition Detection**: Identifies and penalizes text repetition issues

### Generating Reports

Create visual dashboards and reports:

```python
from vad_dashboard import VADDashboard

dashboard = VADDashboard()

# Create all visualizations
outputs = dashboard.create_full_dashboard("results_file.json")

# Individual plots
dashboard.create_performance_comparison(results)
dashboard.create_parameter_heatmaps(results)
dashboard.create_optimization_curve(results)
dashboard.create_correlation_analysis(results)

# Text report
report_path = dashboard.generate_summary_report(results)
```

## Parameter Optimization

The framework tests these VAD parameters:

### Aggressiveness (0-3)
- **0**: Least aggressive, detects more speech
- **1**: Moderately aggressive
- **2**: More aggressive (default)
- **3**: Most aggressive, filters more noise

### Start Gate (ms)
- How much continuous speech needed to trigger detection
- **Lower values**: More responsive, may trigger on noise
- **Higher values**: More stable, may miss short sounds
- **Typical range**: 200-500ms

### End Gate (ms)  
- How much silence needed to end speech detection
- **Lower values**: Creates shorter segments
- **Higher values**: Keeps longer segments together
- **Typical range**: 600-1500ms

### Volume Threshold
- Minimum RMS volume to consider as speech
- **Lower values**: More sensitive to quiet speech
- **Higher values**: Filters more background noise
- **Typical range**: 0.005-0.02

## Best Practices

### Recording Quality Audio
- Use a quiet environment
- Maintain consistent distance from microphone
- Speak clearly at normal volume
- Include natural pauses between phrases

### Test Audio Content
- Use standardized phrases for comparison
- Include target phrase: "the quick brown fox jumps over the lazy dog"
- Record multiple repetitions (5x recommended)
- Vary speaking pace and style

### Parameter Testing Strategy
1. Start with quick test to identify promising ranges
2. Focus detailed testing around best-performing values
3. Test with different audio samples to validate results
4. Consider audio environment when selecting parameters

### Interpreting Results
- **Overall Score > 80**: Excellent performance
- **Overall Score 60-80**: Good performance  
- **Overall Score 40-60**: Acceptable performance
- **Overall Score < 40**: Needs improvement

Look for:
- High key word detection (> 0.8)
- Good sequence similarity (> 0.7)
- Minimal repetition issues
- No profanity detection (indicates clean transcription)

## Integration with Your VAD System

To integrate with your actual VAD system:

1. **Modify `vad_integration.py`:**
   - Update the path to your VAD script
   - Customize parameter injection
   - Adapt output parsing

2. **Test Integration:**
   ```python
   from vad_integration import VADSystemIntegrator
   
   integrator = VADSystemIntegrator("your_vad_script.py")
   result = integrator.run_transcription_on_audio("test.wav", params)
   ```

## Troubleshooting

### Common Issues

**"No audio devices found"**
- Check microphone connection
- Verify audio drivers installed
- Try different USB ports for USB microphones

**"sounddevice import error"**
- Install with: `pip install sounddevice`
- On Linux: `sudo apt-get install portaudio19-dev python3-pyaudio`

**"matplotlib display error"**  
- Install GUI backend: `pip install tkinter` or `pip install PyQt5`
- For headless servers: Use `matplotlib.use('Agg')` before importing pyplot

**"Poor transcription quality"**
- Check audio quality and volume levels
- Verify correct sample rate (16kHz recommended)
- Test microphone with other applications
- Try different VAD parameters

**"Parameter optimization too slow"**
- Use `quick_test=True` for faster results
- Reduce audio file length
- Focus on specific parameter ranges

### Getting Help

1. Check the debug output from VAD testing
2. Validate audio file format and quality
3. Test individual components separately
4. Review generated reports for insights

## Advanced Usage

### Custom Evaluation Metrics

Add your own evaluation functions:

```python
class CustomEvaluator(TranscriptionEvaluator):
    def evaluate_custom_metric(self, actual, expected):
        # Your custom evaluation logic
        return custom_score
```

### Batch Processing

Process multiple audio files:

```python
audio_files = ["test1.wav", "test2.wav", "test3.wav"]
all_results = []

for audio_file in audio_files:
    results = tester.parameter_sweep(audio_file)
    all_results.extend(results)

# Analyze combined results
dashboard.create_full_dashboard(all_results)
```

### Export Results

Export results to different formats:

```python
import pandas as pd

# Convert to DataFrame
df = pd.DataFrame(results)

# Export to CSV
df.to_csv("vad_results.csv", index=False)

# Export to Excel
df.to_excel("vad_results.xlsx", index=False)
```
'''
    
    with open('VAD_TESTING_GUIDE.md', 'w') as f:
        f.write(guide_content)
    
    print("📖 Created VAD_TESTING_GUIDE.md")

def main():
    """Main setup function."""
    
    print("🛠️  VAD Testing Framework Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    print("\\n📦 Installing dependencies...")
    install_dependencies()
    
    # Create directory structure
    print("\\n📁 Setting up directories...")
    create_directories()
    
    # Test audio devices
    print("\\n🎤 Testing audio devices...")
    audio_ok = test_audio_devices()
    
    # Create helper scripts
    print("\\n📄 Creating helper scripts...")
    create_quick_start_script()
    create_usage_guide()
    
    # Final status
    print("\\n" + "=" * 50)
    print("🎉 VAD Testing Framework Setup Complete!")
    print("\\nNext steps:")
    print("1. Record test audio: python quick_start_vad.py")
    print("2. Read the guide: VAD_TESTING_GUIDE.md")
    print("3. Run full workflow: python quick_start_vad.py (option 4)")
    
    if not audio_ok:
        print("\\n⚠️  Note: Audio device issues detected")
        print("   Make sure microphone is connected and working")
    
    print("\\nHappy testing! 🚀")
    
    return 0

if __name__ == "__main__":
    exit(main())