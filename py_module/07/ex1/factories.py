from ex0.creatures import Creature
from ex0.factories import CreatureFactory
from ex1.creatures import Bloomelle
from ex1.creatures import Morphagon
from ex1.creatures import Shiftling
from ex1.creatures import Sproutling


class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Sproutling()

    def create_evolved(self) -> Creature:
        return Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Shiftling()

    def create_evolved(self) -> Creature:
        return Morphagon()
