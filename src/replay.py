from dataclasses import dataclass

from src.graph import Graph
from src.zone import Zone


@dataclass
class DronePosition:
    """A drone's location at a given point in the replay."""

    zone: Zone
    target_zone: Zone | None = None

    @property
    def in_transit(self) -> bool:
        """Whether the drone is mid-flight toward a restricted zone."""
        return self.target_zone is not None


class Replay:
    """Reconstructs each drone's position turn by turn from the log."""

    def __init__(
        self, graph: Graph, turns: list[list[str]], nb_drones: int
    ) -> None:
        self._graph = graph
        self._turns = turns
        self._nb_drones = nb_drones

    @property
    def total_turns(self) -> int:
        """Number of recorded turns."""
        return len(self._turns)

    def positions_at(self, turn_index: int) -> dict[int, DronePosition]:
        """Every drone's position after `turn_index` turns have played."""
        positions = {
            drone_id: DronePosition(zone=self._graph.start)
            for drone_id in range(1, self._nb_drones + 1)
        }
        for turn in self._turns[:turn_index]:
            for token in turn:
                self._apply_token(positions, token)
        return positions

    def _apply_token(
        self, positions: dict[int, DronePosition], token: str
    ) -> None:
        label, _, target = token.partition("-")
        drone_id = int(label[1:])
        state = positions[drone_id]
        if "-" in target:
            name_a, _, name_b = target.partition("-")
            dest_name = name_b if state.zone.name == name_a else name_a
            state.target_zone = self._graph.get_zone(dest_name)
        else:
            state.zone = self._graph.get_zone(target)
            state.target_zone = None
