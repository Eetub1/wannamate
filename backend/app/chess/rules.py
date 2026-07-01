"""Chess rules and legality: check detection and legal-move filtering.

This module sits on top of move generation. The dependency flows one way:
rules.py -> moves.py -> board.py (never backward), which avoids circular imports.

Key distinction this module enforces:
  - PSEUDO-LEGAL moves (from moves.py) ignore check.
  - LEGAL moves are pseudo-legal moves that don't leave your own king in check.
"""

from app.chess.board import apply_move, indices_to_algebraic, algebraic_to_indices
from app.chess.moves import calculate_moves, is_position_inbounds, square_state, CellContentType
from enum import Enum

class GameState(Enum):
    ONGOING = "ongoing"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"

def find_king(board: list[list[str]], is_white: bool) -> list[int]:
    """Locate the given side's king on the board.

    Args:
        board: The current board.
        is_white: True to find the white king ("K"), False for black ("k").

    Returns:
        The king's square as [row, col].

    Raises:
        ValueError: If no such king is on the board (should never happen in a
            real game, but worth failing loudly rather than returning nonsense).
    """
    target = "K" if is_white else "k"

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == target:
                return [i, j]

    raise ValueError("Couldn't find the given side's king on board")


def is_square_attacked(board: list[list[str]], square: list[int], by_white: bool) -> bool:
    """Return True if `square` is attacked by any piece of the given color.

    This is the core primitive: check detection is just "is the king's square
    attacked by the enemy?"

    Args:
        board: The current board.
        square: The [row, col] being tested.
        by_white: True to test for attacks by white pieces, False for black.

    Returns:
        True if at least one piece of color `by_white` attacks `square`.
    """
    t_row, t_col = square

    for row in range(len(board)):
        for col in range(len(board[0])):
            contains = board[row][col]

            if (not contains
                or (not by_white and contains.upper() == contains) 
                or (by_white and contains.lower() == contains)):
                continue

            if contains.lower() == "p": # Handle pawn separately
                offsets = [(-1, 1), (-1, -1)] if by_white else [(1, 1), (1, -1)]

                valid_squares = []

                # Check if pawn can attack left and right
                for dy, dx in offsets:
                    n_row = row + dy
                    n_col = col + dx
                    if is_position_inbounds([n_row, n_col]):
                        valid_squares.append(indices_to_algebraic([n_row, n_col]))
            else:
                valid_squares = calculate_moves(board, indices_to_algebraic([row, col]))
            
            if indices_to_algebraic([t_row, t_col]) in valid_squares:
                return True
    return False


def is_in_check(board: list[list[str]], is_white: bool) -> bool:
    """Return True if the given side's king is currently in check.

    Args:
        board: The current board.
        is_white: True to test the white king, False for black.

    Returns:
        True if that king's square is attacked by the opponent.
    """
    location = find_king(board, is_white)
    return is_square_attacked(board, location, not is_white)


def is_move_legal(board: list[list[str]], from_square: str, to_square: str, is_white: bool) -> bool:
    """Return True if making this move does NOT leave the mover's own king in check.

    Args:
        board: The current board.
        from_square: Algebraic origin, e.g. "e2".
        to_square: Algebraic destination, e.g. "e4".
        is_white: True if the moving side is white.

    Returns:
        True if the resulting position has the mover's own king safe.
    """
    new_board = apply_move(board, from_square, to_square)
    return not is_in_check(new_board, is_white)


def calculate_legal_moves(board: list[list[str]], position: str, is_whites_turn: bool) -> list[str]:
    """Return the fully-legal moves for the piece on `position`.

    Pseudo-legal moves (from moves.py) filtered down to those that don't leave
    the mover's own king in check. This is what the rest of the app should use
    for "what can this piece actually do."

    Args:
        board: The current board.
        position: The square to generate moves from, in algebraic notation.
        is_whites_turn: True if it is white's turn.

    Returns:
        Legal destination squares in algebraic notation.
    """
    row, col = algebraic_to_indices(position)
    piece = board[row][col]

    if not piece:  # ignore empty squares
        return []

    is_white = piece == piece.upper()

    # if it is whites turn and the piece is not white, return empty
    # and vice versa for black
    if is_whites_turn != is_white:
        return []

    all_moves = calculate_moves(board, position)
    return [move for move in all_moves if is_move_legal(board, position, move, is_white)]


def is_stalemate_or_checkmate(board: list[list[str]], is_whites_turn: bool) -> GameState:
    """Determine whether the side to move is checkmated, stalemated, or neither.

    Checks whether the side to move has ANY legal move. If it does, the game is
    ongoing. If it has none, the result depends on whether that side is in check:
    no legal moves while in check is checkmate; no legal moves while not in check
    is stalemate.

    Important: `is_whites_turn` must be the side whose turn it is NOW — i.e. the
    side that must respond, not the side that just moved. Callers processing a
    move should pass this AFTER flipping the turn.

    Args:
        board: The current board (after the move has been applied).
        is_whites_turn: True if it is white's turn to move.

    Returns:
        GameState.ONGOING if the side to move has at least one legal move,
        GameState.CHECKMATE if it has none and is in check,
        GameState.STALEMATE if it has none and is not in check.
    """
    # Does the side to move have any legal moves
    for i in range(len(board)):
        for j in range(len(board[0])):
            content = board[i][j]
            if not content:
                continue

            is_white_piece = content == content.upper()

            # only consider pieces belonging to the side to move
            if is_whites_turn == is_white_piece:
                legal_moves = calculate_legal_moves(board, indices_to_algebraic([i, j]), is_whites_turn)
                if legal_moves:
                    return GameState.ONGOING

    is_check = is_in_check(board, is_whites_turn)
    if is_check:
        return GameState.CHECKMATE
    return GameState.STALEMATE

