from __future__ import annotations
from mazegen.maze import MazeState

WALL_SIZE: int = 2
NORTH: int = 0x1
EAST:  int = 0x2
SOUTH: int = 0x4
WEST:  int = 0x8
COLOR_BACKGROUND: int = 0xFF1A1A2E
COLOR_WALL: int       = 0xFFE0E0E0
COLOR_ENTRY: int      = 0xFF00FF88
COLOR_EXIT: int       = 0xFFFF4444
COLOR_42: int         = 0xFF444466
COLOR_PATH_START: int = 0xFF00BFFF
COLOR_PATH_END: int   = 0xFFFF6B6B
WALL_PALETTES: list[int] = [
    0xFFE0E0E0,
    0xFFFFD700,
    0xFF00FF88,
    0xFFFF6B6B,
    0xFF9B59B6,
]


class MlxRenderer:
    def _draw(self) -> None:
        if self._img_data is None: # type: ignore[attr-defined]
            return
        self._fill_background()
        self._draw_cells()
        if self._show_path and self._maze.state == MazeState.GENERATED: # type: ignore[attr-defined]
            self._draw_path()
        self._mlx.mlx_put_image_to_window(  # type: ignore[attr-defined]
            self._mlx_ptr,  # type: ignore[attr-defined]
            self._win_ptr,  # type: ignore[attr-defined]
            self._img_ptr,  # type: ignore[attr-defined]
            0, 0
        )


    def _fill_background(self) -> None:
        color_bytes = COLOR_BACKGROUND.to_bytes(4, 'little') * self._win_w # type: ignore[attr-defined]
        for row in range(self._win_h):  # type: ignore[attr-defined]
            offset = row * self._img_sl  # type: ignore[attr-defined]
            self._img_data[offset:offset + self._win_w * 4] = color_bytes  # type: ignore[attr-defined]


    def _draw_cells(self) -> None:
        grid = self._maze.grid  # type: ignore[attr-defined]
        forty_two = self._maze.forty_two_cells  # type: ignore[attr-defined]
        for y in range(self._maze.height):  # type: ignore[attr-defined]
            for x in range(self._maze.width):  # type: ignore[attr-defined]
                self._draw_cell(x, y, grid[y][x], (x, y) in forty_two)


    def _draw_cell(
        self,
        cx: int,
        cy: int,
        cell_val: int,
        is_42: bool,
    ) -> None:
        px = cx * self._cell_size  # type: ignore[attr-defined]
        py = cy * self._cell_size  # type: ignore[attr-defined]
        entry = self._maze.entry  # type: ignore[attr-defined]
        exit_ = self._maze.exit   # type: ignore[attr-defined]
        if is_42:
            cell_color = COLOR_42
        elif (cx, cy) == entry:
            cell_color = COLOR_ENTRY
        elif (cx, cy) == exit_:
            cell_color = COLOR_EXIT
        else:
            cell_color = COLOR_BACKGROUND
        self._fill_rect(
            px + WALL_SIZE,
            py + WALL_SIZE,
            self._cell_size - WALL_SIZE,  # type: ignore[attr-defined]
            self._cell_size - WALL_SIZE,  # type: ignore[attr-defined]
            cell_color,
        )
        wall = self._wall_color if not is_42 else COLOR_42  # type: ignore[attr-defined]
        if cell_val & NORTH:
            self._fill_rect(px, py, self._cell_size, WALL_SIZE, wall)  # type: ignore[attr-defined]
        if cell_val & WEST:
            self._fill_rect(px, py, WALL_SIZE, self._cell_size, wall)  # type: ignore[attr-defined]
        if cell_val & SOUTH:
            self._fill_rect(px, py + self._cell_size - WALL_SIZE, self._cell_size, WALL_SIZE, wall)  # type: ignore[attr-defined]
        if cell_val & EAST:
            self._fill_rect(px + self._cell_size - WALL_SIZE, py, WALL_SIZE, self._cell_size, wall)  # type: ignore[attr-defined]


    def _draw_path(self) -> None:
        try:
            path = self._maze.solution  # type: ignore[attr-defined]
        except RuntimeError:
            return
        direction_to_delta = {
            'N': (0, -1),
            'S': (0,  1),
            'E': (1,  0),
            'W': (-1, 0),
        }
        grid = self._maze.grid  # type: ignore[attr-defined]
        x, y = self._maze.entry  # type: ignore[attr-defined]
        positions = [(x, y)]
        for step in path:
            dx, dy = direction_to_delta[step]
            x += dx
            y += dy
            positions.append((x, y))
        inner = positions[1:]
        total = max(len(inner) - 1, 1)
        for i, (cx, cy) in enumerate(inner):
            t = i / total
            color = self._lerp_color(COLOR_PATH_START, COLOR_PATH_END, t)
            cell_val = grid[cy][cx]
            off_n = WALL_SIZE if (cell_val & NORTH) else 0
            off_s = WALL_SIZE if (cell_val & SOUTH) else 0
            off_w = WALL_SIZE if (cell_val & WEST)  else 0
            off_e = WALL_SIZE if (cell_val & EAST)  else 0
            self._fill_rect(
                cx * self._cell_size + off_w,  # type: ignore[attr-defined]
                cy * self._cell_size + off_n,  # type: ignore[attr-defined]
                self._cell_size - off_w - off_e,  # type: ignore[attr-defined]
                self._cell_size - off_n - off_s,  # type: ignore[attr-defined]
                color,
            )


    def _lerp_color(self, c1: int, c2: int, t: float) -> int:
        r1, g1, b1 = (c1 >> 16) & 0xFF, (c1 >> 8) & 0xFF, c1 & 0xFF
        r2, g2, b2 = (c2 >> 16) & 0xFF, (c2 >> 8) & 0xFF, c2 & 0xFF
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return 0xFF000000 | (r << 16) | (g << 8) | b


    def _fill_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        if w <= 0 or h <= 0:
            return
        x1 = max(x, 0)
        y1 = max(y, 0)
        x2 = min(x + w, self._win_w)  # type: ignore[attr-defined]
        y2 = min(y + h, self._win_h)  # type: ignore[attr-defined]
        if x1 >= x2 or y1 >= y2:
            return
        color_bytes = color.to_bytes(4, 'little') * (x2 - x1)
        row_len = len(color_bytes)
        for row in range(y1, y2):
            offset = row * self._img_sl + x1 * 4  # type: ignore[attr-defined]
            self._img_data[offset:offset + row_len] = color_bytes  # type: ignore[attr-defined]


    def _put_pixel(self, x: int, y: int, color: int) -> None:
        if 0 <= x < self._win_w and 0 <= y < self._win_h:  # type: ignore[attr-defined]
            offset = y * self._img_sl + x * 4  # type: ignore[attr-defined]
            self._img_data[offset:offset + 4] = color.to_bytes(4, 'little')  # type: ignore[attr-defined]
