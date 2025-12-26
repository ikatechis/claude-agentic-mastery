"""Tests for configuration module (src/config.py)"""

from config import (
    GameConfig,
    PlayerConfig,
    ScoreConfig,
    UIConfig,
    WaveConfig,
    ZombieConfig,
)


class TestGameConfig:
    """Test game configuration."""

    def test_game_defaults(self):
        """Test game config has expected default values"""
        config = GameConfig()
        assert config.screen_width == 800
        assert config.screen_height == 600
        assert config.fps == 60
        assert config.background_color == (50, 50, 50)
        assert config.spawn_offscreen_buffer == 50


class TestPlayerConfig:
    """Test player configuration."""

    def test_player_defaults(self):
        """Test player config has expected default values"""
        config = PlayerConfig()
        assert config.radius == 15
        assert config.speed == 200
        assert config.max_health == 100
        assert config.color == (0, 255, 0)
        assert config.attack_range == 50
        assert config.attack_cooldown == 0.5
        assert config.damage_cooldown == 1.0


class TestZombieConfig:
    """Test zombie configuration."""

    def test_zombie_defaults(self):
        """Test zombie config has expected default values"""
        config = ZombieConfig()
        assert config.radius == 12
        assert config.speed == 80
        assert config.color == (200, 50, 50)
        assert config.damage == 10


class TestWaveConfig:
    """Test wave configuration."""

    def test_wave_defaults(self):
        """Test wave config has expected default values"""
        config = WaveConfig()
        assert config.initial_zombies == 3
        assert config.zombies_per_wave_multiplier == 1.5
        assert config.max_zombies_per_wave == 20
        assert config.wave_delay == 3.0
        assert config.spawn_interval == 0.5


class TestScoreConfig:
    """Test score configuration."""

    def test_score_defaults(self):
        """Test score config has expected default values"""
        config = ScoreConfig()
        assert config.points_per_kill == 10
        assert config.score_x_ratio == 0.95
        assert config.score_y_ratio == 0.0167


class TestUIConfig:
    """Test UI configuration."""

    def test_ui_defaults(self):
        """Test UI config has expected default values"""
        config = UIConfig()
        assert config.health_bar_x_ratio == 0.0125
        assert config.health_bar_y_ratio == 0.0167
        assert config.health_bar_width_ratio == 0.25
        assert config.health_bar_height == 30
        assert config.font_size == 36
        assert config.wave_notification_duration == 2.0
        assert config.wave_font_size == 72
