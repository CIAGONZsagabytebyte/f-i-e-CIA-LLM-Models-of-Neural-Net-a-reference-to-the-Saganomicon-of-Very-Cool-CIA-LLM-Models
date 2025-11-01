"""
Solarpunk Space Starter Kit - Pygame Prototype v2
A playable 2D space game with solarpunk aesthetics
Pure algorithmic implementation - no neural networks or ML
"""

import pygame
import random
import sys
from game_objects import Player, SolarOrb, Debris, Star, ParticleEffect

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (10, 5, 30)  # Deep space blue

# Game states
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"


class SolarpunkSpaceGame:
    """Main game class"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Solarpunk Space Starter Kit - v2")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.reset_game()

    def reset_game(self):
        """Reset game to initial state"""
        self.state = STATE_PLAYING
        self.score = 0
        self.player = Player(100, SCREEN_HEIGHT // 2)

        # Create background stars (3 layers for parallax)
        self.stars = []
        for layer in range(3):
            for _ in range(50):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                self.stars.append(Star(x, y, layer))

        # Create solar orbs
        self.orbs = []
        self.spawn_orbs(5)

        # Create debris
        self.debris = []
        self.spawn_debris(3)

        # Particle effects
        self.particles = []

        # Timers
        self.orb_spawn_timer = 0
        self.debris_spawn_timer = 0

    def spawn_orbs(self, count):
        """Spawn solar orbs at random positions"""
        for _ in range(count):
            x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.orbs.append(SolarOrb(x, y))

    def spawn_debris(self, count):
        """Spawn debris at random positions"""
        for _ in range(count):
            x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            size = random.randint(15, 30)
            self.debris.append(Debris(x, y, size))

    def check_collisions(self):
        """Check for all game collisions"""
        player_rect = self.player.get_rect()

        # Check orb collection
        for orb in self.orbs[:]:
            if player_rect.colliderect(orb.get_rect()):
                self.orbs.remove(orb)
                self.score += 10
                # Create particle effect
                self.particles.append(
                    ParticleEffect(orb.x, orb.y, (255, 220, 100), 15)
                )

        # Check debris collision (game over)
        for debris in self.debris:
            if player_rect.colliderect(debris.get_rect()):
                self.state = STATE_GAME_OVER
                # Create explosion effect
                self.particles.append(
                    ParticleEffect(self.player.x, self.player.y, (255, 100, 50), 30)
                )

    def update(self):
        """Update game state"""
        if self.state == STATE_PLAYING:
            # Get input
            keys = pygame.key.get_pressed()
            self.player.move(keys, SCREEN_WIDTH, SCREEN_HEIGHT)

            # Update stars
            for star in self.stars:
                star.update(SCREEN_WIDTH)

            # Update orbs
            for orb in self.orbs:
                orb.update()

            # Update debris
            for debris in self.debris[:]:
                debris.update()
                if debris.is_off_screen():
                    self.debris.remove(debris)

            # Update particles
            for particle in self.particles[:]:
                particle.update()
                if particle.is_finished():
                    self.particles.remove(particle)

            # Check collisions
            self.check_collisions()

            # Spawn new orbs
            self.orb_spawn_timer += 1
            if self.orb_spawn_timer > 120 and len(self.orbs) < 8:
                self.spawn_orbs(1)
                self.orb_spawn_timer = 0

            # Spawn new debris
            self.debris_spawn_timer += 1
            if self.debris_spawn_timer > 90:
                self.spawn_debris(1)
                self.debris_spawn_timer = 0

    def draw(self):
        """Draw all game elements"""
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)

        # Draw stars (parallax background)
        for star in self.stars:
            star.draw(self.screen)

        # Draw orbs
        for orb in self.orbs:
            orb.draw(self.screen)

        # Draw debris
        for debris in self.debris:
            debris.draw(self.screen)

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)

        # Draw player
        if self.state == STATE_PLAYING:
            self.player.draw(self.screen)

        # Draw UI
        self.draw_ui()

        # Draw game over screen
        if self.state == STATE_GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_ui(self):
        """Draw score and instructions"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, (100, 255, 150))
        self.screen.blit(score_text, (10, 10))

        # Instructions
        if self.score == 0:
            instructions = [
                "WASD/Arrows: Move",
                "Collect Solar Orbs (yellow)",
                "Avoid Debris (brown)"
            ]
            y_offset = SCREEN_HEIGHT - 80
            for instruction in instructions:
                text = self.small_font.render(instruction, True, (150, 150, 150))
                self.screen.blit(text, (10, y_offset))
                y_offset += 25

    def draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Game over text
        game_over_text = self.font.render("GAME OVER", True, (255, 100, 100))
        rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, rect)

        # Final score
        final_score = self.font.render(f"Final Score: {self.score}", True, (100, 255, 150))
        rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(final_score, rect)

        # Restart instruction
        restart_text = self.small_font.render("Press SPACE to restart or ESC to quit", True, (200, 200, 200))
        rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, rect)

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

        return True

    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    game = SolarpunkSpaceGame()
    game.run()


if __name__ == "__main__":
    main()
