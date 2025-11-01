"""
I/O Fields Module - Data Stream Processing and Field Transformations

Inspired by the Saganomicon principles of information flow through cosmic fields.
This module provides tools for stream processing, data pipelines, and field operations.

Foundational Principle: i.f(I) = I = f(x)
Where identity is preserved through transformation AND identity is itself functional.
"""

from .stream_processor import StreamProcessor, FieldStream, DataPipeline
from .field_io import FieldReader, FieldWriter, BinaryFieldCodec
from .quantum_channels import QuantumChannel, EntangledStream, CosmicBuffer
from .identity_field import (
    IdentityField,
    IdentityOperator,
    FunctionalIdentity,
    SagaIdentityTheorem,
    IdentityFieldAlgebra,
    identity_field_transform
)

__all__ = [
    'StreamProcessor',
    'FieldStream',
    'DataPipeline',
    'FieldReader',
    'FieldWriter',
    'BinaryFieldCodec',
    'QuantumChannel',
    'EntangledStream',
    'CosmicBuffer',
    'IdentityField',
    'IdentityOperator',
    'FunctionalIdentity',
    'SagaIdentityTheorem',
    'IdentityFieldAlgebra',
    'identity_field_transform'
]

__version__ = '1.1.0'
__author__ = 'PAUL RUTHERFORDS'
