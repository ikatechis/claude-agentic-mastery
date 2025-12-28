"""Utility functions for the Zombie Survival game."""

import pygame

from logger import get_logger

logger = get_logger(__name__)


def load_sprite(path: str, size: int) -> pygame.Surface | None:
    """Load and scale a sprite image with error handling.

    Args:
        path: Path to the sprite image file
        size: Target size (width and height) for the sprite

    Returns:
        Scaled pygame Surface, or None if loading fails
    """
    try:
        sprite = pygame.image.load(path).convert_alpha()
        scaled = pygame.transform.scale(sprite, (int(size), int(size)))
        logger.debug(f"Loaded sprite: {path}")
        return scaled
    except (pygame.error, FileNotFoundError):
        logger.debug(f"Sprite not found: {path}, using fallback")
        return None
