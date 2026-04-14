from abc import ABC, abstractmethod


class HealCapability(ABC):
    @abstractmethod
    def heal(self, target: str | None = None) -> str:
        ...


class TransformCapability(ABC):
    def __init__(self) -> None:
        self._is_transformed = False

    @property
    def is_transformed(self) -> bool:
        return self._is_transformed

    @abstractmethod
    def transform(self) -> str:
        ...

    @abstractmethod
    def revert(self) -> str:
        ...
