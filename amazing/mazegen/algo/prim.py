from __future__ import annotations
from collections.abc import Generator
from typing import List, Tuple, Set
from mazegen.algo.base import BaseGenerator

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
    EAST:  (1,  0),
    SOUTH: (0,  1),
    WEST:  (-1, 0),
}


class Prim(BaseGenerator):
    """Generate a maze using the randomized Prim algorithm."""

    def _get_unvisited_neighbors(
        self,
        x: int,
        y: int,
        visited: Set[Tuple[int, int]],
    ) -> List[Tuple[int, int, int]]:
        """Return unvisited and non-blocked neighbors.

        Args:
            x (int): Cell x coordinate.
            y (int): Cell y coordinate.
            visited (Set[Tuple[int, int]]): Visited cells.

        Returns:
            List[Tuple[int, int, int]]: Neighbor coordinates and direction.
        """
        result = []
        for direction, (dx, dy) in DELTA.items():
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and (nx, ny) not in self.blocked
                and (nx, ny) not in visited
            ):
                result.append((nx, ny, direction))
        return result

    def _get_visited_neighbors(
        self,
        x: int,
        y: int,
        visited: Set[Tuple[int, int]],
    ) -> List[Tuple[int, int, int]]:
        """Return visited and non-blocked neighbors.

        Args:
            x (int): Cell x coordinate.
            y (int): Cell y coordinate.
            visited (Set[Tuple[int, int]]): Visited cells.

        Returns:
            List[Tuple[int, int, int]]: Neighbor coordinates and direction.
        """
        result = []
        for direction, (dx, dy) in DELTA.items():
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and (nx, ny) not in self.blocked
                and (nx, ny) in visited
            ):
                result.append((nx, ny, direction))
        return result

    def _carve_between(
        self,
        x: int,
        y: int,
        nx: int,
        ny: int,
        direction: int,
    ) -> None:
        """Remove the wall between two adjacent cells.

        Args:
            x (int): Source cell x coordinate.
            y (int): Source cell y coordinate.
            nx (int): Neighbor x coordinate.
            ny (int): Neighbor y coordinate.
            direction (int): Direction to carve.
        """
        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~OPPOSITE[direction]

    def _carve_around(self, x: int, y: int) -> None:
        """Propagate wall state to neighboring cells.

        Args:
            x (int): Cell x coordinate.
            y (int): Cell y coordinate.
        """
        for direction, (dx, dy) in DELTA.items():
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and (nx, ny) not in self.blocked
            ):
                if not (self.grid[y][x] & direction):
                    self.grid[ny][nx] &= ~OPPOSITE[direction]
                else:
                    self.grid[ny][nx] |= OPPOSITE[direction]

    def _would_create_open_3x3(
        self,
        cx: int,
        cy: int,
        direction: int,
    ) -> bool:
        """Check whether removing a wall creates an open 3x3 area.

        Args:
            cx (int): Source cell x coordinate.
            cy (int): Source cell y coordinate.
            direction (int): Wall direction.

        Returns:
            bool: True if a 3x3 open area would be created.
        """
        dx, dy = DELTA[direction]
        nx, ny = cx + dx, cy + dy

        is_vertical = direction in (EAST, WEST)

        candidates: List[Tuple[int, int]] = []
        if is_vertical:
            left = min(cx, nx) - 1
            for bx in range(left, left + 2):
                for by in range(cy - 2, cy + 1):
                    candidates.append((bx, by))
        else:
            top = min(cy, ny) - 1
            for by in range(top, top + 2):
                for bx in range(cx - 2, cx + 1):
                    candidates.append((bx, by))

        for bx, by in candidates:
            if bx < 0 or bx + 2 >= self.width:
                continue
            if by < 0 or by + 2 >= self.height:
                continue

            all_open = True

            for r in range(by, by + 3):
                for c in range(bx, bx + 2):
                    is_target = (
                        (c == cx and r == cy and direction == EAST)
                        or (c + 1 == cx and r == cy and direction == WEST)
                    )
                    if not is_target and (self.grid[r][c] & EAST):
                        all_open = False
                        break
                if not all_open:
                    break

            if not all_open:
                continue

            for r in range(by, by + 2):
                for c in range(bx, bx + 3):
                    is_target = (
                        (c == cx and r == cy and direction == SOUTH)
                        or (c == cx and r + 1 == cy and direction == NORTH)
                    )
                    if not is_target and (self.grid[r][c] & SOUTH):
                        all_open = False
                        break
                if not all_open:
                    break

            if all_open:
                return True

        return False

    def _make_imperfect(self) -> None:
        """Break additional walls to create loops in the maze."""
        all_cells = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in self.blocked
        ]

        self.rng.shuffle(all_cells)

        def count_walls(x: int, y: int) -> int:
            return bin(self.grid[y][x]).count('1')

        all_cells.sort(key=lambda c: count_walls(c[0], c[1]))

        total_walls = sum(
            count_walls(x, y) for x, y in all_cells
        )
        total_walls -= (self.height + self.width) * 2
        total_walls //= 2
        walls_to_break = max(1, int(total_walls * 0.2))

        directions = [NORTH, EAST, SOUTH, WEST]
        break_count = 0
        idx = len(all_cells) - 1

        while break_count < walls_to_break and idx >= 0:
            x, y = all_cells[idx]
            idx -= 1

            shuffled = directions[:]
            self.rng.shuffle(shuffled)

            for direction in shuffled:
                if not (self.grid[y][x] & direction):
                    continue

                dx, dy = DELTA[direction]
                nx, ny = x + dx, y + dy

                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if (nx, ny) in self.blocked:
                    continue
                if self._would_create_open_3x3(x, y, direction):
                    continue

                self._carve_between(x, y, nx, ny, direction)
                self._carve_around(x, y)
                break_count += 1
                break

    def run(self) -> Generator[None, None, None]:
        """Generate the maze step by step.

        Yields:
            None: One generation step for animation.
        """
        passable = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in self.blocked
        ]
        start_x, start_y = self.rng.choice(passable)

        visited: Set[Tuple[int, int]] = {(start_x, start_y)}

        frontier: List[Tuple[int, int, int, int, int]] = []

        for nx, ny, direction in self._get_unvisited_neighbors(
            start_x, start_y, visited
        ):
            frontier.append((nx, ny, start_x, start_y, direction))

        while frontier:
            idx = self.rng.randrange(len(frontier))
            nx, ny, fx, fy, direction = frontier[idx]
            frontier[idx] = frontier[-1]
            frontier.pop()

            if (nx, ny) in visited:
                continue

            self._carve_between(fx, fy, nx, ny, direction)
            visited.add((nx, ny))

            yield

            for nnx, nny, ndir in self._get_unvisited_neighbors(
                nx, ny, visited
            ):
                frontier.append((nnx, nny, nx, ny, ndir))

        if not self.perfect:
            self._make_imperfect()
