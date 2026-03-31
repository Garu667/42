import sys


def main() -> None:
    input_stream: str = "Input Stream active."
    try:
        archivist_id: str = input(input_stream + " Enter archivist ID: ")
        status_report: str = input(input_stream + " Enter status report: ")
    except (KeyboardInterrupt, EOFError):
        print("\nQuitting...")
    else:
        print("\n[STANDARD] Archive status from",
              f"{archivist_id}: {status_report}")
        sys.stderr.write(
                "[ALERT] System diagnostic: Communication channels verified\n")
        sys.stdout.write("[STANDARD] Data transmission complete\n")

        print("\nThree-channel communication test successful.")


if __name__ == "__main__":
    try:
        print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n")
        main()
    except Exception as e:
        print(f"Error: {e}")
