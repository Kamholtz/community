import importlib.util
from pathlib import Path
import sys
import unittest


MODULE_PATH = (
    Path(__file__).parents[1] / "my-config" / "whisper" / "whisper_transcript_state.py"
)
SPEC = importlib.util.spec_from_file_location("whisper_transcript_state", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
TranscriptState = MODULE.TranscriptState


class TranscriptStateTests(unittest.TestCase):
    def test_full_then_polished_resolves_polished_text(self):
        state = TranscriptState()
        displaced, pending = state.begin_full("original")

        self.assertIsNone(displaced)
        self.assertIs(state.apply_polished("polished"), pending)
        self.assertEqual(state.resolve(pending.identity).insertion_text, "polished")

    def test_full_without_polished_resolves_original_text(self):
        state = TranscriptState()
        _, pending = state.begin_full("original")

        self.assertEqual(state.resolve(pending.identity).insertion_text, "original")

    def test_stale_timer_cannot_resolve_a_new_transcript(self):
        state = TranscriptState()
        _, first = state.begin_full("first")
        displaced, second = state.begin_full("second")

        self.assertIs(displaced, first)
        self.assertIsNone(state.resolve(first.identity))
        self.assertEqual(state.resolve(second.identity).insertion_text, "second")

    def test_repeated_text_gets_distinct_identities(self):
        state = TranscriptState()
        _, first = state.begin_full("repeat")
        state.resolve(first.identity)
        _, second = state.begin_full("repeat")

        self.assertNotEqual(first.identity, second.identity)

    def test_polished_without_full_is_ignored(self):
        self.assertIsNone(TranscriptState().apply_polished("orphan"))


if __name__ == "__main__":
    unittest.main()
