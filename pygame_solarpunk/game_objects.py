"""
Game Objects for Solarpunk Space Game

Contains all game entity classes.
"""

import pygame
import random
from typing import Tuple


class Player(pygame.sprite.Sprite):
    """Player spaceship with solar sails."""

    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill((100, 200, 150))  # Mint green ship

        # Draw simple ship shape
        pygame.draw.polygon(self.image, (150, 220, 200),
                          [(20, 0), (0, 50), (40, 50)])
        pygame.draw.circle(self.image, (255, 200, 100), (20, 25), 8)  # Solar core

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.velocity_y = 0
        self.velocity_x = 0
        self.drag = 0.95

    def update(self, keys, screen_width: int, screen_height: int):
        """Update player position based on input."""
        # Acceleration-based movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x -= 0.5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x += 0.5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y -= 0.5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y += 0.5

        # Apply drag
        self.velocity_x *= self.drag
        self.velocity_y *= self.drag

        # Limit speed
        max_speed = 8
        speed = (self.velocity_x**2 + self.velocity_y**2)**0.5
        if speed > max_speed:
            ratio = max_speed / speed
            self.velocity_x *= ratio
            self.velocity_y *= ratio

        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Keep on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))


class SolarOrb(pygame.sprite.Sprite):
    """Collectible solar energy orb."""

    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)

        # Draw glowing orb
        pygame.draw.circle(self.image, (255, 220, 100, 200), (10, 10), 10)
        pygame.draw.circle(self.image, (255, 255, 150, 150), (10, 10), 6)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.float_offset = random.uniform(0, 6.28)
        self.time = 0

    def update(self):
        """Gentle floating animation."""
        self.time += 0.1
        self.rect.y += pygame.math.Vector2(0, 1).rotate(
            (self.time + self.float_offset) * 20
        ).y * 0.5


class Debris(pygame.sprite.Sprite):
    """Space debris obstacle."""

    def __init__(self, x: int, y: int, speed: float = 2):
        super().__init__()
        size = random.randint(30, 60)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)

        # Draw rocky debris with dusty orange tones
        color = (
            random.randint(180, 220),
            random.randint(130, 160),
            random.randint(90, 120)
        )
        points = []
        for i in range(random.randint(6, 10)):
            angle = (i / 8) * 6.28
            radius = random.randint(size//3, size//2)
            x_point = size//2 + radius * pygame.math.Vector2(1, 0).rotate(angle * 57.3).x
            y_point = size//2 + radius * pygame.math.Vector2(1, 0).rotate(angle * 57.3).y
            points.append((x_point, y_point))

        pygame.draw.polygon(self.image, color, points)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.rotation_speed = random.uniform(-2, 2)
        self.angle = 0

    def update(self):
        """Move debris across screen."""
        self.rect.x -= self.speed
        self.angle += self.rotation_speed


class Star:
    """Background star for parallax effect."""

    def __init__(self, x: int, y: int, depth: int):
        self.x = x
        self.y = y
        self.depth = depth
        self.speed = 1 / depth
        self.size = max(1, 3 - depth)
        self.color = (
            150 + depth * 20,
            150 + depth * 20,
            150 + depth * 30
        )

    def update(self, screen_width: int):
        """Move star for parallax effect."""
        self.x -= self.speed
        if self.x < 0:
            self.x = screen_width
            self.y = random.randint(0, 600)

    def draw(self, screen):
        """Draw the star."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class Particle:
    """Particle effect for collections and explosions."""

    def __init__(self, x: int, y: int, color: Tuple[int, int, int], velocity: Tuple[float, float]):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = 30
        self.size = random.randint(2, 5)

    def update(self):
        """Update particle position and lifetime."""
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.lifetime -= 1
        self.size = max(1, self.size - 0.1)

    def draw(self, screen):
        """Draw the particle."""
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / 30))
            color = (*self.color, alpha)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

    def is_alive(self) -> bool:
        """Check if particle should still exist."""
        return self.lifetime > 0
