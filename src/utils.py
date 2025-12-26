"""Utility functions for the Zombie Survival game."""

import contextlib

import pygame


def load_sprite(path: str, size: int) -> pygame.Surface | None:
    """Load and scale a sprite image with error handling.

    Args:
        path: Path to the sprite image file
        size: Target size (width and height) for the sprite

    Returns:
        Scaled pygame Surface, or None if loading fails
    """
    with contextlib.suppress(pygame.error, FileNotFoundError):
        sprite = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(sprite, (int(size), int(size)))
    return None
