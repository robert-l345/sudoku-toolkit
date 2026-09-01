# sudoku-toolkit

A small library and CLI for reading sudoku boards and checking whether they
follow the rules: no repeated digit in any row, column, or 3x3 box.

Every sudoku site and puzzle collection seems to have its own text format.
This started because I wanted one parser that didn't care whether a board
came as nine lines of digits, a single 81-character line, or piped in from
some other program, and would tell me exactly which row or box was broken
instead of just "invalid".

## Input format

Two forms are accepted, and both use `.` or `0` for an empty cell:

Nine lines of nine characters:

```
53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79
```

Or a single line of 81 characters:

```
53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79
```

Lines starting with `#` are ignored, so a board file can carry a comment or
a source citation at the top.

## Usage

As a library:

```python
from sudoku_toolkit import Board, solve

board = Board.from_text(open("puzzle.txt").read())
print(board.pretty())
print(board.is_valid())      # no rule violations so far
print(board.is_complete())   # every cell filled in
print(board.conflicts())     # list of specific violations, if any

solved = solve(board)        # a solved copy, or None if unsolvable
if solved is not None:
    print(solved.pretty())
```

From the command line, reading a file:

```
$ sudoku-toolkit check puzzle.txt
```

Or reading from stdin, which is the point of this project:

```
$ cat puzzle.txt | sudoku-toolkit check
$ curl -s https://example.com/puzzle.txt | sudoku-toolkit check -
```

Omitting the file argument, or passing `-` explicitly, both read stdin.

Exit codes for `check`: `0` for a valid board, `1` if rule violations were
found, `2` if the input couldn't be parsed as a board at all.

To solve a board:

```
$ sudoku-toolkit solve puzzle.txt
$ sudoku-toolkit solve --oneline puzzle.txt
```

Exit codes for `solve`: `0` on success, `1` if the board has rule violations
or has no solution, `2` if the input couldn't be parsed.

## Status

This parses, validates, and solves boards, both as a library and from the
CLI. It doesn't generate new puzzles yet, and there's no way to write a
solved board back out in a form another tool expects - see the roadmap in
the issue tracker.

## License

MIT, see LICENSE.
