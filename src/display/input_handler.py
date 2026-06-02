from __future__ import annotations
from pynput.keyboard import Key, KeyCode
from mazegen.maze import MazeState


class MlxInputHandler:
    def _on_key(self, key: object) -> None:
        self._pending_keys.add(key)

    def _process_keys(self) -> None:
        keys = self._pending_keys.copy()
        self._pending_keys.clear()
        seen: set[object] = set()
        for key in keys:
            if key in seen:
                continue
            seen.add(key)
            if key == Key.esc or key == KeyCode.from_char('q'):
                self._mlx.mlx_loop_exit(self._mlx_ptr)
            elif key == KeyCode.from_char('s'):
                self._skip_animation()
            elif key == KeyCode.from_char('r'):
                self._regenerate()
            elif key == KeyCode.from_char('p'):
                self._show_path = not self._show_path
            elif key == KeyCode.from_char('c'):
                from src.display.renderer import WALL_PALETTES
                self._wall_color_idx = (
                    (self._wall_color_idx + 1) % len(WALL_PALETTES)
                )
                self._wall_color = WALL_PALETTES[self._wall_color_idx]

    def _regenerate(self) -> None:
        self._show_path = False
        self._solved = False
        try:
            self._maze.reset()
            if self._maze.state == MazeState.INITIALIZED:
                self._maze.generate(self._algo_class)
        except RuntimeError as e:
            print(f"[Warning] Regeneration skipped: {e}")

    def _skip_animation(self) -> None:
        if self._maze.state == MazeState.GENERATING:
            self._maze.run_all()
        elif self._maze.is_solving:
            while self._maze.tick_solve():
                pass
