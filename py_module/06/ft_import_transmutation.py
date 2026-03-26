
def main() -> None:
    print("Method 1 - Full module import:")
    import alchemy.elements

    print(f"alchemy.elements.create_fire(): {alchemy.elements.create_fire()}")

    print("\nMethod 2 - Specific function import:")
    from alchemy.elements import create_water

    print(f"create_water(): {create_water()}")

    print("\nMethod 3 - Aliased import:")
    from alchemy.potions import healing_potion as heal

    print(f"heal(): {heal()}")

    print("\nMethod 4 - Multiple imports:")
    from alchemy.elements import create_earth, create_fire
    from alchemy.potions import strength_potion

    print(f"create_earth(): {create_earth()}")
    print(f"create_fire(): {create_fire()}")
    print(f"strength_potion(): {strength_potion()}")

    print("\nAll import transmutation methods mastered!")


if __name__ == "__main__":
    print("=== Import Transmutation Mastery ===\n")
    main()
