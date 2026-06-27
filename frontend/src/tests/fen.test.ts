import { describe, test, expect } from "vitest";

import parseFEN from "../utils/parseFEN";


describe("parseFEN function tests", () => {
    test("parseFEN should return a 2D array with 64 values", () => {
        const result = parseFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        expect(result).toBeInstanceOf(Array)
        expect(result).toHaveLength(8)

        result.forEach(row => {
            expect(row).toBeInstanceOf(Array)
            expect(row).toHaveLength(8)
        })
    })
})

