"""
Game objects for Solarpunk Space
Contains all sprite classes: Player, SolarOrb, Debris, Stars
"""

import pygame
import random

# Colors
TEAL = (76, 215, 177)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
DARK_TEAL = (40, 120, 100)


class Player(pygame.sprite.Sprite):
    """Player spaceship with solar sails."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.draw_ship()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def draw_ship(self):
        """Draw a simple ship with solarpunk aesthetic."""
        # Solar sail (teal triangles)
        pygame.draw.polygon(self.image, TEAL, [(20, 5), (10, 20), (30, 20)])
        # Ship body
        pygame.draw.polygon(self.image, DARK_TEAL, [(20, 20), (15, 35), (25, 35)])
        # Energy core
        pygame.draw.circle(self.image, GOLD, (20, 25), 4)

    def update(self):
        """Update player position based on input."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600


class SolarOrb(pygame.sprite.Sprite):
    """Collectible solar energy orbs."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        self.draw_orb()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2

    def draw_orb(self):
        """Draw a glowing solar orb."""
        # Outer glow
        pygame.draw.circle(self.image, (255, 235, 100, 100), (12, 12), 12)
        # Inner orb
        pygame.draw.circle(self.image, GOLD, (12, 12), 8)
        # Core
        pygame.draw.circle(self.image, WHITE, (12, 12), 4)

    def update(self):
        """Move orb down the screen."""
        self.rect.y += self.speed

        # Remove if off screen
        if self.rect.top > 600:
            self.kill()


class Debris(pygame.sprite.Sprite):
    """Floating space debris to avoid."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.draw_debris()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.uniform(1.5, 3.5)
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)

    def draw_debris(self):
        """Draw angular debris."""
        points = [(5, 10), (15, 5), (25, 12), (20, 25), (8, 22)]
        pygame.draw.polygon(self.image, RED, points)
        pygame.draw.polygon(self.image, (150, 50, 50), points, 2)

    def update(self):
        """Move and rotate debris."""
        self.rect.y += self.speed
        self.rotation += self.rotation_speed

        # Remove if off screen
        if self.rect.top > 600:
            self.kill()


class Star(pygame.sprite.Sprite):
    """Background parallax stars."""

    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.size = random.randint(1, 3)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(0, screen_height)
        self.speed = self.size * 0.5

    def update(self):
        """Move star down for parallax effect."""
        self.rect.y += self.speed

        # Wrap around when off screen
        if self.rect.top > 600:
            self.rect.y = -5
            self.rect.x = random.randint(0, 800)
