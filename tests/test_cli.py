"""Tests for sudoku_toolkit.cli."""

from __future__ import annotations

import contextlib
import io
import unittest
from unittest import mock

from sudoku_toolkit import cli

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

SOLUTION_ONELINE = (
    "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
)

CONFLICTING = "11" + "." * 79

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


def _run(argv, stdin_text=""):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with mock.patch("sys.stdin", io.StringIO(stdin_text)):
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli.main(argv)
    return code, stdout.getvalue(), stderr.getvalue()


class SolveCommandTests(unittest.TestCase):
    def test_solves_and_prints_grid(self):
        code, out, err = _run(["solve"], stdin_text=PUZZLE)
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        self.assertIn("5 3 4", out)
        self.assertNotIn(".", out)

    def test_solves_and_prints_oneline(self):
        code, out, err = _run(["solve", "--oneline"], stdin_text=PUZZLE)
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), SOLUTION_ONELINE)

    def test_rejects_board_with_conflicts(self):
        code, out, err = _run(["solve"], stdin_text=CONFLICTING)
        self.assertEqual(code, 1)
        self.assertIn("rule violations", err)

    def test_reports_unsolvable_board(self):
        code, out, err = _run(["solve"], stdin_text=UNSOLVABLE_BUT_CONFLICT_FREE)
        self.assertEqual(code, 1)
        self.assertIn("no solution", err)

    def test_reports_parse_error(self):
        code, out, err = _run(["solve"], stdin_text="not a board")
        self.assertEqual(code, 2)
        self.assertIn("error:", err)


class GenerateCommandTests(unittest.TestCase):
    def test_generates_a_valid_puzzle(self):
        code, out, err = _run(["generate", "--difficulty", "easy"])
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        self.assertIn(".", out)

    def test_generates_oneline_puzzle(self):
        code, out, err = _run(["generate", "--oneline"])
        self.assertEqual(code, 0)
        self.assertEqual(len(out.strip()), 81)


if __name__ == "__main__":
    unittest.main()
