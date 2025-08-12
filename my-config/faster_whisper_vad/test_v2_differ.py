 """
Test the improved text differ with the exact user scenario.
"""

from text_differ_v2 import StreamingASRTextDiffer

def test_user_repetition_scenario():
    """Test with the exact pattern the user experienced."""
    differ = StreamingASRTextDiffer()

    # Simulate the exact sequence from user's output
    sequence = [
        ("partial", "quick brown"),
        ("partial", "quick brown fox jumps"),
        ("partial", "The quick brown fox jumps over the lazy to-"),
        ("final", "The quick brown fox jumps over the lazy dog"),
        ("end_utterance", None),

        # This is where the repetition problem starts
        ("final", "The quick brown fox jumps over the lazy dog"),  # Should be skipped
        ("end_utterance", None),

        ("partial", "The quick brown fox"),
        ("final", "The quick brown fox jumps over the lazy dog"),  # Should be skipped (repeat)
        ("end_utterance", None),

        ("final", "The quick brown fox jumps over the lazy dog"),  # Should be skipped (repeat)
        ("end_utterance", None),

        # More repeats...
        ("final", "The quick brown fox jumps over the lazy dog"),  # Should be skipped
        ("final", "The quick brown fox jumps over the lazy dog"),  # Should be skipped
        ("final", "The quick brown fox jumps over the lazy dog"),  # Should be skipped
    ]

    print("=== Testing User Repetition Scenario ===")
    outputs = []

    for i, (action_type, text) in enumerate(sequence):
        print(f"\nStep {i+1}: {action_type.upper()}")

        if action_type == "partial":
            result = differ.process_partial_hypothesis(text)
        elif action_type == "final":
            result = differ.process_final_hypothesis(text)
        elif action_type == "end_utterance":
            result = differ.end_utterance()

        outputs.append(result)
        print(f"  Output: '{result}'")

    print(f"\n=== Results ===")
    full_output = "".join(outputs)
    print(f"Full reconstructed output: '{full_output}'")

    # Count repetitions
    repetitions = full_output.count("The quick brown fox jumps over the lazy dog")
    print(f"Number of complete phrase repetitions: {repetitions}")
    print(f"Expected: 1, Actual: {repetitions}")

    return repetitions == 1

def test_incremental_growth():
    """Test normal incremental partial hypothesis growth."""
    differ = StreamingASRTextDiffer()

    sequence = [
        ("partial", "hello"),
        ("partial", "hello world"),
        ("partial", "hello world this"),
        ("partial", "hello world this is"),
        ("final", "hello world this is a test"),
        ("end_utterance", None)
    ]

    print("\n\n=== Testing Incremental Growth ===")
    outputs = []

    for action_type, text in sequence:
        if action_type == "partial":
            result = differ.process_partial_hypothesis(text)
        elif action_type == "final":
            result = differ.process_final_hypothesis(text)
        elif action_type == "end_utterance":
            result = differ.end_utterance()

        outputs.append(result)
        print(f"{action_type.upper()}: '{text}' -> '{result}'")

    full_output = "".join(outputs)
    print(f"Full output: '{full_output}'")
    expected = "hello world this is a test "
    print(f"Expected: '{expected}'")
    print(f"Match: {full_output == expected}")

    return full_output == expected

if __name__ == "__main__":
    print("Testing improved ASR text differ...")

    test1_passed = test_user_repetition_scenario()
    test2_passed = test_incremental_growth()

    print(f"\n=== Final Results ===")
    print(f"User repetition test: {'PASS' if test1_passed else 'FAIL'}")
    print(f"Incremental growth test: {'PASS' if test2_passed else 'FAIL'}")
    print(f"Overall: {'PASS' if test1_passed and test2_passed else 'FAIL'}")