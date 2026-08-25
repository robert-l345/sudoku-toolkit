"""Backtracking solver for sudoku boards."""

from __future__ import annotations

from typing import Optional

from .board import BOX_SIZE, EMPTY, SIZE, Board


def solve(board: Board) -> Optional[Board]:
    """Return a solved copy of board, or None if it has no solution.

    Boards with existing rule violations are rejected up front rather
    than fed to the search, since a conflicting clue can never be
    satisfied no matter how the remaining cells are filled.
    """
    if not board.is_valid():
        return None
    grid = [row[:] for row in board.cells]
    if not _solve_grid(grid):
        return None
    return Board(grid)


def _solve_grid(grid) -> bool:
    cell = _find_best_empty_cell(grid)
    if cell is None:
        return True
    row, col, candidates = cell
    for value in candidates:
        grid[row][col] = value
        if _solve_grid(grid):
            return True
        grid[row][col] = EMPTY
    return False


def _find_best_empty_cell(grid):
    """Return (row, col, candidates) for the most constrained empty cell.

    Branching on the cell with the fewest legal values first, instead
    of scanning left to right, prunes dead branches almost immediately
    and keeps ordinary 9x9 puzzles fast under plain backtracking.
    """
    best = None
    for row in range(SIZE):
        for col in range(SIZE):
            if grid[row][col] != EMPTY:
                continue
            candidates = _candidates(grid, row, col)
            if not candidates:
                return row, col, candidates
            if best is None or len(candidates) < len(best[2]):
                best = (row, col, candidates)
                if len(candidates) == 1:
                    return best
    return best


def _candidates(grid, row, col):
    used = set(grid[row])
    used.update(grid[r][col] for r in range(SIZE))
    box_row, box_col = (row // BOX_SIZE) * BOX_SIZE, (col // BOX_SIZE) * BOX_SIZE
    for r in range(box_row, box_row + BOX_SIZE):
        for c in range(box_col, box_col + BOX_SIZE):
            used.add(grid[r][c])
    return [value for value in range(1, SIZE + 1) if value not in used]
