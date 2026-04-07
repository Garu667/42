import alchemy.elements


def main() -> None:
    print("Accessing alchemy/elements.py using 'import ...' structure")
    print("Testing create_earth: ", end="")
    print(f"{alchemy.elements.create_earth()}")


if __name__ == "__main__":
    try:
        print("=== Alembic 2 ===")
        main()
    except Exception as e:
        print(f"Error: {e}")
