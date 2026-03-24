import math


def parsing_string(data: str) -> tuple[float, float, float] | None:
    if "," in str(data):
        try:
            values: list[str] = data.split(",")
            x, y, z = map(float, values)
            return (x, y, z)
        except ValueError as ve:
            if "could not convert" in str(ve):
                bad_value = str(ve).split("'")[1]
                print(f"Error on parameter '{bad_value}': {ve}")
            else:
                print("Invalid syntax")
            return None
    else:
        print("Invalid syntax")
    return None


def get_player_pos() -> tuple[float, float, float] | None:
    input_str: str = "Enter new coordinates as floats in format 'x,y,z': "
    while True:
        try:
            user_input: str = input(input_str)
        except (KeyboardInterrupt, EOFError):
            print("\nLeaving...")
            return None
        pos = parsing_string(user_input)
        if pos is not None:
            break
    return pos


def calculate_distance(
    pos1: tuple[float, float, float],
    pos2: tuple[float, float, float]
        ) -> float:
    return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1])
                     ** 2 + (pos2[2] - pos1[2]) ** 2)


def main() -> None:
    center: tuple = (0.0, 0.0, 0.0)
    print("Get a first set of coordinates")
    pos1: tuple[float, float, float] | None = get_player_pos()
    if pos1 is None:
        return
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")
    print(f"Distance to center: {calculate_distance(center, pos1):.4f}")

    print("\nGet a second set of coordinates")
    pos2: tuple[float, float, float] | None = get_player_pos()
    if pos2 is None:
        return
    print("Distance between the 2 sets of",
          f"coordinates: {calculate_distance(pos1, pos2):.4f}")


if __name__ == "__main__":
    print("=== Game Coordinate System ===\n")
    main()
