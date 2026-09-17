*This project has been created as part of the 42 curriculum by ramaroud*

# Description

Fly-in routes a fleet of drones from a start hub to an end hub across a
network of connected zones, in as few simulation turns as possible.

A map file describes the network: how many drones to route, the zones with
their coordinates and metadata, and the bidirectional connections between
them. Each zone has a type that drives its movement cost (`normal` and
`priority` cost 1 turn, `restricted` costs 2, `blocked` cannot be entered)
and a capacity limiting how many drones may occupy it at once. Connections
carry their own capacity limit.

The program parses the map, plans a path for every drone, simulates the
fleet turn by turn while respecting every capacity and movement rule, and
prints the moves in the required output format alongside a colored terminal
view and an optional graphical replay.

No graph library is used: the graph, the shortest-path search and the
scheduler are all implemented from scratch, and the whole project is
object-oriented and type-annotated.

# Instructions

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
make install                        # install dependencies
make run                            # run on the default map
make run MAP=maps/hard/02_capacity_hell.txt
make debug MAP=maps/easy/02_simple_fork.txt
make lint                           # flake8 + mypy
make lint-strict                    # flake8 + mypy --strict
make clean
```

Running directly:

```bash
uv run python fly-in.py <map_file>              # terminal output + GUI
uv run python fly-in.py <map_file> --no-gui     # terminal output only
```

## Example

Input, `maps/easy/02_simple_fork.txt`:

```
nb_drones: 4

start_hub: start 0 0 [color=green]
hub: junction 1 0 [color=yellow max_drones=2]
hub: path_a 2 1 [color=blue]
hub: path_b 2 -1 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-junction [max_link_capacity=2]
connection: junction-path_a
connection: junction-path_b
connection: path_a-goal
connection: path_b-goal
```

Output:

```
  1: D1-junction D2-junction
  2: D1-path_b D2-path_a D3-junction D4-junction
  3: D1-goal D2-goal D3-path_b D4-path_a
  4: D3-goal D4-goal

Fly-in — simulation complete
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Metric           ┃ Value ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Drones delivered │     4 │
│ Total turns      │     4 │
└──────────────────┴───────┘
```

The two branches are used in parallel from turn 2, so four drones clear a
network whose junction only holds two of them at a time in four turns.

Errors stop the program with the offending line and cause, for example
`Error: line 3: invalid zone type: 'bogus'`.

# Technical choices

| Module | Responsibility |
|---|---|
| `src/network.py` | `Zone`, `ZoneType`, `Connection` and the hand-written `Graph` |
| `src/parsing.py` | Map file parser, raises `ParseError` with line and cause |
| `src/pathfinding.py` | Dijkstra search, `Congestion` counters, space-time planner |
| `src/simulation.py` | `Drone` state, path assignment strategies, turn-by-turn `Simulation` |
| `src/application.py` | CLI entry point and colored terminal output (rich) |
| `src/gui.py` | Graphical replay (pygame): layout, camera, replay, drawing |

`Graph` validates its own invariants (duplicate zones, duplicate
connections, unknown endpoints) by raising `ValueError`; the parser catches
those and re-raises them as a `ParseError` carrying the line number, so the
validation rules live in one place only.

# Algorithm

## Pathfinding

`Pathfinder` runs Dijkstra over the network, weighting each edge by the
movement cost of the destination zone rather than by a uniform 1, so
`restricted` zones are correctly counted as two turns. Blocked zones are
never expanded. Priority zones receive a small cost bonus, which makes them
win among paths of otherwise equal cost without ever justifying a detour
that would cost extra turns.

Complexity is O(E log V) per call, with V zones and E connections.

## Path assignment

Three strategies are computed and simulated, and the shorter result is kept:

- **Shared**: every drone follows the single cheapest path. This is optimal
  when the network has no contention, since nothing beats the shortest route
  when nobody is queueing.
- **Spread**: every drone gets its own path. Paths are assigned from the
  highest drone id down to the lowest, and each assignment records its zones
  and connections in a `Congestion` object which raises their cost for
  subsequent searches. Since the drones leaving last are the ones with the
  least slack, giving them the cheapest routes first and pushing
  earlier-departing drones onto alternate branches shortens the tail of the
  simulation.

Running both is cheap (paths are computed once, never recomputed during the
simulation) and guarantees that spreading drones out never makes a map that
did not need it worse.

## Simulation

`Simulation` advances in discrete turns. Within a turn, in-flight drones
land first, then drones standing on a zone attempt to depart, both in
drone-id order, which is what resolves conflicts: the lowest id wins the
contested slot. Because a departing drone is removed from its zone's
occupancy immediately, a drone behind it can take that slot in the same
turn, as the subject requires.

Waiting is implicit. A drone whose move fails a capacity check simply stays
where it is and retries next turn, and is omitted from that turn's output
line.

Restricted zones are the delicate case. A drone entering one commits to a
two-turn transit and cannot stop midway, so the destination slot is booked
one turn ahead in `_future_arrivals`, and the connection is charged for both
turns. The booking check is deliberately conservative: current occupants of
the destination are assumed still present on arrival, since their own moves
are not decided yet. This can cost a few turns of margin but makes an
invalid schedule impossible.

Memory is O(V + E) for the graph plus O(D * L) for the D drone paths of
length L; the per-turn usage maps are keyed by turn and stay proportional to
the number of moves actually made.

# Performance

| Map | Drones | Target | Result |
|---|---|---|---|
| Linear path | 2 | <= 6 | 4 |
| Simple fork | 4 | <= 8 | 4 |
| Basic capacity | 4 | <= 6 | 4 |
| Dead end trap | 5 | <= 12 | 8 |
| Circular loop | 6 | <= 15 | 14 |
| Priority puzzle | 5 | <= 12 | 6 |
| Maze nightmare | 8 | <= 30 | 13 |
| Capacity hell | 12 | <= 35 | 16 |
| Ultimate challenge | 15 | <= 45 | 26 |
| The Impossible Dream | 25 | record 45 | 45 |

Every mandatory target is met. The challenger map matches the reference
record but does not beat it: its entry gates are a chain of
`max_link_capacity=1` connections that serialise the fleet regardless of how
well the rest is routed, so going lower would need a search over departure
orders rather than over path choices alone.

# Visual representation

Both display modes required by the subject are provided.

The **terminal output** is the required move format, colored token by token
by the destination zone. A zone's `color=` value is used when it is a color
rich can render, otherwise the color falls back to the zone type, so the map
author's intent is respected without ever breaking on an arbitrary value.
This means the mandatory output and the mandatory visual feedback are the
same text, and cannot drift apart. A legend is printed once, and a summary
table closes the run.

The **graphical replay** (pygame, opens by default, disable with `--no-gui`)
draws the network using the zone coordinates from the map file, colors zones
by type, and shows each drone as a colored dot, drawn halfway along a
connection while in transit toward a restricted zone. The replay is
navigable: step forward and backward through turns, or autoplay. Being able
to step backwards is what makes it useful for understanding a schedule,
since a blockage is easier to read by replaying the turn before it.

On maps above 25 zones the view switches to smaller markers and hides labels
until zoomed in, which keeps a 54-zone map readable instead of a wall of
overlapping text; the mouse wheel zooms, dragging pans, and `R` resets.

Controls: `SPACE` / right arrow next turn, left arrow previous turn, `A`
autoplay, wheel zoom, drag pan, `R` reset view, `ESC` quit.

# Resources

- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Multi-agent pathfinding](https://en.wikipedia.org/wiki/Multi-agent_pathfinding)
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html)
- [rich documentation](https://rich.readthedocs.io/)
- [pygame documentation](https://www.pygame.org/docs/)
- [PEP 257 docstring conventions](https://peps.python.org/pep-0257/)
- [mypy documentation](https://mypy.readthedocs.io/)

## Use of AI

AI (Claude) was used as a design and review partner, not as a code
generator to copy from. Concretely:

- Discussing how to model the problem before writing anything: what the
  subject's rules imply, and why this is a multi-agent pathfinding problem
  rather than plain pathfinding.
- Reviewing the parser and the data model, and catching bugs in them: a
  restricted-zone token references a connection rather than a zone, which
  broke the terminal coloring when the traversal direction differed from the
  declaration order in the map file.
- Exploring why all drones sharing one path stalls on congested maps, and
  measuring congestion-penalty variants against the provided maps to settle
  on the two-strategy approach.
- Reviewing the display code, including making the dense-map view readable.

Every suggestion was tested against the provided maps before being kept, and
the turn counts in the performance table above were measured, not estimated.
