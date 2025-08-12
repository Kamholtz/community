"""
Comprehensive VAD Testing Framework

This module provides tools for:
1. Recording standardized test audio
2. Automated VAD parameter testing
3. Transcription accuracy measurement with fuzzy matching
4. Performance comparison and optimization
"""

import os
import json
import time
import numpy as np
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# For fuzzy matching
from difflib import SequenceMatcher
try:
    from fuzzywuzzy import fuzz
    FUZZYWUZZY_AVAILABLE = True
except ImportError:
    print("fuzzywuzzy not available - install with: pip install fuzzywuzzy")
    FUZZYWUZZY_AVAILABLE = False

try:
    import jellyfish
    JELLYFISH_AVAILABLE = True
except ImportError:
    print("jellyfish not available - install with: pip install jellyfish")
    JELLYFISH_AVAILABLE = False

# Local imports
from text_differ_v2 import StreamingASRTextDiffer


class AudioRecorder:
    """Handles recording standardized test audio files."""
    
    def __init__(self, base_dir="test_audio"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.samplerate = 16000  # Match faster-whisper expected rate
        
    def record_test_audio(self, filename: str, duration: int = 30, 
                         prompt: str = None) -> str:
        """Record test audio with user prompts."""
        
        filepath = self.base_dir / filename
        
        if not prompt:
            prompt = "Say 'the quick brown fox jumps over the lazy dog' 5 times with natural pauses"
        
        print(f"\n🎙️  Recording {filename}")
        print(f"Duration: {duration} seconds")
        print(f"Instructions: {prompt}")
        print("\nPress Enter when ready to start recording...")
        input()
        
        print("🔴 Recording started!")
        for i in range(3, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
        print("🎵 GO!")
        
        # Record audio
        audio = sd.rec(int(duration * self.samplerate), 
                      samplerate=self.samplerate, channels=1, dtype='float32')
        
        # Show countdown
        for remaining in range(duration, 0, -5):
            sd.wait(5000)  # Wait 5 seconds
            if remaining > 5:
                print(f"⏰ {remaining-5} seconds remaining...")
        
        sd.wait()  # Wait for recording to finish
        
        # Save audio
        sf.write(str(filepath), audio, self.samplerate)
        print(f"✅ Recording saved to {filepath}")
        print(f"File size: {filepath.stat().st_size / 1024:.1f} KB")
        
        return str(filepath)
    
    def create_test_suite(self) -> Dict[str, str]:
        """Create a complete test suite of recordings."""
        
        recordings = {}
        
        test_scenarios = [
            {
                "filename": "quick_fox_5x_normal.wav",
                "duration": 25,
                "prompt": "Say 'the quick brown fox jumps over the lazy dog' exactly 5 times at normal speaking pace with 2-second pauses"
            },
            {
                "filename": "quick_fox_5x_fast.wav", 
                "duration": 15,
                "prompt": "Say 'the quick brown fox jumps over the lazy dog' exactly 5 times quickly with minimal pauses"
            },
            {
                "filename": "quick_fox_5x_slow.wav",
                "duration": 35, 
                "prompt": "Say 'the quick brown fox jumps over the lazy dog' exactly 5 times slowly and clearly with long pauses"
            },
            {
                "filename": "natural_conversation.wav",
                "duration": 30,
                "prompt": "Have a natural conversation or read some text naturally (not the test phrase)"
            }
        ]
        
        for scenario in test_scenarios:
            filepath = self.record_test_audio(**scenario)
            recordings[scenario["filename"].replace(".wav", "")] = filepath
            
            print(f"\n⏸️  Recorded {scenario['filename']}")
            print("Take a break before the next recording if needed...")
            input("Press Enter to continue to next recording (or Ctrl+C to stop)...")
        
        return recordings


class TranscriptionEvaluator:
    """Evaluates transcription accuracy using multiple metrics."""
    
    def __init__(self):
        self.expected_phrase = "the quick brown fox jumps over the lazy dog"
        self.key_words = ["quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
        self.profanity_indicators = ["fuck", "shit", "damn", "ass", "hell"]  # Add more as needed
    
    def evaluate_transcription_accuracy(self, actual_text: str, 
                                      expected_repetitions: int = 5) -> Dict:
        """Comprehensive transcription evaluation with multiple metrics."""
        
        # Clean and normalize
        actual = actual_text.lower().strip()
        expected = (self.expected_phrase + " ") * expected_repetitions
        expected = expected.strip()
        
        metrics = {
            # Basic info
            "actual_text": actual,
            "expected_text": expected,
            "actual_length": len(actual),
            "expected_length": len(expected),
            
            # Exact matching
            "exact_match": actual == expected,
            
            # Length comparison
            "length_ratio": len(actual) / len(expected) if expected else 0,
            
            # Word-level analysis
            "word_accuracy": self._calculate_word_accuracy(actual, expected),
            "key_words_detected": self._count_key_words_detected(actual),
            
            # Sequence similarity
            "sequence_similarity": SequenceMatcher(None, actual, expected).ratio(),
        }
        
        # Fuzzy matching (if available)
        if FUZZYWUZZY_AVAILABLE:
            metrics.update({
                "fuzzy_ratio": fuzz.ratio(actual, expected),
                "fuzzy_partial": fuzz.partial_ratio(actual, expected),
                "fuzzy_token_sort": fuzz.token_sort_ratio(actual, expected),
                "fuzzy_token_set": fuzz.token_set_ratio(actual, expected),
            })
        
        # Phonetic matching (if available)
        if JELLYFISH_AVAILABLE:
            metrics["phonetic_match"] = jellyfish.jaro_winkler(actual, expected)
        
        # Quality issues
        metrics.update({
            "repetitions_detected": self._count_phrase_repetitions(actual),
            "expected_repetitions": expected_repetitions,
            "repetition_accuracy": abs(expected_repetitions - metrics["repetitions_detected"]) <= 1,
            "profanity_detected": self._check_for_profanity(actual),
            "text_fragmentation": self._measure_fragmentation(actual),
        })
        
        # Overall score
        metrics["overall_score"] = self._calculate_overall_score(metrics)
        
        return metrics
    
    def _calculate_word_accuracy(self, actual: str, expected: str) -> float:
        """Calculate word-level accuracy (similar to WER but simpler)."""
        actual_words = set(actual.split())
        expected_words = set(expected.split())
        
        if not expected_words:
            return 1.0 if not actual_words else 0.0
        
        correct_words = len(actual_words & expected_words)
        total_expected = len(expected_words)
        
        return correct_words / total_expected
    
    def _count_key_words_detected(self, actual: str) -> float:
        """Count what fraction of key content words were detected."""
        detected = sum(1 for word in self.key_words if word in actual)
        return detected / len(self.key_words)
    
    def _count_phrase_repetitions(self, text: str) -> int:
        """Count how many times the target phrase appears."""
        return text.count(self.expected_phrase)
    
    def _check_for_profanity(self, text: str) -> bool:
        """Check if transcription contains profanity (ASR errors)."""
        return any(word in text for word in self.profanity_indicators)
    
    def _measure_fragmentation(self, text: str) -> float:
        """Measure how fragmented the text is (lots of short words/fragments)."""
        words = text.split()
        if not words:
            return 0.0
        
        # Calculate average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Short average word length indicates fragmentation
        # Normal English words average ~4.5 characters
        fragmentation_score = max(0, (4.5 - avg_word_length) / 4.5)
        
        return fragmentation_score
    
    def _calculate_overall_score(self, metrics: Dict) -> float:
        """Calculate composite score (0-100)."""
        
        weights = {
            'key_words_detected': 0.3,      # Most important - content accuracy
            'sequence_similarity': 0.2,      # Structure preservation  
            'word_accuracy': 0.2,           # Word-level accuracy
            'repetition_accuracy': 0.15,    # Correct number of repetitions
            'profanity_penalty': -0.1,      # Penalty for profanity
            'fragmentation_penalty': -0.05  # Penalty for fragmentation
        }
        
        score = 0
        score += metrics.get('key_words_detected', 0) * weights['key_words_detected'] * 100
        score += metrics.get('sequence_similarity', 0) * weights['sequence_similarity'] * 100
        score += metrics.get('word_accuracy', 0) * weights['word_accuracy'] * 100
        score += (1 if metrics.get('repetition_accuracy', False) else 0) * weights['repetition_accuracy'] * 100
        score += metrics.get('profanity_detected', False) * weights['profanity_penalty'] * 100
        score += metrics.get('text_fragmentation', 0) * weights['fragmentation_penalty'] * 100
        
        # Add fuzzy matching if available
        if FUZZYWUZZY_AVAILABLE and 'fuzzy_ratio' in metrics:
            score += metrics['fuzzy_ratio'] * 0.1  # 10% weight for fuzzy matching
        
        return max(0, min(100, score))


class VADTester:
    """Main VAD testing framework."""
    
    def __init__(self, test_audio_dir="test_audio", results_dir="test_results"):
        self.test_audio_dir = Path(test_audio_dir)
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
        self.evaluator = TranscriptionEvaluator()
        self.baseline_results = {}
        
    def run_single_test(self, audio_file: str, vad_params: Dict, 
                       expected_repetitions: int = 5) -> Dict:
        """Run a single VAD test with specific parameters."""
        
        print(f"🧪 Testing with params: {vad_params}")
        
        # Here you would integrate with your actual VAD system
        # For now, this is a placeholder that would call your transcription system
        transcription_result = self._run_transcription_with_params(audio_file, vad_params)
        
        # Evaluate the results
        metrics = self.evaluator.evaluate_transcription_accuracy(
            transcription_result['text'], 
            expected_repetitions
        )
        
        # Add VAD-specific metrics
        metrics.update({
            'vad_params': vad_params,
            'audio_file': audio_file,
            'test_timestamp': datetime.now().isoformat(),
            'processing_time': transcription_result.get('processing_time', 0),
            'segment_count': transcription_result.get('segment_count', 0),
        })
        
        return metrics
    
    def _run_transcription_with_params(self, audio_file: str, vad_params: Dict) -> Dict:
        """Placeholder for actual transcription system integration."""
        
        # This is where you would integrate with your faster_whisper_vad.py system
        # For now, return a mock result
        
        print(f"   Running transcription on {audio_file}")
        print(f"   VAD params: {vad_params}")
        
        # TODO: Replace with actual integration
        mock_result = {
            'text': 'the quick brown fox jumps over the lazy dog ' * 5,  # Mock perfect result
            'processing_time': 2.5,
            'segment_count': 5
        }
        
        return mock_result
    
    def parameter_sweep(self, audio_file: str, quick_test: bool = True) -> List[Dict]:
        """Test different VAD parameter combinations."""
        
        print(f"\n🔬 Starting parameter sweep on {audio_file}")
        
        results = []
        
        if quick_test:
            # Quick test with fewer combinations
            param_combinations = [
                {'aggressiveness': 1, 'start_gate_ms': 200, 'end_gate_ms': 800, 'volume_threshold': 0.008},
                {'aggressiveness': 2, 'start_gate_ms': 300, 'end_gate_ms': 1000, 'volume_threshold': 0.01},
                {'aggressiveness': 3, 'start_gate_ms': 400, 'end_gate_ms': 1200, 'volume_threshold': 0.015},
            ]
        else:
            # Full parameter grid
            aggressiveness_levels = [0, 1, 2, 3]
            start_gates = [200, 300, 500]
            end_gates = [600, 1000, 1500]
            volume_thresholds = [0.005, 0.01, 0.02]
            
            param_combinations = []
            for agg in aggressiveness_levels:
                for start in start_gates:
                    for end in end_gates:
                        for vol in volume_thresholds:
                            param_combinations.append({
                                'aggressiveness': agg,
                                'start_gate_ms': start,
                                'end_gate_ms': end,
                                'volume_threshold': vol
                            })
        
        print(f"Testing {len(param_combinations)} parameter combinations...")
        
        for i, params in enumerate(param_combinations):
            print(f"\nTest {i+1}/{len(param_combinations)}")
            
            try:
                result = self.run_single_test(audio_file, params)
                results.append(result)
                
                print(f"   Score: {result['overall_score']:.1f}")
                print(f"   Key words: {result['key_words_detected']:.2f}")
                
            except Exception as e:
                print(f"   ❌ Test failed: {e}")
                continue
        
        return results
    
    def find_optimal_parameters(self, results: List[Dict]) -> Dict:
        """Find the best performing parameter combination."""
        
        if not results:
            return {}
        
        # Sort by overall score
        best_result = max(results, key=lambda x: x['overall_score'])
        
        print(f"\n🏆 Best performing configuration:")
        print(f"   Overall Score: {best_result['overall_score']:.1f}")
        print(f"   Parameters: {best_result['vad_params']}")
        print(f"   Key Words Detected: {best_result['key_words_detected']:.2f}")
        print(f"   Sequence Similarity: {best_result['sequence_similarity']:.2f}")
        
        return best_result
    
    def save_results(self, results: List[Dict], filename: str = None):
        """Save test results to JSON file."""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vad_test_results_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to {filepath}")
        
        return str(filepath)
    
    def generate_report(self, results: List[Dict]) -> str:
        """Generate a human-readable test report."""
        
        if not results:
            return "No results to report."
        
        report = []
        report.append("# VAD Testing Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Tests Run: {len(results)}")
        report.append("")
        
        # Summary statistics
        scores = [r['overall_score'] for r in results]
        report.append("## Summary Statistics")
        report.append(f"Average Score: {np.mean(scores):.1f}")
        report.append(f"Best Score: {np.max(scores):.1f}") 
        report.append(f"Worst Score: {np.min(scores):.1f}")
        report.append(f"Score StdDev: {np.std(scores):.1f}")
        report.append("")
        
        # Best configuration
        best = max(results, key=lambda x: x['overall_score'])
        report.append("## Best Configuration")
        report.append(f"Score: {best['overall_score']:.1f}")
        for param, value in best['vad_params'].items():
            report.append(f"{param}: {value}")
        report.append("")
        
        # Top 5 configurations
        top_5 = sorted(results, key=lambda x: x['overall_score'], reverse=True)[:5]
        report.append("## Top 5 Configurations")
        for i, result in enumerate(top_5):
            report.append(f"{i+1}. Score: {result['overall_score']:.1f} - {result['vad_params']}")
        report.append("")
        
        return "\n".join(report)


def main():
    """Main function to run VAD testing."""
    
    print("🎯 VAD Testing Framework")
    print("=" * 50)
    
    # Initialize components
    recorder = AudioRecorder()
    tester = VADTester()
    
    # Menu system
    while True:
        print("\nOptions:")
        print("1. Record test audio")
        print("2. Record full test suite")
        print("3. Run VAD parameter sweep (quick)")
        print("4. Run VAD parameter sweep (full)")
        print("5. View previous results")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            filename = input("Audio filename (e.g., test_audio.wav): ").strip()
            if not filename.endswith('.wav'):
                filename += '.wav'
            recorder.record_test_audio(filename)
            
        elif choice == "2":
            print("Recording full test suite...")
            recordings = recorder.create_test_suite()
            print(f"Recorded {len(recordings)} files: {list(recordings.keys())}")
            
        elif choice == "3":
            audio_file = input("Path to test audio file: ").strip()
            if not os.path.exists(audio_file):
                print(f"File not found: {audio_file}")
                continue
                
            results = tester.parameter_sweep(audio_file, quick_test=True)
            best = tester.find_optimal_parameters(results)
            
            # Save results
            results_file = tester.save_results(results)
            
            # Generate report
            report = tester.generate_report(results)
            print(f"\n{report}")
            
        elif choice == "4":
            audio_file = input("Path to test audio file: ").strip()
            if not os.path.exists(audio_file):
                print(f"File not found: {audio_file}")
                continue
                
            print("⚠️  Full parameter sweep will take a long time!")
            confirm = input("Continue? (y/N): ").strip().lower()
            if confirm != 'y':
                continue
                
            results = tester.parameter_sweep(audio_file, quick_test=False)
            best = tester.find_optimal_parameters(results)
            
            # Save results  
            results_file = tester.save_results(results)
            
            # Generate report
            report = tester.generate_report(results)
            print(f"\n{report}")
            
        elif choice == "5":
            results_dir = Path("test_results")
            if not results_dir.exists():
                print("No results directory found.")
                continue
                
            json_files = list(results_dir.glob("*.json"))
            if not json_files:
                print("No result files found.")
                continue
                
            print("Available result files:")
            for i, f in enumerate(json_files):
                print(f"{i+1}. {f.name}")
                
            try:
                file_idx = int(input("Select file number: ")) - 1
                selected_file = json_files[file_idx]
                
                with open(selected_file) as f:
                    results = json.load(f)
                
                report = tester.generate_report(results)
                print(f"\n{report}")
                
            except (ValueError, IndexError, FileNotFoundError) as e:
                print(f"Error loading results: {e}")
                
        elif choice == "6":
            print("Goodbye!")
            break
            
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()