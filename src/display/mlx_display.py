from __future__ import annotations
from typing import Optional
from mlx import Mlx
from pynput import keyboard
from mazegen.maze import Maze, MazeState
from mazegen.algo.base import BaseGenerator
from mazegen.algo.a_star import A_Star
from src.display.renderer import (MlxRenderer,
                                  WALL_PALETTES,
                                  WALL_SIZE,
                                  COLOR_42)
from src.display.input_handler import MlxInputHandler

WIN_W: int = 1900
WIN_H: int = 1000

X_EVENT_CLOSE: int = 33


class MlxDisplay(MlxRenderer, MlxInputHandler):
    """Main application class handling maze rendering, input, and lifecycle."""

    def __init__(
        self,
        maze: Maze,
        algo_class: type[BaseGenerator],
        title: str = "A-Maze-ing",
    ) -> None:
        """Initialize display, maze, and rendering context.

        Args:
            maze (Maze): Maze instance to display.
            algo_class (type[BaseGenerator]): Generation algorithm.
            title (str): Window title.
        """
        self._maze = maze
        self._algo_class = algo_class
        self._title = title
        self._running: bool = False

        self._show_path: bool = False
        self._solved: bool = False
        self._color_idx: int = 0
        self._wall_color: int = WALL_PALETTES[0]
        self._42_color: int = COLOR_42[0]

        cell_w = (WIN_W - WALL_SIZE) // maze.width
        cell_h = (WIN_H - WALL_SIZE) // maze.height
        self._cell_size: int = max(4, min(cell_w, cell_h))

        self._win_w: int = maze.width * self._cell_size + WALL_SIZE
        self._win_h: int = maze.height * self._cell_size + WALL_SIZE

        self._mlx: Optional[Mlx] = None
        self._mlx_ptr = None
        self._win_ptr = None
        self._img_ptr = None
        self._img_data: Optional[bytearray] = None
        self._img_sl: int = 0

        self._pending_keys: set[object] = set()
        self._listener: Optional[keyboard.Listener] = None

    def run(self) -> None:
        """Start rendering loop and generate maze."""
        self._setup()
        self._running = True
        self._maze.generate(self._algo_class)

        if self._mlx is None:
            raise RuntimeError("MLX not initalized")

        self._mlx.mlx_loop_hook(
            self._mlx_ptr,
            self._on_frame,
            self
        )

        self._mlx.mlx_hook(
            self._win_ptr,
            X_EVENT_CLOSE,
            0,
            self._on_close,
            self
        )

        try:
            self._mlx.mlx_loop(self._mlx_ptr)
        except KeyboardInterrupt:
            pass
        finally:
            self._running = False
            self._cleanup()

    def _on_frame(self, app: MlxDisplay) -> None:
        """Main frame update loop."""
        if not app._running:
            return
        try:
            app._process_keys()
            if app._maze.state == MazeState.GENERATING:
                for _ in range(10):
                    if not app._maze.tick():
                        break
            if app._maze.state == MazeState.GENERATED and not app._solved:
                try:
                    app._maze.solve_animated(A_Star)
                    app._solved = True
                except ValueError:
                    app._solved = True
            if app._solved and app._show_path:
                app._maze.tick_solve()
            app._draw()
        except KeyboardInterrupt:
            app._running = False
            if app._mlx is not None:
                app._mlx.mlx_loop_exit(app._mlx_ptr)
        except Exception:
            pass

    def _on_close(self, app: MlxDisplay) -> None:
        """Handle window close event."""
        mlx = app._mlx
        ptr = app._mlx_ptr

        if mlx is None:
            raise RuntimeError("MLX not initialized")

        mlx.mlx_loop_exit(ptr)

    def _setup(self) -> None:
        """Initialize MLX context, window, image buffer, and input listener."""
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

        self._listener = keyboard.Listener(on_press=self._on_key)
        self._listener.start()

    def _cleanup(self) -> None:
        """Release MLX resources and stop input listener."""
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
