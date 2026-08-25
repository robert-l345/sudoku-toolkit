"""Tests for sudoku_toolkit.solver."""

from __future__ import annotations

import unittest

from sudoku_toolkit.board import Board
from sudoku_toolkit.solver import solve

PUZZLE = """\
53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79
"""

SOLUTION = """\
534678912
672195348
198342567
859761423
426853791
713924856
961537284
287419635
345286179
"""

# Every cell but one is already filled, leaving a single legal value.
NEARLY_SOLVED = """\
53467891.
672195348
198342567
859761423
426853791
713924856
961537284
287419635
345286179
"""

# No duplicate sits in any row, column, or box, but row 0 uses every
# digit except 9 while column 8 already has a 9 elsewhere, so the
# last cell in row 0 has no legal value and the board cannot be solved.
UNSOLVABLE_BUT_CONFLICT_FREE = """\
12345678.
.........
.........
........9
.........
.........
.........
.........
.........
"""


class SolveTests(unittest.TestCase):
    def test_solves_known_puzzle(self):
        board = Board.from_text(PUZZLE)
        solved = solve(board)
        self.assertIsNotNone(solved)
        self.assertEqual(solved.to_text(), Board.from_text(SOLUTION).to_text())

    def test_solved_board_is_valid_and_complete(self):
        solved = solve(Board.from_text(PUZZLE))
        self.assertTrue(solved.is_valid())
        self.assertTrue(solved.is_complete())

    def test_solving_does_not_mutate_the_input_board(self):
        board = Board.from_text(PUZZLE)
        original = [row[:] for row in board.cells]
        solve(board)
        self.assertEqual(board.cells, original)

    def test_solves_a_nearly_complete_board(self):
        solved = solve(Board.from_text(NEARLY_SOLVED))
        self.assertEqual(solved.to_text(), Board.from_text(SOLUTION).to_text())

    def test_already_solved_board_solves_to_itself(self):
        board = Board.from_text(SOLUTION)
        solved = solve(board)
        self.assertEqual(solved.to_text(), board.to_text())

    def test_returns_none_for_board_with_conflicts(self):
        rows = ["123456781"] + ["0" * 9] * 8
        board = Board.from_text("\n".join(rows))
        self.assertIsNone(solve(board))

    def test_returns_none_for_unsolvable_but_conflict_free_board(self):
        board = Board.from_text(UNSOLVABLE_BUT_CONFLICT_FREE)
        self.assertTrue(board.is_valid())
        self.assertIsNone(solve(board))

    def test_empty_board_solves_to_a_valid_complete_board(self):
        board = Board.from_text("\n".join(["0" * 9] * 9))
        solved = solve(board)
        self.assertTrue(solved.is_valid())
        self.assertTrue(solved.is_complete())


if __name__ == "__main__":
    unittest.main()
