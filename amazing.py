import pytest
from mazegen.maze import Maze, MazeState
from mazegen.algo.prim import Prim
from src.display.mlx_display import MlxDisplay

def main() -> None:
    try:
        maze = Maze(20, 20, (0, 0), (19, 19), seed=42)
        maze.initialize()
        display = MlxDisplay(maze, Prim)
        display.run()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except Error as e:
        print(f"Error: {e}")
