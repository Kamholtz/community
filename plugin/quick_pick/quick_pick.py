from talon import Module, Context, ui, speech_system, actions
from talon.screen import Screen
from talon.canvas import Canvas, MouseEvent
from talon.skia import RoundRect, Canvas as SkiaCanvas
from talon.types import Rect, Point2d
from talon.grammar import Phrase
from dataclasses import dataclass
from typing import Callable, Optional
import math, os, platform, struct

# NOTE: This file was originally copied from C:\Users\carlk\repos\andreas-talon\plugins\quick_pick\quick_pick.py
# it has been adopted so that it no longer produces errors on Linux and windows and remains a work in progress


# Font must be installed on the OS — Skia silently falls back to a font without
# symbol coverage if the name is not found. "Segoe UI Symbol" ships with Windows
# and covers ASCII, arrows, geometric shapes, and U+23xx media transport symbols,
# but lacks high-plane emoji (U+1F5xx, U+1F86x). A Nerd Font such as "Maple Mono
# NF" covers those but is not always present. _font_covers() detects availability
# at load time so each option list uses the best glyph the installed font provides.
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
                        font_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
                        return os.path.join(font_dir, value)
                    i += 1
                except OSError:
                    break
    except Exception:
        pass
    return None


def _font_covers(font_path: str, codepoint: int) -> bool:
    """Return True if the TTF/OTF font file has a glyph for codepoint.

    Checks cmap format 4 (BMP, U+0000–U+FFFF) and format 12 (full Unicode).
    """
    try:
        with open(font_path, "rb") as f:
            data = f.read()
        num_tables = struct.unpack_from(">H", data, 4)[0]
        for i in range(num_tables):
            tag = data[12 + i * 16 : 12 + i * 16 + 4].decode("ascii", errors="ignore")
            if tag != "cmap":
                continue
            cmap_off = struct.unpack_from(">I", data, 12 + i * 16 + 8)[0]
            n_sub = struct.unpack_from(">H", data, cmap_off + 2)[0]
            for j in range(n_sub):
                sub_off = cmap_off + struct.unpack_from(">I", data, cmap_off + 4 + j * 8 + 4)[0]
                fmt = struct.unpack_from(">H", data, sub_off)[0]
                if fmt == 4 and codepoint <= 0xFFFF:
                    seg_count = struct.unpack_from(">H", data, sub_off + 6)[0] // 2
                    ends   = [struct.unpack_from(">H", data, sub_off + 14 + k * 2)[0] for k in range(seg_count)]
                    starts = [struct.unpack_from(">H", data, sub_off + 16 + seg_count * 2 + k * 2)[0] for k in range(seg_count)]
                    if any(s <= codepoint <= e for s, e in zip(starts, ends)):
                        return True
                elif fmt == 12:
                    n_groups = struct.unpack_from(">I", data, sub_off + 12)[0]
                    for k in range(n_groups):
                        start = struct.unpack_from(">I", data, sub_off + 16 + k * 12)[0]
                        end   = struct.unpack_from(">I", data, sub_off + 16 + k * 12 + 4)[0]
                        if start <= codepoint <= end:
                            return True
    except Exception:
        pass
    return False


_font_path  = _find_font_path(FONT_FAMILY)
_has_emoji  = _font_path is not None and _font_covers(_font_path, 0x1F591)  # 🖑 high-plane
_has_media  = _font_path is not None and _font_covers(_font_path, 0x23EE)   # ⏮ U+23xx
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
    CircleOption("🖑" if _has_emoji else "DRAG",   -90,  actions.mouse_drag, True),
    CircleOption("🖖" if _has_emoji else "CTRL",   -140, lambda: actions.user.mouse_click("control"), True),
    CircleOption("🖙" if _has_emoji else "RIGHT",  -40,  lambda: actions.user.mouse_click("right"), True),
    CircleOption("🡨" if _has_emoji else "←",      -170, actions.user.go_back),
    CircleOption("🡪" if _has_emoji else "→",      -10,  actions.user.go_forward),
    CircleOption("╳",                              13,   actions.app.tab_close),
    CircleOption("🖳" if _has_emoji else "TASK",   140,  lambda: actions.key("ctrl-shift-escape")),
    CircleOption("🗗" if _has_emoji else "WIN",    40,   lambda: actions.user.window_switcher_menu()),
    CircleOption("🔍" if _has_emoji else "SEARCH", 90,   actions.user.browser_search_selected),
]

media_options = [
    Option("⏮" if _has_media else "◀◀", lambda: actions.key("prev")),
    Option("⏯" if _has_media else "▶‖",  lambda: actions.key("play_pause")),
    Option("⏭" if _has_media else "▶▶", lambda: actions.key("next")),
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
