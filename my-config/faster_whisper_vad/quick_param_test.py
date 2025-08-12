#!/usr/bin/env python3
"""
Quick Parameter Testing Script
Test specific VAD parameters quickly and get immediate feedback.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from advanced_vad_analyzer_pure import AdvancedVADAnalyzer

def update_single_parameter(param_name, param_value):
    """Update a single VAD parameter in faster_whisper_vad.py"""
    
    vad_script = Path("faster_whisper_vad.py")
    if not vad_script.exists():
        print("❌ faster_whisper_vad.py not found")
        return False
    
    # Read current script
    with open(vad_script, 'r') as f:
        content = f.read()
    
    # Parameter patterns
    patterns = {
        'aggressiveness': (r'vad = webrtcvad\.Vad\((\d+)\)', f'vad = webrtcvad.Vad({param_value})'),
        'start_gate_ms': (r'START_GATE_MS = int\(os\.environ\.get\([\'"]START_GATE_MS[\'"], (\d+)\)\)', 
                         f'START_GATE_MS = int(os.environ.get(\'START_GATE_MS\', {param_value}))'),
        'end_gate_ms': (r'END_GATE_MS = int\(os\.environ\.get\([\'"]END_GATE_MS[\'"], (\d+)\)\)', 
                       f'END_GATE_MS = int(os.environ.get(\'END_GATE_MS\', {param_value}))'),
        'volume_threshold': (r'VOLUME_THRESHOLD = ([\d.]+)', f'VOLUME_THRESHOLD = {param_value}')
    }
    
    if param_name not in patterns:
        print(f"❌ Unknown parameter: {param_name}")
        return False
    
    pattern, replacement = patterns[param_name]
    
    # Apply replacement
    new_content = re.sub(pattern, replacement, content)
    
    if new_content == content:
        print(f"⚠️  Could not find pattern for {param_name}")
        return False
    
    # Write updated script
    with open(vad_script, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Updated {param_name} = {param_value}")
    return True

def quick_test_and_analyze():
    """Quick test current parameters and analyze results."""
    
    print("\n" + "="*50)
    print("🎤 QUICK VAD TEST")
    print("="*50)
    print("1. Run your VAD system now")
    print("2. Say 'the quick brown fox jumps over the lazy dog' 3 times")
    print("3. Paste the output below:")
    print()
    
    transcription = input("Transcription output: ").strip()
    
    if not transcription:
        print("❌ No transcription provided")
        return None
    
    # Analyze
    analyzer = AdvancedVADAnalyzer()
    results = analyzer.comprehensive_analysis(transcription, expected_repetitions=3)
    
    # Show key results
    print(f"\n📊 Quick Results:")
    print(f"   Overall Score: {results['overall_score']:.1f}/100")
    print(f"   Word Accuracy: {results['word_accuracy']*100:.1f}%")
    print(f"   Phrase Repetitions: {results['phrase_repetitions']}/3")
    
    # Show issues
    issues = []
    if results.get('profanity_detected'):
        issues.append("Audio quality problems detected")
    if results.get('text_fragments', 0) > 0:
        issues.append(f"Text fragmentation: {results['text_fragments']} fragments")
    if results['phrase_repetitions'] != 3:
        issues.append(f"Wrong repetition count: {results['phrase_repetitions']} vs 3 expected")
    
    if issues:
        print(f"   Issues: {', '.join(issues)}")
    
    # Quick suggestions
    if results['optimization_suggestions']:
        print(f"   💡 Top suggestion: {results['optimization_suggestions'][0]}")
    
    return results

def interactive_parameter_tuning():
    """Interactive parameter tuning session."""
    
    print("🎯 Interactive VAD Parameter Tuning")
    print("=" * 50)
    print("Available parameters:")
    print("  1. aggressiveness (0-3)")
    print("  2. start_gate_ms (100-500)")
    print("  3. end_gate_ms (400-1500)")
    print("  4. volume_threshold (0.005-0.025)")
    print()
    
    # Parameter suggestions based on common issues
    suggestions = {
        'audio_quality': {
            'volume_threshold': 0.015,
            'description': "Increase volume threshold for audio quality issues"
        },
        'over_segmentation': {
            'end_gate_ms': 1000,
            'description': "Increase end gate to reduce over-segmentation"
        },
        'under_segmentation': {
            'end_gate_ms': 600,
            'description': "Decrease end gate to improve segmentation"
        },
        'sensitivity': {
            'aggressiveness': 1,
            'start_gate_ms': 200,
            'description': "Make VAD more sensitive"
        },
        'conservative': {
            'aggressiveness': 3,
            'start_gate_ms': 400,
            'description': "Make VAD more conservative"
        }
    }
    
    print("🚀 Quick presets available:")
    for i, (name, config) in enumerate(suggestions.items(), 1):
        print(f"  {i}. {name}: {config['description']}")
    
    print("  6. Manual parameter entry")
    print("  7. Test current settings")
    print()
    
    while True:
        choice = input("Choose option (1-7, or 'q' to quit): ").strip().lower()
        
        if choice == 'q':
            break
        elif choice == '7':
            quick_test_and_analyze()
        elif choice == '6':
            # Manual parameter entry
            print("\nManual parameter entry:")
            param_name = input("Parameter name (aggressiveness/start_gate_ms/end_gate_ms/volume_threshold): ").strip()
            param_value = input(f"New value for {param_name}: ").strip()
            
            try:
                if param_name == 'aggressiveness':
                    param_value = int(param_value)
                elif param_name in ['start_gate_ms', 'end_gate_ms']:
                    param_value = int(param_value)
                elif param_name == 'volume_threshold':
                    param_value = float(param_value)
                else:
                    print("❌ Invalid parameter name")
                    continue
                
                if update_single_parameter(param_name, param_value):
                    print("✅ Parameter updated! Test it now.")
            
            except ValueError:
                print("❌ Invalid parameter value")
        
        elif choice.isdigit() and 1 <= int(choice) <= 5:
            # Apply preset
            preset_names = list(suggestions.keys())
            preset_name = preset_names[int(choice) - 1]
            preset = suggestions[preset_name]
            
            print(f"\n🔧 Applying preset: {preset_name}")
            print(f"   {preset['description']}")
            
            for param_name, param_value in preset.items():
                if param_name != 'description':
                    update_single_parameter(param_name, param_value)
            
            print("✅ Preset applied! Test it now.")
        
        else:
            print("❌ Invalid choice")
        
        print()

def main():
    """Main function."""
    
    print("🔧 VAD Parameter Testing Tools")
    print("=" * 40)
    print("Choose testing mode:")
    print("  1. Interactive tuning session")
    print("  2. Quick single test")
    print("  3. Apply specific parameter")
    print()
    
    mode = input("Choose mode (1-3): ").strip()
    
    if mode == '1':
        interactive_parameter_tuning()
    elif mode == '2':
        quick_test_and_analyze()
    elif mode == '3':
        param_name = input("Parameter name: ").strip()
        param_value = input("Parameter value: ").strip()
        
        try:
            if param_name == 'aggressiveness':
                param_value = int(param_value)
            elif param_name in ['start_gate_ms', 'end_gate_ms']:
                param_value = int(param_value)
            elif param_name == 'volume_threshold':
                param_value = float(param_value)
            
            update_single_parameter(param_name, param_value)
        except ValueError:
            print("❌ Invalid parameter value")
    else:
        print("❌ Invalid mode")

if __name__ == "__main__":
    main()