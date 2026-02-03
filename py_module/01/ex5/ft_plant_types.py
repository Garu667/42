#! /usr/bin/env python3

class Plant:
    def __init__(self, name = "Dirt"):
        self.name = name
        self.height = 0
        self.old = 0

    def set_height(self, height):
        if (height < 0):
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
        self.height += height

    def set_age(self, days):
        if (days < 0):
            print(f"Invalid operation attempted: age {days} days [REJECTED]")
            print("Security: Negative age rejected")
        self.old += days

    def get_height(self):
        return (f"{self.height}cm")
    def get_age(self):
        return (f"{self.old} days")

    def get_info(self):
        return (f"{self.name} (...): {self.height}cm, {self.old} days")

class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name)
        super().set_height(height)
        super().set_age(age)
        self.color = color
    def bloom(self):
        print(f"{self.name} is blooming beautifully!")
    def get_info(self):
        return (f"{self.name} (Flower): {self.height}cm, {self.old} days, {self.color} color")

class Tree(Plant):
    def __init__(self, name, height, age, trunk_diameter):
        super().__init__(name)
        super().set_height(height)
        super().set_age(age)
        self.trunk_diameter = trunk_diameter
    def produce_shade(self):
        shade_area = (self.trunk_diameter / 10) ** 2 * 3.14
        print(f"{self.name} provides {shade_area:.0f} square meters of shade")
    def get_info(self):
        return (f"{self.name} (Tree): {self.height}cm, {self.old} days, {self.trunk_diameter}cm diameter")

class Vegetable(Plant):
    def __init__(self, name, height, age, harvest_season, nutritional_value):
        super().__init__(name)
        super().set_height(height)
        super().set_age(age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value
    def get_info(self):
        return (f"{self.name} (Vegetable): {self.height}cm, {self.old} days, {self.harvest_season} harvest\nTomato is rich in vitamin {self.nutritional_value}")

if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    rose = Flower("Rose", 25, 30, "red")
    print(f"{rose.get_info()}")
    rose.bloom()
    print()
    oak = Tree("Oak", 500, 1825, 50)
    print(f"{oak.get_info()}")
    oak.produce_shade()
    print()
    tomate = Vegetable("Tomato", 80, 90, "summer", "C")
    print(f"{tomate.get_info()}")
