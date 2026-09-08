import importlib.util
from pathlib import Path
import sys
import unittest


MODULE_PATH = (
    Path(__file__).parents[1] / "my-config" / "whisper" / "whisper_service_state.py"
)
SPEC = importlib.util.spec_from_file_location("whisper_service_state", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
WhisperServiceState = MODULE.WhisperServiceState


class WhisperServiceStateTests(unittest.TestCase):
    def test_service_status_updates_optional_services(self):
        state = WhisperServiceState()
        state.apply_service_status(
            {
                "polisher": {"enabled": True, "available": True},
                "context_extractor": {"enabled": False, "available": False},
            }
        )

        self.assertEqual(state.polisher.label(), "available, not tested")
        self.assertEqual(state.context_extractor.label(), "disabled")

    def test_polishing_failure_keeps_plain_transcription_available(self):
        state = WhisperServiceState(connected=True)
        state.polisher.apply_test(False, "Polisher test failed")

        self.assertEqual(
            state.polishing_label(), "failed; plain transcription available"
        )

    def test_retry_is_visible(self):
        state = WhisperServiceState()
        state.polisher.apply_test(True, "polished text", attempts=2)

        self.assertEqual(state.polisher.label(), "passed after retry")

    def test_fresh_unavailable_status_outranks_previous_pass(self):
        state = WhisperServiceState(connected=True)
        state.polisher.apply_test(True, "polished text")
        state.apply_service_status(
            {"polisher": {"enabled": True, "available": False}}
        )

        self.assertEqual(state.polisher.label(), "unavailable")
        self.assertEqual(
            state.polishing_label(), "unavailable; plain transcription available"
        )

    def test_live_polish_verifies_service(self):
        state = WhisperServiceState(connected=True)
        state.apply_service_status(
            {"polisher": {"enabled": True, "available": True}}
        )
        self.assertEqual(state.polishing_label(), "available, not tested")

        self.assertTrue(state.polisher.verify_live())
        self.assertEqual(state.polishing_label(), "ready")
        self.assertEqual(state.polisher.detail, "verified by live use")

    def test_live_verification_keeps_existing_probe_result(self):
        state = WhisperServiceState(connected=True)
        state.polisher.apply_test(True, "probe detail", attempts=2)

        self.assertFalse(state.polisher.verify_live())
        self.assertEqual(state.polisher.detail, "probe detail")
        self.assertEqual(state.polisher.label(), "passed after retry")

    def test_fresh_unavailable_still_outranks_live_verification(self):
        state = WhisperServiceState(connected=True)
        state.polisher.verify_live()
        state.apply_service_status(
            {"polisher": {"enabled": True, "available": False}}
        )

        self.assertEqual(state.polisher.label(), "unavailable")

    def test_dictation_is_not_claimed_ready_before_whisper_test(self):
        state = WhisperServiceState(connected=True)

        self.assertEqual(state.dictation_label(), "connected, Whisper not tested")


if __name__ == "__main__":
    unittest.main()
