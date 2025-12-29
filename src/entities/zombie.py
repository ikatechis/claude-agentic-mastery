"""Normal zombie variant."""

from config import zombie_config
from entities.base_zombie import BaseZombie


class Zombie(BaseZombie):
    """A normal zombie enemy that chases the player."""

    def __init__(self, x: float, y: float):
        """Initialize zombie at given position.

        Args:
            x: Starting x coordinate
            y: Starting y coordinate
        """
        # Initialize with zombie config and default rotation speed (540°/sec)
        super().__init__(x, y, config=zombie_config, rotation_speed=540.0)
