"""Power-up collectibles that enhance player abilities."""

import random
from enum import Enum, auto

import pygame

from config import powerup_config
from logger import get_logger
from utils import load_sprite

logger = get_logger(__name__)


class PowerupType(Enum):
    """Types of power-ups available in the game."""

    HEALTH = auto()  # Restores player health
    SPEED = auto()  # Temporarily increases movement speed
    SHIELD = auto()  # Blocks incoming damage


class Powerup:
    """A collectible power-up that spawns when zombies are killed."""

    def __init__(self, x: float, y: float, powerup_type: PowerupType | None = None):
        """Initialize a power-up at the given position.

        Args:
            x: Starting x coordinate
            y: Starting y coordinate
            powerup_type: Type of power-up (random if None)
        """
        # Configuration
        self.config = powerup_config

        # Position
        self.x = x
        self.y = y
        self.radius = self.config.radius

        # Determine type (random if not specified)
        self.powerup_type = powerup_type or random.choice(list(PowerupType))

        # Visual properties based on type
        self.color = self._get_color()

        # Sprite loading (fallback to circle if sprite fails)
        sprite_size = self.radius * 2
        sprite_path = self._get_sprite_path()
        self.sprite_image = load_sprite(sprite_path, sprite_size)

        # Lifetime management
        self.lifetime = self.config.lifetime
        self.is_visible = True  # For blink animation

        # Blink state (used during warning phase)
        self.blink_timer = 0.0

        logger.debug(f"Powerup spawned: {self.powerup_type.name} at ({int(x)}, {int(y)})")

    def _get_color(self) -> tuple:
        """Get the color for this power-up type."""
        if self.powerup_type == PowerupType.HEALTH:
            return self.config.health_color
        elif self.powerup_type == PowerupType.SPEED:
            return self.config.speed_color
        else:  # SHIELD
            return self.config.shield_color

    def _get_sprite_path(self) -> str:
        """Get the sprite path for this power-up type."""
        # 64x64 sprites with transparent backgrounds
        if self.powerup_type == PowerupType.HEALTH:
            return "assets/sprites/powerup_health.png"  # Green health potion
        elif self.powerup_type == PowerupType.SPEED:
            return "assets/sprites/powerup_speed.png"  # Cyan lightning bolt
        else:  # SHIELD
            return "assets/sprites/powerup_shield.png"  # Golden shield

    def update(self, delta_time: float) -> bool:
        """Update power-up state (lifetime countdown, blink animation).

        Args:
            delta_time: Time since last frame in seconds

        Returns:
            False if power-up has expired, True otherwise
        """
        # Countdown lifetime
        self.lifetime -= delta_time

        # Check if expired
        if self.lifetime <= 0:
            logger.debug(f"Powerup expired: {self.powerup_type.name}")
            return False

        # Handle blink warning in final seconds
        if self.lifetime <= self.config.warning_duration:
            self.blink_timer += delta_time

            # Toggle visibility every half blink cycle
            if self.blink_timer >= self.config.blink_frequency / 2:
                self.is_visible = not self.is_visible
                self.blink_timer = 0.0

        return True

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the power-up (skip if in blink-off state).

        Args:
            screen: Pygame surface to draw on
        """
        # Skip rendering if blinking off
        if not self.is_visible:
            return

        # Draw sprite or fallback to colored circle
        if self.sprite_image:
            rect = self.sprite_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.sprite_image, rect)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def apply_effect(self, player) -> dict:
        """Apply this power-up's effect to the player.

        Args:
            player: The player entity to affect

        Returns:
            Dictionary with effect details for visual feedback
            (e.g., {"type": "health", "amount": 40})
        """
        if self.powerup_type == PowerupType.HEALTH:
            # Restore random amount of health
            restore_amount = random.randint(
                self.config.health_restore_min, self.config.health_restore_max
            )
            old_health = player.health
            player.health = min(player.max_health, player.health + restore_amount)
            actual_restored = player.health - old_health

            logger.debug(f"Powerup collected: HEALTH restored {int(actual_restored)} HP")
            return {"type": "health", "amount": actual_restored, "color": self.color}

        elif self.powerup_type == PowerupType.SPEED:
            # Apply speed boost for random duration
            duration = random.uniform(
                self.config.speed_duration_min, self.config.speed_duration_max
            )
            player.apply_speed_boost(self.config.speed_multiplier, duration)

            logger.debug(f"Powerup collected: SPEED {duration:.1f}s")
            return {"type": "speed", "duration": duration, "color": self.color}

        else:  # SHIELD
            # Add shield hits
            player.apply_shield(self.config.shield_hits)

            logger.debug(f"Powerup collected: SHIELD {self.config.shield_hits} hits")
            return {"type": "shield", "hits": self.config.shield_hits, "color": self.color}
