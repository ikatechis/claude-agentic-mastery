"""
Main game class for Zombie Survival
Handles the game loop, rendering, and event processing
"""
import pygame
from entities.player import Player


class Game:
    """Main game class"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()

        # Game configuration
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.BACKGROUND_COLOR = (50, 50, 50)  # Dark gray

        # Create the game window
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Zombie Survival")

        # Create clock for FPS control
        self.clock = pygame.time.Clock()

        # Game state
        self.running = True

        # Create player at center of screen
        self.player = Player(
            self.SCREEN_WIDTH // 2,
            self.SCREEN_HEIGHT // 2,
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT
        )

    def handle_events(self):
        """Process game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, delta_time):
        """Update game state

        Args:
            delta_time: Time elapsed since last frame in seconds
        """
        # Update player
        self.player.update(delta_time)

    def render(self):
        """Render the game"""
        # Fill background
        self.screen.fill(self.BACKGROUND_COLOR)

        # Render player
        self.player.render(self.screen)

        # Update display
        pygame.display.flip()

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
