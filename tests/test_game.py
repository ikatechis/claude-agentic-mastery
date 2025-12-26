"""Tests for main game logic (src/game.py)"""

import pygame
import pytest

from config import DamagePopup, KillFlash
from game import Game
from game_state import GameState


@pytest.fixture
def game():
    """Create a Game instance for testing."""
    pygame.init()
    game = Game()
    yield game
    pygame.quit()


class TestGameInitialization:
    """Test game initialization and setup."""

    def test_initial_state(self, game):
        """Test game starts in MENU state"""
        assert game.state == GameState.MENU

    def test_initial_score(self, game):
        """Test score starts at zero"""
        assert game.score == 0

    def test_new_game_reset(self, game):
        """Test start_new_game resets all state"""
        # Simulate some gameplay
        game.score = 100
        game.current_wave = 5
        game.zombies.append("fake_zombie")  # Add dummy zombie

        # Start new game
        game.start_new_game()

        assert game.score == 0
        assert game.current_wave == 1  # start_wave increments from 0
        assert game.player.health == 100
        assert len(game.zombies) == 0  # Zombies list cleared
        assert game.zombies_to_spawn == 3  # First wave ready


class TestWaveSystem:
    """Test wave calculation and progression."""

    def test_wave_zombie_calculation(self, game):
        """Test progressive difficulty formula"""
        assert game.calculate_wave_zombies(1) == 3  # 3 * 1.5^0 = 3
        assert game.calculate_wave_zombies(2) == 4  # 3 * 1.5^1 = 4.5 → 4
        assert game.calculate_wave_zombies(3) == 6  # 3 * 1.5^2 = 6.75 → 6
        assert game.calculate_wave_zombies(4) == 10  # 3 * 1.5^3 = 10.125 → 10
        assert game.calculate_wave_zombies(5) == 15  # 3 * 1.5^4 = 15.1875 → 15

    def test_wave_cap(self, game):
        """Test max zombies per wave cap"""
        # High wave number should hit cap
        assert game.calculate_wave_zombies(100) == 20

    def test_start_wave(self, game):
        """Test wave initialization"""
        game.start_wave()
        assert game.current_wave == 1
        assert game.zombies_to_spawn == 3
        assert game.wave_notification_timer > 0

    def test_wave_progression(self, game):
        """Test multiple wave starts"""
        game.start_wave()
        assert game.current_wave == 1

        game.start_wave()
        assert game.current_wave == 2
        assert game.zombies_to_spawn == 4

        game.start_wave()
        assert game.current_wave == 3
        assert game.zombies_to_spawn == 6


class TestGameStates:
    """Test game state transitions."""

    def test_state_enum_values(self):
        """Test GameState enum has expected values"""
        assert GameState.MENU
        assert GameState.PLAYING
        assert GameState.GAME_OVER


class TestScoreSystem:
    """Test score tracking."""

    def test_score_config_loaded(self, game):
        """Test score config is properly loaded"""
        assert game.score_config.points_per_kill == 10
        assert game.score_config.score_x_ratio == 0.95
        assert game.score_config.score_y_ratio == 0.0167

    def test_score_reset_on_new_game(self, game):
        """Test score resets when starting new game"""
        game.score = 150
        game.start_new_game()
        assert game.score == 0


class TestWaveConfig:
    """Test wave configuration."""

    def test_wave_config_defaults(self, game):
        """Test wave config has expected defaults"""
        assert game.wave_config.initial_zombies == 3
        assert game.wave_config.zombies_per_wave_multiplier == 1.5
        assert game.wave_config.max_zombies_per_wave == 20
        assert game.wave_config.wave_delay == 3.0
        assert game.wave_config.spawn_interval == 0.5


class TestVisualEffects:
    """Test visual effects rendering (kill flashes, damage popups, etc.)"""

    def test_render_kill_flashes_normal(self, game):
        """Test rendering with normal timer values."""
        game.kill_flashes = [
            KillFlash(x=100, y=100, radius=15, timer=0.15),
            KillFlash(x=200, y=200, radius=15, timer=0.075),
        ]
        # Should not raise any errors
        game.render_kill_flashes()

    def test_render_kill_flashes_timer_exceeds_max(self, game):
        """Test rendering when timer exceeds expected max (edge case bug)."""
        game.kill_flashes = [
            KillFlash(x=100, y=100, radius=15, timer=0.16),  # Slightly over 0.15
            KillFlash(x=200, y=200, radius=15, timer=0.20),  # Well over 0.15
            KillFlash(x=300, y=300, radius=15, timer=1.0),  # Way over
        ]
        # Should not raise ValueError about invalid color
        game.render_kill_flashes()

    def test_render_kill_flashes_negative_timer(self, game):
        """Test rendering with negative timer (should be handled gracefully)."""
        game.kill_flashes = [
            KillFlash(x=100, y=100, radius=15, timer=-0.01),
            KillFlash(x=200, y=200, radius=15, timer=-0.10),
        ]
        # Should not raise ValueError about invalid color
        game.render_kill_flashes()

    def test_render_kill_flashes_zero_timer(self, game):
        """Test rendering with zero timer."""
        game.kill_flashes = [KillFlash(x=100, y=100, radius=15, timer=0.0)]
        # Should not raise any errors
        game.render_kill_flashes()

    def test_render_kill_flashes_empty_list(self, game):
        """Test rendering with no kill flashes."""
        game.kill_flashes = []
        # Should not raise any errors
        game.render_kill_flashes()

    def test_render_damage_popups_normal(self, game):
        """Test rendering with normal popup values."""
        game.damage_popups = [
            DamagePopup(x=100, y=100, text="-10", timer=1.0),
            DamagePopup(x=200, y=200, text="-5", timer=0.5),
        ]
        # Should not raise any errors
        game.render_damage_popups()

    def test_render_damage_popups_empty_list(self, game):
        """Test rendering with no damage popups."""
        game.damage_popups = []
        # Should not raise any errors
        game.render_damage_popups()

    def test_render_attack_cooldown_active(self, game):
        """Test rendering when attack is on cooldown."""
        game.player.attack_cooldown = 0.3
        game.player.attack_cooldown_time = 0.5
        # Should not raise any errors
        game.render_attack_cooldown()

    def test_render_attack_cooldown_not_active(self, game):
        """Test rendering when no cooldown active."""
        game.player.attack_cooldown = 0.0
        # Should not raise any errors (should just not render anything)
        game.render_attack_cooldown()

    def test_render_attack_cooldown_full(self, game):
        """Test rendering when cooldown is at maximum."""
        game.player.attack_cooldown = 0.5
        game.player.attack_cooldown_time = 0.5
        # Should not raise any errors
        game.render_attack_cooldown()
