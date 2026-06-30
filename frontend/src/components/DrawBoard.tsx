import { useState } from "react"

interface DrawBoardProps {
    board: string[][]
    onMove: (fromRow: number, fromCol: number, toRow: number, toCol: number) => void
    getValidSquares: (from: [number, number]) => Promise<number[][]>
}

const CELL_SIZE = 64

const getPieceImage = (char: string) => {
    if (!char) return undefined // Return undefined for empty cells

    switch (char) {
        case "P": return "https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg"
        case "N": return "https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg"
        case "B": return "https://upload.wikimedia.org/wikipedia/commons/b/b1/Chess_blt45.svg"
        case "R": return "https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg"
        case "Q": return "https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg"
        case "K": return "https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_klt45.svg"
        case "p": return "https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg"
        case "n": return "https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg"
        case "b": return "https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg"
        case "r": return "https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg"
        case "q": return "https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg"
        case "k": return "https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg"
        default: return undefined
    }
}


const DrawBoard = ({ board, onMove, getValidSquares }: DrawBoardProps) => {
    const [highlightCells, setHighlightCells] = useState<number[][]>([])

    const handleDragStart = async (e: React.DragEvent, row: number, col: number) => {
        e.dataTransfer.setData("text/plain", JSON.stringify({ row, col }))
        const validSquares = await getValidSquares([row, col])
        setHighlightCells(validSquares)
    }

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault()
    }

    const handleDrop = (e: React.DragEvent, toRow: number, toCol: number) => {
        setHighlightCells([])

        e.preventDefault()
        try {
            const data = e.dataTransfer.getData("text/plain")
            if (!data) return

            const parsedObject = JSON.parse(data)
            const fromRow = parsedObject.row
            const fromCol = parsedObject.col

            // Prevent moving to the same square
            // Should be handled in the backend, DELETE THIS CHECK
            if (fromRow === toRow && fromCol === toCol) return
            
            onMove(fromRow, fromCol, toRow, toCol)
        } catch (err) {
            console.error("Failed to parse drag data", err)
        }
    }

    return (
        <div style={{ userSelect: "none" }}>
            {board.map((row, rowIndex) => (
                <div key={rowIndex} style={{ display: "flex" }}>
                    {row.map((cell, colIndex) => {
                        const imgSrc = getPieceImage(cell)
                        const isLightSquare = (rowIndex + colIndex) % 2 === 0

                        return (
                            <div className={highlightCells.some(([r, c]) => r === rowIndex && c === colIndex) ? "highlight" : ""}
                                key={colIndex} 
                                onDragOver={handleDragOver}
                                onDrop={(e) => handleDrop(e, rowIndex, colIndex)}
                                style={{ 
                                    display: "flex", 
                                    justifyContent: "center", 
                                    alignItems: "center", 
                                    width: CELL_SIZE, 
                                    height: CELL_SIZE, 
                                    backgroundColor: isLightSquare ? "#eeeed2" : "#769656"
                                }}
                            >
                                {imgSrc && (
                                    <img 
                                        src={imgSrc} 
                                        alt={cell} 
                                        draggable={true}
                                        onDragStart={(e) => handleDragStart(e, rowIndex, colIndex)}
                                        style={{ width: "100%", height: "100%", cursor: "grab" }} 
                                    />
                                )}
                            </div>
                        )
                    })}
                </div>
            ))}
        </div>
    )
}

export default DrawBoard