from talon import Module, Context, ui, speech_system, actions
from talon.screen import Screen
from talon.canvas import Canvas, MouseEvent
from talon.skia import RoundRect, Canvas as SkiaCanvas
from talon.types import Rect, Point2d
from talon.grammar import Phrase
from dataclasses import dataclass
from typing import Callable, Optional
import math

# Font must be installed on the OS. "DejaVu Sans" is not present on Windows and
# causes all icon rendering to fail silently (Skia falls back to a font without
# symbol coverage). "Segoe UI Symbol" ships with Windows and covers ASCII, arrows,
# geometric shapes, and the U+23xx media transport symbols.
# NOTE: high-plane emoji (U+1F5xx, U+1F86x) are missing from Segoe UI Symbol —
# those were replaced with text labels in commit de0818b9 for exactly this reason.
FONT_FAMILY = "Segoe UI Symbol"
BACKGROUND_COLOR = "fffafa"  # Snow
HOVER_COLOR = "6495ed"  # CornflowerBlue
BORDER_COLOR = "000000"  # Black
TEXT_COLOR = "000000"  # Black
SNAP_COLORS = [
    "cd5c5c",  # IndianRed
    "1e90ff",  # DodgerBlue
    "556b2f",  # DarkOliveGreen
    "c0c0c0",  # Silver
    "ba55d3",  # MediumOrchid
    "fa8072",  # Salmon
]


@dataclass
class CircleOption:
    text: str
    degrees: int
    callback: Callable[[], None]
    move_mouse: Optional[bool] = False


@dataclass
class Option:
    text: str
    callback: Callable[[], None]
    move_mouse: Optional[bool] = False


@dataclass
class Button:
    rect: Rect
    callback: Callable[[], None]
    move_mouse: Optional[bool] = False


class Size:
    def __init__(self, scale: float):
        self.text = 24 * scale
        self.height = self.text * 2
        self.width = self.height * 2.5
        self.radius = self.width * 1.25
        self.corner_radius = self.text / 2
        self.margin = self.height * 0.25
        self.offset = 2 * self.radius
        self.snap_width = self.width * 1.5


ctx = Context()
ctx.matches = r"""
mode: all
and mode: command
mode: all
and mode: dictation
"""

mod = Module()
size: Size = None
canvas: Canvas = None
mouse_pos: Point2d = None
hover_rect: Rect = None
repeater_callback: Callable[[], None] = None
buttons: list[Button] = []

circle_options = [
    CircleOption("DRAG", -90, actions.mouse_drag, True),
    CircleOption("CTRL", -140, lambda: actions.user.mouse_click("control"), True),
    CircleOption("RIGHT", -40, lambda: actions.user.mouse_click("right"), True),
    CircleOption("←", -170, actions.user.go_back),
    CircleOption("→", -10, actions.user.go_forward),
    CircleOption("X", 13, actions.app.tab_close),
    CircleOption("TASK", 140, lambda: actions.key("ctrl-shift-escape")),
    CircleOption("WIN", 40, lambda: actions.user.window_switcher_menu()),
    CircleOption("SEARCH", 90, actions.user.browser_search_selected),
]

# Icon rendering requires a font that covers the codepoint (see FONT_FAMILY above).
# With DejaVu Sans (not installed on Windows) ALL icons below fail to render.
# With Segoe UI Symbol both sets work:
#   original U+23xx media transport symbols: ⏮ U+23EE, ⏯ U+23EF, ⏭ U+23ED
#   geometric shape alternatives: ◀◀ U+25C0, ▶‖ U+25B6+U+2016, ▶▶ U+25B6
media_options = [
    Option("◀◀", lambda: actions.key("prev")),
    Option("▶‖", lambda: actions.key("play_pause")),
    Option("▶▶", lambda: actions.key("next")),
]

snap_positions = [
    ["left", "right"],
    ["full"],
    ["top", "bottom"],
    ["left large"],
    ["center"],
    ["right large"],
    ["top left large", "bottom left large"],
    ["top center small", "bottom center small"],
    ["top right large", "bottom right large"],
    ["left small", "center small", "right small"],
    ["top left", "top right", "bottom left", "bottom right"],
    [
        "top left small",
        "top center small",
        "top right small",
        "bottom left small",
        "bottom center small",
        "bottom right small",
    ],
    [],
    ["center"],
]


def get_midpoint(length: int, value: float):
    return (length * value + (length - 1) * size.margin) / 2


def add_button(c: SkiaCanvas, text: str, rect: Rect):
    rrect = RoundRect.from_rect(rect, x=size.corner_radius, y=size.corner_radius)

    c.paint.style = c.paint.Style.FILL
    c.paint.color = HOVER_COLOR if hover_rect == rect else BACKGROUND_COLOR
    c.draw_rrect(rrect)

    c.paint.style = c.paint.Style.STROKE
    c.paint.color = BORDER_COLOR
    c.draw_rrect(rrect)

    c.paint.style = c.paint.Style.FILL
    c.paint.color = TEXT_COLOR
    c.paint.textsize = size.text

    if len(text) > 10:
        text = text[:10]

    text_rect = c.paint.measure_text(text)[1]
    c.draw_text(
        text,
        rect.center.x + text_rect.x - text_rect.width / 2,
        rect.center.y - text_rect.y - text_rect.height / 2,
    )


def draw_horizontal(c: SkiaCanvas, options: list[Option], x: float, y: float):
    x -= get_midpoint(len(options), size.width)
    y -= size.height / 2
    for option in options:
        rect = Rect(x, y, size.width, size.height)
        x += size.width + size.margin
        buttons.append(Button(rect, option.callback, option.move_mouse))
        add_button(c, option.text, rect)


def draw_vertical(c: SkiaCanvas, options: list[Option], x: float, y: float):
    x -= size.width / 2
    y -= get_midpoint(len(options), size.height)
    for option in options:
        rect = Rect(x, y, size.width, size.height)
        y += size.height + size.margin
        buttons.append(Button(rect, option.callback, option.move_mouse))
        add_button(c, option.text, rect)


def draw_circle(c: SkiaCanvas, options: list[CircleOption], cx: float, cy: float):
    for option in options:
        radians = math.radians(option.degrees)
        x = cx + size.radius * math.cos(radians)
        y = cy + size.radius * 1.25 * math.sin(radians)
        rect = Rect(x - size.width / 2, y - size.height / 2, size.width, size.height)
        buttons.append(Button(rect, option.callback, option.move_mouse))
        add_button(c, option.text, rect)


def draw_snap_positions(
    c: SkiaCanvas, positions: list[list[str]], org_x: float, y: float
):
    height = size.snap_width * c.height / c.width
    x = org_x
    y -= get_midpoint(math.ceil(len(positions) / 3), height)

    for i, group in enumerate(positions):
        rect = Rect(x, y, size.snap_width, height)
        if i % 3 == 2:
            x = org_x
            y += height + size.margin
        else:
            x += size.snap_width + size.margin

        if len(group) == 0:
            continue

        c.paint.style = c.paint.Style.FILL
        c.paint.color = BACKGROUND_COLOR
        c.draw_rect(rect)

        for j, position in enumerate(group):
            pos_rect = actions.user.snap_apply_position_to_rect(rect, position)

            def callback(position=position):
                return actions.user.snap_active_window_to_position(position)

            buttons.append(Button(pos_rect, callback))
            c.paint.color = BORDER_COLOR if hover_rect == pos_rect else SNAP_COLORS[j]
            c.draw_rect(pos_rect)

        c.paint.style = c.paint.Style.STROKE
        c.paint.color = BORDER_COLOR
        c.draw_rect(rect)


def get_running_options() -> list[Option]:
    try:
        running = actions.user.get_running_applications()
    except Exception:
        return []

    if not isinstance(running, dict):
        return []

    return [
        Option(key, lambda key=key: actions.user.window_focus_name(running[key]))
        for key in sorted(running)
    ]


def on_draw(c: SkiaCanvas):
    global buttons
    buttons = []

    c.paint.typeface = FONT_FAMILY

    draw_circle(
        c,
        circle_options,
        c.rect.center.x,
        c.rect.center.y,
    )

    draw_vertical(
        c,
        get_running_options(),
        c.rect.center.x - size.offset - size.width / 2,
        c.rect.center.y,
    )

    draw_horizontal(
        c,
        media_options,
        c.rect.center.x,
        c.rect.center.y + size.offset + size.height / 2,
    )

    draw_snap_positions(
        c,
        snap_positions,
        c.rect.center.x + size.offset,
        c.rect.center.y,
    )


def get_button_for_position(pos: Point2d):
    for button in buttons:
        if button.rect.contains(pos):
            return button
    return None


def run_callback(callback: Callable[[], None]) -> bool:
    try:
        callback()
        return True
    except Exception:
        return False


def on_mouse(e: MouseEvent):
    global repeater_callback, hover_rect
    button = get_button_for_position(e.gpos)

    if e.event == "mousemove":
        hover_rect_new = button.rect if button else None
        if hover_rect != hover_rect_new:
            hover_rect = hover_rect_new
            canvas.freeze()

    elif e.event == "mouseup" and e.button == 0:
        hide()
        if button:
            if button.move_mouse:
                actions.mouse_move(mouse_pos.x, mouse_pos.y)
            actions.sleep("150ms")
            if run_callback(button.callback):
                repeater_callback = button.callback


def show():
    global canvas, mouse_pos, size
    mouse_pos = Point2d(actions.mouse_x(), actions.mouse_y())
    screen: Screen = ui.main_screen()
    size = Size(screen.scale)
    canvas = Canvas.from_screen(screen)
    canvas.blocks_mouse = True
    canvas.register("draw", on_draw)
    canvas.register("mouse", on_mouse)
    canvas.freeze()


def hide():
    global canvas
    canvas.unregister("draw", on_draw)
    canvas.unregister("mouse", on_mouse)
    canvas.close()
    canvas = None


# @ctx.action_class("user")
# class UserActions:
#     def noise_cluck():
#         # If available the repeat noise repeats the last quick pick callback
#         if repeater_callback:
#             run_callback(repeater_callback)
#         else:
#             actions.next()


@mod.action_class
class Actions:
    def quick_pick_show():
        """Show quick pick"""
        if not canvas:
            show()
        else:
            hide()


def on_post_phrase(phrase: Phrase):
    global repeater_callback
    # On each spoken phrase the repeater noise returns to default implementation
    if repeater_callback and phrase.get("phrase"):
        repeater_callback = None


speech_system.register("post:phrase", on_post_phrase)
