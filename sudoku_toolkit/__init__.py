"""A small library for parsing and validating sudoku boards."""

from .board import Board, BoardError
from .solver import solve

__all__ = ["Board", "BoardError", "solve"]
__version__ = "0.1.0"
