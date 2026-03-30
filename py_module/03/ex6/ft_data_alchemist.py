import random


def main() -> None:
    players: list[str] = [
        "Alice", "bob", "Charlie", "dylan", "Emma",
        "Gregory", "john", "kevin", "Liam"
    ]

    all_capital: list[str] = [p.capitalize() for p in players]
    already_capital: list[str] = [p for p in players if p[0].isupper()]

    print(f"Initial list of players: {players}")
    print(f"New list with all names capitalized: {all_capital}")
    print(f"New list of capitalized names only: {already_capital}")

    scores: dict[str, int] = {p: random.randint(0, 1000) for p in all_capital}
    average: float = round(sum(scores.values()) / len(scores), 2)

    high_scores: dict[str, int] = {
        p: s for p, s in scores.items() if s > average
    }

    print(f"Score dict: {scores}")
    print(f"Score average is {average}")
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    try:
        print("=== Game Data Alchemist ===\n")
        main()
    except Exception as e:
        print(f"Error: {e}")
