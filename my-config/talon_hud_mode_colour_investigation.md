# Talon HUD mode color investigation

## How sleep mode turns the HUD blue
- The status bar background color is driven by the current HUD "mode" variable.
- `content/mode_poller.py` publishes the mode variable via:
  - `self.content.publish_event("variable", "mode", "replace", current_mode)`
- `widgets/statusbar.py` reads that variable and picks a theme color key:
  - `mode = self.content.get_variable("mode", "command")`
  - `mode_colour = self.theme.get_colour(mode + "_mode_colour")`
  - This is used in a gradient for the status bar background.
- In the dark theme, `themes/dark/theme.csv` sets `sleep_mode_colour` to `#2071A3` (blue). So when `mode == "sleep"`, the background uses that blue value.
- Light theme uses `sleep_mode_colour,#777777`, so sleep mode is gray there; the blue effect is specifically from the dark theme’s `sleep_mode_colour` value.

Key files:
- `/home/carl/.talon/user/talon_hud/widgets/statusbar.py`
- `/home/carl/.talon/user/talon_hud/content/mode_poller.py`
- `/home/carl/.talon/user/talon_hud/themes/dark/theme.csv`
- `/home/carl/.talon/user/talon_hud/themes/light/theme.csv`
- `/home/carl/.talon/user/talon_hud/themes/_base_theme/theme.csv`
- `/home/carl/.talon/user/talon_hud/APPEARANCE.md`

## How to apply this to custom modes (user-defined)
The HUD’s mode tracking is designed to be extended. The key is to make the mode name show up in `hud_determine_mode()` and provide a matching `*_mode_colour` in your theme.

Mechanics:
- `content/mode_poller.py` uses `actions.user.hud_determine_mode()` to compute the mode string, then publishes it.
- The default `hud_get_status_modes()` returns `['dictation', 'command', 'sleep']`.
- `hud_determine_mode()` loops through the list from `hud_get_status_modes()` and picks the first entry that exists in Talon’s `scope.get("mode")` list.
- The status bar then looks for a theme key named `<mode>_mode_colour`.

Implications for custom modes:
1. You can override `user.hud_get_status_modes()` to include your custom mode name.
   - `CUSTOMIZATION.md` explicitly notes that adding modes here enables more theming options.
2. If multiple modes are active at once, the list order in `hud_get_status_modes()` determines which mode wins.
   - This matters because your whisper mode currently enables `user.whisper` *alongside* `command`.
3. You must add a matching theme key in the active theme’s `theme.csv`:
   - If the mode name is `user.whisper`, then the key should be `user.whisper_mode_colour`.
   - If you instead want a simpler key like `whisper_mode_colour`, you would need `hud_determine_mode()` to return `whisper` (not `user.whisper`).
4. If you want a status bar icon for the custom mode, the HUD expects a theme image named `<mode>_icon.png`.
   - With `user.whisper`, that would be `user.whisper_icon.png` in the theme images folder.

Relevant documentation:
- `/home/carl/.talon/user/talon_hud/CUSTOMIZATION.md` (Customizing mode tracking)

## Applying this to your Whisper mode (goal: green background)
Your custom mode is defined in:
- `/home/carl/.talon/user/community/my-config/scribe/whisper_mode.py`
  - It enables `actions.mode.enable("user.whisper")` when whisper starts.

To make the HUD background green in whisper mode (conceptually, no edits yet):
1. Ensure `hud_get_status_modes()` includes `"user.whisper"` and place it *before* `"command"` so whisper takes priority while command remains active.
2. Add a theme color key in the active theme:
   - Example: `user.whisper_mode_colour,#00FF00` (pick any green you like).
3. (Optional) Add an icon named `user.whisper_icon.png` in the theme’s images directory for the status bar.

Notes on existing code:
- `whisper_mode.py` calls `actions.user.hud_set_theme("green")` / `actions.user.hud_set_theme("default")`.
  - The Talon HUD project exposes `actions.user.hud_switch_theme()` (see `display.py` and `hud_commands.talon`).
  - I did not find a `hud_set_theme` action in this repo.
  - This may be unrelated to the mode-color system above, but it is worth noting for later if you intended to switch full themes.

## Summary of the sleep-mode color path (trace)
1. Talon sleep mode becomes active.
2. `actions.user.hud_determine_mode()` returns `"sleep"`.
3. `mode_poller` publishes the `mode` variable.
4. `statusbar.py` uses `sleep_mode_colour` from the theme to draw its background gradient.

