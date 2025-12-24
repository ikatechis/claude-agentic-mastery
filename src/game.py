"""
Main game class for Zombie Survival
Handles the game loop, rendering, and event processing
"""
import pygame
import math
from entities.player import Player
from entities.zombie import Zombie
from config import game_config, zombie_config, ui_config


class Game:
    """Main game class"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()

        # Game configuration
        self.config = game_config
        self.SCREEN_WIDTH = self.config.screen_width
        self.SCREEN_HEIGHT = self.config.screen_height
        self.FPS = self.config.fps
        self.BACKGROUND_COLOR = self.config.background_color

        # Create the game window
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Zombie Survival")

        # Create clock for FPS control
        self.clock = pygame.time.Clock()

        # Initialize font for UI
        pygame.font.init()
        self.ui_config = ui_config
        self.font = pygame.font.Font(None, self.ui_config.font_size)

        # Game state
        self.running = True

        # Create player at center of screen
        self.player = Player(
            self.SCREEN_WIDTH // 2,
            self.SCREEN_HEIGHT // 2,
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT
        )

        # Create a test zombie (top-left area)
        self.zombie = Zombie(150, 150)

    def handle_events(self):
        """Process game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def check_collision(self, entity1, entity2):
        """Check circle collision between two entities.

        Args:
            entity1: First entity (must have x, y, radius)
            entity2: Second entity (must have x, y, radius)

        Returns:
            bool: True if entities are colliding
        """
        # Calculate distance between centers
        dx = entity1.x - entity2.x
        dy = entity1.y - entity2.y
        distance = math.sqrt(dx * dx + dy * dy)

        # Collision if distance < sum of radii
        return distance < (entity1.radius + entity2.radius)

    def update(self, delta_time):
        """Update game state

        Args:
            delta_time: Time elapsed since last frame in seconds
        """
        # Update player
        self.player.update(delta_time)

        # Update zombie (pass player position for chasing)
        self.zombie.update(delta_time, self.player.x, self.player.y)

        # Check collision between player and zombie
        if self.check_collision(self.player, self.zombie):
            # Apply damage to player
            if self.player.take_damage(self.zombie.damage):
                # Damage was applied (not on cooldown)
                if not self.player.is_alive():
                    # Player died - game over
                    self.running = False

    def render(self):
        """Render the game"""
        # Fill background
        self.screen.fill(self.BACKGROUND_COLOR)

        # Render zombie
        self.zombie.draw(self.screen)

        # Render player (on top of zombie)
        self.player.render(self.screen)

        # Render health bar
        self.render_health_bar()

        # Update display
        pygame.display.flip()

    def render_health_bar(self):
        """Draw the player's health bar (responsive to screen size)"""
        # Calculate position based on screen dimensions
        bar_x = int(self.SCREEN_WIDTH * self.ui_config.health_bar_x_ratio)
        bar_y = int(self.SCREEN_HEIGHT * self.ui_config.health_bar_y_ratio)
        bar_width = int(self.SCREEN_WIDTH * self.ui_config.health_bar_width_ratio)
        bar_height = self.ui_config.health_bar_height

        # Background (red, shows missing health)
        pygame.draw.rect(self.screen, self.ui_config.health_bar_bg_color,
                        (bar_x, bar_y, bar_width, bar_height))

        # Foreground (green, shows current health)
        health_width = int((self.player.health / self.player.max_health) * bar_width)
        pygame.draw.rect(self.screen, self.ui_config.health_bar_fg_color,
                        (bar_x, bar_y, health_width, bar_height))

        # Border
        pygame.draw.rect(self.screen, self.ui_config.health_bar_border_color,
                        (bar_x, bar_y, bar_width, bar_height),
                        self.ui_config.health_bar_border_width)

        # Health text
        health_text = self.font.render(
            f"HP: {int(self.player.health)}/{self.player.max_health}",
            True,
            self.ui_config.text_color
        )
        self.screen.blit(health_text, (bar_x + bar_width + 10, bar_y))

    def run(self):
        """Main game loop"""
        while self.running:
            # Get delta time in seconds
            delta_time = self.clock.tick(self.FPS) / 1000.0

            # Process events
            self.handle_events()

            # Update game state
            self.update(delta_time)

            # Render
            self.render()

        # Cleanup
        pygame.quit()
