"""Tests for player entity (src/entities/player.py)"""

from entities.player import Player


class TestPlayer:
    """Test player entity"""

    def test_player_initialization(self):
        """Test player is created with correct defaults"""
        player = Player(400, 300, 800, 600)
        assert player.x == 400
        assert player.y == 300
        assert player.health == 100
        assert player.is_alive()

    def test_player_take_damage(self):
        """Test player takes damage correctly"""
        player = Player(400, 300, 800, 600)
        assert player.take_damage(30) is True  # First damage succeeds
        assert player.health == 70

        # Second damage should fail (cooldown)
        assert player.take_damage(10) is False
        assert player.health == 70  # Health unchanged

    def test_player_death(self):
        """Test player death when health reaches 0"""
        player = Player(400, 300, 800, 600)
        player.take_damage(100)
        assert player.health == 0
        assert not player.is_alive()

    def test_player_attack_cooldown(self):
        """Test attack cooldown system"""
        player = Player(400, 300, 800, 600)
        player.attack()
        assert player.is_attacking is True
        assert player.attack_cooldown > 0
