from .validator import validate_ingredients


def record_spell(spell_name: str, ingredients: str) -> str:
    validation: str = validate_ingredients(ingredients)
    if validation == f"{ingredients} - VALID":
        return f"Spell recorded: {spell_name} ({validation})"
    return f"Spell rejected: {spell_name} ({validation})"
