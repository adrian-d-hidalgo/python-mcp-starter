"""
📋 Logging Configuration Module

Provides centralized logging configuration for the MCP server.
Follows the Single Responsibility Principle by separating logging concerns.
"""

import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure structured logging for the application.

    Args:
        level: The logging level to use (default: logging.INFO)
    """
    # Configure structured logging
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Configure uvicorn loggers
    if level > logging.DEBUG:
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.error").setLevel(logging.ERROR)


# Create logger instance
logger = logging.getLogger("mcp_server")
