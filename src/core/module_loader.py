"""Module loader for dynamically loading MCP components."""

import importlib
import importlib.util
from collections.abc import Callable
from pathlib import Path
from typing import Any, Protocol

from mcp.server.fastmcp import FastMCP

from src.core.logger import logger


class ModuleType(Protocol):
    """Protocol defining the expected module structure."""

    tools: dict[str, Callable[..., Any]]
    prompts: dict[str, Callable[..., Any]]
    resources: dict[str, Callable[..., Any]]


class ModuleLoader:
    """Loads and manages Python modules from the tools directory."""

    def __init__(self, mcp: FastMCP):
        """Initialize the module loader.

        Args:
            mcp: The FastMCP instance to use for registering components
        """
        self.mcp = mcp
        self.base_dir = Path(__file__).parent.parent
        self.component_dirs = {
            "tools": self.base_dir / "tools",
            "prompts": self.base_dir / "prompts",
            "resources": self.base_dir / "resources",
        }
        self.loaded_modules: dict[str, Any] = {}

    def load_all_modules(self) -> int:
        """Load all Python modules from the component directories.

        Returns:
            int: Number of components loaded
        """
        component_count = 0
        for dir_name, dir_path in self.component_dirs.items():
            if not dir_path.exists():
                logger.warning(f"Directory not found: {dir_path}")
                continue

            for py_file in dir_path.glob("*.py"):
                if py_file.name.startswith("__"):
                    continue

                try:
                    module = self._load_module(py_file)
                    if module:
                        self.loaded_modules[py_file.stem] = module
                        component_count += 1
                        logger.info(f"Loaded {dir_name} module: {py_file.stem}")
                except Exception as e:
                    logger.error(f"Error loading module {py_file}: {e}")

        return component_count

    def _load_module(self, file_path: Path) -> Any | None:
        """Load a Python module from a file.

        Args:
            file_path: Path to the Python file

        Returns:
            Optional[Any]: Loaded module or None if loading failed
        """
        try:
            spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
            if not spec or not spec.loader:
                return None

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Register components if they exist
            if hasattr(module, "set_resources"):
                module.set_resources(self.mcp)
            if hasattr(module, "set_prompts"):
                module.set_prompts(self.mcp)
            if hasattr(module, "set_tools"):
                module.set_tools(self.mcp)

            return module

        except Exception as e:
            logger.error(f"Error loading module {file_path}: {e}")
            return None

    def get_module(self, name: str) -> Any | None:
        """Get a loaded module by name.

        Args:
            name: Name of the module to get

        Returns:
            Optional[Any]: The loaded module or None if not found
        """
        return self.loaded_modules.get(name)

    def list_modules(self) -> list[str]:
        """List all loaded module names.

        Returns:
            List[str]: List of loaded module names
        """
        return list(self.loaded_modules.keys())
