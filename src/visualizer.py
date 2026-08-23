from src.camera import Camera
from src.graph import Graph
from src.layout import Layout
from src.replay import Replay
from src.zone import Zone, ZoneType
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame  # noqa: E402

BACKGROUND = (18, 18, 24)
TEXT_COLOR = (230, 230, 230)
CONNECTION_COLOR = (90, 90, 100)
START_COLOR = (230, 200, 60)
END_COLOR = (230, 60, 130)
DENSE_THRESHOLD = 25
DENSE_LABEL_ZOOM = 1.6

ZONE_TYPE_COLORS = {
    ZoneType.NORMAL: (70, 130, 200),
    ZoneType.BLOCKED: (90, 90, 90),
    ZoneType.RESTRICTED: (200, 70, 70),
    ZoneType.PRIORITY: (70, 200, 120),
}

DRONE_COLORS = [
    (255, 200, 60), (255, 100, 100), (100, 200, 255), (200, 100, 255),
    (100, 255, 150), (255, 150, 100), (150, 150, 255), (255, 255, 120),
]


class Visualizer:
    """Draws the network and steps through a simulation's turns.

    Controls: SPACE or right arrow next turn, left arrow previous turn,
    A autoplay, wheel zoom, drag pan, R reset view, ESC quit. On maps
    above DENSE_THRESHOLD zones, labels only show once zoomed in.
    """

    def __init__(
        self,
        graph: Graph,
        turns: list[list[str]],
        nb_drones: int,
        width: int = 1000,
        height: int = 700,
    ) -> None:
        pygame.init()
        pygame.display.set_caption("Fly-in")
        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._width = width
        self._height = height
        self._graph = graph
        self._replay = Replay(graph, turns, nb_drones)
        self._nb_drones = nb_drones
        self._layout = Layout(graph, width, height, top_offset=90)
        self._camera = Camera()
        self._dense = len(graph.zones) > DENSE_THRESHOLD
        self._zone_radius = 10 if self._dense else 18
        self._drone_radius = 4 if self._dense else 6
        self._label_zoom = DENSE_LABEL_ZOOM if self._dense else 0.0
        self._font = pygame.font.SysFont(
            "consolas,dejavusansmono,monospace",
            16 if self._dense else 20,
            bold=True
        )
        self._turn_index = 0
        self._autoplay = False
        self._autoplay_interval_ms = 500
        self._time_since_advance = 0
        self._dragging = False
        self._drag_from = (0, 0)

    def run(self) -> None:
        """Event and render loop until the user closes the window."""
        running = True
        while running:
            dt = self._clock.tick(60)
            running = self._handle_events()
            self._maybe_autoplay(dt)
            self._draw()
        pygame.quit()

    def draw_frame(self, turn_index: int | None = None) -> None:
        """Render a single frame without running the event loop."""
        if turn_index is not None:
            self._turn_index = turn_index
        self._draw()

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if not self._handle_keydown(event.key):
                    return False
            elif event.type == pygame.MOUSEWHEEL:
                factor = 1.15 if event.y > 0 else 1 / 1.15
                self._camera.zoom_at(factor, pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._dragging = True
                self._drag_from = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._dragging = False
            elif event.type == pygame.MOUSEMOTION and self._dragging:
                self._camera.pan(
                    event.pos[0] - self._drag_from[0],
                    event.pos[1] - self._drag_from[1],
                )
                self._drag_from = event.pos
        return True

    def _handle_keydown(self, key: int) -> bool:
        if key == pygame.K_ESCAPE:
            return False
        if key in (pygame.K_SPACE, pygame.K_RIGHT):
            self._step(1)
        elif key == pygame.K_LEFT:
            self._step(-1)
        elif key == pygame.K_a:
            self._autoplay = not self._autoplay
        elif key == pygame.K_r:
            self._camera.reset()
        return True

    def _maybe_autoplay(self, dt: int) -> None:
        if not self._autoplay:
            return
        self._time_since_advance += dt
        if self._time_since_advance < self._autoplay_interval_ms:
            return
        self._time_since_advance = 0
        if self._turn_index < self._replay.total_turns:
            self._step(1)
        else:
            self._autoplay = False

    def _step(self, delta: int) -> None:
        self._turn_index = max(
            0, min(self._replay.total_turns, self._turn_index + delta)
        )

    def _screen_pos(self, zone: Zone) -> tuple[int, int]:
        return self._camera.to_screen(*self._layout.position(zone))

    def _draw(self) -> None:
        self._screen.fill(BACKGROUND)
        self._draw_connections()
        self._draw_zones()
        self._draw_drones()
        self._draw_hud()
        pygame.display.flip()

    def _draw_connections(self) -> None:
        seen = set()
        width = max(1, int(2 * self._camera.zoom))
        for zone in self._graph.zones:
            for neighbor, connection in self._graph.neighbors(zone):
                if connection.name in seen:
                    continue
                seen.add(connection.name)
                pygame.draw.line(
                    self._screen,
                    CONNECTION_COLOR,
                    self._screen_pos(zone),
                    self._screen_pos(neighbor),
                    width,
                )

    def _draw_zones(self) -> None:
        radius = max(2, int(self._zone_radius * self._camera.zoom))
        show_labels = self._camera.zoom >= self._label_zoom
        for zone in self._graph.zones:
            x, y = self._screen_pos(zone)
            if not -radius <= x <= self._width + radius:
                continue
            if not -radius <= y <= self._height + radius:
                continue
            pygame.draw.circle(
                self._screen, self._zone_color(zone), (x, y), radius
            )
            if show_labels:
                label = self._font.render(zone.name, True, TEXT_COLOR)
                self._screen.blit(
                    label, (x - label.get_width() // 2, y + radius + 2)
                )

    @staticmethod
    def _zone_color(zone: Zone) -> tuple[int, int, int]:
        if zone.is_start:
            return START_COLOR
        if zone.is_end:
            return END_COLOR
        return ZONE_TYPE_COLORS[zone.zone_type]

    def _draw_drones(self) -> None:
        radius = max(2, int(self._drone_radius * self._camera.zoom))
        positions = self._replay.positions_at(self._turn_index)
        for drone_id, state in positions.items():
            color = DRONE_COLORS[(drone_id - 1) % len(DRONE_COLORS)]
            if state.target_zone is not None:
                world = self._layout.interpolated(
                    state.zone, state.target_zone, 0.5
                )
                x, y = self._camera.to_screen(*world)
            else:
                x, y = self._screen_pos(state.zone)
                x += int(((drone_id * 7) % 20 - 10) * self._camera.zoom)
                y += int(((drone_id * 13) % 20 - 10) * self._camera.zoom)
            pygame.draw.circle(self._screen, color, (x, y), radius)

    def _draw_hud(self) -> None:
        positions = self._replay.positions_at(self._turn_index)
        delivered = sum(
            1
            for state in positions.values()
            if state.zone.is_end and state.target_zone is None
        )
        lines = [
            f"Turn {self._turn_index} / {self._replay.total_turns}",
            f"Delivered: {delivered} / {self._nb_drones}",
            "SPACE/-> next   <- prev   A autoplay   wheel zoom   "
            "drag pan   R reset   ESC quit",
        ]
        for i, text in enumerate(lines):
            surface = self._font.render(text, True, TEXT_COLOR)
            self._screen.blit(surface, (10, 10 + i * 18))
