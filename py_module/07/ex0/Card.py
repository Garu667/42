from abc import ABC, abstractmethod
from typing import Dict
from enum import Enum


class Rarity(Enum):
    COMMON = "Common"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


class Card(ABC):
    def __init__(self, name: str, cost: int, rarity: Rarity | str):
        if isinstance(rarity, Rarity):
            rarity = Rarity(rarity).value

        self.info = {
            "name": name,
            "cost": cost,
            "rarity": rarity
        }

    @abstractmethod
    def play(self, game_state: Dict) -> Dict:
        pass

    def get_card_info(self) -> Dict:
        return self.info

    def is_playable(self, available_mana: int) -> bool:
        return self.info["cost"] <= available_mana
