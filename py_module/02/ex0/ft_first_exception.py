
def check_temperature(temp_str: str) -> int:
    print(f"Testing temperature: {temp_str}")
    try:
        tmp: int = int(temp_str)
    except ValueError as ve:
        print(f"Error: '{temp_str}' is not a valid number")
        return
    if tmp > 40:
        print(f"Error: {tmp} is too hot for plants (max 40°C)")
    elif tmp < 0:
        print(f"Error: {tmp} is too cold for plants (min 0°C)")
    else:
        print(f"Temperature {tmp}°C is perfect for plants!")
    return tmp
"""
if __name__ == "__main__":
    print("=== Garden Temperature Checker ===\n")
    print(check_temperature("25"), "\n")

    print(check_temperature("abc"), "\n")

    print(check_temperature(100), "\n")

    print(check_temperature(-50), "\n")

    print("All tests completed - program didn't crash!")
"""
