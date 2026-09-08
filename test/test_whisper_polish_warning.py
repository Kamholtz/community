import ast
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


ROOT = Path(__file__).parents[1] / "my-config" / "whisper"


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


Watch = load("whisper_polish_watch").PolishWatch
State = load("whisper_transcript_state").TranscriptState
Content = load("whisper_hud_content")
Services = load("whisper_service_state").WhisperServiceState


class PolishWarningTests(unittest.TestCase):
    def setUp(self):
        self.now = 0.0
        self.strict = True
        self.config = {
            "user.whisper_polish_warning_ms": 5000,
            "user.whisper_polish_segments": True,
            "user.whisper_polish_fallback_ms": 700,
        }
        self.state = State()
        self.insert = Mock()
        self.cron = SimpleNamespace(after=Mock(), interval=Mock(), cancel=Mock())
        self.namespace = {
            "json": json,
            "time": SimpleNamespace(monotonic=lambda: self.now),
            "settings": SimpleNamespace(get=self.config.__getitem__),
            "cron": self.cron,
            "PendingTranscript": object,
            "_whisper_enabled": True,
            "_whisper_last_event_signature": None,
            "_whisper_last_realtime": None,
            "_whisper_polish_watch": Watch(),
            "_whisper_polish_warning_job": None,
            "_whisper_polish_warning": None,
            "_whisper_transcripts": self.state,
            "_whisper_services": Services(),
            "_queue_ui_action": lambda action: action(),
            "_polished_only": lambda: self.strict,
            "_insert_and_remember": self.insert,
        }
        for name in (
            "_refresh_hud_panel", "_set_whisper_ui_state", "_set_hud_draft",
            "_show_whisper_subtitle", "_retain_pending_transcript",
            "_release_pending_transcript", "_remember_session_transcript", "_notify",
        ):
            self.namespace[name] = Mock()
        names = {
            "_refresh_polish_warning", "_watch_for_polish", "_polish_received",
            "_reset_polish_warning", "_handle_ws_event", "_cancel_fallback",
            "_resolve_pending_transcript", "_insert_displaced_transcript",
        }
        tree = ast.parse((ROOT / "whisper_mode.py").read_text(encoding="utf-8"))
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
        exec(compile(ast.Module(body=functions, type_ignores=[]), "whisper_mode.py", "exec"), self.namespace)

    def event(self, kind, text):
        self.namespace["_handle_ws_event"]({"type": kind, "content": text})

    def tick(self, now):
        self.now = now
        self.namespace["_refresh_polish_warning"]()
        return self.namespace["_whisper_polish_warning"]

    def test_strict_warning_at_five_seconds_clears_on_polish(self):
        self.event("full", "raw")
        self.assertIsNone(self.tick(4.99))
        self.assertIn("over 5s", self.tick(5.0))
        self.event("realtime", "next live words")
        self.assertIsNotNone(self.namespace["_whisper_polish_warning"])
        self.insert.assert_not_called()
        self.event("polished", "Polished.")
        self.assertIsNone(self.namespace["_whisper_polish_warning"])
        self.assertIsNone(self.namespace["_whisper_polish_warning_job"])
        self.insert.assert_called_once_with("Polished. ")

    def test_fallback_insertion_does_not_cancel_warning_or_reinsert_late_result(self):
        self.strict = False
        self.event("full", "raw")
        self.now = 0.7
        self.cron.after.call_args.args[1]()
        self.insert.assert_called_once_with("raw ")
        self.assertIsNone(self.state.pending)
        self.assertIn("over 5s", self.tick(5))
        self.event("polished", "Polished.")
        self.assertIsNone(self.namespace["_whisper_polish_warning"])
        self.insert.assert_called_once_with("raw ")

    def test_immediate_insertion_mode_also_warns(self):
        self.strict = False
        self.config["user.whisper_polish_segments"] = False
        self.event("full", "raw")
        self.insert.assert_called_once_with("raw ")
        self.assertIsNotNone(self.tick(5))

    def test_fast_polishing_never_warns(self):
        self.event("full", "raw")
        self.now = 1
        self.event("polished", "Polished.")
        self.assertIsNone(self.tick(10))

    def test_new_segment_does_not_hide_a_missing_earlier_result(self):
        self.event("full", "first")
        self.now = 2
        self.event("full", "second")
        self.assertIn("2 segments missing", self.tick(7))
        self.event("polished", "Second.")
        self.assertIsNotNone(self.tick(8))
        self.assertEqual(self.namespace["_whisper_polish_watch"].overdue(8, 5), 1)

    def test_reset_cancels_timer_and_clears_warning(self):
        self.event("full", "raw")
        self.tick(5)
        self.namespace["_reset_polish_warning"]()
        self.cron.cancel.assert_called()
        self.assertIsNone(self.namespace["_whisper_polish_warning_job"])
        self.assertIsNone(self.tick(50))

    def test_configurable_delay(self):
        self.config["user.whisper_polish_warning_ms"] = 8000
        self.event("full", "raw")
        self.assertIsNone(self.tick(5))
        self.assertIn("over 8s", self.tick(8))

    def test_warning_visible_in_both_panel_views_and_modes(self):
        for strict in (True, False):
            for details in (True, False):
                body = Content.format_whisper_panel(
                    "listening", Services(), ["Existing text"], "draft", "realtime",
                    show_details=details, polished_only=strict,
                    polish_warning="Still waiting for polished text (over 5s)",
                )
                self.assertEqual(body.splitlines()[1], "<!Warning: Still waiting for polished text (over 5s)/>")
                self.assertIn("Existing text", body)


if __name__ == "__main__":
    unittest.main()
