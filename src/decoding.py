import json
from typing import Callable, Protocol

import numpy as np

from src.constraints import (
    NEUTRAL_VALUES,
    Segment,
    Slot,
    is_complete,
    is_viable,
)
from src.models import DecodingError, VocabError
from src.vocab import Vocab, to_clean_str

MAX_TOKENS_PER_SLOT = 64
MAX_TOKENS_PER_STRING = 48
MAX_SCALAR_CHARS = 24


class LogitsProvider(Protocol):
    """Minimal view of the SDK the decoder depends on."""

    def get_logits_from_input_ids(self, input_ids: list[int]) -> list[float]:
        """Return the next-token logits for the given context."""
        ...


Encoder = Callable[[str], list[int]]


def append_literal(
    input_ids: list[int],
    vocab: Vocab,
    encode: Encoder,
    literal: str,
) -> None:
    """Append a literal to the context, healing the token boundary.

    The last token is re-encoded with the literal so the merges the
    tokenizer would have made are preserved.
    """
    try:
        tail = vocab.text_of(input_ids[-1])
    except VocabError:
        input_ids.extend(encode(literal))
        return
    input_ids[-1:] = encode(tail + literal)


def allowed_token_ids(slot: Slot, partial: str,
                      vocab: Vocab) -> frozenset[int]:
    """Return the ids of the tokens that keep the value viable."""
    if slot.kind in ("number", "integer"):
        return frozenset(tid for tid in vocab.numeric
                         if is_viable(slot, partial + vocab.text_of(tid)))

    if slot.kind == "string":
        return vocab.string_safe

    return frozenset(tid for tid, text in vocab.texts.items()
                     if is_viable(slot, partial + text))


def _salvage(slot: Slot, partial: str) -> str:
    """Return the longest valid prefix of an unfinished value."""
    for size in range(len(partial), -1, -1):
        head = partial[:size]
        if is_complete(slot, head):
            return head
    if slot.kind == "enum":
        matching = [c for c in (slot.choices or []) if c.startswith(partial)]
        return (matching or slot.choices or [""])[0]
    return json.dumps(NEUTRAL_VALUES[slot.kind])


def _pick_token(
    model: LogitsProvider,
    input_ids: list[int],
    allowed: set[int],
) -> int:
    """Return the best allowed token, every other one masked to -inf.

    Raises DecodingError if no allowed token exists in the logits.
    """
    logits = np.asarray(model.get_logits_from_input_ids(input_ids),
                        dtype=np.float64)
    candidates = np.fromiter(
        (tid for tid in allowed if tid < logits.size), dtype=np.int64
    )
    if candidates.size == 0:
        raise DecodingError("no token can satisfy the constraint")

    masked = np.full(logits.shape, -np.inf, dtype=np.float64)
    masked[candidates] = logits[candidates]
    return int(np.argmax(masked))


SlotState = tuple[int, str, int]


def _advance(
    slot: Slot,
    next_literal: str,
    state: SlotState,
    text: str,
) -> SlotState | None:
    """Walk a candidate token through ``opening + value + next_literal``.

    Returns the state reached, or None if the token does not fit.
    """
    opening = slot.opening
    open_done, value, next_done = state
    for char in text:
        if open_done < len(opening):
            if char != opening[open_done]:
                return None
            open_done += 1
        elif next_done:
            if next_done >= len(next_literal) \
                    or char != next_literal[next_done]:
                return None
            next_done += 1
        elif (next_literal and char == next_literal[0]
                and not is_viable(slot, value + char)
                and is_complete(slot, value)):
            next_done = 1
        else:
            value += char
    if not next_done and not is_viable(slot, value):
        return None
    return open_done, value, next_done


def generate_slot(
    model: LogitsProvider,
    vocab: Vocab,
    input_ids: list[int],
    slot: Slot,
    next_literal: str,
) -> tuple[str, int]:
    """Fill one slot, token by token, under its type constraint.

    Returns the value and how many characters of ``next_literal`` the
    last token already wrote.
    """
    edge_ids = vocab.containing(next_literal[0]) if next_literal \
        else frozenset()

    budget = MAX_TOKENS_PER_STRING if slot.kind == "string" \
        else MAX_TOKENS_PER_SLOT
    state: SlotState = (0, "", 0)
    for _ in range(budget):
        open_done, value, _ = state
        if open_done < len(slot.opening):
            pool = (vocab.starting_with(slot.opening)
                    | vocab.prefixes_of(slot.opening))
        else:
            pool = allowed_token_ids(slot, value, vocab) | edge_ids
        moves: dict[int, SlotState] = {}
        for token_id in pool:
            reached = _advance(slot, next_literal, state,
                               vocab.text_of(token_id))
            if reached is not None:
                moves[token_id] = reached
        if not moves:
            break
        token_id = _pick_token(model, input_ids, set(moves))
        input_ids.append(token_id)
        state = moves[token_id]
        if state[2]:
            return state[1], state[2]
        if slot.kind != "string" and len(state[1]) >= MAX_SCALAR_CHARS:
            break
    return _salvage(slot, state[1]), 0


def fill_skeleton(
    model: LogitsProvider,
    vocab: Vocab,
    input_ids: list[int],
    skeleton: list[Segment],
    encode: Encoder,
) -> str:
    """Walk a skeleton, writing literals and generating slots."""
    produced: list[str] = []
    written = 0
    for index, segment in enumerate(skeleton):
        if isinstance(segment, str):
            pending = segment[written:]
            written = 0
            if pending:
                append_literal(input_ids, vocab, encode, pending)
            produced.append(segment)
            continue
        following = skeleton[index + 1]
        assert isinstance(following, str), "skeletons alternate"
        value, written = generate_slot(
            model, vocab, input_ids, segment, following
        )
        produced.append(segment.opening + value)
    return to_clean_str("".join(produced))
