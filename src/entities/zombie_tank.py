"""Tank zombie variant - slow but tough."""

from config import tank_zombie_config
from entities.base_zombie import BaseZombie


class TankZombie(BaseZombie):
    """A tank zombie variant that moves slowly but has high health."""

    def __init__(self, x: float, y: float):
        """Initialize tank zombie at given position.

        Args:
            x: Starting x coordinate
            y: Starting y coordinate
        """
        # Initialize with tank zombie config and slower rotation (360°/sec = 1 rotation/sec)
        super().__init__(x, y, config=tank_zombie_config, rotation_speed=360.0)
