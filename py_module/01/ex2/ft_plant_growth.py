class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.__name: str = name
        self.__height: int = height
        self.__old: int = age

    def grow(self, length) -> None:
        self.__height += length

    def age(self, days) -> None:
        self.__old += days

    def get_info(self) -> None:
        print(f"{self.__name}: {self.__height}cm, {self.__old} days old")


if __name__ == "__main__":
    print(f"=== Day {0 + 1} ===")
    plant1 = Plant("Rose", 25, 30)
    plant1.get_info()
    plant1.grow(6)
    plant1.age(6)
    print(f"=== Day {1 + 6} ===")
    plant1.get_info()
    print("Growth this week: +6cm")
