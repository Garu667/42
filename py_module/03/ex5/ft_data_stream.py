import random
import typing


def gen_event() -> typing.Generator[tuple[str, str], None, None]:
    players: list[str] = ["alice", "bob", "charlie", "dylan"]
    actions: list[str] = ["run", "eat", "sleep", "grab", "move",
                          "climb", "swim", "use", "release"]
    while True:
        yield (random.choice(players), random.choice(actions))


def consume_event(
    events: list[tuple[str, str]]
) -> typing.Generator[tuple[str, str], None, None]:
    while len(events) > 0:
        event = random.choice(events)
        events.remove(event)
        print(f"Remains in list: {events}")
        yield event


def main() -> None:
    generator = gen_event()

    for i in range(1000):
        event = next(generator)
        print(f"Event {i}: Player {event[0]} did action {event[1]}")

    event_list: list[tuple[str, str]] = [next(generator) for _ in range(10)]
    print(f"\nBuilt list of 10 events: {event_list}")

    for event in consume_event(event_list):
        print(f"Got event from list: {event}")


if __name__ == "__main__":
    print("=== Game Data Stream Processor ===")
    main()
