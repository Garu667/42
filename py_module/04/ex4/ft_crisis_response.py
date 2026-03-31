def crisis_handler(filename: str) -> int:
    try:
        with open(filename, "r") as fd:
            content = fd.read()
            print(f"SUCCESS: Archive recovered - ``{content}''")
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
        return 1
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
        return 2
    except Exception as e:
        print(f"RESPONSE: Unknown anomaly - {e}")
        return 3
    return 0


def main() -> None:
    attempt_1: str = "lost_archive.txt"
    print(f"CRISIS ALERT: Attempting access to '{attempt_1}'...")
    if crisis_handler(attempt_1) == 1:
        print("STATUS: Crisis handled, system stable")

    attempt_2: str = "classified_vault.txt"
    print(f"\nCRISIS ALERT: Attempting access to '{attempt_2}'...")
    if crisis_handler(attempt_2) == 2:
        print("STATUS: Crisis handled, security maintained")

    attempt_3: str = "standard_archive.txt"
    print(f"\nROUTINE ACCESS: Attempting access to '{attempt_3}'...")
    if crisis_handler(attempt_3) == 0:
        print("STATUS: Normal operations resumed\n")

    print("All crisis scenarios handled successfully. Archive secure.")


if __name__ == "__main__":
    try:
        print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")
        main()
    except Exception as e:
        print(f"Error: {e}")
