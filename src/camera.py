MIN_ZOOM = 0.4
MAX_ZOOM = 6.0


class Camera:
    """Pan and zoom transform applied on top of Layout's world pixels."""

    def __init__(self) -> None:
        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0

    def to_screen(self, world_x: int, world_y: int) -> tuple[int, int]:
        """World pixel coordinates translated to screen coordinates."""
        sx = (world_x + self.pan_x) * self.zoom
        sy = (world_y + self.pan_y) * self.zoom
        return int(sx), int(sy)

    def zoom_at(self, factor: float, anchor: tuple[int, int]) -> None:
        """Zoom by `factor`, keeping the world point under `anchor` fixed."""
        old_zoom = self.zoom
        new_zoom = max(MIN_ZOOM, min(MAX_ZOOM, old_zoom * factor))
        if new_zoom == old_zoom:
            return
        ax, ay = anchor
        world_x = ax / old_zoom - self.pan_x
        world_y = ay / old_zoom - self.pan_y
        self.zoom = new_zoom
        self.pan_x = ax / new_zoom - world_x
        self.pan_y = ay / new_zoom - world_y

    def pan(self, dx: int, dy: int) -> None:
        """Shift the view by a screen-space offset."""
        self.pan_x += dx / self.zoom
        self.pan_y += dy / self.zoom

    def reset(self) -> None:
        """Return to the default unzoomed, uncentered view."""
        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
