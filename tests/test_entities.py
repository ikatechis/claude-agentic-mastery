"""Tests for game entities"""

from entities.player import Player
from entities.zombie import Zombie


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


class TestZombie:
    """Test zombie entity"""

    def test_zombie_initialization(self):
        """Test zombie is created with correct defaults"""
        zombie = Zombie(100, 200)
        assert zombie.x == 100
        assert zombie.y == 200
        assert zombie.speed == 80
        assert zombie.damage == 10

    def test_zombie_movement(self):
        """Test zombie moves toward player"""
        zombie = Zombie(0, 0)
        initial_x = zombie.x
        initial_y = zombie.y

        # Player at (100, 100), zombie should move toward them
        zombie.update(1.0, 100, 100)

        assert zombie.x > initial_x  # Moved right
        assert zombie.y > initial_y  # Moved down
