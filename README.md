
# A-Maze-ing

*This project has been created as part of the 42 curriculum by hhamidi and ramaroud.*

A maze generator written in Python that creates perfect or imperfect mazes, displays them visually, and exports them in a hexadecimal format.

---

# Description

A-Maze-ing generates mazes from a configuration file. It uses **Prim's algorithm** to build the maze structure, supports both perfect mazes (single path between entry and exit) and imperfect ones (multiple paths), and finds the shortest path using **A***.

The maze is exported to a file using a hexadecimal wall encoding and displayed graphically using MLX.

The maze always contains a visible **"42" pattern** formed by fully closed cells, and no fully open 3×3 area can be created.

---

# Requirements

* Python 3.10+
* pip

---

# Installation

```bash
make install
```

---

# Run

```bash
make run
```

or

```bash
python3 a_maze_ing.py config.txt
```

---

# Debug

```bash
make debug
```

---

# Lint

```bash
make lint
```

or

```bash
make lint-strict
```

---

# Clean

```bash
make clean
```

---

# Configuration File

The configuration file uses one `KEY=VALUE` pair per line.

Lines beginning with `#` are ignored.

Example:

```txt
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Available Keys

| Key         | Type          | Required | Description             |
| ----------- | ------------- | -------- | ----------------------- |
| WIDTH       | int (3–100)   | ✅        | Maze width              |
| HEIGHT      | int (3–100)   | ✅        | Maze height             |
| ENTRY       | x,y           | ✅        | Entry coordinates       |
| EXIT        | x,y           | ✅        | Exit coordinates        |
| OUTPUT_FILE | .txt filename | ✅        | Output file name        |
| PERFECT     | True/False    | ✅        | Generate a perfect maze |
| SEED        | int           | ✅        | Random seed             |

---

# Controls

| Key     | Action                 |
| ------- | ---------------------- |
| S       | Skip current animation |
| R       | Regenerate maze        |
| P       | Show / hide solution   |
| C       | Change color palette   |
| Q / Esc | Quit                   |

---

# Output Format

Each cell is encoded as a hexadecimal digit.

Walls are represented by bit flags:

| Bit | Direction |
| --- | --------- |
| 0   | North     |
| 1   | East      |
| 2   | South     |
| 3   | West      |

A wall present = `1`

A wall removed = `0`

Examples:

```txt
F = 1111
```

All walls closed.

```txt
A = 1010
```

East and West walls closed.

The output file contains:

```txt
<maze grid>

entry_x,entry_y
exit_x,exit_y
solution_path
```

Example:

```txt
FFFF
F99F
FFFF

0,0
3,2
EESS
```

The solution path uses:

* N = North
* E = East
* S = South
* W = West

---

# Maze Generation

The maze is generated using a randomized version of **Prim's algorithm**.

## Algorithm

1. Choose a random starting cell.
2. Mark it as visited.
3. Add all unvisited neighbors to a frontier list.
4. Randomly select cells from the frontier.
5. Connect them to the maze.
6. Continue until every reachable cell has been visited.

## Why Prim?

* Produces natural-looking mazes.
* Guarantees connectivity.
* Generates perfect mazes.
* Easy to animate step by step.

---

# Imperfect Mazes

When:

```txt
PERFECT=False
```

additional walls are removed after the maze has been generated.

This creates loops and multiple possible paths while preserving the constraint that no fully open 3×3 area can exist.

The algorithm verifies this condition before breaking any additional wall.

---

# Pathfinding

The shortest path is found using **A*** with the Manhattan distance heuristic.

```text
h(n) = |x - goal_x| + |y - goal_y|
```

Nodes are explored according to:

```text
f(n) = g(n) + h(n)
```

where:

* `g(n)` = distance from the start
* `h(n)` = estimated distance to the goal

This guarantees the shortest path in the generated maze.

---

# Architecture

Main components:

```text
src/
├── parsing.py
├── maze_output.py
└── display/
    ├── mlx_display.py
    ├── renderer.py
    └── input_handler.py

mazegen/
├── maze.py
└── algo/
    ├── base.py
    ├── prim.py
    └── a_star.py
```

---
# Reusable module — mazegen

The maze generation logic is encapsulated in the Maze class and the mazegen package.
It can be used as a standalone library to generate and solve mazes programmatically, independently from the MLX graphical interface.

## Installation
```
pip install mazegen-1.0.0-py3-none-any.whl
```
## Basic usage
```python
from mazegen.maze import Maze, MazeState
from mazegen.algo.prim import Prim
from mazegen.algo.a_star import A_Star

maze = Maze(20, 15, (0, 0), (19, 14), seed=42)

maze.initialize()
maze.generate(Prim)
maze.run_all()
maze.solve(A_Star)

print("State:", maze.state)
print("Solution length:", len(maze.solution))
print("First 5 steps:", maze.solution[:5])
print("OK - mazegen works standalone")
```
## Advanced usage

You can use different configurations:
```python
maze = Maze(30, 30, (0, 0), (29, 29), seed=123, perfect=False)

maze.initialize()
maze.generate(Prim)
maze.run_all()
maze.solve(A_Star)
```
## Package build
To build the package:
```
pip install build
python3 -m build
```
This generates:
```
dist/mazegen-1.0.0-py3-none-any.whl
```
## Notes
Maze is fully independent from the MLX renderer.
You can plug any generator inheriting from BaseGenerator.
You can plug any solver inheriting from BaseSolver.
The API supports step-by-step generation (tick) or full generation (run_all).

---
# Bonus Features
- Deterministic generation using seeds.
- Animated maze generation.
- Animated A* pathfinding visualization.
- Solution path display with color gradient.
- Multiple color palettes switchable at runtime.
- Embedded "42" pattern.
- Runtime maze regeneration.

---

# Team and Project Management

## Roles

| Member   | Tasks                             |
| -------- | --------------------------------- |
| hhamidi  | Generation, pathfinding, parsing  |
| ramaroud | Maze core, MLX rendering, Maze output |

## Development Steps

1. Configuration parsing and validation.
2. Maze core implementation.
3. Prim maze generation.
4. A* pathfinding.
5. File export.
6. MLX graphical rendering.
7. Packaging and cleanup.

## Challenges

* Designing a reusable Maze class.
* Implementing the no-open-3×3 constraint.
* Integrating MLX rendering and animation.

## What Worked Well

* Pydantic validation.
* Clear separation of responsibilities.
* Strong typing with mypy.

## Possible Improvements

* Additional generation algorithms (DFS, Kruskal).
* Multiple solving algorithms.
* Maze statistics and benchmarks.

---

# Tools Used

* Python 3.13
* Pydantic v2
* mypy
* flake8
* MiniLibX

---

# Resources

* Maze Generation Algorithms — Wikipedia
* Prim's Algorithm — Wikipedia
* A* Search Algorithm — Wikipedia
* https://docs.pydantic.dev/
* https://docs.python.org/3/library/heapq.html

---

# AI Usage

Claude and ChatGPT were used for:

* Explaining algorithmic concepts.
* Reviewing documentation.
* Assisting with README drafting.

All design decisions, implementation, debugging, testing and final validation were performed by the project authors.
