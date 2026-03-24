import sys


def get_stats(nbrs: list[int]):
    print(f"Scores processed: {nbrs}")
    print(f"Total players: {len(nbrs)}")
    print(f"Average score: {sum(nbrs) / len(nbrs)}")
    print(f"High score: {max(nbrs)}")
    print(f"Low score: {min(nbrs)}")
    print(f"Score range: {max(nbrs) - min(nbrs)}")


def check(av: list[str]) -> int:
    error: int = 0
    for arg in av[1:]:
        try:
            int(arg)
        except ValueError:
            error = -1
            print(f"Invalid parameter: '{arg}'")
    return error


def parsing(av: list[str]) -> list[int]:
    return [int(arg) for arg in av[1:]]


def main(ac: int, av: list[str]) -> None:
    if ac == 1 or check(av) != 0:
        print("No scores provided.", end=" ")
        print(f"Usage: python3 {av[0]} <score1> <score2> ...")
        return
    score: list[int] = parsing(av)
    get_stats(score)


if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    main(len(sys.argv), sys.argv)
