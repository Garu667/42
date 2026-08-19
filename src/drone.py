from enum import Enum, auto

from src.zone import Zone


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
