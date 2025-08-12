# 🎯 VAD Testing Framework

A comprehensive testing framework for optimizing Voice Activity Detection (VAD) parameters in real-time speech recognition systems.

## 🌟 Features

- **📹 Standardized Test Audio Recording** - Create consistent test recordings for reproducible results
- **🧪 Automated Parameter Testing** - Test multiple VAD parameter combinations automatically  
- **📊 Performance Metrics** - Multiple evaluation metrics including fuzzy matching and phonetic similarity
- **📈 Visual Dashboards** - Generate comprehensive performance visualizations and reports
- **🔧 Easy Integration** - Integrate with existing VAD transcription systems
- **⚡ Quick Start Scripts** - Get up and running in minutes

## 🚀 Quick Start

1. **Setup (one time):**
   ```bash
   python setup_vad_testing.py
   ```

2. **Record test audio:**
   ```bash
   python quick_start_vad.py
   # Select option 1: Record test audio
   ```

3. **Optimize VAD parameters:**
   ```bash
   python quick_start_vad.py  
   # Select option 2: Run quick parameter test
   ```

4. **View results dashboard:**
   ```bash
   python quick_start_vad.py
   # Select option 3: Generate dashboard
   ```

## 📁 Framework Structure

```
vad_testing_framework/
├── 🎙️  Audio Recording
│   ├── vad_tester.py           # Core testing framework
│   └── quick_start_vad.py      # Easy-to-use interface
├── 🔧 Integration  
│   ├── vad_integration.py      # Integration with your VAD system
│   └── setup_vad_testing.py    # Complete setup script
├── 📊 Analysis & Visualization
│   ├── vad_dashboard.py        # Performance dashboards
│   └── install_testing_deps.py # Dependency installer
├── 📚 Documentation
│   ├── VAD_TESTING_GUIDE.md    # Comprehensive usage guide
│   └── VAD_TESTING_README.md   # This file
└── 📂 Generated Directories
    ├── test_audio/             # Recorded test audio files
    ├── test_results/           # Test results (JSON)
    ├── reports/                # Generated reports and charts
    └── temp/                   # Temporary files
```

## 🎵 Test Audio Recording

### Standard Test Phrases
The framework uses **"the quick brown fox jumps over the lazy dog"** as the standard test phrase because it:
- Contains all major English phonemes
- Has a predictable structure for evaluation
- Is commonly used in speech recognition benchmarks
- Allows for consistent cross-session comparisons

### Recording Scenarios
- **Normal pace**: Natural speaking speed with 2-second pauses
- **Fast pace**: Rapid speech with minimal pauses
- **Slow pace**: Deliberate, clear speech with long pauses  
- **Natural conversation**: Unscripted speech for real-world testing

### Audio Quality Requirements
- **Sample Rate**: 16kHz (matches faster-whisper expectations)
- **Format**: 16-bit PCM WAV
- **Channels**: Mono
- **Duration**: 20-30 seconds for standard tests

## 🧪 Parameter Testing

### VAD Parameters Optimized

| Parameter | Range | Description |
|-----------|-------|-------------|
| **Aggressiveness** | 0-3 | WebRTC VAD sensitivity (0=least, 3=most aggressive) |
| **Start Gate** | 200-500ms | Continuous speech needed to trigger detection |
| **End Gate** | 600-1500ms | Silence duration needed to end detection |
| **Volume Threshold** | 0.005-0.02 | Minimum RMS volume to consider as speech |

### Testing Strategies

**Quick Test** (3 combinations):
- Fast overview of performance
- Good for initial parameter exploration
- Takes 1-3 minutes per audio file

**Full Test** (48+ combinations):  
- Comprehensive parameter grid search
- Best for final optimization
- Takes 15-30 minutes per audio file

## 📊 Performance Metrics

### Core Metrics

| Metric | Range | Description |
|--------|-------|-------------|
| **Overall Score** | 0-100 | Composite performance score |
| **Key Words Detected** | 0.0-1.0 | Fraction of important words correctly transcribed |
| **Sequence Similarity** | 0.0-1.0 | Structural similarity to expected text |
| **Word Accuracy** | 0.0-1.0 | Word-level accuracy (similar to WER) |
| **Fuzzy Ratio** | 0-100 | String similarity using fuzzy matching |
| **Repetition Count** | Integer | Number of phrase repetitions detected |

### Quality Indicators

- **✅ Excellent**: Overall Score > 80, Key Words > 0.8
- **✅ Good**: Overall Score 60-80, Key Words > 0.6  
- **⚠️ Acceptable**: Overall Score 40-60, Key Words > 0.4
- **❌ Needs Work**: Overall Score < 40, Key Words < 0.4

### Advanced Metrics (when available)
- **Phonetic Similarity**: Sound-alike matching using Jaro-Winkler distance
- **Token Matching**: Advanced fuzzy string algorithms
- **Profanity Detection**: Identifies ASR transcription errors
- **Text Fragmentation**: Measures output coherence

## 📈 Dashboard Visualizations

### Performance Comparison
- Bar charts showing overall scores across parameter combinations
- Breakdown by individual metrics (key words, similarity, accuracy)
- Clear identification of best and worst performers

### Parameter Heatmaps
- 2D heatmaps showing parameter interaction effects
- Color-coded performance indicators
- Easy identification of optimal parameter ranges

### Optimization Curves
- Progress tracking showing improvement over parameter combinations
- Score distribution histograms
- Convergence analysis

### Correlation Analysis  
- Parameter-performance correlation matrices
- Identify which parameters most impact performance
- Guide future optimization efforts

## 🔧 Integration Guide

### With Existing VAD Systems

1. **Modify Integration Layer:**
   ```python
   # In vad_integration.py
   def _create_test_script(self, vad_params):
       # Customize parameter injection for your system
       pass
   ```

2. **Test Integration:**
   ```python
   from vad_integration import VADSystemIntegrator
   
   integrator = VADSystemIntegrator("your_vad_script.py")
   result = integrator.run_transcription_on_audio("test.wav", params)
   ```

3. **Validate Results:**
   ```python
   from vad_tester import TranscriptionEvaluator
   
   evaluator = TranscriptionEvaluator()
   metrics = evaluator.evaluate_transcription_accuracy(result['text'])
   ```

### Custom Evaluation Metrics

Add domain-specific evaluation:

```python
class CustomEvaluator(TranscriptionEvaluator):
    def evaluate_domain_specific(self, actual, expected):
        # Your custom evaluation logic
        domain_score = calculate_domain_accuracy(actual, expected)
        return domain_score
```

## 📋 Testing Workflows

### Basic Workflow
1. Record standardized test audio (20-30 seconds)
2. Run quick parameter sweep (3-5 combinations)
3. Identify best-performing configuration
4. Test with additional audio samples to validate

### Advanced Workflow  
1. Create comprehensive test suite (multiple scenarios)
2. Run full parameter grid search
3. Analyze results with correlation matrices
4. Fine-tune around optimal parameter ranges
5. Validate with real-world audio samples

### Continuous Testing
1. Set up automated testing with scheduled audio samples
2. Track performance trends over time
3. Alert on performance degradation
4. Automatically re-optimize when needed

## 📊 Example Results

### Typical Performance Scores
- **Baseline (default parameters)**: 45-65
- **Quick optimization**: 65-80
- **Full optimization**: 75-90
- **Fine-tuned system**: 85-95

### Common Optimization Patterns
- **High aggressiveness** (2-3) often works well in clean environments
- **Medium start gates** (200-400ms) balance responsiveness and stability  
- **Longer end gates** (800-1200ms) reduce over-segmentation
- **Low volume thresholds** (0.005-0.01) capture quiet speech

## 🛠️ Troubleshooting

### Common Issues

**Audio Recording Problems:**
```bash
# No audio devices found
sudo apt-get install portaudio19-dev  # Linux
# Check microphone permissions on macOS/Windows
```

**Dependency Issues:**
```bash
# Missing visualization libraries  
pip install matplotlib seaborn pandas

# Missing audio libraries
pip install sounddevice soundfile
```

**Performance Issues:**
```bash
# Tests running too slowly
python quick_start_vad.py  # Use quick test option

# Large audio files
ffmpeg -i input.wav -t 30 -ar 16000 output.wav  # Trim and resample
```

### Getting Help

1. **Check the logs** - All components provide detailed debug output
2. **Validate audio quality** - Use built-in audio validation tools
3. **Test components individually** - Isolate issues by testing each part
4. **Review generated reports** - Look for patterns in performance data

## 🔬 Advanced Features

### Batch Processing
```python
# Process multiple audio files
audio_files = ["test1.wav", "test2.wav", "test3.wav"] 
for audio_file in audio_files:
    results = tester.parameter_sweep(audio_file)
    # Process results...
```

### Custom Parameter Ranges
```python
# Define custom parameter grid
custom_params = {
    'aggressiveness': [1, 2],
    'start_gate_ms': [250, 300, 350], 
    'end_gate_ms': [800, 1000, 1200],
    'volume_threshold': [0.008, 0.01, 0.012]
}
```

### Export and Analysis
```python
# Export results to different formats
df = pd.DataFrame(results)
df.to_csv("vad_results.csv")
df.to_excel("vad_results.xlsx") 

# Statistical analysis
from scipy import stats
correlation = stats.pearsonr(scores, parameters)
```

## 📚 Further Reading

- **VAD_TESTING_GUIDE.md** - Comprehensive usage guide with examples
- **WebRTC VAD Documentation** - Understanding aggressiveness levels
- **Faster-Whisper Documentation** - Model-specific optimization tips
- **Speech Recognition Evaluation** - Standard metrics and practices

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional evaluation metrics
- More VAD algorithm integrations  
- Enhanced visualization options
- Better real-time testing tools
- Mobile/embedded device support

## 📄 License

This testing framework is provided as-is for educational and development purposes.

---

**Happy optimizing!** 🎉 

For questions or issues, please refer to the troubleshooting section or check the comprehensive usage guide.