/**
 * Parses a string in Forsyth-Edwards Notation into a 2D array
 * @param fen 
 * @returns 2D array
 */
const parseFEN = (fen: string): string[][] => {
    const placement = fen.split(" ")[0]
    const rows = placement.split("/")

    const board: string[][] = []
    for (let i = 0; i < 8; i++) {
        board.push([])
    }

    for (let i = 0; i < 8; i++) {
        const row = rows[i]
        for (const c of row) {
            if (isNaN(Number(c))) {
                board[i].push(c)
            } else {
                // row contains a number n. We need to add n empty spaces
                const n = Number(c)
                for (let j = 0; j < n; j++) {
                    board[i].push("")
                }
            }
        }
    }
    return board
}

export default parseFEN