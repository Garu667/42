from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class DataStream(ABC):
    def __init__(self, stream_id: str) -> None:
        self.stream_id: str = stream_id
        self._processed_batches: int = 0
        self._processed_items: int = 0
        self._last_summary: str = ""

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
            self,
            data_batch: List[Any],
            criteria: Optional[str] = None
            ) -> List[Any]:
        _ = criteria
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.stream_id,
            "batches": self._processed_batches,
            "items": self._processed_items,
            "last": self._last_summary,
        }


class SensorStream(DataStream):
    def process_batch(self, data_batch: List[Any]) -> str:
        print("Processing sensor batch:", data_batch)
        try:
            readings = [x for x in data_batch if isinstance(x, str)]
            temps = []
            for item in readings:
                if item.startswith("temp:"):
                    temps.append(float(item.split(":", 1)[1]))
            self._processed_batches += 1
            self._processed_items += len(readings)
            avg_temp = sum(temps) / len(temps) if temps else 0.0
            self._last_summary = f"{len(readings)} readings processed"
            res = (
                f"Sensor analysis: {len(readings)} "
                f"readings processed, avg temp: {avg_temp}°C"
            )
            return res
        except (ValueError, TypeError):
            return "Sensor analysis: error while processing batch"

    def filter_data(
            self,
            data_batch: List[Any],
            criteria: Optional[str] = None
            ) -> List[Any]:
        if criteria == "critical":
            return [x for x in data_batch
                    if isinstance(x, str) and "ALERT" in x]
        return super().filter_data(data_batch, criteria)


class TransactionStream(DataStream):
    def process_batch(self, data_batch: List[Any]) -> str:
        print("Processing transaction batch:", data_batch)
        try:
            ops = [x for x in data_batch if isinstance(x, str)]
            net = 0.0
            for op in ops:
                if ":" not in op:
                    continue
                kind, amount_s = op.split(":", 1)
                kind = kind.strip().lower()
                amount = float(amount_s)
                if kind == "buy":
                    net -= amount
                elif kind == "sell":
                    net += amount
            self._processed_batches += 1
            self._processed_items += len(ops)
            self._last_summary = f"{len(ops)} operations processed"
            res = (
                f"Transaction analysis: {len(ops)} "
                f"operations, net flow: {net} units"
            )
            return res
        except (ValueError, TypeError):
            return "Transaction analysis: error while processing batch"

    def filter_data(
            self,
            data_batch: List[Any],
            criteria: Optional[str] = None
            ) -> List[Any]:
        if criteria == "large":
            out: List[Any] = []
            for x in data_batch:
                if isinstance(x, str) and ":" in x:
                    _, amount_s = x.split(":", 1)
                    try:
                        if float(amount_s) >= 100:
                            out.append(x)
                    except ValueError:
                        pass
            return out
        return super().filter_data(data_batch, criteria)


class EventStream(DataStream):
    def process_batch(self, data_batch: List[Any]) -> str:
        print("Processing event batch:", data_batch)
        try:
            events = [x for x in data_batch if isinstance(x, str)]
            error_count = len([e for e in events if e.lower() == "error"])
            self._processed_batches += 1
            self._processed_items += len(events)
            self._last_summary = f"{len(events)} events processed"
            res = (
                f"Event analysis: {len(events)} events,"
                f" {error_count} error detected"
            )
            return res
        except Exception:
            return "Event analysis: error while processing batch"

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
            ) -> List[Any]:
        if criteria == "errors":
            return [x for x in data_batch
                    if isinstance(x, str) and x.lower() == "error"]
        return super().filter_data(data_batch, criteria)


class StreamProcessor:
    def __init__(self) -> None:
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        self.streams.append(stream)

    def process(self, stream: DataStream, batch: List[Any]) -> str:
        try:
            return stream.process_batch(batch)
        except Exception:
            return "StreamProcessor: processing failure"


def main() -> None:
    print("Initializing Sensor Stream...")
    sensor = SensorStream("SENSOR_001")
    print(f"Stream ID: {sensor.stream_id}, Type: Environmental Data")
    print(sensor.process_batch(["temp:22.5", "humidity:65", "pressure:1013"]))

    print("\nInitializing Transaction Stream...")
    trans = TransactionStream("TRANS_001")
    print(f"Stream ID: {trans.stream_id}, Type: Financial Data")
    print(trans.process_batch(["buy:100", "sell:150", "buy:75"]))

    print("\nInitializing Event Stream...")
    event = EventStream("EVENT_001")
    print(f"Stream ID: {event.stream_id}, Type: System Events")
    print(event.process_batch(["login", "error", "logout"]))

    print("\n=== Polymorphic Stream Processing ===")
    manager = StreamProcessor()
    manager.add_stream(sensor)
    manager.add_stream(trans)
    manager.add_stream(event)

    batch1_sensor = ["temp:25.0", "ALERT: temp:99.0"]
    batch1_trans = ["buy:10", "sell:200", "sell:5", "buy:1"]
    batch1_event = ["login", "error", "error"]
    str_sensor = manager.process(sensor, batch1_sensor)
    str_trans = manager.process(trans, batch1_trans)
    str_event = manager.process(event, batch1_event)
    print("Processing mixed stream types through unified interface...\n")

    print("Batch 1 Results:")
    print(f"- {str_sensor}")
    print(f"- {str_trans}")
    print(f"- {str_event}")

    print("\nStream filtering active: High-priority data only")
    crit_sensor = sensor.filter_data(batch1_sensor, "critical")
    large_trans = trans.filter_data(batch1_trans, "large")
    print(
        f"Filtered results: {len(crit_sensor)} critical sensor alerts,"
        f" {len(large_trans)} large transaction")

    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")
    main()
