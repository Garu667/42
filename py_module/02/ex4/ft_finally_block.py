
class GardenError(Exception):
    """Base class for garden-related exceptions"""
    pass


class PlantError(GardenError):
    """Exception raised for plant-related problems"""
    pass


def water_plants(plant_name: str) -> None:
    """Water plants while handling TypeError errors"""
    plant_name = plant_name.capitalize()
    if plant_name == plant_name.capitalize():
        print(f"Watering {plant_name}: [OK]")
    else:
        raise PlantError("not capitalized")


def test_watering_system() -> None:
    """Test the water_plants function with and without errrors"""

    print("Testing valid plants...")
    print("Opening watering system")
    try:
        water_plants("tomato")
        water_plants("lettuce")
        water_plants("carrots")
    except PlantError as pe:
        print(f"Caught PlantError: {pe}")
    finally:
        print("Closing watering system")


if __name__ == "__main__":
    print("=== Garden Watering System ===\n")
    test_watering_system()
