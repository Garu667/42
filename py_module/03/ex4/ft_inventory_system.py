import sys


usage: str = f"Usage: python3 {sys.argv[0]} <item:value> <item:value> ..."


def parsing(av: list[str]) -> dict[str, int]:
    av_dict: dict[str, int] = {}
    for item in av[1:]:
        if ":" not in item:
            print(f"Error - invalid parameter '{item}'")
            continue
        parse = item.split(":")
        if parse[0] in av_dict:
            print(f"Redundant item '{parse[0]}' - discarding")
            continue
        try:
            quantity: int = int(parse[1])
        except ValueError:
            print(f"Quantity error for '{parse[0]}': "
                  f"invalid literal for int() with base 10: '{parse[1]}'")
            continue
        av_dict[parse[0]] = quantity
    return av_dict


def inventory_stats(inventory: dict[str, int]) -> None:
    print(f"Got inventory: {inventory}")
    print(f"Item list: {list(inventory.keys())}")
    print(f"Total quantity of the {len(inventory)} items: "
          f"{sum(inventory.values())}")
    for item in inventory:
        print(f"Item {item} represents "
              f"{round(inventory[item] / sum(inventory.values()) * 100, 1)}%")
    most = max(inventory, key=lambda item: inventory[item])
    least = min(inventory, key=lambda item: inventory[item])
    print(f"Item most abundant: {most} with quantity {inventory[most]}")
    print(f"Item least abundant: {least} with quantity {inventory[least]}")


def main(ac: int, av: list[str]) -> None:
    if ac == 1:
        print(usage)
        return
    inventory: dict[str, int] = parsing(av)
    inventory_stats(inventory)
    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    print("=== Inventory System Analysis ===")
    main(len(sys.argv), sys.argv)
