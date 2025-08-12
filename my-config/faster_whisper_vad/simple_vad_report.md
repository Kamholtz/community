# Simple VAD Testing Report
Generated: 2025-08-12 22:19:42

## Current System Performance
Overall Score: 73.4/100
Key Words Detected: 100%
Sequence Similarity: 34%
Word Accuracy: 100%
Phrase Repetitions: 10 (expected: 3)

## Actual Output Text
```
and fuckfox jumps over. fox jumps over the lazy dog., the quick brown fox.. the quick brown fox jumps. the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy the quick brown fox jumps over the lazy dog. the quick brown fox jumps over the lazy dog. the quick brown fox jumps over the lazy dog. the quick brown fox jumps over the lazy dog. the quick brown fox jumps over the lazy dog. the quick brown fox jumps over the lazy dog. the quick brown fox jumps over the lazy dog. the quick brown fox jumps over the lazy dog. the quick brown fox jumps over the lazy dog.
```

## Expected Output Text
```
the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog
```

## Performance Assessment
✅ **GOOD** - System performing adequately

## Next Steps
1. Install full dependencies for advanced testing:
   `pip install sounddevice soundfile matplotlib seaborn fuzzywuzzy`
2. Record standardized test audio with the phrase:
   'the quick brown fox jumps over the lazy dog' (3 times)
3. Run comprehensive parameter optimization
4. Generate visual performance dashboards

## Quick Fixes to Try
- Adjust VAD aggressiveness level (try 1 or 3 instead of 2)
- Modify END_GATE_MS (try 800ms or 1200ms)
- Check VOLUME_THRESHOLD (try 0.005-0.02 range)
- Verify audio input quality and microphone setup