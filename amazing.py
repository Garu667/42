import pytest
from mazegen.maze import Maze, MazeState
from mazegen.algo.prim import Prim
from src.display.mlx_display import MlxDisplay

def main() -> None:
    print("Hello World")
    try:
        maze = Maze(20, 15, (0, 0), (19, 14), seed=42)
        maze.initialize()
        display = MlxDisplay(maze, Prim)
        display.run()
        maze.generate(Prim)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
