class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.__name: str = name
        self.__height: int = height
        self.__old: int = age
        print(f"Created: {self.__name} ({self.__height}cm, {self.__old} days)")

    def grow(self, length) -> None:
        self.__height += length

    def age(self, days) -> None:
        self.__old += days

    def get_info(self) -> None:
        print(f"{self.__name} ({self.__height}cm, {self.__old} days)")


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    rose = Plant("Rose", 25, 30)
    oak = Plant("Oak", 200, 365)
    cactus = Plant("Cactus", 5, 90)
    sunflower = Plant("Sunflower", 80, 45)
    fern = Plant("Fern", 15, 120)
    print("\nTotal plants created: 5")
