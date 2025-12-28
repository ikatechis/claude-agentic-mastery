"""
Main game class for Zombie Survival
Handles the game loop, rendering, and event processing
"""

import dataclasses
import math
import random
from pathlib import Path

import pygame

from config import (
    DamagePopup,
    KillFlash,
    PickupFlash,
    game_config,
    powerup_config,
    score_config,
    ui_config,
    wave_config,
)
from entities.player import Player
from entities.powerup import Powerup
from entities.zombie import Zombie
from game_state import GameState
from logger import get_logger

logger = get_logger(__name__)


class Game:
    """Main game class"""

    # High score persistence
    HIGHSCORE_FILE = Path("highscore.txt")

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
        self.high_score = 0
        self.load_high_score()  # Load persistent high score from file

        # Power-up configuration
        self.powerup_config = powerup_config

        # Create player at center of screen
        self.player = Player(
            self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        )

        # Zombie management
        self.zombies = []

        # Power-up management
        self.powerups = []

        # Visual effects
        self.damage_popups = []  # List of DamagePopup dataclasses
        self.kill_flashes = []  # List of KillFlash dataclasses
        self.pickup_flashes = []  # List of PickupFlash dataclasses

        # Pause screen optimization
        self.pause_surface = None  # Captured screen for pause overlay

        # Background tile loading (fallback to solid color if fails)
        self.background_tile = None
        try:
            self.background_tile = pygame.image.load("assets/sprites/tile_background.png").convert()
            logger.debug("Background tile loaded successfully")
        except (pygame.error, FileNotFoundError):
            logger.info("Background tile not found, using solid color fallback")

    def load_high_score(self):
        """Load high score from file. Defaults to 0 if file doesn't exist or is invalid."""
        try:
            if self.HIGHSCORE_FILE.exists():
                score_text = self.HIGHSCORE_FILE.read_text().strip()
                self.high_score = int(score_text)
                logger.info(f"High score loaded: {self.high_score}")
            else:
                logger.info("No high score file found, starting fresh")
                self.high_score = 0
        except (ValueError, OSError) as e:
            logger.warning(f"Failed to load high score: {e}, defaulting to 0")
            self.high_score = 0

    def save_high_score(self):
        """Save high score to file."""
        try:
            self.HIGHSCORE_FILE.write_text(str(self.high_score))
            logger.info(f"High score saved: {self.high_score}")
        except OSError as e:
            logger.warning(f"Failed to save high score: {e}")

    def handle_events(self):
        """Process game events during PLAYING state"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                # Capture current screen for pause overlay (optimization)
                self.pause_surface = self.screen.copy()
                # Toggle pause
                self.state = GameState.PAUSED

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

        # Reset visual effects
        self.damage_popups = []
        self.kill_flashes = []

        # Start first wave immediately
        self.start_wave()

    def update(self, delta_time):
        """Update game state

        Args:
            delta_time: Time elapsed since last frame in seconds
        """
        # Handle wave delay countdown (don't block other updates)
        if self.wave_delay_timer > 0:
            self.wave_delay_timer -= delta_time
            if self.wave_delay_timer <= 0:
                self.start_wave()

        # Spawn zombies gradually (only if not in wave delay)
        if self.wave_delay_timer <= 0 and self.zombies_to_spawn > 0:
            self.spawn_timer -= delta_time
            if self.spawn_timer <= 0:
                self.spawn_zombie()
                self.zombies_to_spawn -= 1
                self.spawn_timer = self.wave_config.spawn_interval

        # Check if wave complete (only if not already in delay)
        if self.wave_delay_timer <= 0 and len(self.zombies) == 0 and self.zombies_to_spawn == 0:
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

                    # Add visual effects
                    # Flash effect at zombie position
                    self.kill_flashes.append(
                        KillFlash(
                            x=zombie.x,
                            y=zombie.y,
                            radius=zombie.radius,
                            timer=self.ui_config.kill_flash_duration,
                        )
                    )
                    # Damage popup above zombie
                    self.damage_popups.append(
                        DamagePopup(
                            x=zombie.x,
                            y=zombie.y - 20,
                            text=f"+{self.score_config.points_per_kill}",
                            timer=self.ui_config.damage_popup_duration,
                        )
                    )

                    # Spawn power-up with drop_chance probability
                    if random.random() < self.powerup_config.drop_chance:
                        self.powerups.append(Powerup(zombie.x, zombie.y))
                else:
                    survivors.append(zombie)
            self.zombies = survivors

        # Check collisions with all zombies
        for zombie in self.zombies:
            if not self.check_collision(self.player, zombie):
                continue

            # Apply knockback - push zombie to collision boundary
            distance = self.get_distance(self.player, zombie)
            if distance > 0:  # Avoid division by zero
                # Calculate direction from player to zombie
                dx = zombie.x - self.player.x
                dy = zombie.y - self.player.y
                # Normalize direction
                dx /= distance
                dy /= distance
                # Push zombie to collision boundary (sum of radii)
                collision_dist = self.player.radius + zombie.radius
                zombie.x = self.player.x + dx * collision_dist
                zombie.y = self.player.y + dy * collision_dist

            # Apply damage to player
            if not self.player.take_damage(zombie.damage):
                continue  # Damage on cooldown

            # Check if player died
            if not self.player.is_alive():
                # Update high score
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()  # Persist to file immediately
                self.state = GameState.GAME_OVER
                return

        # Update visual effects
        # Update kill flashes
        self.kill_flashes = [
            dataclasses.replace(flash, timer=flash.timer - delta_time)
            for flash in self.kill_flashes
            if flash.timer > 0
        ]

        # Update damage popups (move up and fade)
        self.damage_popups = [
            dataclasses.replace(popup, timer=popup.timer - delta_time, y=popup.y - 30 * delta_time)
            for popup in self.damage_popups
            if popup.timer > 0
        ]

        # Update pickup flashes
        self.pickup_flashes = [
            dataclasses.replace(flash, timer=flash.timer - delta_time)
            for flash in self.pickup_flashes
            if flash.timer > 0
        ]

        # Update all powerups (remove expired ones)
        self.powerups = [powerup for powerup in self.powerups if powerup.update(delta_time)]

        # Check powerup collection
        collected = []
        for powerup in self.powerups:
            if self.check_collision(self.player, powerup):
                # Apply power-up effect
                effect_data = powerup.apply_effect(self.player)

                # Create pickup flash visual effect
                self.pickup_flashes.append(
                    PickupFlash(
                        x=powerup.x,
                        y=powerup.y,
                        radius=powerup.radius * 2,  # Larger flash
                        color=effect_data["color"],
                        timer=self.powerup_config.pickup_flash_duration,
                    )
                )

                collected.append(powerup)

        # Remove collected powerups
        self.powerups = [p for p in self.powerups if p not in collected]

    def render_background(self):
        """Draw the background - either tiled or solid color"""
        if self.background_tile:
            # Draw tiled background
            tile_width = self.background_tile.get_width()
            tile_height = self.background_tile.get_height()
            for x in range(0, self.SCREEN_WIDTH, tile_width):
                for y in range(0, self.SCREEN_HEIGHT, tile_height):
                    self.screen.blit(self.background_tile, (x, y))
        else:
            # Fallback to solid color
            self.screen.fill(self.BACKGROUND_COLOR)

    def render(self):
        """Render the game"""
        # Draw background
        self.render_background()

        # Render all zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)

        # Render all powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # Render kill flash effects (on top of zombies)
        self.render_kill_flashes()

        # Render pickup flash effects
        self.render_pickup_flashes()

        # Render attack range (under player)
        self.render_attack_range()

        # Render player (on top of zombies)
        self.player.render(self.screen)

        # Render attack cooldown (above player)
        self.render_attack_cooldown()

        # Render active power-up effects (shield, speed boost indicators)
        self.render_player_effects()

        # Render damage popups (floating text)
        self.render_damage_popups()

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

    def render_attack_range(self):
        """Show attack range circle when player is attacking."""
        if self.player.is_attacking:
            # Draw semi-transparent attack range circle
            attack_surface = pygame.Surface(
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA
            )
            # Yellow circle with 30% opacity
            pygame.draw.circle(
                attack_surface,
                (255, 255, 0, 76),  # RGBA - 76 is ~30% of 255
                (int(self.player.x), int(self.player.y)),
                self.player.attack_range,
                2,  # 2 pixel border width
            )
            self.screen.blit(attack_surface, (0, 0))

    def render_attack_cooldown(self):
        """Show attack cooldown bar below player."""
        if self.player.attack_cooldown > 0:
            # Bar position: centered below player
            bar_width = 40
            bar_height = 4
            bar_x = int(self.player.x - bar_width // 2)
            bar_y = int(self.player.y + self.player.radius + 5)

            # Background (gray)
            pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

            # Foreground (cooldown progress - orange)
            cooldown_ratio = self.player.attack_cooldown / self.player.attack_cooldown_time
            cooldown_width = int(bar_width * cooldown_ratio)
            pygame.draw.rect(self.screen, (255, 165, 0), (bar_x, bar_y, cooldown_width, bar_height))

    def render_kill_flashes(self):
        """Render white flash effects where zombies were killed."""
        for flash in self.kill_flashes:
            # Flash intensity based on remaining timer
            alpha = int(255 * (flash.timer / self.ui_config.kill_flash_duration))
            # Clamp alpha to valid range [0, 255]
            alpha = max(0, min(255, alpha))
            # Draw white circle with fading alpha
            flash_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(
                flash_surface,
                (255, 255, 255, alpha),
                (int(flash.x), int(flash.y)),
                int(flash.radius),
            )
            self.screen.blit(flash_surface, (0, 0))

    def render_pickup_flashes(self):
        """Render colored flash effects where powerups were collected."""
        for flash in self.pickup_flashes:
            # Flash intensity based on remaining timer
            alpha = int(255 * (flash.timer / self.powerup_config.pickup_flash_duration))
            # Clamp alpha to valid range [0, 255]
            alpha = max(0, min(255, alpha))
            # Draw colored circle with fading alpha
            flash_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            # flash.color is RGB, add alpha channel
            color_with_alpha = (*flash.color, alpha)
            pygame.draw.circle(
                flash_surface,
                color_with_alpha,
                (int(flash.x), int(flash.y)),
                int(flash.radius),
            )
            self.screen.blit(flash_surface, (0, 0))

    def render_damage_popups(self):
        """Render floating damage numbers."""
        for popup in self.damage_popups:
            # Fade out based on remaining timer
            alpha_ratio = popup.timer / self.ui_config.damage_popup_duration
            color = (255, 255, 0)  # Yellow

            # Render text with fade
            text = self.font.render(popup.text, True, color)
            text_rect = text.get_rect(center=(int(popup.x), int(popup.y)))

            # Apply alpha to surface
            text.set_alpha(int(255 * alpha_ratio))
            self.screen.blit(text, text_rect)

    def render_player_effects(self):
        """Render visual indicators for active power-up effects."""
        # Shield indicator
        if self.player.has_shield():
            # Draw gold circle around player
            effect_surface = pygame.Surface(
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA
            )
            pygame.draw.circle(
                effect_surface,
                (255, 215, 0, 128),  # Gold with 50% opacity
                (int(self.player.x), int(self.player.y)),
                self.player.radius + 5,  # Slightly larger than player
                3,  # Border width
            )
            self.screen.blit(effect_surface, (0, 0))

            # Show remaining shield hits below player
            shield_text = self.font.render(
                f"Shield: {self.player.shield_hits_remaining}",
                True,
                (255, 215, 0),  # Gold
            )
            text_rect = shield_text.get_rect(
                center=(int(self.player.x), int(self.player.y + self.player.radius + 20))
            )
            self.screen.blit(shield_text, text_rect)

        # Speed boost indicator
        if self.player.has_speed_boost():
            # Progress bar showing remaining time
            bar_width = 60
            bar_height = 6
            bar_x = int(self.player.x - bar_width / 2)
            bar_y = int(self.player.y - self.player.radius - 15)

            # Calculate progress (initial duration is stored in config)
            # We need to estimate initial duration from config
            max_duration = self.powerup_config.speed_duration_max
            progress = self.player.speed_boost_timer / max_duration

            # Background (dark)
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

            # Foreground (cyan, shows remaining time)
            filled_width = int(bar_width * progress)
            pygame.draw.rect(
                self.screen,
                (0, 255, 255),  # Cyan
                (bar_x, bar_y, filled_width, bar_height),
            )

            # Border
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),  # White border
                (bar_x, bar_y, bar_width, bar_height),
                1,  # Border width
            )

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
        self.render_background()

        # Title
        title_text = self.wave_font.render("ZOMBIE SURVIVAL", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        # High Score display
        if self.high_score > 0:
            high_score_text = self.wave_font.render(
                f"High Score: {self.high_score}", True, (255, 255, 0)
            )
            high_score_rect = high_score_text.get_rect(
                center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3 + 60)
            )
            self.screen.blit(high_score_text, high_score_rect)

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
        self.render_background()

        # Game Over title
        title_text = self.wave_font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        # Check if new high score
        is_new_high_score = self.score == self.high_score and self.score > 0

        # New high score banner
        y_offset = self.SCREEN_HEIGHT // 2 - 40
        if is_new_high_score:
            new_high_text = self.wave_font.render("NEW HIGH SCORE!", True, (0, 255, 0))
            new_high_rect = new_high_text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(new_high_text, new_high_rect)
            y_offset += 50

        # Final score
        score_text = self.wave_font.render(f"Final Score: {self.score}", True, (255, 255, 0))
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset))
        self.screen.blit(score_text, score_rect)

        # High score display
        high_score_text = self.font.render(
            f"High Score: {self.high_score}", True, self.ui_config.text_color
        )
        high_score_rect = high_score_text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset + 50))
        self.screen.blit(high_score_text, high_score_rect)

        # Wave reached
        wave_text = self.font.render(
            f"Wave Reached: {self.current_wave}", True, self.ui_config.text_color
        )
        wave_rect = wave_text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset + 90))
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

    def handle_pause_events(self):
        """Handle events in PAUSED state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_p):
                    # Resume game
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_q:
                    self.running = False

    def render_paused(self):
        """Render the pause overlay."""
        # Blit the captured pause surface (performance optimization)
        if self.pause_surface:
            self.screen.blit(self.pause_surface, (0, 0))
        else:
            # Fallback if pause_surface is None (shouldn't happen)
            self.render()

        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # PAUSED title
        title_text = self.wave_font.render("PAUSED", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        # Instructions
        instructions = [
            "Press ESC or P to Resume",
            "Press Q to Quit",
        ]

        y_offset = self.SCREEN_HEIGHT // 2
        for instruction in instructions:
            text = self.font.render(instruction, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40

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
            elif self.state == GameState.PAUSED:
                self.handle_pause_events()
                self.render_paused()
            elif self.state == GameState.GAME_OVER:
                self.handle_game_over_events()
                self.render_game_over()

        # Cleanup
        pygame.quit()
