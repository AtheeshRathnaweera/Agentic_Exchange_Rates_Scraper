import os
from logging.handlers import RotatingFileHandler
import logging


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Optional: colored logs for terminal (install via pip install colorlog)
try:
    import colorlog
    COLOR_AVAILABLE = True
except ImportError:
    COLOR_AVAILABLE = False


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger instance that logs to both console and file."""
    logger = logging.getLogger(name)

    if not logger.handlers:  # Prevent duplicate logs
        logger.setLevel(logging.DEBUG)

        # --- Console Handler (shows in terminal) ---
        console_handler = logging.StreamHandler()
        if COLOR_AVAILABLE:
            console_formatter = colorlog.ColoredFormatter(
                "%(log_color)s[%(asctime)s] [%(levelname)s] %(name)s.%(funcName)s:%(reset)s %(message)s",
                datefmt="%H:%M:%S",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            )
        else:
            console_formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(name)s.%(funcName)s: %(message)s",
                datefmt="%H:%M:%S",
            )
        console_handler.setFormatter(console_formatter)

        # --- File Handler (persistent logs) ---
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s.%(funcName)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)

        # --- Add both handlers ---
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
