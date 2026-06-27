import DrawBoard from "./components/DrawBoard"
import parseFEN from "./utils/parseFEN"

const START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

function App() {

    return (
        <>
            <DrawBoard board={parseFEN(START)}/>
        </>
    )
}

export default App
