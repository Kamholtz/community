from talon import Module, ctrl, ui


mod = Module()


@mod.action_class
class Actions:
    def mouse_position(square: int):
        """Move the mouse to the centre of one of the nine main-screen squares."""
        if square < 1 or square > 9:
            return

        rect = ui.main_screen().rect
        column = (square - 1) % 3
        row = 2 - (square - 1) // 3

        x = rect.x + (column + 0.5) * rect.width / 3
        y = rect.y + (row + 0.5) * rect.height / 3
        ctrl.mouse_move(x, y)
