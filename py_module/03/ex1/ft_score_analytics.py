import sys


def get_stats(nbrs: list[int]):
    print(f"Scores processed: {nbrs}")
    print(f"Total players: {len(nbrs)}")
    print(f"Total score: {sum(nbrs)}")
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
    def is_valid(s: str) -> bool:
        try:
            int(s)
        except ValueError:
            return False
        return True
    return [int(arg) for arg in av[1:] if is_valid(arg)]


def main(ac: int, av: list[str]) -> None:
    usage: str = "Usage: python3 {av[0]} <score1> <score2> ..."
    if ac == 1:
        print(f"No scores provided. {usage}")
        return
    scores: list[int] = parsing(av)
    if not scores:
        print(f"No scores provided. {usage}")
        return
    get_stats(scores)


if __name__ == "__main__":
    try:
        print("=== Player Score Analytics ===")
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(f"Error as {e}")
