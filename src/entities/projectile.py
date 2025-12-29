"""Projectile entity for ranged attacks."""

import math

import pygame

from config import projectile_config
from logger import get_logger
from utils import load_sprite

logger = get_logger(__name__)


class Projectile:
    """A projectile entity (bullet) fired by the player."""

    def __init__(self, x: float, y: float, angle: float):
        """Initialize projectile at position with direction.

        Args:
            x: Spawn X position (player center)
            y: Spawn Y position (player center)
            angle: Direction in degrees (0° = right, 90° = up, 180° = left, 270° = down)
        """
        # Position
        self.x = x
        self.y = y

        # Configuration
        self.config = projectile_config

        # Convert angle to velocity (handle pygame Y-axis inversion)
        angle_rad = math.radians(angle)
        self.velocity_x = math.cos(angle_rad) * self.config.speed
        self.velocity_y = -math.sin(angle_rad) * self.config.speed  # Negative for upward

        # State
        self.age = 0.0  # Seconds since spawn
        self.alive = True

        # Sprite loading (fallback to circle if sprite fails)
        sprite_size = self.config.radius * 2
        self.sprite_image = load_sprite(self.config.sprite_path, sprite_size)

        # Store original sprite for potential rotation
        self.original_sprite = None
        if self.sprite_image:
            self.original_sprite = self.sprite_image.copy()

        logger.debug(f"Projectile spawned at ({int(x)}, {int(y)}) angle={angle}°")

    def update(self, delta_time: float) -> None:
        """Update projectile position and lifetime.

        Args:
            delta_time: Time since last frame (seconds)
        """
        if not self.alive:
            return

        # Frame-independent movement
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time

        # Track lifetime
        self.age += delta_time
        if self.age >= self.config.lifetime:
            self.alive = False
            logger.debug(f"Projectile expired at ({int(self.x)}, {int(self.y)})")

    def render(self, screen: pygame.Surface) -> None:
        """Render projectile to screen.

        Args:
            screen: Pygame surface to draw on
        """
        if not self.alive:
            return

        # Draw sprite or fallback to circle
        if self.sprite_image:
            rect = self.sprite_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.sprite_image, rect)
        else:
            pygame.draw.circle(
                screen, self.config.color, (int(self.x), int(self.y)), self.config.radius
            )

    def check_collision(self, other_x: float, other_y: float, other_radius: int) -> bool:
        """Check circle collision with another entity.

        Args:
            other_x: Other entity X position
            other_y: Other entity Y position
            other_radius: Other entity collision radius

        Returns:
            True if entities are colliding
        """
        # Calculate distance between centers
        dx = self.x - other_x
        dy = self.y - other_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Collision if distance < sum of radii
        return distance < (self.config.radius + other_radius)

    def mark_for_removal(self) -> None:
        """Mark projectile as dead (hit target or expired)."""
        self.alive = False
        logger.debug(f"Projectile hit target at ({int(self.x)}, {int(self.y)})")

    def is_alive(self) -> bool:
        """Check if projectile should remain in game.

        Returns:
            True if projectile is still active
        """
        return self.alive
