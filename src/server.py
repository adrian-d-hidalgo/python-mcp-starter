"""
MCP Server - Core Server Logic and Initialization

This module contains the MCP server instance and all server-related functionality.
"""

import asyncio
import importlib
import os
from typing import Any, cast

import uvicorn
from mcp.server.fastmcp import FastMCP

from src.core.logger import logger
from src.core.module_loader import ModuleLoader, ModuleType


class MCPServer:
    """MCP Server implementation with optimized loading and caching."""

    def __init__(self, auto_register: bool = True):
        """
        Initialize the MCP server.

        Args:
            auto_register: Whether to automatically register all components.
        """
        # Initialize FastMCP with optimized settings
        self.mcp = FastMCP(
            name="mcp-server-template",
            instructions="MCP Server Template with modular tools, prompts, and resources",
            json_response=False,
            stateless_http=False,
            # Enable FastAPI performance optimizations
            docs_url=None,  # Disable docs in production
            redoc_url=None,  # Disable redoc in production
        )

        # Initialize component tracking
        self._registered_modules: list[str] = []
        self._module_cache: dict[str, Any] = {}
        self._component_count: int = 0

        # Register components if auto_register is True
        if auto_register:
            self._register_all_components()

    async def _register_module_async(self, module_name: str) -> None:
        """Register a module asynchronously with the server.

        Args:
            module_name: The name of the module to register.
        """
        if module_name in self._registered_modules:
            logger.debug(f"Module {module_name} is already registered")
            return

        try:
            # Use cached module if available
            if module_name in self._module_cache:
                module = self._module_cache[module_name]
            else:
                module = importlib.import_module(module_name)
                self._module_cache[module_name] = module

            self._registered_modules.append(module_name)
            logger.debug(f"Registered module: {module_name}")

            # Register components concurrently
            if not all(hasattr(module, attr) for attr in ["tools", "prompts", "resources"]):
                logger.warning(f"Module {module_name} is missing required attributes")
                return

            module_typed = cast(ModuleType, module)
            await asyncio.gather(
                self._register_tools(module_typed, module_name),
                self._register_prompts(module_typed, module_name),
                self._register_resources(module_typed, module_name),
            )

        except ImportError as e:
            logger.error(f"Failed to import module {module_name}: {e}")
            raise

    async def _register_tools(self, module: ModuleType, module_name: str) -> None:
        """Register tools from a module asynchronously."""
        if hasattr(module, "tools"):
            for tool_name, func in module.tools.items():
                self.mcp.tool()(func)
                self._component_count += 1
                logger.debug(f"Registered tool: {tool_name} from {module_name}")

    async def _register_prompts(self, module: ModuleType, module_name: str) -> None:
        """Register prompts from a module asynchronously."""
        if hasattr(module, "prompts"):
            for prompt_name, func in module.prompts.items():
                self.mcp.prompt()(func)
                self._component_count += 1
                logger.debug(f"Registered prompt: {prompt_name} from {module_name}")

    async def _register_resources(self, module: ModuleType, module_name: str) -> None:
        """Register resources from a module asynchronously."""
        if hasattr(module, "resources"):
            for resource_name, func in module.resources.items():
                self.mcp.resource(uri=f"/{resource_name}")(func)
                self._component_count += 1
                logger.debug(f"Registered resource: {resource_name} from {module_name}")

    def _register_all_components(self) -> None:
        """Register all components from the tools directory."""
        module_loader = ModuleLoader(self.mcp)
        self._component_count = module_loader.load_all_modules()
        logger.info(f"🎯 Loaded {self._component_count} components")

    def run(
        self,
        host: str = "0.0.0.0",
        port: int = 8000,
        workers: int | None = None,
        reload: bool = False,
    ) -> None:
        """Run the MCP server.

        Args:
            host: The host to bind to.
            port: The port to bind to.
            workers: Number of worker processes. If None, uses min(CPU count, 8).
            reload: Whether to enable auto-reload on code changes.
        """
        try:
            # Configure Uvicorn with optimized settings
            config = uvicorn.Config(
                app=self.mcp.streamable_http_app,
                host=host,
                port=port,
                workers=workers or min(os.cpu_count() or 1, 8),
                loop="uvloop",  # Use uvloop for better performance
                http="httptools",  # Use httptools for faster HTTP parsing
                log_level="info",
                access_log=False,  # Disable access logs in production
                proxy_headers=True,  # Enable proxy headers
                server_header=False,  # Don't send server header
                reload=reload,  # Enable auto-reload in development
                reload_dirs=["src"],  # Monitor the src directory for changes
                reload_delay=0.25,  # Small delay to prevent multiple reloads
            )
            server = uvicorn.Server(config)
            server.run()
        except Exception as e:
            logger.error(f"Failed to run server: {e}")
            raise
