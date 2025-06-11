"""
Basic resources for the MCP server.
"""

from mcp.server.fastmcp import FastMCP


def set_resources(mcp: FastMCP) -> None:
    """
    Set basic resources with the MCP server.

    Args:
        mcp: The MCP server instance.
    """

    @mcp.resource(name="server_info", uri="server://info")
    def server_info() -> dict:
        """Return server information.

        Returns:
            A dictionary containing server information.
        """
        return {
            "version": "1.0.0",
            "description": "MCP Server Template",
            "capabilities": ["tools", "prompts", "resources"],
        }
