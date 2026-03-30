import sys


def main() -> None:
    args: list[str] = sys.argv
    print(f"Program name: {args[0]}")
    if len(args) <= 1:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(args) - 1}")
    for id, strings in enumerate(args[1:]):
        print(f"Argument {id + 1}: {strings}")
    print(f"Total arguments: {len(args)}")


if __name__ == "__main__":
    try:
        print("=== Command Quest ===")
        main()
    except Exception as e:
        print(f"Error: {e}")
