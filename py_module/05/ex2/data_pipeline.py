from abc import ABC, abstractmethod
from typing import Any, List, Tuple
import typing


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


class ExportPlugin(typing.Protocol):
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        if not data:
            return
        print("CSV Output:")
        print(",".join(val for _, val in data))


class JSONExportPlugin:
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        if not data:
            return
        print("JSON Output:")
        parts = [f'"item_{rank}": "{val}"' for rank, val in data]
        print("{" + ", ".join(parts) + "}")


class DataStream:
    def __init__(self) -> None:
        self._processors: List[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: List[Any]) -> None:
        for element in stream:
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    break

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            to_export: List[Tuple[int, str]] = []
            for _ in range(nb):
                if proc.remaining > 0:
                    to_export.append(proc.output())
            if to_export:
                plugin.process_output(to_export)

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

    print("\nRegistering Processors")
    ds.register_processor(NumericProcessor("Numeric Processor"))
    ds.register_processor(TextProcessor("Text Processor"))
    ds.register_processor(LogProcessor("Log Processor"))

    batch1: List[Any] = [
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

    print(f"\nSend first batch of data on stream: {batch1}")
    ds.process_stream(batch1)
    ds.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    ds.output_pipeline(3, CSVExportPlugin())
    ds.print_processors_stats()

    batch2: List[Any] = [
        21,
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [
            {
                'log_level': 'ERROR',
                'log_message': '500 server crash'
            },
            {
                'log_level': 'NOTICE',
                'log_message': 'Certificate expires in 10 days'
            }
        ],
        [32, 42, 64, 84, 128, 168],
        'World hello'
    ]

    print(f"\nSend another batch of data: {batch2}")
    ds.process_stream(batch2)
    ds.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    ds.output_pipeline(5, JSONExportPlugin())
    ds.print_processors_stats()


if __name__ == "__main__":
    try:
        print("=== Code Nexus - Data Pipeline ===\n")
        main()
    except Exception as e:
        print(f"Error: {e}")
