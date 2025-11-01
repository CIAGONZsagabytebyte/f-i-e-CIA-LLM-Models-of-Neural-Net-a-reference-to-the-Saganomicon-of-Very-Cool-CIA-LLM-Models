#!/usr/bin/env python3
"""
Solarpunk Space Starter Kit - Pygame Prototype v2
A playable demo using mathematical transformations (NO NEURONS!)

Mathematical Foundation:
- Complex number rotations: z * e^(iθ)
- Ring theory: toroidal wrapping via modular arithmetic
- Harmonic oscillators: f(t) = A·sin(ωt)
- Affine transformations: parallax scrolling

Controls:
- Arrow Keys / WASD: Move ship
- ESC: Quit
- R: Restart after game over
"""

import pygame
import sys
import random
from game_objects import (
    Player, SolarOrb, Debris, ParallaxStar,
    check_collision, ComplexTransform
)


class SolarpunkSpaceGame:
    """Main game class using functional paradigm"""

    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Solarpunk Space - Ring-0 Edition")

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.score = 0
        self.high_score = 0

        # Colors - Solarpunk palette
        self.bg_color = (10, 5, 25)  # Deep space
        self.text_color = (150, 255, 180)

        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Initialize game objects
        self.reset_game()

    def reset_game(self):
        """Reset game state using functional initialization"""
        self.game_over = False
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0

        # Player
        self.player = Player(self.screen_width // 2, self.screen_height // 2)

        # Solar Orbs (collectibles)
        self.solar_orbs = []
        for _ in range(8):
            x = random.randint(50, self.screen_width - 50)
            y = random.randint(50, self.screen_height - 50)
            self.solar_orbs.append(SolarOrb(x, y))

        # Debris (obstacles)
        self.debris_list = []
        for _ in range(5):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            vx = random.uniform(-30, 30)
            vy = random.uniform(-30, 30)
            self.debris_list.append(Debris(x, y, vx, vy))

        # Parallax stars
        self.stars = []
        for _ in range(100):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            depth = random.random()
            self.stars.append(ParallaxStar(x, y, depth))

    def spawn_solar_orb(self):
        """Spawn new orb using random transformation"""
        x = random.randint(50, self.screen_width - 50)
        y = random.randint(50, self.screen_height - 50)
        self.solar_orbs.append(SolarOrb(x, y))

    def handle_events(self):
        """Event handling - pure function mapping events to actions"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()

    def update(self, dt: float):
        """Update game state using functional composition"""
        if self.game_over:
            return

        # Update player
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, dt)
        self.player.update(dt, self.screen_width, self.screen_height)

        # Update stars with parallax
        for star in self.stars:
            star.update(self.player.velocity_x, self.player.velocity_y, dt)
            # Wrap stars using ring kernel
            star.x = ComplexTransform.ring_kernel(star.x, self.screen_width)
            star.y = ComplexTransform.ring_kernel(star.y, self.screen_height)

        # Update solar orbs
        for orb in self.solar_orbs[:]:
            orb.update(dt)
            # Check collection
            if check_collision(self.player, orb):
                self.solar_orbs.remove(orb)
                self.score += 10
                self.spawn_solar_orb()

        # Update debris
        for debris in self.debris_list:
            debris.update(dt, self.screen_width, self.screen_height)
            # Check collision
            if check_collision(self.player, debris):
                self.game_over = True

    def draw(self):
        """Render game state - pure visual transform"""
        self.screen.fill(self.bg_color)

        # Draw stars
        for star in self.stars:
            star.draw(self.screen)

        # Draw solar orbs
        for orb in self.solar_orbs:
            orb.draw(self.screen)

        # Draw debris
        for debris in self.debris_list:
            debris.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        # Draw UI
        score_text = self.font.render(f"Energy: {self.score}", True, self.text_color)
        self.screen.blit(score_text, (10, 10))

        high_score_text = self.small_font.render(
            f"High: {self.high_score}", True, self.text_color
        )
        self.screen.blit(high_score_text, (10, 50))

        # Draw instructions
        if not self.game_over:
            help_text = self.small_font.render(
                "Collect Solar Orbs | Avoid Debris", True, (100, 200, 150)
            )
            self.screen.blit(help_text, (10, self.screen_height - 30))

        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("SYSTEM CRASH", True, (255, 100, 100))
            rect = game_over_text.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 - 50)
            )
            self.screen.blit(game_over_text, rect)

            final_score = self.font.render(
                f"Final Energy: {self.score}", True, self.text_color
            )
            rect = final_score.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2)
            )
            self.screen.blit(final_score, rect)

            restart_text = self.small_font.render(
                "Press R to Restart | ESC to Quit", True, self.text_color
            )
            rect = restart_text.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 + 50)
            )
            self.screen.blit(restart_text, rect)

        pygame.display.flip()

    def run(self):
        """Main game loop - functional iteration"""
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


def main():
    """Entry point - pure function"""
    print("=" * 60)
    print("SOLARPUNK SPACE STARTER KIT - v2")
    print("Mathematical Foundation: Ring Theory & Complex Transforms")
    print("NO NEURONS | NO UNITS | Pure Functional Design")
    print("=" * 60)
    print("\nControls:")
    print("  Arrow Keys / WASD: Move ship")
    print("  ESC: Quit")
    print("  R: Restart after game over")
    print("\nf(i) = -i | Ring-0 Control | Saga Gonzo Edition")
    print("=" * 60)

    game = SolarpunkSpaceGame()
    game.run()


if __name__ == "__main__":
    main()
