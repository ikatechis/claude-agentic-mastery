"""
Main game class for Zombie Survival
Handles the game loop, rendering, and event processing
"""

import math
import random

import pygame

from config import game_config, score_config, ui_config, wave_config
from entities.player import Player
from entities.zombie import Zombie
from game_state import GameState


class Game:
    """Main game class"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()

        # Game configuration
        self.config = game_config
        self.SCREEN_WIDTH = self.config.screen_width
        self.SCREEN_HEIGHT = self.config.screen_height
        self.FPS = self.config.fps
        self.BACKGROUND_COLOR = self.config.background_color

        # Create the game window
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Zombie Survival")

        # Create clock for FPS control
        self.clock = pygame.time.Clock()

        # Initialize font for UI
        pygame.font.init()
        self.ui_config = ui_config
        self.font = pygame.font.Font(None, self.ui_config.font_size)
        self.wave_font = pygame.font.Font(None, self.ui_config.wave_font_size)

        # Game state management
        self.running = True
        self.state = GameState.MENU

        # Wave system
        self.wave_config = wave_config
        self.current_wave = 0
        self.zombies_to_spawn = 0
        self.spawn_timer = 0.0
        self.wave_delay_timer = 0.0
        self.wave_notification_timer = 0.0

        # Score tracking
        self.score_config = score_config
        self.score = 0

        # Create player at center of screen
        self.player = Player(
            self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        )

        # Zombie management
        self.zombies = []

    def handle_events(self):
        """Process game events"""
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                self.running = False

    @staticmethod
    def get_distance(entity1, entity2):
        """Calculate distance between two entities.

        Args:
            entity1: First entity (must have x, y)
            entity2: Second entity (must have x, y)

        Returns:
            float: Distance between entity centers
        """
        dx = entity1.x - entity2.x
        dy = entity1.y - entity2.y
        return math.hypot(dx, dy)

    def check_collision(self, entity1, entity2):
        """Check circle collision between two entities.

        Args:
            entity1: First entity (must have x, y, radius)
            entity2: Second entity (must have x, y, radius)

        Returns:
            bool: True if entities are colliding
        """
        distance = self.get_distance(entity1, entity2)
        # Collision if distance < sum of radii
        return distance < (entity1.radius + entity2.radius)

    def spawn_zombie(self):
        """Spawn a zombie at a random position off-screen."""
        buffer = self.config.spawn_offscreen_buffer
        side = random.choice(("top", "bottom", "left", "right"))

        if side == "top":
            x = random.randint(0, self.SCREEN_WIDTH)
            y = -buffer
        elif side == "bottom":
            x = random.randint(0, self.SCREEN_WIDTH)
            y = self.SCREEN_HEIGHT + buffer
        elif side == "left":
            x = -buffer
            y = random.randint(0, self.SCREEN_HEIGHT)
        else:  # right
            x = self.SCREEN_WIDTH + buffer
            y = random.randint(0, self.SCREEN_HEIGHT)

        self.zombies.append(Zombie(x, y))

    def calculate_wave_zombies(self, wave_number):
        """Calculate how many zombies to spawn for a given wave.

        Args:
            wave_number: The wave number (1-indexed)

        Returns:
            int: Number of zombies to spawn (capped at max)
        """
        base = self.wave_config.initial_zombies
        multiplier = self.wave_config.zombies_per_wave_multiplier
        zombies = int(base * (multiplier ** (wave_number - 1)))
        return min(zombies, self.wave_config.max_zombies_per_wave)

    def start_wave(self):
        """Initialize a new wave of zombies."""
        self.current_wave += 1
        self.zombies_to_spawn = self.calculate_wave_zombies(self.current_wave)
        self.spawn_timer = 0.0
        self.wave_notification_timer = self.ui_config.wave_notification_duration

    def start_new_game(self):
        """Reset game state for a new game."""
        # Reset player
        self.player = Player(
            self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        )

        # Reset wave system
        self.current_wave = 0
        self.zombies = []
        self.zombies_to_spawn = 0
        self.wave_delay_timer = 0.0
        self.wave_notification_timer = 0.0

        # Reset score
        self.score = 0

        # Start first wave immediately
        self.start_wave()

    def update(self, delta_time):
        """Update game state

        Args:
            delta_time: Time elapsed since last frame in seconds
        """
        # Handle wave delay (between waves)
        if self.wave_delay_timer > 0:
            self.wave_delay_timer -= delta_time
            if self.wave_delay_timer <= 0:
                self.start_wave()
            return  # Don't update gameplay during delay

        # Spawn zombies gradually
        if self.zombies_to_spawn > 0:
            self.spawn_timer -= delta_time
            if self.spawn_timer <= 0:
                self.spawn_zombie()
                self.zombies_to_spawn -= 1
                self.spawn_timer = self.wave_config.spawn_interval

        # Check if wave complete
        if len(self.zombies) == 0 and self.zombies_to_spawn == 0:
            self.wave_delay_timer = self.wave_config.wave_delay

        # Update wave notification timer
        if self.wave_notification_timer > 0:
            self.wave_notification_timer -= delta_time

        # Update player
        self.player.update(delta_time)

        # Update all zombies
        for zombie in self.zombies:
            zombie.update(delta_time, self.player.x, self.player.y)

        # Check player attacks
        if self.player.is_attacking:
            # Kill zombies within attack range
            survivors = []
            for zombie in self.zombies:
                if self.get_distance(self.player, zombie) <= self.player.attack_range:
                    # Zombie killed - award points
                    self.score += self.score_config.points_per_kill
                else:
                    survivors.append(zombie)
            self.zombies = survivors

        # Check collisions with all zombies
        for zombie in self.zombies:
            if not self.check_collision(self.player, zombie):
                continue

            # Apply damage to player
            if not self.player.take_damage(zombie.damage):
                continue  # Damage on cooldown

            # Check if player died
            if not self.player.is_alive():
                self.state = GameState.GAME_OVER
                return

    def render(self):
        """Render the game"""
        # Fill background
        self.screen.fill(self.BACKGROUND_COLOR)

        # Render all zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)

        # Render player (on top of zombies)
        self.player.render(self.screen)

        # Render UI
        self.render_health_bar()
        self.render_score()
        self.render_wave_notification()

        # Update display
        pygame.display.flip()

    def render_health_bar(self):
        """Draw the player's health bar (responsive to screen size)"""
        # Calculate position based on screen dimensions
        bar_x = int(self.SCREEN_WIDTH * self.ui_config.health_bar_x_ratio)
        bar_y = int(self.SCREEN_HEIGHT * self.ui_config.health_bar_y_ratio)
        bar_width = int(self.SCREEN_WIDTH * self.ui_config.health_bar_width_ratio)
        bar_height = self.ui_config.health_bar_height

        # Background (red, shows missing health)
        pygame.draw.rect(
            self.screen, self.ui_config.health_bar_bg_color, (bar_x, bar_y, bar_width, bar_height)
        )

        # Foreground (green, shows current health)
        health_width = int((self.player.health / self.player.max_health) * bar_width)
        pygame.draw.rect(
            self.screen,
            self.ui_config.health_bar_fg_color,
            (bar_x, bar_y, health_width, bar_height),
        )

        # Border
        pygame.draw.rect(
            self.screen,
            self.ui_config.health_bar_border_color,
            (bar_x, bar_y, bar_width, bar_height),
            self.ui_config.health_bar_border_width,
        )

        # Health text
        health_text = self.font.render(
            f"HP: {int(self.player.health)}/{self.player.max_health}",
            True,
            self.ui_config.text_color,
        )
        self.screen.blit(health_text, (bar_x + bar_width + 10, bar_y))

    def render_score(self):
        """Draw the current score in top-right corner."""
        score_text = self.font.render(f"Score: {self.score}", True, self.ui_config.text_color)

        # Right-align the score
        text_rect = score_text.get_rect()
        score_x = int(self.SCREEN_WIDTH * self.score_config.score_x_ratio) - text_rect.width
        score_y = int(self.SCREEN_HEIGHT * self.score_config.score_y_ratio)

        self.screen.blit(score_text, (score_x, score_y))

    def render_wave_notification(self):
        """Show 'Wave X' notification at start of each wave."""
        if self.wave_notification_timer > 0:
            wave_text = self.wave_font.render(f"Wave {self.current_wave}", True, (255, 255, 0))
            text_rect = wave_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
            self.screen.blit(wave_text, text_rect)

    def handle_menu_events(self):
        """Handle events in MENU state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Start new game
                    self.start_new_game()
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_q:
                    self.running = False

    def render_menu(self):
        """Render the main menu screen."""
        self.screen.fill(self.BACKGROUND_COLOR)

        # Title
        title_text = self.wave_font.render("ZOMBIE SURVIVAL", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        # Instructions
        instructions = [
            "Press ENTER or SPACE to Start",
            "Press Q or ESC to Quit",
            "",
            "Controls: WASD to move, SPACE to attack",
        ]

        y_offset = self.SCREEN_HEIGHT // 2
        for instruction in instructions:
            text = self.font.render(instruction, True, self.ui_config.text_color)
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40

        pygame.display.flip()

    def handle_game_over_events(self):
        """Handle events in GAME_OVER state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Restart game
                    self.start_new_game()
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_m:
                    # Return to menu
                    self.state = GameState.MENU

    def render_game_over(self):
        """Render the game over screen."""
        self.screen.fill(self.BACKGROUND_COLOR)

        # Game Over title
        title_text = self.wave_font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        # Final score
        score_text = self.wave_font.render(f"Final Score: {self.score}", True, (255, 255, 0))
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        # Wave reached
        wave_text = self.font.render(
            f"Wave Reached: {self.current_wave}", True, self.ui_config.text_color
        )
        wave_rect = wave_text.get_rect(
            center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 60)
        )
        self.screen.blit(wave_text, wave_rect)

        # Instructions
        instructions = [
            "",
            "Press ENTER to Restart",
            "Press M for Main Menu",
            "Press Q or ESC to Quit",
        ]

        y_offset = self.SCREEN_HEIGHT // 2 + 120
        for instruction in instructions:
            text = self.font.render(instruction, True, self.ui_config.text_color)
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 35

        pygame.display.flip()

    def run(self):
        """Main game loop with state machine"""
        while self.running:
            # Get delta time in seconds
            delta_time = self.clock.tick(self.FPS) / 1000.0

            # State-based event handling and rendering
            if self.state == GameState.MENU:
                self.handle_menu_events()
                self.render_menu()
            elif self.state == GameState.PLAYING:
                self.handle_events()
                self.update(delta_time)
                self.render()
            elif self.state == GameState.GAME_OVER:
                self.handle_game_over_events()
                self.render_game_over()

        # Cleanup
        pygame.quit()
