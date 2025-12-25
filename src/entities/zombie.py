import math

import pygame

from config import zombie_config


class Zombie:
    """A zombie enemy that chases the player."""

    def __init__(self, x, y):
        """Initialize zombie at given position.

        Args:
            x: Starting x coordinate
            y: Starting y coordinate
        """
        # Configuration
        self.config = zombie_config

        # Position
        self.x = x
        self.y = y

        # Zombie properties
        self.radius = self.config.radius
        self.color = self.config.color
        self.speed = self.config.speed
        self.damage = self.config.damage

    def update(self, delta_time, player_x, player_y):
        """Update zombie state - chase the player.

        Args:
            delta_time: Time since last frame in seconds
            player_x: Player's x position
            player_y: Player's y position
        """
        # Calculate direction to player
        dx = player_x - self.x
        dy = player_y - self.y

        # Calculate distance
        distance = math.sqrt(dx * dx + dy * dy)

        # Only move if not already at player position
        if distance > 0:
            # Normalize direction vector
            dx /= distance
            dy /= distance

            # Move toward player
            self.x += dx * self.speed * delta_time
            self.y += dy * self.speed * delta_time

    def draw(self, screen):
        """Draw the zombie on screen.

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
