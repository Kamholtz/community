"""
Unit tests for the TextDiffer module.

Tests various scenarios including incremental updates, corrections,
and edge cases that can occur during real-time transcription.
"""

import unittest
from text_differ import TextDiffer


class TestTextDiffer(unittest.TestCase):
    
    def setUp(self):
        """Create a fresh TextDiffer instance for each test."""
        self.differ = TextDiffer()
    
    def test_basic_incremental_typing(self):
        """Test normal incremental transcription updates."""
        # Simulate partial transcriptions getting longer
        delta1 = self.differ.process_transcription("hello")
        self.assertEqual(delta1, "hello")
        self.assertEqual(self.differ.get_typed_context(), "hello")
        
        delta2 = self.differ.process_transcription("hello world")
        self.assertEqual(delta2, " world")
        self.assertEqual(self.differ.get_typed_context(), "hello world")
        
        delta3 = self.differ.process_transcription("hello world testing")
        self.assertEqual(delta3, " testing")
        self.assertEqual(self.differ.get_typed_context(), "hello world testing")
    
    def test_word_correction_scenario(self):
        """Test when a word gets corrected mid-transcription."""
        # Initial partial transcription
        delta1 = self.differ.process_transcription("the quick")
        self.assertEqual(delta1, "the quick")
        
        # Word gets corrected (brown added)
        delta2 = self.differ.process_transcription("the quick brown")
        self.assertEqual(delta2, " brown")
        
        # More words added
        delta3 = self.differ.process_transcription("the quick brown fox")
        self.assertEqual(delta3, " fox")
    
    def test_major_correction_fallback(self):
        """Test fallback behavior when transcription changes significantly."""
        # Initial transcription
        delta1 = self.differ.process_transcription("hello world")
        self.assertEqual(delta1, "hello world")
        
        # Major change - doesn't start with previous text
        delta2 = self.differ.process_transcription("goodbye everyone")
        self.assertEqual(delta2, " goodbye everyone")
        self.assertEqual(self.differ.get_typed_context(), "hello world goodbye everyone")
    
    def test_repeated_text_issue(self):
        """
        Test the specific issue from user feedback where repeated text occurs.
        This simulates the problem with "the quick brown fox" being repeated.
        """
        # Simulate the sequence that caused issues
        transcriptions = [
            "the quick",
            "the quick brown fox",
            "the quick round fox jumps over the light",  # Mishearing
            "the quick brown fox jumps over the lazy dog",  # Correction
            "the quick brown fox jumps over the lazy dog",  # Repeat (shouldn't type anything)
            "the quick brown fox jumps over the lazy dog",  # Another repeat
        ]
        
        results = []
        for transcription in transcriptions:
            delta = self.differ.process_transcription(transcription)
            results.append(delta)
        
        # Check the deltas
        self.assertEqual(results[0], "the quick")
        self.assertEqual(results[1], " brown fox")
        self.assertEqual(results[2], " round fox jumps over the light")  # Fallback due to mismatch
        self.assertEqual(results[3], " the quick brown fox jumps over the lazy dog")  # Fallback
        self.assertEqual(results[4], "")  # No change - should be empty
        self.assertEqual(results[5], "")  # No change - should be empty
    
    def test_empty_and_whitespace_handling(self):
        """Test handling of empty strings and whitespace."""
        # Empty string
        delta1 = self.differ.process_transcription("")
        self.assertEqual(delta1, "")
        
        # Whitespace only
        delta2 = self.differ.process_transcription("   ")
        self.assertEqual(delta2, "")
        
        # First real text
        delta3 = self.differ.process_transcription("hello")
        self.assertEqual(delta3, "hello")
    
    def test_space_and_reset_functionality(self):
        """Test the space addition and context reset at end of utterance."""
        # Type some text
        self.differ.process_transcription("hello world")
        self.assertEqual(self.differ.get_typed_context(), "hello world")
        
        # Add space and reset (end of utterance)
        space = self.differ.add_space_and_reset()
        self.assertEqual(space, " ")
        self.assertEqual(self.differ.get_typed_context(), "")
        
        # Start fresh transcription
        delta = self.differ.process_transcription("new sentence")
        self.assertEqual(delta, "new sentence")
    
    def test_partial_truncation_issue(self):
        """
        Test handling of partial transcriptions that get cut off.
        This simulates "The quick brown fox jumps over..." -> full sentence.
        """
        # Partial transcription (cut off)
        delta1 = self.differ.process_transcription("the quick brown fox jumps over")
        self.assertEqual(delta1, "the quick brown fox jumps over")
        
        # Complete sentence
        delta2 = self.differ.process_transcription("the quick brown fox jumps over the lazy dog")
        self.assertEqual(delta2, " the lazy dog")
    
    def test_punctuation_changes(self):
        """Test when punctuation gets added or corrected."""
        # Initial without punctuation
        delta1 = self.differ.process_transcription("hello world")
        self.assertEqual(delta1, "hello world")
        
        # Punctuation added
        delta2 = self.differ.process_transcription("hello world.")
        self.assertEqual(delta2, ".")
        
        # More text after punctuation
        delta3 = self.differ.process_transcription("hello world. How are you")
        self.assertEqual(delta3, " How are you")
    
    def test_reset_functionality(self):
        """Test manual reset functionality."""
        self.differ.process_transcription("some text")
        self.assertEqual(self.differ.get_typed_context(), "some text")
        
        self.differ.reset()
        self.assertEqual(self.differ.get_typed_context(), "")
        
        # Should work normally after reset
        delta = self.differ.process_transcription("new text")
        self.assertEqual(delta, "new text")
    
    def test_compute_diff_edge_cases(self):
        """Test the compute_diff method directly with edge cases."""
        self.differ.typed_so_far = "hello"
        
        # Normal extension
        delta, should_reset = self.differ.compute_diff("hello world")
        self.assertEqual(delta, " world")
        self.assertFalse(should_reset)
        
        # Complete mismatch
        delta, should_reset = self.differ.compute_diff("goodbye")
        self.assertEqual(delta, " goodbye")
        self.assertTrue(should_reset)
        
        # Empty text
        delta, should_reset = self.differ.compute_diff("")
        self.assertEqual(delta, "")
        self.assertFalse(should_reset)


class TestRealWorldScenarios(unittest.TestCase):
    """Test scenarios based on real-world transcription patterns."""
    
    def setUp(self):
        self.differ = TextDiffer()
    
    def test_user_reported_repetition_bug(self):
        """
        Test the exact scenario reported by the user with repeated phrases.
        This simulates the VAD system creating separate final transcriptions.
        """
        # Each of these represents a separate final transcription from VAD chunks
        final_transcriptions = [
            "the quick brown fox jumps over the lazy dog",
            "the quick brown fox jumps over the lazy dog",  # Identical repeat  
            "the quick brown fox jumps over the lazy dog",  # Another repeat
            "the quick brown fox jumps over the lazy dog",  # Yet another
            "the quick brown fox jumps over the lazy dog",  # And more...
        ]
        
        outputs = []
        for i, transcription in enumerate(final_transcriptions):
            print(f"Processing final transcription[{i}]: '{transcription}'")
            delta = self.differ.process_final_transcription(transcription)
            outputs.append(delta)
            print(f"  -> Output: '{delta}'")
            
            # End utterance after each final transcription (simulate VAD ending)
            space = self.differ.end_utterance()
            print(f"  -> End utterance space: '{space}'")
        
        # First should type the content
        self.assertEqual(outputs[0], "the quick brown fox jumps over the lazy dog")
        # All repeats should produce empty output
        self.assertEqual(outputs[1], "")  # First repeat should be empty
        self.assertEqual(outputs[2], "")  # Second repeat should be empty
        self.assertEqual(outputs[3], "")  # Third repeat should be empty
        self.assertEqual(outputs[4], "")  # Fourth repeat should be empty
    
    def test_vad_chunking_simulation(self):
        """
        Simulate how VAD chunking might create overlapping transcriptions.
        """
        # Start of speech
        delta1 = self.differ.process_transcription("hello")
        
        # VAD continues, more context
        delta2 = self.differ.process_transcription("hello there")
        
        # End of first VAD chunk, space added
        space1 = self.differ.add_space_and_reset()
        
        # New VAD chunk starts
        delta3 = self.differ.process_transcription("how are")
        
        # Final chunk
        delta4 = self.differ.process_transcription("how are you")
        
        # End space
        space2 = self.differ.add_space_and_reset()
        
        expected_full_output = "hello there how are you "
        actual_full_output = delta1 + delta2 + space1 + delta3 + delta4 + space2
        
        self.assertEqual(actual_full_output, expected_full_output)


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)