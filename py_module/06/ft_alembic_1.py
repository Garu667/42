from elements import create_water


def main() -> None:
    print("Using 'from ... import ...' structure to access elements.py")
    print("Testing create_water:", create_water())


if __name__ == "__main__":
    try:
        print("=== Alembic 1 ===")
        main()
    except Exception as e:
        print(f"Error: {e}")
