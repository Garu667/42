from mazegen.Maze import Maze


class PrimGenerator(BaseGenerator):

    def _get_unvisited_neighbors(
        self,
        cell: Cell,
        visited_cells: Set[Cell],
    ) -> List[Tuple[Cell, EDirection]]:
        neighbors: List[Tuple[Cell, EDirection]] = []
        maze = self.get_maze()

        if (
            cell.position.y > 0
            and not maze.map[cell.position.y - 1][cell.position.x].locked
            and maze.map[cell.position.y - 1][cell.position.x]
            not in visited_cells
        ):
            neighbors.append(
                (maze.map[cell.position.y - 1][cell.position.x],
                 EDirection.NORTH)
            )

        if (
            cell.position.x < maze.width - 1
            and not maze.map[cell.position.y][cell.position.x + 1].locked
            and maze.map[cell.position.y][cell.position.x + 1]
            not in visited_cells
        ):
            neighbors.append(
                (maze.map[cell.position.y][cell.position.x + 1],
                 EDirection.EAST)
            )

        if (
            cell.position.y < maze.height - 1
            and not maze.map[cell.position.y + 1][cell.position.x].locked
            and maze.map[cell.position.y + 1][cell.position.x]
            not in visited_cells
        ):
            neighbors.append(
                (maze.map[cell.position.y + 1][cell.position.x],
                 EDirection.SOUTH)
            )

        if (
            cell.position.x > 0
            and not maze.map[cell.position.y][cell.position.x - 1].locked
            and maze.map[cell.position.y][cell.position.x - 1]
            not in visited_cells
        ):
            neighbors.append(
                (maze.map[cell.position.y][cell.position.x - 1],
                 EDirection.WEST)
            )

        return neighbors

    def _get_visited_neighbors(
        self,
        cell: Cell,
        visited_cells: Set[Cell],
    ) -> List[Tuple[Cell, EDirection]]:
        neighbors: List[Tuple[Cell, EDirection]] = []
        maze = self.get_maze()

        if (
            cell.position.y > 0
            and not maze.map[cell.position.y - 1][cell.position.x].locked
            and maze.map[cell.position.y - 1][cell.position.x] in visited_cells
        ):
            neighbors.append(
                (maze.map[cell.position.y - 1][cell.position.x],
                 EDirection.NORTH)
            )

        if (
            cell.position.x < maze.width - 1
            and not maze.map[cell.position.y][cell.position.x + 1].locked
            and maze.map[cell.position.y][cell.position.x + 1] in visited_cells
        ):
            neighbors.append(
                (maze.map[cell.position.y][cell.position.x + 1],
                 EDirection.EAST)
            )

        if (
            cell.position.y < maze.height - 1
            and not maze.map[cell.position.y + 1][cell.position.x].locked
            and maze.map[cell.position.y + 1][cell.position.x] in visited_cells
        ):
            neighbors.append(
                (maze.map[cell.position.y + 1][cell.position.x],
                 EDirection.SOUTH)
            )

        if (
            cell.position.x > 0
            and not maze.map[cell.position.y][cell.position.x - 1].locked
            and maze.map[cell.position.y][cell.position.x - 1] in visited_cells
        ):
            neighbors.append(
                (maze.map[cell.position.y][cell.position.x - 1],
                 EDirection.WEST)
            )

        return neighbors

    def _carve_between(self, cell: Cell, neighbor: Cell,
                       direction: EDirection) -> None:
        opposite = {
            EDirection.NORTH: EDirection.SOUTH,
            EDirection.EAST: EDirection.WEST,
            EDirection.SOUTH: EDirection.NORTH,
            EDirection.WEST: EDirection.EAST,
        }

        self.get_maze().carve_cell(cell, direction)
        cell.carve(direction)
        neighbor.carve(opposite[direction])

    def _carve_around(self, cell: Cell) -> None:
        directions = [
            EDirection.NORTH,
            EDirection.EAST,
            EDirection.SOUTH,
            EDirection.WEST,
        ]

        direction_neighbor = {
            EDirection.NORTH: (0, -1),
            EDirection.EAST: (1, 0),
            EDirection.SOUTH: (0, 1),
            EDirection.WEST: (-1, 0),
        }

        opposite_direction = {
            EDirection.NORTH: EDirection.SOUTH,
            EDirection.EAST: EDirection.WEST,
            EDirection.SOUTH: EDirection.NORTH,
            EDirection.WEST: EDirection.EAST,
        }

        for dir in directions:
            is_open = not bool(cell.walls & dir.value)
            x, y = cell.position.x, cell.position.y
            move_x, move_y = direction_neighbor[dir]
            n_x, n_y = x + move_x, y + move_y

            if n_x not in range(self.get_maze().width):
                continue
            if n_y not in range(self.get_maze().height):
                continue
            if self.get_maze().map[n_y][n_x].locked:
                continue

            n_cell = self.get_maze().map[n_y][n_x]
            opposite = opposite_direction[dir]

            if is_open:
                n_cell.walls &= ~opposite.value
            else:
                n_cell.walls |= opposite.value

    def _would_create_open_3x3(
        self,
        cell_x: int,
        cell_y: int,
        direction: EDirection,
    ) -> bool:
        maze = self.get_maze()
        grid = maze.map

        if direction == EDirection.EAST:
            edge_cols = (cell_x, cell_x + 1)
            edge_row = cell_y
            is_vertical = True
        elif direction == EDirection.WEST:
            edge_cols = (cell_x - 1, cell_x)
            edge_row = cell_y
            is_vertical = True
        elif direction == EDirection.SOUTH:
            edge_rows = (cell_y, cell_y + 1)
            edge_col = cell_x
            is_vertical = False
        else:  # NORTH
            edge_rows = (cell_y - 1, cell_y)
            edge_col = cell_x
            is_vertical = False

        candidates: List[Tuple[int, int]] = []
        if is_vertical:
            for cx in range(edge_cols[0] - 1, edge_cols[0] + 1):
                for cy in range(edge_row - 2, edge_row + 1):
                    candidates.append((cx, cy))
        else:
            for cy in range(edge_rows[0] - 1, edge_rows[0] + 1):
                for cx in range(edge_col - 2, edge_col + 1):
                    candidates.append((cx, cy))

        for cx, cy in candidates:
            if (
                cx < 0
                or cx + 2 >= maze.width
                or cy < 0
                or cy + 2 >= maze.height
            ):
                continue

            all_open = True

            for r in range(cy, cy + 3):
                for c in range(cx, cx + 2):
                    is_target = (
                        c == cell_x
                        and r == cell_y
                        and direction == EDirection.EAST
                    ) or (
                        c + 1 == cell_x
                        and r == cell_y
                        and direction == EDirection.WEST
                    )
                    if not is_target and (
                        grid[r][c].walls & EDirection.EAST.value
                    ):
                        all_open = False
                        break
                if not all_open:
                    break

            if not all_open:
                continue

            for r in range(cy, cy + 2):
                for c in range(cx, cx + 3):
                    is_target = (
                        c == cell_x
                        and r == cell_y
                        and direction == EDirection.SOUTH
                    ) or (
                        c == cell_x
                        and r + 1 == cell_y
                        and direction == EDirection.NORTH
                    )
                    if not is_target and (
                        grid[r][c].walls & EDirection.SOUTH.value
                    ):
                        all_open = False
                        break
                if not all_open:
                    break

            if all_open:
                return True

        return False

    def _make_imperfect(self) -> None:
        directions = [
            EDirection.NORTH,
            EDirection.EAST,
            EDirection.SOUTH,
            EDirection.WEST,
        ]

        direction_neighbor = {
            EDirection.NORTH: (0, -1),
            EDirection.EAST: (1, 0),
            EDirection.SOUTH: (0, 1),
            EDirection.WEST: (-1, 0),
        }

        maze = self.get_maze()

        def count_walls(cell: Cell) -> int:
            c = 0
            for d in directions:
                if cell.walls & d.value:
                    c += 1
            return c

        temp_available_cells: List[Cell] = [
            cell for row in maze.map for cell in row if not cell.locked
        ]

        self._get_rng().shuffle(temp_available_cells)

        available_cells: SortedKeyList[Cell, int] = SortedKeyList(
            temp_available_cells, key=lambda x: count_walls(x)
        )

        wall_number = sum(
            [
                1
                for cell in available_cells
                for d in directions
                if cell.walls & d.value
            ]
        )

        wall_number -= (maze.height + maze.width) * 2
        wall_number //= 2
        walls_to_break = int(wall_number * 0.2)
        walls_to_break = max(1, walls_to_break)

        break_count = 0
        while break_count < walls_to_break and available_cells:
            cell = available_cells.pop()
            x, y = cell.position.x, cell.position.y
            self._get_rng().shuffle(directions)

            for dir in directions:
                broke = False

                if not (cell.walls & dir.value):
                    continue

                move_x, move_y = direction_neighbor[dir]
                n_x, n_y = x + move_x, y + move_y

                if n_x not in range(maze.width):
                    continue
                if n_y not in range(maze.height):
                    continue
                if maze.map[n_y][n_x].locked:
                    continue

                if self._would_create_open_3x3(x, y, dir):
                    continue

                cell.walls &= ~dir.value
                self._carve_around(cell)
                break_count += 1
                broke = True
                break

            if broke:
                available_cells.add(cell)

    def generate(self, seed: Optional[str] = None) -> List[Cell]:
        if seed is not None:
            self._get_rng().seed(seed)

        if self.get_maze().status == Maze.Status.GENERATED:
            self.reset_maze()

        self.get_maze().status = Maze.Status.GENERATING

        start_cell = self._get_rng().choice(
            [
                cell
                for row in self.get_maze().map
                for cell in row
                if not cell.locked
            ]
        )

        visited_cells: Set[Cell] = {start_cell}
        updated_cells: List[Cell] = [start_cell]

        # Frontier: unvisited neighbours of the visited region.
        # Duplicates are allowed and skipped when popped if already visited.
        frontiers: List[Cell] = []

        for neighbor, _ in self._get_unvisited_neighbors(start_cell,
                                                         visited_cells):
            frontiers.append(neighbor)

        rng = self._get_rng()

        while frontiers:
            # Pick a random frontier cell (swap-with-last for O(1) removal)
            idx = rng.randint(0, len(frontiers) - 1)
            frontier_cell = frontiers[idx]
            frontiers[idx] = frontiers[-1]
            frontiers.pop()

            # Skip if already visited
            # (can happen due to duplicates in the list)
            if frontier_cell in visited_cells:
                continue

            # Connect frontier_cell to a random visited neighbour
            visited_neighbors = self._get_visited_neighbors(frontier_cell,
                                                            visited_cells)
            if not visited_neighbors:
                continue

            neighbor, direction = rng.choice(visited_neighbors)
            self._carve_between(frontier_cell, neighbor, direction)

            visited_cells.add(frontier_cell)
            updated_cells.append(frontier_cell)

            # Extend the frontier with new unvisited neighbours
            for frontier, _ in self._get_unvisited_neighbors(frontier_cell,
                                                             visited_cells):
                frontiers.append(frontier)

        self.get_maze().status = Maze.Status.GENERATED

        if not self._get_perfect():
            self._make_imperfect()

        return updated_cells
