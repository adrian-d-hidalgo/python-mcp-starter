"""
{{resource_name}} - Resource Handler

This resource handler provides functionality for [brief description of what the resource does].
"""

from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP


def set_resources(mcp: FastMCP) -> None:
    """Register resources with the MCP server.

    Args:
        mcp: The MCP server instance to register resources with.
    """
    @mcp.resource(uri="/{{resource_name}}")
    def {{resource_name}}(request: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle resource requests with optional configuration.

        Args:
            request: The request data containing resource parameters.
            options: Optional configuration parameters.

        Returns:
            A dictionary containing the resource response and metadata.

        Example:
            ```python
            response = {{resource_name}}(
                {"query": "example"},
                {"format": "json"}
            )
            ```
        """
        # Initialize options if not provided
        options = options or {}

        # Extract request parameters
        query = request.get("query", "")
        format_type = options.get("format", "text")

        # Process the request
        result = f"Resource response for: {query}"

        # Return structured response
        return {
            "data": result,
            "metadata": {
                "format": format_type,
                "processed_at": "{{date}}",
                "options_used": options
            }
        }


# Example usage with more complex resource handling:
"""
@mcp.resource(uri="/{{resource_name}}")
def {{resource_name}}(
    request: Dict[str, Any],
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    \"\"\"Handle resource requests with advanced options.

    Args:
        request: The request data containing resource parameters.
        method: HTTP method (GET, POST, etc.).
        params: Additional URL parameters.
        options: Configuration options for resource handling.

    Returns:
        A dictionary with the resource response and metadata.

    Example:
        ```python
        response = {{resource_name}}(
            {"query": "example"},
            method="POST",
            params={"filter": "active"},
            options={"cache": True}
        )
        ```
    \"\"\"
    # Implementation here
    return {
        "data": processed_data,
        "metadata": {
            "method": method,
            "params": params,
            "options_used": options
        }
    }
"""
