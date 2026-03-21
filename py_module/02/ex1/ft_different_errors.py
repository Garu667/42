
def garden_operations() -> None:
    print("Testing ValueError...")
    try:
        tmp: int = int("abc")
    except ValueError as ve:
        print(f"Caught ValueError: {ve}\n")
    print("Testing ZeroDivisionError...")
    try:
        x: int = 40 / 0
    except ZeroDivisionError as zde:
        print(f"Caught ZeroDivisionError: {zde}\n")
    print("Testing FileNotFoundError...")
    try:
        fd: int = open("missing.txt")
    except FileNotFoundError as fnfe:
        print(f"Caught FileNotFoundError: {fnfe}\n")
    print("Testing KeyError...")
    plants = {'Rose': 30, 'Tulipe': 28, 'Sunflower': 33}
    try:
        plants['missing_plant']
    except KeyError as ke:
        print(f"Caught KeyError: {ke}\n")
    print("Testing multiple errors together...")

"""
if __name__ == "__main__":
    print("=== Garden Error Types Demo ===\n")

    garden_operations()
    print("Caught an error, but program continues!\n")
    print("All error types tested successfully")
"""
