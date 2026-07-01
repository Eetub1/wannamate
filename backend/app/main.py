from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.chess.board import parse_fen, apply_move, to_fen, flip_turn, algebraic_to_indices
from app.chess.moves import calculate_moves
from app.chess.rules import calculate_legal_moves, is_move_legal, is_stalemate_or_checkmate, GameState

app = FastAPI(title="Blunder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}


class MoveRequest(BaseModel):
    fen: str
    from_square: str # algebraic notation, i.e. "e4"
    to_square: str
    promotion: str | None = None # for example, "Q" means that a pawn can be promoted to white queen

class MoveResponse(BaseModel):
    fen: str
    legal: bool
    stalemate: bool | None = None
    checkmate: bool | None = None

class ValidSquaresRequest(BaseModel):
    fen: str
    square: str

class ValidSquaresResponse(BaseModel):
    valid_squares: list[str]


@app.post("/api/move", response_model=MoveResponse)
def make_move(req: MoveRequest):
    original_fen = req.fen
    fen_parts = req.fen.split(" ")
    fen_placement = fen_parts[0]
    fen_tail = fen_parts[1:]
    
    try:
        board = parse_fen(fen_placement)
        is_whites_turn = fen_parts[1].lower() == "w"

        # checking if move is legal
        legal_targets = calculate_legal_moves(board, req.from_square, is_whites_turn)
        if req.to_square not in legal_targets:
            return MoveResponse(fen=original_fen, legal=False)
        
        board = apply_move(board, req.from_square, req.to_square)

        # if the move is a promotion, put the correct promoted piece on board
        if req.promotion:
            row, col = algebraic_to_indices(req.to_square)
            board[row][col] = req.promotion

        fen_placement = to_fen(board)

        fen = fen_placement + " " + " ".join(fen_tail)
        fen = flip_turn(fen)
    
        game_result = is_stalemate_or_checkmate(board, not is_whites_turn)
        print(f"Game result: {game_result}")

        stalemate = game_result == GameState.STALEMATE
        checkmate = game_result == GameState.CHECKMATE
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return MoveResponse(fen=fen, legal=True, stalemate=stalemate, checkmate=checkmate)


@app.post("/api/moves", response_model=ValidSquaresResponse)
def get_valid_squares(req: ValidSquaresRequest):
    try:
        fen_pieces = req.fen.split(" ")
        board = parse_fen(fen_pieces[0])
        is_whites_turn = fen_pieces[1].lower() == "w"

        valid_squares = calculate_legal_moves(board, req.square, is_whites_turn)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return ValidSquaresResponse(valid_squares=valid_squares)