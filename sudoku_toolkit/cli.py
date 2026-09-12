"""Command line interface for sudoku_toolkit."""

from __future__ import annotations

import argparse
import sys

from .board import Board, BoardError
from .generator import DIFFICULTIES, generate
from .solver import solve


def _read_board(path):
    # '-' matches the common convention for "read stdin instead of a file".
    if path is None or path == "-":
        return Board.from_text(sys.stdin.read())
    return Board.from_file(path)


def cmd_check(args: argparse.Namespace) -> int:
    try:
        board = _read_board(args.file)
    except (BoardError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(board.pretty())
    problems = board.conflicts()
    if problems:
        print(f"\n{len(problems)} problem(s) found:")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    status = "complete and valid" if board.is_complete() else "valid so far"
    print(f"\n{status}")
    return 0


def cmd_solve(args: argparse.Namespace) -> int:
    try:
        board = _read_board(args.file)
    except (BoardError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    problems = board.conflicts()
    if problems:
        print("error: board has rule violations, cannot solve:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    solved = solve(board)
    if solved is None:
        print("error: no solution exists for this board", file=sys.stderr)
        return 1

    if args.oneline:
        print(solved.to_line())
    else:
        print(solved.pretty())
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    board = generate(args.difficulty)
    if args.oneline:
        print(board.to_line())
    else:
        print(board.pretty())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sudoku-toolkit",
        description="Read and validate sudoku boards.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser(
        "check", help="parse a board and report rule violations"
    )
    check.add_argument(
        "file",
        nargs="?",
        default=None,
        help="path to a board file; omit or pass '-' to read from stdin",
    )
    check.set_defaults(func=cmd_check)

    solve_parser = subparsers.add_parser(
        "solve", help="solve a board and print the solution"
    )
    solve_parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="path to a board file; omit or pass '-' to read from stdin",
    )
    solve_parser.add_argument(
        "--oneline",
        action="store_true",
        help="print the solution as a single 81-character line instead of a grid",
    )
    solve_parser.set_defaults(func=cmd_solve)

    generate_parser = subparsers.add_parser(
        "generate", help="generate a new puzzle with a unique solution"
    )
    generate_parser.add_argument(
        "--difficulty",
        choices=sorted(DIFFICULTIES),
        default="medium",
        help="how many clues to leave; fewer is harder (default: medium)",
    )
    generate_parser.add_argument(
        "--oneline",
        action="store_true",
        help="print the puzzle as a single 81-character line instead of a grid",
    )
    generate_parser.set_defaults(func=cmd_generate)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
