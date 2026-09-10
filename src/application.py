import argparse
import sys

from src.graph import Graph
from src.parsing import ParseError, Parser
from src.scheduler import Scheduler, SchedulingError
from src.terminal_display import TerminalDisplay


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
        from src.visualizer import Visualizer
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
