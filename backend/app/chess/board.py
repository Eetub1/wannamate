
def parse_fen(fen: str) -> list[list[str]]:
    """Parse a FEN string into a 2D board.

    Args:
        fen: A full FEN string. Only the first (piece-placement) field is used.

    Returns:
        An 8x8 grid where board[0] is rank 8 (top from White's view).
        Pieces are FEN chars ('K', 'p', ...); empty squares are "".
    """
    raise NotImplementedError  # TODO: take field 0, split ranks, expand digits


def to_fen(board: list[list[str]]) -> str:
    """Serialize a board back into a FEN piece-placement field.

    Args:
        board: An 8x8 grid as produced by parse_fen.

    Returns:
        The piece-placement field only (the part before the first space).
    """
    raise NotImplementedError  # TODO: inverse of parse — collapse empties into counts


def apply_move(board: list[list[str]], from_square: str, to_square: str) -> list[list[str]]:
    """Move a piece from one square to another. No legality checking.

    Args:
        board: The current board.
        from_square: Algebraic origin, e.g. "e2".
        to_square: Algebraic destination, e.g. "e4".

    Returns:
        The resulting board.
    """
    raise NotImplementedError  # TODO: convert squares -> indices, move piece, clear origin