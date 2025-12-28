"""
Player entity for Zombie Survival game
Handles player movement, rendering, and collision
"""

import pygame

from config import player_config
from logger import get_logger
from utils import load_sprite

logger = get_logger(__name__)


class Player(pygame.sprite.Sprite):
    """Player character with WASD movement"""

    def __init__(self, x, y, screen_width, screen_height):
        """Initialize the player

        Args:
            x: Initial x position
            y: Initial y position
            screen_width: Width of the game screen
            screen_height: Height of the game screen
        """
        super().__init__()

        # Configuration
        self.config = player_config

        # Player properties
        self.radius = self.config.radius
        self.color = self.config.color
        self.speed = self.config.speed

        # Position (center of circle)
        self.x = float(x)
        self.y = float(y)

        # Screen boundaries
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Health system
        self.max_health = self.config.max_health
        self.health: float = float(self.max_health)
        self.damage_cooldown = 0.0  # Seconds until can take damage again
        self.damage_cooldown_time = self.config.damage_cooldown

        # Attack system
        self.attack_range = self.config.attack_range
        self.attack_cooldown = 0.0  # Seconds until can attack again
        self.attack_cooldown_time = self.config.attack_cooldown
        self.is_attacking = False  # True during attack frame

        # Power-up effects
        self.speed_multiplier = 1.0  # Speed boost multiplier (1.0 = normal)
        self.speed_boost_timer = 0.0  # Seconds remaining for speed boost
        self.shield_hits_remaining = 0  # Number of hits shield can block

        # Sprite loading (fallback to circle if sprite fails)
        sprite_size = self.radius * 2
        self.sprite_image = load_sprite(self.config.sprite_path, sprite_size)

        # Rotation state
        self.angle = 0.0  # Start facing RIGHT (sprite default orientation)
        self.original_sprite = None
        if self.sprite_image:
            self.original_sprite = self.sprite_image.copy()

    def update(self, delta_time):
        """Update player state

        Args:
            delta_time: Time elapsed since last frame in seconds
        """
        # Update damage cooldown
        if self.damage_cooldown > 0:
            self.damage_cooldown -= delta_time

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

        # Update speed boost timer
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= delta_time
            if self.speed_boost_timer <= 0:
                self.speed_multiplier = 1.0  # Reset to normal speed

        # Reset attack state
        self.is_attacking = False

        # Get keyboard state
        keys = pygame.key.get_pressed()

        # Handle attack
        if keys[pygame.K_SPACE] and self.attack_cooldown <= 0:
            self.attack()

        # Calculate movement delta
        dx = 0.0
        dy = 0.0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        # Normalize diagonal movement to prevent faster diagonal speed
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071

        # Apply movement (frame-independent using delta_time)
        # Speed multiplier allows power-ups to temporarily boost speed
        self.x += dx * self.speed * self.speed_multiplier * delta_time
        self.y += dy * self.speed * self.speed_multiplier * delta_time

        # Keep player within screen boundaries
        self.x = max(self.radius, min(self.x, self.screen_width - self.radius))
        self.y = max(self.radius, min(self.y, self.screen_height - self.radius))

        # Calculate target rotation from movement
        if dx != 0 or dy != 0:
            # atan2(-dy, dx) accounts for inverted Y-axis in pygame
            import math

            target_angle = math.degrees(math.atan2(-dy, dx))
            target_angle = target_angle % 360

            # Smooth rotation (720°/sec = 2 full rotations per second)
            rotation_speed = 720.0
            angle_diff = target_angle - self.angle

            # Shortest rotation path (handle 359° -> 1° wrap)
            if angle_diff > 180:
                angle_diff -= 360
            elif angle_diff < -180:
                angle_diff += 360

            # Apply rotation
            max_rotation = rotation_speed * delta_time
            if abs(angle_diff) < max_rotation:
                self.angle = target_angle
            else:
                self.angle += max_rotation if angle_diff > 0 else -max_rotation

            self.angle = self.angle % 360
        # When idle (dx==0, dy==0), keep last angle

    def take_damage(self, amount):
        """Apply damage to the player (shield blocks if active).

        Args:
            amount: Damage amount to apply

        Returns:
            bool: True if hit occurred (damage or shield block), False if on cooldown
        """
        if self.damage_cooldown <= 0:
            # Check if shield is active
            if self.shield_hits_remaining > 0:
                # Shield blocks the damage
                self.shield_hits_remaining -= 1
                self.damage_cooldown = self.damage_cooldown_time
                logger.debug(f"Shield blocked damage, {self.shield_hits_remaining} hits remaining")
                return True  # Hit was blocked by shield
            else:
                # No shield, apply damage
                self.health -= amount
                self.health = max(0.0, self.health)  # Don't go below 0
                self.damage_cooldown = self.damage_cooldown_time
                logger.debug(f"Took {amount} damage, health: {int(self.health)}/{self.max_health}")
                return True
        return False

    def is_alive(self):
        """Check if player is still alive.

        Returns:
            bool: True if health > 0
        """
        return self.health > 0

    def attack(self):
        """Perform melee attack.

        Sets is_attacking flag and starts cooldown.
        Game loop should check this flag to kill nearby zombies.
        """
        self.is_attacking = True
        self.attack_cooldown = self.attack_cooldown_time
        logger.debug(f"Player attacked (range: {self.attack_range})")

    def apply_speed_boost(self, multiplier: float, duration: float) -> None:
        """Apply a speed boost effect.

        Args:
            multiplier: Speed multiplier (e.g., 1.5 for 50% faster)
            duration: How long the boost lasts in seconds
        """
        self.speed_multiplier = multiplier
        self.speed_boost_timer = duration
        logger.debug(f"Speed boost applied: {multiplier}x for {duration}s")

    def apply_shield(self, hits: int) -> None:
        """Apply a shield that blocks incoming damage.

        Args:
            hits: Number of hits the shield can block
        """
        self.shield_hits_remaining += hits
        logger.debug(f"Shield applied: {hits} hits, total: {self.shield_hits_remaining}")

    def has_shield(self) -> bool:
        """Check if player currently has an active shield.

        Returns:
            True if shield has remaining hits
        """
        return self.shield_hits_remaining > 0

    def has_speed_boost(self) -> bool:
        """Check if player currently has an active speed boost.

        Returns:
            True if speed boost timer is active
        """
        return self.speed_boost_timer > 0

    def render(self, screen):
        """Draw the player with rotation

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
