from dataclasses import dataclass
from typing import Callable, Optional
import math
import os
import platform
import struct

from talon import Context, Module, actions, speech_system, ui
from talon.canvas import Canvas, MouseEvent
from talon.grammar import Phrase
from talon.screen import Screen
from talon.skia import Canvas as SkiaCanvas
from talon.skia import RoundRect
from talon.types import Point2d, Rect

# NOTE: This file was originally copied from
# C:\Users\carlk\repos\andreas-talon\plugins\quick_pick\quick_pick.py.
# It now exposes reusable menu/view objects so app contexts can provide their
# own quick-pick panels while retaining the original global menu.

FONT_FAMILY = "Segoe UI Symbol"


def _find_font_path(font_name: str) -> str | None:
    """Return the file path for font_name via the Windows font registry, or None."""
    if platform.system() != "Windows":
        return None
    import winreg

    try:
        key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as hkey:
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(hkey, i)
                    if font_name.lower() in name.lower():
                        font_dir = os.path.join(
                            os.environ.get("WINDIR", r"C:\Windows"), "Fonts"
                        )
                        return os.path.join(font_dir, value)
                    i += 1
                except OSError:
                    break
    except Exception:
        pass
    return None


def _font_covers(font_path: str, codepoint: int) -> bool:
    """Return True if the TTF/OTF font file has a glyph for codepoint."""
    try:
        with open(font_path, "rb") as f:
            data = f.read()
        num_tables = struct.unpack_from(">H", data, 4)[0]
        for i in range(num_tables):
            tag = data[12 + i * 16 : 12 + i * 16 + 4].decode(
                "ascii", errors="ignore"
            )
            if tag != "cmap":
                continue
            cmap_off = struct.unpack_from(">I", data, 12 + i * 16 + 8)[0]
            n_sub = struct.unpack_from(">H", data, cmap_off + 2)[0]
            for j in range(n_sub):
                sub_off = cmap_off + struct.unpack_from(
                    ">I", data, cmap_off + 4 + j * 8 + 4
                )[0]
                fmt = struct.unpack_from(">H", data, sub_off)[0]
                if fmt == 4 and codepoint <= 0xFFFF:
                    seg_count = struct.unpack_from(">H", data, sub_off + 6)[0] // 2
                    ends = [
                        struct.unpack_from(">H", data, sub_off + 14 + k * 2)[0]
                        for k in range(seg_count)
                    ]
                    starts = [
                        struct.unpack_from(
                            ">H", data, sub_off + 16 + seg_count * 2 + k * 2
                        )[0]
                        for k in range(seg_count)
                    ]
                    if any(s <= codepoint <= e for s, e in zip(starts, ends)):
                        return True
                elif fmt == 12:
                    n_groups = struct.unpack_from(">I", data, sub_off + 12)[0]
                    for k in range(n_groups):
                        start = struct.unpack_from(">I", data, sub_off + 16 + k * 12)[
                            0
                        ]
                        end = struct.unpack_from(
                            ">I", data, sub_off + 16 + k * 12 + 4
                        )[0]
                        if start <= codepoint <= end:
                            return True
    except Exception:
        pass
    return False


_font_path = _find_font_path(FONT_FAMILY)
_has_media = _font_path is not None and _font_covers(_font_path, 0x23EE)

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
class QuickPickOption:
    text: str
    callback: Callable[[], None]
    move_mouse: Optional[bool] = False


@dataclass
class QuickPickCircleOption:
    text: str
    degrees: int
    callback: Callable[[], None]
    move_mouse: Optional[bool] = False


@dataclass
class QuickPickView:
    circle_options: list[QuickPickCircleOption]
    left_options: Optional[list[QuickPickOption]] = None
    bottom_options: Optional[list[QuickPickOption]] = None
    snap_positions: Optional[list[list[str]]] = None


@dataclass
class QuickPickMenu:
    id: str
    title: str
    view_provider: Callable[[], QuickPickView]


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
size: Optional[Size] = None
canvas: Optional[Canvas] = None
mouse_pos: Optional[Point2d] = None
hover_rect: Optional[Rect] = None
repeater_callback: Optional[Callable[[], None]] = None
buttons: list[Button] = []
current_menu: Optional[QuickPickMenu] = None

circle_options = [
    QuickPickCircleOption("DRAG", -90, actions.mouse_drag, True),
    QuickPickCircleOption("CTRL", -140, lambda: actions.user.mouse_click("control"), True),
    QuickPickCircleOption("RIGHT", -40, lambda: actions.user.mouse_click("right"), True),
    QuickPickCircleOption("BACK", -170, actions.user.go_back),
    QuickPickCircleOption("FWD", -10, actions.user.go_forward),
    QuickPickCircleOption("CLOSE", 13, actions.app.tab_close),
    QuickPickCircleOption("TASK", 140, lambda: actions.key("ctrl-shift-escape")),
    QuickPickCircleOption("WIN", 40, lambda: actions.user.window_switcher_menu()),
    QuickPickCircleOption("SEARCH", 90, actions.user.browser_search_selected),
]

media_options = [
    QuickPickOption("PREV" if not _has_media else "PREV", lambda: actions.key("prev")),
    QuickPickOption("PLAY", lambda: actions.key("play_pause")),
    QuickPickOption("NEXT", lambda: actions.key("next")),
    QuickPickOption("EYE OFF", lambda: actions.tracking.control_toggle(False)),
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
    if not size or length <= 0:
        return 0
    return (length * value + (length - 1) * size.margin) / 2


def add_button(c: SkiaCanvas, text: str, rect: Rect):
    if not size:
        return

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


def draw_horizontal(c: SkiaCanvas, options: list[QuickPickOption], x: float, y: float):
    if not size:
        return

    x -= get_midpoint(len(options), size.width)
    y -= size.height / 2
    for option in options:
        rect = Rect(x, y, size.width, size.height)
        x += size.width + size.margin
        buttons.append(Button(rect, option.callback, option.move_mouse))
        add_button(c, option.text, rect)


def draw_vertical(c: SkiaCanvas, options: list[QuickPickOption], x: float, y: float):
    if not size:
        return

    x -= size.width / 2
    y -= get_midpoint(len(options), size.height)
    for option in options:
        rect = Rect(x, y, size.width, size.height)
        y += size.height + size.margin
        buttons.append(Button(rect, option.callback, option.move_mouse))
        add_button(c, option.text, rect)


def draw_circle(
    c: SkiaCanvas, options: list[QuickPickCircleOption], cx: float, cy: float
):
    if not size:
        return

    for option in options:
        radians = math.radians(option.degrees)
        x = cx + size.radius * math.cos(radians)
        y = cy + size.radius * 1.25 * math.sin(radians)
        rect = Rect(x - size.width / 2, y - size.height / 2, size.width, size.height)
        buttons.append(Button(rect, option.callback, option.move_mouse))
        add_button(c, option.text, rect)


def draw_snap_positions(c: SkiaCanvas, positions: list[list[str]], org_x: float, y: float):
    if not size:
        return

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


def get_running_options() -> list[QuickPickOption]:
    try:
        running = actions.user.get_running_applications()
    except Exception:
        return []

    if not isinstance(running, dict):
        return []

    return [
        QuickPickOption(key, lambda key=key: actions.user.window_focus_name(running[key]))
        for key in sorted(running)
    ]


def get_app_menu() -> Optional[QuickPickMenu]:
    try:
        menu = actions.user.quick_pick_app_menu_get()
    except Exception:
        return None
    return menu if isinstance(menu, QuickPickMenu) else None


def get_global_view() -> QuickPickView:
    options = list(circle_options)
    if get_app_menu():
        options.append(
            QuickPickCircleOption("APP", -225, actions.user.quick_pick_app_show)
        )

    return QuickPickView(
        circle_options=options,
        left_options=get_running_options(),
        bottom_options=media_options,
        snap_positions=snap_positions,
    )


def get_global_menu() -> QuickPickMenu:
    return QuickPickMenu("global", "Global", get_global_view)


def on_draw(c: SkiaCanvas):
    global buttons
    buttons = []

    c.paint.typeface = FONT_FAMILY
    view = current_menu.view_provider() if current_menu else get_global_view()

    draw_circle(c, view.circle_options, c.rect.center.x, c.rect.center.y)

    if view.left_options:
        draw_vertical(
            c,
            view.left_options,
            c.rect.center.x - size.offset - size.width / 2,
            c.rect.center.y,
        )

    if view.bottom_options:
        draw_horizontal(
            c,
            view.bottom_options,
            c.rect.center.x,
            c.rect.center.y + size.offset + size.height / 2,
        )

    if view.snap_positions:
        draw_snap_positions(
            c, view.snap_positions, c.rect.center.x + size.offset, c.rect.center.y
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
    global hover_rect, repeater_callback
    button = get_button_for_position(e.gpos)

    if e.event == "mousemove":
        hover_rect_new = button.rect if button else None
        if hover_rect != hover_rect_new:
            hover_rect = hover_rect_new
            if canvas:
                canvas.freeze()

    elif e.event == "mouseup" and e.button == 0:
        hide()
        if button:
            if button.move_mouse and mouse_pos:
                actions.mouse_move(mouse_pos.x, mouse_pos.y)
            actions.sleep("150ms")
            if run_callback(button.callback):
                repeater_callback = button.callback


def show(menu: QuickPickMenu):
    global canvas, current_menu, mouse_pos, size
    if canvas:
        hide()

    current_menu = menu
    mouse_pos = Point2d(actions.mouse_x(), actions.mouse_y())
    screen: Screen = ui.main_screen()
    size = Size(screen.scale)
    canvas = Canvas.from_screen(screen)
    canvas.blocks_mouse = True
    canvas.register("draw", on_draw)
    canvas.register("mouse", on_mouse)
    canvas.freeze()


def hide():
    global canvas, current_menu, hover_rect
    if not canvas:
        return

    canvas.unregister("draw", on_draw)
    canvas.unregister("mouse", on_mouse)
    canvas.close()
    canvas = None
    current_menu = None
    hover_rect = None


@mod.action_class
class Actions:
    def quick_pick_show():
        """Show quick pick."""
        if not canvas:
            show(get_global_menu())
        else:
            hide()

    def quick_pick_global_show():
        """Show the global quick pick menu."""
        show(get_global_menu())

    def quick_pick_app_menu_get():
        """Return the active app quick pick menu, or None."""
        return None

    def quick_pick_app_show():
        """Show the active app quick pick menu if one is available."""
        menu = get_app_menu()
        if menu:
            show(menu)


def on_post_phrase(phrase: Phrase):
    global repeater_callback
    # On each spoken phrase the repeater noise returns to default implementation.
    if repeater_callback and phrase.get("phrase"):
        repeater_callback = None


speech_system.register("post:phrase", on_post_phrase)
