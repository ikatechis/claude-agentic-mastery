"""
Game configuration using dataclasses
All tunable game parameters organized by component

Last Updated: Session 3 - Wave-based spawning, score system, game states
"""

from dataclasses import dataclass


@dataclass
class GameConfig:
    """Main game settings"""

    screen_width: int = 800
    screen_height: int = 600
    fps: int = 60
    background_color: tuple = (50, 50, 50)  # Dark gray
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
    sprite_path: str = "assets/sprites/player.png"


@dataclass
class ZombieConfig:
    """Zombie entity settings"""

    radius: int = 12
    color: tuple = (200, 50, 50)  # Red
    speed: int = 70  # Pixels per second
    damage: int = 10  # Damage per hit
    sprite_path: str = "assets/sprites/zombie.png"


@dataclass
class WaveConfig:
    """Wave spawning system settings"""

    initial_zombies: int = 3  # Wave 1 zombie count
    zombies_per_wave_multiplier: float = 1.5  # Each wave multiplies by this
    max_zombies_per_wave: int = 20  # Cap to prevent performance issues
    wave_delay: float = 3.0  # Seconds between waves
    spawn_interval: float = 0.5  # Seconds between individual spawns


@dataclass
class ScoreConfig:
    """Score system settings"""

    points_per_kill: int = 10  # Points awarded per zombie kill
    score_x_ratio: float = 0.95  # 95% from left (right-aligned)
    score_y_ratio: float = 0.0167  # Same height as health bar


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

    # Wave notifications
    wave_notification_duration: float = 2.0  # Seconds to show "Wave X" message
    wave_font_size: int = 72  # Larger font for wave notifications

    # Visual effects
    kill_flash_duration: float = 0.2  # Seconds to show kill flash effect
    damage_popup_duration: float = 1.0  # Seconds to show damage popup


@dataclass
class PowerupConfig:
    """Power-up system settings"""

    # Spawning
    drop_chance: float = 0.2  # 20% on zombie death

    # Lifetime
    lifetime: float = 10.0  # Seconds before despawn
    warning_duration: float = 2.0  # Blink warning duration
    blink_frequency: float = 0.2  # Blink cycle time (0.1s on, 0.1s off)

    # Visual
    radius: int = 10
    health_color: tuple = (0, 255, 0)  # Green
    speed_color: tuple = (0, 255, 255)  # Cyan
    shield_color: tuple = (255, 215, 0)  # Gold

    # Effects
    health_restore_min: int = 30
    health_restore_max: int = 50
    speed_multiplier: float = 1.5
    speed_duration_min: float = 5.0
    speed_duration_max: float = 10.0
    shield_hits: int = 3

    # Visual effects
    pickup_flash_duration: float = 0.15


@dataclass
class KillFlash:
    """Visual effect for zombie kills"""

    x: float
    y: float
    radius: int
    timer: float


@dataclass
class PickupFlash:
    """Visual effect for power-up pickups"""

    x: float
    y: float
    radius: int
    color: tuple  # Matches power-up type color
    timer: float


@dataclass
class DamagePopup:
    """Visual effect for damage numbers"""

    x: float
    y: float
    text: str
    timer: float


@dataclass
class ProjectileConfig:
    """Projectile/bullet settings"""

    # Movement
    speed: float = 500.0  # Pixels per second

    # Visual
    radius: int = 4  # Collision radius
    color: tuple = (255, 255, 0)  # Yellow
    sprite_path: str = "assets/sprites/projectile.png"

    # Behavior
    lifetime: float = 2.0  # Seconds before despawn
    damage: int = 10  # Damage to zombies


@dataclass
class WeaponConfig:
    """Weapon/shooting settings (used by Player)"""

    max_ammo: int = 30  # Maximum ammunition
    fire_rate: float = 0.3  # Seconds between shots
    reload_time: float = 0.0  # Instant reload for now


# Global config instances
game_config = GameConfig()
player_config = PlayerConfig()
zombie_config = ZombieConfig()
wave_config = WaveConfig()
score_config = ScoreConfig()
ui_config = UIConfig()
powerup_config = PowerupConfig()
projectile_config = ProjectileConfig()
weapon_config = WeaponConfig()
