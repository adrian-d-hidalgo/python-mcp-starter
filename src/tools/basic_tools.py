"""
Basic tools for the MCP server.
"""

from mcp.server.fastmcp import FastMCP


def set_tools(mcp: FastMCP) -> None:
    """
    Set basic tools with the MCP server.

    Args:
        mcp: The MCP server instance.
    """

    @mcp.tool(name="hello")
    def hello() -> str:
        """Return a greeting message.

        Returns:
            A friendly greeting message.
        """
        return "Hello from MCP server!"

    @mcp.tool(name="echo")
    def echo(message: str) -> str:
        """Echo back the input message.

        Args:
            message: The message to echo back.

        Returns:
            The same message.
        """
        return message

    @mcp.tool(name="status")
    def status() -> dict:
        """Get server status information.

        Returns:
            A dictionary containing server status information.
        """
        return {
            "status": "running",
            "version": "1.0.0",
            "uptime": "0:00:00",  # This should be calculated in a real implementation
        }
