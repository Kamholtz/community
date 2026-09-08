import ast
import importlib.util
from pathlib import Path
import sys
import tempfile
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


Preferences = load("whisper_insertion_preferences").InsertionPreferences
State = load("whisper_transcript_state").TranscriptState


class InsertionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "state.json"
        self.preferences = Preferences(self.path)
        self.state = State()
        self.insert = Mock()
        self.namespace = {
            "PendingTranscript": object,
            "_insertion_preferences": self.preferences,
            "_whisper_transcripts": self.state,
            "settings": SimpleNamespace(get=lambda _: True),
            "cron": SimpleNamespace(cancel=Mock()),
            "_insert_and_remember": self.insert,
            "_remember_session_transcript": Mock(),
            "_notify": Mock(),
            "_refresh_hud_panel": Mock(),
        }
        names = {
            "_polished_only", "_retain_pending_transcript",
            "_release_pending_transcript", "_resolve_pending_transcript",
            "_insert_displaced_transcript", "_flush_pending_transcript",
            "_cancel_fallback", "_set_polished_only",
        }
        tree = ast.parse((ROOT / "whisper_mode.py").read_text(encoding="utf-8"))
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
        exec(compile(ast.Module(body=functions, type_ignores=[]), "whisper_mode.py", "exec"), self.namespace)

    def call(self, name, *args):
        return self.namespace[name](*args)

    def test_saved_toggle_overrides_default_after_restart(self):
        self.assertTrue(self.preferences.enabled(True))
        self.preferences.set_enabled(False)
        self.assertFalse(Preferences(self.path).enabled(True))
        self.preferences.set_enabled(True)
        self.assertTrue(Preferences(self.path).enabled(False))

    def test_timeout_and_stop_do_not_insert_raw_then_late_polish_inserts_once(self):
        _, pending = self.state.begin_full("hello world")
        self.call("_resolve_pending_transcript", pending.identity)
        self.call("_flush_pending_transcript")
        self.insert.assert_not_called()
        self.assertEqual(Preferences(self.path).withheld_text(), "hello world")
        self.state.apply_polished("Hello, world.")
        self.call("_resolve_pending_transcript", pending.identity)
        self.call("_flush_pending_transcript")
        self.insert.assert_called_once_with("Hello, world. ")
        self.assertEqual(Preferences(self.path).withheld_text(), "")

    def test_displaced_failed_segment_is_retained_across_reset(self):
        self.state.begin_full("first raw")
        displaced, pending = self.state.begin_full("second raw")
        self.call("_insert_displaced_transcript", displaced)
        self.state.apply_polished("Second, polished.")
        self.call("_resolve_pending_transcript", pending.identity)
        self.state.reset()
        self.assertEqual(Preferences(self.path).withheld_text(), "first raw")
        self.insert.assert_called_once_with("Second, polished. ")

    def test_switching_off_restores_original_insertion(self):
        self.state.begin_full("raw")
        self.call("_flush_pending_transcript")
        self.call("_set_polished_only", False)
        self.insert.assert_called_once_with("raw ")
        self.assertFalse(Preferences(self.path).enabled(True))
        self.assertEqual(self.preferences.withheld_text(), "")

    def test_duplicate_withheld_text_is_retained_independently(self):
        first = self.preferences.retain("repeat")
        self.preferences.retain("repeat")
        self.preferences.release(first)
        self.assertEqual(Preferences(self.path).withheld_text(), "repeat")


if __name__ == "__main__":
    unittest.main()
