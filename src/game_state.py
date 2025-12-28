"""
Game state management using Enum pattern
Defines all possible game states for state machine
"""

from enum import Enum, auto


class GameState(Enum):
    """Enumeration of all possible game states"""

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
