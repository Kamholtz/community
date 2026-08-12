"""Data-driven D-pad overlay for common Whisper session actions."""

from dataclasses import dataclass
from typing import Callable

from talon import Context, Module, actions, ui
from talon.canvas import Canvas
from talon.skia import RoundRect
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.types import Rect


mod = Module()
mod.tag("whisper_dpad", desc="Whisper D-pad overlay is visible")
ctx = Context()


@dataclass(frozen=True)
class WhisperDpadBinding:
    direction: str
    label: str
    command: Callable[[], None]
    should_dismiss: Callable[[], bool]


def keep_visible() -> bool:
    return False


def dismiss_after_command() -> bool:
    return True


# This is the sole command configuration.  Input handlers dispatch by direction
# and evaluate should_dismiss only after the command has completed.
WHISPER_DPAD_BINDINGS = (
    WhisperDpadBinding("up", "Toggle Whisper", actions.user.whisper_toggle, keep_visible),
    WhisperDpadBinding("left", "Copy last session", actions.user.whisper_session_copy, dismiss_after_command),
    WhisperDpadBinding("right", "Insert last session", actions.user.whisper_session_insert, dismiss_after_command),
    WhisperDpadBinding("down", "Copy current session", actions.user.whisper_session_copy_current, dismiss_after_command),
)
_BINDINGS_BY_DIRECTION = {binding.direction: binding for binding in WHISPER_DPAD_BINDINGS}

_canvas: Canvas | None = None
_scale = 1.0


def _is_active() -> bool:
    try:
        return actions.user.whisper_is_active()
    except Exception:
        return False


def _set_tag(visible: bool) -> None:
    ctx.tags = ["user.whisper_dpad"] if visible else []


def _draw_button(
    c: SkiaCanvas,
    rect: Rect,
    direction: str,
    arrow: str,
    label: str,
    active: bool,
) -> None:
    rounded_rect = RoundRect.from_rect(rect, x=14 * _scale, y=14 * _scale)
    c.paint.style = c.paint.Style.FILL
    c.paint.color = "1f6f43" if active else "30343b"
    c.draw_rrect(rounded_rect)
    c.paint.style = c.paint.Style.STROKE
    c.paint.stroke_width = 2 * _scale
    c.paint.color = "83e6a5" if active else "d6d9de"
    c.draw_rrect(rounded_rect)
    c.paint.style = c.paint.Style.FILL
    c.paint.color = "ffffff"
    c.paint.textsize = 34 * _scale
    arrow_bounds = c.paint.measure_text(arrow)[1]
    c.draw_text(
        arrow,
        rect.center.x - arrow_bounds.x - arrow_bounds.width / 2,
        rect.center.y - arrow_bounds.y - arrow_bounds.height / 2,
    )
    c.paint.textsize = 18 * _scale
    label_bounds = c.paint.measure_text(label)[1]
    label_y = rect.center.y - label_bounds.y - label_bounds.height / 2
    label_gap = 14 * _scale
    if direction == "left":
        label_x = rect.x - label_gap - label_bounds.x - label_bounds.width
    else:
        label_x = rect.x + rect.width + label_gap - label_bounds.x
    c.draw_text(label, label_x, label_y)


def _draw(c: SkiaCanvas) -> None:
    active = _is_active()
    # Leave the canvas untouched outside the controls so the desktop remains
    # visible, matching Quick Pick's transparent overlay behaviour.
    c.paint.style = c.paint.Style.FILL
    c.paint.color = "83e6a5" if active else "ffffff"
    c.paint.textsize = 24 * _scale
    title = "WHISPER ACTIVE" if active else "WHISPER CONTROLS"
    bounds = c.paint.measure_text(title)[1]
    c.draw_text(
        title,
        c.rect.center.x - bounds.x - bounds.width / 2,
        c.rect.y + 42 * _scale,
    )

    side = 72 * _scale
    gap = 18 * _scale
    centre_x, top_y = c.rect.center.x, c.rect.center.y - 85 * _scale
    positions = {
        "up": Rect(centre_x - side / 2, top_y, side, side),
        "left": Rect(centre_x - side - gap, top_y + side + gap, side, side),
        "right": Rect(centre_x + gap, top_y + side + gap, side, side),
        "down": Rect(centre_x - side / 2, top_y + (side + gap) * 2, side, side),
    }
    arrows = {"up": "↑", "left": "←", "right": "→", "down": "↓"}
    for binding in WHISPER_DPAD_BINDINGS:
        _draw_button(
            c,
            positions[binding.direction],
            binding.direction,
            arrows[binding.direction],
            binding.label,
            active,
        )

    c.paint.color = "c4c8ce"
    c.paint.textsize = 15 * _scale
    hint = "Press another mapped button to dismiss"
    hint_bounds = c.paint.measure_text(hint)[1]
    c.draw_text(
        hint,
        c.rect.center.x - hint_bounds.x - hint_bounds.width / 2,
        c.rect.y + c.rect.height - 22 * _scale,
    )


def _show() -> None:
    global _canvas, _scale
    if _canvas:
        return
    screen = ui.main_screen()
    _scale = screen.scale
    _canvas = Canvas.from_screen(screen)
    _canvas.blocks_mouse = False
    _canvas.register("draw", _draw)
    _set_tag(True)
    _canvas.freeze()


def _hide() -> None:
    global _canvas
    _set_tag(False)
    if not _canvas:
        return
    _canvas.unregister("draw", _draw)
    _canvas.close()
    _canvas = None


@mod.action_class
class Actions:
    def whisper_dpad_toggle() -> None:
        """Show or hide the Whisper D-pad overlay."""
        if _canvas:
            _hide()
        else:
            _show()

    def whisper_dpad_hide() -> None:
        """Hide the Whisper D-pad overlay."""
        _hide()

    def whisper_dpad_refresh() -> None:
        """Redraw the visible Whisper D-pad overlay."""
        if _canvas:
            _canvas.freeze()

    def whisper_dpad_dispatch(direction: str) -> None:
        """Run the configured Whisper D-pad command for direction."""
        binding = _BINDINGS_BY_DIRECTION.get(direction)
        if binding is None:
            _hide()
            return
        binding.command()
        if binding.should_dismiss():
            _hide()
