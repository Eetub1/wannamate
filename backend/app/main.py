from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.chess.board import parse_fen, apply_move, to_fen

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
    from_square: str # these are both in algebraic notation, so "e4"
    to_square: str

class MoveResponse(BaseModel):
    fen: str
    legal: bool


@app.post("/api/move", response_model=MoveResponse)
def make_move(req: MoveRequest):
    fen_parts = req.fen.split(" ")
    fen_placement = fen_parts[0]
    fen_tail = fen_parts[1:]
    fen_tail = " ".join(fen_tail)
    
    try:
        board = parse_fen(fen_placement)
        board = apply_move(board, req.from_square, req.to_square) # Move should be validated before applying TODO
        fen_placement = to_fen(board)

        fen = fen_placement + " " + fen_tail
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # right now every move is true
    return MoveResponse(fen=fen, legal=True)