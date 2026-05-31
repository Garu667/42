from __future__ import annotations
from abc import ABC, abstractmethod
import random


class BaseGenerator(ABC):
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
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.blocked = blocked
        self.perfect = perfect
        self.rng = rng

    @abstractmethod
    def run(self) -> None:
        ...


class BaseSolver(ABC):
    def __init__(
        self,
        grid: list[list[int]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_

    @abstractmethod
    def solve(self) -> list[str]:
        ...
