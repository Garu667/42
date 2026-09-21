*This project has been created as part of the 42 curriculum by ramaroud.*

# codexion

## Description

Dining philosophers, rewritten. `number_of_coders` coders sit in a circle with
one USB dongle between each pair of neighbours (so: as many dongles as coders).
A coder needs **both** of its adjacent dongles to compile.

Each coder loops:

```
take both dongles -> compile -> release both -> debug -> refactor
```

The simulation ends when a coder **burns out** (no compile started within
`time_to_burnout` ms of its previous one) or when every coder has compiled
`number_of_compiles_required` times.

**Core design idea:** a coder never touches a dongle itself. A single **arbiter
thread** owns every dongle and one global ordered wait queue, and only ever
hands out a **complete pair**. Since nobody can hold half a pair, a circular
wait cannot exist.

## Instructions

### Build

```sh
make            # produces ./codexion
make clean      # objects
make fclean     # objects + binary
make re
```

Compiled with `-Wall -Wextra -Werror -pthread`, no warnings. No dependency
beyond libpthread.

### Run

```sh
./codexion n_coders time_to_burnout time_to_compile time_to_debug \
           time_to_refactor n_compiles_required dongle_cooldown scheduler
```

| Argument              | Meaning                                                      |
| --------------------- | ------------------------------------------------------------ |
| `n_coders`            | Number of coders, and of dongles (must be > 0)                |
| `time_to_burnout`     | ms without starting a compile before a coder burns out (> 0)  |
| `time_to_compile`     | ms spent compiling, both dongles held (> 0)                   |
| `time_to_debug`       | ms spent debugging (> 0)                                      |
| `time_to_refactor`    | ms spent refactoring (> 0)                                    |
| `n_compiles_required` | Stop once every coder reached this count (may be 0)           |
| `dongle_cooldown`     | ms a dongle stays unusable after release (may be 0)           |
| `scheduler`           | `fifo` or `edf`, lowercase — order used to arbitrate requests |

All values are integers. Anything else (negative, overflowing, `FIFO`, missing
argument) exits with an error message and no thread started.

### Output

One line per state change, `timestamp_ms coder_id action`:

```
0 1 has taken a dongle
0 1 has taken a dongle
0 1 is compiling
200 1 is debugging
400 1 is refactoring
```

Every `is compiling` is preceded by exactly two `has taken a dongle` lines for
the same coder. `burned out` is always the last line printed.

### Reference runs

```sh
./codexion 1 800 200 200 200 10 0 fifo     # 1 dongle for 2 needed -> burns out at ~800
./codexion 5 2000 200 200 200 10 0 fifo    # no burnout, stops after 10 compiles each
./codexion 5 2000 200 200 200 7 0 edf      # same with edf
./codexion 5 500 200 200 200 10 0 fifo     # cycle (600) > burnout (500) -> burns out at ~500
./codexion 5 3000 200 200 200 10 400 fifo  # cooldown respected, no burnout
```

## Blocking cases handled

- **Deadlock (circular wait).** Grants are all-or-nothing and done by one
  thread under one mutex: a coder is either given both dongles or none. No
  partial hold, no hold-and-wait, no cycle.
- **Starvation.** The queue is kept sorted (`fifo` by arrival, `edf` by
  deadline). When the arbiter cannot serve a waiter during a pass, it marks
  both of its dongles `reserved`, so no lower-priority waiter can take them
  later in that same pass. A blocked waiter is therefore only ever blocked by
  coders that are *currently compiling*, and those release after
  `time_to_compile`.
- **Cooldown.** A released dongle stays unavailable for `dongle_cooldown` ms.
  The check happens at grant time, inside the arbiter, so a cooling dongle is
  reserved for its rightful owner instead of being stolen by whoever asks next.
- **Lost / spurious wakeups.** A coder waits on `while (!granted && !stop)`:
  the flag, not the signal, is the contract. The arbiter flips both dongles to
  `in_use` *before* signalling, so a grant can never be missed or duplicated.
- **Waiting on time vs waiting on a thread.** During a cooldown no thread will
  signal the arbiter, so blocking in `pthread_cond_wait` would hang it. It
  drops the mutex for a short sleep instead, and goes back to `cond_wait` as
  soon as the only possible change is another thread's action.
- **Lock-order inversion (AB-BA).** `sched_mutex`, `log_mutex` and
  `coders_mutex` are never nested into one another; `stop_mutex` is always the
  innermost lock. A single global ordering exists, checked with `helgrind`.
- **Shutdown without hanging.** `stop` is set under its own mutex, then every
  coder condvar and the arbiter condvar are broadcast, so no thread stays
  parked in `cond_wait`. Every sleep is a poll loop that rechecks `stop`
  instead of sleeping blindly for the full duration.
- **Log serialization.** All output goes through one mutexed `printf`, and
  logging is refused once `stop` is set, so lines never interleave and nothing
  is printed after the final `burned out`.
- **Single coder.** With `n_coders == 1`, left and right are the same dongle:
  the coder takes it, can never compile, and burns out on time.

## Thread synchronization mechanisms

Threads: `n_coders` coder threads, one arbiter, one monitor. No global
variable — everything lives in `t_sim`, passed by pointer.

| Primitive       | Protects / does                                                            |
| --------------- | -------------------------------------------------------------------------- |
| `sched_mutex`   | Dongle state, wait queue, sequence counter, `granted` flags                 |
| `sched_cond`    | Wakes the arbiter on a new request or a release                             |
| `coder[i].cond` | One condvar per coder, signalled when its pair is granted                   |
| `coders_mutex`  | `last_compile` and `compile_count` (written by coders, read by the monitor) |
| `stop_mutex`    | The `stop` flag, locked for reads as well as writes                         |
| `log_mutex`     | The single `printf` used for every log line                                 |

- **Queue (`queue.c`).** Sorted insertion into a fixed array, not a heap: the
  arbiter needs to walk *all* waiters in priority order on each pass, which a
  heap cannot do without being destroyed. O(n) insert, O(1) ordered traversal.
- **Scheduler policy.** `fifo` and `edf` differ only by the comparator
  `has_priority()`. `seq` is unique and assigned under `sched_mutex`, so the
  order is total and the runs are reproducible.
- **Monitor thread.** Polls each coder's `last_compile` on a short interval and
  stops the simulation within the 10 ms tolerance of the deadline.

### Source layout

| File                       | Role                                              |
| -------------------------- | ------------------------------------------------- |
| `main.c`                   | Entry point, monitor thread, shutdown             |
| `parsing.c` / `init.c`     | Argument checking, allocation, thread startup     |
| `coders.c`                 | Coder lifecycle and logging                       |
| `dongle.c`                 | Request / release seen from the coder side        |
| `scheduler.c`              | The arbiter: grant, reserve, scan                 |
| `sched_wait.c`             | When the arbiter blocks and when it sleeps        |
| `queue.c`                  | Ordered wait queue, `fifo` / `edf` comparator     |
| `utils.c` / `error.c`      | Time helpers, interruptible sleep, cleanup paths  |

## Resources

- [Codexion Visualizer](https://github.com/0xS4cha/codexion_visualizer) by [sservant](https://github.com/0xS4cha)
- [Understanding threads in C](https://medium.com/@akshatarhabib/understanding-threads-in-c-c9feb5e9372a) (Medium)
- `man 3 pthread_mutex_lock`, `man 3 pthread_cond_wait`, `man 3 pthread_cond_signal`
- `valgrind --tool=helgrind` and `--tool=drd`, plus `-fsanitize=thread`, used to
  check for data races and lock-order inversions

### AI usage

An AI assistant was used as an explainer and a reviewer, not as a code
generator:

- **Explaining concepts** on demand: lock-order vs resource-order deadlock, why
  reading a shared flag still requires a mutex, why a condvar always needs a
  predicate loop.
- **Reviewing the arbiter design** (`scheduler.c`, `queue.c`) after a first
  version where each dongle had its own queue and its own cooldown check: that
  version could starve a waiter and applied the cooldown at the wrong moment.
  The discussion led to the current single-queue arbiter with reservation.
- **Writing this README**: structure and wording.
