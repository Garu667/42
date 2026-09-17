from enum import Enum, auto

from src.network import Connection, Graph, Zone, ZoneType
from src.pathfinding import Congestion, Pathfinder, SpaceTimePlanner


class DroneStatus(Enum):
    """Lifecycle state of a drone during the simulation."""

    AT_ZONE = auto()
    IN_TRANSIT = auto()
    ARRIVED = auto()


class Drone:
    """A single drone following a precomputed path to the end zone."""

    def __init__(self, drone_id: int, path: list[Zone]) -> None:
        self.drone_id = drone_id
        self.path = path
        self.path_index = 0
        self.status = DroneStatus.AT_ZONE
        self.transit_arrival_turn: int | None = None

    @property
    def label(self) -> str:
        """Output identifier, e.g. 'D3'."""
        return f"D{self.drone_id}"

    @property
    def current_zone(self) -> Zone:
        """The zone this drone currently occupies."""
        return self.path[self.path_index]

    @property
    def next_zone(self) -> Zone | None:
        """The next zone on the path, None if already at the end."""
        if self.path_index + 1 >= len(self.path):
            return None
        return self.path[self.path_index + 1]

    def has_arrived(self) -> bool:
        """Whether this drone has reached the end of its path."""
        return self.status is DroneStatus.ARRIVED


MAX_TURNS = 5000


class SchedulingError(Exception):
    """Raised when no valid schedule can be produced."""


class Simulation:
    """Runs the turn-by-turn movement of drones on their assigned paths.

    Conflicts are resolved in drone-id order. A restricted-zone transit
    books its destination one turn ahead, as a drone cannot wait on a
    connection once committed.
    """

    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self._graph = graph
        self._drones = drones
        self._occupancy: dict[str, set[int]] = {
            graph.start.name: {d.drone_id for d in drones}
        }
        self._connection_usage: dict[str, dict[int, int]] = {}
        self._future_arrivals: dict[str, dict[int, int]] = {}

    def run(self) -> list[list[str]]:
        """Simulate to completion, one move list per non-empty turn."""
        turns: list[list[str]] = []
        turn = 0
        while not all(d.has_arrived() for d in self._drones):
            turn += 1
            if turn > MAX_TURNS:
                raise SchedulingError(
                    f"no valid schedule found within {MAX_TURNS} turns"
                )
            moves = self._simulate_turn(turn)
            if moves:
                turns.append(moves)
        return turns

    def _simulate_turn(self, turn: int) -> list[str]:
        moves: list[str] = []
        landed: set[int] = set()
        ordered = sorted(self._drones, key=lambda d: d.drone_id)
        for drone in ordered:
            token = self._complete_transit_if_due(drone, turn)
            if token is not None:
                moves.append(token)
                landed.add(drone.drone_id)
        for drone in ordered:
            if drone.drone_id in landed:
                continue
            token = self._attempt_departure(drone, turn)
            if token is not None:
                moves.append(token)
        return moves

    def _complete_transit_if_due(self, drone: Drone, turn: int) -> str | None:
        if drone.status is not DroneStatus.IN_TRANSIT:
            return None
        if drone.transit_arrival_turn != turn:
            return None
        drone.path_index += 1
        zone = drone.current_zone
        self._occupancy.setdefault(zone.name, set()).add(drone.drone_id)
        drone.status = (
            DroneStatus.ARRIVED if drone.next_zone is None
            else DroneStatus.AT_ZONE
        )
        return f"{drone.label}-{zone.name}"

    def _attempt_departure(self, drone: Drone, turn: int) -> str | None:
        if drone.status is not DroneStatus.AT_ZONE:
            return None
        next_zone = drone.next_zone
        if next_zone is None:
            drone.status = DroneStatus.ARRIVED
            return None
        connection = self._graph.get_connection(drone.current_zone, next_zone)
        assert connection is not None
        if next_zone.zone_type is ZoneType.RESTRICTED:
            return self._try_restricted_departure(
                drone, connection, next_zone, turn
            )
        return self._try_simple_move(drone, connection, next_zone, turn)

    def _try_simple_move(
        self,
        drone: Drone,
        connection: Connection,
        next_zone: Zone,
        turn: int,
    ) -> str | None:
        if not self._connection_room(connection, turn):
            return None
        if not self._zone_room_now(next_zone):
            return None
        self._occupancy[drone.current_zone.name].discard(drone.drone_id)
        self._occupancy.setdefault(next_zone.name, set()).add(drone.drone_id)
        self._use_connection(connection, turn)
        drone.path_index += 1
        drone.status = (
            DroneStatus.ARRIVED if drone.next_zone is None
            else DroneStatus.AT_ZONE
        )
        return f"{drone.label}-{next_zone.name}"

    def _try_restricted_departure(
        self,
        drone: Drone,
        connection: Connection,
        next_zone: Zone,
        turn: int,
    ) -> str | None:
        arrival_turn = turn + 1
        if not self._connection_room(connection, turn):
            return None
        if not self._connection_room(connection, arrival_turn):
            return None
        if not self._zone_room_future(next_zone, arrival_turn):
            return None
        self._occupancy[drone.current_zone.name].discard(drone.drone_id)
        self._use_connection(connection, turn)
        self._use_connection(connection, arrival_turn)
        bucket = self._future_arrivals.setdefault(next_zone.name, {})
        bucket[arrival_turn] = bucket.get(arrival_turn, 0) + 1
        drone.status = DroneStatus.IN_TRANSIT
        drone.transit_arrival_turn = arrival_turn
        return f"{drone.label}-{connection.name}"

    def _zone_room_now(self, zone: Zone) -> bool:
        if zone.capacity is None:
            return True
        return len(self._occupancy.get(zone.name, set())) < zone.capacity

    def _zone_room_future(self, zone: Zone, turn: int) -> bool:
        if zone.capacity is None:
            return True
        booked = self._future_arrivals.get(zone.name, {}).get(turn, 0)
        current = len(self._occupancy.get(zone.name, set()))
        return current + booked < zone.capacity

    def _connection_room(self, connection: Connection, turn: int) -> bool:
        used = self._connection_usage.get(connection.name, {}).get(turn, 0)
        return used < connection.max_link_capacity

    def _use_connection(self, connection: Connection, turn: int) -> None:
        bucket = self._connection_usage.setdefault(connection.name, {})
        bucket[turn] = bucket.get(turn, 0) + 1


class Scheduler:
    """Assigns paths to drones and keeps the shorter of two strategies.

    The shared strategy sends every drone down the single cheapest path.
    The spread strategy gives each drone its own path, assigned from the
    highest drone id down, so the drones leaving last get the cheapest
    routes and earlier ones are pushed onto alternate branches. The
    spacetime strategy plans in (zone, turn) space so drones can wait
    and pipeline through narrow corridors.
    """

    def __init__(self, graph: Graph, nb_drones: int) -> None:
        self._graph = graph
        self._nb_drones = nb_drones

    def run(self) -> list[list[str]]:
        """Return the shortest turn-by-turn output of every strategy."""
        plans = [self._shared_plan(), self._spread_plan()]
        results = [Simulation(self._graph, plan).run() for plan in plans]
        timed = self._spacetime_turns()
        if timed is not None:
            results.append(timed)
        return min(results, key=len)

    def _spacetime_turns(self) -> list[list[str]] | None:
        planner = SpaceTimePlanner(self._graph)
        plans = planner.plan(self._nb_drones)
        if plans is None:
            return None
        return planner.to_turns(plans)

    def _shared_plan(self) -> list[Drone]:
        path = Pathfinder(self._graph).shortest_path(
            self._graph.start, self._graph.end
        )
        if path is None:
            raise SchedulingError("no path exists between start and end")
        return [Drone(i, path) for i in range(1, self._nb_drones + 1)]

    def _spread_plan(self) -> list[Drone]:
        pathfinder = Pathfinder(self._graph)
        congestion = Congestion()
        paths: dict[int, list[Zone]] = {}
        for drone_id in range(self._nb_drones, 0, -1):
            path = pathfinder.shortest_path(
                self._graph.start, self._graph.end, congestion
            )
            if path is None:
                raise SchedulingError("no path exists between start and end")
            congestion.record(path, self._graph)
            paths[drone_id] = path
        return [Drone(i, paths[i]) for i in range(1, self._nb_drones + 1)]
