"""Tests for sudoku_toolkit.generator."""

from __future__ import annotations

import random
import unittest

from sudoku_toolkit.generator import DIFFICULTIES, _count_solutions, generate


class GenerateTests(unittest.TestCase):
    def test_unknown_difficulty_is_an_error(self):
        with self.assertRaises(ValueError):
            generate("impossible")

    def test_generated_boards_are_valid_and_incomplete(self):
        for difficulty in DIFFICULTIES:
            board = generate(difficulty, rng=random.Random(1))
            self.assertTrue(board.is_valid())
            self.assertFalse(board.is_complete())

    def test_clue_count_is_close_to_target(self):
        for difficulty, target in DIFFICULTIES.items():
            board = generate(difficulty, rng=random.Random(1))
            clues = sum(1 for row in board.cells for value in row if value)
            # Digging holes in a single fixed order can occasionally get
            # stuck a little above the target before every position has
            # been tried, so allow some slack instead of an exact match.
            self.assertGreaterEqual(clues, target)
            self.assertLessEqual(clues, target + 10)

    def test_generated_board_has_a_unique_solution(self):
        board = generate("hard", rng=random.Random(7))
        grid = [row[:] for row in board.cells]
        self.assertEqual(_count_solutions(grid, limit=2), 1)

    def test_same_seed_produces_same_puzzle(self):
        first = generate("medium", rng=random.Random(42))
        second = generate("medium", rng=random.Random(42))
        self.assertEqual(first.cells, second.cells)


if __name__ == "__main__":
    unittest.main()
