def main() -> None:
    filename: str = "ancient_fragment.txt"

    print(f"Accessing Storage Vault: {filename}")
    try:
        fd = open(filename, "r")
    except FileNotFoundError:
        print("ERROR: Storage vault not found.")
        print("Run data generator first.")
        return
    if fd:
        print("Connection established...\n")
        content: str = fd.read()

        print("RECOVERED DATA:")
        print(content + "\n")

        fd.close()
        print("Data recovery complete. Storage unit disconnected.")


if __name__ == "__main__":
    try:
        print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
        main()
    except Exception as e:
        print(f"Error: {e}")
