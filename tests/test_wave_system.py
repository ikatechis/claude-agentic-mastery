"""Tests for wave spawning system, game states, and score tracking"""

from game import Game
from game_state import GameState


class TestWaveSystem:
    """Test wave calculation and progression"""

    def test_wave_zombie_calculation(self):
        """Test progressive difficulty formula"""
        game = Game()
        assert game.calculate_wave_zombies(1) == 3  # 3 * 1.5^0 = 3
        assert game.calculate_wave_zombies(2) == 4  # 3 * 1.5^1 = 4.5 → 4
        assert game.calculate_wave_zombies(3) == 6  # 3 * 1.5^2 = 6.75 → 6
        assert game.calculate_wave_zombies(4) == 10  # 3 * 1.5^3 = 10.125 → 10
        assert game.calculate_wave_zombies(5) == 15  # 3 * 1.5^4 = 15.1875 → 15

    def test_wave_cap(self):
        """Test max zombies per wave cap"""
        game = Game()
        # High wave number should hit cap
        assert game.calculate_wave_zombies(100) == 20

    def test_start_wave(self):
        """Test wave initialization"""
        game = Game()
        game.start_wave()
        assert game.current_wave == 1
        assert game.zombies_to_spawn == 3
        assert game.wave_notification_timer > 0

    def test_wave_progression(self):
        """Test multiple wave starts"""
        game = Game()
        game.start_wave()
        assert game.current_wave == 1

        game.start_wave()
        assert game.current_wave == 2
        assert game.zombies_to_spawn == 4

        game.start_wave()
        assert game.current_wave == 3
        assert game.zombies_to_spawn == 6


class TestGameStates:
    """Test game state transitions"""

    def test_initial_state(self):
        """Test game starts in MENU state"""
        game = Game()
        assert game.state == GameState.MENU

    def test_new_game_reset(self):
        """Test start_new_game resets all state"""
        game = Game()
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

    def test_state_enum_values(self):
        """Test GameState enum has expected values"""
        assert GameState.MENU
        assert GameState.PLAYING
        assert GameState.GAME_OVER


class TestScoreSystem:
    """Test score tracking"""

    def test_initial_score(self):
        """Test score starts at zero"""
        game = Game()
        assert game.score == 0

    def test_score_config_loaded(self):
        """Test score config is properly loaded"""
        game = Game()
        assert game.score_config.points_per_kill == 10
        assert game.score_config.score_x_ratio == 0.95
        assert game.score_config.score_y_ratio == 0.0167

    def test_score_reset_on_new_game(self):
        """Test score resets when starting new game"""
        game = Game()
        game.score = 150
        game.start_new_game()
        assert game.score == 0


class TestWaveConfig:
    """Test wave configuration"""

    def test_wave_config_defaults(self):
        """Test wave config has expected defaults"""
        game = Game()
        assert game.wave_config.initial_zombies == 3
        assert game.wave_config.zombies_per_wave_multiplier == 1.5
        assert game.wave_config.max_zombies_per_wave == 20
        assert game.wave_config.wave_delay == 3.0
        assert game.wave_config.spawn_interval == 0.5
