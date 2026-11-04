from talon import Module, ctrl, ui


mod = Module()


def square_centre(x: float, y: float, width: float, height: float, square: int):
    """Return the centre of a numpad-oriented square within the given bounds."""
    column = (square - 1) % 3
    row = 2 - (square - 1) // 3
    return (
        x + (column + 0.5) * width / 3,
        y + (row + 0.5) * height / 3,
    )


@mod.action_class
class Actions:
    def mouse_position(square: int):
        """Move the mouse to the centre of one of the nine main-screen squares."""
        if square < 1 or square > 9:
            return

        rect = ui.main_screen().rect
        x, y = square_centre(rect.x, rect.y, rect.width, rect.height, square)
        ctrl.mouse_move(x, y)

    def mouse_position_recursive(first_square: int, second_square: int):
        """Move to a square nested inside one of the nine main-screen squares."""
        if not 1 <= first_square <= 9 or not 1 <= second_square <= 9:
            return

        rect = ui.main_screen().rect
        first_column = (first_square - 1) % 3
        first_row = 2 - (first_square - 1) // 3
        cell_width = rect.width / 3
        cell_height = rect.height / 3

        x, y = square_centre(
            rect.x + first_column * cell_width,
            rect.y + first_row * cell_height,
            cell_width,
            cell_height,
            second_square,
        )
        ctrl.mouse_move(x, y)
