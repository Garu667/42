
def input_temperature(temp_str: str) -> int | None:
    """
    try to convert a temperature string to a int, except an error
    return with an error message if error is raised
    return temperature if nothing
    """
    try:
        tmp: int = int(temp_str)
    except ValueError as ve:
        print(f"Caught input_temperature error: {ve}")
        return None
    print(f"Temperature is now {tmp}°C")
    return tmp


def test_temperature() -> None:
    """
    Test different case of error for the input_temperature
    """
    print("\nInput data is '25'")
    input_temperature("25")

    print("\nInput data is 'abc'")
    input_temperature("abc")

    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===")
    test_temperature()
