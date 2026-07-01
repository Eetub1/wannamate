import { useState } from "react"
import DrawBoard from "./components/DrawBoard"
import parseFen from "./utils/parseFen"
import indicesToAlgebraic from "./utils/indicesToAlgebraic"
import algebraicToIndices from "./utils/algebraicToIndices"

// Starting position in FEN notation
const START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

function App() {
    const [fen, setFen] = useState(START)

    const handleMove = (fromRow: number, fromCol: number, toRow: number, toCol: number, promotion: string) => {
        const from_square = indicesToAlgebraic([fromRow, fromCol])
        const to_square = indicesToAlgebraic([toRow, toCol])
        let content

        // Right now the promoted piece is always a queen
        // This should be asked on the frontend TODO
        if (promotion) {
            content = {fen, from_square, to_square, promotion: promotion}
        } else {
            content = {fen, from_square, to_square}
        }

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


    const getValidSquares = (from: [number, number]): Promise<number[][]> => {
        const content = { fen, square: indicesToAlgebraic(from) }

        return fetch("http://localhost:8000/api/moves", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(content)
        })
            .then(res => res.json())
            .then(data => data.valid_squares.map(algebraicToIndices))
            .catch(err => {
                console.error("Failed to get valid squares: ", err)
                return []
            })
    }


    return (
        <>
            <DrawBoard board={parseFen(fen)} handleMove={handleMove} getValidSquares={getValidSquares}/>
        </>
    )
}

export default App
