from talon import Module, actions, cron, ctrl, settings, ui


mod = Module()
mod.setting(
    "hot_corners_enabled",
    type=bool,
    default=False,
    desc="Open the desktop switcher when the pointer enters a top screen corner",
)
mod.setting(
    "hot_corners_size",
    type=int,
    default=8,
    desc="Width and height in pixels of each enabled hot-corner area",
)

_corner_active = False


def _is_in_top_corner(x: int, y: int) -> bool:
    corner_size = max(1, settings.get("user.hot_corners_size"))

    for screen in ui.screens():
        rect = screen.rect
        inside_top = rect.y <= y < rect.y + corner_size
        inside_left = rect.x <= x < rect.x + corner_size
        inside_right = rect.x + rect.width - corner_size <= x < rect.x + rect.width
        if inside_top and (inside_left or inside_right):
            return True

    return False


def _poll_hot_corners() -> None:
    global _corner_active

    if not settings.get("user.hot_corners_enabled"):
        _corner_active = False
        return

    x, y = ctrl.mouse_pos()
    in_corner = _is_in_top_corner(x, y)
    if in_corner and not _corner_active:
        actions.user.desktop_show()

    _corner_active = in_corner


cron.interval("50ms", _poll_hot_corners)
