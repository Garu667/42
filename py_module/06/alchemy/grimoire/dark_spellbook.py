from .dark_validator import validate_dark_ingredients
from typing import List


def dark_spell_allowed_ingredients() -> List[str]:
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    validation: str = validate_dark_ingredients(ingredients)
    if "VALID" in validation and "INVALID" not in validation:
        return f"Spell recorded: {spell_name} ({validation})"
    return f"Spell rejected: {spell_name} ({validation})"
