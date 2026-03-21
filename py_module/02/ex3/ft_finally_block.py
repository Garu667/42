
def water_plants(plant_list: list[str | None]) -> None:
    """Water plants while handling TypeError errors"""
    error: bool = False
    print("Opening watering system")
    try:
        for plant in plant_list:
            if plant is None:
                print("Error: Cannot water None - invalid plant!")
                error = True
                break
            print(f"Watering {plant}")
    except TypeError as te:
        print(f"Caught TypeError: {te}")
        error = True
    finally:
        print("Closing watering system (cleanup)")
    if error is True:
        return
    print("Watering completed successfully!")

def test_watering_system() -> None:
    """Test the water_plants function with and without errrors"""
    print("=== Garden Watering System ===\n")

    print("Testing normal watering...")
    water_plants(["tomato", "lettuce", "carrots"])
    print()

    print("Testing with error...")
    #Someone ate lettuce
    water_plants(["tomato", None, "carrots"])
    print("\nCleanup always happens, even with errors!")

if __name__ == "__main__":
    test_watering_system()
