import random


ACHIEVEMENTS: list[str] = [
    "Crafting Genius",
    "Strategist",
    "World Savior",
    "Speed Runner",
    "Survivor",
    "Master Explorer",
    "Treasure Hunter",
    "Unstoppable",
    "First Steps",
    "Collector Supreme",
    "Untouchable",
    "Sharp Mind",
    "Boss Slayer",
    "Hidden Path Finder"
]


def gen_player_achievements() -> set[str]:
    count = random.randint(1, len(ACHIEVEMENTS))
    return set(random.sample(ACHIEVEMENTS, count))


def achievement() -> list:
    alice: set[str] = gen_player_achievements()
    bob: set[str] = gen_player_achievements()
    charlie: set[str] = gen_player_achievements()
    dylan: set[str] = gen_player_achievements()

    players = [alice, bob, charlie, dylan]
    print(f"Player Alice: {alice}")
    print(f"Player Bob: {bob}")
    print(f"Player Charlie: {charlie}")
    print(f"Player Dylan: {dylan}")
    return players


def main() -> None:
    p = achievement()
    all_achievement = p[0].union(p[1], p[2], p[3])
    print(f"\nAll distinct achievements: {all_achievement}")

    common = p[0].intersection(p[1], p[2])
    print(f"\nCommon achievements: {common}\n")

    print(f"Only Alice has: {p[0].difference(p[1], p[2], p[3])}")
    print(f"Only Bob has: {p[1].difference(p[0], p[2], p[3])}")
    print(f"Only Charlie has: {p[2].difference(p[0], p[1], p[3])}")
    print(f"Only Dylan has: {p[3].difference(p[0], p[1], p[2])}")

    print()
    all_achievements_set = set(ACHIEVEMENTS)
    print(f"Alice is missing: {all_achievements_set.difference(p[0])}")
    print(f"Bob is missing: {all_achievements_set.difference(p[1])}")
    print(f"Charlie is missing: {all_achievements_set.difference(p[2])}")
    print(f"Dylan is missing: {all_achievements_set.difference(p[3])}")


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")
    main()
