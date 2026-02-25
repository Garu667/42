class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name: str = name
        self.height: int = height
        self.old: int = age


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    rose = Plant("Rose", 25, 30)
    print(f"{rose.name}: {rose.height}cm, {rose.old} days old")
    sunflower = Plant("Sunflower", 80, 45)
    print(f"{sunflower.name}: {sunflower.height}cm, {sunflower.old} days old")
    cactus = Plant("Cactus", 15, 120)
    print(f"{cactus.name}: {cactus.height}cm, {cactus.old} days old")
