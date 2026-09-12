import heapq

from src.connection import Connection
from src.graph import Graph
from src.zone import Zone, ZoneType

Step = tuple[str, int, str, int, Connection | None]


class Reservations:
    """Occupancy already booked by planned drones, indexed by turn."""

    def __init__(self) -> None:
        self._zones: dict[tuple[str, int], int] = {}
        self._links: dict[tuple[str, int], int] = {}

    def zone_free(self, zone: Zone, time: int) -> bool:
        """Whether `zone` still has room at `time`."""
        if zone.capacity is None:
            return True
        return self._zones.get((zone.name, time), 0) < zone.capacity

    def link_free(self, connection: Connection, turn: int) -> bool:
        """Whether `connection` still has room during `turn`."""
        used = self._links.get((connection.name, turn), 0)
        return used < connection.max_link_capacity

    def book(self, steps: list[Step]) -> None:
        """Reserve every zone-time and link-turn slot used by `steps`."""
        for departure, left_at, arrival, reached_at, connection in steps:
            self._zones[(departure, left_at)] = (
                self._zones.get((departure, left_at), 0) + 1
            )
            if connection is None:
                continue
            for turn in range(left_at + 1, reached_at + 1):
                key = (connection.name, turn)
                self._links[key] = self._links.get(key, 0) + 1
        last = steps[-1]
        key_zone = (last[2], last[3])
        self._zones[key_zone] = self._zones.get(key_zone, 0) + 1


class SpaceTimePlanner:
    """Plans each drone through (zone, turn) space, avoiding bookings.

    Drones are planned one after another; each new drone treats the
    slots already taken as blocked, so it either waits or takes another
    branch instead of colliding. This is what lets a fleet pipeline
    through capacity-1 corridors and around restricted zones.
    """

    HORIZON = 400

    def __init__(self, graph: Graph) -> None:
        self._graph = graph
        self._remaining = self._backward_costs()

    def plan(self, nb_drones: int) -> list[list[Step]] | None:
        """Plan every drone, or None if one of them cannot be routed."""
        reservations = Reservations()
        plans: list[list[Step]] = []
        for _ in range(nb_drones):
            steps = self._plan_one(reservations)
            if steps is None:
                return None
            reservations.book(steps)
            plans.append(steps)
        return plans

    def _backward_costs(self) -> dict[str, int]:
        best = {self._graph.end.name: 0}
        heap = [(0, self._graph.end.name)]
        while heap:
            cost, name = heapq.heappop(heap)
            if cost != best.get(name):
                continue
            zone = self._graph.get_zone(name)
            for neighbor, _connection in self._graph.neighbors(zone):
                if not neighbor.is_passable():
                    continue
                new_cost = cost + zone.movement_cost
                if new_cost < best.get(neighbor.name, self.HORIZON):
                    best[neighbor.name] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor.name))
        return best

    def _plan_one(self, reservations: Reservations) -> list[Step] | None:
        start, end = self._graph.start, self._graph.end
        heap = [(self._heuristic(start.name), 0, start.name)]
        came: dict[tuple[str, int], tuple[str, int, Connection | None]] = {}
        seen = {(start.name, 0)}
        while heap:
            _, time, name = heapq.heappop(heap)
            if name == end.name:
                return self._reconstruct(came, name, time)
            if time >= self.HORIZON:
                continue
            zone = self._graph.get_zone(name)
            self._push_wait(heap, came, seen, reservations, zone, time)
            self._push_moves(heap, came, seen, reservations, zone, time)
        return None

    def _push_wait(
        self,
        heap: list[tuple[int, int, str]],
        came: dict[tuple[str, int], tuple[str, int, Connection | None]],
        seen: set[tuple[str, int]],
        reservations: Reservations,
        zone: Zone,
        time: int,
    ) -> None:
        state = (zone.name, time + 1)
        if state in seen or not reservations.zone_free(zone, time + 1):
            return
        seen.add(state)
        came[state] = (zone.name, time, None)
        heapq.heappush(
            heap, (time + 1 + self._heuristic(zone.name), time + 1, zone.name)
        )

    def _push_moves(
        self,
        heap: list[tuple[int, int, str]],
        came: dict[tuple[str, int], tuple[str, int, Connection | None]],
        seen: set[tuple[str, int]],
        reservations: Reservations,
        zone: Zone,
        time: int,
    ) -> None:
        for neighbor, connection in self._graph.neighbors(zone):
            if not neighbor.is_passable():
                continue
            duration = 2 if neighbor.zone_type is ZoneType.RESTRICTED else 1
            arrival = time + duration
            turns = range(time + 1, arrival + 1)
            if not all(reservations.link_free(connection, t) for t in turns):
                continue
            if not reservations.zone_free(neighbor, arrival):
                continue
            state = (neighbor.name, arrival)
            if state in seen:
                continue
            seen.add(state)
            came[state] = (zone.name, time, connection)
            heapq.heappush(
                heap,
                (arrival + self._heuristic(neighbor.name), arrival,
                 neighbor.name),
            )

    def _heuristic(self, name: str) -> int:
        return self._remaining.get(name, self.HORIZON)

    @staticmethod
    def _reconstruct(
        came: dict[tuple[str, int], tuple[str, int, Connection | None]],
        name: str,
        time: int,
    ) -> list[Step]:
        steps: list[Step] = []
        state = (name, time)
        while state in came:
            previous_name, previous_time, connection = came[state]
            steps.append(
                (previous_name, previous_time, state[0], state[1], connection)
            )
            state = (previous_name, previous_time)
        steps.reverse()
        return steps

    @staticmethod
    def to_turns(plans: list[list[Step]]) -> list[list[str]]:
        """Convert planned steps into one token list per turn."""
        lines: dict[int, list[str]] = {}
        for index, steps in enumerate(plans, start=1):
            for departure, left_at, arrival, reached_at, conn in steps:
                if conn is None:
                    continue
                if reached_at - left_at == 2:
                    lines.setdefault(left_at + 1, []).append(
                        f"D{index}-{conn.name}"
                    )
                lines.setdefault(reached_at, []).append(f"D{index}-{arrival}")
        if not lines:
            return []
        return [lines.get(turn, []) for turn in range(1, max(lines) + 1)]
