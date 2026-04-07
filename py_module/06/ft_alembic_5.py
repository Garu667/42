from alchemy import create_air


def main() -> None:
    print("Accessing the alchemy module using 'from alchemy import ...'")
    print("Testing create_air: ", end="")
    print(f"{create_air()}")


if __name__ == "__main__":
    print("=== Alembic 5 ===")
    main()
