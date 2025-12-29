"""
Sound effects system for Zombie Survival game.
Handles loading and playing retro/8-bit sound effects from Kenney audio assets.

Usage:
    from sound import init_sounds, play_sound

    # In Game.__init__():
    init_sounds()

    # When event occurs:
    play_sound("fire")
"""

import os
from pathlib import Path

import pygame

from config import sound_config
from logger import get_logger

logger = get_logger(__name__)

# Module-level sound cache
_sounds: dict[str, pygame.mixer.Sound] = {}
_initialized: bool = False


def init_sounds() -> None:
    """Initialize the sound system and preload all sounds.

    Must be called AFTER pygame.init().
    Gracefully handles missing files - game continues without sound.
    """
    global _initialized

    if not sound_config.enabled:
        logger.info("Sound system disabled by config")
        return

    if _initialized:
        logger.debug("Sound system already initialized")
        return

    # Initialize pygame mixer
    try:
        pygame.mixer.init()
        logger.debug("pygame.mixer initialized")
    except pygame.error as e:
        # Try dummy audio driver as fallback (for testing/headless environments)
        logger.warning(f"Failed to initialize pygame.mixer with default driver: {e}")
        logger.info("Trying SDL dummy audio driver for testing...")
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        try:
            pygame.mixer.init()
            logger.info("pygame.mixer initialized with dummy audio driver (no sound output)")
        except pygame.error as e2:
            logger.warning(f"Failed to initialize pygame.mixer with dummy driver: {e2}")
            return

    # Sound file mappings: event_name -> filename
    sound_files = {
        "fire": "fire.ogg",
        "reload_start": "reload_start.ogg",
        "reload_complete": "reload_complete.ogg",
        "zombie_death": "zombie_death.ogg",
        "player_damage": "player_damage.ogg",
        "shield_block": "shield_block.ogg",
        "powerup_collect": "powerup_collect.ogg",
        "wave_start": "wave_start.ogg",
        "wave_complete": "wave_complete.ogg",
        "game_over": "game_over.ogg",
    }

    # Volume mappings (from config)
    volumes = {
        "fire": sound_config.fire_volume,
        "reload_start": sound_config.reload_start_volume,
        "reload_complete": sound_config.reload_complete_volume,
        "zombie_death": sound_config.zombie_death_volume,
        "player_damage": sound_config.player_damage_volume,
        "shield_block": sound_config.shield_block_volume,
        "powerup_collect": sound_config.powerup_collect_volume,
        "wave_start": sound_config.wave_start_volume,
        "wave_complete": sound_config.wave_complete_volume,
        "game_over": sound_config.game_over_volume,
    }

    sounds_dir = Path(sound_config.sounds_dir)
    loaded_count = 0

    for name, filename in sound_files.items():
        sound_path = sounds_dir / filename
        try:
            sound = pygame.mixer.Sound(str(sound_path))
            # Apply master volume * individual volume
            sound.set_volume(sound_config.master_volume * volumes.get(name, 1.0))
            _sounds[name] = sound
            loaded_count += 1
            logger.debug(f"Loaded sound: {name} from {sound_path}")
        except (pygame.error, FileNotFoundError) as e:
            logger.warning(f"Failed to load sound '{name}' from {sound_path}: {e}")

    _initialized = True
    logger.info(f"Sound system initialized: {loaded_count}/{len(sound_files)} sounds loaded")


def play_sound(name: str) -> None:
    """Play a sound effect by name.

    Args:
        name: Sound identifier (e.g., "fire", "zombie_death")

    Safe to call even if sound failed to load (graceful no-op).
    """
    if not sound_config.enabled:
        return

    if not _initialized:
        logger.debug(f"Sound system not initialized, skipping: {name}")
        return

    sound = _sounds.get(name)
    if sound:
        sound.play()
        logger.debug(f"Playing sound: {name}")
    else:
        logger.debug(f"Sound not loaded, skipping: {name}")


def set_master_volume(volume: float) -> None:
    """Update master volume for all sounds.

    Args:
        volume: Volume level (0.0 to 1.0)
    """
    sound_config.master_volume = max(0.0, min(1.0, volume))

    # Volume mappings (from config)
    volumes = {
        "fire": sound_config.fire_volume,
        "reload_start": sound_config.reload_start_volume,
        "reload_complete": sound_config.reload_complete_volume,
        "zombie_death": sound_config.zombie_death_volume,
        "player_damage": sound_config.player_damage_volume,
        "shield_block": sound_config.shield_block_volume,
        "powerup_collect": sound_config.powerup_collect_volume,
        "wave_start": sound_config.wave_start_volume,
        "wave_complete": sound_config.wave_complete_volume,
        "game_over": sound_config.game_over_volume,
    }

    # Update all loaded sounds
    for name, sound in _sounds.items():
        sound.set_volume(sound_config.master_volume * volumes.get(name, 1.0))

    logger.debug(f"Master volume set to: {volume}")


def toggle_sound(enabled: bool | None = None) -> bool:
    """Toggle sound on/off.

    Args:
        enabled: If None, toggle current state. Otherwise set explicitly.

    Returns:
        New enabled state
    """
    if enabled is None:
        sound_config.enabled = not sound_config.enabled
    else:
        sound_config.enabled = enabled

    logger.info(f"Sound {'enabled' if sound_config.enabled else 'disabled'}")
    return sound_config.enabled
