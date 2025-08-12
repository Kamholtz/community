"""
Research and testing of existing text diffing libraries for real-time transcription.

Libraries to evaluate:
1. difflib (built-in) - SequenceMatcher for finding longest common subsequence
2. python-diff-match-patch - Google's diff-match-patch library
3. rapidfuzz - Fast string matching/diffing
"""

import difflib
from difflib import SequenceMatcher

def test_difflib_approach():
    """Test using Python's built-in difflib for text diffing."""
    print("=== Testing difflib approach ===")
    
    # Simulate the repetition scenario
    typed_so_far = ""
    transcriptions = [
        "quick brown",
        "quick brown fox", 
        "quick brown fox jumps",
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",  # Repeat
        "The quick brown fox jumps over the lazy dog",  # Repeat
    ]
    
    for i, new_text in enumerate(transcriptions):
        print(f"\nStep {i+1}: Processing '{new_text}'")
        print(f"  Current typed: '{typed_so_far}'")
        
        # Check for exact match (repetition)
        if new_text == typed_so_far:
            print(f"  -> Exact match, no output")
            continue
            
        # Use SequenceMatcher to find the common prefix
        matcher = SequenceMatcher(None, typed_so_far, new_text)
        match = matcher.find_longest_match(0, len(typed_so_far), 0, len(new_text))
        
        if match.size > 0 and match.a == 0 and match.b == 0:
            # Common prefix found at start
            common_len = match.size
            if new_text.startswith(typed_so_far):
                # Simple incremental case
                delta = new_text[len(typed_so_far):]
                print(f"  -> Incremental: '{delta}'")
                typed_so_far = new_text
            else:
                # More complex diff needed
                delta = new_text[common_len:]
                print(f"  -> After common part: '{delta}'")
                typed_so_far = new_text
        else:
            # No common prefix, major change
            if typed_so_far:
                delta = " " + new_text
                print(f"  -> Major change: '{delta}'")
                typed_so_far += delta.strip()
            else:
                delta = new_text
                print(f"  -> First text: '{delta}'")
                typed_so_far = new_text

def test_simple_lcs_approach():
    """Test using Longest Common Subsequence approach."""
    print("\n\n=== Testing simple LCS approach ===")
    
    def find_lcs_prefix(s1, s2):
        """Find longest common prefix between two strings."""
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return i
    
    typed_so_far = ""
    last_final = ""  # Track last final transcription for repetition detection
    
    test_cases = [
        ("partial", "quick brown"),
        ("partial", "quick brown fox"),
        ("final", "The quick brown fox jumps over the lazy dog"),
        ("final", "The quick brown fox jumps over the lazy dog"),  # Repeat
        ("final", "The quick brown fox jumps over the lazy dog"),  # Repeat
    ]
    
    for i, (ttype, new_text) in enumerate(test_cases):
        print(f"\nStep {i+1}: {ttype.upper()} - '{new_text}'")
        print(f"  Current typed: '{typed_so_far}'")
        print(f"  Last final: '{last_final}'")
        
        if ttype == "final":
            # Check for repetition of final transcriptions
            if new_text == last_final:
                print(f"  -> Final repetition detected, no output")
                continue
            last_final = new_text
        
        # Check for exact match
        if new_text == typed_so_far:
            print(f"  -> Exact match, no output")
            continue
            
        # Find common prefix
        common_len = find_lcs_prefix(typed_so_far, new_text)
        
        if common_len == len(typed_so_far) and new_text.startswith(typed_so_far):
            # Simple incremental addition
            delta = new_text[len(typed_so_far):]
            print(f"  -> Incremental addition: '{delta}'")
            typed_so_far = new_text
        elif common_len > 0:
            # Partial match, some correction
            delta = new_text[common_len:]
            print(f"  -> Partial correction from pos {common_len}: '{delta}'")
            typed_so_far = new_text[:common_len] + delta
        else:
            # No common prefix, major change
            if typed_so_far:
                delta = " " + new_text
                print(f"  -> Major change: '{delta}'")
                typed_so_far += delta
            else:
                delta = new_text
                print(f"  -> First text: '{delta}'")
                typed_so_far = new_text

def test_real_world_patterns():
    """Test patterns observed in the actual transcription output."""
    print("\n\n=== Testing real-world patterns ===")
    
    # This is the actual pattern from the user's output
    real_sequence = [
        "quick brown",  # partial
        "quick brown fox jumps",  # partial
        "The quick brown fox jumps over the lazy to-",  # partial (cut off)
        "The quick brown fox jumps over the lazy dog",  # final
        "The quick brown fox jumps over the lazy dog",  # final (repeat)
        "The quick brown fox",  # new partial (new utterance)
        "The quick brown fox jumps over the lazy dog",  # final
        # ... more repeats
    ]
    
    current_utterance = ""
    last_final = ""
    
    for i, text in enumerate(real_sequence):
        print(f"\nProcessing[{i}]: '{text}'")
        
        # Heuristic: if it's much shorter than last final, it's probably a new partial
        is_likely_new_utterance = last_final and len(text) < len(last_final) * 0.7
        
        if is_likely_new_utterance:
            print(f"  -> Likely new utterance (shorter than last final)")
            current_utterance = ""  # Reset for new utterance
            
        # Check for exact repetition of final transcription
        if text == last_final:
            print(f"  -> Exact repetition of last final - SKIP")
            continue
            
        # Check if it's incremental from current utterance
        if current_utterance and text.startswith(current_utterance):
            delta = text[len(current_utterance):]
            print(f"  -> Incremental from current utterance: '{delta}'")
            current_utterance = text
        else:
            # New or corrected text
            if current_utterance:
                delta = " " + text
                print(f"  -> Correction/new text: '{delta}'")
            else:
                delta = text
                print(f"  -> First in utterance: '{delta}'")
            current_utterance = text
            
        # Assume longer texts are "final" transcriptions
        if len(text) > 30:  # Heuristic threshold
            last_final = text
            print(f"  -> Marked as final transcription")

if __name__ == "__main__":
    test_difflib_approach()
    test_simple_lcs_approach()
    test_real_world_patterns()