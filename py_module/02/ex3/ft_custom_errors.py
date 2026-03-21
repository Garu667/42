
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
    """ test the PlantError() """
    raise PlantError(f"The {name} plant is wilting!")


def water_check(liter: int) -> None:
    """ test the WaterError() """
    if liter > 10:
        raise WaterError("Not enough water in the tank!")


def main() -> None:
    """ use plant_check and water_check to show custom errors """
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
