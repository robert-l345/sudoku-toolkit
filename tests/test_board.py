"""Tests for sudoku_toolkit.board."""

from __future__ import annotations

import unittest

from sudoku_toolkit.board import Board, BoardError

# Classic example puzzle and its unique solution, used across several tests.
PUZZLE_MULTILINE = """\
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

PUZZLE_SINGLE_LINE = (
    "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
)

SOLUTION_MULTILINE = """\
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


class FromTextTests(unittest.TestCase):
    def test_parses_nine_line_form(self):
        board = Board.from_text(PUZZLE_MULTILINE)
        self.assertEqual(board.row(0), [5, 3, 0, 0, 7, 0, 0, 0, 0])
        self.assertEqual(board.row(8), [0, 0, 0, 0, 8, 0, 0, 7, 9])

    def test_parses_single_line_form(self):
        board = Board.from_text(PUZZLE_SINGLE_LINE)
        self.assertEqual(board.row(0), [5, 3, 0, 0, 7, 0, 0, 0, 0])
        self.assertEqual(board.row(8), [0, 0, 0, 0, 8, 0, 0, 7, 9])

    def test_two_forms_agree(self):
        self.assertEqual(
            Board.from_text(PUZZLE_MULTILINE).cells,
            Board.from_text(PUZZLE_SINGLE_LINE).cells,
        )

    def test_zero_and_space_and_dot_all_mean_empty(self):
        text = "\n".join(
            [
                "1234567.9",
                "123456789",
                "123456780",
                "123456789",
                "123 56789",
                "123456789",
                "123456789",
                "123456789",
                "123456789",
            ]
        )
        board = Board.from_text(text)
        self.assertEqual(board.cells[0][7], 0)
        self.assertEqual(board.cells[2][8], 0)
        self.assertEqual(board.cells[4][3], 0)

    def test_ignores_comment_and_blank_lines(self):
        text = "# from some collection\n\n" + PUZZLE_MULTILINE + "\n# end\n"
        board = Board.from_text(text)
        self.assertEqual(board.row(0), [5, 3, 0, 0, 7, 0, 0, 0, 0])

    def test_empty_input_is_an_error(self):
        with self.assertRaises(BoardError):
            Board.from_text("")

    def test_comment_only_input_is_an_error(self):
        with self.assertRaises(BoardError):
            Board.from_text("# nothing here\n")

    def test_wrong_row_count_is_an_error(self):
        text = "\n".join(["123456789"] * 8)
        with self.assertRaises(BoardError):
            Board.from_text(text)

    def test_wrong_row_length_is_an_error(self):
        rows = ["123456789"] * 8 + ["12345678"]
        with self.assertRaises(BoardError):
            Board.from_text("\n".join(rows))

    def test_wrong_single_line_length_is_an_error(self):
        with self.assertRaises(BoardError):
            Board.from_text("1" * 80)

    def test_invalid_character_is_an_error(self):
        rows = ["123456789"] * 8 + ["12345678x"]
        with self.assertRaises(BoardError):
            Board.from_text("\n".join(rows))


class ConflictDetectionTests(unittest.TestCase):
    def test_original_puzzle_has_no_conflicts(self):
        board = Board.from_text(PUZZLE_MULTILINE)
        self.assertEqual(board.conflicts(), [])
        self.assertTrue(board.is_valid())

    def test_solved_board_is_valid_and_complete(self):
        board = Board.from_text(SOLUTION_MULTILINE)
        self.assertTrue(board.is_valid())
        self.assertTrue(board.is_complete())

    def test_unsolved_board_is_not_complete(self):
        board = Board.from_text(PUZZLE_MULTILINE)
        self.assertFalse(board.is_complete())

    def test_detects_row_duplicate(self):
        rows = ["123456781"] + ["0" * 9] * 8
        board = Board.from_text("\n".join(rows))
        problems = board.conflicts()
        self.assertTrue(any("row 1" in p for p in problems))

    def test_detects_column_duplicate(self):
        rows = ["1" + "0" * 8]
        rows += ["0" * 9] * 6
        rows += ["1" + "0" * 8]
        rows += ["0" * 9]
        board = Board.from_text("\n".join(rows))
        problems = board.conflicts()
        self.assertTrue(any("column 1" in p for p in problems))

    def test_detects_box_duplicate(self):
        rows = ["100000000", "010000000", "100000000"]
        rows += ["0" * 9] * 6
        board = Board.from_text("\n".join(rows))
        problems = board.conflicts()
        self.assertTrue(any("box 1" in p for p in problems))

    def test_empty_cells_never_count_as_duplicates(self):
        board = Board.from_text("\n".join(["0" * 9] * 9))
        self.assertEqual(board.conflicts(), [])
        self.assertTrue(board.is_valid())
        self.assertFalse(board.is_complete())


class ConstructorTests(unittest.TestCase):
    def test_rejects_wrong_row_count(self):
        with self.assertRaises(BoardError):
            Board([[0] * 9] * 8)

    def test_rejects_wrong_column_count(self):
        rows = [[0] * 9 for _ in range(9)]
        rows[0] = [0] * 8
        with self.assertRaises(BoardError):
            Board(rows)

    def test_rejects_out_of_range_value(self):
        rows = [[0] * 9 for _ in range(9)]
        rows[0][0] = 10
        with self.assertRaises(BoardError):
            Board(rows)


class RenderingTests(unittest.TestCase):
    def test_to_text_round_trips_through_from_text(self):
        board = Board.from_text(PUZZLE_MULTILINE)
        round_tripped = Board.from_text(board.to_text())
        self.assertEqual(board.cells, round_tripped.cells)

    def test_pretty_includes_box_separators(self):
        board = Board.from_text(PUZZLE_MULTILINE)
        text = board.pretty()
        self.assertIn("------+-------+------", text)
        self.assertEqual(text.count("------+-------+------"), 2)

    def test_to_line_matches_single_line_form(self):
        board = Board.from_text(PUZZLE_MULTILINE)
        self.assertEqual(board.to_line(), PUZZLE_SINGLE_LINE)

    def test_to_line_round_trips_through_from_text(self):
        board = Board.from_text(PUZZLE_MULTILINE)
        round_tripped = Board.from_text(board.to_line())
        self.assertEqual(board.cells, round_tripped.cells)


if __name__ == "__main__":
    unittest.main()
