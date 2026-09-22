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


class Connection:
    """A bidirectional link between two zones."""

    def __init__(
        self,
        zone_a: Zone,
        zone_b: Zone,
        max_link_capacity: int = 1,
    ) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    @property
    def name(self) -> str:
        """Name in the simulation output format, e.g. 'roof1-roof2'."""
        return f"{self.zone_a.name}-{self.zone_b.name}"

    def other_end(self, zone: Zone) -> Zone:
        """Return the endpoint opposite to `zone`, else raise ValueError."""
        if zone == self.zone_a:
            return self.zone_b
        if zone == self.zone_b:
            return self.zone_a
        raise ValueError(f"{zone.name!r} not on {self.name!r}")

    def connects(self, zone: Zone) -> bool:
        """Whether `zone` is one of the two endpoints."""
        return zone == self.zone_a or zone == self.zone_b

    def has_room_for(self, in_transit_count: int) -> bool:
        """Whether `in_transit_count` drones fit on this link."""
        return in_transit_count <= self.max_link_capacity

    def __repr__(self) -> str:
        return f"Connection({self.name!r}, cap={self.max_link_capacity})"


class Graph:
    """Zones indexed by name, with an adjacency map of connections."""

    def __init__(self) -> None:
        self._zones: dict[str, Zone] = {}
        self._adjacency: dict[str, list[Connection]] = {}
        self._start: Zone | None = None
        self._end: Zone | None = None

    def add_zone(self, zone: Zone) -> None:
        """Register a zone, raising ValueError on duplicates."""
        if zone.name in self._zones:
            raise ValueError(f"duplicate zone name: {zone.name!r}")
        if zone.is_start:
            if self._start is not None:
                raise ValueError("a start hub is already defined")
            self._start = zone
        if zone.is_end:
            if self._end is not None:
                raise ValueError("an end hub is already defined")
            self._end = zone
        self._zones[zone.name] = zone
        self._adjacency[zone.name] = []

    def add_connection(self, connection: Connection) -> None:
        """Register a connection, raising ValueError if invalid."""
        for zone in (connection.zone_a, connection.zone_b):
            if zone.name not in self._zones:
                raise ValueError(f"unknown zone: {zone.name!r}")
        if self.get_connection(connection.zone_a, connection.zone_b):
            raise ValueError(f"duplicate connection: {connection.name!r}")
        self._adjacency[connection.zone_a.name].append(connection)
        self._adjacency[connection.zone_b.name].append(connection)

    def get_zone(self, name: str) -> Zone:
        """Look up a zone by name, raising KeyError if unknown."""
        return self._zones[name]

    def get_connection(
        self, zone_a: Zone, zone_b: Zone
    ) -> Connection | None:
        """Return the connection between two zones, None if absent."""
        for connection in self._adjacency.get(zone_a.name, []):
            if connection.connects(zone_b):
                return connection
        return None

    def neighbors(self, zone: Zone) -> list[tuple[Zone, Connection]]:
        """Return the neighbors of `zone` with their connection."""
        return [
            (connection.other_end(zone), connection)
            for connection in self._adjacency.get(zone.name, [])
        ]

    @property
    def start(self) -> Zone:
        """The unique start hub, raising ValueError if unset."""
        if self._start is None:
            raise ValueError("no start hub defined")
        return self._start

    @property
    def end(self) -> Zone:
        """The unique end hub, raising ValueError if unset."""
        if self._end is None:
            raise ValueError("no end hub defined")
        return self._end

    @property
    def zones(self) -> list[Zone]:
        """All registered zones."""
        return list(self._zones.values())

    def __len__(self) -> int:
        return len(self._zones)
