"""
Basic prompts for the MCP server.
"""

from mcp.server.fastmcp import FastMCP


def set_prompts(mcp: FastMCP) -> None:
    """
    Set basic prompts with the MCP server.

    Args:
        mcp: The MCP server instance.
    """

    @mcp.prompt(name="greeting")
    def greeting_prompt() -> str:
        """Return a greeting prompt.

        Returns:
            A greeting prompt.
        """
        return "You are a helpful assistant. Always be polite and professional."

    @mcp.prompt(name="error_handling")
    def error_handling_prompt() -> str:
        """Return an error handling prompt.

        Returns:
            An error handling prompt.
        """
        return "When encountering errors, provide clear explanations and suggest solutions."
