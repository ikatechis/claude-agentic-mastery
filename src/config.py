"""
Game configuration using dataclasses
All tunable game parameters organized by component
"""
from dataclasses import dataclass


@dataclass
class GameConfig:
    """Main game settings"""
    screen_width: int = 800
    screen_height: int = 600
    fps: int = 60
    background_color: tuple = (50, 50, 50)  # Dark gray
    initial_zombies: int = 3  # Number of zombies at game start
    spawn_offscreen_buffer: int = 50  # Distance off-screen for spawning


@dataclass
class PlayerConfig:
    """Player entity settings"""
    radius: int = 15
    color: tuple = (0, 255, 0)  # Green
    speed: int = 200  # Pixels per second
    max_health: int = 100
    damage_cooldown: float = 1.0  # Seconds between damage ticks
    attack_range: int = 50  # Pixels
    attack_cooldown: float = 0.5  # Seconds between attacks


@dataclass
class ZombieConfig:
    """Zombie entity settings"""
    radius: int = 12
    color: tuple = (200, 50, 50)  # Red
    speed: int = 80  # Pixels per second
    damage: int = 10  # Damage per hit


@dataclass
class UIConfig:
    """UI/HUD settings (all positions as ratios of screen dimensions)"""
    # Health bar positioning (relative to screen size)
    health_bar_x_ratio: float = 0.0125  # 1.25% from left edge
    health_bar_y_ratio: float = 0.0167  # 1.67% from top edge
    health_bar_width_ratio: float = 0.25  # 25% of screen width
    health_bar_height: int = 30  # Fixed height in pixels

    # Health bar colors
    health_bar_bg_color: tuple = (200, 0, 0)  # Red background
    health_bar_fg_color: tuple = (0, 200, 0)  # Green foreground
    health_bar_border_color: tuple = (255, 255, 255)  # White border
    health_bar_border_width: int = 2

    # Font
    font_size: int = 36
    text_color: tuple = (255, 255, 255)  # White


# Global config instances
game_config = GameConfig()
player_config = PlayerConfig()
zombie_config = ZombieConfig()
ui_config = UIConfig()