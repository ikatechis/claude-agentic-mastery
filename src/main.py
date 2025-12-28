"""
Entry point for Zombie Survival game
Run with: uv run python src/main.py
Debug mode: GAME_DEBUG=1 uv run python src/main.py
"""

from game import Game
from logger import get_logger, setup_logging

logger = get_logger(__name__)


def main():
    """Start the game"""
    # Initialize logging system
    setup_logging()

    try:
        logger.info("Game started")
        game = Game()
        game.run()
        logger.info("Game ended normally")
    except KeyboardInterrupt:
        logger.info("Game interrupted by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
