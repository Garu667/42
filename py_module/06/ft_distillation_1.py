import alchemy


def main() -> None:
    print("Using: 'import alchemy' structure to access potions")
    print(f"Testing strength_potion: {alchemy.strength_potion()}")
    print(f"Testing heal alias: {alchemy.heal()}")


if __name__ == "__main__":
    try:
        print("=== Distillation 1 ===")
        main()
    except Exception as e:
        print(f"Error: {e}")
