#! /usr/bin/env python3

class Plant:
    def __init__(self, name = "Rose", height = 25, old = 30):
        self.name = name
        self.height = height
        self.old = old

    def grow(self, length):
        self.height += length

    def age(self, days):
        self.old += days

    def get_info(self):
        return (f"{self.name} ({self.height}cm, {self.old} days)")


if __name__ == "__main__":
    print(f"=== Plant Factory Output ===")
    rose = Plant()
    print("Created: ", rose.get_info())
    oak = Plant("Oak", 200, 365)
    print("Created: ", oak.get_info())
    cactus = Plant("Cactus", 5, 90)
    print("Created: ", cactus.get_info())
    sunflower = Plant("Sunflower", 80, 45)
    print("Created: ", sunflower.get_info())
    fern = Plant("Fern", 15, 120)
    print("Created: ", fern.get_info())

    print("Total plants created: 5")
