#! /usr/bin/env python3

class Plant:
    def __init__(self, name, height, old):
        self.name = name
        self.height = height
        self.old = old

    def grow(self, length):
        self.height += length

    def age(self, days):
        self.old += days

    def get_info(self):
        print(f"{self.name}: {self.height}cm, {self.old} days old")


if __name__ == "__main__":
    print(f"=== Day {0 + 1} ===")
    plant1 = Plant("Rose", 25, 30)
    plant1.get_info()
    plant1.grow(6)
    plant1.age(6)
    print(f"=== Day {1 + 6} ===")
    plant1.get_info()
    print("Growth this week: +6cm")
