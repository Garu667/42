from src.connection import Connection
from src.zone import Zone


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
