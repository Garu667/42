import alchemy.transmutation as transmutation


def main() -> None:
    print("Import transmutation module directly")
    print(f"Testing lead to gold: {transmutation.lead_to_gold()}")


if __name__ == "__main__":
    try:
        print("=== Transmutation 1 ===")
        main()
    except Exception as e:
        print(f"Error: {e}")
