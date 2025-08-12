#!/usr/bin/env python3
"""
Custom VAD Analysis Script
Analyze your own transcription output with the advanced framework.
"""

from advanced_vad_analyzer_pure import AdvancedVADAnalyzer, create_comprehensive_report

def analyze_custom_output():
    """Analyze your custom transcription output."""
    
    print("🔬 Advanced VAD Analysis - Custom Input")
    print("=" * 50)
    
    # Replace this with your actual transcription output
    your_transcription_output = input("Paste your transcription output here:\n> ")
    
    if not your_transcription_output.strip():
        print("❌ No input provided. Using sample data...")
        your_transcription_output = "the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog"
    
    # How many times did you say the phrase?
    try:
        repetitions = int(input("How many times did you say the phrase? (default: 3): ") or "3")
    except ValueError:
        repetitions = 3
    
    # Analyze
    analyzer = AdvancedVADAnalyzer()
    results = analyzer.comprehensive_analysis(your_transcription_output, expected_repetitions=repetitions)
    
    # Show results
    print(f"\n📊 Analysis Results:")
    print(f"   Overall Score: {results['overall_score']:.1f}/100")
    print(f"   Word Accuracy: {results['word_accuracy']*100:.1f}%")
    print(f"   Sequence Similarity: {results['sequence_similarity']*100:.1f}%")
    print(f"   Phrase Repetitions Found: {results['phrase_repetitions']} (expected: {repetitions})")
    
    # Show issues
    if results.get('profanity_detected'):
        print("   ⚠️  Audio quality issues detected (profanity)")
    if results.get('text_fragments', 0) > 0:
        print(f"   ⚠️  Text fragmentation: {results['text_fragments']} fragments")
    
    # Show top suggestions
    if results['optimization_suggestions']:
        print(f"\n💡 Top Optimization Suggestions:")
        for i, suggestion in enumerate(results['optimization_suggestions'][:3], 1):
            print(f"   {i}. {suggestion}")
    
    # Create detailed report
    report_file = create_comprehensive_report(results, "my_vad_analysis.json")
    print(f"\n📄 Detailed report: {report_file}")
    
    return results

if __name__ == "__main__":
    analyze_custom_output()