from typing import Any, List, Optional
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self._storage: List[Any] = []
        self.total_processed = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> Any:
        if self._storage:
            return self._storage.pop(0)
        return None

    @property
    def remaining(self) -> int:
        return len(self._storage)

class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)): return True
        if isinstance(data, list): return all(isinstance(x, (int, float)) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data): raise Exception("Invalid Numeric")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append(str(item))
            self.total_processed += 1

class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str): return True
        if isinstance(data, list): return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data): raise Exception("Invalid Text")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append(item)
            self.total_processed += 1

class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        is_dict = lambda d: isinstance(d, dict) and all(isinstance(k, str) for k in d.keys())
        if is_dict(data): return True
        if isinstance(data, list): return all(is_dict(x) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data): raise Exception("Invalid Log")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append(f"{item.get('log_level')}: {item.get('log_message')}")
            self.total_processed += 1


class DataStream:
    def __init__(self) -> None:
        self.processors: List[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        """Enregistre un nouveau processeur dans le flux."""
        self.processors.append(proc)

    def process_stream(self, stream: List[Any]) -> None:
        """Analyse et route chaque élément vers le bon processeur."""
        for element in stream:
            handled = False
            for proc in self.processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            
            if not handled:
                print(f"DataStream error - Can't process element in stream: {element}")

    def print_processors_stats(self) -> None:
        """Affiche les statistiques de chaque processeur enregistré."""
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return
        
        for proc in self.processors:
            print(f"{proc.name}: total {proc.total_processed} items processed, "
                  f"remaining {proc.remaining} on processor")


def main() -> None:
    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Numeric Processor\n")
    num_proc = NumericProcessor("Numeric Processor")
    ds.register_processor(num_proc)

    batch = [
        'Hello world', 
        [3.14, -1, 2.71], 
        [{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'}, 
         {'log_level': 'INFO', 'log_message': 'User wil is connected'}], 
        42, 
        ['Hi', 'five']
    ]

    print(f"Send first batch of data on stream: {batch}")
    ds.process_stream(batch)
    ds.print_processors_stats()

    print("\nRegistering other data processors")
    ds.register_processor(TextProcessor("Text Processor"))
    ds.register_processor(LogProcessor("Log Processor"))

    print("Send the same batch again")
    ds.process_stream(batch)
    ds.print_processors_stats()

    print("\nConsume some elements from the data processors: Numeric 3, Text 2, Log 1")
    for _ in range(3): num_proc.output()
    ds.processors[1].output()
    ds.processors[1].output()
    ds.processors[2].output()

    ds.print_processors_stats()

if __name__ == "__main__":
    try:
        print("=== Code Nexus - Data Stream ===\n")
        main()
    except Exception as e:
        print(f"Error: {e}")
