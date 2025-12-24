"""
Player entity for Zombie Survival game
Handles player movement, rendering, and collision
"""
import pygame
from config import player_config


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
        self.health = self.max_health
        self.damage_cooldown = 0  # Seconds until can take damage again
        self.damage_cooldown_time = self.config.damage_cooldown

    def update(self, delta_time):
        """Update player state

        Args:
            delta_time: Time elapsed since last frame in seconds
        """
        # Update damage cooldown
        if self.damage_cooldown > 0:
            self.damage_cooldown -= delta_time

        # Get keyboard state
        keys = pygame.key.get_pressed()

        # Calculate movement delta
        dx = 0
        dy = 0

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
        self.x += dx * self.speed * delta_time
        self.y += dy * self.speed * delta_time

        # Keep player within screen boundaries
        self.x = max(self.radius, min(self.x, self.screen_width - self.radius))
        self.y = max(self.radius, min(self.y, self.screen_height - self.radius))

    def take_damage(self, amount):
        """Apply damage to the player.

        Args:
            amount: Damage amount to apply

        Returns:
            bool: True if damage was applied, False if on cooldown
        """
        if self.damage_cooldown <= 0:
            self.health -= amount
            self.health = max(0, self.health)  # Don't go below 0
            self.damage_cooldown = self.damage_cooldown_time
            return True
        return False

    def is_alive(self):
        """Check if player is still alive.

        Returns:
            bool: True if health > 0
        """
        return self.health > 0

    def render(self, screen):
        """Draw the player

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
