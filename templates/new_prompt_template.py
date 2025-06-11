"""
{{prompt_name}} - Prompt Template

This prompt template provides a structured way to [brief description of what the prompt does].
"""

from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP


def set_prompts(mcp: FastMCP) -> None:
    """Register prompts with the MCP server.

    Args:
        mcp: The MCP server instance to register prompts with.
    """
    @mcp.prompt(name="{{prompt_name}}")
    def {{prompt_name}}(context: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> str:
        """Generate a prompt based on context and options.

        Args:
            context: The context information for prompt generation.
            options: Optional configuration parameters.

        Returns:
            A formatted prompt string.

        Example:
            ```python
            prompt = {{prompt_name}}(
                {"user_input": "example"},
                {"style": "formal"}
            )
            ```
        """
        # Initialize options if not provided
        options = options or {}

        # Extract context information
        user_input = context.get("user_input", "")
        style = options.get("style", "default")

        # Generate prompt based on style
        if style == "formal":
            prompt = f"Please process the following input in a formal manner: {user_input}"
        else:
            prompt = f"Process this input: {user_input}"

        return prompt


# Example usage with more complex prompt generation:
"""
@mcp.prompt(name="{{prompt_name}}")
def {{prompt_name}}(
    context: Dict[str, Any],
    template: str = "default",
    variables: Optional[Dict[str, Any]] = None,
    options: Optional[Dict[str, Any]] = None
) -> str:
    \"\"\"Generate a prompt using templates and variables.

    Args:
        context: The context information for prompt generation.
        template: The template to use (default, formal, casual).
        variables: Additional variables for template interpolation.
        options: Configuration options for prompt generation.

    Returns:
        A formatted prompt string.

    Example:
        ```python
        prompt = {{prompt_name}}(
            {"user_input": "example"},
            template="formal",
            variables={"tone": "professional"},
            options={"max_length": 100}
        )
        ```
    \"\"\"
    # Implementation here
    return formatted_prompt
"""
