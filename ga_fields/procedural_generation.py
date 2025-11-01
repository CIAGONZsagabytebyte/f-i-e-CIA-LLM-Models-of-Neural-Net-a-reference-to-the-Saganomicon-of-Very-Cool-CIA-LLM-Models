"""
Procedural Generation - Cosmic content generation using GA principles

Generate terrain, space environments, and solarpunk structures
using evolutionary and procedural algorithms.
"""

import random
import math
from typing import List, Tuple, Dict, Any, Optional


class CosmicGenerator:
    """Base generator for cosmic procedural content"""

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed or random.randint(0, 999999)
        random.seed(self.seed)
        self.generation_count = 0

    def reset_seed(self, seed: Optional[int] = None) -> 'CosmicGenerator':
        """Reset the random seed"""
        self.seed = seed or random.randint(0, 999999)
        random.seed(self.seed)
        return self

    def generate(self) -> Any:
        """Override in subclasses"""
        self.generation_count += 1
        return None

    def __repr__(self):
        return f"{self.__class__.__name__}(seed={self.seed}, generations={self.generation_count})"


class TerrainGenerator(CosmicGenerator):
    """Generate terrain using procedural algorithms"""

    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        super().__init__(seed)
        self.width = width
        self.height = height

    def generate_heightmap(self, octaves: int = 4, persistence: float = 0.5) -> List[List[float]]:
        """Generate a heightmap using multi-octave noise"""
        heightmap = [[0.0 for _ in range(self.width)] for _ in range(self.height)]

        for octave in range(octaves):
            frequency = 2 ** octave
            amplitude = persistence ** octave

            for y in range(self.height):
                for x in range(self.width):
                    # Simple procedural noise
                    value = self._noise(x * frequency / self.width,
                                       y * frequency / self.height)
                    heightmap[y][x] += value * amplitude

        # Normalize to 0-1
        min_val = min(min(row) for row in heightmap)
        max_val = max(max(row) for row in heightmap)
        if max_val > min_val:
            heightmap = [[(val - min_val) / (max_val - min_val) for val in row]
                        for row in heightmap]

        self.generation_count += 1
        return heightmap

    def _noise(self, x: float, y: float) -> float:
        """Simple pseudo-noise function"""
        # Using sine waves for reproducible pseudo-random values
        return (math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % 1.0

    def generate_islands(self, count: int = 5, min_radius: float = 10,
                        max_radius: float = 50) -> List[Dict[str, Any]]:
        """Generate island data"""
        islands = []
        for _ in range(count):
            island = {
                'x': random.uniform(0, self.width),
                'y': random.uniform(0, self.height),
                'radius': random.uniform(min_radius, max_radius),
                'height': random.uniform(0.5, 1.0),
                'type': random.choice(['mountain', 'forest', 'desert', 'tundra'])
            }
            islands.append(island)

        self.generation_count += 1
        return islands

    def generate_solarpunk_biome(self) -> Dict[str, Any]:
        """Generate a solarpunk-themed biome with sustainable features"""
        biome = {
            'type': random.choice(['solar_garden', 'wind_farm', 'hydro_valley', 'green_cityscape']),
            'solar_coverage': random.uniform(0.3, 0.8),
            'vegetation_density': random.uniform(0.5, 1.0),
            'water_features': random.randint(2, 10),
            'renewable_structures': random.randint(5, 20),
            'color_palette': {
                'primary': random.choice(['#64C8B4', '#B4A0FF', '#64C8DC']),
                'secondary': random.choice(['#DCA06E', '#228B22', '#FFD700']),
                'accent': random.choice(['#19141F', '#4B0082'])
            }
        }

        self.generation_count += 1
        return biome

    def generate_cave_system(self, complexity: int = 50) -> List[Tuple[int, int]]:
        """Generate a cave system using random walk"""
        cave_cells = set()
        start_x, start_y = self.width // 2, self.height // 2

        x, y = start_x, start_y

        for _ in range(complexity * 100):
            cave_cells.add((x, y))

            # Random walk with bias toward center
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            x = max(1, min(self.width - 2, x + dx))
            y = max(1, min(self.height - 2, y + dy))

        self.generation_count += 1
        return list(cave_cells)


class SpaceGenerator(CosmicGenerator):
    """Generate space environments, star systems, and celestial bodies"""

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)

    def generate_star_system(self, num_planets: Optional[int] = None) -> Dict[str, Any]:
        """Generate a complete star system"""
        if num_planets is None:
            num_planets = random.randint(3, 12)

        star_types = ['G-type', 'K-type', 'M-type', 'F-type', 'A-type']
        star_colors = ['#FFD700', '#FFA500', '#FF6347', '#FFFACD', '#F0F8FF']

        star_type = random.choice(star_types)
        star_color = star_colors[star_types.index(star_type)]

        system = {
            'name': self._generate_star_name(),
            'star': {
                'type': star_type,
                'color': star_color,
                'mass': random.uniform(0.5, 2.0),
                'radius': random.uniform(0.8, 1.5),
                'luminosity': random.uniform(0.1, 10.0)
            },
            'planets': [],
            'asteroid_belts': random.randint(0, 3),
            'habitable_zone': (random.uniform(0.8, 1.2), random.uniform(1.5, 2.0))
        }

        # Generate planets
        orbital_distance = random.uniform(0.3, 0.5)
        for i in range(num_planets):
            orbital_distance += random.uniform(0.2, 0.8)
            planet = self.generate_planet(orbital_distance)
            system['planets'].append(planet)

        self.generation_count += 1
        return system

    def generate_planet(self, orbital_distance: float) -> Dict[str, Any]:
        """Generate a single planet"""
        planet_types = ['rocky', 'gas_giant', 'ice_giant', 'dwarf', 'super_earth']
        planet_type = random.choice(planet_types)

        planet = {
            'name': self._generate_planet_name(),
            'type': planet_type,
            'orbital_distance': orbital_distance,
            'radius': self._get_planet_radius(planet_type),
            'mass': random.uniform(0.1, 10.0),
            'atmosphere': random.choice([True, False]),
            'moons': random.randint(0, 5) if planet_type in ['gas_giant', 'ice_giant'] else random.randint(0, 2),
            'color': self._get_planet_color(planet_type),
            'rotation_period': random.uniform(10, 200),
            'axial_tilt': random.uniform(0, 45)
        }

        # Add solarpunk features if in habitable zone
        if 0.8 <= orbital_distance <= 2.0 and planet_type in ['rocky', 'super_earth']:
            planet['solarpunk_potential'] = {
                'habitability': random.uniform(0.5, 1.0),
                'solar_resources': random.uniform(0.6, 1.0),
                'terraforming_difficulty': random.uniform(0.1, 0.5)
            }

        return planet

    def _get_planet_radius(self, planet_type: str) -> float:
        """Get radius based on planet type"""
        radius_ranges = {
            'rocky': (0.4, 1.2),
            'gas_giant': (8.0, 15.0),
            'ice_giant': (3.0, 6.0),
            'dwarf': (0.2, 0.6),
            'super_earth': (1.2, 2.5)
        }
        min_r, max_r = radius_ranges.get(planet_type, (0.5, 1.5))
        return random.uniform(min_r, max_r)

    def _get_planet_color(self, planet_type: str) -> str:
        """Get color based on planet type"""
        colors = {
            'rocky': ['#8B4513', '#CD853F', '#DEB887', '#F4A460'],
            'gas_giant': ['#FFA500', '#FFD700', '#FFDAB9', '#E6E6FA'],
            'ice_giant': ['#87CEEB', '#4682B4', '#5F9EA0', '#B0E0E6'],
            'dwarf': ['#A9A9A9', '#696969', '#778899'],
            'super_earth': ['#228B22', '#64C8B4', '#4169E1', '#9370DB']
        }
        return random.choice(colors.get(planet_type, ['#808080']))

    def _generate_star_name(self) -> str:
        """Generate a procedural star name"""
        prefixes = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta']
        suffixes = ['Centauri', 'Draconis', 'Phoenicis', 'Aquarii', 'Cygni', 'Orionis']
        return f"{random.choice(prefixes)} {random.choice(suffixes)}"

    def _generate_planet_name(self) -> str:
        """Generate a procedural planet name"""
        consonants = 'bcdfghjklmnpqrstvwxyz'
        vowels = 'aeiou'

        name = ''
        for i in range(random.randint(3, 6)):
            if i % 2 == 0:
                name += random.choice(consonants)
            else:
                name += random.choice(vowels)

        return name.capitalize()

    def generate_nebula(self) -> Dict[str, Any]:
        """Generate a nebula"""
        nebula_types = ['emission', 'reflection', 'dark', 'planetary', 'supernova_remnant']

        nebula = {
            'name': f"{self._generate_star_name()} Nebula",
            'type': random.choice(nebula_types),
            'size': random.uniform(1.0, 100.0),  # light years
            'density': random.uniform(0.1, 10.0),
            'temperature': random.uniform(10, 10000),  # Kelvin
            'colors': [
                random.choice(['#B4A0FF', '#FF69B4', '#64C8DC', '#FFD700', '#FF6347'])
                for _ in range(random.randint(2, 5))
            ],
            'star_formation_active': random.choice([True, False])
        }

        self.generation_count += 1
        return nebula

    def generate_asteroid_field(self, count: int = 100, radius: float = 50.0) -> List[Dict[str, Any]]:
        """Generate an asteroid field"""
        asteroids = []

        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, radius)

            asteroid = {
                'x': distance * math.cos(angle),
                'y': distance * math.sin(angle),
                'z': random.uniform(-radius * 0.2, radius * 0.2),
                'size': random.uniform(0.1, 5.0),
                'composition': random.choice(['iron', 'rock', 'ice', 'mixed']),
                'velocity': (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
            }
            asteroids.append(asteroid)

        self.generation_count += 1
        return asteroids

    def generate_space_habitat(self) -> Dict[str, Any]:
        """Generate a solarpunk space habitat"""
        habitat_types = ['O\'Neill_cylinder', 'Stanford_torus', 'Bernal_sphere', 'McKendree_cylinder']

        habitat = {
            'name': f"Habitat {self._generate_planet_name()}",
            'type': random.choice(habitat_types),
            'population': random.randint(1000, 100000),
            'radius': random.uniform(0.5, 10.0),  # km
            'length': random.uniform(5.0, 50.0),  # km
            'rotation_speed': random.uniform(0.5, 2.0),  # rpm
            'solar_arrays': {
                'count': random.randint(4, 20),
                'power_output': random.uniform(100, 10000)  # MW
            },
            'agriculture': {
                'area': random.uniform(1.0, 100.0),  # km²
                'food_sufficiency': random.uniform(0.7, 1.2)
            },
            'ecosystem': {
                'biodiversity_index': random.uniform(0.5, 1.0),
                'sustainability_rating': random.uniform(0.6, 1.0)
            },
            'theme': random.choice(['forest_habitat', 'ocean_world', 'desert_paradise', 'cloud_cities'])
        }

        self.generation_count += 1
        return habitat
