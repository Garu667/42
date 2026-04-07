from typing import List


def light_spell_allowed_ingredients() -> List[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from .light_validator import validate_light_ingredients
    validation: str = validate_light_ingredients(ingredients)
    if "VALID" in validation and "INVALID" not in validation:
        return f"Spell recorded: {spell_name} ({validation})"
    return f"Spell rejected: {spell_name} ({validation})"
