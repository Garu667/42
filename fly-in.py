import argparse
import sys

from src.parsing import ParseError, Parser
from src.scheduler import Scheduler, SchedulingError
from src.terminal_display import TerminalDisplay


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Route a fleet of drones through a zone network."
    )
    parser.add_argument("map_file", help="Path to a map description file")
    parser.add_argument(
        "-n", "--no-gui",
        action="store_true",
        help="Disable the pygame graphical replay window",
    )
    return parser.parse_args()


def main() -> None:
    """Parse the map, run the simulation and display the result."""
    args = parse_args()
    graph, nb_drones = Parser().parse(args.map_file)
    turns = Scheduler(graph, nb_drones).run()
    display = TerminalDisplay(graph)
    display.show_legend()
    for i, tokens in enumerate(turns, start=1):
        display.show_turn(i, tokens)
    display.show_summary(total_turns=len(turns), nb_drones=nb_drones)
    if not args.no_gui:
        from src.visualizer import Visualizer
        Visualizer(graph, turns, nb_drones).run()


if __name__ == "__main__":
    try:
        main()
    except (ParseError, SchedulingError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error: cannot read map file: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)
