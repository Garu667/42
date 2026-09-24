import json
import re
from typing import Any

from pydantic import BaseModel

from src.models import FunctionDefinition, UnsupportedTypeError

INTEGER = re.compile(r"-?(0|[1-9]\d*)")
INTEGER_PREFIX = re.compile(r"-?(0|[1-9]\d*)?")
NUMBER = re.compile(r"-?(0|[1-9]\d*)(\.\d+)?")
NUMBER_PREFIX = re.compile(r"-?((0|[1-9]\d*)(\.\d*)?)?")

NUMBER_CHARS = frozenset("0123456789.-")

_SIMPLE_ESCAPES = set('"\\/bfnrt')
_HEX_DIGITS = set("0123456789abcdefABCDEF")

NEUTRAL_VALUES: dict[str, Any] = {
    "integer": 0, "number": 0.0, "string": "", "boolean": False,
}
_SUPPORTED = frozenset(NEUTRAL_VALUES)


def is_json_string_chunk(text: str) -> bool:
    """Tell whether the text can sit inside a JSON string as-is.

    The text is JSON *source*, so ``\\"`` is legal while a bare ``"``
    closes the value. A chunk must start and end outside an escape.
    """
    index = 0
    while index < len(text):
        char = text[index]
        if char == '"' or char < " " or char == "\x7f":
            return False
        if char == "\\":
            index += 1
            if index >= len(text):
                return False
            escape = text[index]
            if escape == "u":
                digits = text[index + 1:index + 5]
                if len(digits) < 4 or not all(d in _HEX_DIGITS
                                              for d in digits):
                    return False
                index += 4
            elif escape not in _SIMPLE_ESCAPES:
                return False
        index += 1
    return True


class Slot(BaseModel):
    """A hole the model fills, plus the punctuation introducing it."""

    kind: str
    choices: list[str] | None = None
    opening: str = ""


Segment = str | Slot


def build_skeleton(fn: FunctionDefinition) -> list[Segment]:
    """Split a call body into literals and typed slots.

    Raises UnsupportedTypeError if a parameter type is not handled.
    """
    if not fn.parameters:
        return ["{}"]

    segments: list[Segment] = []
    literal = "{"
    for index, (name, spec) in enumerate(fn.parameters.items()):
        kind = spec.type
        if kind not in _SUPPORTED:
            raise UnsupportedTypeError(fn.name, name, kind)
        if index:
            literal += ", "
        literal += f'{json.dumps(name)}:'
        if kind == "string":
            segments.append(literal)
            segments.append(Slot(kind=kind, opening=' "'))
            literal = '"'
        else:
            segments.append(literal + " ")
            segments.append(Slot(kind=kind))
            literal = ""
    segments.append(literal + "}")
    return segments


def is_viable(slot: Slot, partial: str) -> bool:
    """Tell whether the prefix can still grow into a valid value."""
    if slot.kind == "enum":
        return any(c.startswith(partial) for c in (slot.choices or []))
    if slot.kind == "boolean":
        return "true".startswith(partial) or "false".startswith(partial)
    if slot.kind == "integer":
        return INTEGER_PREFIX.fullmatch(partial) is not None
    if slot.kind == "number":
        return NUMBER_PREFIX.fullmatch(partial) is not None
    if slot.kind == "string":
        return is_json_string_chunk(partial)
    return False


def is_complete(slot: Slot, partial: str) -> bool:
    """Tell whether the prefix is already a finished valid value."""
    if slot.kind == "enum":
        return partial in (slot.choices or [])
    if slot.kind == "boolean":
        return partial in ("true", "false")
    if slot.kind == "integer":
        return INTEGER.fullmatch(partial) is not None
    if slot.kind == "number":
        return NUMBER.fullmatch(partial) is not None
    if slot.kind == "string":
        return is_json_string_chunk(partial)
    return False
