from talon import Module, actions, cron, ctrl, settings, ui


mod = Module()
mod.setting(
    "hot_corners_enabled",
    type=bool,
    default=False,
    desc="Open the desktop switcher at top left or Quick Pick at top right",
)
mod.setting(
    "hot_corners_size",
    type=int,
    default=8,
    desc="Width and height in pixels of each enabled hot-corner area",
)

_corner_active = False


def _top_corner_at(x: int, y: int) -> str:
    corner_size = max(1, settings.get("user.hot_corners_size"))

    for screen in ui.screens():
        rect = screen.rect
        inside_top = rect.y <= y < rect.y + corner_size
        inside_left = rect.x <= x < rect.x + corner_size
        inside_right = rect.x + rect.width - corner_size <= x < rect.x + rect.width
        if inside_top and inside_right:
            return "right"
        if inside_top and inside_left:
            return "left"

    return ""


def _poll_hot_corners() -> None:
    global _corner_active

    if not settings.get("user.hot_corners_enabled"):
        _corner_active = False
        return

    x, y = ctrl.mouse_pos()
    corner = _top_corner_at(x, y)
    in_corner = bool(corner)
    if in_corner and not _corner_active:
        if corner == "right":
            actions.user.quick_pick_global_show()
        else:
            actions.user.desktop_show()

    _corner_active = in_corner


cron.interval("50ms", _poll_hot_corners)
