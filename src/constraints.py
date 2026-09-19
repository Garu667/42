from dataclasses import dataclass
import re

_HEX = "0123456789abcdefABCDEF"
_JSON_TO_KIND = {
    "integer": "integer",
    "number": "number",
    "string": "string",
    "boolean": "boolean",
}

@dataclass
class Slot:
    """A slot that need to be filled by the model"""
    kind: str
    choices: list[str] | None = None

Segment = str | Slot

def _scan_string(partial: str) -> str | None:
    """État d'un préfixe de string JSON, ou None s'il est déjà invalide."""
    state, hexa = "start", 0
    for ch in partial:
        if state == "start":
            if ch != '"':
                return None
            state = "in"
        elif state == "in":
            if ch == '"':
                state = "done"
            elif ch == "\\":
                state = "esc"
            elif ch < " ":
                return None          # contrôle brut interdit en JSON
        elif state == "esc":
            if ch == "u":
                state, hexa = "hex", 0
            elif ch in '"\\/bfnrt':
                state = "in"
            else:
                return None
        elif state == "hex":
            if ch not in _HEX:
                return None
            hexa += 1
            if hexa == 4:
                state = "in"
        else:                        # "done" : rien ne peut suivre
            return None
    return state

def build_skeleton(fn: FunctionDefinition) -> list[Segment]:
    """Alternate between slots and literal
    Args:
        fn: The definition of the functions

    Returns:
        List of segments example:
        ['{"a": ', Slot('number'), ', "b": ', Slot('number'), '}'].

    Raises:
        UnsupportedTypeError: If a param has a type we don't handle
    """
    if not fn.parameters:
        return ["{}"]

    segments: list[Segment] = []
    for index, (name, spec) in enumerate(fn.parameters.items()):
        kind = _JSON_TO_KIND.get(spec.type)
        if kind is None:
            raise UnsupportedTypeError(fn.name, name, spec.type)
        separator = "{" if index == 0 else ", "
        segments.append(f'{separator}{json.dumps(name)}: ')
        segments.append(Slot(kind))
    segments.append("}")
    return segments

# TODO: precalc frozenset
def is_viable(slot: Slot, partial: str) -> bool:
    """This prefix can lead to a valid value of the good type ?"""
    if slot.kind == "enum":
        return any(c.startswith(partial) for c in (slot.choices or []))
    if slot.kind == "boolean":
        return "true".startswith(partial) or "false".startswith(partial)
    if slot.kind == "integer":
        return re.fullmatch(r"-?|-?0|-?[1-9][0-9]*", partial) is not None
    if slot.kind == "number":
        return re.fullmatch(r"-?((0|[1-9]\d*)(\.\d*)?)?", partial) is not None
    if slot.kind == "string":
        return _scan_string(partial) is not None
    return False

def is_complete(slot: Slot, partial: str) -> bool:
    """This prefix is already a finished valid value ?"""
    if slot.kind == "enum":
        return partial in (slot.choices or [])
    if slot.kind == "boolean":
        return partial in ("true", "false")
    if slot.kind == "integer":
        return re.fullmatch(r"-?(0|[1-9]\d*)", partial) is not None
    if slot.kind == "number":
        return re.fullmatch(r"-?(0|[1-9]\d*)\.\d+", partial) is not None
    if slot.kind == "string":
        return _scan_string(partial) == "done"
    return False

def allowed_token_ids(slot: Slot, partial: str, vocab: Vocab) -> set[int]:
    """Ids des tokens qui, ajoutés à `partial`, gardent la valeur viable."""
    return {tid for tid, text in vocab.items()
            if is_viable(slot, partial + text)}
