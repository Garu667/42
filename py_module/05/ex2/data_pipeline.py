from abc import ABC, abstractmethod
from typing import Any, List, Tuple, Union, Protocol, Dict


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self._storage: List[Tuple[int, str]] = []
        self.total_processed = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> Tuple[int, str]:
        if self._storage:
            return self._storage.pop(0)
        return (-1, "")

    @property
    def remaining(self) -> int:
        return len(self._storage)

class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return isinstance(data, (int, float)) or (isinstance(data, list) and all(isinstance(x, (int, float)) for x in data))
    
    def ingest(self, data: Any) -> None:
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self.total_processed, str(item)))
            self.total_processed += 1

class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return isinstance(data, str) or (isinstance(data, list) and all(isinstance(x, str) for x in data))
    
    def ingest(self, data: Any) -> None:
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self.total_processed, item))
            self.total_processed += 1

class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        is_dict = lambda d: isinstance(d, dict) and "log_level" in d
        return is_dict(data) or (isinstance(data, list) and all(is_dict(x) for x in data))
    
    def ingest(self, data: Any) -> None:
        items = data if isinstance(data, list) else [data]
        for item in items:
            log_str = f"{item.get('log_level')}: {item.get('log_message')}"
            self._storage.append((self.total_processed, log_str))
            self.total_processed += 1


class ExportPlugin(Protocol):
    """Contrainte pour les plugins d'export via duck typing."""
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        ...

class CSVExportPlugin:
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        if not data: return
        print("CSV Output:")
        values = [val for _, val in data]
        print(",".join(values))

class JSONExportPlugin:
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        if not data: return
        print("JSON Output:")
        json_parts = [f'"item_{rank}": "{val}"' for rank, val in data]
        print("{" + ", ".join(json_parts) + "}")

class DataStream:
    def __init__(self) -> None:
        self.processors: List[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: List[Any]) -> None:
        for element in stream:
            for proc in self.processors:
                if proc.validate(element):
                    proc.ingest(element)
                    break

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        """Consomme nb éléments de chaque processeur et exporte."""
        for proc in self.processors:
            to_export = []
            for _ in range(nb):
                if proc.remaining > 0:
                    to_export.append(proc.output())
            if to_export:
                plugin.process_output(to_export)

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return
        for proc in self.processors:
            print(f"{proc.name}: total {proc.total_processed} items processed, remaining {proc.remaining} on processor")


def main() -> None:
    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Processors\n")
    ds.register_processor(NumericProcessor("Numeric Processor"))
    ds.register_processor(TextProcessor("Text Processor"))
    ds.register_processor(LogProcessor("Log Processor"))

    batch1 = [
        'Hello world', 
        [3.14, -1, 2.71], 
        [{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'}, 
         {'log_level': 'INFO', 'log_message': 'User wil is connected'}], 
        42, 
        ['Hi', 'five']
    ]
    
    print(f"Send first batch of data on stream: {batch1}")
    ds.process_stream(batch1)
    ds.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    ds.output_pipeline(3, CSVExportPlugin())
    ds.print_processors_stats()

    batch2 = [
        21, 
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'], 
        [{'log_level': 'ERROR', 'log_message': '500 server crash'}, 
         {'log_level': 'NOTICE', 'log_message': 'Certificate expires in 10 days'}], 
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
