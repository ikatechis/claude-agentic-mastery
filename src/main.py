"""
Entry point for Zombie Survival game
Run with: uv run python src/main.py
"""

from game import Game


def main():
    """Start the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
