"""
MCP Server Template Package

This package provides a complete MCP server implementation with:
- FastMCP-based server
- Example tools for file operations and API integration
- Resources for configuration and help
- Prompts for debugging and code review
"""

from mcp.server.fastmcp import FastMCP

__version__ = "0.1.0"

# Export FastMCP for use in other modules
__all__ = ["FastMCP"]
