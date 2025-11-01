"""
Solarpunk Space Game - Main Game Loop

Fly your ship through space, collect solar orbs, and avoid debris!
"""

import pygame
import random
import sys
from game_objects import Player, SolarOrb, Debris, Star, Particle


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (Solarpunk palette: mint, lavender, cyan, dusty orange)
BG_COLOR = (25, 20, 35)
TEXT_COLOR = (200, 255, 220)
ACCENT_COLOR = (180, 160, 255)


class Game:
    """Main game class."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Solarpunk Space - Collect Solar Orbs!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.reset_game()

    def reset_game(self):
        """Reset game state."""
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.orbs = pygame.sprite.Group()
        self.debris_group = pygame.sprite.Group()

        # Player
        self.player = Player(100, SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.player)

        # Background stars for parallax
        self.stars = [
            Star(random.randint(0, SCREEN_WIDTH),
                 random.randint(0, SCREEN_HEIGHT),
                 random.randint(1, 3))
            for _ in range(100)
        ]

        # Particles
        self.particles = []

        # Game state
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.debris_timer = 0

    def spawn_orb(self):
        """Spawn a solar orb."""
        y = random.randint(50, SCREEN_HEIGHT - 50)
        orb = SolarOrb(SCREEN_WIDTH + 20, y)
        self.orbs.add(orb)
        self.all_sprites.add(orb)

    def spawn_debris(self):
        """Spawn debris obstacle."""
        y = random.randint(30, SCREEN_HEIGHT - 30)
        speed = random.uniform(2, 4)
        debris = Debris(SCREEN_WIDTH + 30, y, speed)
        self.debris_group.add(debris)
        self.all_sprites.add(debris)

    def create_particle_burst(self, x: int, y: int, color: tuple, count: int = 10):
        """Create particle effect."""
        for _ in range(count):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(1, 4)
            velocity = (
                speed * pygame.math.Vector2(1, 0).rotate(angle * 57.3).x,
                speed * pygame.math.Vector2(1, 0).rotate(angle * 57.3).y
            )
            self.particles.append(Particle(x, y, color, velocity))

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        return True

    def update(self):
        """Update game logic."""
        if self.game_over:
            return

        # Get keys
        keys = pygame.key.get_pressed()

        # Update player
        self.player.update(keys, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Update stars (parallax)
        for star in self.stars:
            star.update(SCREEN_WIDTH)

        # Update sprites
        self.orbs.update()
        self.debris_group.update()

        # Update particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()

        # Spawn orbs
        self.spawn_timer += 1
        if self.spawn_timer > random.randint(80, 150):
            self.spawn_orb()
            self.spawn_timer = 0

        # Spawn debris
        self.debris_timer += 1
        if self.debris_timer > random.randint(60, 120):
            self.spawn_debris()
            self.debris_timer = 0

        # Check collisions with orbs
        collected = pygame.sprite.spritecollide(
            self.player, self.orbs, True, pygame.sprite.collide_circle
        )
        for orb in collected:
            self.score += 10
            self.create_particle_burst(
                orb.rect.centerx, orb.rect.centery,
                (255, 220, 100), 15
            )

        # Check collisions with debris
        hit = pygame.sprite.spritecollide(
            self.player, self.debris_group, False, pygame.sprite.collide_circle
        )
        if hit:
            self.game_over = True
            self.create_particle_burst(
                self.player.rect.centerx, self.player.rect.centery,
                (255, 100, 100), 30
            )

        # Remove off-screen sprites
        for sprite in self.all_sprites:
            if hasattr(sprite, 'rect') and sprite.rect.right < -50:
                sprite.kill()

    def draw(self):
        """Draw everything."""
        # Background
        self.screen.fill(BG_COLOR)

        # Stars
        for star in self.stars:
            star.draw(self.screen)

        # Sprites
        self.all_sprites.draw(self.screen)

        # Particles
        for particle in self.particles:
            particle.draw(self.screen)

        # Score
        score_text = self.font.render(f"Solar Energy: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))

        # Instructions
        if not self.game_over:
            help_text = self.small_font.render(
                "WASD/Arrows: Move  |  ESC: Quit", True, ACCENT_COLOR
            )
            self.screen.blit(help_text, (10, SCREEN_HEIGHT - 30))

        # Game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((20, 15, 30))
            self.screen.blit(overlay, (0, 0))

            # Game over text
            game_over_text = self.font.render("MISSION FAILED", True, (255, 150, 150))
            score_text = self.font.render(f"Solar Energy Collected: {self.score}", True, TEXT_COLOR)
            restart_text = self.small_font.render("Press R to Restart  |  ESC to Quit", True, ACCENT_COLOR)

            self.screen.blit(game_over_text,
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
            self.screen.blit(score_text,
                           (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 260))
            self.screen.blit(restart_text,
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
