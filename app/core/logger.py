import sys
from loguru import logger


def configure_logger(debug: bool) -> None:
    """Configure structured application logging."""

    logger.remove()

    log_level = "DEBUG" if debug else "INFO"

    logger.add(
        sys.stdout,
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )