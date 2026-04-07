
def main() -> None:
    print("Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    from alchemy.grimoire.dark_spellbook import dark_spell_record
    print(f"Testing record dark spell: {dark_spell_record('Shadow', 'bats')}")


if __name__ == "__main__":
    print("=== Kaboom 1 ===")
    main()
