import random
from collections.abc import Generator
from enum import IntEnum
from typing import Optional, Type
from mazegen.algo.base import BaseGenerator, BaseSolver


NORTH: int = 0x1
EAST:  int = 0x2
SOUTH: int = 0x4
WEST:  int = 0x8

OPPOSITE: dict[int, int] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST:  WEST,
    WEST:  EAST,
}

DELTA: dict[int, tuple[int, int]] = {
    NORTH: (0, -1),
    SOUTH: (0,  1),
    EAST:  (1,  0),
    WEST:  (-1, 0),
}

_DIGIT_4: list[list[int]] = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1],
]

_DIGIT_2: list[list[int]] = [
    [1, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1],
]

_PATTERN_W: int = 7
_PATTERN_H: int = 5

class MazeState(IntEnum):
    BLANK       = 0   # Objet créé, aucune grille allouée
    INITIALIZED = 1   # Grille à 0xF, pattern "42" placé
    GENERATING  = 2   # Algorithme en cours (yields intermédiaires)
    GENERATED   = 3   # Labyrinthe complet et valide
    ERROR       = -1  # Paramètres invalides ou génération échouée


class Maze:
    MIN_SIZE_FOR_42: tuple[int, int] = (_PATTERN_W + 2, _PATTERN_H + 2)

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        self._validate(width, height, entry, exit_)

        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit_
        self._perfect = perfect
        self._seed = seed

        self._state: MazeState = MazeState.BLANK
        self._grid: list[list[int]] = []
        self._42_cells: set[tuple[int, int]] = set()
        self._solution: list[str] = []
        self._iterator: Optional[Generator[None, None, None]] = None


    @property
    def state(self) -> MazeState:
        return self._state

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def entry(self) -> tuple[int, int]:
        return self._entry

    @property
    def exit(self) -> tuple[int, int]:
        return self._exit

    @property
    def grid(self) -> list[list[int]]:
        self._require_state_gte(MazeState.INITIALIZED, "grid")
        return [row[:] for row in self._grid]

    @property
    def forty_two_cells(self) -> set[tuple[int, int]]:
        self._require_state_gte(MazeState.INITIALIZED, "forty_two_cells")
        return set(self._42_cells)

    @property
    def solution(self) -> list[str]:
        if not self._solution:
            raise RuntimeError(
                "Appelez solve() avant d'accéder à la solution."
            )
        return list(self._solution)


    def initialize(self) -> None:
        try:
            self._grid = [[0xF] * self._width for _ in range(self._height)]
            self._42_cells = set()
            self._solution = []
            self._iterator = None

            if self.can_fit_42():
                self._place_42()
            else:
                print(
                    f"[Warning] Trop petit pour le pattern '42' "
                    f"(minimum {self.MIN_SIZE_FOR_42[0]}×"
                    f"{self.MIN_SIZE_FOR_42[1]})."
                )

            self._state = MazeState.INITIALIZED

        except Exception as e:
            self._state = MazeState.ERROR
            raise RuntimeError(f"Échec de l'initialisation : {e}") from e

    def generate(self, algo: Type[BaseGenerator]) -> None:
        self._require_state(MazeState.INITIALIZED, "generate()")

        try:
            rng = random.Random(self._seed)
            instance = algo(
                grid=self._grid,
                width=self._width,
                height=self._height,
                entry=self._entry,
                exit_=self._exit,
                blocked=self._42_cells,
                perfect=self._perfect,
                rng=rng,
            )
            self._iterator = instance.run()
            self._state = MazeState.GENERATING

        except Exception as e:
            self._state = MazeState.ERROR
            raise RuntimeError(f"Échec du lancement de la génération : {e}") from e

    def tick(self) -> bool:
        self._require_state(MazeState.GENERATING, "tick()")

        try:
            next(self._iterator)    # type: ignore[arg-type]
            return True
        except StopIteration:
            self._state = MazeState.GENERATED
            self._iterator = None
            return False

    def run_all(self) -> None:
        self._require_state(MazeState.GENERATING, "run_all()")
        while self.tick():
            pass

    def solve(self, solver: Type[BaseSolver]) -> None:
        self._require_state(MazeState.GENERATED, "solve()")

        instance = solver(
            grid=self._grid,
            width=self._width,
            height=self._height,
            entry=self._entry,
            exit_=self._exit,
        )
        result = instance.solve()

        if not result:
            raise ValueError(
                "Aucun chemin trouvé entre l'entrée et la sortie."
            )

        self._solution = result

    def reset(self) -> None:
        self._state = MazeState.BLANK
        self._grid = []
        self._42_cells = set()
        self._solution = []
        self._iterator = None
        self.initialize()

    def is_done(self) -> bool:
        return self._state == MazeState.GENERATED

    def can_fit_42(self) -> bool:
        min_w, min_h = self.MIN_SIZE_FOR_42
        return self._width >= min_w and self._height >= min_h


    def carve(self, x: int, y: int, direction: int) -> None:
        dx, dy = DELTA[direction]
        nx, ny = x + dx, y + dy
        self._grid[y][x]   &= ~direction
        self._grid[ny][nx] &= ~OPPOSITE[direction]

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        return bool(self._grid[y][x] & direction)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self._width and 0 <= y < self._height

    def is_blocked(self, x: int, y: int) -> bool:
        return (x, y) in self._42_cells

    def get_neighbors(
        self, x: int, y: int
    ) -> list[tuple[int, int, int]]:
        result: list[tuple[int, int, int]] = []
        for direction, (dx, dy) in DELTA.items():
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and not self.is_blocked(nx, ny):
                result.append((nx, ny, direction))
        return result


    @staticmethod
    def _validate(
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        if width < 2 or height < 2:
            raise ValueError("Les dimensions doivent être au minimum 2×2.")
        ex, ey = entry
        if not (0 <= ex < width and 0 <= ey < height):
            raise ValueError(
                f"L'entrée {entry} est hors limites ({width}×{height})."
            )
        fx, fy = exit_
        if not (0 <= fx < width and 0 <= fy < height):
            raise ValueError(
                f"La sortie {exit_} est hors limites ({width}×{height})."
            )
        if entry == exit_:
            raise ValueError("L'entrée et la sortie doivent être différentes.")

    def _require_state(self, expected: MazeState, action: str) -> None:
        if self._state != expected:
            raise RuntimeError(
                f"'{action}' requiert l'état {expected.name}, "
                f"état actuel : {self._state.name}."
            )

    def _require_state_gte(self, minimum: MazeState, prop: str) -> None:
        if self._state < minimum:
            raise RuntimeError(
                f"'{prop}' non disponible en état {self._state.name} "
                f"(minimum requis : {minimum.name})."
            )


    def _place_42(self) -> None:
        start_x = (self._width  - _PATTERN_W) // 2
        start_y = (self._height - _PATTERN_H) // 2

        for row, bits in enumerate(_DIGIT_4):
            for col, on in enumerate(bits):
                if on:
                    self._42_cells.add((start_x + col, start_y + row))

        x_off = start_x + len(_DIGIT_4[0]) + 1
        for row, bits in enumerate(_DIGIT_2):
            for col, on in enumerate(bits):
                if on:
                    self._42_cells.add((x_off + col, start_y + row))
