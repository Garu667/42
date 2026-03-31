def crisis_handler(filename: str) -> None:
    try:
        with open(filename, "r") as fd:
            content = fd.read()
            print(f"SUCCESS: Archive recovered - ``{content}''")
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
    except Exception as e:
        print(f"RESPONSE: Unknown anomaly - {e}")


def main() -> None:
    attempt_1: str = "lost_archive.txt"
    print(f"CRISIS ALERT: Attempting access to '{attempt_1}'...")
    crisis_handler(attempt_1)
    print("STATUS: Crisis handled, system stable\n")

    attempt_2: str = "classified_vault.txt"
    print(f"CRISIS ALERT: Attempting access to '{attempt_2}'...")
    crisis_handler(attempt_2)
    print("STATUS: Crisis handled, security maintained\n")

    attempt_3: str = "standard_archive.txt"
    print(f"ROUTINE ACCESS: Attempting access to '{attempt_3}'...")
    crisis_handler(attempt_3)
    print("STATUS: Normal operations resumed\n")

    print("All crisis scenarios handled successfully. Archive secure.")


if __name__ == "__main__":
    try:
        print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")
        main()
    except Exception as e:
        print(f"Error: {e}")
