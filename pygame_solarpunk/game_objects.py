"""
Game Objects for Solarpunk Space Starter Kit
All game entities: Player, Orbs, Debris, Background layers
Pure algorithmic approach - no neural networks
"""

import pygame
import random
import math


class Player:
    """Spaceship controlled by the player"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 5
        self.color = (100, 255, 150)  # Solarpunk green
        self.trail = []

    def move(self, keys, screen_width, screen_height):
        """Handle player movement with boundary checks"""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        # Boundary checking
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))

        # Add to trail for visual effect
        self.trail.append((self.x + self.width // 2, self.y + self.height // 2))
        if len(self.trail) > 20:
            self.trail.pop(0)

    def draw(self, screen):
        """Draw player ship with trail effect"""
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            radius = int(3 * (i / len(self.trail)))
            color = (100, 255, 150, alpha)
            pygame.draw.circle(screen, color[:3], pos, radius)

        # Draw ship (simple triangle)
        points = [
            (self.x + self.width, self.y + self.height // 2),  # nose
            (self.x, self.y),  # top back
            (self.x, self.y + self.height)  # bottom back
        ]
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, (50, 200, 100), points, 2)  # outline

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class SolarOrb:
    """Collectible energy orbs - using complex number mathematics for movement"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.color = (255, 220, 100)  # Golden yellow
        self.glow_radius = self.radius
        self.pulse_speed = 0.1
        self.angle = random.uniform(0, 2 * math.pi)
        # Complex number representation: position as complex number
        self.complex_pos = complex(x, y)

    def update(self):
        """Pulsing glow effect using sine wave"""
        self.glow_radius = self.radius + 5 * abs(math.sin(self.angle))
        self.angle += self.pulse_speed

    def draw(self, screen):
        """Draw orb with glowing effect"""
        # Outer glow
        for i in range(3):
            glow_color = (255, 220, 100, 100 - i * 30)
            radius = int(self.glow_radius + i * 5)
            pygame.draw.circle(screen, glow_color[:3], (int(self.x), int(self.y)), radius)

        # Core orb
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 255, 200), (int(self.x), int(self.y)), self.radius - 4)

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)


class Debris:
    """Floating space debris - obstacles to avoid"""

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = random.uniform(1, 3)
        self.color = (150, 100, 80)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        """Move debris and rotate"""
        self.x -= self.speed
        self.rotation += self.rotation_speed

    def draw(self, screen):
        """Draw rotating debris"""
        # Create debris shape (irregular polygon)
        points = []
        num_points = 6
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi + math.radians(self.rotation)
            variance = random.uniform(0.7, 1.3)
            px = self.x + math.cos(angle) * self.size * variance
            py = self.y + math.sin(angle) * self.size * variance
            points.append((int(px), int(py)))

        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, (100, 70, 50), points, 2)

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.size, self.y - self.size,
                          self.size * 2, self.size * 2)

    def is_off_screen(self):
        """Check if debris has moved off screen"""
        return self.x < -self.size * 2


class Star:
    """Background stars for parallax effect"""

    def __init__(self, x, y, layer):
        self.x = x
        self.y = y
        self.layer = layer  # 0-2, determines speed
        self.speed = (layer + 1) * 0.5
        self.size = layer + 1
        self.brightness = random.randint(150, 255)

    def update(self, screen_width):
        """Move star for parallax effect"""
        self.x -= self.speed
        if self.x < 0:
            self.x = screen_width
            self.y = random.randint(0, 600)

    def draw(self, screen):
        """Draw star"""
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)


class ParticleEffect:
    """Particle effects for collection and explosions"""

    def __init__(self, x, y, color, num_particles=10):
        self.particles = []
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'color': color
            })

    def update(self):
        """Update particle positions and lifetime"""
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 0.02

        # Remove dead particles
        self.particles = [p for p in self.particles if p['life'] > 0]

    def draw(self, screen):
        """Draw particles"""
        for particle in self.particles:
            alpha = int(255 * particle['life'])
            size = int(4 * particle['life'])
            if size > 0:
                pygame.draw.circle(screen, particle['color'],
                                 (int(particle['x']), int(particle['y'])), size)

    def is_finished(self):
        """Check if all particles are gone"""
        return len(self.particles) == 0
