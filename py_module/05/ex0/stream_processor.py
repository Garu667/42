#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        print("Processing data:", data)
        try:
            if not self.validate(data):
                raise ValueError("Invalid numeric data")
            values = [float(x) for x in data]
            total = sum(values)
            count = len(values)
            avg = total / count if count > 0 else 0.0
            res = (f"Processed {count} numeric values, "
                   f"sum={int(total) if total % 1 == 0 else total}, "
                   f"avg={avg}")
            return res
        except (TypeError, ValueError):
            return "Error: NumericProcessor received invalid data"

    def validate(self, data: Any) -> bool:
        if not isinstance(data, (list, tuple)):
            return False
        if len(data) == 0:
            return False
        for x in data:
            if not isinstance(x, (int, float)):
                return False
        return True


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        print(f'Processing data: "{data}"')
        try:
            if not self.validate(data):
                raise ValueError("Invalid text data")
            text = data
            char_count = len(text)
            wcount = len([w for w in text.split() if w])
            return f"Processed text: {char_count} characters, {wcount} words"
        except (TypeError, ValueError):
            return "Error: TextProcessor received invalid data"

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)


class LogProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        print(f'Processing data: "{data}"')
        try:
            if not self.validate(data):
                raise ValueError("Invalid log entry")
            line = data.strip()
            level = "INFO"
            message = line

            if ":" in line:
                maybe_level, rest = line.split(":", 1)
                maybe_level = maybe_level.strip().upper()
                if maybe_level in ("INFO", "WARNING", "ERROR"):
                    level = maybe_level
                    message = rest.strip()

            if level == "ERROR":
                return f"[ALERT] ERROR level detected: {message}"
            if level == "WARNING":
                return f"[WARN] WARNING level detected: {message}"
            return f"[INFO] INFO level detected: {message}"
        except (TypeError, ValueError):
            return "Error: LogProcessor received invalid data"

    def validate(self, data: Any) -> bool:
        return isinstance(data, str) and len(data.strip()) > 0


def main() -> None:
    print("Initializing Numeric Processor...")
    num = NumericProcessor()
    result = num.process([1, 2, 3, 4, 5])
    print("Validation: Numeric data verified"
          if num.validate([1, 2, 3, 4, 5]) else "Validation: Failed")
    print(num.format_output(result))

    print("\nInitializing Text Processor...")
    txt = TextProcessor()
    result = txt.process("Hello Nexus World")
    print("Validation: Text data verified"
          if txt.validate("Hello Nexus World") else "Validation: Failed")
    print(txt.format_output(result))

    print("\nInitializing Log Processor...")
    log = LogProcessor()
    result = log.process("ERROR: Connection timeout")
    print("Validation: Log entry verified"
          if log.validate("ERROR: Connection timeout")
          else "Validation: Failed")
    print(log.format_output(result))

    print("\n=== Polymorphic Processing Demo ===")
    processors = [NumericProcessor(), TextProcessor(), LogProcessor()]
    samples = [[1, 2, 3], "Hello Nexus", "INFO: System ready"]

    print("Processing multiple data types through same interface...")
    for i, (proc, sample) in enumerate(zip(processors, samples), start=1):
        print(f"Result {i}:", proc.process(sample))

    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
    main()
