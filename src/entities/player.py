"""
Player entity for Zombie Survival game
Handles player movement, rendering, and collision
"""
import pygame


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

        # Player properties
        self.radius = 15
        self.color = (0, 255, 0)  # Green
        self.speed = 200  # Pixels per second

        # Position (center of circle)
        self.x = float(x)
        self.y = float(y)

        # Screen boundaries
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, delta_time):
        """Update player state

        Args:
            delta_time: Time elapsed since last frame in seconds
        """
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

    def render(self, screen):
        """Draw the player

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
