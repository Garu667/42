from __future__ import annotations
from typing import Optional
from mlx import Mlx
from mazegen.maze import Maze, MazeState
from mazegen.algo.base import BaseGenerator
from mazegen.algo.a_star import A_Star
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

WIN_W: int = 1900
WIN_H: int = 1000

WALL_SIZE: int = 2        # épaisseur des murs en pixels

NORTH: int = 0x1
EAST:  int = 0x2
SOUTH: int = 0x4
WEST:  int = 0x8

COLOR_BACKGROUND: int = 0xFF1A1A2E   # fond sombre
COLOR_WALL: int       = 0xFFE0E0E0   # murs blanc cassé
COLOR_ENTRY: int      = 0xFF00FF88   # entrée verte
COLOR_EXIT: int       = 0xFFFF4444   # sortie rouge
COLOR_PATH: int       = 0xFF00BFFF   # chemin solution bleu
COLOR_42: int         = 0xFF444466   # cellules du pattern "42"

# Palettes de couleurs de murs — cycle avec 'C'
WALL_PALETTES: list[int] = [
    0xFFE0E0E0,   # blanc cassé (défaut)
    0xFFFFD700,   # or
    0xFF00FF88,   # vert
    0xFFFF6B6B,   # rouge corail
    0xFF9B59B6,   # violet
]
# Événement X11 — fermeture fenêtre
X_EVENT_CLOSE: int = 33

class MlxDisplay:
    """Gère l'affichage MLX du labyrinthe.
    Args:
        maze:       Instance de ``Maze`` déjà initialisée.
        algo_class: Classe de génération héritant de ``BaseGenerator``.
        title:      Titre de la fenêtre.
    """

    def __init__(
        self,
        maze: Maze,
        algo_class: type[BaseGenerator],
        title: str = "A-Maze-ing",
    ) -> None:
        self._maze = maze
        self._algo_class = algo_class
        self._title = title
        # État d'affichage
        self._show_path: bool = False
        self._wall_color_idx: int = 0
        self._wall_color: int = WALL_PALETTES[0]
        # Calculer la taille de la fenêtre
        cell_w = (WIN_W - WALL_SIZE) // maze.width
        cell_h = (WIN_H - WALL_SIZE) // maze.height
        self._cell_size = max(4, min(cell_w, cell_h))
        self._win_w: int = maze.width  * self._cell_size + WALL_SIZE
        self._win_h: int = maze.height * self._cell_size + WALL_SIZE
        # Pointeurs MLX — initialisés dans _setup()
        self._mlx: Optional[Mlx] = None
        self._mlx_ptr = None
        self._win_ptr = None
        self._img_ptr = None
        self._img_data = None
        self._img_sl: int = 0   # size_line — bytes par ligne
        # Buffer thread-safe pour pynput
        self._pending_keys: set = set()
        self._listener: Optional[keyboard.Listener] = None

    def run(self) -> None:
        self._setup()
        self._maze.generate(self._algo_class)

        self._mlx.mlx_loop_hook(self._mlx_ptr, self._on_frame, self)
        self._mlx.mlx_hook(
            self._win_ptr, X_EVENT_CLOSE, 0, self._on_close, self
        )

        self._mlx.mlx_loop(self._mlx_ptr)
        self._cleanup()


    def _on_frame(self, app: MlxDisplay) -> None:
        """ Step one frame on the generation and draw """
        app._process_keys() # Check the key buffer
        if app._maze.state == MazeState.GENERATING:
            for _ in range(10):
                if not app._maze.tick():
                    break

        # Résoudre automatiquement une fois la génération terminée
        if app._maze.state == MazeState.GENERATED and not app._maze._solution:
            try:
                app._maze.solve(A_Star)
            except ValueError:
                pass  # pas de chemin — rare mais on ne crash pas
        app._draw()

   
    def _on_key(self, key) -> None:
        """Callback pynput — thread séparé, on écrit juste dans le buffer."""
        self._pending_keys.add(key)

    def _process_keys(self) -> None:
        """Appelé depuis _on_frame — thread MLX, on consomme le buffer."""
        keys = self._pending_keys.copy()
        self._pending_keys.clear()

        for key in keys:
            if key == Key.esc or key == KeyCode.from_char('q'):
                self._mlx.mlx_loop_exit(self._mlx_ptr)
            elif key == KeyCode.from_char('s'):
                self._skip_animation()
            elif key == KeyCode.from_char('r'):
                self._regenerate()
            elif key == KeyCode.from_char('p'):
                self._show_path = not self._show_path
            elif key == KeyCode.from_char('c'):
                self._wall_color_idx = (
                    (self._wall_color_idx + 1) % len(WALL_PALETTES)
                )
                self._wall_color = WALL_PALETTES[self._wall_color_idx]

    def _skip_animation(self) -> None:
        """Skip l'animation et génère le maze d'un coup."""
        if self._maze.state == MazeState.GENERATING:
            self._maze.run_all()


    def _on_close(self, app: MlxDisplay) -> None:
        """Appelé quand l'utilisateur clique sur la croix de la fenêtre."""
        app._mlx.mlx_loop_exit(app._mlx_ptr)   # type: ignore[union-attr]

    def _regenerate(self) -> None:
        """Réinitialise et relance la génération du labyrinthe."""
        self._show_path = False
        self._maze.reset()
        if self._maze.state == MazeState.INITIALIZED:
            self._maze.generate(self._algo_class)

    def _draw(self) -> None:
        """Redessine l'image complète et l'affiche dans la fenêtre."""
        if self._img_data is None:
            return

        self._fill_background()
        self._draw_cells()

        if self._show_path and self._maze.state == MazeState.GENERATED:
            self._draw_path()

        self._mlx.mlx_put_image_to_window(       # type: ignore[union-attr]
            self._mlx_ptr, self._win_ptr, self._img_ptr, 0, 0
        )

    def _fill_background(self) -> None:
        """Remplit toute l'image avec la couleur de fond."""
        color_bytes = COLOR_BACKGROUND.to_bytes(4, 'little') * self._win_w
        for row in range(self._win_h):
            offset = row * self._img_sl
            self._img_data[offset:offset + self._win_w * 4] = color_bytes  # type: ignore[index]

    def _draw_cells(self) -> None:
        """Dessine chaque cellule du labyrinthe avec ses murs."""
        grid = self._maze.grid
        forty_two = self._maze.forty_two_cells

        for y in range(self._maze.height):
            for x in range(self._maze.width):
                self._draw_cell(x, y, grid[y][x], (x, y) in forty_two)

    def _draw_cell(
        self,
        cx: int,
        cy: int,
        cell_val: int,
        is_42: bool,
    ) -> None:
        """Dessine une cellule et ses murs fermés.

        Args:
            cx:       Colonne de la cellule.
            cy:       Ligne de la cellule.
            cell_val: Valeur hex encodant les murs fermés.
            is_42:    Si True, colorie la cellule en couleur "42".
        """

        px = cx * self._cell_size   # pixel top-left de la cellule
        py = cy * self._cell_size

        entry = self._maze.entry
        exit_ = self._maze.exit

        # Couleur de fond de la cellule
        if is_42:
            cell_color = COLOR_42
        elif (cx, cy) == entry:
            cell_color = COLOR_ENTRY
        elif (cx, cy) == exit_:
            cell_color = COLOR_EXIT
        else:
            cell_color = COLOR_BACKGROUND

        # Remplir l'intérieur de la cellule (hors murs)
        self._fill_rect(
            px + WALL_SIZE,
            py + WALL_SIZE,
            self._cell_size - WALL_SIZE,
            self._cell_size - WALL_SIZE,
            cell_color,
        )

        wall = self._wall_color if not is_42 else COLOR_42

        # Mur Nord
        if cell_val & NORTH:
            self._fill_rect(px, py, self._cell_size, WALL_SIZE, wall)
        # Mur Ouest
        if cell_val & WEST:
            self._fill_rect(px, py, WALL_SIZE, self._cell_size, wall)
        # Mur Sud (bord bas de la cellule)
        if cell_val & SOUTH:
            self._fill_rect(px, py + self._cell_size - WALL_SIZE, self._cell_size, WALL_SIZE, wall)
        # Mur Est (bord droit de la cellule)
        if cell_val & EAST:
            self._fill_rect(px + self._cell_size - WALL_SIZE, py, WALL_SIZE, self._cell_size, wall)

    def _lerp_color(self, c1: int, c2: int, t: float) -> int:
        """Interpolation linéaire entre deux couleurs 0xAARRGGBB.

        Args:
            c1: Couleur de départ.
            c2: Couleur d'arrivée.
            t:  Facteur 0.0 → 1.0.

        Returns:
            Couleur interpolée.
        """
        r1, g1, b1 = (c1 >> 16) & 0xFF, (c1 >> 8) & 0xFF, c1 & 0xFF
        r2, g2, b2 = (c2 >> 16) & 0xFF, (c2 >> 8) & 0xFF, c2 & 0xFF

        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)

        return 0xFF000000 | (r << 16) | (g << 8) | b


    def _draw_path(self) -> None:
        """Dessine le chemin solution par-dessus les cellules."""
        try:
            path = self._maze.solution
        except RuntimeError:
            return

        direction_to_delta = {
            'N': (0, -1),
            'S': (0,  1),
            'E': (1,  0),
            'W': (-1, 0),
        }

        direction_to_wall = {
            'N': NORTH,
            'S': SOUTH,
            'E': EAST,
            'W': WEST,
        }

        grid = self._maze.grid
        x, y = self._maze.entry
        entry = self._maze.entry
        exit_ = self._maze.exit

        positions = [(x, y)]
        for step in path:
            dx, dy = direction_to_delta[step]
            x += dx
            y += dy
            positions.append((x, y))

        inner = positions[1:]
        total = max(len(inner) -1, 1)
        for i, (cx, cy) in enumerate(inner):
            t = i / total
            color = self._lerp_color(0xFF00BFFF, 0xFFFF6B6B, t)

            cell_val = grid[cy][cx]
            off_n = WALL_SIZE if (cell_val & NORTH) else 0
            off_s = WALL_SIZE if (cell_val & SOUTH) else 0
            off_w = WALL_SIZE if (cell_val & WEST)  else 0
            off_e = WALL_SIZE if (cell_val & EAST)  else 0

            self._fill_rect(
                cx * self._cell_size + off_w,
                cy * self._cell_size + off_n,
                self._cell_size - off_w - off_e,
                self._cell_size - off_n - off_s,
                color,
            )

    def _fill_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: int,
    ) -> None:
        """Remplit un rectangle de pixels dans l'image en mémoire.

        Args:
            x:     Colonne du pixel top-left.
            y:     Ligne du pixel top-left.
            w:     Largeur en pixels.
            h:     Hauteur en pixels.
            color: Couleur 0xAARRGGBB.
        """
        if w <= 0 or h <= 0:
            return

        x1 = max(x, 0)
        y1 = max(y, 0)
        x2 = min (x + w, self._win_w)
        y2 = min (y + h, self._win_h)

        if x1 >= x2 or y1 >= y2:
            return

        # A precalculated line of pixels reused every row
        color_bytes = color.to_bytes(4, 'little') * (x2 - x1)
        row_len = len(color_bytes)
        for row in range(y1, y2):
            offset = row * self._img_sl + x1 * 4
            self._img_data[offset:offset + row_len] = color_bytes


    def _put_pixel(self, x: int, y: int, color: int) -> None:
        """Écrit un pixel à ``(x, y)`` dans l'image en mémoire.

        Args:
            x:     Colonne.
            y:     Ligne.
            color: Couleur 0xAARRGGBB.
        """
        if 0 <= x < self._win_w and 0 <= y < self._win_h:
            offset = y * self._img_sl + x * 4
            self._img_data[offset:offset + 4] = color.to_bytes(4, 'little')  # type: ignore[index]

    def _setup(self) -> None:
        """Initialize MLX, create windows and renderer.

        Raises:
            RuntimeError: If mlx can't initialize.
        """
        try:
            self._mlx = Mlx()
        except Exception as e:
            raise RuntimeError(f"Impossible d'initialiser MLX : {e}") from e
        self._mlx_ptr = self._mlx.mlx_init()
        if not self._mlx_ptr:
            raise RuntimeError("mlx_init() a échoué.")
        self._win_ptr = self._mlx.mlx_new_window(
            self._mlx_ptr, self._win_w, self._win_h, self._title
        )
        if not self._win_ptr:
            raise RuntimeError("mlx_new_window() a échoué.")
        self._img_ptr = self._mlx.mlx_new_image(
            self._mlx_ptr, self._win_w, self._win_h
        )
        if not self._img_ptr:
            raise RuntimeError("mlx_new_image() a échoué.")
        self._img_data, _bpp, self._img_sl, _fmt = (
            self._mlx.mlx_get_data_addr(self._img_ptr)
        )
        # Initlize the key buffer
        self._listener = keyboard.Listener(on_press=self._on_key)
        self._listener.start()

    def _cleanup(self) -> None:
        """Libère toutes les ressources MLX."""
        if self._mlx is None:
            return
        if self._listener:
            self._listener.stop()
        if self._img_ptr:
            self._mlx.mlx_destroy_image(self._mlx_ptr, self._img_ptr)
        if self._win_ptr:
            self._mlx.mlx_destroy_window(self._mlx_ptr, self._win_ptr)
        if self._mlx_ptr:
            self._mlx.mlx_release(self._mlx_ptr)
