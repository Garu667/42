import alchemy.transmutation.recipes as recipes


def main() -> None:
    print("Using file alchemy/transmutation/recipes.py directly")
    print(f"Testing lead to gold: {recipes.lead_to_gold()}")


if __name__ == "__main__":
    try:
        print("=== Transmutation 0 ===")
        main()
    except Exception as e:
        print(f"Error: {e}")
