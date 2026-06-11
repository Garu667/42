from sys import argv
from pydantic import ValidationError
from src.parsing import Parsing, MissingKeyError
from src.parsing import PositionError, FileNameError


def list_to_dict(data: list[str]) -> dict[str, str]:
    config: dict[str, str] = {}
    for element in data:
        if '#' in element:
            element = element.split('#', 1)[0].strip()
        pair = element.split("=", 1)
        if len(pair) == 2:
            config[pair[0].strip()] = pair[1].strip()
    return config


def main(argv: list[str]) -> None:
    if len(argv) == 1:
        print("You must add the config file")
        print("python3 a_maze_ing.py <file_name.txt> OR make run")
        return
    if not argv[1].endswith(".txt"):
        print("You must use a text file (exemple: config.txt)")
        return


if __name__ == "__main__":
    try:
        main(argv)
    except Exception as e:
        print(e)
