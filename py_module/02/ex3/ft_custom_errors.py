
class GardenError(Exception):
    """Base class for garden-related exceptions"""
    pass


class PlantError(GardenError):
    """Exception raised for plant-related problems"""
    pass


class WaterError(GardenError):
    """Exception raised for watering-related problems"""
    pass


def plant_check(name: str) -> None:
    """
    Simulate a plant-related failure.

    Args:
        name (str): Name of the plant.

    Raises:
        PlantError: Always raised to simulate plant failure.
    """
    raise PlantError(f"The {name} plant is wilting!")


def water_check(liter: int) -> None:
    """
    Validate water quantity.

    Args:
        liter (int): Amount of water in liters.

    Raises:
        WaterError: If the water amount exceeds allowed threshold.
    """
    if liter > 10:
        raise WaterError("Not enough water in the tank!")


def main() -> None:
    """
    Demonstrate usage of custom exceptions and exception hierarchy.
    """
    print("=== Custom Garden Errors Demo ===\n")

    print("Testing PlantError...")
    try:
        plant_check("tomato")
    except PlantError as pe:
        print(f"Caught PlantError: {pe}\n")

    print("Testing WaterError...")
    try:
        water_check(11)
    except WaterError as we:
        print(f"Caught WaterError: {we}\n")

    print("Testing catching all garden error...")
    try:
        plant_check("tomato")
    except GardenError as ge:
        print(f"Caught GardenError: {ge}")
    try:
        water_check(11)
    except GardenError as ge:
        print(f"Caught GardenError: {ge}")

    print("\nAll custom error types work correctly!")


if __name__ == "__main__":
    main()
