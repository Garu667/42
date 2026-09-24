import json
from pathlib import Path
from typing import Callable

from pydantic import BaseModel, PrivateAttr

from src.constraints import NUMBER_CHARS, is_json_string_chunk
from src.models import VocabError


def _bytes_to_unicode() -> dict[int, str]:
    """Build the reversible byte-to-unicode map of byte-level BPE."""
    byte_values = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    code_points = list(byte_values)
    shift = 0
    for byte in range(256):
        if byte not in byte_values:
            byte_values.append(byte)
            code_points.append(256 + shift)
            shift += 1
    return {b: chr(c) for b, c in zip(byte_values, code_points)}


def _decode_token(raw: str, byte_of: dict[str, int]) -> str | None:
    """Decode a raw vocabulary key, or None if it is a special token."""
    try:
        data = bytes(byte_of[char] for char in raw)
    except KeyError:
        return None
    return data.decode("utf-8", errors="surrogateescape")


class Vocab(BaseModel):
    """The vocabulary, decoded once and indexed for the decoder."""

    texts: dict[int, str]

    _string_safe: frozenset[int] = PrivateAttr(default=frozenset())
    _numeric: frozenset[int] = PrivateAttr(default=frozenset())
    _starting: dict[str, frozenset[int]] = PrivateAttr(default_factory=dict)
    _containing: dict[str, frozenset[int]] = PrivateAttr(default_factory=dict)
    _prefixes: dict[str, frozenset[int]] = PrivateAttr(default_factory=dict)

    def model_post_init(self, context: object, /) -> None:
        """Precompute the candidate pools once, after validation."""
        self._string_safe = self._select(is_json_string_chunk)
        self._numeric = self._select(
            lambda text: bool(text) and set(text) <= NUMBER_CHARS
        )

    @property
    def string_safe(self) -> frozenset[int]:
        """The ids of the tokens that can sit inside a JSON string."""
        return self._string_safe

    @property
    def numeric(self) -> frozenset[int]:
        """The ids of the tokens made only of number characters."""
        return self._numeric

    def text_of(self, token_id: int) -> str:
        """Return the decoded text of a token, or raise VocabError."""
        try:
            return self.texts[token_id]
        except KeyError:
            raise VocabError(f"unknown token id {token_id}") from None

    def starting_with(self, prefix: str) -> frozenset[int]:
        """Return the ids whose text begins with the given prefix."""
        return self._cached(self._starting, prefix,
                            lambda text: text.startswith(prefix))

    def containing(self, char: str) -> frozenset[int]:
        """Return the ids whose text holds the given character."""
        return self._cached(self._containing, char,
                            lambda text: char in text)

    def prefixes_of(self, literal: str) -> frozenset[int]:
        """Return the ids whose text starts the given literal."""
        return self._cached(self._prefixes, literal,
                            lambda text: bool(text)
                            and literal.startswith(text))

    def _select(self, keep: Callable[[str], bool]) -> frozenset[int]:
        """Return the ids of every token whose text passes the test."""
        return frozenset(tid for tid, text in self.texts.items()
                         if keep(text))

    def _cached(
        self,
        cache: dict[str, frozenset[int]],
        key: str,
        keep: Callable[[str], bool],
    ) -> frozenset[int]:
        """Run a scan once per key, then serve it from the cache."""
        if key not in cache:
            cache[key] = self._select(keep)
        return cache[key]


def to_clean_str(text: str) -> str:
    """Replace any lone surrogate left by a partial UTF-8 token."""
    raw = text.encode("utf-8", errors="surrogateescape")
    return raw.decode("utf-8", errors="replace")


def load_vocab(path: str | Path) -> Vocab:
    """Read ``vocab.json`` and decode every token to readable text.

    Raises VocabError if the file is unreadable or not a mapping.
    """
    try:
        with open(path, encoding="utf-8") as stream:
            raw_vocab = json.load(stream)
    except OSError as err:
        raise VocabError(f"cannot read vocabulary '{path}': {err}") from err
    except json.JSONDecodeError as err:
        raise VocabError(f"vocabulary '{path}' is not valid JSON") from err

    if not isinstance(raw_vocab, dict) or not raw_vocab:
        raise VocabError(f"vocabulary '{path}' is not a token mapping")

    byte_of = {char: byte for byte, char in _bytes_to_unicode().items()}
    texts: dict[int, str] = {}
    for raw_token, token_id in raw_vocab.items():
        if not isinstance(raw_token, str) or not isinstance(token_id, int):
            raise VocabError(f"vocabulary '{path}' has a malformed entry")
        decoded = _decode_token(raw_token, byte_of)
        if decoded:
            texts[token_id] = decoded

    if not texts:
        raise VocabError(f"vocabulary '{path}' decoded to nothing")
    return Vocab(texts=texts)
