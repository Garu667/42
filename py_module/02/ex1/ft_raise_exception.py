
def input_temperature(temp_str: str) -> int:
    """
    Convert a string to an integer temperature and validate plant conditions.
    Args:
        temp_str (str): The temperature as a string input.

    Returns:
        Optional[int]: The parsed temperature if valid, otherwise None.

    Behavior:
        - Raise ValueError if conversion fails.
        - Raise ValueError if temperature is outside plant tolerance range.
        - Prints temperature state if everything is ok.
    """
    tmp: int = int(temp_str)
    if tmp > 40:
        raise ValueError(f"{tmp}°C is too hot for plants (max 40°C)")
    elif tmp < 0:
        raise ValueError(f"{tmp}°C is too cold for plants (min 0°C)")
    else:
        print(f"Temperature is now {tmp}°C")
    return tmp


def test_temperature() -> None:
    """
    Run multiple test cases for input_temperature function.
    Except ValueError and prints them if caught
    """
    print("\nInput data is '25'")
    input_temperature("25")

    print("\nInput data is 'abc'")
    try:
        input_temperature("abc")
    except ValueError as ve:
        print(f"Caught input_temperature error: {ve}")

    print("\nInput data is '100'")
    try:
        input_temperature("100")
    except ValueError as ve:
        print(f"Caught input_temperature error: {ve}")

    print("\nInput data is '-50'")
    try:
        input_temperature("-50")
    except ValueError as ve:
        print(f"Caught input_temperature error: {ve}")

    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===")
    test_temperature()
