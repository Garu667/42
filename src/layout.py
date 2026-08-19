from src.graph import Graph
from src.zone import Zone


class Layout:
    """Linear transform from data-space zone coordinates to pixels."""

    def __init__(
        self,
        graph: Graph,
        width: int,
        height: int,
        margin: int = 60,
        top_offset: int = 0,
    ) -> None:
        xs = [zone.x for zone in graph.zones]
        ys = [zone.y for zone in graph.zones]
        self._min_x, self._max_x = min(xs), max(xs)
        self._min_y, self._max_y = min(ys), max(ys)
        self._width = width
        self._height = height
        self._margin = margin
        self._top_offset = top_offset

    def position(self, zone: Zone) -> tuple[int, int]:
        """Pixel position for a zone's center."""
        span_x = max(self._max_x - self._min_x, 1)
        span_y = max(self._max_y - self._min_y, 1)
        usable_w = self._width - 2 * self._margin
        top = self._top_offset + self._margin
        bottom = self._height - self._margin
        usable_h = bottom - top
        px = self._margin + (zone.x - self._min_x) / span_x * usable_w
        py = top + (1 - (zone.y - self._min_y) / span_y) * usable_h
        return int(px), int(py)

    def interpolated(
        self, zone_a: Zone, zone_b: Zone, t: float
    ) -> tuple[int, int]:
        """Pixel position along zone_a -> zone_b at t in [0, 1]."""
        ax, ay = self.position(zone_a)
        bx, by = self.position(zone_b)
        return int(ax + (bx - ax) * t), int(ay + (by - ay) * t)
