"""A small library for parsing and validating sudoku boards."""

from .board import Board, BoardError
from .generator import DIFFICULTIES, generate
from .solver import solve

__all__ = ["Board", "BoardError", "DIFFICULTIES", "generate", "solve"]
__version__ = "0.1.0"
