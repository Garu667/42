class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.__name: str = name
        self.__height: int = height
        self.__old: int = age

    def get_height(self) -> int:
        return (self.__height)

    def get_age(self) -> int:
        return (self.__old)

    def get_name(self) -> str:
        return (self.__name)

    def get_info(self) -> None:
        print(f"{self.__name}: {self.__height}cm, {self.__old} days old")

    def grow(self, height: int) -> None:
        if (height < 0):
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
            return
        self.__height += height
        print(f"Height updated: {self.__height}cm [OK]")

    def set_age(self, days: int) -> None:
        if (days < 0):
            print(f"Invalid operation attempted: age {days} days [REJECTED]")
            print("Security: Negative age rejected")
            return
        self.__old += days
        print(f"Age updated: {self.__old} days [OK]")


class Flower(Plant):
    def __init__(self, name: str, height: int, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self.__color: str = color

    def bloom(self) -> None:
        print(f"{self.get_name()} is blooming beautifully!")

    def get_info(self) -> None:
        print(f"{self.get_name()} (Flower): {self.get_height()}cm, \
{self.get_age()} days, {self.__color} color")


class Tree(Plant):
    def __init__(self, name: str, height: int, age: int, trunk: int) -> None:
        super().__init__(name, height, age)
        self.__trunk_diameter: int = trunk

    def produce_shade(self) -> None:
        shade_area: float = (self.__trunk_diameter / 10) ** 2 * 3.14
        print(f"{self.get_name()} provides {shade_area:.0f} \
square meters of shade")

    def get_info(self) -> None:
        print(f"{self.get_name()} (Tree): {self.get_height()}cm, \
{self.get_age()} days, {self.__trunk_diameter}cm diameter")


class Vegetable(Plant):
    def __init__(self, name: str, h: int, age: int, s: str, n: str) -> None:
        super().__init__(name, h, age)
        self.__harvest_season = s
        self.__nutritional_value = n

    def get_info(self) -> None:
        print(f"{self.get_name()} (Vegetable): {self.get_height()}cm,\
 {self.get_age()} days, {self.__harvest_season} harvest")

    def get_nutritional_value(self) -> None:
        print(f"Tomato is rich in vitamin {self.__nutritional_value}")


if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    print()
    rose = Flower("Rose", 25, 30, "red")
    rose.get_info()
    rose.bloom()
    print()
    oak = Tree("Oak", 500, 1825, 50)
    oak.get_info()
    oak.produce_shade()
    print()
    tomate = Vegetable("Tomato", 80, 90, "summer", "C")
    tomate.get_info()
    tomate.get_nutritional_value()
