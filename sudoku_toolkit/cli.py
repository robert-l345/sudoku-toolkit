"""Command line interface for sudoku_toolkit."""

from __future__ import annotations

import argparse
import sys

from .board import Board, BoardError


def _read_input(path):
    # '-' matches the common convention for "read stdin instead of a file".
    if path is None or path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def cmd_check(args: argparse.Namespace) -> int:
    text = _read_input(args.file)
    try:
        board = Board.from_text(text)
    except BoardError as exc:
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

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
