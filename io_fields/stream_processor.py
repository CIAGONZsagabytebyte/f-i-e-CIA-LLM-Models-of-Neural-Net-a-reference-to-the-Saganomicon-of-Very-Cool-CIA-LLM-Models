"""
Stream Processor - Handle data streams with field transformations

Implements the Saga principle: i(f(Saga)=i) where information flows through
transformation fields while preserving essential patterns.
"""

from typing import Any, Callable, Iterator, List, Optional
import time
from collections import deque


class FieldStream:
    """A stream of data flowing through transformation fields"""

    def __init__(self, name: str = "unnamed_stream"):
        self.name = name
        self.buffer = deque(maxlen=1000)
        self.transformations = []
        self.timestamp = time.time()

    def emit(self, data: Any) -> None:
        """Emit data into the stream"""
        self.buffer.append({
            'data': data,
            'timestamp': time.time(),
            'stream': self.name
        })

    def apply_field(self, transformation: Callable) -> 'FieldStream':
        """Apply a transformation field to the stream (f(Saga))"""
        self.transformations.append(transformation)
        return self

    def flow(self) -> Iterator[Any]:
        """Let data flow through all transformation fields"""
        for packet in self.buffer:
            data = packet['data']
            for transform in self.transformations:
                data = transform(data)
            yield data

    def __repr__(self):
        return f"FieldStream(name={self.name}, buffer_size={len(self.buffer)})"


class StreamProcessor:
    """Process multiple streams with saga-inspired field operations"""

    def __init__(self):
        self.streams = {}
        self.global_fields = []

    def create_stream(self, name: str) -> FieldStream:
        """Create a new field stream"""
        stream = FieldStream(name)
        self.streams[name] = stream
        return stream

    def get_stream(self, name: str) -> Optional[FieldStream]:
        """Retrieve a stream by name"""
        return self.streams.get(name)

    def apply_global_field(self, field: Callable) -> None:
        """Apply a transformation field to all streams"""
        self.global_fields.append(field)
        for stream in self.streams.values():
            stream.apply_field(field)

    def merge_streams(self, stream_names: List[str], output_name: str) -> FieldStream:
        """Merge multiple streams into one (saga convergence)"""
        merged = self.create_stream(output_name)
        for name in stream_names:
            if name in self.streams:
                for data in self.streams[name].flow():
                    merged.emit(data)
        return merged

    def fork_stream(self, source_name: str, target_names: List[str]) -> List[FieldStream]:
        """Fork a stream into multiple streams (saga divergence)"""
        source = self.streams.get(source_name)
        if not source:
            return []

        forks = []
        for target_name in target_names:
            fork = self.create_stream(target_name)
            for data in source.flow():
                fork.emit(data)
            forks.append(fork)
        return forks

    def __repr__(self):
        return f"StreamProcessor(streams={len(self.streams)}, global_fields={len(self.global_fields)})"


class DataPipeline:
    """A pipeline for complex data transformations through multiple field stages"""

    def __init__(self, name: str = "saga_pipeline"):
        self.name = name
        self.stages = []
        self.input_data = None
        self.output_data = None

    def add_stage(self, name: str, transform: Callable,
                  validate: Optional[Callable] = None) -> 'DataPipeline':
        """Add a transformation stage to the pipeline"""
        self.stages.append({
            'name': name,
            'transform': transform,
            'validate': validate or (lambda x: True)
        })
        return self

    def process(self, data: Any) -> Any:
        """Process data through all pipeline stages"""
        self.input_data = data
        current = data

        for i, stage in enumerate(self.stages):
            try:
                # Apply transformation
                current = stage['transform'](current)

                # Validate
                if not stage['validate'](current):
                    raise ValueError(f"Stage {i} ({stage['name']}) validation failed")

            except Exception as e:
                print(f"Pipeline error at stage {i} ({stage['name']}): {e}")
                return None

        self.output_data = current
        return current

    def saga_transform(self, data: Any) -> Any:
        """
        Apply the Saga principle: i(f(Saga)=i)
        Transform data while preserving its essential identity
        """
        result = self.process(data)

        # Verify the saga property: output maintains type/structure of input
        if result is not None:
            if type(result) == type(data):
                return result
            else:
                print(f"Warning: Saga property violated - type changed from {type(data)} to {type(result)}")
        return result

    def __repr__(self):
        return f"DataPipeline(name={self.name}, stages={len(self.stages)})"


# Example field transformations
def identity_field(data: Any) -> Any:
    """Identity transformation - returns data unchanged"""
    return data


def amplify_field(factor: float = 2.0) -> Callable:
    """Create an amplification field"""
    def amplifier(data):
        if isinstance(data, (int, float)):
            return data * factor
        elif isinstance(data, str):
            return data * int(factor)
        return data
    return amplifier


def filter_field(predicate: Callable) -> Callable:
    """Create a filtering field"""
    def filter_fn(data):
        if isinstance(data, (list, tuple)):
            return [x for x in data if predicate(x)]
        return data if predicate(data) else None
    return filter_fn


def cosmic_resonance_field(data: Any) -> Any:
    """
    Apply cosmic resonance - extract harmonic patterns
    Inspired by Sagan's vision of cosmic interconnectedness
    """
    if isinstance(data, (int, float)):
        # Return the golden ratio resonance
        return data * 1.618033988749
    elif isinstance(data, str):
        # Return the string with cosmic markers
        return f"☄️{data}✨"
    elif isinstance(data, list):
        # Return harmonically ordered list
        return sorted(data, key=lambda x: hash(x) % 7)
    return data
