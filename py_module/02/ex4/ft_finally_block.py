
class GardenError(Exception):
    """Base class for garden-related exceptions"""
    pass


class PlantError(GardenError):
    """Exception raised for plant-related problems"""
    pass


def water_plants(plant_name: str) -> None:
    """Water plants while handling TypeError errors"""
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")


def test_watering_system() -> None:
    """Test the water_plants function with and without errrors"""

    print("Testing valid plants...")
    print("Opening watering system")
    try:
        water_plants("Tomato")
        water_plants("Lettuce")
        water_plants("Carrots")
    except PlantError as pe:
        print(f"Caught PlantError: {pe}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")

    print()
    print("Testing invalid plants...")
    print("Opening watering system")
    try:
        water_plants("Tomato")
        water_plants("lettuce")
        water_plants("Carrots")
    except PlantError as pe:
        print(f"Caught PlantError: {pe}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")


if __name__ == "__main__":
    print("=== Garden Watering System ===\n")
    test_watering_system()
    print("\nCleanup always happens, even with errors!")
