from alchemy.potions import healing_potion, strength_potion


def main() -> None:
    print("Direct access to alchemy/potions.py")
    print(f"Testing strength_potion: {strength_potion()}")
    print(f"Testing healing_potion: {healing_potion()}")


if __name__ == "__main__":
    try:
        print("=== Distillation 0 ===")
        main()
    except Exception as e:
        print(f"Error: {e}")
