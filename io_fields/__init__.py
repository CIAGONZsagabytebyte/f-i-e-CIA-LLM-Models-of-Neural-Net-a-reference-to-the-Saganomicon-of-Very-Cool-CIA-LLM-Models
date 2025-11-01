"""
I/O Fields Module - Data Stream Processing and Field Transformations

Inspired by the Saganomicon principles of information flow through cosmic fields.
This module provides tools for stream processing, data pipelines, and field operations.
"""

from .stream_processor import StreamProcessor, FieldStream, DataPipeline
from .field_io import FieldReader, FieldWriter, BinaryFieldCodec
from .quantum_channels import QuantumChannel, EntangledStream, CosmicBuffer

__all__ = [
    'StreamProcessor',
    'FieldStream',
    'DataPipeline',
    'FieldReader',
    'FieldWriter',
    'BinaryFieldCodec',
    'QuantumChannel',
    'EntangledStream',
    'CosmicBuffer'
]

__version__ = '1.0.0'
__author__ = 'PAUL RUTHERFORDS'
