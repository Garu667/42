import elements


def main() -> None:
    print("Using 'import ...' structure to access elements.py")
    print("Testing create_fire:", elements.create_fire())


if __name__ == "__main__":
    try:
        print("=== Alembic 0 ===")
        main()
    except Exception as e:
        print(f"Error: {e}")
