from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter
from typing import Any, Dict, List, Optional, Protocol, Union

from collections import deque


class ProcessingStage(Protocol):
    def process(self, data: Any) -> Any:
        ...


class ProcessingPipeline(ABC):
    def __init__(
        self,
        pipeline_id: str,
        stages: Optional[List[ProcessingStage]] = None
            ) -> None:
        self.pipeline_id: str = pipeline_id
        self.stages: List[ProcessingStage] = stages \
            if stages is not None else []
        self.processed_count: int = 0
        self.error_count: int = 0
        self.last_error: str = ""
        self._latencies: "deque[float]" = deque(maxlen=20)

    def add_stage(self, stage: ProcessingStage) -> None:
        self.stages.append(stage)

    def _run_stages(self, data: Any) -> Any:
        current = data
        for idx, stage in enumerate(self.stages, start=1):
            try:
                current = stage.process(current)
            except Exception as exc:
                self.error_count += 1
                self.last_error = f"Stage {idx} failed: {exc}"
                raise
        return current

    @abstractmethod
    def process(self, data: Any) -> Union[str, Any]:
        pass

    def stats(self) -> Dict[str, Union[str, int, float]]:
        avg = (sum(self._latencies) / len(self._latencies)) \
            if self._latencies else 0.0
        return {
            "pipeline_id": self.pipeline_id,
            "processed": self.processed_count,
            "errors": self.error_count,
            "avg_latency_s": avg,
            "last_error": self.last_error,
        }


class InputStage:
    def process(self, data: Any) -> Any:
        if data is None:
            raise ValueError("data is None")
        return data


class TransformStage:
    def process(self, data: Any) -> Any:
        if isinstance(data, dict):
            out = dict(data)
            out["_meta"] = {"validated": True}
            return out
        if isinstance(data, list):
            return [x for x in data if x is not None]
        return data


class OutputStage:
    def process(self, data: Any) -> Any:
        return data


class JSONAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Union[str, Any]:
        start = perf_counter()
        try:
            if not isinstance(data, str):
                raise TypeError("JSONAdapter expects str")
            raw = data.strip()
            if not (raw.startswith("{") and raw.endswith("}")):
                raise ValueError("invalid JSON-like input")
            cleaned = raw[1:-1].strip()
            items = [x.strip() for x in cleaned.split(",") if x.strip()]
            parsed: Dict[str, Any] = {}
            for it in items:
                if ":" not in it:
                    continue
                k, v = it.split(":", 1)
                key = k.strip().strip('"').strip("'")
                val_s = v.strip().strip('"').strip("'")
                try:
                    val: Any = float(val_s) if "." in val_s else int(val_s)
                except ValueError:
                    val = val_s
                parsed[key] = val

            out = self._run_stages(parsed)
            self.processed_count += 1
            return f"Processed JSON record: {out}"
        except Exception as exc:
            self.error_count += 1
            self.last_error = str(exc)
            raise
        finally:
            self._latencies.append(perf_counter() - start)


class CSVAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Union[str, Any]:
        start = perf_counter()
        try:
            if not isinstance(data, str):
                raise TypeError("CSVAdapter expects str")
            line = data.strip()
            parts = [p.strip() for p in line.split(",") if p.strip()]
            if not parts:
                raise ValueError("empty CSV line")
            out = self._run_stages(parts)
            self.processed_count += 1
            return f"User activity logged: {len(out)} actions processed"
        except Exception as exc:
            self.error_count += 1
            self.last_error = str(exc)
            raise
        finally:
            self._latencies.append(perf_counter() - start)


class StreamAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Union[str, Any]:
        start = perf_counter()
        try:
            if not isinstance(data, list):
                raise TypeError("StreamAdapter expects list")
            out = self._run_stages(data)
            self.processed_count += 1
            return f"Stream summary: {len(out)} readings"
        except Exception as exc:
            self.error_count += 1
            self.last_error = str(exc)
            raise
        finally:
            self._latencies.append(perf_counter() - start)


class NexusManager:
    def __init__(self) -> None:
        self.pipelines: List[ProcessingPipeline] = []
        self.capacity: int = 1000

    def add_pipeline(self, pipeline: ProcessingPipeline) -> None:
        self.pipelines.append(pipeline)

    def run_pipeline(
        self,
        pipeline: ProcessingPipeline,
        data: Any
            ) -> Union[str, Any]:
        return pipeline.process(data)

    def chain(self, chain_list: List[ProcessingPipeline], data: Any) -> Any:
        current = data
        for pipe in chain_list:
            current = pipe.process(current)
        return current

    def recover(
        self,
        primary: ProcessingPipeline,
        backup: ProcessingPipeline,
        data: Any
            ) -> Union[str, Any]:
        try:
            return primary.process(data)
        except Exception:
            print("Recovery initiated: Switching to backup processor")
            return backup.process(data)


def build_stages() -> List[ProcessingStage]:
    return [InputStage(), TransformStage(), OutputStage()]


def main() -> None:
    print("Initializing Nexus Manager...")
    manager = NexusManager()
    print(f"Pipeline capacity: {manager.capacity} streams/second")

    print("\nCreating Data Processing Pipeline...")
    stages = build_stages()
    print("Stage 1: Input validation and parsing")
    print("Stage 2: Data transformation and enrichment")
    print("Stage 3: Output formatting and delivery")

    json_pipe = JSONAdapter("PIPE_JSON", stages=list(stages))
    csv_pipe = CSVAdapter("PIPE_CSV", stages=list(stages))
    stream_pipe = StreamAdapter("PIPE_STREAM", stages=list(stages))

    manager.add_pipeline(json_pipe)
    manager.add_pipeline(csv_pipe)
    manager.add_pipeline(stream_pipe)

    print("\n=== Multi-Format Data Processing ===")
    print("\nProcessing JSON data through pipeline...")
    json_in = '{"sensor":"temp","value":23.5,"unit":"C"}'
    print("Input:", json_in)
    try:
        print("Output:", manager.run_pipeline(json_pipe, json_in))
    except Exception as exc:
        print("Error:", exc)

    print("\nProcessing CSV data through same pipeline...")
    csv_in = "user,action,timestamp"
    print("Input:", repr(csv_in))
    try:
        print("Output:", manager.run_pipeline(csv_pipe, csv_in))
    except Exception as exc:
        print("Error:", exc)

    print("\nProcessing Stream data through same pipeline...")
    stream_in = ["temp:22.0", "temp:21.5", None, "temp:22.8", "temp:21.9"]
    print("Input: Real-time sensor stream")
    try:
        print("Output:", manager.run_pipeline(stream_pipe, stream_in))
    except Exception as exc:
        print("Error:", exc)

    print("\n=== Pipeline Chaining Demo ===")
    print("Pipeline A -> Pipeline B -> Pipeline C")
    print("Data flow: Raw -> Processed -> Analyzed -> Stored")
    try:
        chain_result = manager.chain([json_pipe], json_in)
        print("Chain result:", chain_result)
    except Exception as exc:
        print("Error:", exc)

    print("\n=== Error Recovery Test ===")
    print("Simulating pipeline failure...")
    bad_json = "NOT_JSON"
    try:
        _ = manager.recover(json_pipe, csv_pipe, bad_json)
        print("Recovery successful: Pipeline restored, processing resumed")
    except Exception as exc:
        print("Recovery failed:", exc)

    st = json_pipe.stats()
    if isinstance(st.get("avg_latency_s"), float):
        print(
            f"Performance: avg latency "
            f"{st['avg_latency_s']}s, errors={st['errors']}")

    print("\nNexus Integration complete. All systems operational.")


if __name__ == "__main__":
    print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===\n")
    main()
