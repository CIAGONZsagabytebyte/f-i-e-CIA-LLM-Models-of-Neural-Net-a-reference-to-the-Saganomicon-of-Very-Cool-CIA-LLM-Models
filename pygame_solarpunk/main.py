#!/usr/bin/env python3
"""
Solarpunk Space - Pygame Prototype v2
A playable 2D space game with solarpunk aesthetics.
Fly your ship, collect Solar Orbs, and avoid debris.
"""

import pygame
import sys
from game_objects import Player, SolarOrb, Debris, Star

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (Solarpunk palette)
SPACE_BLACK = (10, 10, 20)
TEAL = (76, 215, 177)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Solarpunk Space - Collect Solar Energy!")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.score = 0

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.solar_orbs = pygame.sprite.Group()
        self.debris = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        # Create background stars
        for _ in range(100):
            star = Star(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.stars.add(star)
            self.all_sprites.add(star)

        # Create player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.all_sprites.add(self.player)

        # Spawn initial objects
        self.spawn_timer = 0

        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def spawn_objects(self):
        """Spawn solar orbs and debris."""
        import random

        # Spawn solar orb
        if random.random() < 0.02:
            orb = SolarOrb(random.randint(20, SCREEN_WIDTH - 20), -20)
            self.solar_orbs.add(orb)
            self.all_sprites.add(orb)

        # Spawn debris
        if random.random() < 0.015:
            debris_obj = Debris(random.randint(20, SCREEN_WIDTH - 20), -20)
            self.debris.add(debris_obj)
            self.all_sprites.add(debris_obj)

    def check_collisions(self):
        """Check for collisions."""
        # Player collects solar orbs
        orb_hits = pygame.sprite.spritecollide(self.player, self.solar_orbs, True)
        for orb in orb_hits:
            self.score += 10

        # Player hits debris
        debris_hits = pygame.sprite.spritecollide(self.player, self.debris, False)
        if debris_hits:
            self.game_over = True

    def run(self):
        """Main game loop."""
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_over and event.key == pygame.K_RETURN:
                        self.__init__()  # Restart game

            if not self.game_over:
                # Update
                self.all_sprites.update()
                self.spawn_objects()
                self.check_collisions()

            # Draw
            self.screen.fill(SPACE_BLACK)
            self.all_sprites.draw(self.screen)

            # Draw UI
            score_text = self.font.render(f"Solar Energy: {self.score}", True, TEAL)
            self.screen.blit(score_text, (10, 10))

            if self.game_over:
                game_over_text = self.font.render("SHIP DAMAGED!", True, GOLD)
                restart_text = self.small_font.render("Press ENTER to restart", True, WHITE)

                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

                self.screen.blit(game_over_text, text_rect)
                self.screen.blit(restart_text, restart_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
