from ex0.Card import Card, Rarity
from typing import Dict


class CreatureCard(Card):
    def __init__(
            self, name: str, cost: int, rarity: Rarity | str,
            attack: int, health: int):
        super().__init__(name, cost, rarity)
        self.info["type"] = "Creature"
        if attack <= 0:
            raise ValueError("attack can't be initialize as a negative value")
        self.info["attack"] = attack
        if health <= 0:
            raise ValueError("health can't be initialize as a negative value")
        self.info["health"] = health

    def play(self, game_state: dict) -> dict:
        play_result = {
            "card_played": game_state["card_wating"].info["name"],
            "mana_used": game_state["card_wating"].info["cost"],
            "effect": 'Creature summoned to battlefield',
        }
        return play_result

    def attack_target(self, target) -> Dict:
        target.info["health"] -= self.info["attack"]
        attack_result = {
            "attacker": self.info["name"],
            "target": target.info["name"],
            "damage_dealt": self.info["attack"],
            "combat_resolved": target.info["health"] <= 0
        }
        return attack_result
