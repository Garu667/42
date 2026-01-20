#! /usr/bin/env python3

class SecurePlant:
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
        return (f"{self.name} ({self.height}cm, {self.old} days)")

if __name__ == "__main__":
    print(f"=== Garden Security System ===")
    rose = SecurePlant("Rose")
    print(f"Plant created: {rose.name}")
    rose.set_height(25)
    rose.set_age(30)
    print(f"Height updated: {rose.get_height()} [OK]")
    print(f"Age updated: {rose.get_age()} [OK]")
    print()
    rose.set_height(-5)
    print()
    print(f"Current plant: {rose.get_info()}")
