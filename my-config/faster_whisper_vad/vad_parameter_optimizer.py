#!/usr/bin/env python3
"""
VAD Parameter Optimization Loop
Automatically tests different VAD parameters and finds optimal settings.
"""

import os
import json
import time
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from advanced_vad_analyzer_pure import AdvancedVADAnalyzer, create_comprehensive_report

class VADParameterOptimizer:
    """Automatically optimize VAD parameters through iterative testing."""
    
    def __init__(self, test_audio_file=None):
        self.test_audio_file = test_audio_file
        self.analyzer = AdvancedVADAnalyzer()
        self.optimization_history = []
        self.best_score = 0
        self.best_params = None
        
        # Parameter ranges to test
        self.parameter_space = {
            'aggressiveness': [0, 1, 2, 3],
            'start_gate_ms': [100, 200, 300, 400, 500],
            'end_gate_ms': [400, 600, 800, 1000, 1200, 1500],
            'volume_threshold': [0.005, 0.008, 0.01, 0.015, 0.02, 0.025]
        }
        
        # Current best-guess parameters (from previous analysis)
        self.current_params = {
            'aggressiveness': 1,
            'start_gate_ms': 200,
            'end_gate_ms': 800,
            'volume_threshold': 0.008
        }
    
    def update_vad_parameters(self, params):
        """Update VAD parameters in faster_whisper_vad.py"""
        
        vad_script = Path("faster_whisper_vad.py")
        if not vad_script.exists():
            raise FileNotFoundError("faster_whisper_vad.py not found")
        
        # Read current script
        with open(vad_script, 'r') as f:
            content = f.read()
        
        # Update parameters
        replacements = {
            f'START_GATE_MS = int(os.environ.get(\'START_GATE_MS\', {self.current_params["start_gate_ms"]}))':
                f'START_GATE_MS = int(os.environ.get(\'START_GATE_MS\', {params["start_gate_ms"]}))',
            f'END_GATE_MS = int(os.environ.get(\'END_GATE_MS\', {self.current_params["end_gate_ms"]}))':
                f'END_GATE_MS = int(os.environ.get(\'END_GATE_MS\', {params["end_gate_ms"]}))',
            f'VOLUME_THRESHOLD = {self.current_params["volume_threshold"]}':
                f'VOLUME_THRESHOLD = {params["volume_threshold"]}',
            f'vad = webrtcvad.Vad({self.current_params["aggressiveness"]})':
                f'vad = webrtcvad.Vad({params["aggressiveness"]})'
        }
        
        # Apply replacements
        new_content = content
        for old, new in replacements.items():
            if old in new_content:
                new_content = new_content.replace(old, new)
            else:
                # Try to find similar patterns
                import re
                patterns = {
                    'START_GATE_MS': r'START_GATE_MS = int\(os\.environ\.get\([\'"]START_GATE_MS[\'"], (\d+)\)\)',
                    'END_GATE_MS': r'END_GATE_MS = int\(os\.environ\.get\([\'"]END_GATE_MS[\'"], (\d+)\)\)',
                    'VOLUME_THRESHOLD': r'VOLUME_THRESHOLD = ([\d.]+)',
                    'aggressiveness': r'vad = webrtcvad\.Vad\((\d+)\)'
                }
                
                for param_name, pattern in patterns.items():
                    if param_name in ['START_GATE_MS', 'END_GATE_MS'] and param_name.lower().replace('_', '') + '_ms' in params:
                        param_key = param_name.lower().replace('_', '') + '_ms'
                        new_content = re.sub(pattern, f'{param_name} = int(os.environ.get(\'{param_name}\', {params[param_key]}))', new_content)
                    elif param_name == 'VOLUME_THRESHOLD' and 'volume_threshold' in params:
                        new_content = re.sub(pattern, f'VOLUME_THRESHOLD = {params["volume_threshold"]}', new_content)
                    elif param_name == 'aggressiveness' and 'aggressiveness' in params:
                        new_content = re.sub(pattern, f'vad = webrtcvad.Vad({params["aggressiveness"]})', new_content)
        
        # Write updated script
        with open(vad_script, 'w') as f:
            f.write(new_content)
        
        self.current_params = params
        print(f"✅ Updated VAD parameters: {params}")
    
    def run_vad_test(self, params, timeout=30):
        """Run VAD system with given parameters and capture output."""
        
        print(f"🧪 Testing parameters: {params}")
        
        # Update parameters
        self.update_vad_parameters(params)
        
        # Prepare test command
        if self.test_audio_file and os.path.exists(self.test_audio_file):
            # TODO: Modify VAD script to accept audio file input
            print("⚠️  Audio file testing not implemented yet - using manual test")
            return self._manual_test_prompt()
        else:
            return self._manual_test_prompt()
    
    def _manual_test_prompt(self):
        """Prompt user to manually test and provide output."""
        
        print("\n" + "="*50)
        print("🎤 MANUAL TEST REQUIRED")
        print("="*50)
        print("1. Run your VAD system now with the updated parameters")
        print("2. Say 'the quick brown fox jumps over the lazy dog' 3 times")
        print("3. Copy the transcription output")
        print("4. Paste it below (press Enter twice when done)")
        print("="*50)
        
        lines = []
        while True:
            line = input()
            if line == "" and lines:
                break
            lines.append(line)
        
        transcription = "\n".join(lines).strip()
        
        if not transcription:
            print("❌ No transcription provided - skipping this test")
            return None
        
        print("✅ Transcription captured!")
        return transcription
    
    def analyze_result(self, transcription, params):
        """Analyze transcription result and return score."""
        
        if not transcription:
            return None
        
        results = self.analyzer.comprehensive_analysis(transcription, expected_repetitions=3)
        results['parameters'] = params
        results['test_timestamp'] = datetime.now().isoformat()
        
        score = results['overall_score']
        
        print(f"📊 Score: {score:.1f}/100")
        print(f"   Word Accuracy: {results['word_accuracy']*100:.1f}%")
        print(f"   Sequence Similarity: {results['sequence_similarity']*100:.1f}%")
        print(f"   Phrase Repetitions: {results['phrase_repetitions']}/3")
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"optimization_test_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        return results
    
    def suggest_next_parameters(self):
        """Suggest next parameter set to try based on results."""
        
        if not self.optimization_history:
            # Start with current best-guess
            return self.current_params
        
        # Simple optimization strategy - vary one parameter at a time
        best_result = max(self.optimization_history, key=lambda x: x['overall_score'])
        best_params = best_result['parameters']
        
        # Try to improve the worst-performing aspect
        suggestions = []
        
        if best_result['profanity_detected']:
            # Audio quality issues - increase volume threshold
            new_threshold = min(0.025, best_params['volume_threshold'] * 1.5)
            suggestions.append({**best_params, 'volume_threshold': new_threshold})
        
        if best_result['short_segments'] > 2:
            # Over-segmentation - increase end gate
            new_end_gate = min(1500, best_params['end_gate_ms'] + 200)
            suggestions.append({**best_params, 'end_gate_ms': new_end_gate})
        
        if best_result['consistency_score'] < 0.7:
            # Poor consistency - try different aggressiveness
            new_agg = (best_params['aggressiveness'] + 1) % 4
            suggestions.append({**best_params, 'aggressiveness': new_agg})
        
        if best_result['word_accuracy'] < 0.9:
            # Low word accuracy - adjust start gate
            new_start_gate = max(100, best_params['start_gate_ms'] - 50)
            suggestions.append({**best_params, 'start_gate_ms': new_start_gate})
        
        # Return first suggestion or explore parameter space
        if suggestions:
            return suggestions[0]
        else:
            # Grid search through remaining parameters
            return self._grid_search_next(best_params)
    
    def _grid_search_next(self, current_best):
        """Simple grid search for next parameters to try."""
        
        # Find untested combinations near current best
        tested_params = [result['parameters'] for result in self.optimization_history]
        
        # Vary each parameter slightly
        variations = []
        
        for param in ['aggressiveness', 'start_gate_ms', 'end_gate_ms', 'volume_threshold']:
            current_value = current_best[param]
            possible_values = self.parameter_space[param]
            
            # Try next higher and lower values
            try:
                current_idx = possible_values.index(current_value)
                if current_idx > 0:
                    new_params = {**current_best, param: possible_values[current_idx - 1]}
                    if new_params not in tested_params:
                        variations.append(new_params)
                
                if current_idx < len(possible_values) - 1:
                    new_params = {**current_best, param: possible_values[current_idx + 1]}
                    if new_params not in tested_params:
                        variations.append(new_params)
            except ValueError:
                # Current value not in predefined list, try closest
                closest = min(possible_values, key=lambda x: abs(x - current_value))
                new_params = {**current_best, param: closest}
                if new_params not in tested_params:
                    variations.append(new_params)
        
        return variations[0] if variations else current_best
    
    def run_optimization_loop(self, max_iterations=10):
        """Run the full optimization loop."""
        
        print("🎯 VAD Parameter Optimization Loop")
        print("=" * 60)
        print(f"Target: Find optimal parameters for VAD transcription")
        print(f"Max iterations: {max_iterations}")
        print(f"Test phrase: 'the quick brown fox jumps over the lazy dog' (3 times)")
        print()
        
        for iteration in range(max_iterations):
            print(f"\n🔄 Iteration {iteration + 1}/{max_iterations}")
            print("-" * 40)
            
            # Get next parameters to test
            test_params = self.suggest_next_parameters()
            
            # Run test
            transcription = self.run_vad_test(test_params)
            
            if transcription is None:
                print("⏭️  Skipping this iteration")
                continue
            
            # Analyze results
            results = self.analyze_result(transcription, test_params)
            
            if results:
                self.optimization_history.append(results)
                
                # Update best score
                if results['overall_score'] > self.best_score:
                    self.best_score = results['overall_score']
                    self.best_params = test_params
                    print(f"🏆 New best score: {self.best_score:.1f}/100")
                
                # Check if we should continue
                if self.best_score >= 95:
                    print("✅ Excellent score achieved! Optimization complete.")
                    break
                
                # Ask user if they want to continue
                if iteration < max_iterations - 1:
                    continue_opt = input("\n➡️  Continue optimization? (y/n/s=summary): ").lower()
                    if continue_opt == 'n':
                        break
                    elif continue_opt == 's':
                        self.print_optimization_summary()
                        continue_opt = input("Continue after summary? (y/n): ").lower()
                        if continue_opt == 'n':
                            break
        
        # Final summary
        print("\n" + "=" * 60)
        print("🎉 OPTIMIZATION COMPLETE")
        print("=" * 60)
        self.print_optimization_summary()
        self.save_optimization_results()
    
    def print_optimization_summary(self):
        """Print optimization summary."""
        
        if not self.optimization_history:
            print("No optimization results yet.")
            return
        
        print(f"\n📈 Optimization Summary:")
        print(f"   Tests completed: {len(self.optimization_history)}")
        print(f"   Best score: {self.best_score:.1f}/100")
        print(f"   Best parameters: {self.best_params}")
        
        print(f"\n📊 Score progression:")
        for i, result in enumerate(self.optimization_history):
            score = result['overall_score']
            params_str = f"agg={result['parameters']['aggressiveness']}, gates={result['parameters']['start_gate_ms']}/{result['parameters']['end_gate_ms']}, vol={result['parameters']['volume_threshold']}"
            print(f"   Test {i+1}: {score:.1f}/100 ({params_str})")
    
    def save_optimization_results(self):
        """Save complete optimization results."""
        
        results = {
            'optimization_summary': {
                'best_score': self.best_score,
                'best_parameters': self.best_params,
                'total_tests': len(self.optimization_history),
                'timestamp': datetime.now().isoformat()
            },
            'all_tests': self.optimization_history
        }
        
        filename = f"vad_optimization_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"💾 Complete results saved: {filename}")

def main():
    """Main optimization function."""
    
    # Check if we have a test audio file
    test_audio = None
    if os.path.exists("test_audio/quick_fox_test.wav"):
        test_audio = "test_audio/quick_fox_test.wav"
        print("✅ Found test audio file")
    else:
        print("⚠️  No test audio file found - will use manual testing")
    
    optimizer = VADParameterOptimizer(test_audio)
    
    print("🚀 Starting VAD Parameter Optimization")
    print("This will help you find the best VAD settings automatically.")
    print()
    
    # Ask for confirmation
    start = input("Ready to start optimization? (y/n): ").lower()
    if start != 'y':
        print("Optimization cancelled.")
        return
    
    try:
        optimizer.run_optimization_loop(max_iterations=8)
    except KeyboardInterrupt:
        print("\n\n⚠️  Optimization interrupted by user")
        optimizer.print_optimization_summary()
        optimizer.save_optimization_results()

if __name__ == "__main__":
    main()