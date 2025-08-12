# Comprehensive VAD Analysis Report
Generated: 2025-08-12T22:44:20.493414

## Executive Summary
**Overall Score: 69.6/100**

- Word Accuracy: 100.0%
- Sequence Similarity: 53.5%
- Consistency Score: 54.4%
- Vocabulary Overlap: 100.0%

## Text Analysis Results
- Character Count: 321 (expected: 131)
- Word Count: 63 (expected: 27)
- Phrase Repetitions: 4 (expected: 3)

## Text Quality Analysis
- Profanity Detected: ⚠️ YES
- Text Fragments: 0
- Punctuation Errors: 2
- Repeated Patterns: 0
- Capitalization Consistency: 50.0%

## Linguistic Analysis
- Unique Words: 15
- Vocabulary Overlap: 100.0%
- Phonetic Errors: 0
- Bigram Accuracy: 100.0%
- Word Order Violations: 0

## Segmentation Analysis
- Total Segments: 7
- Average Segment Length: 9.1 words
- Short Segments: 1
- Long Segments: 1
- Boundary Quality Score: 85.7%
- Segmentation Consistency: 71.4%

## Error Analysis
- Deletion Errors: 0
- Homophone Errors: 7
- Word Boundary Errors: 0

## Reliability Analysis
- Consistency Score: 54.4%
- Reliability Variance: 0.044

## Optimization Suggestions
- CRITICAL: Audio quality issues detected - check for noise/interference
- Increase VOLUME_THRESHOLD to 0.015-0.02
- Check microphone positioning and room acoustics
- Low consistency between repetitions - check VAD aggressiveness
- Consider adjusting START_GATE_MS for better speech detection

## Actual vs Expected Text

### Actual Output:
```
and fuckFox jumps over. Fox jumps over the lazy dog., the quick brown fox.. The quick brown fox jumps. the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.
```

### Expected Output:
```
the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog 
```

## Technical Data (JSON)
```json
{
  "timestamp": "2025-08-12T22:44:20.493414",
  "audio_file": null,
  "expected_repetitions": 3,
  "actual_text": "and fuckFox jumps over. Fox jumps over the lazy dog., the quick brown fox.. The quick brown fox jumps. the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.",
  "expected_text": "the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog ",
  "character_count": 321,
  "word_count": 63,
  "expected_character_count": 131,
  "expected_word_count": 27,
  "length_ratio": 2.450381679389313,
  "exact_match": false,
  "sequence_similarity": 0.5353982300884956,
  "word_accuracy": 1.0,
  "phrase_repetitions": 4,
  "repetition_accuracy": true,
  "profanity_detected": true,
  "text_fragments": 0,
  "incomplete_words": 1,
  "repeated_patterns": 0,
  "punctuation_errors": 2,
  "sentence_count": 7,
  "avg_sentence_length": 9.142857142857142,
  "capitalization_consistency": 0.5,
  "unique_words": 15,
  "vocabulary_overlap": 1.0,
  "word_frequency_deviation": 1.1458333333333333,
  "phonetic_errors": 0,
  "bigram_accuracy": 1.0,
  "word_order_violations": 0,
  "substitution_errors": 0,
  "insertion_errors": 0,
  "deletion_errors": 0,
  "word_boundary_errors": 0,
  "homophone_errors": 7,
  "concatenation_errors": 0,
  "total_segments": 7,
  "avg_segment_length": 9.142857142857142,
  "short_segments": 1,
  "long_segments": 1,
  "boundary_quality_score": 0.8571428571428571,
  "segmentation_consistency": 0.7142857142857143,
  "consistency_score": 0.54409471641919,
  "reliability_variance": 0.04367756136724246,
  "repetition_quality": [
    0.5538461538461539,
    0.7714285714285715,
    0.59375,
    0.7352941176470589,
    0.5058823529411764,
    1.0,
    1.0
  ],
  "overall_score": 69.58367106234347,
  "optimization_suggestions": [
    "CRITICAL: Audio quality issues detected - check for noise/interference",
    "Increase VOLUME_THRESHOLD to 0.015-0.02",
    "Check microphone positioning and room acoustics",
    "Low consistency between repetitions - check VAD aggressiveness",
    "Consider adjusting START_GATE_MS for better speech detection"
  ]
}
```