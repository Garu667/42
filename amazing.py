import pytest
from mazegen.maze import Maze, MazeState
from mazegen.algo.prim import Prim
from src.display.mlx_display import MlxDisplay
from src.parsing import Parsing, MissingKeyError, PositionError, FileNameError

def load_config(path: str) -> Parsing:
    data = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, _, value = line.partition('=')
            data[key.strip()] = value.strip()
    return Parsing(**data)


def main() -> None:

    try:
        config = load_config("config.txt")
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
        if config.animation:
            display = MlxDisplay(maze, Prim)
            display.run()
        else:
            maze.generate(PrimGenerator)
            maze.run_all()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except Error as e:
        print(f"Error: {e}")
