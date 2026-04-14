from ex0.factories import CreatureFactory
from ex1 import HealingCreatureFactory
from ex1 import TransformCreatureFactory
from ex1.capabilities import HealCapability
from ex1.capabilities import TransformCapability


def test_healing_factory(factory: CreatureFactory) -> None:
    print("Testing Creature with healing capability")
    base_creature = factory.create_base()
    evolved_creature = factory.create_evolved()

    print("base:")
    print(base_creature.describe())
    print(base_creature.attack())
    if isinstance(base_creature, HealCapability):
        print(base_creature.heal())

    print("evolved:")
    print(evolved_creature.describe())
    print(evolved_creature.attack())
    if isinstance(evolved_creature, HealCapability):
        print(evolved_creature.heal())


def test_transform_factory(factory: CreatureFactory) -> None:
    print("Testing Creature with transform capability")
    base_creature = factory.create_base()
    evolved_creature = factory.create_evolved()

    print("base:")
    print(base_creature.describe())
    print(base_creature.attack())
    if isinstance(base_creature, TransformCapability):
        print(base_creature.transform())
        print(base_creature.attack())
        print(base_creature.revert())

    print("evolved:")
    print(evolved_creature.describe())
    print(evolved_creature.attack())
    if isinstance(evolved_creature, TransformCapability):
        print(evolved_creature.transform())
        print(evolved_creature.attack())
        print(evolved_creature.revert())


if __name__ == "__main__":
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    test_healing_factory(healing_factory)
    print()
    test_transform_factory(transform_factory)
