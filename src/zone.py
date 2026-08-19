from enum import Enum


class ZoneType(Enum):
    """Behaviour category of a zone."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    @property
    def movement_cost(self) -> int:
        """Number of turns required to enter a zone of this type."""
        return 2 if self is ZoneType.RESTRICTED else 1

    @property
    def is_passable(self) -> bool:
        """Whether a drone can enter a zone of this type."""
        return self is not ZoneType.BLOCKED


class Zone:
    """A named node of the network, placed at (x, y)."""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: str | None = None,
        max_drones: int = 1,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.is_start = is_start
        self.is_end = is_end
        self._max_drones = max_drones

    @property
    def capacity(self) -> int | None:
        """Max simultaneous occupants, None for start and end hubs."""
        if self.is_start or self.is_end:
            return None
        return self._max_drones

    @property
    def movement_cost(self) -> int:
        """Number of turns required to enter this zone."""
        return self.zone_type.movement_cost

    def is_passable(self) -> bool:
        """Whether a drone can enter this zone."""
        return self.zone_type.is_passable

    def has_room_for(self, occupant_count: int) -> bool:
        """Whether `occupant_count` drones fit in this zone."""
        if self.capacity is None:
            return True
        return occupant_count <= self.capacity

    def __repr__(self) -> str:
        return f"Zone({self.name!r}, type={self.zone_type.value})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Zone):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
