import sys
import argparse

from src.parsing import Parser
from src.scheduler import Scheduler

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Route a fleet of drones through a zone network."
    )
    parser.add_argument("map_file", help="Path to a map description file")
    parser.add_argument(
        "-g", "--gui",
        action="store_true",
        help="Also open the pygame graphical replay window",
    )
    return parser.parse_args()

def test() -> None:
    args = parse_args()

    graph, nb_drones = Parser().parse(args.map_file)
    if args.gui:
        print("Not yet")


def main() -> None:
    test()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
