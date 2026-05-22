from __future__ import annotations

import random
from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """Interface commune à tous les algorithmes de génération.

    L'instance reçoit la grille déjà initialisée (tous murs fermés) et
    les cellules bloquées (pattern "42"). Elle doit carver des passages
    en modifiant directement ``grid`` en place.

    Args:
        grid:    Grille 2D ``grid[y][x]``, déjà allouée avec tous les murs fermés.
        width:   Nombre de colonnes.
        height:  Nombre de lignes.
        entry:   ``(x, y)`` de l'entrée.
        exit_:   ``(x, y)`` de la sortie.
        blocked: Cellules à ne jamais modifier (pattern "42").
        perfect: Si ``True``, générer un labyrinthe parfait (arbre couvrant).
        rng:     Instance ``random.Random`` pré-seedée.
    """

    def __init__(
        self,
        grid: list[list[int]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        blocked: set[tuple[int, int]],
        perfect: bool,
        rng: random.Random,
    ) -> None:
        """Stocke les paramètres partagés."""
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.blocked = blocked
        self.perfect = perfect
        self.rng = rng

    @abstractmethod
    def run(self) -> None:
        """Lance l'algorithme et modifie ``self.grid`` en place."""
        ...
