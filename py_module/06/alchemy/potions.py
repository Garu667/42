def healing_potion() -> str:
    from .elements import create_fire, create_water

    return f"Healing potion brewed with {create_fire()} and {create_water()}"


def strength_potion() -> str:
    from .elements import create_fire, create_earth

    return f"Strength potion brewed with {create_earth()} and {create_fire()}"


def invisibility_potion() -> str:
    from .elements import create_air, create_water

    return (
        f"Invisibility potion brewed with {create_air()} and {create_water()}"
    )


def wisdom_potion() -> str:
    import elements as e

    result = (
        e.create_earth() + e.create_fire() + e.create_air() + e.create_water()
    )
    return f"Wisdom potion brewed with all elements: {result}"
