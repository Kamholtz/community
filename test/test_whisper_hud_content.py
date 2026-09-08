import importlib.util
from pathlib import Path
import sys
import unittest


def _load(name: str):
    module_path = Path(__file__).parents[1] / "my-config" / "whisper" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CONTENT = _load("whisper_hud_content")
WhisperServiceState = _load("whisper_service_state").WhisperServiceState


class FormatPanelTests(unittest.TestCase):
    def test_every_known_state_renders(self):
        services = WhisperServiceState()
        for state in CONTENT.STATE_TEXT:
            body = CONTENT.format_whisper_panel(state, services, [], None, None)
            self.assertIn(CONTENT.STATE_TEXT[state], body)

    def test_unknown_state_falls_back_to_title_case(self):
        body = CONTENT.format_state_line("weird_state")
        self.assertIn("Weird State", body)

    def test_service_health_markers(self):
        services = WhisperServiceState(connected=True)
        services.polisher.apply_test(True, "ok")
        services.context_extractor.apply_availability(
            {"enabled": True, "available": False}
        )
        body = CONTENT.format_whisper_panel("listening", services, [], None, None, show_details=True)
        self.assertIn("<+ready/>", body)
        self.assertIn("<!!unavailable/>", body)

    def test_degraded_polisher_mentions_plain_transcription(self):
        services = WhisperServiceState(connected=True)
        services.polisher.apply_test(False, "boom")
        body = CONTENT.format_whisper_panel("listening", services, [], None, None, show_details=True)
        self.assertIn("plain transcription available", body)

    def test_draft_phases_use_expected_markers(self):
        services = WhisperServiceState()
        for phase, marker in (("realtime", "<@"), ("final", "<!"), ("polished", "<+")):
            body = CONTENT.format_whisper_panel(
                "realtime", services, [], "hello there", phase
            )
            self.assertIn(f"{marker}hello there/>", body)

    def test_session_tail_limits_and_escapes(self):
        services = WhisperServiceState()
        lines = [f"line {i}" for i in range(20)] + ["evil <!!marker/> text"]
        body = CONTENT.format_whisper_panel(
            "listening", services, lines, None, None, session_tail=3
        )
        self.assertNotIn("line 17", body)
        self.assertIn("line 19", body)
        self.assertNotIn("<!!marker/>", body)
        self.assertIn("‹!!marker/ >", body)

    def test_shutdown_countdown(self):
        services = WhisperServiceState()
        body = CONTENT.format_whisper_panel(
            "session_finishing", services, [], None, None, shutdown_remaining_s=12.4
        )
        self.assertIn("forcing stop in 12s", body)

    def test_input_device_line(self):
        services = WhisperServiceState()
        body = CONTENT.format_whisper_panel(
            "listening", services, [], None, None,
            input_device="Microphone (AnkerWork M650 RX)",
            show_details=True,
        )
        self.assertIn("Mic → WSL:", body)
        self.assertIn("Microphone (AnkerWork M650 RX)", body)
        body_without = CONTENT.format_whisper_panel(
            "listening", services, [], None, None
        )
        self.assertNotIn("Mic", body_without)

    def test_no_transcript_section_when_empty(self):
        services = WhisperServiceState()
        body = CONTENT.format_whisper_panel("listening", services, [], "  ", None)
        self.assertNotIn("\n\n", body)

    def test_compact_panel_hides_routine_details_without_losing_transcript(self):
        services = WhisperServiceState(connected=True)
        services.polisher.apply_test(True, "ok")
        services.context_extractor.apply_availability({"available": False})
        body = CONTENT.format_whisper_panel(
            "polished", services, ["Session text"], "Live words", "realtime",
            input_device="Long microphone name",
        )
        self.assertEqual(body.splitlines()[0], "<+Polished/> · Context off")
        self.assertNotIn("Long microphone name", body)
        self.assertNotIn("Polish:", body)
        self.assertIn("Session text", body)
        self.assertIn("<@Live words/>", body)

    def test_compact_panel_keeps_failures_visible(self):
        services = WhisperServiceState(connected=True)
        services.polisher.apply_test(False, "probe failed")
        services.context_extractor.apply_test(False, "probe failed")
        body = CONTENT.format_whisper_panel("listening", services, [], None, None)
        self.assertIn("<!!Polish failed/>", body)
        self.assertIn("<!!Context failed/>", body)


class StatusAndContextPanelTests(unittest.TestCase):
    def test_service_status_panel_includes_details(self):
        services = WhisperServiceState(connected=True)
        services.polisher.apply_test(True, "polished text ok", attempts=2)
        body = CONTENT.format_service_status_panel(services)
        self.assertIn("Whisper not tested", body)
        self.assertIn("<+ready/>", body)
        self.assertIn("polished text ok", body)
        self.assertIn("Polisher tested:", body)

    def test_context_panel_renders_dict_and_escapes(self):
        body = CONTENT.format_context_panel(
            {"status": "ready", "text": "code <!!alert/>"}
        )
        self.assertIn("<*Status:/> ready", body)
        self.assertNotIn("<!!alert/>", body)

    def test_context_panel_empty(self):
        self.assertIn("No context status", CONTENT.format_context_panel(None))


class HistoryChoicesTests(unittest.TestCase):
    def test_numbering_matches_whisper_pick(self):
        history = ["oldest", "middle", "newest"]
        choices = CONTENT.build_history_choices(history)
        # whisper pick 1 == newest (reversed, 1-based) in whisper_mode.py
        self.assertEqual(choices[0]["index"], 1)
        self.assertIn("newest", choices[0]["text"])
        self.assertEqual(choices[2]["index"], 3)
        self.assertIn("oldest", choices[2]["text"])

    def test_empty_history(self):
        self.assertEqual(CONTENT.build_history_choices([]), [])

    def test_preview_truncation(self):
        choices = CONTENT.build_history_choices(["x" * 100], preview_len=20)
        self.assertTrue(choices[0]["text"].endswith("..."))
        self.assertLessEqual(len(choices[0]["text"]), len("1: ") + 20)


class LogLevelTests(unittest.TestCase):
    def test_event_levels(self):
        self.assertEqual(CONTENT.log_level_for_event("client_connected"), "event")
        self.assertEqual(CONTENT.log_level_for_event("session_error"), "error")
        self.assertIsNone(CONTENT.log_level_for_event("realtime"))

    def test_service_change_levels(self):
        self.assertIsNone(CONTENT.log_level_for_service_change("ready", "ready"))
        self.assertEqual(
            CONTENT.log_level_for_service_change(
                "ready", "unavailable; plain transcription available"
            ),
            "warning",
        )
        self.assertEqual(
            CONTENT.log_level_for_service_change("unavailable", "ready"), "success"
        )
        self.assertEqual(
            CONTENT.log_level_for_service_change(
                "available, not tested", "passed"
            ),
            "event",
        )


if __name__ == "__main__":
    unittest.main()
