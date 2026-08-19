from rich.console import Console
from rich.errors import StyleSyntaxError
from rich.style import Style
from rich.table import Table
from rich.text import Text

from src.graph import Graph
from src.zone import Zone, ZoneType

ZONE_TYPE_STYLE = {
    ZoneType.NORMAL: "cyan",
    ZoneType.BLOCKED: "grey50",
    ZoneType.RESTRICTED: "red",
    ZoneType.PRIORITY: "green",
}


class TerminalDisplay:
    """Prints the required per-turn output, colored per zone.

    Uses the map's `color=` value when it's a valid rich color,
    falling back to a color keyed on zone type otherwise.
    """

    def __init__(self, graph: Graph, console: Console | None = None) -> None:
        self._graph = graph
        self._console = console or Console()

    def show_legend(self) -> None:
        """Print a one-time color legend for zone types."""
        legend = Text("Zones: ")
        for zone_type, style in ZONE_TYPE_STYLE.items():
            legend.append(f" {zone_type.value} ", style=f"bold {style}")
        legend.append(" start ", style="bold yellow")
        legend.append(" end ", style="bold magenta")
        self._console.print(legend)
        self._console.print()

    def show_turn(self, turn_number: int, tokens: list[str]) -> None:
        """Print one simulation turn, colored token by token."""
        line = Text(f"{turn_number:>3}: ")
        for i, token in enumerate(tokens):
            if i:
                line.append(" ")
            line.append(token, style=self._style_for_token(token))
        self._console.print(line)

    def _style_for_token(self, token: str) -> str:
        """Style for a `D<ID>-<target>` token, keyed on its destination."""
        _, _, target = token.partition("-")
        try:
            zone = self._graph.get_zone(target)
        except KeyError:
            return ZONE_TYPE_STYLE[ZoneType.RESTRICTED]
        return self._zone_style(zone)

    def _zone_style(self, zone: Zone) -> str:
        """Zone's declared color if valid, else a color for its type."""
        if zone.color and self._is_valid_color(zone.color):
            return zone.color
        if zone.is_end:
            return "bold magenta"
        return ZONE_TYPE_STYLE[zone.zone_type]

    @staticmethod
    def _is_valid_color(value: str) -> bool:
        """Whether rich can render `value` as a style/color."""
        try:
            Style.parse(value)
        except StyleSyntaxError:
            return False
        return True

    def show_summary(self, total_turns: int, nb_drones: int) -> None:
        """Print a final summary table."""
        table = Table(title="Fly-in — simulation complete")
        table.add_column("Metric")
        table.add_column("Value", justify="right")
        table.add_row("Drones delivered", str(nb_drones))
        table.add_row("Total turns", str(total_turns))
        self._console.print()
        self._console.print(table)
