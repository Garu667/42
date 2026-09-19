
class VocabError(Exception):
    ...
class UnsupportedTypeError(Exception):
    """Un paramètre utilise un type JSON que le décodeur ne gère pas."""

    def __init__(self, fn_name: str, param: str, type_name: str) -> None:
        super().__init__(
            f"function '{fn_name}': parameter '{param}' has unsupported "
            f"type '{type_name}' (expected integer, number, string or boolean)"
        )
