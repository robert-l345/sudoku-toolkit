"""Puzzle generation.

Builds a full random solved grid, then removes clues one at a time,
checking after each removal that the puzzle still has exactly one
solution. That check is what makes this more than shuffling digits
into a valid grid and poking holes in it - a puzzle with two possible
solutions isn't a real puzzle.
"""

from __future__ import annotations

import random

from .board import EMPTY, SIZE, Board
from .solver import _find_best_empty_cell

# Clues left behind per difficulty. Sudoku's proven floor for a unique
# solution is 17 clues, so "expert" stays comfortably above that rather
# than chasing the theoretical minimum.
DIFFICULTIES = {
    "easy": 46,
    "medium": 38,
    "hard": 30,
    "expert": 24,
}


def generate(difficulty: str = "medium", rng: "random.Random | None" = None) -> Board:
    """Generate a puzzle with a unique solution at the given difficulty."""
    if difficulty not in DIFFICULTIES:
        raise ValueError(
            f"unknown difficulty {difficulty!r}, choose from {sorted(DIFFICULTIES)}"
        )
    rng = rng if rng is not None else random.Random()
    grid = [[EMPTY] * SIZE for _ in range(SIZE)]
    _fill_randomly(grid, rng)
    _dig_holes(grid, DIFFICULTIES[difficulty], rng)
    return Board(grid)


def _fill_randomly(grid, rng) -> bool:
    cell = _find_best_empty_cell(grid)
    if cell is None:
        return True
    row, col, candidates = cell
    rng.shuffle(candidates)
    for value in candidates:
        grid[row][col] = value
        if _fill_randomly(grid, rng):
            return True
        grid[row][col] = EMPTY
    return False


def _dig_holes(grid, target_clues: int, rng) -> None:
    positions = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    rng.shuffle(positions)
    clues = SIZE * SIZE
    for row, col in positions:
        if clues <= target_clues:
            return
        removed = grid[row][col]
        grid[row][col] = EMPTY
        if _count_solutions(grid, limit=2) == 1:
            clues -= 1
        else:
            grid[row][col] = removed


def _count_solutions(grid, limit: int) -> int:
    """Count solutions to `grid`, stopping early once `limit` is reached."""
    cell = _find_best_empty_cell(grid)
    if cell is None:
        return 1
    row, col, candidates = cell
    total = 0
    for value in candidates:
        grid[row][col] = value
        total += _count_solutions(grid, limit - total)
        grid[row][col] = EMPTY
        if total >= limit:
            break
    return total
