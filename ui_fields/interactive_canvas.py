"""
Interactive Canvas - Dynamic visual field representations

Implements canvas-based fields for visualizing cosmic data,
particle systems, and interactive saga transformations.
"""

import math
import random
from typing import List, Tuple, Optional, Dict, Any


class CosmicCanvas:
    """An interactive canvas for cosmic visualizations"""

    def __init__(self, width: int, height: int, name: str = "cosmos"):
        self.width = width
        self.height = height
        self.name = name
        self.background_color = (25, 20, 31)  # Deep purple-black
        self.elements = []
        self.frame_count = 0

    def add_element(self, element: Dict[str, Any]) -> 'CosmicCanvas':
        """Add a visual element to the canvas"""
        self.elements.append(element)
        return self

    def remove_element(self, element_id: str) -> 'CosmicCanvas':
        """Remove an element by ID"""
        self.elements = [e for e in self.elements if e.get('id') != element_id]
        return self

    def clear(self) -> 'CosmicCanvas':
        """Clear all elements"""
        self.elements = []
        return self

    def update(self, dt: float = 0.016) -> 'CosmicCanvas':
        """Update all elements (dt in seconds, ~60fps = 0.016)"""
        self.frame_count += 1

        for element in self.elements:
            if 'update' in element:
                element['update'](element, dt)

        return self

    def get_elements_at(self, x: float, y: float, radius: float = 5.0) -> List[Dict]:
        """Get elements within radius of point"""
        nearby = []
        for element in self.elements:
            ex, ey = element.get('x', 0), element.get('y', 0)
            dist = math.sqrt((x - ex)**2 + (y - ey)**2)
            if dist <= radius:
                nearby.append(element)
        return nearby

    def to_ascii_art(self, char_map: Dict[str, str] = None) -> str:
        """Render canvas as ASCII art"""
        char_map = char_map or {'particle': '*', 'star': '.', 'default': 'o'}

        # Create grid
        grid = [[' ' for _ in range(self.width // 4)] for _ in range(self.height // 8)]

        for element in self.elements:
            x = int(element.get('x', 0)) // 4
            y = int(element.get('y', 0)) // 8

            if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
                element_type = element.get('type', 'default')
                grid[y][x] = char_map.get(element_type, 'o')

        return '\n'.join(''.join(row) for row in grid)

    def __repr__(self):
        return f"CosmicCanvas(size={self.width}x{self.height}, elements={len(self.elements)})"


class ParticleField:
    """A field of particles with physics and saga properties"""

    def __init__(self, name: str = "particle_field"):
        self.name = name
        self.particles = []
        self.forces = []
        self.constraints = []

    def add_particle(self, x: float, y: float, vx: float = 0, vy: float = 0,
                     mass: float = 1.0, color: Tuple[int, int, int] = (100, 200, 255)) -> int:
        """Add a particle and return its ID"""
        particle = {
            'id': len(self.particles),
            'x': x,
            'y': y,
            'vx': vx,
            'vy': vy,
            'ax': 0.0,
            'ay': 0.0,
            'mass': mass,
            'color': color,
            'age': 0.0,
            'lifetime': None,  # None = infinite
            'alive': True
        }
        self.particles.append(particle)
        return particle['id']

    def add_force(self, force_func: callable) -> 'ParticleField':
        """
        Add a force function that takes (particle) and returns (fx, fy)
        Example: lambda p: (0, 9.8 * p['mass'])  # Gravity
        """
        self.forces.append(force_func)
        return self

    def add_constraint(self, constraint_func: callable) -> 'ParticleField':
        """
        Add a constraint function that takes (particle) and modifies it
        Example: lambda p: p.update({'x': max(0, min(800, p['x']))})  # Boundaries
        """
        self.constraints.append(constraint_func)
        return self

    def update(self, dt: float = 0.016) -> 'ParticleField':
        """Update all particles"""
        for particle in self.particles:
            if not particle['alive']:
                continue

            # Reset acceleration
            particle['ax'] = 0.0
            particle['ay'] = 0.0

            # Apply forces
            for force in self.forces:
                fx, fy = force(particle)
                particle['ax'] += fx / particle['mass']
                particle['ay'] += fy / particle['mass']

            # Update velocity
            particle['vx'] += particle['ax'] * dt
            particle['vy'] += particle['ay'] * dt

            # Update position
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt

            # Apply constraints
            for constraint in self.constraints:
                constraint(particle)

            # Update age
            particle['age'] += dt
            if particle['lifetime'] and particle['age'] > particle['lifetime']:
                particle['alive'] = False

        # Remove dead particles
        self.particles = [p for p in self.particles if p['alive']]
        return self

    def get_particle(self, particle_id: int) -> Optional[Dict]:
        """Get particle by ID"""
        for particle in self.particles:
            if particle['id'] == particle_id:
                return particle
        return None

    def apply_saga_resonance(self) -> 'ParticleField':
        """Apply saga resonance to all particles (cosmic harmony)"""
        # Create harmonic motion patterns
        center_x = sum(p['x'] for p in self.particles) / len(self.particles) if self.particles else 0
        center_y = sum(p['y'] for p in self.particles) / len(self.particles) if self.particles else 0

        for particle in self.particles:
            dx = particle['x'] - center_x
            dy = particle['y'] - center_y
            dist = math.sqrt(dx*dx + dy*dy)

            if dist > 0:
                # Add harmonic force toward center
                harmony = 0.1
                particle['vx'] += -dx * harmony
                particle['vy'] += -dy * harmony

        return self

    def __repr__(self):
        return f"ParticleField(name={self.name}, particles={len(self.particles)})"


class VectorField:
    """A field of vectors for visualizing flow and forces"""

    def __init__(self, name: str, width: int, height: int, resolution: int = 20):
        self.name = name
        self.width = width
        self.height = height
        self.resolution = resolution
        self.vectors = []

        # Initialize grid of vectors
        for y in range(0, height, resolution):
            for x in range(0, width, resolution):
                self.vectors.append({
                    'x': x,
                    'y': y,
                    'dx': 0.0,
                    'dy': 0.0,
                    'magnitude': 0.0,
                    'angle': 0.0
                })

    def set_vector_function(self, func: callable) -> 'VectorField':
        """
        Set vectors using a function (x, y) -> (dx, dy)
        Example: lambda x, y: (y - height/2, -(x - width/2))  # Vortex
        """
        for vector in self.vectors:
            dx, dy = func(vector['x'], vector['y'])
            vector['dx'] = dx
            vector['dy'] = dy
            vector['magnitude'] = math.sqrt(dx*dx + dy*dy)
            vector['angle'] = math.atan2(dy, dx)

        return self

    def create_vortex(self, center_x: float, center_y: float, strength: float = 1.0) -> 'VectorField':
        """Create a vortex pattern"""
        def vortex_func(x, y):
            dx = center_x - x
            dy = center_y - y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                return (-dy/dist * strength, dx/dist * strength)
            return (0, 0)

        return self.set_vector_function(vortex_func)

    def create_wave(self, wavelength: float = 50.0, amplitude: float = 10.0, time: float = 0) -> 'VectorField':
        """Create a wave pattern"""
        def wave_func(x, y):
            angle = (x / wavelength + time) * 2 * math.pi
            dy = math.sin(angle) * amplitude
            dx = math.cos(angle) * amplitude * 0.5
            return (dx, dy)

        return self.set_vector_function(wave_func)

    def create_perlin_field(self, scale: float = 0.1, seed: int = 42) -> 'VectorField':
        """Create Perlin-like noise field"""
        random.seed(seed)

        def perlin_func(x, y):
            angle = (random.random() * 2 * math.pi * scale + x * 0.01 + y * 0.01) % (2 * math.pi)
            magnitude = random.random()
            return (math.cos(angle) * magnitude, math.sin(angle) * magnitude)

        return self.set_vector_function(perlin_func)

    def add_vectors(self, other: 'VectorField') -> 'VectorField':
        """Add another vector field to this one"""
        if len(self.vectors) != len(other.vectors):
            return self

        for i, vector in enumerate(self.vectors):
            other_vector = other.vectors[i]
            vector['dx'] += other_vector['dx']
            vector['dy'] += other_vector['dy']
            vector['magnitude'] = math.sqrt(vector['dx']**2 + vector['dy']**2)
            vector['angle'] = math.atan2(vector['dy'], vector['dx'])

        return self

    def scale(self, factor: float) -> 'VectorField':
        """Scale all vectors by a factor"""
        for vector in self.vectors:
            vector['dx'] *= factor
            vector['dy'] *= factor
            vector['magnitude'] *= factor

        return self

    def normalize(self) -> 'VectorField':
        """Normalize all vectors to unit length"""
        for vector in self.vectors:
            mag = vector['magnitude']
            if mag > 0:
                vector['dx'] /= mag
                vector['dy'] /= mag
                vector['magnitude'] = 1.0

        return self

    def __repr__(self):
        return f"VectorField(name={self.name}, size={self.width}x{self.height}, vectors={len(self.vectors)})"
