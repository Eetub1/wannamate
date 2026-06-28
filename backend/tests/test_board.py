# This file is fully AI generated!

import pytest

from app.chess.board import parse_fen, to_fen, apply_move, algebraic_to_board_indices


# --- round-trip: parse then serialize should give back the original placement ---

ROUND_TRIP_PLACEMENTS = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",  # start
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR",  # after 1.e4 c5
    "8/8/8/8/8/8/8/8",  # empty board
    "8/8/8/8/4P3/8/8/8",  # single piece, trailing empties in a rank
    "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R",  # a midgame position
]


@pytest.mark.parametrize("placement", ROUND_TRIP_PLACEMENTS)
def test_round_trip(placement):
    assert to_fen(parse_fen(placement)) == placement


# --- parse_fen structure: check concrete squares, independent of to_fen ---

def test_parse_start_position_squares():
    board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

    assert len(board) == 8
    assert all(len(row) == 8 for row in board)

    assert board[0][0] == "r"   # a8 black rook
    assert board[0][4] == "k"   # e8 black king
    assert board[7][0] == "R"   # a1 white rook
    assert board[7][4] == "K"   # e1 white king

    assert board[1] == ["p"] * 8          # rank 7 all black pawns
    assert board[6] == ["P"] * 8          # rank 2 all white pawns
    assert board[3] == [""] * 8           # an empty rank


def test_parse_empty_board():
    board = parse_fen("8/8/8/8/8/8/8/8")
    assert board == [[""] * 8 for _ in range(8)]


# --- parse_fen validation: malformed input must raise ---

def test_parse_rejects_too_few_ranks():
    with pytest.raises(ValueError):
        parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP")  # only 7 ranks


def test_parse_rejects_bad_character():
    with pytest.raises(ValueError):
        parse_fen("rnbqkbXr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")  # 'X' is not a piece


# --- to_fen: collapses empties correctly, including the trailing-run edge case ---

def test_to_fen_start_position():
    board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    assert to_fen(board) == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


def test_to_fen_trailing_empties():
    # a rank that ends on empty squares — the flush-at-end-of-rank case
    board = parse_fen("8/8/8/8/8/8/8/4P3")
    assert to_fen(board) == "8/8/8/8/8/8/8/4P3"


# --- algebraic_to_board_indices: the conversion + the rank flip ---

def test_algebraic_corners():
    assert algebraic_to_board_indices("a1") == [7, 0]
    assert algebraic_to_board_indices("h8") == [0, 7]
    assert algebraic_to_board_indices("e2") == [6, 4]
    assert algebraic_to_board_indices("a8") == [0, 0]


@pytest.mark.parametrize("bad", ["e9", "e0", "z2", "a", "abc", "12"])
def test_algebraic_rejects_bad_input(bad):
    with pytest.raises(ValueError):
        algebraic_to_board_indices(bad)


# --- apply_move: mechanical move and capture, no legality ---

def test_apply_move_simple():
    board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    result = apply_move(board, "e2", "e4")

    assert result[4][4] == "P"   # e4 now has the white pawn
    assert result[6][4] == ""    # e2 is now empty


def test_apply_move_capture():
    # white pawn on e4, black pawn on d5; white captures d5
    board = parse_fen("8/8/8/3p4/4P3/8/8/8")
    result = apply_move(board, "e4", "d5")

    assert result[3][3] == "P"   # d5 now holds the white pawn
    assert result[4][4] == ""    # e4 is empty