"""
Improved text diffing for real-time ASR with proper partial/final hypothesis handling.
Based on research into streaming speech recognition patterns.
"""

class StreamingASRTextDiffer:
    """
    Handles incremental text output for streaming ASR systems.
    
    Key concepts:
    - Partial hypotheses: intermediate results that grow incrementally
    - Final hypotheses: completed transcriptions that should not repeat
    - Text deltas: only output the new/changed portion
    """
    
    def __init__(self):
        self.current_partial = ""  # Current partial hypothesis text
        self.last_final = ""      # Last completed final hypothesis (for dedup)
        self.debug = False        # Disable debug output for cleaner logs
        
    def _debug_print(self, message):
        if self.debug:
            print(f"[ASR_DIFFER] {message}")
    
    def process_partial_hypothesis(self, text):
        """
        Process a partial (intermediate) hypothesis from ASR.
        These typically grow incrementally: "hello" -> "hello world" -> "hello world test"
        
        Args:
            text (str): The current partial transcription
            
        Returns:
            str: Text to output (delta only)
        """
        if not text:
            return ""
            
        text = text.strip()
        self._debug_print(f"PARTIAL: '{text}' (current: '{self.current_partial}')")
        
        # Exact match - no change
        if text == self.current_partial:
            self._debug_print("PARTIAL: No change")
            return ""
        
        # Common case: incremental growth
        if text.startswith(self.current_partial):
            delta = text[len(self.current_partial):]
            self.current_partial = text
            self._debug_print(f"PARTIAL: Incremental -> '{delta}'")
            return delta
        
        # Partial correction (less common)
        # Find longest common prefix
        common_len = 0
        while (common_len < len(self.current_partial) and 
               common_len < len(text) and
               self.current_partial[common_len] == text[common_len]):
            common_len += 1
        
        if common_len > 0:
            # Some common prefix exists - output the different part
            delta = text[common_len:]
            self.current_partial = text
            self._debug_print(f"PARTIAL: Correction from pos {common_len} -> '{delta}'")
            return delta
        
        # Completely different - major correction
        if self.current_partial:
            delta = " " + text
            self.current_partial = text
            self._debug_print(f"PARTIAL: Major change -> '{delta}'")
            return delta
        else:
            # First partial in utterance
            self.current_partial = text
            self._debug_print(f"PARTIAL: First -> '{text}'")
            return text
    
    def process_final_hypothesis(self, text):
        """
        Process a final (completed) hypothesis from ASR.
        These should not repeat - if we see the same final twice, ignore it.
        
        Args:
            text (str): The final transcription
            
        Returns:
            str: Text to output (delta only)
        """
        if not text:
            return ""
            
        text = text.strip()
        self._debug_print(f"FINAL: '{text}' (current: '{self.current_partial}', last_final: '{self.last_final}')")
        
        # CRITICAL: Check for exact repetition of final hypothesis
        if text == self.last_final:
            self._debug_print("FINAL: Exact repetition - SKIP")
            return ""
        
        # Update last final to prevent future repeats
        self.last_final = text
        
        # Case 1: Final is same as current partial (no additional output needed)
        if text == self.current_partial:
            self._debug_print("FINAL: Same as partial - no additional output")
            return ""
        
        # Case 2: Final extends the current partial
        if self.current_partial and text.startswith(self.current_partial):
            delta = text[len(self.current_partial):]
            self._debug_print(f"FINAL: Extends partial -> '{delta}'")
            return delta
        
        # Case 3: Final is completely different from partial (correction)
        if self.current_partial:
            delta = " " + text
            self._debug_print(f"FINAL: Correction -> '{delta}'")
            return delta
        
        # Case 4: No partial, just final (shouldn't happen in normal flow)
        self._debug_print(f"FINAL: No partial context -> '{text}'")
        return text
    
    def end_utterance(self):
        """
        Mark the end of an utterance. Reset partial state but keep final for deduplication.
        
        Returns:
            str: Trailing space character
        """
        self._debug_print(f"END_UTTERANCE: Resetting partial '{self.current_partial}' -> ''")
        self.current_partial = ""
        return " "
    
    def reset_all(self):
        """Reset all state (for testing or restart)."""
        self.current_partial = ""
        self.last_final = ""
        self._debug_print("RESET: All state cleared")
    
    def get_state(self):
        """Get current state for debugging."""
        return {
            "current_partial": self.current_partial,
            "last_final": self.last_final
        }