import argparse

from src.parsing import Parser
from src.scheduler import Scheduler
from src.terminal_display import TerminalDisplay
from src.visualizer import Visualizer


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
    args = parse_args()
    graph, nb_drones = Parser().parse(args.map_file)
    turns = Scheduler(graph, nb_drones).run()
    display = TerminalDisplay(graph)
    display.show_legend()
    for i, tokens in enumerate(turns, start=1):
        display.show_turn(i, tokens)
    display.show_summary(total_turns=len(turns), nb_drones=nb_drones)
    if not args.no_gui:
        Visualizer(graph, turns, nb_drones).run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
