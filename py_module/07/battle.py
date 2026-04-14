from ex0 import AquaFactory
from ex0 import CreatureFactory
from ex0 import FlameFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base_creature = factory.create_base()
    evolved_creature = factory.create_evolved()

    print(base_creature.describe())
    print(base_creature.attack())
    print(evolved_creature.describe())
    print(evolved_creature.attack())


def test_base_battle(
    left_factory: CreatureFactory,
    right_factory: CreatureFactory,
) -> None:
    print("Testing battle")
    left_creature = left_factory.create_base()
    right_creature = right_factory.create_base()

    print(left_creature.describe())
    print("vs.")
    print(right_creature.describe())
    print("fight!")
    print(left_creature.attack())
    print(right_creature.attack())


if __name__ == "__main__":
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()

    test_factory(flame_factory)
    print()
    test_factory(aqua_factory)
    print()
    test_base_battle(flame_factory, aqua_factory)
