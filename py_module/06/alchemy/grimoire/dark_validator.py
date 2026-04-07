from .dark_spellbook import dark_spell_allowed_ingredients


def validate_dark_ingredients(ingredients: str) -> str:
    allowed: list[str] = dark_spell_allowed_ingredients()
    for item in allowed:
        if item in ingredients.lower():
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
