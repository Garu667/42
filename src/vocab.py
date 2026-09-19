"""Vocabulary loading and token helpers for constrained decoding.

The model uses a byte-level BPE tokenizer: ``vocab.json`` maps a token
string to its id, but that string is *not* readable text. Every raw byte
has been remapped to a printable unicode character (a space becomes
``\u0120``, a newline ``\u010a``, and so on) so that the vocabulary file
stays valid JSON. This module undoes that mapping once, at load time, so
that the rest of the project only ever manipulates ordinary strings.
"""

import json
from pathlib import Path

from pydantic import BaseModel

from src.errors import VocabError

_STRING_UNSAFE = {'"', "\\"}
_NUMERIC_CHARS = set("0123456789.-eE+")


def _bytes_to_unicode() -> dict[int, str]:
    """Build the reversible byte to unicode map used by byte-level BPE.

    Returns:
        A mapping of the 256 byte values to distinct printable characters.
    """
    # clé : les octets déjà imprimables se représentent eux-mêmes, les
    # autres sont décalés au-dessus de 255 pour rester affichables.
    byte_values = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("\u00a1"), ord("\u00ac") + 1))
        + list(range(ord("\u00ae"), ord("\u00ff") + 1))
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
    """Turn a raw vocabulary key into readable text.

    Args:
        raw: The token as written in ``vocab.json``.
        byte_of: Reverse of :func:`_bytes_to_unicode`.

    Returns:
        The decoded text, or None if the key uses characters outside the
        byte-level alphabet (added special tokens, for instance).
    """
    try:
        data = bytes(byte_of[char] for char in raw)
    except KeyError:
        return None
    # clé : un token peut couper un caractère UTF-8 en deux. surrogate-
    # escape garde ces octets orphelins dans la chaîne au lieu de lever.
    return data.decode("utf-8", errors="surrogateescape")


def _is_string_safe(text: str) -> bool:
    """Tell whether a token can appear as-is inside a JSON string."""
    if any(char in _STRING_UNSAFE for char in text):
        return False
    return all(char >= " " and char != "\x7f" for char in text)


class Vocab(BaseModel):
    """
    ...
    """

    texts: dict[int, str]
    string_safe: frozenset[int] = frozenset()
    string_special: frozenset[int] = frozenset()
    numeric: frozenset[int] = frozenset()

    def model_post_init(self, context: object, /) -> None:
        """Precompute the two candidate pools once, after validation."""

        self.string_safe = frozenset(
            tid for tid, text in self.texts.items()
            if _is_string_safe(text)
        )
        self.string_special = frozenset(self.texts) - self.string_safe
        self.numeric = frozenset(
            tid for tid, text in self.texts.items()
            if text and all(char in _NUMERIC_CHARS for char in text)
        )

    def items(self) -> list[tuple[int, str]]:
        """Return every (id, text) pair, for exhaustive scans."""
        return list(self.texts.items())

    def text_of(self, token_id: int) -> str:
        """Return the decoded text of a token.

        Raises:
            VocabError: If the id is not part of the vocabulary.
        """
        try:
            return self.texts[token_id]
        except KeyError:
            raise VocabError(f"unknown token id {token_id}") from None

    def prefixes_of(self, literal: str) -> set[int]:
        """Return the ids whose text starts the given literal.

        Used to let a slot end: once its value is complete, the tokens
        opening the next literal become allowed alongside it.
        """
        return {
            tid for tid, text in self.texts.items()
            if text and literal.startswith(text)
        }

    def join(self, token_ids: list[int]) -> str:
        """Concatenate the texts of the given tokens."""
        return "".join(self.text_of(tid) for tid in token_ids)


def to_clean_str(text: str) -> str:
    """..."""
    raw = text.encode("utf-8", errors="surrogateescape")
    return raw.decode("utf-8", errors="replace")


def load_vocab(path: str | Path) -> Vocab:
    """
    ...
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
    # clé : le fichier est {token: id}, on l'inverse en {id: texte}.
    for raw_token, token_id in raw_vocab.items():
        if not isinstance(raw_token, str) or not isinstance(token_id, int):
            raise VocabError(f"vocabulary '{path}' has a malformed entry")
        decoded = _decode_token(raw_token, byte_of)
        if decoded is not None:
            texts[token_id] = decoded

    if not texts:
        raise VocabError(f"vocabulary '{path}' decoded to nothing")
    return Vocab(texts=texts)
