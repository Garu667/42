from typing import Any

from pydantic import BaseModel


class ParameterSpec(BaseModel):
    """The declared type of one parameter or of a return value."""

    type: str


class FunctionDefinition(BaseModel):
    """One callable function, as described in the definition file."""

    name: str
    description: str = ""
    parameters: dict[str, ParameterSpec] = {}


class TestCase(BaseModel):
    """One natural-language request to translate into a call."""

    prompt: str


class FunctionCall(BaseModel):
    """One line of the output file: exactly the three expected keys."""

    prompt: str
    name: str
    parameters: dict[str, Any]


class CallMeMaybeError(Exception):
    """Base class for every error this program raises on purpose."""


class InputError(CallMeMaybeError):
    """An input file is missing, unreadable, or badly shaped."""


class OutputError(CallMeMaybeError):
    """The output file cannot be written."""


class VocabError(CallMeMaybeError):
    """The vocabulary file cannot be read or decoded."""


class ModelError(CallMeMaybeError):
    """The model cannot be loaded or queried."""


class DecodingError(CallMeMaybeError):
    """The constrained decoder cannot produce a value."""


class UnsupportedTypeError(CallMeMaybeError):
    """A parameter uses a JSON type the decoder does not handle."""

    def __init__(self, fn_name: str, param: str, type_name: str) -> None:
        """Build the message naming the offending parameter."""
        super().__init__(
            f"function '{fn_name}': parameter '{param}' has unsupported "
            f"type '{type_name}' (expected integer, number, string or boolean)"
        )
