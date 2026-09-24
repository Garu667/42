from src.vocab import Vocab

_SINGLE_CHARS = ["\n"] + [chr(code) for code in range(32, 127)] + list("éàü€")
_MERGED = [
    ' "', '", ', '": ', '"}', '")', "40", "345", ".5", "true", "false",
    "shrek", "hello", "\\\\", '\\"', "fn_", "add", "_numbers",
]


def make_vocab() -> Vocab:
    """Build a tiny vocabulary: every printable char plus a few merges."""
    return Vocab(texts=dict(enumerate(_SINGLE_CHARS + _MERGED)))


class GreedyEncoder:
    """Tokenize by always taking the longest matching token."""

    def __init__(self, vocab: Vocab) -> None:
        """Index the tokens by text, longest first."""
        self._by_text = {text: tid for tid, text in vocab.texts.items()}
        self._longest = max(len(text) for text in self._by_text)

    def __call__(self, text: str) -> list[int]:
        """Return the ids of the text."""
        ids: list[int] = []
        index = 0
        while index < len(text):
            for size in range(min(self._longest, len(text) - index), 0, -1):
                tid = self._by_text.get(text[index:index + size])
                if tid is not None:
                    ids.append(tid)
                    index += size
                    break
            else:
                raise ValueError(f"cannot encode {text[index]!r}")
        return ids


class ScriptedModel:
    """A model that always wants to write one given text.

    Every token that continues ``target`` from the current context is
    scored by its length; any other token gets a score of zero.
    """

    def __init__(self, vocab: Vocab, target: str) -> None:
        """Remember the text the model wants to produce."""
        self._vocab = vocab
        self._target = target
        self._size = max(vocab.texts) + 1

    def get_logits_from_input_ids(self, input_ids: list[int]) -> list[float]:
        """Favour the longest token that stays on the scripted text."""
        context = "".join(self._vocab.texts[tid] for tid in input_ids)
        logits = [0.0] * self._size
        if not self._target.startswith(context):
            return logits
        rest = self._target[len(context):]
        for tid, text in self._vocab.texts.items():
            if rest.startswith(text):
                logits[tid] = float(len(text))
        return logits
