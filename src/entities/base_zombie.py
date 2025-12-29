"""Base zombie class with shared logic for all zombie variants."""

import math

import pygame

from logger import get_logger
from utils import load_sprite

logger = get_logger(__name__)


class BaseZombie:
    """Base class for all zombie variants with shared movement and rendering logic."""

    def __init__(self, x: float, y: float, config, rotation_speed: float = 540.0):
        """Initialize zombie at given position.

        Args:
            x: Starting x coordinate
            y: Starting y coordinate
            config: Zombie configuration (ZombieConfig, FastZombieConfig, etc.)
            rotation_speed: Degrees per second for rotation (default: 540)
        """
        # Configuration
        self.config = config

        # Position
        self.x = x
        self.y = y

        # Zombie properties from config
        self.radius = self.config.radius
        self.color = self.config.color
        self.speed = self.config.speed
        self.damage = self.config.damage

        # Health system (if config has health attribute)
        if hasattr(self.config, "health"):
            self.max_health = self.config.health
            self.health = self.max_health
        else:
            self.max_health = None
            self.health = None

        # Sprite loading (fallback to circle if sprite fails)
        sprite_size = self.radius * 2
        self.sprite_image = load_sprite(self.config.sprite_path, sprite_size)

        # Rotation state
        self.angle = 0.0  # Start facing RIGHT (sprite default orientation)
        self.rotation_speed = rotation_speed
        self.original_sprite = None
        if self.sprite_image:
            self.original_sprite = self.sprite_image.copy()

        # Log spawn with health if applicable
        if self.health is not None:
            logger.debug(
                f"{self.__class__.__name__} spawned at ({int(x)}, {int(y)}) - HP: {self.health}/{self.max_health}"
            )
        else:
            logger.debug(f"{self.__class__.__name__} spawned at ({int(x)}, {int(y)})")

    def take_damage(self, amount: int) -> bool:
        """Take damage and return True if still alive.

        Args:
            amount: Damage to take

        Returns:
            True if zombie is still alive after damage, False if dead
        """
        if self.health is None:
            # Zombies without health system die in one hit
            logger.debug(f"{self.__class__.__name__} died at ({int(self.x)}, {int(self.y)})")
            return False

        self.health -= amount
        logger.debug(
            f"{self.__class__.__name__} took {amount} damage, health: {self.health}/{self.max_health}"
        )

        if self.health <= 0:
            logger.debug(f"{self.__class__.__name__} died at ({int(self.x)}, {int(self.y)})")
            return False
        return True

    def update(self, delta_time: float, player_x: float, player_y: float) -> None:
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

            # Smooth rotation
            angle_diff = target_angle - self.angle

            # Shortest rotation path
            if angle_diff > 180:
                angle_diff -= 360
            elif angle_diff < -180:
                angle_diff += 360

            max_rotation = self.rotation_speed * delta_time
            if abs(angle_diff) < max_rotation:
                self.angle = target_angle
            else:
                self.angle += max_rotation if angle_diff > 0 else -max_rotation

            self.angle = self.angle % 360

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the zombie with rotation.

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
