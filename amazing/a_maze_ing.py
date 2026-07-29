from mazegen.maze import Maze
from mazegen.algo.prim import Prim
from mazegen.algo.a_star import A_Star
from src.display.mlx_display import MlxDisplay
from src.parsing import Parsing, MissingKeyError, PositionError, FileNameError
from src.maze_output import MazeWriter
import sys


def load_config(path: str) -> Parsing:
    """Load and validate configuration from a file.

    Args:
        path (str): Path to the configuration file.

    Returns:
        Parsing: Validated configuration object.
    """
    data: dict[str, str] = {}

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, _, value = line.partition('=')
            data[key.strip()] = value.strip()
        return Parsing.model_validate(data)


def main(ac: int, av: list[str]) -> None:
    """Run the maze generation program.

    Args:
        ac (int): Number of command-line arguments.
        av (list[str]): Command-line arguments.
    """
    if len(av) == 1:
        print("You must add the config file")
        print("python3 a_maze_ing.py <file_name.txt> OR make run")
        return
    if not av[1].endswith(".txt"):
        print("You must use a text file (exemple: config.txt)")
        return
    try:
        config = load_config(av[1])
    except MissingKeyError as e:
        print(f"Config incomplète : {e}")
        exit(1)
    except PositionError as e:
        print(f"Coordonnées invalides : {e}")
        exit(1)
    except FileNameError as e:
        print(f"Nom de fichier invalide : {e}")
        exit(1)
    except ValueError as e:
        print(f"Valeur invalide : {e}")
        exit(1)
    try:
        maze = Maze(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit_=config.exit,
            perfect=config.perfect,
            seed=config.seed,
        )
        maze.initialize()
        display = MlxDisplay(maze, Prim)
        display.run()
        if not maze.is_done():
            maze.run_all()
        if not maze.has_solution:
            maze.solve(A_Star)
        writer = MazeWriter(maze, config.output_file)
        writer.output()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(f"Error: {e}")
