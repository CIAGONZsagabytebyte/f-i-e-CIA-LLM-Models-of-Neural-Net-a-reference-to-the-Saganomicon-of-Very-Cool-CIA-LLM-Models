"""
GA Fields Module - Genetic Algorithms and Procedural Generation

Implements evolutionary algorithms, procedural content generation,
and game architecture patterns inspired by cosmic evolution and the Saganomicon.
"""

from .genetic_engine import GeneticAlgorithm, Individual, Population, FitnessFunction
from .evolution_fields import EvolutionField, MutationField, CrossoverField, SelectionField
from .procedural_generation import CosmicGenerator, TerrainGenerator, SpaceGenerator
from .game_architecture import GameStateField, EntityField, SystemField, WorldField

__all__ = [
    'GeneticAlgorithm',
    'Individual',
    'Population',
    'FitnessFunction',
    'EvolutionField',
    'MutationField',
    'CrossoverField',
    'SelectionField',
    'CosmicGenerator',
    'TerrainGenerator',
    'SpaceGenerator',
    'GameStateField',
    'EntityField',
    'SystemField',
    'WorldField'
]

__version__ = '1.0.0'
__author__ = 'PAUL RUTHERFORDS'
