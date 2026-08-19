from src.zone import Zone


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
