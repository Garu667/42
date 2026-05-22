"""
mazegen.maze
~~~~~~~~~~~~

Classe principale ``Maze`` — gère le cycle de vie d'un labyrinthe.

States:

    BLANK → INITIALIZED → GENERATING → GENERATED
                ↑                           |
                └─────── reset() ───────────┘

Example::

    from mazegen.maze import Maze
    from mazegen.algorithms.prim import PrimGenerator
    from mazegen.algorithms.bfs import BFSSolver

    maze = Maze(20, 15, (0, 0), (19, 14), seed=42)
    maze.initialize()
    maze.generate(PrimGenerator)

    # Sans animation — génère d'un coup
    while not maze.is_done():
        maze.tick()

    maze.solve(BFSSolver)
    print(maze.solution)
"""

from __future__ import annotations

import random
from collections.abc import Generator
from enum import IntEnum
from typing import Optional, Type

from mazegen.algorithms.base import BaseGenerator, BaseSolver


NORTH: int = 0x1
EAST:  int = 0x2
SOUTH: int = 0x4
WEST:  int = 0x8

OPPOSITE: dict[int, int] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST:  WEST,
    WEST:  EAST,
}

DELTA: dict[int, tuple[int, int]] = {
    NORTH: (0, -1),
    SOUTH: (0,  1),
    EAST:  (1,  0),
    WEST:  (-1, 0),
}


_DIGIT_4: list[list[int]] = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1],
]

_DIGIT_2: list[list[int]] = [
    [1, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1],
]

_PATTERN_W: int = 7
_PATTERN_H: int = 5

class MazeState(IntEnum):
    """Cycle de vie d'un labyrinthe.

    Les valeurs entières permettent des comparaisons ordinales :
    ``state >= MazeState.GENERATED``.
    """

    BLANK       = 0   # Objet créé, aucune grille allouée
    INITIALIZED = 1   # Grille à 0xF, pattern "42" placé
    GENERATING  = 2   # Algorithme en cours (yields intermédiaires)
    GENERATED   = 3   # Labyrinthe complet et valide
    ERROR       = -1  # Paramètres invalides ou génération échouée

class Maze:
    """Gère le cycle de vie complet d'un labyrinthe.

    Cette classe est le point d'entrée principal de ``mazegen``. Elle ne
    contient aucun algorithme — elle délègue la génération à un
    ``BaseGenerator`` et la résolution à un ``BaseSolver``.

    Args:
        width:   Nombre de colonnes. Minimum 2.
        height:  Nombre de lignes. Minimum 2.
        entry:   ``(x, y)`` de la cellule d'entrée.
        exit_:   ``(x, y)`` de la cellule de sortie.
        perfect: Labyrinthe parfait si ``True`` (chemin unique).
        seed:    Graine pour la reproductibilité.

    Raises:
        ValueError: Si les paramètres sont invalides.

    Example::
        maze = Maze(20, 15, (0, 0), (19, 14), seed=42)
        maze.initialize()
        maze.generate(PrimGenerator)
        while not maze.is_done():
            maze.tick()
        maze.solve(BFSSolver)
    """

    MIN_SIZE_FOR_42: tuple[int, int] = (_PATTERN_W + 2, _PATTERN_H + 2)

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        """Initialise et valide les paramètres sans allouer la grille."""
        self._validate(width, height, entry, exit_)

        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit_
        self._perfect = perfect
        self._seed = seed

        self._state: MazeState = MazeState.BLANK
        self._grid: list[list[int]] = []
        self._42_cells: set[tuple[int, int]] = set()
        self._solution: list[str] = []
        self._iterator: Optional[Generator[None, None, None]] = None


    @property
    def state(self) -> MazeState:
        """État courant du labyrinthe."""
        return self._state

    @property
    def width(self) -> int:
        """Nombre de colonnes."""
        return self._width

    @property
    def height(self) -> int:
        """Nombre de lignes."""
        return self._height

    @property
    def entry(self) -> tuple[int, int]:
        """Coordonnées ``(x, y)`` de l'entrée."""
        return self._entry

    @property
    def exit(self) -> tuple[int, int]:
        """Coordonnées ``(x, y)`` de la sortie."""
        return self._exit

    @property
    def grid(self) -> list[list[int]]:
        """Copie de la grille 2D ``grid[y][x]``, disponible dès INITIALIZED.

        Raises:
            RuntimeError: Si l'état est BLANK.
        """
        self._require_state_gte(MazeState.INITIALIZED, "grid")
        return [row[:] for row in self._grid]

    @property
    def forty_two_cells(self) -> set[tuple[int, int]]:
        """Positions ``(x, y)`` des cellules du pattern "42".

        Raises:
            RuntimeError: Si l'état est BLANK.
        """
        self._require_state_gte(MazeState.INITIALIZED, "forty_two_cells")
        return set(self._42_cells)

    @property
    def solution(self) -> list[str]:
        """Chemin de l'entrée à la sortie sous forme de lettres directionnelles.

        Raises:
            RuntimeError: Si ``solve()`` n'a pas encore été appelé.
        """
        if not self._solution:
            raise RuntimeError(
                "Appelez solve() avant d'accéder à la solution."
            )
        return list(self._solution)


    def initialize(self) -> None:
        """Alloue la grille et place le pattern "42".

        Transitions : BLANK → INITIALIZED  (ou ERROR si taille invalide).

        La grille est entièrement remplie de murs (``0xF``).
        Le pattern "42" est centré et ses cellules marquées comme bloquées.
        Si le labyrinthe est trop petit pour "42", un avertissement est
        affiché mais l'initialisation continue.
        """
        try:
            self._grid = [[0xF] * self._width for _ in range(self._height)]
            self._42_cells = set()
            self._solution = []
            self._iterator = None

            if self.can_fit_42():
                self._place_42()
            else:
                print(
                    f"[Warning] Trop petit pour le pattern '42' "
                    f"(minimum {self.MIN_SIZE_FOR_42[0]}×"
                    f"{self.MIN_SIZE_FOR_42[1]})."
                )

            self._state = MazeState.INITIALIZED

        except Exception as e:
            self._state = MazeState.ERROR
            raise RuntimeError(f"Échec de l'initialisation : {e}") from e

    def generate(self, algo: Type[BaseGenerator]) -> None:
        """Lance la génération du labyrinthe avec l'algorithme donné.

        L'algorithme n'est pas exécuté immédiatement — son générateur est
        stocké. Appelez ``tick()`` pour avancer étape par étape, ou
        ``run_all()`` pour générer d'un coup.

        Transitions : INITIALIZED → GENERATING

        Args:
            algo: Classe héritant de ``BaseGenerator`` (ex: PrimGenerator).

        Raises:
            RuntimeError: Si l'état n'est pas INITIALIZED.
        """
        self._require_state(MazeState.INITIALIZED, "generate()")

        try:
            rng = random.Random(self._seed)
            instance = algo(
                grid=self._grid,
                width=self._width,
                height=self._height,
                entry=self._entry,
                exit_=self._exit,
                blocked=self._42_cells,
                perfect=self._perfect,
                rng=rng,
            )
            self._iterator = instance.run()
            self._state = MazeState.GENERATING

        except Exception as e:
            self._state = MazeState.ERROR
            raise RuntimeError(f"Échec du lancement de la génération : {e}") from e

    def tick(self) -> bool:
        """Avance la génération d'une étape (un ``yield`` de l'algo).

        Conçu pour être appelé à chaque frame par la MLX ou dans une boucle.
        Passe automatiquement en GENERATED quand l'algo est terminé.

        Transitions : GENERATING → GENERATING  (ou → GENERATED à la fin)

        Returns:
            ``True`` si la génération est toujours en cours,
            ``False`` si elle vient de se terminer.

        Raises:
            RuntimeError: Si l'état n'est pas GENERATING.
        """
        self._require_state(MazeState.GENERATING, "tick()")

        try:
            next(self._iterator)    # type: ignore[arg-type]
            return True
        except StopIteration:
            self._state = MazeState.GENERATED
            self._iterator = None
            return False

    def run_all(self) -> None:
        """Génère le labyrinthe en entier sans animation.

        Équivaut à appeler ``tick()`` jusqu'à épuisement du générateur.

        Transitions : GENERATING → GENERATED

        Raises:
            RuntimeError: Si l'état n'est pas GENERATING.
        """
        self._require_state(MazeState.GENERATING, "run_all()")
        while self.tick():
            pass

    def solve(self, solver: Type[BaseSolver]) -> None:
        """Résout le labyrinthe et stocke le chemin le plus court.

        Args:
            solver: Classe héritant de ``BaseSolver`` (ex: BFSSolver).

        Raises:
            RuntimeError: Si l'état n'est pas GENERATED.
            ValueError:   Si aucun chemin n'existe.
        """
        self._require_state(MazeState.GENERATED, "solve()")

        instance = solver(
            grid=self._grid,
            width=self._width,
            height=self._height,
            entry=self._entry,
            exit_=self._exit,
        )
        result = instance.solve()

        if not result:
            raise ValueError(
                "Aucun chemin trouvé entre l'entrée et la sortie."
            )

        self._solution = result

    def reset(self) -> None:
        """Remet le labyrinthe à zéro et le réinitialise immédiatement.

        Transitions : (n'importe quel état) → BLANK → INITIALIZED

        Utile pour régénérer un nouveau labyrinthe avec les mêmes paramètres
        (ex: appui sur 'R' dans la MLX).
        """
        self._state = MazeState.BLANK
        self._grid = []
        self._42_cells = set()
        self._solution = []
        self._iterator = None
        self.initialize()

    def is_done(self) -> bool:
        """Retourne ``True`` si la génération est terminée (état GENERATED)."""
        return self._state == MazeState.GENERATED

    def can_fit_42(self) -> bool:
        """Retourne ``True`` si le labyrinthe est assez grand pour "42"."""
        min_w, min_h = self.MIN_SIZE_FOR_42
        return self._width >= min_w and self._height >= min_h


    def carve(self, x: int, y: int, direction: int) -> None:
        """Ouvre le mur entre ``(x, y)`` et son voisin dans *direction*.

        Met à jour les deux cellules pour garantir la cohérence des murs.

        Args:
            x:         Colonne de la cellule source.
            y:         Ligne de la cellule source.
            direction: ``NORTH``, ``EAST``, ``SOUTH`` ou ``WEST``.
        """
        dx, dy = DELTA[direction]
        nx, ny = x + dx, y + dy
        self._grid[y][x]   &= ~direction
        self._grid[ny][nx] &= ~OPPOSITE[direction]

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        """Retourne ``True`` si le mur dans *direction* est fermé.

        Args:
            x:         Colonne de la cellule.
            y:         Ligne de la cellule.
            direction: ``NORTH``, ``EAST``, ``SOUTH`` ou ``WEST``.
        """
        return bool(self._grid[y][x] & direction)

    def in_bounds(self, x: int, y: int) -> bool:
        """Retourne ``True`` si ``(x, y)`` est dans les limites de la grille."""
        return 0 <= x < self._width and 0 <= y < self._height

    def is_blocked(self, x: int, y: int) -> bool:
        """Retourne ``True`` si ``(x, y)`` appartient au pattern "42"."""
        return (x, y) in self._42_cells

    def get_neighbors(
        self, x: int, y: int
    ) -> list[tuple[int, int, int]]:
        """Retourne les voisins passables de ``(x, y)``.

        Un voisin est passable s'il est dans les limites et n'est pas
        une cellule bloquée ("42").

        Args:
            x: Colonne de la cellule source.
            y: Ligne de la cellule source.

        Returns:
            Liste de ``(voisin_x, voisin_y, direction)`` tuples.
        """
        result: list[tuple[int, int, int]] = []
        for direction, (dx, dy) in DELTA.items():
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and not self.is_blocked(nx, ny):
                result.append((nx, ny, direction))
        return result


    @staticmethod
    def _validate(
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        """Lève ``ValueError`` si les paramètres sont invalides."""
        if width < 2 or height < 2:
            raise ValueError("Les dimensions doivent être au minimum 2×2.")
        ex, ey = entry
        if not (0 <= ex < width and 0 <= ey < height):
            raise ValueError(
                f"L'entrée {entry} est hors limites ({width}×{height})."
            )
        fx, fy = exit_
        if not (0 <= fx < width and 0 <= fy < height):
            raise ValueError(
                f"La sortie {exit_} est hors limites ({width}×{height})."
            )
        if entry == exit_:
            raise ValueError("L'entrée et la sortie doivent être différentes.")

    def _require_state(self, expected: MazeState, action: str) -> None:
        """Lève ``RuntimeError`` si l'état courant n'est pas *expected*."""
        if self._state != expected:
            raise RuntimeError(
                f"'{action}' requiert l'état {expected.name}, "
                f"état actuel : {self._state.name}."
            )

    def _require_state_gte(self, minimum: MazeState, prop: str) -> None:
        """Lève ``RuntimeError`` si l'état est inférieur à *minimum*."""
        if self._state < minimum:
            raise RuntimeError(
                f"'{prop}' non disponible en état {self._state.name} "
                f"(minimum requis : {minimum.name})."
            )


    def _place_42(self) -> None:
        """Estampille le pattern "42" centré dans la grille."""
        start_x = (self._width  - _PATTERN_W) // 2
        start_y = (self._height - _PATTERN_H) // 2

        for row, bits in enumerate(_DIGIT_4):
            for col, on in enumerate(bits):
                if on:
                    self._42_cells.add((start_x + col, start_y + row))

        x_off = start_x + len(_DIGIT_4[0]) + 1
        for row, bits in enumerate(_DIGIT_2):
            for col, on in enumerate(bits):
                if on:
                    self._42_cells.add((x_off + col, start_y + row))
