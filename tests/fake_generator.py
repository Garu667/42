from collections.abc import Generator
from mazegen.generator import BaseGenerator

class FakeGenerator(BaseGenerator):
    """Algo factice pour les tests — ouvre tous les murs sans logique."""

    def run(self) -> Generator[None, None, None]:
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.blocked:
                    continue
                # Ouvre le mur sud si le voisin existe et n'est pas bloqué
                if y + 1 < self.height and (x, y + 1) not in self.blocked:
                    self.grid[y][x]     &= ~0x4  # South
                    self.grid[y+1][x]   &= ~0x1  # North
                # Ouvre le mur est si le voisin existe et n'est pas bloqué
                if x + 1 < self.width and (x + 1, y) not in self.blocked:
                    self.grid[y][x]     &= ~0x2  # East
                    self.grid[y][x+1]   &= ~0x8  # West
                yield
