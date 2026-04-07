import alchemy


def main() -> None:
    print("Import alchemy module only")
    print(f"Testing lead to gold: {alchemy.lead_to_gold()}")


if __name__ == "__main__":
    try:
        print("=== Transmutation 2 ===")
        main()
    except Exception as e:
        print(f"Error: {e}")
