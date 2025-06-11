"""
{{tool_name}} - Tool Description

This tool provides functionality for [brief description of what the tool does].
"""

from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP


def set_tools(mcp: FastMCP) -> None:
    """Register tools with the MCP server.

    Args:
        mcp: The MCP server instance to register tools with.
    """
    @mcp.tool(name="{{tool_name}}")
    def {{tool_name}}(input_text: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process the input text with optional configuration.

        Args:
            input_text: The text to process.
            options: Optional configuration parameters.

        Returns:
            A dictionary containing the processed result and metadata.

        Example:
            ```python
            result = {{tool_name}}("example text", {"option": "value"})
            ```
        """
        # Initialize options if not provided
        options = options or {}

        # Process the input
        result = f"Processed: {input_text}"

        # Return structured response
        return {
            "result": result,
            "metadata": {
                "processed_at": "{{date}}",
                "options_used": options
            }
        }


# Example usage with more complex parameters:
"""
@mcp.tool(name="{{tool_name}}")
def {{tool_name}}(
    input_text: str,
    max_length: Optional[int] = None,
    format_type: str = "text",
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    \"\"\"Process text with advanced options.

    Args:
        input_text: The text to process.
        max_length: Maximum length of output (optional).
        format_type: Output format type (text, json, html).
        options: Additional processing options.

    Returns:
        A dictionary with the processed result and metadata.

    Example:
        ```python
        result = {{tool_name}}(
            "example text",
            max_length=100,
            format_type="json",
            options={"trim": True}
        )
        ```
    \"\"\"
    # Implementation here
    return {
        "result": processed_text,
        "metadata": {
            "format": format_type,
            "length": len(processed_text),
            "options_used": options
        }
    }
"""
