from app.chess.board import indices_to_algebraic, algebraic_to_indices
from enum import Enum

class CellContentType(Enum):
    EMPTY = "empty"
    FRIEND = "friend"
    ENEMY = "enemy"

KNIGHT_OFFSETS = [
    (-2, -1), (-2, 1),
    (-1, -2), (-1, 2),
    (1, -2),  (1, 2),
    (2, -1),  (2, 1)
]


def is_position_inbounds(position: list[int]) -> bool:
    """Return True if [row, col] falls within the 8x8 board."""
    row, col = position
    if row < 0 or row >= 8 or col < 0 or col >= 8:
        return False
    return True


def calculate_moves(board: list[list[str]], position: str) -> list[str]:
    """Return the pseudo-legal moves for whatever piece sits on `position`.

    Dispatches to a per-piece generator based on the piece type. Does not
    consider checks. Returns an empty list if the square is empty.

    Args:
        board: The current board.
        position: The square to generate moves from, in algebraic notation.

    Returns:
        A list of destination squares in algebraic notation, e.g. ["c3", "e4"].
    """
    row, col = algebraic_to_indices(position)
    piece = board[row][col]

    if not piece:  # ignore empty squares
        return []

    is_white = piece == piece.upper()

    possibilities = []
    match piece.lower():
        case "r":
            pass
        case "n":
            possibilities = calculate_knight_moves(board, [row, col], is_white)
        case "b":
            pass
        case "q":
            pass
        case "k":
            pass
        case "p":
            pass
    return possibilities


def square_state(board: list[list[str]], position: list[int], is_white: bool) -> CellContentType:
    """Classify a target square relative to the moving piece's color.

    Args:
        board: The current board.
        position: The [row, col] of the square to classify.
        is_white: True if the moving piece is white.

    Returns:
        EMPTY, FRIEND, or ENEMY depending on the square's contents.
    """
    row, col = position
    cell_content = board[row][col]

    if cell_content == "":
        return CellContentType.EMPTY

    if is_white:
        if cell_content == cell_content.lower():
            return CellContentType.ENEMY
        else:
            return CellContentType.FRIEND
    else:
        if cell_content == cell_content.upper():
            return CellContentType.ENEMY
        else:
            return CellContentType.FRIEND


def calculate_knight_moves(board: list[list[str]], position: list[int], is_white: bool) -> list[str]:
    """Generate pseudo-legal knight moves from `position`.

    A knight jumps to its eight L-shaped offsets, ignoring anything in between.
    A target is valid unless it holds a friendly piece (off-board targets and
    friendly-occupied targets are skipped; empty and enemy targets are allowed).

    Args:
        board: The current board.
        position: The knight's square as [row, col].
        is_white: True if the knight is white.

    Returns:
        Destination squares in algebraic notation.
    """
    row, col = position

    valid_squares = []
    for dy, dx in KNIGHT_OFFSETS:
        n_row, n_col = row + dy, col + dx
        if not is_position_inbounds([n_row, n_col]):
            continue

        content = square_state(board, [n_row, n_col], is_white)
        if content != CellContentType.FRIEND:
            valid_squares.append(indices_to_algebraic([n_row, n_col]))
    return valid_squares