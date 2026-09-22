import argparse
import sys

from rich.console import Console
from rich.errors import StyleSyntaxError
from rich.style import Style
from rich.table import Table
from rich.text import Text

from src.network import Graph, Zone, ZoneType
from src.parsing import ParseError, Parser
from src.simulation import Scheduler, SchedulingError


ZONE_TYPE_STYLE = {
    ZoneType.NORMAL: "cyan",
    ZoneType.BLOCKED: "grey50",
    ZoneType.RESTRICTED: "red",
    ZoneType.PRIORITY: "green",
}


class TerminalDisplay:
    """Prints the required per-turn output, colored per zone.

    Uses the map's `color=` value when it is a valid rich color, and
    falls back to a color keyed on zone type otherwise.
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
        _, _, target = token.partition("-")
        try:
            zone = self._graph.get_zone(target)
        except KeyError:
            return ZONE_TYPE_STYLE[ZoneType.RESTRICTED]
        return self._zone_style(zone)

    def _zone_style(self, zone: Zone) -> str:
        if zone.color and self._is_valid_color(zone.color):
            return zone.color
        if zone.is_end:
            return "bold magenta"
        return ZONE_TYPE_STYLE[zone.zone_type]

    @staticmethod
    def _is_valid_color(value: str) -> bool:
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


class Application:
    """Command-line front end: parses a map, simulates it, displays it."""

    EXIT_SUCCESS = 0
    EXIT_FAILURE = 1
    EXIT_INTERRUPTED = 130

    def __init__(self, argv: list[str] | None = None) -> None:
        self._args = self._build_parser().parse_args(argv)

    def run(self) -> int:
        """Run the whole pipeline and return a process exit code."""
        try:
            return self._execute()
        except (ParseError, SchedulingError) as exc:
            return self._fail(str(exc))
        except OSError as exc:
            return self._fail(f"cannot read map file: {exc}")
        except KeyboardInterrupt:
            return self.EXIT_INTERRUPTED

    def _execute(self) -> int:
        graph, nb_drones = Parser().parse(self._args.map_file)
        turns = Scheduler(graph, nb_drones).run()
        self._show(graph, turns, nb_drones)
        return self.EXIT_SUCCESS

    def _show(
        self, graph: Graph, turns: list[list[str]], nb_drones: int
    ) -> None:
        display = TerminalDisplay(graph)
        display.show_legend()
        for number, tokens in enumerate(turns, start=1):
            display.show_turn(number, tokens)
        display.show_summary(total_turns=len(turns), nb_drones=nb_drones)
        if not self._args.no_gui:
            self._open_gui(graph, turns, nb_drones)

    @staticmethod
    def _open_gui(
        graph: Graph, turns: list[list[str]], nb_drones: int
    ) -> None:
        from src.gui import Visualizer
        Visualizer(graph, turns, nb_drones).run()

    @classmethod
    def _fail(cls, message: str) -> int:
        print(f"Error: {message}", file=sys.stderr)
        return cls.EXIT_FAILURE

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Route a fleet of drones through a zone network."
        )
        parser.add_argument(
            "map_file", help="Path to a map description file"
        )
        parser.add_argument(
            "-n", "--no-gui",
            action="store_true",
            help="Disable the pygame graphical replay window",
        )
        return parser

class CapacityReporter:
    """Shows zone and connection usage after each turn."""

    def __init__(self, graph: Graph, console: Console | None = None) -> None:
        self._graph = graph
        self._console = console or Console()
        self._positions: dict[str, str] = {}

    def show(self, tokens: list[str]) -> None:
        """Print the used/max capacity of every occupied location."""
        for token in tokens:
            drone, _, target = token.partition("-")
            self._positions[drone] = target
        counts: dict[str, int] = {}
        for target in self._positions.values():
            counts[target] = counts.get(target, 0) + 1
        for name, used in sorted(counts.items()):
            self._console.print(f"     {self._describe(name, used)}")

    def _describe(self, name: str, used: int) -> str:
        try:
            capacity = self._graph.get_zone(name).capacity
            limit = "inf" if capacity is None else capacity
            return f"Zone {name}: {used}/{limit} drones"
        except KeyError:
            first, _, second = name.partition("-")
            link = self._graph.get_connection(
                self._graph.get_zone(first), self._graph.get_zone(second)
            )
            limit = link.max_link_capacity if link else "?"
            return f"Connection {name}: {used}/{limit} capacity used"
