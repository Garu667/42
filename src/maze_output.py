from mazegen.maze import Maze

class MazeWriter:
    def __init__(self, maze: Maze, output_path: str) -> None:
        self._maze = maze
        self._output_path = output_path

    def output(self) -> None:
        """Écrit le fichier de sortie au format imposé par le sujet."""
        grid = self._maze.grid
        solution = self._maze.solution

        with open(self._output_path, 'w') as f:
            # Grille hex — une ligne par row
            for row in grid:
                f.write("".join(f"{cell:X}" for cell in row) + "\n")

            # Ligne vide
            f.write("\n")

            # Entrée, sortie, chemin
            ex, ey = self._maze.entry
            fx, fy = self._maze.exit
            f.write(f"{ex},{ey}\n")
            f.write(f"{fx},{fy}\n")
            f.write("".join(solution) + "\n")
