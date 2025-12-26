"""Tests for zombie entity (src/entities/zombie.py)"""

from entities.zombie import Zombie


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
