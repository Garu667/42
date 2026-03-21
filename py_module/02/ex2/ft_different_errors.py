def garden_operations(operation_number: int) -> None:
    x: int = 40
    tmp: str = "test"
    if operation_number == 0:
        try:
            x = int("abc")
        except ValueError as ve:
            print(f"Caught ValueError: {ve}\n")
    elif operation_number == 1:
        try:
            x /= 0
        except ZeroDivisionError as zde:
            print(f"Caught ZeroDivisionError: {zde}\n")
    elif operation_number == 2:
        try:
            x = open("/non/existent/file")
        except FileNotFoundError as fnfe:
            print(f"Caught FileNotFoundError: {fnfe}\n")
    elif operation_number == 3:
        try:
            tmp += 5
        except TypeError as te:
            print(f"Caught TypeError: {te}\n")
    else:
        print("Operation completed successfully")
        return


def test_error_types() -> None:
    print("Testing operation 0...")
    garden_operations(0)

    print("Testing operation 1...")
    garden_operations(1)

    print("Testing operation 2...")
    garden_operations(2)

    print("Testing operation 3...")
    garden_operations(3)

    print("Testing operation 4...")
    garden_operations(4)


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===\n")

    test_error_types()
    print("\nAll error types tested successfully")
