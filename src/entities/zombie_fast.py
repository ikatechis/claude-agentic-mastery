"""Fast zombie variant - quick but fragile."""

from config import fast_zombie_config
from entities.base_zombie import BaseZombie


class FastZombie(BaseZombie):
    """A fast zombie variant that moves quickly but has low health."""

    def __init__(self, x: float, y: float):
        """Initialize fast zombie at given position.

        Args:
            x: Starting x coordinate
            y: Starting y coordinate
        """
        # Initialize with fast zombie config and faster rotation (720°/sec = 2 rotations/sec)
        super().__init__(x, y, config=fast_zombie_config, rotation_speed=720.0)
