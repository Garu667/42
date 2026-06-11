from mazegen.maze import Maze


class MazeWriter:
    """Write maze data and solution to an output file."""

    def __init__(self, maze: Maze, output_path: str) -> None:
        """Initialize writer with maze and output file path.

        Args:
            maze (Maze): Maze instance to export.
            output_path (str): Path to output file.
        """
        self._maze = maze
        self._output_path = output_path

    def output(self) -> None:
        """Write maze grid, entry/exit and solution to file."""
        grid = self._maze.grid
        solution = self._maze.solution

        with open(self._output_path, 'w') as f:
            for row in grid:
                f.write("".join(f"{cell:X}" for cell in row) + "\n")
            f.write("\n")
            ex, ey = self._maze.entry
            fx, fy = self._maze.exit
            f.write(f"{ex},{ey}\n")
            f.write(f"{fx},{fy}\n")
            f.write("".join(solution) + "\n")
