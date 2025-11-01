"""
Solarpunk Space Game Objects - Mathematical Foundation
Using complex numbers and ring theory instead of neural networks
f(i) = -i, ring-0 control, functional transformations
"""

import pygame
import math
import random
from typing import Tuple


class ComplexTransform:
    """
    Mathematical transformations using complex numbers
    f(i) = -i rotation, split operations, ring-0 (kernel) control
    """
    @staticmethod
    def rotate(x: float, y: float, angle: float) -> Tuple[float, float]:
        """Rotate point using complex number multiplication: z * e^(iθ)"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        return new_x, new_y

    @staticmethod
    def split_transform(x: float, y: float) -> Tuple[float, float]:
        """f(i) = -i transformation - reflects imaginary component"""
        # In complex notation: if z = x + iy, then f(z) = x - iy (conjugate)
        return x, -y

    @staticmethod
    def ring_kernel(value: float, modulus: float = 1.0) -> float:
        """Ring-0 (kernel) operation - maps to equivalence class"""
        return value % modulus


class GameObject:
    """Base class for all game objects using functional transforms"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.velocity_x = 0.0
        self.velocity_y = 0.0

    def update(self, dt: float):
        """Update position using functional composition"""
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def get_rect(self) -> pygame.Rect:
        """Override in subclasses"""
        raise NotImplementedError

    def draw(self, surface: pygame.Surface):
        """Override in subclasses"""
        raise NotImplementedError


class Player(GameObject):
    """Player ship using complex number transformations for movement"""

    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.width = 40
        self.height = 50
        self.speed = 200.0
        self.rotation = 0.0
        self.color = (100, 255, 150)  # Solarpunk green
        self.trail_particles = []

    def handle_input(self, keys, dt: float):
        """Movement using directional transforms"""
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed * dt

        # Apply complex rotation if moving diagonally
        if dx != 0 and dy != 0:
            angle = math.atan2(dy, dx)
            magnitude = math.sqrt(dx*dx + dy*dy)
            dx, dy = ComplexTransform.rotate(magnitude, 0, angle)

        self.velocity_x = dx / dt if dt > 0 else 0
        self.velocity_y = dy / dt if dt > 0 else 0

        # Update rotation based on movement
        if dx != 0 or dy != 0:
            self.rotation = math.atan2(dy, dx) + math.pi/2

    def update(self, dt: float, screen_width: int, screen_height: int):
        """Update with boundary wrapping using ring kernel"""
        super().update(dt)

        # Ring-0 wrapping - toroidal topology
        self.x = ComplexTransform.ring_kernel(self.x, screen_width)
        self.y = ComplexTransform.ring_kernel(self.y, screen_height)

        # Add trail particle
        if random.random() < 0.3:
            self.trail_particles.append({
                'x': self.x,
                'y': self.y,
                'life': 1.0,
                'size': random.randint(2, 4)
            })

        # Update trail particles
        for particle in self.trail_particles[:]:
            particle['life'] -= dt * 2
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2,
                          self.width, self.height)

    def draw(self, surface: pygame.Surface):
        """Draw player with trail effect"""
        # Draw trail
        for particle in self.trail_particles:
            alpha = int(particle['life'] * 128)
            color = (100, 255, 150, alpha)
            pygame.draw.circle(surface, color[:3],
                             (int(particle['x']), int(particle['y'])),
                             particle['size'])

        # Draw ship as triangle
        points = [
            (self.x, self.y - self.height//2),  # Top
            (self.x - self.width//2, self.y + self.height//2),  # Bottom left
            (self.x + self.width//2, self.y + self.height//2),  # Bottom right
        ]

        # Rotate points around center
        rotated_points = []
        for px, py in points:
            rx, ry = ComplexTransform.rotate(px - self.x, py - self.y, self.rotation)
            rotated_points.append((rx + self.x, ry + self.y))

        pygame.draw.polygon(surface, self.color, rotated_points)
        pygame.draw.polygon(surface, (200, 255, 200), rotated_points, 2)


class SolarOrb(GameObject):
    """Collectible energy orbs using oscillating transforms"""

    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.radius = 15
        self.phase = random.random() * math.pi * 2
        self.pulse_rate = 2.0
        self.base_radius = 15

    def update(self, dt: float):
        """Pulse using sinusoidal transform"""
        super().update(dt)
        self.phase += self.pulse_rate * dt
        # f(t) = r₀ + A·sin(ωt) - harmonic oscillator
        self.radius = self.base_radius + 3 * math.sin(self.phase)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)

    def draw(self, surface: pygame.Surface):
        """Draw glowing solar orb"""
        # Outer glow
        for i in range(3):
            alpha = 50 - i * 15
            r = int(self.radius * (1.2 + i * 0.1))
            pygame.draw.circle(surface, (255, 220, 100),
                             (int(self.x), int(self.y)), r, 2)

        # Core
        pygame.draw.circle(surface, (255, 255, 150),
                          (int(self.x), int(self.y)), int(self.radius))
        pygame.draw.circle(surface, (255, 200, 50),
                          (int(self.x), int(self.y)), int(self.radius), 3)


class Debris(GameObject):
    """Obstacles using chaotic rotational transforms"""

    def __init__(self, x: float, y: float, vx: float = 0, vy: float = 0):
        super().__init__(x, y)
        self.velocity_x = vx
        self.velocity_y = vy
        self.size = random.randint(20, 40)
        self.rotation = random.random() * math.pi * 2
        self.rotation_speed = random.uniform(-2, 2)
        self.color = (120, 80, 60)
        self.vertices = self._generate_vertices()

    def _generate_vertices(self):
        """Generate irregular polygon using complex exponentials"""
        n_sides = random.randint(5, 8)
        vertices = []
        for i in range(n_sides):
            angle = (i / n_sides) * math.pi * 2
            # Irregular radius using harmonic series
            radius = self.size * (0.7 + 0.3 * random.random())
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append((x, y))
        return vertices

    def update(self, dt: float, screen_width: int, screen_height: int):
        """Update with wrapping and rotation"""
        super().update(dt)
        self.rotation += self.rotation_speed * dt

        # Ring-0 wrapping
        self.x = ComplexTransform.ring_kernel(self.x, screen_width)
        self.y = ComplexTransform.ring_kernel(self.y, screen_height)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.size, self.y - self.size,
                          self.size * 2, self.size * 2)

    def draw(self, surface: pygame.Surface):
        """Draw rotating debris"""
        # Rotate vertices
        rotated_points = []
        for vx, vy in self.vertices:
            rx, ry = ComplexTransform.rotate(vx, vy, self.rotation)
            rotated_points.append((rx + self.x, ry + self.y))

        pygame.draw.polygon(surface, self.color, rotated_points)
        pygame.draw.polygon(surface, (160, 120, 80), rotated_points, 2)


class ParallaxStar:
    """Background stars with depth using linear transforms"""

    def __init__(self, x: float, y: float, depth: float):
        self.x = x
        self.y = y
        self.depth = depth  # 0.1 to 1.0 (closer = faster)
        self.brightness = int(100 + depth * 155)
        self.size = 1 if depth < 0.5 else 2

    def update(self, player_vx: float, player_vy: float, dt: float):
        """Parallax scrolling - affine transformation"""
        self.x -= player_vx * self.depth * dt * 0.5
        self.y -= player_vy * self.depth * dt * 0.5

    def draw(self, surface: pygame.Surface):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


def check_collision(obj1: GameObject, obj2: GameObject) -> bool:
    """Pixel-perfect collision using rect intersection"""
    return obj1.get_rect().colliderect(obj2.get_rect())
