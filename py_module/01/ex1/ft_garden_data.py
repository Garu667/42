
#! /usr/bin/env python3

class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    plant1 = Plant("Rose", 25, 30)
    print(f"{plant1.name}: {plant1.height}cm, {plant1.age} days old");
    plant2 = Plant("Sunflower", 80, 45)
    print(f"{plant2.name}: {plant2.height}cm, {plant2.age} days old");
    plant3 = Plant("Cactus", 15, 120)
    print(f"{plant3.name}: {plant3.height}cm, {plant3.age} days old");
