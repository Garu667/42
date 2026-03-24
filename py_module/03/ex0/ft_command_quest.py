import sys


def main() -> None:
    i: int = 1
    args: list[str] = sys.argv
    print(f"Program name: {args[0]}")
    if len(args) <= 1:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(args) - 1}")
    for strings in args[1:]:
        print(f"Argument {i}: {strings}")
        i += 1
    print(f"Total arguments: {len(args)}")


if __name__ == "__main__":
    print("=== Command Quest ===")
    main()
