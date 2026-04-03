from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self._storage: List[Tuple[int, str]] = []
        self._global_counter: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> Tuple[int, str]:
        if not self._storage:
            raise IndexError("No data to output")
        return self._storage.pop(0)

    @property
    def remaining(self) -> int:
        return len(self._storage)


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
        items: List[Any] = data if isinstance(data, list) else [data]
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
        items: List[Any] = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._global_counter, item))
            self._global_counter += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def is_log_dict(d: Any) -> bool:
            return (
                isinstance(d, dict)
                and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in d.items()
                )
            )
        if is_log_dict(data):
            return True
        if isinstance(data, list):
            return all(is_log_dict(x) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        items: List[Any] = data if isinstance(data, list) else [data]
        for item in items:
            log_str = (
                f"{item.get('log_level', '')}: {item.get('log_message', '')}"
            )
            self._storage.append((self._global_counter, log_str))
            self._global_counter += 1


class DataStream:
    def __init__(self) -> None:
        self._processors: List[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: List[Any]) -> None:
        for element in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            if not handled:
                print(
                    f"DataStream error - "
                    f"Can't process element in stream: {element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            print(
                f"{proc.name}: total {proc._global_counter} items processed,"
                f" remaining {proc.remaining} on processor"
            )


def main() -> None:
    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    print()
    print("Registering Numeric Processor")
    num_proc = NumericProcessor("Numeric Processor")
    ds.register_processor(num_proc)

    batch: List[Any] = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {
                'log_level': 'WARNING',
                'log_message': 'Telnet access! Use ssh instead'
            },
            {
                'log_level': 'INFO',
                'log_message': 'User wil is connected'
            }
        ],
        42,
        ['Hi', 'five']
    ]

    print(f"Send first batch of data on stream: {batch}")
    ds.process_stream(batch)
    ds.print_processors_stats()

    print()
    print("Registering other data processors")
    ds.register_processor(TextProcessor("Text Processor"))
    ds.register_processor(LogProcessor("Log Processor"))
    print("Send the same batch again")
    ds.process_stream(batch)
    ds.print_processors_stats()

    print()
    print(
        "Consume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )
    for _ in range(3):
        num_proc.output()
    for _ in range(2):
        ds._processors[1].output()
    ds._processors[2].output()

    ds.print_processors_stats()


if __name__ == "__main__":
    try:
        print("=== Code Nexus - Data Stream ===\n")
        main()
    except Exception as e:
        print(f"Error: {e}")
