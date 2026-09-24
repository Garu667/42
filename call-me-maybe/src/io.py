import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from src.models import (
    FunctionCall,
    FunctionDefinition,
    InputError,
    OutputError,
    TestCase,
)


def _load_json(path: str | Path) -> Any:
    """Read a JSON file, turning every failure into an InputError."""
    try:
        with open(path, encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError:
        raise InputError(f"input file '{path}' does not exist") from None
    except OSError as err:
        raise InputError(f"cannot read '{path}': {err}") from err
    except json.JSONDecodeError as err:
        raise InputError(
            f"'{path}' is not valid JSON (line {err.lineno}: {err.msg})"
        ) from err


def load_functions(path: str | Path) -> list[FunctionDefinition]:
    """Load the function definitions, in file order.

    Raises InputError if the file holds no valid function.
    """
    raw = _load_json(path)
    if not isinstance(raw, list) or not raw:
        raise InputError(f"'{path}' must hold a non-empty JSON array")

    functions: list[FunctionDefinition] = []
    seen: set[str] = set()
    for index, entry in enumerate(raw):
        try:
            function = FunctionDefinition.model_validate(entry)
        except ValidationError as err:
            raise InputError(
                f"'{path}' entry {index} is not a valid function: "
                f"{err.error_count()} problem(s), first at "
                f"{err.errors()[0]['loc']}"
            ) from err
        if function.name in seen:
            raise InputError(f"'{path}' declares '{function.name}' twice")
        seen.add(function.name)
        functions.append(function)
    return functions


def load_tests(path: str | Path) -> list[TestCase]:
    """Load the prompts to process, in file order.

    Raises InputError if an entry has no usable 'prompt'.
    """
    raw = _load_json(path)
    if not isinstance(raw, list):
        raise InputError(f"'{path}' must hold a JSON array")

    tests: list[TestCase] = []
    for index, entry in enumerate(raw):
        try:
            tests.append(TestCase.model_validate(entry))
        except ValidationError:
            raise InputError(
                f"'{path}' entry {index} has no usable 'prompt' field"
            ) from None
    return tests


def write_results(path: str | Path, results: list[FunctionCall]) -> None:
    """Write the calls as a JSON array, creating the directory if needed.

    Raises OutputError if the file cannot be written.
    """
    destination = Path(path)
    payload = [result.model_dump() for result in results]
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
    except OSError as err:
        raise OutputError(f"cannot write '{destination}': {err}") from err
