import pytest
from mazegen.maze import Maze, MazeState
from tests.fake_generator import FakeGenerator

def test_initial_state():
    maze = Maze(10, 10, (0, 0), (9, 9))
    assert maze.state == MazeState.BLANK

def test_initialize():
    maze = Maze(10, 10, (0, 0), (9, 9))
    maze.initialize()
    assert maze.state == MazeState.INITIALIZED
    assert len(maze.grid) == 10
    assert all(v == 0xF for row in maze.grid for v in row
               if (col, row_i) not in maze.forty_two_cells
               for col, row_i in [(maze.grid[0].index(v), 0)])

def test_generate_transitions():
    maze = Maze(10, 10, (0, 0), (9, 9))
    maze.initialize()
    maze.generate(FakeGenerator)
    assert maze.state == MazeState.GENERATING

def test_run_all():
    maze = Maze(10, 10, (0, 0), (9, 9))
    maze.initialize()
    maze.generate(FakeGenerator)
    maze.run_all()
    assert maze.state == MazeState.GENERATED
    assert maze.is_done()

def test_tick_returns_false_when_done():
    maze = Maze(5, 5, (0, 0), (4, 4))
    maze.initialize()
    maze.generate(FakeGenerator)
    results = []
    while True:
        still_going = maze.tick()
        results.append(still_going)
        if not still_going:
            break
    assert results[-1] == False
    assert maze.state == MazeState.GENERATED

def test_reset():
    maze = Maze(10, 10, (0, 0), (9, 9))
    maze.initialize()
    maze.generate(FakeGenerator)
    maze.run_all()
    maze.reset()
    assert maze.state == MazeState.INITIALIZED

def test_grid_unavailable_when_blank():
    maze = Maze(10, 10, (0, 0), (9, 9))
    with pytest.raises(RuntimeError):
        _ = maze.grid

def test_invalid_dimensions():
    with pytest.raises(ValueError):
        Maze(1, 10, (0, 0), (0, 9))

def test_entry_equals_exit():
    with pytest.raises(ValueError):
        Maze(10, 10, (0, 0), (0, 0))
