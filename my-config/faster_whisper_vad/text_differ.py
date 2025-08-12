"""
Differential text typing module for incremental transcription updates.

This module handles the logic for computing text differences and managing
the typing state without any audio or platform-specific dependencies.
"""

class TextDiffer:
    """Manages differential text typing for real-time transcription."""
    
    def __init__(self):
        self.current_utterance_text = ""  # Text from current partial transcriptions
        self.last_final_text = ""  # Last complete final transcription
    
    def process_partial_transcription(self, full_text):
        """
        Process a partial transcription during an ongoing utterance.
        
        Args:
            full_text (str): The complete transcribed text for current utterance
            
        Returns:
            str: The text that should be typed (delta only)
        """
        if not full_text:
            return ""
            
        full_text = full_text.strip()
        print(f"[PARTIAL] Input: '{full_text}', Current: '{self.current_utterance_text}'")
        
        # Handle exact match - no change
        if full_text == self.current_utterance_text:
            print(f"[PARTIAL] Exact match - no output")
            return ""
        
        # Handle incremental growth (common case)
        if full_text.startswith(self.current_utterance_text):
            delta = full_text[len(self.current_utterance_text):]
            self.current_utterance_text = full_text
            print(f"[PARTIAL] Incremental - outputting: '{delta}'")
            return delta
        
        # Handle corrections within utterance - rare case
        if self.current_utterance_text:
            # For now, we'll just append the difference to prevent text loss
            delta = " " + full_text
            self.current_utterance_text += " " + full_text
            print(f"[PARTIAL] Correction - outputting: '{delta}'")
            return delta
        else:
            # First partial in utterance
            self.current_utterance_text = full_text
            print(f"[PARTIAL] First partial - outputting: '{full_text}'")
            return full_text
    
    def process_final_transcription(self, full_text):
        """
        Process a final transcription at the end of an utterance.
        
        Args:
            full_text (str): The complete final transcribed text
            
        Returns:
            str: The text that should be typed (delta only)
        """
        if not full_text:
            return ""
            
        full_text = full_text.strip()
        print(f"[FINAL] Input: '{full_text}', Current: '{self.current_utterance_text}', Last Final: '{self.last_final_text}'")
        
        # Check if this is identical to the last final transcription (repetition issue)
        if full_text == self.last_final_text:
            print(f"[FINAL] Repetition detected - no output")
            return ""  # Skip repeated final transcriptions
        
        # Check if it's the same as current partial text
        if full_text == self.current_utterance_text:
            # Just finalize, no additional typing needed
            self.last_final_text = full_text
            print(f"[FINAL] Same as partial - no output, just finalized")
            return ""
        
        # Handle case where final differs from partials
        if self.current_utterance_text and full_text.startswith(self.current_utterance_text):
            # Final adds to partials
            delta = full_text[len(self.current_utterance_text):]
            self.last_final_text = full_text
            print(f"[FINAL] Extends partial - outputting: '{delta}'")
            return delta
        
        # Handle major corrections in final
        if self.current_utterance_text:
            # Replace partial with final - this is a correction scenario
            delta = " " + full_text  # Add space before correction
            self.last_final_text = full_text
            print(f"[FINAL] Major correction - outputting: '{delta}'")
            return delta
        else:
            # No partials, just final
            self.last_final_text = full_text
            print(f"[FINAL] No partials - outputting: '{full_text}'")
            return full_text
    
    def end_utterance(self):
        """
        Mark the end of an utterance and reset for next one.
        
        Returns:
            str: A trailing space
        """
        print(f"[END_UTTERANCE] Resetting current utterance: '{self.current_utterance_text}' -> ''")
        self.current_utterance_text = ""
        # Keep last_final_text to prevent repetitions
        return " "
    
    def reset(self):
        """Reset all state - useful for testing or starting fresh."""
        self.current_utterance_text = ""
        self.last_final_text = ""
    
    def get_current_state(self):
        """Get current state for debugging."""
        return {
            "current_utterance": self.current_utterance_text,
            "last_final": self.last_final_text
        }