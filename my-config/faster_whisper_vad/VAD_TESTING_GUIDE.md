# VAD Testing Framework Usage Guide

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
