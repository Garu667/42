
def input_temperature(temp_str: str) -> int | None:
    """
    Convert a string to an integer temperature and validate plant conditions.

    Args:
        temp_str (str): The temperature as a string input.

    Returns:
        Optional[int]: The parsed temperature if valid, otherwise None.

    Behavior:
        - Prints an error if conversion fails.
        - Prints warnings if temperature is outside plant tolerance range.
        - Prints success message if temperature is acceptable.
    """
    try:
        tmp: int = int(temp_str)
    except ValueError as ve:
        print(f"Caught input_temperature error: {ve}")
        return None
    if tmp > 40:
        print(f"Caught input_temperature error: {tmp}°C is too hot for \
plants (max 40°C)")
    elif tmp < 0:
        print(f"Caught input_temperature error: {tmp}°C is too cold for \
plants (min 0°C)")
    else:
        print(f"Temperature {tmp}°C is perfect for plants!")
    return tmp


def test_temperature() -> None:
    """
    Run multiple test cases for input_temperature function.
    """
    print("\nInput data is '25'")
    input_temperature("25")

    print("\nInput data is 'abc'")
    input_temperature("abc")

    print("\nInput data is '100'")
    input_temperature("100")

    print("\nInput data is '-50'")
    input_temperature("-50")

    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===")
    test_temperature()
