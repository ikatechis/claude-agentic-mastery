import math

import pygame

from config import zombie_config
from utils import load_sprite


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

        # Sprite loading (fallback to circle if sprite fails)
        sprite_size = self.radius * 2
        self.sprite_image = load_sprite(self.config.sprite_path, sprite_size)

        # Rotation state
        self.angle = 0.0  # Start facing RIGHT (sprite default orientation)
        self.original_sprite = None
        if self.sprite_image:
            self.original_sprite = self.sprite_image.copy()

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

            # Calculate target rotation from chase direction
            target_angle = math.degrees(math.atan2(-dy, dx))
            target_angle = target_angle % 360

            # Zombies rotate slower (540°/sec = 1.5 rotations/sec)
            rotation_speed = 540.0
            angle_diff = target_angle - self.angle

            # Shortest rotation path
            if angle_diff > 180:
                angle_diff -= 360
            elif angle_diff < -180:
                angle_diff += 360

            max_rotation = rotation_speed * delta_time
            if abs(angle_diff) < max_rotation:
                self.angle = target_angle
            else:
                self.angle += max_rotation if angle_diff > 0 else -max_rotation

            self.angle = self.angle % 360

    def draw(self, screen):
        """Draw the zombie with rotation

        Args:
            screen: Pygame surface to draw on
        """
        if self.original_sprite:
            # Rotate from original (avoid degradation)
            rotated_sprite = pygame.transform.rotate(self.original_sprite, self.angle)
            rect = rotated_sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_sprite, rect)
        elif self.sprite_image:
            # Fallback without rotation
            rect = self.sprite_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.sprite_image, rect)
        else:
            # Circle fallback
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
