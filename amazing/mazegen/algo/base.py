from __future__ import annotations
from collections.abc import Generator
from abc import ABC, abstractmethod
import random


class BaseGenerator(ABC):
    """Abstract base class for maze generation algorithms."""
    def __init__(
        self,
        grid: list[list[int]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        blocked: set[tuple[int, int]],
        perfect: bool,
        rng: random.Random,
    ) -> None:
        """Initialize a maze generator.

        Args:
            grid (list[list[int]]): Maze grid.
            width (int): Grid width.
            height (int): Grid height.
            entry (tuple[int, int]): Entry position.
            exit_ (tuple[int, int]): Exit position.
            blocked (set[tuple[int, int]]): Blocked cells.
            perfect (bool): Whether the maze must be perfect.
            rng (random.Random): Random number generator.
        """
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.blocked = blocked
        self.perfect = perfect
        self.rng = rng

    @abstractmethod
    def run(self) -> Generator[None, None, None]:
        """Generate the maze step by step."""
        ...


class BaseSolver(ABC):
    """Abstract base class for maze solving algorithms."""
    def __init__(
        self,
        grid: list[list[int]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        """Initialize a maze solver.

        Args:
            grid (list[list[int]]): Maze grid.
            width (int): Grid width.
            height (int): Grid height.
            entry (tuple[int, int]): Entry position.
            exit_ (tuple[int, int]): Exit position.
        """
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_

    @abstractmethod
    def solve(self) -> list[str]:
        """Return a path from entry to exit."""
        ...

    @abstractmethod
    def solve_animated(self) -> Generator[list[str], None, None]:
        """Yield solving steps for animation."""
        ...
