"""
Tests for the {{tool_name}} tool.
"""

import pytest
from mcp.server.fastmcp import FastMCP

from src.tools.{{tool_name}} import set_tools


@pytest.fixture
def mcp():
    """Create a FastMCP instance for testing."""
    return FastMCP()


@pytest.fixture
def tool(mcp):
    """Register and return the {{tool_name}} tool."""
    set_tools(mcp)
    return mcp.tools["{{tool_name}}"]


def test_{{tool_name}}_basic(tool):
    """Test basic functionality of {{tool_name}}."""
    result = tool("test input")
    assert isinstance(result, dict)
    assert "result" in result
    assert "metadata" in result
    assert "Processed: test input" in result["result"]


def test_{{tool_name}}_with_options(tool):
    """Test {{tool_name}} with custom options."""
    options = {"option1": "value1", "option2": "value2"}
    result = tool("test input", options)
    assert isinstance(result, dict)
    assert result["metadata"]["options_used"] == options


def test_{{tool_name}}_empty_input(tool):
    """Test {{tool_name}} with empty input."""
    result = tool("")
    assert isinstance(result, dict)
    assert "result" in result
    assert "metadata" in result


def test_{{tool_name}}_none_options(tool):
    """Test {{tool_name}} with None options."""
    result = tool("test input", None)
    assert isinstance(result, dict)
    assert result["metadata"]["options_used"] == {}
