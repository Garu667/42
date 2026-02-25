class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.__name: str = name
        self.__height: int = height
        self.__old: int = age

    def get_height(self) -> int:
        return self.__height

    def get_age(self) -> int:
        return self.__old

    def get_name(self) -> str:
        return self.__name

    def get_info(self) -> None:
        print(f" - {self.__name}: {self.__height}cm")

    def grow(self, height: int) -> None:
        if (height < 0):
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
            return
        self.__height += height
        print(f"{self.get_name()} grew {height}cm")

    def set_age(self, days: int) -> None:
        if (days < 0):
            print(f"Invalid operation attempted: age {days} days [REJECTED]")
            print("Security: Negative age rejected")
            return
        self.__old += days
        print(f"Age updated: {self.get_age()} days [OK]")


class FloweringPlant(Plant):
    def __init__(self, name: str, height: int, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self._color: str = color
        self._bloom: bool = 0

    def get_color(self) -> None:
        return self._color

    def bloom(self) -> None:
        self._bloom = 1

    def get_info(self) -> None:
        print(f" - {self.get_name()}: {self.get_height()}cm, \
{self.get_color()} flowers", end="")
        if (self._bloom == 1):
            print(" (blooming)")
        else:
            print()


class PrizeFlower(FloweringPlant):
    def __init__(
            self, name: str, height: int, age: int, color: str, prize: int
            ) -> None:
        super().__init__(name, height, age, color)
        self._prize: int = prize

    def get_price(self) -> int:
        return self._prize

    def change_price(self, cost: int) -> None:
        if (cost < 0):
            print("Can't put negative cost [REJECTED]")
            return
        self._prize = cost

    def get_info(self) -> None:
        print(f" - {self.get_name()}: {self.get_height()}cm, \
{self.get_color()} flowers", end="")
        if (self._bloom == 1):
            print(" (blooming)", end="")
        print(f", Prize points: {self._prize}")


class Garden:
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._growth: int = 0
        self._plants = []

    def add_plant(self, plant: Plant) -> None:
        self._plants.append(plant)
        print(f"Added {plant.get_name()} to {self._name}'s garden")

    def get_name(self) -> str:
        return self._name

    def get_plants(self) -> list[Plant]:
        return self._plants

    def grow_all(self, value: int) -> None:
        print(f"{self._name} is helping all plants grow...")
        for p in self._plants:
            self._growth += value
            p.grow(value)

    def garden_info(self) -> None:
        print("Plants in garden:")
        for p in self._plants:
            p.get_info()

    def garden_inventory(self) -> None:
        plant: int = 0
        prizes: int = 0
        flowers: int = 0
        for p in self._plants:
            if isinstance(p, PrizeFlower):
                prizes += 1
            elif isinstance(p, FloweringPlant):
                flowers += 1
            elif isinstance(p, Plant):
                plant += 1
        print(f"Plant types: {plant} regular, {flowers} flowering, \
{prizes} prize flowers")

    def garden_report(self) -> None:
        print(f"=== {self.get_name()}'s Garden Report ===")
        self.garden_info()
        print()
        i: int = 0
        for p in self._plants:
            i += 1
        print(f"Plants added: {i}, Total growth: {self._growth}cm")
        self.garden_inventory()


class GardenManager:
    def __init__(self) -> None:
        self._gardens: list[Garden] = []

    def get_gardens(self) -> list[Garden]:
        return self._gardens

    @staticmethod
    def validate_name(name: str) -> bool:
        return len(name) > 0

    def add_garden(self, garden: Garden) -> None:
        if self.validate_name(garden.get_name()) == 0:
            return
        self._gardens.append(garden)

    @classmethod
    def create_garden_network(cls, name: str) -> GardenManager:
        manager = cls()
        manager.add_garden(Garden(name))
        return manager

    class GardenStats:

        @staticmethod
        def height_test(plants) -> bool:
            for p in plants:
                if p.get_height() <= 0:
                    return False
            return True

        @staticmethod
        def score_test(plants) -> int:
            score: int = 0

            for p in plants:
                score += 10
                score += p.get_height()
                if (isinstance(p, PrizeFlower)):
                    score += p.get_price()
            return score

        @staticmethod
        def count_gardens(manager) -> int:
            count: int = 0
            for g in manager.get_gardens():
                count += 1
            return count

        @staticmethod
        def garden_tests(manager) -> None:
            score: int = 0
            h: bool = False
            print("Height validation test:", end="")
            for garden in manager.get_gardens():
                h = GardenManager.GardenStats.height_test(garden.get_plants())
                if h is False:
                    print(" False")
            print(" True")
            print("Garden scores -", end="")
            first: bool = True
            for garden in manager.get_gardens():
                score = GardenManager.GardenStats.\
                    score_test(garden.get_plants())
                if not first:
                    print(",", end="")
                print(f" {garden.get_name()}: {score}", end="")
                first = False
            print(f"\nTotal gardens managed: \
{GardenManager.GardenStats.count_gardens(manager)}")


def main() -> None:
    print("=== Garden Management System Demo ===")
    manager = GardenManager.create_garden_network("Alice")
    stats = GardenManager.GardenStats()
    alice = manager.get_gardens()[0]
    bob = Garden("Bob")
    manager.add_garden(bob)
    print()

    oak = Plant("Oak Tree", 100, 50)
    rose = FloweringPlant("Rose", 25, 30, "red")
    iris = FloweringPlant("Iris", 30, 20, "blue")
    violete = FloweringPlant("Violete", 40, 30, "violet")
    sunflower = PrizeFlower("Sunflower", 50, 90, "yellow", 10)

    alice.add_plant(oak)
    alice.add_plant(rose)
    alice.add_plant(sunflower)
    bob.add_plant(violete)
    bob.add_plant(iris)
    print()

    alice.grow_all(1)
    bob.grow_all(1)
    rose.bloom()
    sunflower.bloom()
    print()

    alice.garden_report()
    print()

    stats.garden_tests(manager)


if __name__ == "__main__":
    main()
