
def create_entry() -> list[str]:
    entries: list[str] = [
            "[ENTRY 001] New quantum algorithm discovered",
            "[ENTRY 002] Efficiency increased by 347%",
            "[ENTRY 003] Archived by Data Archivist trainee"
            ]
    return entries


def main() -> None:
    filename: str = "new_discovery.txt"
    entries: list[str] = create_entry()

    print(f"Initializing new storage unit: {filename}")
    fd = open(filename, "w")
    if fd:
        print("Storage unit created successfully...\n\n"
              "Inscribing preservation data...")
        for line in entries:
            fd.write(f"{line}\n")
            print(line)

        fd.close()
        print("\nData inscription complete. Storage unit sealed.")
        print(f"Archive '{filename}' ready for long-term preservation")


if __name__ == "__main__":
    try:
        print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
        main()
    except Exception as e:
        print(f"Error: {e}")
