from __future__ import annotations
from typing import Any
from pynput.keyboard import Key, KeyCode
from mazegen.maze import MazeState, Maze
from mazegen.algo.base import BaseGenerator


class MlxInputHandler:
    """Handle keyboard input events for maze interaction."""
    _pending_keys: set[object]
    _show_path: bool
    _solved: bool
    _color_idx: int
    _wall_color: int
    _42_color: int
    _maze: Maze
    _algo_class: type[BaseGenerator]
    _mlx: Any
    _mlx_ptr: Any

    def _on_key(self, key: object) -> None:
        """Store pressed key for later processing."""
        self._pending_keys.add(key)

    def _process_keys(self) -> None:
        """Process queued keyboard inputs."""
        keys = self._pending_keys.copy()
        self._pending_keys.clear()
        seen: set[object] = set()

        for key in keys:
            if key in seen:
                continue
            seen.add(key)

            if key == Key.esc or key == KeyCode.from_char('q'):
                self._running = False
                self._mlx.mlx_loop_exit(self._mlx_ptr)
            elif key == KeyCode.from_char('s'):
                self._skip_animation()
            elif key == KeyCode.from_char('r'):
                self._regenerate()
            elif key == KeyCode.from_char('p'):
                self._show_path = not self._show_path
            elif key == KeyCode.from_char('c'):
                from src.display.renderer import WALL_PALETTES
                from src.display.renderer import COLOR_42
                self._color_idx = (self._color_idx + 1) % len(WALL_PALETTES)
                self._wall_color = WALL_PALETTES[self._color_idx]
                self._42_color = COLOR_42[self._color_idx]

    def _regenerate(self) -> None:
        """Reset and regenerate the maze."""
        self._show_path = False
        self._solved = False

        try:
            self._maze.reset()
            if self._maze.state == MazeState.INITIALIZED:
                self._maze.generate(self._algo_class)
        except RuntimeError as e:
            print(f"[Warning] Regeneration skipped: {e}")

    def _skip_animation(self) -> None:
        """Skip generation or solving animation."""
        if self._maze.state == MazeState.GENERATING:
            self._maze.run_all()
        elif self._maze.is_solving:
            while self._maze.tick_solve():
                pass
