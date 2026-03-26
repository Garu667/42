import alchemy.grimoire as grim

def main() -> None:
    print(f"Testing ingredient validation:")
    fire_air: str = "fire air"
    dragon: str = "dragon scales"
    print(
        f'validate_ingredients("{fire_air}"): {grim.validate_ingredients(fire_air)}'
    )
    print(
        f'validate_ingredients("{dragon}"): {grim.validate_ingredients(dragon)}'
    )

    print("\nTesting spell recording with validation:")
    print(
        f"""record_spell("Fireball", "fire air"): {grim.record_spell('Fireball', 'fire air')}"""
    )
    print(
        f"""record_spell("Dark Magic", "shadow"): {grim.record_spell("Dark Magic", "shadow")}"""
    )

    print("\nTesting late import technique:")
    print(
        f"""record_spell("Lightning", "air"): {grim.record_spell("Lightning", "air")}"""
    )

    print("\nCircular dependency curse avoided using late imports!")
    print("All spells processed safely!")


if __name__ == "__main__":
    print("=== Circular Curse Breaking ===\n")
    main()
