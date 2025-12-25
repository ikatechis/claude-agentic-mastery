"""
Main game class for Zombie Survival
Handles the game loop, rendering, and event processing
"""

import math
import random

import pygame

from config import game_config, ui_config
from entities.player import Player
from entities.zombie import Zombie


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
            self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        )

        # Zombie management
        self.zombies = []

        # Spawn initial zombies
        for _ in range(self.config.initial_zombies):
            self.spawn_zombie()

    def handle_events(self):
        """Process game events"""
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                self.running = False

    @staticmethod
    def get_distance(entity1, entity2):
        """Calculate distance between two entities.

        Args:
            entity1: First entity (must have x, y)
            entity2: Second entity (must have x, y)

        Returns:
            float: Distance between entity centers
        """
        dx = entity1.x - entity2.x
        dy = entity1.y - entity2.y
        return math.hypot(dx, dy)

    def check_collision(self, entity1, entity2):
        """Check circle collision between two entities.

        Args:
            entity1: First entity (must have x, y, radius)
            entity2: Second entity (must have x, y, radius)

        Returns:
            bool: True if entities are colliding
        """
        distance = self.get_distance(entity1, entity2)
        # Collision if distance < sum of radii
        return distance < (entity1.radius + entity2.radius)

    def spawn_zombie(self):
        """Spawn a zombie at a random position off-screen."""
        buffer = self.config.spawn_offscreen_buffer
        side = random.choice(("top", "bottom", "left", "right"))

        if side == "top":
            x = random.randint(0, self.SCREEN_WIDTH)
            y = -buffer
        elif side == "bottom":
            x = random.randint(0, self.SCREEN_WIDTH)
            y = self.SCREEN_HEIGHT + buffer
        elif side == "left":
            x = -buffer
            y = random.randint(0, self.SCREEN_HEIGHT)
        else:  # right
            x = self.SCREEN_WIDTH + buffer
            y = random.randint(0, self.SCREEN_HEIGHT)

        self.zombies.append(Zombie(x, y))

    def update(self, delta_time):
        """Update game state

        Args:
            delta_time: Time elapsed since last frame in seconds
        """
        # Update player
        self.player.update(delta_time)

        # Update all zombies
        for zombie in self.zombies:
            zombie.update(delta_time, self.player.x, self.player.y)

        # Check player attacks
        if self.player.is_attacking:
            # Kill zombies within attack range
            survivors = []
            for zombie in self.zombies:
                if self.get_distance(self.player, zombie) <= self.player.attack_range:
                    # Zombie killed - future logic (score, sounds, etc.) goes here
                    pass
                else:
                    survivors.append(zombie)
            self.zombies = survivors

        # Check collisions with all zombies
        for zombie in self.zombies:
            if not self.check_collision(self.player, zombie):
                continue

            # Apply damage to player
            if not self.player.take_damage(zombie.damage):
                continue  # Damage on cooldown

            # Check if player died
            if not self.player.is_alive():
                self.running = False
                break

    def render(self):
        """Render the game"""
        # Fill background
        self.screen.fill(self.BACKGROUND_COLOR)

        # Render all zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)

        # Render player (on top of zombies)
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
        pygame.draw.rect(
            self.screen, self.ui_config.health_bar_bg_color, (bar_x, bar_y, bar_width, bar_height)
        )

        # Foreground (green, shows current health)
        health_width = int((self.player.health / self.player.max_health) * bar_width)
        pygame.draw.rect(
            self.screen,
            self.ui_config.health_bar_fg_color,
            (bar_x, bar_y, health_width, bar_height),
        )

        # Border
        pygame.draw.rect(
            self.screen,
            self.ui_config.health_bar_border_color,
            (bar_x, bar_y, bar_width, bar_height),
            self.ui_config.health_bar_border_width,
        )

        # Health text
        health_text = self.font.render(
            f"HP: {int(self.player.health)}/{self.player.max_health}",
            True,
            self.ui_config.text_color,
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
