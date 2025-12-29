"""Power-up collectibles that enhance player abilities."""

import math
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
    AMMO = auto()  # Restores ammunition


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

        # Determine type (weighted random if not specified)
        if powerup_type:
            self.powerup_type = powerup_type
        else:
            # Use weighted random selection (AMMO is 3x more likely)
            types = list(PowerupType)
            weights = [self.config.powerup_weights[t.name] for t in types]
            self.powerup_type = random.choices(types, weights=weights)[0]

        # Visual properties based on type
        self.color = self._get_color()

        # Sprite loading (fallback to circle if sprite fails)
        sprite_size = self.radius * 2
        sprite_path = self._get_sprite_path()
        self.sprite_image = load_sprite(sprite_path, sprite_size)

        # Animation state
        self.rotation_angle = 0.0  # Current rotation angle (degrees)
        self.bob_timer = 0.0  # Timer for bobbing animation
        self.original_sprite = None  # Store unrotated sprite
        if self.sprite_image:
            self.original_sprite = self.sprite_image.copy()

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
        elif self.powerup_type == PowerupType.SHIELD:
            return self.config.shield_color
        else:  # AMMO
            return self.config.ammo_color

    def _get_sprite_path(self) -> str:
        """Get the sprite path for this power-up type."""
        # 64x64 sprites with transparent backgrounds
        if self.powerup_type == PowerupType.HEALTH:
            return "assets/sprites/powerup_health.png"  # Green health potion
        elif self.powerup_type == PowerupType.SPEED:
            return "assets/sprites/powerup_speed.png"  # Cyan lightning bolt
        elif self.powerup_type == PowerupType.SHIELD:
            return "assets/sprites/powerup_shield.png"  # Golden shield
        else:  # AMMO
            return "assets/sprites/powerup_ammo.png"  # Orange ammo box

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

        # Animate rotation (spin continuously)
        self.rotation_angle += self.config.rotation_speed * delta_time
        self.rotation_angle = self.rotation_angle % 360  # Keep 0-360

        # Animate bobbing (up/down movement)
        self.bob_timer += delta_time

        # Handle blink warning in final seconds
        if self.lifetime <= self.config.warning_duration:
            self.blink_timer += delta_time

            # Toggle visibility every half blink cycle
            if self.blink_timer >= self.config.blink_frequency / 2:
                self.is_visible = not self.is_visible
                self.blink_timer = 0.0

        return True

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the power-up with rotation and bobbing animation.

        Args:
            screen: Pygame surface to draw on
        """
        # Skip rendering if blinking off
        if not self.is_visible:
            return

        # Calculate bobbing offset (vertical movement using sin wave)
        bob_offset = (
            math.sin(self.bob_timer * self.config.bob_speed * 2 * math.pi) * self.config.bob_height
        )

        # Draw sprite or fallback to colored circle
        if self.original_sprite:
            # Rotate sprite and apply bobbing
            rotated = pygame.transform.rotate(self.original_sprite, self.rotation_angle)
            rect = rotated.get_rect(center=(int(self.x), int(self.y + bob_offset)))
            screen.blit(rotated, rect)
        elif self.sprite_image:
            # Fallback without rotation (but with bobbing)
            rect = self.sprite_image.get_rect(center=(int(self.x), int(self.y + bob_offset)))
            screen.blit(self.sprite_image, rect)
        else:
            # Circle fallback with bobbing
            pygame.draw.circle(
                screen, self.color, (int(self.x), int(self.y + bob_offset)), self.radius
            )

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

        elif self.powerup_type == PowerupType.SHIELD:
            # Add shield hits
            player.apply_shield(self.config.shield_hits)

            logger.debug(f"Powerup collected: SHIELD {self.config.shield_hits} hits")
            return {"type": "shield", "hits": self.config.shield_hits, "color": self.color}

        else:  # AMMO
            # Restore random amount of ammunition to stash (reserve)
            restore_amount = random.randint(
                self.config.ammo_restore_min, self.config.ammo_restore_max
            )
            old_stash = player.stash
            player.stash = min(player.max_stash, player.stash + restore_amount)
            actual_restored = player.stash - old_stash

            logger.debug(f"Powerup collected: AMMO restored {actual_restored} rounds to stash")
            return {"type": "ammo", "amount": actual_restored, "color": self.color}
