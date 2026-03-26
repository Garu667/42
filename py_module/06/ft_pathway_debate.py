import alchemy.transmutation.basic as basic
import alchemy.transmutation.advanced as advanced
import alchemy.transmutation as trans


def main() -> None:
    print("Testing Absolute Imports (from basic.py):")
    print(f"lead_to_gold(): {basic.lead_to_gold()}")
    print(f"stone_to_gem(): {basic.stone_to_gem()}")

    print("\nTesting Relative Imports (from advanced.py):")
    print(f"philosophers_stone(): {advanced.philosophers_stone()}")
    print(f"elixir_of_life(): {advanced.elixir_of_life()}")

    print("\nTesting Package Access:")
    print(f"alchemy.transmutation.lead_to_gold(): {trans.lead_to_gold()}")
    print(
        f"alchemy.transmutation.philosophers_stone(): {trans.philosophers_stone()}"
    )

    print("\nBoth pathways work! Absolute: clear, Relative: concise")


if __name__ == "__main__":
    print("=== Pathway Debate Mastery ===\n")
    main()
