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
    """State of the maze lifecycle."""

    BLANK = 0
    INITIALIZED = 1
    GENERATING = 2
    GENERATED = 3
    ERROR = -1


class Maze:
    """Represent and manage a maze lifecycle (generation, solving)."""

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
        """Initialize maze parameters and internal state."""
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
        """Current maze state."""
        return self._state

    @property
    def width(self) -> int:
        """Maze width."""
        return self._width

    @property
    def height(self) -> int:
        """Maze height."""
        return self._height

    @property
    def entry(self) -> tuple[int, int]:
        """Entry coordinates."""
        return self._entry

    @property
    def exit(self) -> tuple[int, int]:
        """Exit coordinates."""
        return self._exit

    @property
    def grid(self) -> list[list[int]]:
        """Return a copy of the maze grid."""
        self._require_state_gte(MazeState.INITIALIZED, "grid")
        return [row[:] for row in self._grid]

    @property
    def forty_two_cells(self) -> set[tuple[int, int]]:
        """Return blocked '42 pattern' cells."""
        self._require_state_gte(MazeState.INITIALIZED, "forty_two_cells")
        return set(self._42_cells)

    @property
    def solution(self) -> list[str]:
        """Return computed solution path."""
        if not self._solution:
            raise RuntimeError(
                "Call solve() before accessing to the solution.")
        return list(self._solution)

    @property
    def is_solving(self) -> bool:
        """Check if solving animation is running."""
        return self._solve_iterator is not None

    @property
    def has_solution(self) -> bool:
        """Check if a solution exists."""
        return bool(self._solution)

    def initialize(self) -> None:
        """Initialize the maze grid and internal state."""
        try:
            self._grid = [[0xF] * self._width for _ in range(self._height)]
            self._42_cells = set()
            self._solution = []
            self._iterator = None

            if self.can_fit_42():
                self._place_42()
                self._validate_pos_42()
            else:
                print(
                    f"[!] Too small for the 42 pattern "
                    f"(minimum {self.MIN_SIZE_FOR_42[0]}×"
                    f"{self.MIN_SIZE_FOR_42[1]})."
                )

            self._state = MazeState.INITIALIZED

        except Exception as e:
            self._state = MazeState.ERROR
            raise RuntimeError(f"Initialization failed: {e}") from e

    def generate(self, algo: Type[BaseGenerator]) -> None:
        """Start maze generation using a given algorithm."""
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
            raise RuntimeError(f"Generation failed: {e}") from e

    def tick(self) -> bool:
        """Advance one step of generation.

        Returns:
            bool: True if generation continues, False if finished.
        """
        self._require_state(MazeState.GENERATING, "tick()")
        it = self._iterator
        if it is None:
            raise RuntimeError("Iterator not initialized")
        try:
            next(it)
            return True
        except StopIteration:
            self._state = MazeState.GENERATED
            self._iterator = None
            return False

    def run_all(self) -> None:
        """Run full maze generation until completion."""
        self._require_state(MazeState.GENERATING, "run_all()")
        while self.tick():
            pass

    def solve(self, solver: Type[BaseSolver]) -> None:
        """Solve the generated maze."""
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
            raise ValueError("No path found between entry and exit")
        self._solution = result

    def reset(self) -> None:
        """Reset the maze to initial state."""
        self._state = MazeState.BLANK
        self._grid = []
        self._42_cells = set()
        self._solution = []
        self._iterator = None
        self._seed = self._rng_seed()
        self.initialize()

    def _rng_seed(self) -> int:
        """Generate a random seed."""
        import random
        return random.randint(0, 2**32 - 1)

    def is_done(self) -> bool:
        """Check if maze generation is complete."""
        return self._state == MazeState.GENERATED

    def can_fit_42(self) -> bool:
        """Check if the '42' pattern can be placed."""
        min_w, min_h = self.MIN_SIZE_FOR_42
        return self._width >= min_w and self._height >= min_h

    def carve(self, x: int, y: int, direction: int) -> None:
        """Remove walls between two adjacent cells."""
        dx, dy = DELTA[direction]
        nx, ny = x + dx, y + dy
        self._grid[y][x] &= ~direction
        self._grid[ny][nx] &= ~OPPOSITE[direction]

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        """Check if a wall exists in a direction."""
        return bool(self._grid[y][x] & direction)

    def in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are inside the grid."""
        return 0 <= x < self._width and 0 <= y < self._height

    def is_blocked(self, x: int, y: int) -> bool:
        """Check if a cell is blocked."""
        return (x, y) in self._42_cells

    def get_neighbors(
        self, x: int, y: int
    ) -> list[tuple[int, int, int]]:
        """Return accessible neighbors with directions."""
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
        """Validate maze parameters."""
        if width < 2 or height < 2:
            raise ValueError("Dimension must be XxX minimun")
        ex, ey = entry
        fx, fy = exit_
        if not (0 <= ex < width and 0 <= ey < height):
            raise ValueError(f"Entry {entry} is out limit ({width}×{height})")
        if not (0 <= fx < width and 0 <= fy < height):
            raise ValueError(f"Exit {exit_} is out limit ({width}×{height})")
        if entry == exit_:
            raise ValueError("Entry and Exit must be on separated cells")

    def _require_state(self, expected: MazeState, action: str) -> None:
        """Ensure maze is in expected state."""
        if self._state != expected:
            raise RuntimeError(
                f"'{action}' requiert the state {expected.name}, "
                f"actuel state: {self._state.name}."
            )

    def _require_state_gte(self, minimum: MazeState, prop: str) -> None:
        """Ensure state is at least a minimum level."""
        if self._state < minimum:
            raise RuntimeError(
                f"'{prop}' is not available with the state {self._state.name} "
                f"(minimum required : {minimum.name})."
            )

    def _place_42(self) -> None:
        """Place the '42' pattern in the maze."""
        start_x = (self._width - _PATTERN_W) // 2
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

    def _validate_pos_42(self) -> None:
        """Ensure entry/exit are not inside the pattern."""
        if self._entry in self._42_cells or self._exit in self._42_cells:
            raise ValueError("Entry or exit in locked cells")

    def solve_animated(self, solver: Type[BaseSolver]) -> None:
        """Start animated solving process."""
        self._require_state(MazeState.GENERATED, "solve_animated()")
        instance = solver(
            grid=self._grid,
            width=self._width,
            height=self._height,
            entry=self._entry,
            exit_=self._exit,
        )
        self._solve_iterator: Generator[list[str], None, None] | None
        self._solve_iterator = instance.solve_animated()
        self._solution = []

    def tick_solve(self) -> bool:
        """Advance one solving step.

        Returns:
            bool: True if solving continues.
        """
        if self._solve_iterator is None:
            return False
        try:
            self._solution = next(self._solve_iterator)
            return True
        except StopIteration:
            self._solve_iterator = None
            return False
