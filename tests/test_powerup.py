"""Tests for power-up system (src/entities/powerup.py)"""

import pygame
import pytest

from config import powerup_config
from entities.player import Player
from entities.powerup import Powerup, PowerupType


@pytest.fixture
def powerup():
    """Create a basic powerup for testing."""
    pygame.init()
    p = Powerup(100, 100, PowerupType.HEALTH)
    yield p
    pygame.quit()


@pytest.fixture
def player():
    """Create a player for testing power-up effects."""
    pygame.init()
    p = Player(400, 300, screen_width=800, screen_height=600)
    yield p
    pygame.quit()


class TestPowerupCreation:
    """Test power-up initialization and type selection."""

    def test_specific_type_creation(self):
        """Test creating power-up with specific type"""
        pygame.init()
        health_powerup = Powerup(100, 100, PowerupType.HEALTH)
        assert health_powerup.powerup_type == PowerupType.HEALTH
        assert health_powerup.color == powerup_config.health_color

        speed_powerup = Powerup(200, 200, PowerupType.SPEED)
        assert speed_powerup.powerup_type == PowerupType.SPEED
        assert speed_powerup.color == powerup_config.speed_color

        shield_powerup = Powerup(300, 300, PowerupType.SHIELD)
        assert shield_powerup.powerup_type == PowerupType.SHIELD
        assert shield_powerup.color == powerup_config.shield_color
        pygame.quit()

    def test_random_type_creation(self):
        """Test creating power-up with random type (no type specified)"""
        pygame.init()
        powerup = Powerup(100, 100)  # No type specified
        assert powerup.powerup_type in [
            PowerupType.HEALTH,
            PowerupType.SPEED,
            PowerupType.SHIELD,
            PowerupType.AMMO,
        ]
        pygame.quit()

    def test_initial_state(self, powerup):
        """Test power-up starts with correct initial state"""
        assert powerup.x == 100
        assert powerup.y == 100
        assert powerup.lifetime == powerup_config.lifetime
        assert powerup.is_visible is True
        assert powerup.blink_timer == 0.0


class TestPowerupLifetime:
    """Test power-up lifetime and expiration."""

    def test_lifetime_countdown(self, powerup):
        """Test lifetime decreases with delta_time"""
        initial_lifetime = powerup.lifetime
        still_alive = powerup.update(1.0)  # 1 second passed

        assert still_alive is True
        assert powerup.lifetime == initial_lifetime - 1.0

    def test_expiration(self, powerup):
        """Test power-up expires when lifetime reaches zero"""
        # Fast-forward to just before expiration
        powerup.update(9.9)
        assert powerup.update(0.05) is True  # Still alive at 0.05s remaining

        # Now it should expire
        assert powerup.update(0.1) is False  # Expired


class TestBlinkAnimation:
    """Test blink warning animation."""

    def test_no_blink_during_normal_lifetime(self, powerup):
        """Test power-up doesn't blink when lifetime > warning_duration"""
        powerup.update(5.0)  # 5s remaining (above 2s warning threshold)
        assert powerup.is_visible is True

    def test_blink_during_warning_phase(self, powerup):
        """Test power-up blinks during warning phase"""
        # Fast-forward to warning phase (2s remaining)
        powerup.update(8.0)  # Now at 2s remaining

        # Blink should toggle every 0.1 seconds (half of 0.2s blink_frequency)
        initial_visibility = powerup.is_visible

        powerup.update(0.1)
        assert powerup.is_visible != initial_visibility  # Should toggle

        powerup.update(0.1)
        assert powerup.is_visible == initial_visibility  # Should toggle back

    def test_blink_timer_reset(self, powerup):
        """Test blink timer resets after each toggle"""
        powerup.update(8.0)  # Enter warning phase

        powerup.update(0.1)  # First toggle
        assert powerup.blink_timer < 0.1  # Timer should have reset


class TestPowerupEffects:
    """Test power-up effect application."""

    def test_health_effect(self, player):
        """Test health power-up restores health"""
        player.health = 50  # Damage player first
        health_powerup = Powerup(100, 100, PowerupType.HEALTH)

        result = health_powerup.apply_effect(player)

        assert result["type"] == "health"
        assert player.health > 50  # Health should increase
        assert player.health <= player.max_health  # Should not exceed max

    def test_health_capping(self, player):
        """Test health power-up respects max health"""
        player.health = 95  # Almost full health
        health_powerup = Powerup(100, 100, PowerupType.HEALTH)

        result = health_powerup.apply_effect(player)

        assert player.health == player.max_health  # Should cap at 100
        assert result["amount"] == 5  # Should report actual amount restored

    def test_speed_effect(self, player):
        """Test speed power-up increases speed multiplier"""
        speed_powerup = Powerup(100, 100, PowerupType.SPEED)

        result = speed_powerup.apply_effect(player)

        assert result["type"] == "speed"
        assert player.speed_multiplier == powerup_config.speed_multiplier
        assert player.speed_boost_timer > 0

    def test_shield_effect(self, player):
        """Test shield power-up adds shield hits"""
        shield_powerup = Powerup(100, 100, PowerupType.SHIELD)

        result = shield_powerup.apply_effect(player)

        assert result["type"] == "shield"
        assert player.shield_hits_remaining == powerup_config.shield_hits


class TestPowerupRendering:
    """Test power-up rendering behavior."""

    def test_render_when_visible(self, powerup):
        """Test power-up renders when visible"""
        screen = pygame.display.set_mode((800, 600))
        powerup.is_visible = True

        # Should not raise errors
        powerup.draw(screen)

    def test_skip_render_when_invisible(self, powerup):
        """Test power-up skips rendering when invisible (blink-off state)"""
        screen = pygame.display.set_mode((800, 600))
        powerup.is_visible = False

        # Should not raise errors and should skip rendering
        powerup.draw(screen)
