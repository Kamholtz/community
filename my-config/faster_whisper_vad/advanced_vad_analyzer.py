#!/usr/bin/env python3
"""
Advanced VAD and ASR Analysis Framework
Comprehensive metrics and feedback for optimizing speech recognition performance.
"""

import os
import re
import json
import time
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from difflib import SequenceMatcher
import statistics

class AdvancedVADAnalyzer:
    """Advanced analyzer for VAD and ASR performance with comprehensive metrics."""
    
    def __init__(self):
        self.expected_phrase = "the quick brown fox jumps over the lazy dog"
        self.key_words = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
        self.phonetically_similar = {
            "quick": ["kick", "thick", "click"],
            "brown": ["grown", "crown", "shown"],
            "fox": ["box", "rocks", "socks"],
            "jumps": ["dumps", "bumps", "pumps"],
            "over": ["ever", "hover", "cover"],
            "lazy": ["crazy", "hazy", "daisy"],
            "dog": ["log", "fog", "hog"]
        }
        
    def comprehensive_analysis(self, actual_text, expected_repetitions=3, audio_file=None):
        """Perform comprehensive analysis of ASR output."""
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "audio_file": audio_file,
            "expected_repetitions": expected_repetitions,
            "actual_text": actual_text,
            "expected_text": (self.expected_phrase + " ") * expected_repetitions,
        }
        
        # Core metrics
        results.update(self._basic_metrics(actual_text, expected_repetitions))
        
        # Advanced text analysis
        results.update(self._text_quality_analysis(actual_text))
        
        # Linguistic analysis
        results.update(self._linguistic_analysis(actual_text))
        
        # Error categorization
        results.update(self._error_analysis(actual_text, expected_repetitions))
        
        # Timing and segmentation analysis
        results.update(self._segmentation_analysis(actual_text))
        
        # Confidence and reliability metrics
        results.update(self._reliability_metrics(actual_text, expected_repetitions))
        
        # Audio-specific metrics (if audio file provided)
        if audio_file and os.path.exists(audio_file):
            results.update(self._audio_analysis(audio_file))
        
        # Overall scoring
        results["overall_score"] = self._calculate_comprehensive_score(results)
        results["optimization_suggestions"] = self._generate_suggestions(results)
        
        return results
    
    def _basic_metrics(self, actual_text, expected_repetitions):
        """Basic accuracy and similarity metrics."""
        actual = actual_text.lower().strip()
        expected = (self.expected_phrase + " ") * expected_repetitions
        expected = expected.strip()
        
        return {
            "character_count": len(actual),
            "word_count": len(actual.split()),
            "expected_character_count": len(expected),
            "expected_word_count": len(expected.split()),
            "length_ratio": len(actual) / len(expected) if expected else 0,
            "exact_match": actual == expected,
            "sequence_similarity": SequenceMatcher(None, actual, expected).ratio(),
            "word_accuracy": self._word_level_accuracy(actual, expected),
            "phrase_repetitions": actual.count(self.expected_phrase),
            "repetition_accuracy": abs(expected_repetitions - actual.count(self.expected_phrase)) <= 1,
        }
    
    def _text_quality_analysis(self, actual_text):
        """Analyze text quality issues."""
        actual = actual_text.lower()
        
        # Detect common ASR errors
        profanity_detected = bool(re.search(r'\b(fuck|shit|damn|hell)\b', actual))
        fragments = len(re.findall(r'\b\w{1,2}\b\.', actual))  # Short word fragments
        incomplete_words = len(re.findall(r'\w+\.{2,}', actual))  # Word...
        repeated_patterns = self._detect_repetition_patterns(actual)
        punctuation_errors = len(re.findall(r'[,\.]{2,}', actual))
        
        # Text coherence
        sentences = [s.strip() for s in re.split(r'[.!?]+', actual) if s.strip()]
        avg_sentence_length = np.mean([len(s.split()) for s in sentences]) if sentences else 0
        
        return {
            "profanity_detected": profanity_detected,
            "text_fragments": fragments,
            "incomplete_words": incomplete_words,
            "repeated_patterns": repeated_patterns,
            "punctuation_errors": punctuation_errors,
            "sentence_count": len(sentences),
            "avg_sentence_length": avg_sentence_length,
            "capitalization_consistency": self._check_capitalization(actual_text),
        }
    
    def _linguistic_analysis(self, actual_text):
        """Analyze linguistic patterns and errors."""
        actual_words = actual_text.lower().split()
        expected_words = (self.expected_phrase + " ") * 3  # Use 3 as default
        expected_words = expected_words.strip().split()
        
        # Word frequency analysis
        word_freq = Counter(actual_words)
        expected_freq = Counter(expected_words)
        
        # Phonetic substitution analysis
        phonetic_errors = self._detect_phonetic_errors(actual_words)
        
        # N-gram analysis
        bigrams_actual = self._get_ngrams(actual_words, 2)
        bigrams_expected = self._get_ngrams(expected_words, 2)
        bigram_accuracy = len(set(bigrams_actual) & set(bigrams_expected)) / len(set(bigrams_expected)) if bigrams_expected else 0
        
        return {
            "unique_words": len(set(actual_words)),
            "vocabulary_overlap": len(set(actual_words) & set(expected_words)) / len(set(expected_words)) if expected_words else 0,
            "word_frequency_deviation": self._calculate_frequency_deviation(word_freq, expected_freq),
            "phonetic_errors": phonetic_errors,
            "bigram_accuracy": bigram_accuracy,
            "word_order_violations": self._count_word_order_violations(actual_words, expected_words),
        }
    
    def _error_analysis(self, actual_text, expected_repetitions):
        """Categorize and analyze different types of errors."""
        actual_words = actual_text.lower().split()
        expected_words = (self.expected_phrase + " ") * expected_repetitions
        expected_words = expected_words.strip().split()
        
        errors = {
            "substitution_errors": 0,
            "insertion_errors": 0,
            "deletion_errors": 0,
            "word_boundary_errors": 0,
            "homophone_errors": 0,
            "concatenation_errors": 0,
        }
        
        # Simple error detection (could be enhanced with edit distance)
        for expected_word in self.key_words:
            if expected_word not in actual_words:
                errors["deletion_errors"] += 1
        
        # Check for homophones and similar-sounding words
        for word in actual_words:
            if word in [item for sublist in self.phonetically_similar.values() for item in sublist]:
                errors["homophone_errors"] += 1
        
        # Word boundary issues (compound words split incorrectly)
        compound_patterns = re.findall(r'\b\w+ \w+\b', actual_text)
        for pattern in compound_patterns:
            if pattern.replace(' ', '') in self.expected_phrase:
                errors["word_boundary_errors"] += 1
        
        return errors
    
    def _segmentation_analysis(self, actual_text):
        """Analyze VAD segmentation quality."""
        sentences = [s.strip() for s in re.split(r'[.!?]+', actual_text) if s.strip()]
        
        # Analyze sentence boundaries
        boundary_quality = []
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 0:
                # Check if sentence starts/ends with expected phrase words
                starts_well = words[0].lower() in self.key_words
                ends_well = words[-1].lower() in self.key_words
                boundary_quality.append((starts_well, ends_well))
        
        # Detect over-segmentation (too many short segments)
        short_segments = len([s for s in sentences if len(s.split()) < 5])
        
        # Detect under-segmentation (very long segments)
        long_segments = len([s for s in sentences if len(s.split()) > 15])
        
        return {
            "total_segments": len(sentences),
            "avg_segment_length": np.mean([len(s.split()) for s in sentences]) if sentences else 0,
            "short_segments": short_segments,
            "long_segments": long_segments,
            "boundary_quality_score": np.mean([sum(bq)/2 for bq in boundary_quality]) if boundary_quality else 0,
            "segmentation_consistency": 1.0 - (short_segments + long_segments) / max(len(sentences), 1),
        }
    
    def _reliability_metrics(self, actual_text, expected_repetitions):
        """Calculate reliability and consistency metrics."""
        repetitions = []
        
        # Extract individual repetitions
        sentences = [s.strip() for s in re.split(r'[.!?]+', actual_text) if s.strip()]
        for sentence in sentences:
            if any(word in sentence.lower() for word in ["quick", "fox", "brown"]):
                repetitions.append(sentence.lower())
        
        if len(repetitions) < 2:
            return {"consistency_score": 0, "reliability_variance": 1.0, "repetition_quality": []}
        
        # Calculate consistency between repetitions
        consistency_scores = []
        for i in range(len(repetitions)):
            for j in range(i+1, len(repetitions)):
                similarity = SequenceMatcher(None, repetitions[i], repetitions[j]).ratio()
                consistency_scores.append(similarity)
        
        return {
            "consistency_score": np.mean(consistency_scores) if consistency_scores else 0,
            "reliability_variance": np.var(consistency_scores) if consistency_scores else 1.0,
            "repetition_quality": [self._rate_repetition_quality(rep) for rep in repetitions],
        }
    
    def _audio_analysis(self, audio_file):
        """Analyze audio file properties (basic implementation)."""
        try:
            # Basic file analysis
            file_size = os.path.getsize(audio_file)
            
            # Estimate duration based on WAV format (rough calculation)
            # For 16kHz mono WAV: ~32KB per second
            estimated_duration = file_size / 32000  # Very rough estimate
            
            return {
                "audio_file_size": file_size,
                "estimated_duration": estimated_duration,
                "audio_quality_estimated": "good" if file_size > 100000 else "poor",
            }
        except Exception as e:
            return {"audio_analysis_error": str(e)}
    
    def _calculate_comprehensive_score(self, results):
        """Calculate comprehensive performance score."""
        weights = {
            "sequence_similarity": 20,
            "word_accuracy": 20,
            "consistency_score": 15,
            "vocabulary_overlap": 10,
            "bigram_accuracy": 10,
            "boundary_quality_score": 10,
            "segmentation_consistency": 10,
            "repetition_accuracy": 5,
        }
        
        score = 0
        total_weight = 0
        
        for metric, weight in weights.items():
            if metric in results and results[metric] is not None:
                if metric == "repetition_accuracy":
                    score += weight if results[metric] else 0
                else:
                    score += results[metric] * weight
                total_weight += weight
        
        # Penalties for serious issues
        penalties = 0
        if results.get("profanity_detected", False):
            penalties += 10
        if results.get("text_fragments", 0) > 3:
            penalties += 5
        if results.get("punctuation_errors", 0) > 2:
            penalties += 3
        
        final_score = (score / total_weight * 100) - penalties if total_weight > 0 else 0
        return max(0, min(100, final_score))
    
    def _generate_suggestions(self, results):
        """Generate optimization suggestions based on analysis."""
        suggestions = []
        
        # Audio quality issues
        if results.get("profanity_detected", False):
            suggestions.append("CRITICAL: Audio quality issues detected - check for noise/interference")
            suggestions.append("Increase VOLUME_THRESHOLD to 0.015-0.02")
            suggestions.append("Check microphone positioning and room acoustics")
        
        # Segmentation issues
        if results.get("short_segments", 0) > 2:
            suggestions.append("Over-segmentation detected - increase END_GATE_MS to 1000-1200ms")
        elif results.get("long_segments", 0) > 1:
            suggestions.append("Under-segmentation detected - decrease END_GATE_MS to 600-800ms")
        
        # Accuracy issues
        if results.get("word_accuracy", 0) < 0.8:
            suggestions.append("Low word accuracy - try different model size (medium or large)")
            suggestions.append("Check audio input quality and reduce background noise")
        
        # Consistency issues
        if results.get("consistency_score", 0) < 0.7:
            suggestions.append("Low consistency between repetitions - check VAD aggressiveness")
            suggestions.append("Consider adjusting START_GATE_MS for better speech detection")
        
        # Text quality issues
        if results.get("text_fragments", 0) > 0:
            suggestions.append("Text fragmentation detected - adjust beam search parameters")
        
        if results.get("repetition_accuracy", True) == False:
            suggestions.append("Repetition count mismatch - fine-tune VAD gate parameters")
        
        return suggestions
    
    # Helper methods
    def _word_level_accuracy(self, actual, expected):
        """Calculate word-level accuracy."""
        actual_words = set(actual.split())
        expected_words = set(expected.split())
        if not expected_words:
            return 1.0 if not actual_words else 0.0
        return len(actual_words & expected_words) / len(expected_words)
    
    def _detect_repetition_patterns(self, text):
        """Detect unwanted repetition patterns."""
        words = text.split()
        patterns = 0
        for i in range(len(words) - 2):
            if words[i] == words[i+1] == words[i+2]:
                patterns += 1
        return patterns
    
    def _check_capitalization(self, text):
        """Check capitalization consistency."""
        sentences = re.split(r'[.!?]+', text)
        consistent = 0
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence[0].isupper():
                consistent += 1
        return consistent / max(len(sentences), 1)
    
    def _get_ngrams(self, words, n):
        """Generate n-grams from word list."""
        return [tuple(words[i:i+n]) for i in range(len(words)-n+1)]
    
    def _detect_phonetic_errors(self, actual_words):
        """Detect phonetically similar substitutions."""
        errors = 0
        for word in actual_words:
            for correct_word, similar_words in self.phonetically_similar.items():
                if word in similar_words and correct_word not in actual_words:
                    errors += 1
        return errors
    
    def _calculate_frequency_deviation(self, actual_freq, expected_freq):
        """Calculate deviation in word frequencies."""
        deviations = []
        for word in expected_freq:
            expected_count = expected_freq[word]
            actual_count = actual_freq.get(word, 0)
            if expected_count > 0:
                deviation = abs(actual_count - expected_count) / expected_count
                deviations.append(deviation)
        return np.mean(deviations) if deviations else 1.0
    
    def _count_word_order_violations(self, actual_words, expected_words):
        """Count word order violations."""
        violations = 0
        # Simple implementation - could be enhanced
        expected_pairs = [(expected_words[i], expected_words[i+1]) 
                         for i in range(len(expected_words)-1)]
        actual_pairs = [(actual_words[i], actual_words[i+1]) 
                       for i in range(len(actual_words)-1)]
        
        for pair in expected_pairs:
            if pair not in actual_pairs:
                violations += 1
        
        return violations
    
    def _rate_repetition_quality(self, repetition):
        """Rate the quality of a single repetition."""
        similarity = SequenceMatcher(None, repetition, self.expected_phrase).ratio()
        return similarity

def create_comprehensive_report(analysis_results, output_file="comprehensive_vad_report.json"):
    """Create comprehensive analysis report."""
    
    # Save detailed JSON report
    with open(output_file, 'w') as f:
        json.dump(analysis_results, f, indent=2, default=str)
    
    # Create human-readable summary
    markdown_file = output_file.replace('.json', '.md')
    
    report_lines = [
        "# Comprehensive VAD Analysis Report",
        f"Generated: {analysis_results['timestamp']}",
        "",
        "## Executive Summary",
        f"**Overall Score: {analysis_results['overall_score']:.1f}/100**",
        "",
        f"- Word Accuracy: {analysis_results['word_accuracy']*100:.1f}%",
        f"- Sequence Similarity: {analysis_results['sequence_similarity']*100:.1f}%",
        f"- Consistency Score: {analysis_results['consistency_score']*100:.1f}%",
        f"- Vocabulary Overlap: {analysis_results['vocabulary_overlap']*100:.1f}%",
        "",
        "## Text Quality Analysis",
        f"- Profanity Detected: {'⚠️ YES' if analysis_results['profanity_detected'] else '✅ No'}",
        f"- Text Fragments: {analysis_results['text_fragments']}",
        f"- Punctuation Errors: {analysis_results['punctuation_errors']}",
        f"- Repeated Patterns: {analysis_results['repeated_patterns']}",
        "",
        "## Segmentation Analysis", 
        f"- Total Segments: {analysis_results['total_segments']}",
        f"- Average Segment Length: {analysis_results['avg_segment_length']:.1f} words",
        f"- Boundary Quality Score: {analysis_results['boundary_quality_score']*100:.1f}%",
        f"- Segmentation Consistency: {analysis_results['segmentation_consistency']*100:.1f}%",
        "",
        "## Error Analysis",
        f"- Phonetic Errors: {analysis_results['phonetic_errors']}",
        f"- Word Order Violations: {analysis_results['word_order_violations']}",
        f"- Deletion Errors: {analysis_results['deletion_errors']}",
        f"- Homophone Errors: {analysis_results['homophone_errors']}",
        "",
        "## Optimization Suggestions",
    ]
    
    for suggestion in analysis_results['optimization_suggestions']:
        report_lines.append(f"- {suggestion}")
    
    report_lines.extend([
        "",
        "## Raw Data",
        "```json",
        json.dumps(analysis_results, indent=2, default=str),
        "```"
    ])
    
    with open(markdown_file, 'w') as f:
        f.write('\n'.join(report_lines))
    
    print(f"📊 Comprehensive report saved:")
    print(f"   JSON: {output_file}")
    print(f"   Markdown: {markdown_file}")
    
    return markdown_file

def main():
    """Main function for comprehensive analysis."""
    
    # Test with the sample output
    sample_output = """and fuckFox jumps over. Fox jumps over the lazy dog., the quick brown fox.. The quick brown fox jumps. the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog."""
    
    analyzer = AdvancedVADAnalyzer()
    
    print("🔬 Running Comprehensive VAD Analysis...")
    print("=" * 60)
    
    results = analyzer.comprehensive_analysis(sample_output, expected_repetitions=3)
    
    print(f"📊 Overall Score: {results['overall_score']:.1f}/100")
    print(f"🎯 Key Metrics:")
    print(f"   Word Accuracy: {results['word_accuracy']*100:.1f}%")
    print(f"   Sequence Similarity: {results['sequence_similarity']*100:.1f}%")
    print(f"   Consistency: {results['consistency_score']*100:.1f}%")
    print(f"   Vocabulary Overlap: {results['vocabulary_overlap']*100:.1f}%")
    
    if results['optimization_suggestions']:
        print(f"\n💡 Top Suggestions:")
        for i, suggestion in enumerate(results['optimization_suggestions'][:3], 1):
            print(f"   {i}. {suggestion}")
    
    # Create comprehensive report
    report_file = create_comprehensive_report(results)
    
    print(f"\n✅ Analysis complete! Check {report_file} for full details.")

if __name__ == "__main__":
    main()