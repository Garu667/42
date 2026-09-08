*This project has been created as part of the 42 curriculum by ramaroud.*

# codexion

## Description

**codexion** is a multithreaded simulation of the classic Dining Philosophers
problem, reframed as coders sharing scarce USB dongles in a co-working space.

`number_of_coders` coders sit in a circular arrangement around a shared
Quantum Compiler. There are exactly as many USB dongles as coders, arranged
the same way: each coder has one dongle on their left and one on their right.
To compile, a coder must hold **both** their dongles at the same time.

Each coder repeats an endless cycle:

```
acquire left + right dongle → compile → release both dongles → debug → refactor → (repeat)
```

If a coder fails to start compiling within `time_to_burnout` milliseconds of
their last compile (or of the start of the simulation), they **burn out**,
and the whole simulation stops. It also stops once every coder has compiled
at least `number_of_compiles_required` times.

The project's real goal is building a correct, deadlock-free,
starvation-free, and precisely-timed concurrent program using only POSIX
threads and mutexes, with a hand-rolled priority queue for fair dongle
arbitration.

## Instructions

### Compilation

The Makefile provides `clean`, `fclean`, and `re` rules.

### Usage

```sh
./codexion number_of_coders time_to_burnout time_to_compile time_to_debug \
           time_to_refactor number_of_compiles_required dongle_cooldown scheduler
```

| Argument                    | Meaning                                                                 |
|------------------------------|--------------------------------------------------------------------------|
| `number_of_coders`           | Number of coders (and number of dongles)                               |
| `time_to_burnout`             | ms since last compile start before a coder burns out                   |
| `time_to_compile`             | ms a compile takes (both dongles held)                                 |
| `time_to_debug`               | ms spent debugging                                                     |
| `time_to_refactor`            | ms spent refactoring                                                    |
| `number_of_compiles_required` | Simulation stops once every coder has compiled at least this many times |
| `dongle_cooldown`             | ms a dongle stays unusable after being released                        |
| `scheduler`                   | `fifo` or `edf` — arbitration policy when several coders want a dongle  |

All arguments are mandatory and must be strictly positive integers (except
`scheduler`, which must be exactly `fifo` or `edf`).

Example:
```sh
# Scheduler in Maj
./codexion 3 500 100 100 100 3 50 FIFO
# Huge number
./codexion 3 999999999999999999999 100 100 100 3 50 fifo
# Zero Coders
./codexion 0 500 100 100 100 3 50 fifo
# One coder
./codexion 1 500 100 100 100 3 50 fifo
# dongle_cd > time_burnout
./codexion 3 200 50 50 50 3 300 fifo
# Stress EDF
./codexion 8 600 20 20 20 8 20 edf
```

### Reading the output

Every state change is logged as `timestamp_in_ms coder_id action`:

```
0 1 has taken a dongle
2 1 has taken a dongle
2 1 is compiling
202 1 is debugging
402 1 is refactoring
```

## Project structure

| File          | Functions                                                                 |
|---------------|----------------------------------------------------------------------------|
| `main.c`      | `monitor_routine`, `main` (top-level orchestration, argument-count check)  |
| `error.c`     | `cleanup_sim`, `abort_sim`, `free_return` (every error/shutdown cleanup path) |
| `init.c`      | `init_dongles`, `init_coders`, `init_unbreakable`, `init_sim`             |
| `parsing.c`   | `invalid_number`, `parse_positive_long`, `invalid_scheduler`, `swap`, `parsing` |
| `dongle.c`    | `dongle_ready`, `acquire_dongle`, `release_dongle`                        |
| `heap.c`      | `has_priority`, `heap_peek`, `heap_push`, `heap_pop`                      |
| `coders.c`    | `log_action`, `coder_compile`, `coder_life`, `coder_routine`, `coder_status` |
| `utils.c`     | `get_time_ms`, `get_elapsed_ms`, `ft_msleep`, `sim_should_stop`, `all_coders_done` |
| `codexion.h`  | Shared structs (`t_sim`, `t_coder`, `t_dongle`, `t_waiter`), the `t_error` enum, and every prototype |

## Blocking cases handled

- **Deadlock prevention (Coffman's circular wait).** Instead of every coder
  always acquiring `left` then `right`, each coder acquires whichever of its
  two dongles has the **lower id first**. This imposes a single global
  acquisition order across all coders, which makes a circular wait — the
  classic dining-philosophers deadlock — structurally impossible, regardless
  of scheduling luck.

- **Starvation prevention.** Each dongle keeps its own tiny waiting array
  (capacity 2 — its two neighbouring coders are structurally the only ones
  who can ever want it), ordered by arrival time (`fifo`) or by deadline
  `last_compile_start + time_to_burnout` (`edf`, with arrival time as a
  deterministic tie-breaker). Release does not hand the dongle to anyone
  directly — it simply clears `in_use`; every queued waiter is polling and
  independently re-checks whether *it* is the highest-priority entry
  (`heap_peek(dongle) == &waiter`) before taking it. A lower-priority waiter
  can win the race to re-lock the mutex first, but its own check will fail,
  so the FIFO/EDF ordering still holds even though no single thread is
  designated the winner at release time.

- **Cooldown handling.** After release, a dongle is unusable until
  `dongle_cooldown` ms have passed — `dongle_ready` refuses any waiter,
  including the highest-priority one, until that window has fully elapsed.
  The wait happens without holding the dongle's mutex for the whole
  duration (each poll only holds it briefly), so it never blocks other
  threads from being scheduled in the meantime.

- **Precise burnout detection.** A dedicated monitor thread polls every
  coder's `last_compile` timestamp on a short interval and compares it
  against `time_to_burnout`, logging the burnout and stopping the simulation
  well within the 10 ms tolerance required by the subject.

- **Log serialization.** All logging goes through a single function that
  locks a dedicated mutex around the `printf` call, so two messages can
  never interleave on one line.

- **Graceful, non-hanging shutdown.** The shared `stop` flag is itself
  protected by a mutex (read and written the same way everywhere — there is
  no "read-only, no lock needed" shortcut). Every wait in the program —
  a coder polling for a dongle, and every compile/debug/refactor sleep — is
  interruptible: each one re-checks the stop flag on a short interval
  instead of blocking or sleeping blindly for the full duration. Without
  this, a coder mid-`debug` with a large `time_to_debug`, or one still
  polling for a contested dongle, would keep the whole program alive long
  after the simulation should have ended.

- **Lock-order deadlock between mutexes (found during development).** An
  earlier version of the shutdown path had a coder lock a dongle's mutex and
  then lock the stop mutex (via the stop-check), while the monitor locked
  the stop mutex and then a dongle's mutex to wake waiters — two threads
  locking the same two mutexes in opposite order, a classic AB-BA deadlock
  risk. It was caught with `helgrind` before it ever triggered in practice.
  The current polling design (above) no longer needs that wake step at all,
  which removed the risk at its root rather than just reordering the locks.

## Thread synchronization mechanisms

- **Per-dongle `pthread_mutex_t`** protects that dongle's `in_use` flag,
  `released_at` timestamp, and its small (capacity-2) waiting queue. Every
  read or write of these fields goes through this lock — including a
  waiter's own eligibility check, so no two threads can ever disagree about
  whether a dongle is currently free.

- **Bounded polling instead of a condition variable.** A waiter registers
  itself in the dongle's queue once, then loops: release the lock, sleep a
  short fixed interval (`usleep`), reacquire the lock, and recheck whether
  it is now the highest-priority *and* cooldown-cleared entry
  (`dongle_ready`). The same loop condition also watches the simulation's
  `stop` flag, so a waiter never blocks past the point where the simulation
  should end.

- **`coders_mutex`** protects `last_compile` and `compile_count` on every
  `t_coder`. These fields are written by the owning coder thread and read by
  the monitor thread; without this lock, the monitor could read a torn or
  stale value while a coder is mid-write — a genuine data race, not just a
  theoretical one, since nothing in the C standard guarantees a plain memory
  write is visible to another thread without synchronization.

- **`stop_mutex`** protects the single `stop` flag shared by every thread.
  It is locked for every read, not only every write — reading a flag another
  thread can modify concurrently is exactly as much a data race as writing
  it.

- **`log_mutex`** wraps the one `printf` call used for all logging, so
  concurrent log lines from different threads never interleave.

- **Fixed-size priority array (`heap.c`)** backs both `fifo` and `edf`
  scheduling — no standard library priority queue is used. Since a given
  dongle can structurally only ever be wanted by its two neighbouring
  coders, the array never needs more than 2 slots: `heap_push` inserts and,
  if there are now two entries, swaps them into priority order with a
  single comparison; `heap_pop` removes the front slot and slides the other
  one forward. The only thing that changes between `fifo` and `edf` is the
  comparator (`has_priority`), which compares arrival time or deadline
  depending on the configured scheduler.

## Resources

- [Codexion Visualizer](https://github.com/0xS4cha/codexion_visualizer) made by [sservant](https://github.com/0xS4cha)
- Medium Forum, [this post](https://medium.com/@akshatarhabib/understanding-threads-in-c-c9feb5e9372a) particularly
- `man 3 pthread_mutex_lock`, `man 3 pthread_cond_wait`, `man 3 pthread_cond_timedwait`
- Youtube video, they are too far in my historic i couldn't link them

### AI usage disclosure

An AI assistant was used throughout this project's development in order to explain concurrency concepts.

- **Explaining concurrency concepts** on request (what a lock-order
  deadlock is versus a resource-order deadlock, why a condition variable
  read still needs a mutex, how a heap-based direct hand-off avoids
  starvation) rather than just supplying fixes.
