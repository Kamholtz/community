import ast
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


ROOT = Path(__file__).parents[1] / "my-config"
MODE_TOGGLE_PATH = ROOT / "mode_toggle.py"
mode_toggle_tree = ast.parse(MODE_TOGGLE_PATH.read_text(encoding="utf-8"))
hud_button_class = next(
    node
    for node in mode_toggle_tree.body
    if isinstance(node, ast.ClassDef) and node.name == "TranscriptionHudButton"
)
hud_button_namespace = {
    "Path": Path,
    "json": json,
    "_TRANSCRIPTION_HUD_TOPIC": "transcription_mode",
}
exec(
    compile(
        ast.Module(body=[hud_button_class], type_ignores=[]),
        "mode_toggle.py",
        "exec",
    ),
    hud_button_namespace,
)
module = SimpleNamespace(
    TranscriptionHudButton=hud_button_namespace["TranscriptionHudButton"]
)


class TranscriptionHudButtonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.icons = {}
        self.options = {}
        self.refresh_count = 0
        self.actions = SimpleNamespace(
            hud_publish_status_icon=lambda topic, icon: self.icons.update({topic: icon}),
            hud_remove_status_icon=lambda topic: self.icons.pop(topic, None),
            hud_create_button=lambda text, callback, image="": SimpleNamespace(
                text=text, callback=callback, image=image
            ),
            hud_create_status_option=lambda topic, default, active: SimpleNamespace(
                default=default, active=active
            ),
            hud_publish_status_option=lambda topic, option: self.options.update(
                {topic: option}
            ),
        )
        self.button = module.TranscriptionHudButton(
            Path(self.temp.name) / "button.json",
            self.actions,
            lambda: setattr(self, "refresh_count", self.refresh_count + 1),
            lambda: "dictation_icon",
        )

    def test_visibility_preference_persists_and_controls_icon(self):
        self.button.publish_option()
        self.button.publish_icon("icon")
        self.assertEqual(self.icons, {"transcription_mode": "icon"})
        option = self.options["transcription_mode_option"]
        self.assertEqual(option.default.text, "Remove transcription mode")
        self.assertEqual(option.default.image, "dictation_icon")

        option.default.callback()
        self.assertEqual(self.icons, {})
        self.assertEqual(self.refresh_count, 1)
        self.assertTrue(self.button.hidden)

        reloaded = module.TranscriptionHudButton(
            Path(self.temp.name) / "button.json",
            self.actions,
            lambda: None,
            lambda: "command_icon",
        )
        self.assertTrue(reloaded.hidden)
        reloaded.publish_option()
        self.assertEqual(
            self.options["transcription_mode_option"].default.text,
            "Add transcription mode",
        )
        self.options["transcription_mode_option"].default.callback()
        self.assertFalse(reloaded.hidden)


class HandySpeechSuppressionTests(unittest.TestCase):
    def test_hud_click_uses_the_handy_mode_selector(self):
        source = (ROOT / "mode_toggle.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        publish_function = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_publish_transcription_hud_button"
        )
        create_icon_call = next(
            node
            for node in ast.walk(publish_function)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "hud_create_status_icon"
        )
        callback = create_icon_call.args[4]

        self.assertIsInstance(callback, ast.Name)
        self.assertEqual(callback.id, "_toggle_f1_handy_mode_from_hud")

        hud_callback = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_toggle_f1_handy_mode_from_hud"
        )
        self.assertIsInstance(hud_callback.args.vararg, ast.arg)
        self.assertEqual(hud_callback.args.vararg.arg, "_args")
        action_call = next(
            node
            for node in ast.walk(hud_callback)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "toggle_f1_handy_mode"
        )
        self.assertEqual(action_call.args, [])

    def test_handy_transcription_disables_and_reenables_speech(self):
        source = (ROOT / "mode_toggle.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        actions_class = next(
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "Actions"
        )
        handy_method = next(
            node
            for node in actions_class.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "toggle_handy_transcription"
        )
        user = SimpleNamespace(handy_toggle=Mock())
        speech = SimpleNamespace(disable=Mock(), enable=Mock())
        namespace = {
            "actions": SimpleNamespace(user=user, speech=speech),
            "_handy_transcribing": False,
            "_publish_transcription_hud_button": Mock(),
        }
        exec(
            compile(
                ast.Module(body=[handy_method], type_ignores=[]),
                "mode_toggle.py",
                "exec",
            ),
            namespace,
        )

        namespace["toggle_handy_transcription"]()
        user.handy_toggle.assert_called_once()
        speech.disable.assert_called_once()
        speech.enable.assert_not_called()

        namespace["toggle_handy_transcription"]()
        self.assertEqual(user.handy_toggle.call_count, 2)
        speech.enable.assert_called_once()


if __name__ == "__main__":
    unittest.main()
