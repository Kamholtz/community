import ast
import importlib.util
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).parents[1] / 'my-config' / 'whisper'
spec = importlib.util.spec_from_file_location('whisper_hud_buttons', ROOT / 'whisper_hud_buttons.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class HudButtonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'buttons.json'
        self.icons = {}
        self.options = {}
        self.actions = SimpleNamespace(
            hud_create_status_icon=lambda *args: args,
            hud_publish_status_icon=lambda topic, icon: self.icons.update({topic: icon}),
            hud_remove_status_icon=lambda topic: self.icons.pop(topic, None),
            hud_create_button=lambda text, callback, image="": SimpleNamespace(text=text, callback=callback, image=image),
            hud_create_status_option=lambda topic, default, active: SimpleNamespace(default=default, active=active),
            hud_publish_status_option=lambda topic, option: self.options.update({topic: option}),
        )
        self.ns = {
            '_whisper_enabled': False, '_whisper_ui_state': None,
            '_whisper_last_session_polished': None,
            '_WHISPER_STATUS_TOPIC': 'whisper_status',
            '_WHISPER_COPY_ON_STOP_TOPIC': 'whisper_copy_on_stop',
            '_WHISPER_SESSION_TOPIC': 'whisper_polished_session',
            '_WHISPER_STATUS_ICON': 'stop', '_WHISPER_START_ICON': 'start',
            '_WHISPER_COPY_ON_STOP_ICON': 'finish_copy', '_WHISPER_SESSION_ICON': 'copy',
            '_WHISPER_STATUS_TEXT': {}, 'actions': SimpleNamespace(user=self.actions),
            '_return_to_command_mode': Mock(), '_switch_to_whisper_mode': Mock(),
            '_return_to_command_mode_and_copy': Mock(), '_copy_last_session_polished': Mock(),
            'whisper_hud': SimpleNamespace(_warn_once=Mock()),
        }
        names = {'_publish_whisper_menu_options', '_whisper_menu_images', '_publish_whisper_status', '_publish_command_mode_whisper_button',
                 '_publish_whisper_mode_buttons', '_remove_whisper_mode_copy_button',
                 '_publish_polished_session_available', '_publish_initial_whisper_button'}
        tree = ast.parse((ROOT / 'whisper_mode.py').read_text(encoding='utf-8'))
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
        exec(compile(ast.Module(body=functions, type_ignores=[]), 'whisper_mode.py', 'exec'), self.ns)
        self.refresh = self.ns['_publish_initial_whisper_button']
        self.labels = {'whisper_status': 'Whisper mode toggle',
                       'whisper_copy_on_stop': 'Whisper stop and copy',
                       'whisper_polished_session': 'Whisper copy latest session'}
        self.buttons = module.WhisperHudButtons(self.path, self.actions, self.labels, self.refresh, self.ns['_whisper_menu_images'])
        self.ns['_whisper_hud_buttons'] = self.buttons

    def test_conditional_icons_and_menu_callbacks(self):
        self.refresh()
        self.assertEqual(set(self.icons), {'whisper_status'})
        self.assertEqual(len(self.options), 3)
        self.assertEqual(self.options['whisper_status_option'].default.image, 'start')
        self.assertEqual(self.options['whisper_copy_on_stop_option'].default.image, 'finish_copy')
        self.assertEqual(self.options['whisper_polished_session_option'].default.image, 'copy')
        for topic in self.labels:
            option = self.options[topic + '_option']
            self.assertTrue(option.default.text.startswith('Remove '))
            self.assertEqual(option.default, option.active)
        self.options['whisper_copy_on_stop_option'].default.callback(object())
        self.assertTrue(self.options['whisper_copy_on_stop_option'].default.text.startswith('Add '))
        self.ns['_whisper_enabled'] = True
        self.ns['_whisper_last_session_polished'] = 'Polished text'
        self.refresh()
        self.assertEqual(set(self.icons), {'whisper_status', 'whisper_polished_session'})
        self.assertEqual(self.options['whisper_status_option'].default.image, 'stop')
        self.assertEqual(self.options['whisper_copy_on_stop_option'].default.image, 'finish_copy')
        self.options['whisper_copy_on_stop_option'].default.callback(object())
        self.assertEqual(set(self.icons), set(self.labels))
        self.assertEqual(self.icons['whisper_copy_on_stop'][1], 'finish_copy')
        self.assertIs(self.icons['whisper_copy_on_stop'][4], self.ns['_return_to_command_mode_and_copy'])
        self.assertEqual(self.icons['whisper_polished_session'][1], 'copy')
        self.assertIs(self.icons['whisper_polished_session'][4], self.ns['_copy_last_session_polished'])
        self.ns['_whisper_enabled'] = False
        self.refresh()
        self.assertNotIn('whisper_copy_on_stop', self.icons)
        self.assertTrue(self.options['whisper_copy_on_stop_option'].default.text.startswith('Remove '))

    def test_hidden_buttons_survive_every_publisher_and_reload(self):
        for topic in self.labels:
            self.buttons.set_visible(topic, False)
        self.ns['_whisper_enabled'] = True
        self.ns['_whisper_last_session_polished'] = 'Polished text'
        for name in ('_publish_whisper_mode_buttons', '_publish_command_mode_whisper_button',
                     '_publish_polished_session_available', '_publish_initial_whisper_button'):
            self.ns[name]()
            self.assertEqual(self.icons, {})
        self.buttons = module.WhisperHudButtons(self.path, self.actions, self.labels, self.refresh, self.ns['_whisper_menu_images'])
        self.ns['_whisper_hud_buttons'] = self.buttons
        self.refresh()
        self.assertEqual(self.icons, {})
        self.buttons.set_visible('whisper_status', True)
        self.assertEqual(set(self.icons), {'whisper_status'})
        self.assertEqual(self.buttons.hidden, {'whisper_copy_on_stop', 'whisper_polished_session'})

    def test_invalid_preferences_do_not_break_startup(self):
        self.path.write_text('{broken', encoding='utf-8')
        buttons = module.WhisperHudButtons(self.path, self.actions, self.labels, self.refresh, self.ns['_whisper_menu_images'])
        self.assertEqual(buttons.hidden, set())


if __name__ == '__main__':
    unittest.main()
