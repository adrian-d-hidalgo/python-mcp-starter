"""
Tests for the {{resource_name}} resource.
"""

import pytest
from mcp.server.fastmcp import FastMCP

from src.resources.{{resource_name}} import set_resources


@pytest.fixture
def mcp():
    """Create a FastMCP instance for testing."""
    return FastMCP()


@pytest.fixture
def resource(mcp):
    """Register and return the {{resource_name}} resource."""
    set_resources(mcp)
    return mcp.resources["/{{resource_name}}"]


def test_{{resource_name}}_basic(resource):
    """Test basic functionality of {{resource_name}}."""
    request = {"query": "test query"}
    result = resource(request)
    assert isinstance(result, dict)
    assert "data" in result
    assert "metadata" in result
    assert "test query" in result["data"]


def test_{{resource_name}}_with_options(resource):
    """Test {{resource_name}} with custom options."""
    request = {"query": "test query"}
    options = {"format": "json"}
    result = resource(request, options)
    assert isinstance(result, dict)
    assert result["metadata"]["format"] == "json"


def test_{{resource_name}}_empty_request(resource):
    """Test {{resource_name}} with empty request."""
    request = {}
    result = resource(request)
    assert isinstance(result, dict)
    assert "data" in result
    assert "metadata" in result


def test_{{resource_name}}_none_options(resource):
    """Test {{resource_name}} with None options."""
    request = {"query": "test query"}
    result = resource(request, None)
    assert isinstance(result, dict)
    assert result["metadata"]["options_used"] == {}
