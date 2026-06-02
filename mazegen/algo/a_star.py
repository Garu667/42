from mazegen.algo.base import BaseSolver
from collections.abc import Generator
from heapq import heappush, heappop

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000


def heuristic(position1: tuple[int, int], position2: tuple[int, int]) -> int:
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


def can_move(grid: list[list[int]], cell: tuple[int, int],
             neighbor: tuple[int, int]) -> bool:
    cx, cy = cell
    nx, ny = neighbor
    if ny == cy + 1:
        return not (grid[cy][cx] & SOUTH)
    elif ny == cy - 1:
        return not (grid[cy][cx] & NORTH)
    elif nx == cx + 1:
        return not (grid[cy][cx] & EAST)
    elif nx == cx - 1:
        return not (grid[cy][cx] & WEST)
    else:
        return False


def get_accessible_neighbors(grid: list[list[int]], cell: tuple[int, int],
                             width: int, height: int) -> list[tuple[int, int]]:
    x, y = cell
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < width - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < height - 1:
        neighbors.append((x, y + 1))
    return [neighbor
            for neighbor in neighbors
            if can_move(grid, cell, neighbor)]


def reconstruct_path(came_from: dict[tuple[int, int], tuple[int, int]],
                     entry_cell: tuple[int, int],
                     exit_cell: tuple[int, int]) -> list[str]:
    path = []
    current = exit_cell
    while current != entry_cell:
        previous = came_from[current]
        cx, cy = current
        px, py = previous
        if cy == py + 1:
            path.append('S')
        elif cy == py - 1:
            path.append('N')
        elif cx == px + 1:
            path.append('E')
        else:
            path.append('W')
        current = previous
    path.reverse()
    return path


class A_Star(BaseSolver):
    """A* solver"""
    def solve(self) -> list[str]:
        """Resolve the maze using A*.

        Returns:
            List of direction ['N','E','S','W'] or nothing
        """
        open_list: list[tuple[int, int, tuple[int, int]]] = []
        heappush(open_list, (0, 0, self.entry))
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], int] = {self.entry: 0}
        while open_list:
            _, g, current = heappop(open_list)
            if current == self.exit_:
                return reconstruct_path(came_from, self.entry, self.exit_)
            if g > g_score.get(current, float('inf')):
                continue
            for neighbor in get_accessible_neighbors(self.grid, current,
                                                     self.width, self.height):
                g_new = g + 1
                if g_new < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = g_new
                    f = g_new + heuristic(neighbor, self.exit_)
                    came_from[neighbor] = current
                    heappush(open_list, (f, g_new, neighbor))
        return []

    def solve_animated(self) -> Generator[list[str], None, None]:
        open_list: list[tuple[int, int, tuple[int, int]]] = []
        heappush(open_list, (0, 0, self.entry))
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], int] = {self.entry: 0}
        while open_list:
            _, g, current = heappop(open_list)
            if current == self.exit_:
                yield reconstruct_path(came_from, self.entry, self.exit_)
                return
            if g > g_score.get(current, float('inf')):
                continue
            if current in came_from:
                yield reconstruct_path(came_from, self.entry, current)
            for neighbor in get_accessible_neighbors(
                self.grid, current, self.width, self.height
            ):
                g_new = g + 1
                if g_new < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = g_new
                    f = g_new + heuristic(neighbor, self.exit_)
                    came_from[neighbor] = current
                    heappush(open_list, (f, g_new, neighbor))
        yield []
