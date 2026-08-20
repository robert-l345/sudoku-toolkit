"""Core representation and validation for a 9x9 sudoku board."""

from __future__ import annotations

SIZE = 9
BOX_SIZE = 3
EMPTY = 0


class BoardError(ValueError):
    """Raised when input text cannot be parsed into a 9x9 board."""


class Board:
    """A 9x9 sudoku board. Cells hold 1-9, or 0 for empty."""

    def __init__(self, cells):
        if len(cells) != SIZE:
            raise BoardError(f"expected {SIZE} rows, got {len(cells)}")
        for row in cells:
            if len(row) != SIZE:
                raise BoardError(f"expected {SIZE} columns, got {len(row)}")
            for value in row:
                if not 0 <= value <= 9:
                    raise BoardError(f"cell value out of range: {value}")
        self.cells = [list(row) for row in cells]

    @classmethod
    def from_text(cls, text: str) -> "Board":
        """Parse a board from text.

        Accepts either nine lines of nine characters each, or a single
        line of 81 characters. In both forms '.', '0', and blank spaces
        mean an empty cell. Blank lines and lines starting with '#' are
        skipped, so puzzle files can carry comments.
        """
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        if not lines:
            raise BoardError("no board data found in input")

        if len(lines) == 1:
            digits = lines[0]
            if len(digits) != SIZE * SIZE:
                raise BoardError(
                    f"single-line board must have {SIZE * SIZE} characters, "
                    f"got {len(digits)}"
                )
            rows = [digits[i * SIZE : (i + 1) * SIZE] for i in range(SIZE)]
        else:
            rows = lines

        cells = []
        for row in rows:
            # A row already at the target width keeps its spaces, since a
            # space there is an empty-cell marker like '.' or '0'. A row
            # padded with separator spaces (e.g. "5 3 . . 7 . . . .") gets
            # them stripped down to the real digits.
            compact = row if len(row) == SIZE else row.replace(" ", "")
            if len(compact) != SIZE:
                raise BoardError(
                    f"each row must have {SIZE} cells, got {len(compact)!r}"
                )
            cells.append([_parse_cell(ch) for ch in compact])
        return cls(cells)

    def to_text(self) -> str:
        """Render as nine lines of nine characters, '.' for empty."""
        return "\n".join(
            "".join(str(v) if v else "." for v in row) for row in self.cells
        )

    def pretty(self) -> str:
        """Render with box separators, for terminal display."""
        lines = []
        for r, row in enumerate(self.cells):
            if r and r % BOX_SIZE == 0:
                lines.append("------+-------+------")
            parts = []
            for c, value in enumerate(row):
                if c and c % BOX_SIZE == 0:
                    parts.append("|")
                parts.append(str(value) if value else ".")
            lines.append(" ".join(parts))
        return "\n".join(lines)

    def row(self, index):
        return self.cells[index]

    def column(self, index):
        return [self.cells[r][index] for r in range(SIZE)]

    def box(self, index):
        br, bc = divmod(index, BOX_SIZE)
        values = []
        for r in range(br * BOX_SIZE, br * BOX_SIZE + BOX_SIZE):
            for c in range(bc * BOX_SIZE, bc * BOX_SIZE + BOX_SIZE):
                values.append(self.cells[r][c])
        return values

    def conflicts(self):
        """Return human-readable descriptions of rule violations, if any."""
        problems = []
        for i in range(SIZE):
            problems.extend(_duplicates(self.row(i), f"row {i + 1}"))
            problems.extend(_duplicates(self.column(i), f"column {i + 1}"))
            problems.extend(_duplicates(self.box(i), f"box {i + 1}"))
        return problems

    def is_valid(self) -> bool:
        return not self.conflicts()

    def is_complete(self) -> bool:
        return all(value != EMPTY for row in self.cells for value in row)


def _parse_cell(ch: str) -> int:
    if ch in ".0 ":
        return EMPTY
    if ch.isdigit() and ch != "0":
        return int(ch)
    raise BoardError(f"invalid cell character: {ch!r}")


def _duplicates(values, label: str):
    seen = set()
    problems = []
    for value in values:
        if value == EMPTY:
            continue
        if value in seen:
            problems.append(f"duplicate {value} in {label}")
        else:
            seen.add(value)
    return problems
