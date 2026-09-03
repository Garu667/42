import heapq

from src.connection import Connection
from src.graph import Graph
from src.zone import Zone, ZoneType

PRIORITY_BONUS = 0.5


class Congestion:
    """Usage counters used to steer later paths away from busy zones."""

    def __init__(self) -> None:
        self._zone_usage: dict[str, int] = {}
        self._connection_usage: dict[str, int] = {}

    def zone_penalty(self, zone: Zone) -> float:
        """Usage-to-capacity ratio of `zone`, 0 if never used."""
        cap = zone.capacity if zone.capacity is not None else float("inf")
        return self._zone_usage.get(zone.name, 0) / cap

    def connection_penalty(self, connection: Connection) -> float:
        """Usage-to-capacity ratio of `connection`, 0 if never used."""
        used = self._connection_usage.get(connection.name, 0)
        return used / connection.max_link_capacity

    def record(self, path: list[Zone], graph: Graph) -> None:
        """Count one more use of every zone and connection of `path`."""
        for zone in path:
            self._zone_usage[zone.name] = (
                self._zone_usage.get(zone.name, 0) + 1
            )
        for a, b in zip(path, path[1:]):
            connection = graph.get_connection(a, b)
            assert connection is not None
            name = connection.name
            self._connection_usage[name] = (
                self._connection_usage.get(name, 0) + 1
            )


class Pathfinder:
    """Dijkstra over zone movement costs, favouring priority zones."""

    def __init__(self, graph: Graph) -> None:
        self._graph = graph

    def shortest_path(
        self,
        start: Zone,
        end: Zone,
        congestion: Congestion | None = None,
        congestion_weight: float = 1.0,
    ) -> list[Zone] | None:
        """Return the cheapest path from `start` to `end`, None if absent.

        With a `congestion`, zones and connections already used cost more,
        which pushes successive calls onto different branches.
        """
        counter = 0
        best: dict[str, float] = {start.name: 0.0}
        came_from: dict[str, Zone] = {}
        heap: list[tuple[float, int, str]] = [(0.0, counter, start.name)]
        while heap:
            cost, _, name = heapq.heappop(heap)
            if cost != best.get(name):
                continue
            if name == end.name:
                return self._reconstruct(came_from, start, end)
            zone = self._graph.get_zone(name)
            for neighbor, connection in self._graph.neighbors(zone):
                if not neighbor.is_passable():
                    continue
                new_cost = cost + self._edge_cost(
                    neighbor, connection, congestion, congestion_weight
                )
                if new_cost >= best.get(neighbor.name, float("inf")) - 1e-9:
                    continue
                best[neighbor.name] = new_cost
                came_from[neighbor.name] = zone
                counter += 1
                heapq.heappush(heap, (new_cost, counter, neighbor.name))
        return None

    @staticmethod
    def _edge_cost(
        neighbor: Zone,
        connection: Connection,
        congestion: Congestion | None,
        weight: float,
    ) -> float:
        penalty = 0.0
        if congestion is not None:
            penalty = weight * (
                congestion.zone_penalty(neighbor)
                + congestion.connection_penalty(connection)
            )
        bonus = (
            PRIORITY_BONUS
            if neighbor.zone_type is ZoneType.PRIORITY
            else 0.0
        )
        return neighbor.movement_cost + penalty - bonus

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
