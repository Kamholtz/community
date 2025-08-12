"""
Simplified VAD Testing Script (no external dependencies)
This version uses only Python built-in libraries for basic VAD testing.
"""

import os
import sys
import json
import time
from pathlib import Path
from difflib import SequenceMatcher
from datetime import datetime

class SimpleVADTester:
    """Simplified VAD tester using only built-in Python libraries."""
    
    def __init__(self):
        self.expected_phrase = "the quick brown fox jumps over the lazy dog"
        self.key_words = ["quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
        
    def evaluate_transcription(self, actual_text, expected_repetitions=5):
        """Evaluate transcription quality using basic metrics."""
        
        actual = actual_text.lower().strip()
        expected = (self.expected_phrase + " ") * expected_repetitions
        expected = expected.strip()
        
        # Basic metrics using only built-in libraries
        metrics = {
            "actual_text": actual,
            "expected_text": expected,
            "actual_length": len(actual),
            "expected_length": len(expected),
            
            # Exact matching
            "exact_match": actual == expected,
            
            # Length comparison
            "length_ratio": len(actual) / len(expected) if expected else 0,
            
            # Sequence similarity (built-in difflib)
            "sequence_similarity": SequenceMatcher(None, actual, expected).ratio(),
            
            # Word-level analysis
            "word_accuracy": self._calculate_word_accuracy(actual, expected),
            "key_words_detected": self._count_key_words(actual),
            
            # Quality checks
            "phrase_repetitions": actual.count(self.expected_phrase),
            "expected_repetitions": expected_repetitions,
            "repetition_accuracy": abs(expected_repetitions - actual.count(self.expected_phrase)) <= 1,
        }
        
        # Calculate overall score
        metrics["overall_score"] = self._calculate_score(metrics)
        
        return metrics
    
    def _calculate_word_accuracy(self, actual, expected):
        """Calculate word-level accuracy."""
        actual_words = set(actual.split())
        expected_words = set(expected.split())
        
        if not expected_words:
            return 1.0 if not actual_words else 0.0
        
        correct_words = len(actual_words & expected_words)
        return correct_words / len(expected_words)
    
    def _count_key_words(self, text):
        """Count fraction of key words detected."""
        detected = sum(1 for word in self.key_words if word in text)
        return detected / len(self.key_words)
    
    def _calculate_score(self, metrics):
        """Calculate overall score (0-100)."""
        score = 0
        score += metrics["key_words_detected"] * 40  # 40% weight
        score += metrics["sequence_similarity"] * 25  # 25% weight  
        score += metrics["word_accuracy"] * 25  # 25% weight
        score += (1 if metrics["repetition_accuracy"] else 0) * 10  # 10% weight
        
        return min(100, max(0, score))

def test_current_vad_output():
    """Test the current VAD output from your system."""
    
    print("🧪 Simple VAD Testing")
    print("=" * 40)
    
    # This is the actual output you reported earlier
    actual_output = """and fuckFox jumps over. Fox jumps over the lazy dog., the quick brown fox.. The quick brown fox jumps. the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog."""
    
    tester = SimpleVADTester()
    results = tester.evaluate_transcription(actual_output, expected_repetitions=5)
    
    print("📊 Current VAD Performance:")
    print(f"   Overall Score: {results['overall_score']:.1f}/100")
    print(f"   Key Words Detected: {results['key_words_detected']:.2f} ({results['key_words_detected']*100:.0f}%)")
    print(f"   Sequence Similarity: {results['sequence_similarity']:.2f} ({results['sequence_similarity']*100:.0f}%)")
    print(f"   Word Accuracy: {results['word_accuracy']:.2f} ({results['word_accuracy']*100:.0f}%)")
    print(f"   Phrase Repetitions: {results['phrase_repetitions']} (expected: {results['expected_repetitions']})")
    print(f"   Exact Match: {'✅' if results['exact_match'] else '❌'}")
    
    # Analysis
    print("\n🔍 Analysis:")
    if results['overall_score'] >= 80:
        print("   ✅ Excellent performance")
    elif results['overall_score'] >= 60:
        print("   ✅ Good performance")
    elif results['overall_score'] >= 40:
        print("   ⚠️  Acceptable performance - some issues detected")
    else:
        print("   ❌ Poor performance - needs optimization")
    
    # Issues detected
    issues = []
    if "fuck" in actual_output.lower():
        issues.append("Profanity detected (ASR transcription error)")
    if results['phrase_repetitions'] > results['expected_repetitions'] + 2:
        issues.append(f"Excessive repetitions ({results['phrase_repetitions']} vs expected {results['expected_repetitions']})")
    if results['key_words_detected'] < 0.8:
        issues.append(f"Low key word detection ({results['key_words_detected']*100:.0f}%)")
    if "fox jumps over. Fox jumps" in actual_output:
        issues.append("Text fragmentation detected")
    
    if issues:
        print("\n⚠️  Issues Found:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if results['overall_score'] < 60:
        print("   • Test different VAD aggressiveness levels (try 1 or 3)")
        print("   • Adjust END_GATE_MS (try 800ms or 1200ms)")
        print("   • Check audio quality and microphone setup")
    if "fuck" in actual_output.lower():
        print("   • Audio quality issue - check for noise/distortion")
        print("   • Try higher VOLUME_THRESHOLD (0.015-0.02)")
    if results['phrase_repetitions'] > results['expected_repetitions'] + 2:
        print("   • The text repetition fix is working but can be improved")
        print("   • Fine-tune the StreamingASRTextDiffer parameters")
    
    return results

def simulate_vad_parameter_test():
    """Simulate testing different VAD parameter combinations."""
    
    print("\n🔬 Simulating VAD Parameter Testing")
    print("=" * 40)
    
    # Simulate different outputs with various parameter combinations
    test_scenarios = [
        {
            "params": {"aggressiveness": 1, "start_gate_ms": 200, "end_gate_ms": 800, "volume_threshold": 0.008},
            "output": "the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog",
            "description": "Low aggressiveness - cleaner output"
        },
        {
            "params": {"aggressiveness": 2, "start_gate_ms": 300, "end_gate_ms": 1000, "volume_threshold": 0.01},
            "output": "quick brown fox jumps over lazy dog quick brown fox jumps over lazy dog quick brown fox jumps over lazy dog quick brown fox jumps over lazy dog quick brown fox jumps over lazy dog",
            "description": "Medium aggressiveness - missing 'the'"
        },
        {
            "params": {"aggressiveness": 3, "start_gate_ms": 400, "end_gate_ms": 1200, "volume_threshold": 0.015},
            "output": "fox jumps lazy dog fox jumps lazy dog fox jumps lazy dog",
            "description": "High aggressiveness - too restrictive"
        }
    ]
    
    tester = SimpleVADTester()
    results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 Test {i}: {scenario['description']}")
        print(f"   Parameters: {scenario['params']}")
        
        metrics = tester.evaluate_transcription(scenario['output'])
        results.append({
            "params": scenario['params'],
            "metrics": metrics,
            "description": scenario['description']
        })
        
        print(f"   Score: {metrics['overall_score']:.1f}/100")
        print(f"   Key Words: {metrics['key_words_detected']*100:.0f}%")
        print(f"   Similarity: {metrics['sequence_similarity']*100:.0f}%")
    
    # Find best configuration
    best = max(results, key=lambda x: x['metrics']['overall_score'])
    print(f"\n🏆 Best Configuration:")
    print(f"   Description: {best['description']}")
    print(f"   Score: {best['metrics']['overall_score']:.1f}/100")
    print(f"   Parameters: {best['params']}")
    
    return results

def create_simple_report(results):
    """Create a simple text report."""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = [
        "# Simple VAD Testing Report",
        f"Generated: {timestamp}",
        "",
        "## Current System Performance",
        f"Overall Score: {results['overall_score']:.1f}/100",
        f"Key Words Detected: {results['key_words_detected']*100:.0f}%",
        f"Sequence Similarity: {results['sequence_similarity']*100:.0f}%", 
        f"Word Accuracy: {results['word_accuracy']*100:.0f}%",
        f"Phrase Repetitions: {results['phrase_repetitions']} (expected: 5)",
        "",
        "## Performance Assessment",
    ]
    
    if results['overall_score'] >= 80:
        report.append("✅ **EXCELLENT** - System performing very well")
    elif results['overall_score'] >= 60:
        report.append("✅ **GOOD** - System performing adequately") 
    elif results['overall_score'] >= 40:
        report.append("⚠️ **ACCEPTABLE** - System has some issues but is functional")
    else:
        report.append("❌ **POOR** - System needs significant optimization")
    
    report.extend([
        "",
        "## Next Steps",
        "1. Install full dependencies for advanced testing:",
        "   `pip install sounddevice soundfile matplotlib seaborn fuzzywuzzy`",
        "2. Record standardized test audio with the phrase:",
        "   'the quick brown fox jumps over the lazy dog' (5 times)",
        "3. Run comprehensive parameter optimization",
        "4. Generate visual performance dashboards",
        "",
        "## Quick Fixes to Try",
        "- Adjust VAD aggressiveness level (try 1 or 3 instead of 2)",
        "- Modify END_GATE_MS (try 800ms or 1200ms)",
        "- Check VOLUME_THRESHOLD (try 0.005-0.02 range)",
        "- Verify audio input quality and microphone setup"
    ])
    
    report_text = "\n".join(report)
    
    # Save report
    with open("simple_vad_report.md", "w") as f:
        f.write(report_text)
    
    print(f"\n📝 Report saved to: simple_vad_report.md")
    
    return report_text

def main():
    """Main function for simple VAD testing."""
    
    print("🎯 Simple VAD Testing (No External Dependencies)")
    print("=" * 60)
    
    # Test current system
    current_results = test_current_vad_output()
    
    # Simulate parameter testing
    simulate_vad_parameter_test()
    
    # Generate report
    create_simple_report(current_results)
    
    print("\n" + "=" * 60)
    print("🎉 Simple VAD Testing Complete!")
    print("\n📋 Summary:")
    print(f"   Current System Score: {current_results['overall_score']:.1f}/100")
    print("   Report: simple_vad_report.md")
    
    print("\n🚀 Next Steps:")
    print("1. Address the issues identified above")
    print("2. Install full dependencies for advanced testing")
    print("3. Record proper test audio")
    print("4. Run comprehensive optimization")

if __name__ == "__main__":
    main()