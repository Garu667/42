from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: List[Tuple[int, str]] = []
        self._global_counter: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Vérifie si les données sont appropriées pour ce processeur."""
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Traite et stocke les données avec leur rang."""
        pass

    def output(self) -> Tuple[int, str]:
        """Extrait et retire la donnée la plus ancienne."""
        if not self._storage:
            raise IndexError("No data to output")
        return self._storage.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._global_counter, str(item)))
            self._global_counter += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._global_counter, item))
            self._global_counter += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def is_log_dict(d: Any) -> bool:
            return (isinstance(d, dict) and
                    all(isinstance(k, str) and
                    isinstance(v, str) for k, v in d.items()))

        if is_log_dict(data):
            return True
        if isinstance(data, list):
            return all(is_log_dict(x) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            log_str = f"{item.get('log_level', '')}:"
            f"{item.get('log_message', '')}"
            self._storage.append((self._global_counter, log_str))
            self._global_counter += 1


def main() -> None:
    num_proc = NumericProcessor()
    print("Testing Numeric Processor...")
    print(f"Trying to validate input '42': {num_proc.validate(42)}")
    print(f"Trying to validate input 'Hello': {num_proc.validate('Hello')}")

    try:
        print("Test invalid ingestion of string 'foo'"
              " without prior validation:")
        num_proc.ingest("foo")
    except Exception as e:
        print(f"Got exception: {e}")

    print("Processing data: [1, 2, 3, 4, 5]")
    num_proc.ingest([1, 2, 3, 4, 5])

    print("Extracting 3 values...")
    for _ in range(3):
        rank, val = num_proc.output()
        print(f"Numeric value {rank}: ", end="")
        print(val)

    print("\nTesting Text Processor...")
    text_proc = TextProcessor()
    print(f"Trying to validate input '42': {text_proc.validate(42)}")
    print("Processing data: ['Hello', 'Nexus', 'World']")
    text_proc.ingest(['Hello', 'Nexus', 'World'])
    rank, val = text_proc.output()
    print(f"Extracting 1 value...\nText value {rank}: {val}")

    print("\nTesting Log Processor...")
    log_proc = LogProcessor()
    print(f"Trying to validate input 'Hello': {log_proc.validate('Hello')}")
    log_data = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!!'}
    ]
    print(f"Processing data: {log_data}")
    log_proc.ingest(log_data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, val = log_proc.output()
        print(f"Log entry {rank}: {val}")


if __name__ == "__main__":
    try:
        print("=== Code Nexus - Data Processor ===\n")
        main()
    except Exception as e:
        print(f"Error: {e}")
