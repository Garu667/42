import heapq

from src.graph import Graph
from src.zone import Zone, ZoneType


class Pathfinder:
    """Computes weighted shortest paths, favoring priority zones."""

    def __init__(self, graph: Graph) -> None:
        self._graph = graph

    def shortest_path(self, start: Zone, end: Zone) -> list[Zone] | None:
        """Return the cheapest path from `start` to `end`, None if absent."""
        counter = 0
        best: dict[str, tuple[int, int]] = {start.name: (0, 0)}
        came_from: dict[str, Zone] = {}
        heap: list[tuple[int, int, int, str]] = [(0, 0, counter, start.name)]
        while heap:
            cost, neg_priority, _, name = heapq.heappop(heap)
            if (cost, neg_priority) != best.get(name):
                continue
            if name == end.name:
                return self._reconstruct(came_from, start, end)
            zone = self._graph.get_zone(name)
            for neighbor, _connection in self._graph.neighbors(zone):
                if not neighbor.is_passable():
                    continue
                new_cost = cost + neighbor.movement_cost
                bonus = 1 if neighbor.zone_type is ZoneType.PRIORITY else 0
                new_key = (new_cost, neg_priority - bonus)
                if neighbor.name not in best or new_key < best[neighbor.name]:
                    best[neighbor.name] = new_key
                    came_from[neighbor.name] = zone
                    counter += 1
                    heapq.heappush(
                        heap, (new_key[0], new_key[1], counter, neighbor.name)
                    )
        return None

    @staticmethod
    def _reconstruct(
        came_from: dict[str, Zone], start: Zone, end: Zone
    ) -> list[Zone]:
        path = [end]
        current = end
        while current.name != start.name:
            current = came_from[current.name]
            path.append(current)
        path.reverse()
        return path
