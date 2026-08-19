from src.connection import Connection
from src.drone import Drone, DroneStatus
from src.graph import Graph
from src.pathfinder import Pathfinder
from src.zone import Zone, ZoneType

MAX_TURNS = 5000


class SchedulingError(Exception):
    """Raised when no valid schedule can be produced."""


class Scheduler:
    """Plans and simulates the movement of all drones through a Graph.

    Every drone follows the same precomputed shortest path. Conflicts
    over zone and connection capacity are resolved turn by turn in
    drone-id priority order. Restricted-zone transits reserve their
    destination one turn ahead, since a drone cannot wait mid-transit
    once committed.
    """

    def __init__(self, graph: Graph, nb_drones: int) -> None:
        self._graph = graph
        self._drones = self._plan_drones(graph, nb_drones)
        self._occupancy: dict[str, set[int]] = {
            graph.start.name: {d.drone_id for d in self._drones}
        }
        self._connection_usage: dict[str, dict[int, int]] = {}
        self._future_arrivals: dict[str, dict[int, int]] = {}

    @staticmethod
    def _plan_drones(graph: Graph, nb_drones: int) -> list[Drone]:
        path = Pathfinder(graph).shortest_path(graph.start, graph.end)
        if path is None:
            raise SchedulingError("no path exists between start and end")
        return [Drone(i, path) for i in range(1, nb_drones + 1)]

    def run(self) -> list[list[str]]:
        """Simulate until every drone has arrived.

        Returns:
            One list of move tokens (e.g. 'D1-roof1') per turn that
            had at least one move, in the required output format.
        """
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
        ordered = sorted(self._drones, key=lambda d: d.drone_id)
        for drone in ordered:
            token = self._complete_transit_if_due(drone, turn)
            if token is not None:
                moves.append(token)
        for drone in ordered:
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
        connection = self._graph.get_connection(
            drone.current_zone, next_zone
        )
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
        self._occupancy.setdefault(next_zone.name, set()).add(
            drone.drone_id
        )
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
