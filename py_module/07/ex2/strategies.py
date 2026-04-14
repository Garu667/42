from abc import ABC, abstractmethod

from ex0.creatures import Creature
from ex1.capabilities import HealCapability
from ex1.capabilities import TransformCapability


class InvalidStrategyCreatureError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        ...

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        ...


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        _ = creature
        return True

    def act(self, creature: Creature) -> list[str]:
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            message = (
                f"Invalid Creature '{creature.name}' "
                "for this aggressive strategy"
            )
            raise InvalidStrategyCreatureError(message)
        transformed_creature = creature
        assert isinstance(transformed_creature, TransformCapability)
        return [
            transformed_creature.transform(),
            creature.attack(),
            transformed_creature.revert(),
        ]


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            message = (
                f"Invalid Creature '{creature.name}' "
                "for this defensive strategy"
            )
            raise InvalidStrategyCreatureError(message)
        healing_creature = creature
        assert isinstance(healing_creature, HealCapability)
        return [
            creature.attack(),
            healing_creature.heal(),
        ]
