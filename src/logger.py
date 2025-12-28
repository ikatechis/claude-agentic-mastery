"""
Logging configuration for Zombie Survival game
Provides dual output: console (WARNING+ or DEBUG+) and file (DEBUG+ always)
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path


def setup_logging() -> None:
    """Initialize the logging system.

    - Creates timestamped log file in logs/ directory
    - Console shows WARNING+ by default, DEBUG+ if GAME_DEBUG=1
    - File always captures DEBUG+ for full playtest history
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_file = log_dir / f"game_{timestamp}.log"

    # Check if debug mode is enabled
    debug_mode = os.getenv("GAME_DEBUG", "0") == "1"

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture everything

    # Remove any existing handlers (avoid duplicates)
    root_logger.handlers = []

    # Console handler - WARNING+ by default, DEBUG+ in debug mode
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if debug_mode else logging.WARNING)
    console_format = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)

    # File handler - always DEBUG+ for full playtest history
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    file_handler.setFormatter(file_format)
    root_logger.addHandler(file_handler)

    # Log the logging configuration
    logger = get_logger("logger")
    logger.info(f"Logging initialized - log file: {log_file}")
    logger.info(f"Debug mode: {'ON' if debug_mode else 'OFF'}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance configured with the game's logging system
    """
    return logging.getLogger(name)
