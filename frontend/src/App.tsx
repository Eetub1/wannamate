import { useState, useEffect } from "react"
import DrawBoard from "./components/DrawBoard"
import parseFen from "./utils/parseFen"
import indicesToAlgebraic from "./utils/indicesToAlgebraic"

// Starting position in FEN notation
const START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

function App() {
    const [fen, setFen] = useState(START)

    // Testing the backend
    /*useEffect(() => {
        fetch("http://localhost:8000/api/health")
            .then(res => res.json())
    }, [])*/


    // Just a dummy move handler for testing that everything works.
    // Real app would send the move to the backend
    /*const handleDummyMove = (fromRow: number, fromCol: number, toRow: number, toCol: number) => {
        // Create a new board to trigger a re-render
        const newBoard = board.map(row => [...row])

        const movingPiece = newBoard[fromRow][fromCol]

        if (movingPiece) {
            newBoard[toRow][toCol] = movingPiece
            newBoard[fromRow][fromCol] = ""
            setBoard(newBoard)
        }
    }*/

    const handleMove = (fromRow: number, fromCol: number, toRow: number, toCol: number) => {
        const from_square = indicesToAlgebraic([fromRow, fromCol])
        const to_square = indicesToAlgebraic([toRow, toCol])
        const content = {fen, from_square, to_square}

        fetch("http://localhost:8000/api/move", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(content)       
        })
            .then(res => res.json())
            .then(data => {
                if (data.fen) {
                    setFen(data.fen)
                } else {
                    console.error("Invalid response from backend: ", data)
                }
            })
            .catch(err => console.error("Failed to send move to backend: ", err))
    }


    return (
        <>
            <DrawBoard board={parseFen(fen)} onMove={handleMove}/>
        </>
    )
}

export default App
