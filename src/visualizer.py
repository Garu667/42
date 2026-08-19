import pygame

from src.graph import Graph
from src.layout import Layout
from src.replay import Replay
from src.zone import ZoneType

BACKGROUND = (18, 18, 24)
TEXT_COLOR = (230, 230, 230)
ZONE_RADIUS = 18
DRONE_RADIUS = 6
CONNECTION_COLOR = (90, 90, 100)

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
    """Renders the network and steps through a simulation's turns.

    Controls: SPACE or right arrow = next turn, left arrow = previous
    turn, A = toggle autoplay, ESC or window close = quit.
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
        self._font = pygame.font.SysFont("consolas", 18)
        self._graph = graph
        self._replay = Replay(graph, turns, nb_drones)
        self._nb_drones = nb_drones
        self._layout = Layout(graph, width, height, top_offset=90)
        self._turn_index = 0
        self._autoplay = False
        self._autoplay_interval_ms = 500
        self._time_since_advance = 0

    def run(self) -> None:
        """Main event and render loop until the user closes the window."""
        running = True
        while running:
            dt = self._clock.tick(60)
            running = self._handle_events()
            self._maybe_autoplay(dt)
            self._draw()
        pygame.quit()

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key in (pygame.K_SPACE, pygame.K_RIGHT):
                    self._step(1)
                elif event.key == pygame.K_LEFT:
                    self._step(-1)
                elif event.key == pygame.K_a:
                    self._autoplay = not self._autoplay
        return True

    def _maybe_autoplay(self, dt: int) -> None:
        if not self._autoplay:
            return
        self._time_since_advance += dt
        if self._time_since_advance >= self._autoplay_interval_ms:
            self._time_since_advance = 0
            if self._turn_index < self._replay.total_turns:
                self._step(1)
            else:
                self._autoplay = False

    def _step(self, delta: int) -> None:
        self._turn_index = max(
            0, min(self._replay.total_turns, self._turn_index + delta)
        )

    def draw_frame(self, turn_index: int | None = None) -> None:
        """Render a single frame without running the event loop."""
        if turn_index is not None:
            self._turn_index = turn_index
        self._draw()

    def _draw(self) -> None:
        self._screen.fill(BACKGROUND)
        self._draw_connections()
        self._draw_zones()
        self._draw_drones()
        self._draw_hud()
        pygame.display.flip()

    def _draw_connections(self) -> None:
        seen = set()
        for zone in self._graph.zones:
            for neighbor, connection in self._graph.neighbors(zone):
                if connection.name in seen:
                    continue
                seen.add(connection.name)
                pygame.draw.line(
                    self._screen,
                    CONNECTION_COLOR,
                    self._layout.position(zone),
                    self._layout.position(neighbor),
                    2,
                )

    def _draw_zones(self) -> None:
        for zone in self._graph.zones:
            color = ZONE_TYPE_COLORS[zone.zone_type]
            if zone.is_start or zone.is_end:
                color = (230, 200, 60) if zone.is_start else (230, 60, 130)
            x, y = self._layout.position(zone)
            pygame.draw.circle(self._screen, color, (x, y), ZONE_RADIUS)
            label = self._font.render(zone.name, True, TEXT_COLOR)
            self._screen.blit(
                label, (x - label.get_width() // 2, y + ZONE_RADIUS + 2)
            )

    def _draw_drones(self) -> None:
        positions = self._replay.positions_at(self._turn_index)
        for drone_id, state in positions.items():
            color = DRONE_COLORS[(drone_id - 1) % len(DRONE_COLORS)]
            if state.target_zone is not None:
                x, y = self._layout.interpolated(
                    state.zone, state.target_zone, 0.5
                )
            else:
                x, y = self._layout.position(state.zone)
                x += ((drone_id * 7) % 20) - 10
                y += ((drone_id * 13) % 20) - 10
            pygame.draw.circle(self._screen, color, (x, y), DRONE_RADIUS)

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
            "SPACE/-> next turn   <- prev turn   A autoplay   ESC quit",
        ]
        for i, text in enumerate(lines):
            surface = self._font.render(text, True, TEXT_COLOR)
            self._screen.blit(surface, (10, 10 + i * 22))
