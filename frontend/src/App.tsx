import { useState } from "react"
import DrawBoard from "./components/DrawBoard"
import parseFEN from "./utils/parseFEN"

// Starting position in FEN notation
const START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

function App() {
    const [board, setBoard] = useState<string[][]>(() => parseFEN(START))

    // Just a dummy move handler for testing that everything works.
    // Real app would send the move to the backend
    const handleDummyMove = (fromRow: number, fromCol: number, toRow: number, toCol: number) => {
        // Create a new board to trigger a re-render
        const newBoard = board.map(row => [...row])

        const movingPiece = newBoard[fromRow][fromCol]

        if (movingPiece) {
            newBoard[toRow][toCol] = movingPiece
            newBoard[fromRow][fromCol] = ""
            setBoard(newBoard)
        }
    }

    return (
        <>
            <DrawBoard board={board} onMove={handleDummyMove}/>
        </>
    )
}

export default App
