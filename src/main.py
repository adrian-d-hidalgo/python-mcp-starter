#!/usr/bin/env python
"""
Main entry point for the MCP server with optimized performance settings.
"""

import argparse
import logging
import multiprocessing
import os
import sys

from src.server import MCPServer

# Configure logging with optimized settings
logger = logging.getLogger(__name__)


def setup_logging(debug: bool = False) -> None:
    """Configure logging with performance optimizations.

    Args:
        debug: Whether to enable debug logging.
    """
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Disable some verbose loggers in production
    if not debug:
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.error").setLevel(logging.ERROR)


def get_default_workers() -> int:
    """Get the default number of worker processes.

    Returns:
        Recommended number of worker processes based on CPU cores.
    """
    cpu_count = multiprocessing.cpu_count()
    # Use CPU count but cap at 8 workers for most efficient performance
    return min(cpu_count, 8)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments with extended options.

    Returns:
        Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="MCP Server with optimized performance",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Server configuration
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with verbose logging",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("MCP_HOST", "0.0.0.0"),
        help="Host to bind the server to",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MCP_PORT", "8000")),
        help="Port to bind the server to",
    )

    # Performance settings
    parser.add_argument(
        "--workers",
        type=int,
        default=int(os.getenv("MCP_WORKERS", "0")),
        help="Number of worker processes (0 for auto-detection)",
    )
    parser.add_argument(
        "--no-auto-register",
        action="store_true",
        help="Disable automatic component registration",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes",
    )

    return parser.parse_args()


def main() -> int | None:
    """Main entry point for the MCP server.

    Returns:
        Exit code (0 for success, 1 for error, None for normal exit)
    """
    # Parse command line arguments
    args = parse_args()

    # Setup optimized logging
    setup_logging(args.debug)

    if args.debug:
        logger.info("🛠️ Starting in DEBUG mode")
    else:
        logger.info("🚀 Starting MCP server")

    try:
        # Calculate optimal number of workers
        workers = args.workers if args.workers > 0 else get_default_workers()

        if args.debug:
            logger.debug("Server configuration:")
            logger.debug(f"- Host: {args.host}")
            logger.debug(f"- Port: {args.port}")
            logger.debug(f"- Workers: {workers}")
            logger.debug(f"- Auto-register: {not args.no_auto_register}")
            logger.debug(f"- Reload: {args.reload}")

        # Create and run the server with optimized settings
        server = MCPServer(auto_register=not args.no_auto_register)
        server.run(
            host=args.host,
            port=args.port,
            workers=workers,
            reload=args.reload,
        )
        return 0

    except KeyboardInterrupt:
        logger.info("👋 Server stopped by user")
        return 0
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}", exc_info=args.debug)
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
