# Talon HUD status buttons

## Add a clickable button

Create and publish a status icon:

```python
from talon import actions

TOPIC = "example_button"


def on_click(*_args) -> None:
    actions.user.example_action()


icon = actions.user.hud_create_status_icon(
    TOPIC,
    "copy_icon",  # Built-in image name or an absolute PNG path
    None,
    "Accessible button name",
    on_click,
)
actions.user.hud_publish_status_icon(TOPIC, icon)
```

Remove it with:

```python
actions.user.hud_remove_status_icon(TOPIC)
```

Callbacks should accept `*_args`; the status bar may pass its widget and icon.

## Choose the icon color from the button surface

Do not choose foreground color from the overall HUD theme name alone. Status
buttons can use a light circular background even when the surrounding HUD is
dark. Inspect `button_colour` and the rendered widget surface:

- Light button surface: use a charcoal or black glyph.
- Dark button surface: use an off-white glyph.
- If the button surface is light in both themes, use the same dark glyph in
  both themes.

This HUD currently uses light status-button circles in both themes, so the
Whisper button always uses its charcoal icon.

## When separate light/dark assets are necessary

Use transparent PNGs with distinct paths, for example:

```text
images/example_icon_light.png
images/example_icon_dark.png
```

Select the variant from the live HUD theme:

```python
theme_name = actions.user.hud_get_theme().name
variant = "dark" if theme_name.startswith("light") else "light"
```

Here, `dark` means a dark glyph for a light surface.

Republish the status icon after `user.hud_switch_theme(...)`; an already
published icon retains its old path. Use a short `cron.after(...)` callback if
the new theme must settle first.

## Avoid stale images and fallback themes

- The HUD caches images by image name/path. After changing an icon's color,
  use a new filename or force the theme to reload.
- Register custom themes with `user.hud_register_theme(name, directory)` before
  switching to them.
- A persisted custom theme may be restored before registration. If its live
  `theme_dir` differs from the registered directory, switch to the base theme
  and back after registration so the HUD rebuilds the custom theme.

Verify the live state through Talon's REPL:

```python
theme = actions.user.hud_get_theme()
print(theme.name, theme.theme_dir)
```

Check both the live theme directory and the published icon path; the theme name
by itself can be misleading when the HUD has fallen back to its base theme.
