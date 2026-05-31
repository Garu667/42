from __future__ import annotations
from pynput.keyboard import Key, KeyCode
from mazegen.maze import MazeState


class MlxInputHandler:
    def _on_key(self, key: object) -> None:
        self._pending_keys.add(key)  # type: ignore[attr-defined]

    def _process_keys(self) -> None:
        keys = self._pending_keys.copy()  # type: ignore[attr-defined]
        self._pending_keys.clear()  # type: ignore[attr-defined]
        seen: set[object] = set()
        for key in keys:
            if key in seen:
                continue
            seen.add(key)
            if key == Key.esc or key == KeyCode.from_char('q'):
                self._mlx.mlx_loop_exit(self._mlx_ptr)  # type: ignore[attr-defined]
            elif key == KeyCode.from_char('s'):
                self._skip_animation()
            elif key == KeyCode.from_char('r'):
                self._regenerate()
            elif key == KeyCode.from_char('p'):
                self._show_path = not self._show_path  # type: ignore[attr-defined]
            elif key == KeyCode.from_char('c'):
                from src.display.renderer import WALL_PALETTES
                self._wall_color_idx = (  # type: ignore[attr-defined]
                    (self._wall_color_idx + 1) % len(WALL_PALETTES)  # type: ignore[attr-defined]
                )
                self._wall_color = WALL_PALETTES[self._wall_color_idx]  # type: ignore[attr-defined]

    def _regenerate(self) -> None:
        self._show_path = False  # type: ignore[attr-defined]
        self._solved = False  # type: ignore[attr-defined]
        try:
            self._maze.reset()  # type: ignore[attr-defined]
            if self._maze.state == MazeState.INITIALIZED:  # type: ignore[attr-defined]
                self._maze.generate(self._algo_class)  # type: ignore[attr-defined]
        except RuntimeError as e:
            print(f"[Warning] Regeneration skipped: {e}")

    def _skip_animation(self) -> None:
        if self._maze.state == MazeState.GENERATING:  # type: ignore[attr-defined]
            self._maze.run_all()  # type: ignore[attr-defined]
        elif self._maze.is_solving:
            while self._maze.tick_solve():          # type: ignore[attr-defined]
                pass
