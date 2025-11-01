"""
UI Fields Module - Interactive User Interface Components with Field Properties

Implements field-based UI systems inspired by the Saganomicon principles.
Each UI component is a field that can transform, resonate, and interact with others.
"""

from .field_components import TextField, NumberField, SelectField, ToggleField, ColorField
from .composite_fields import FormField, TableField, GridField, FlowField
from .interactive_canvas import CosmicCanvas, ParticleField, VectorField
from .field_validators import FieldValidator, ValidationChain, SagaValidator

__all__ = [
    'TextField',
    'NumberField',
    'SelectField',
    'ToggleField',
    'ColorField',
    'FormField',
    'TableField',
    'GridField',
    'FlowField',
    'CosmicCanvas',
    'ParticleField',
    'VectorField',
    'FieldValidator',
    'ValidationChain',
    'SagaValidator'
]

__version__ = '1.0.0'
__author__ = 'PAUL RUTHERFORDS'
