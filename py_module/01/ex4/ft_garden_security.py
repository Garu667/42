class SecurePlant:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        self.__height: int = 0
        self.__old: int = 0
        print(f"Plant created: {self.__name}")

    def get_height(self) -> int:
        return (self.__height)

    def get_age(self) -> int:
        return (self.__old)

    def get_info(self) -> None:
        print(f"Current plant: {self.__name} ({self.__height}cm, \
{self.__old} days)")

    def add_height(self, height) -> None:
        if (height < 0):
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
            return
        self.__height += height
        print(f"Height updated: {self.__height}cm [OK]")

    def set_age(self, days) -> None:
        if (days < 0):
            print(f"Invalid operation attempted: age {days} days [REJECTED]")
            print("Security: Negative age rejected")
            return
        self.__old += days
        print(f"Age updated: {self.__old} days [OK]")


if __name__ == "__main__":
    print("=== Garden Security System ===")
    rose = SecurePlant("Rose")
    rose.add_height(25)
    rose.set_age(30)
    print()
    rose.add_height(-5)
    print()
    rose.get_info()
