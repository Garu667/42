from ex0 import AquaFactory
from ex0 import CreatureFactory
from ex0 import FlameFactory
from ex1 import HealingCreatureFactory
from ex1 import TransformCreatureFactory
from ex2 import AggressiveStrategy
from ex2 import BattleStrategy
from ex2 import DefensiveStrategy
from ex2 import InvalidStrategyCreatureError
from ex2 import NormalStrategy

Opponent = tuple[CreatureFactory, BattleStrategy]


def battle(opponent_a: Opponent, opponent_b: Opponent) -> bool:
    factory_a, strategy_a = opponent_a
    factory_b, strategy_b = opponent_b

    creature_a = factory_a.create_base()
    creature_b = factory_b.create_base()

    print("* Battle *")
    print(creature_a.describe())
    print("vs.")
    print(creature_b.describe())
    print("now fight!")

    try:
        for action in strategy_a.act(creature_a):
            print(action)
        for action in strategy_b.act(creature_b):
            print(action)
    except InvalidStrategyCreatureError as error:
        print(f"Battle error, aborting tournament: {error}")
        return False
    return True


def run_tournament(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved\n")

    for first_index, first_opponent in enumerate(opponents):
        for second_opponent in opponents[first_index + 1:]:
            if not battle(first_opponent, second_opponent):
                return


if __name__ == "__main__":
    tournament_0 = [
        (FlameFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ]
    print(
        "Tournament 0 (basic)\n",
        "[ (Flameling+Normal), (Healing+Defensive) ]",
    )
    run_tournament(tournament_0)

    tournament_1 = [
        (FlameFactory(), AggressiveStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ]
    print(
        "\nTournament 1 (error)\n",
        "[ (Flameling+Aggressive), (Healing+Defensive) ]",
    )
    run_tournament(tournament_1)

    tournament_2 = [
        (AquaFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy()),
    ]
    print(
        "\nTournament 2 (multiple)\n",
        "[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]",
    )
    run_tournament(tournament_2)
