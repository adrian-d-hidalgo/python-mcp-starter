"""
Tests for the {{prompt_name}} prompt.
"""

import pytest
from mcp.server.fastmcp import FastMCP

from src.prompts.{{prompt_name}} import set_prompts


@pytest.fixture
def mcp():
    """Create a FastMCP instance for testing."""
    return FastMCP()


@pytest.fixture
def prompt(mcp):
    """Register and return the {{prompt_name}} prompt."""
    set_prompts(mcp)
    return mcp.prompts["{{prompt_name}}"]


def test_{{prompt_name}}_basic(prompt):
    """Test basic functionality of {{prompt_name}}."""
    context = {"user_input": "test input"}
    result = prompt(context)
    assert isinstance(result, str)
    assert "test input" in result


def test_{{prompt_name}}_with_options(prompt):
    """Test {{prompt_name}} with custom options."""
    context = {"user_input": "test input"}
    options = {"style": "formal"}
    result = prompt(context, options)
    assert isinstance(result, str)
    assert "formal manner" in result


def test_{{prompt_name}}_empty_context(prompt):
    """Test {{prompt_name}} with empty context."""
    context = {}
    result = prompt(context)
    assert isinstance(result, str)
    assert "" in result


def test_{{prompt_name}}_none_options(prompt):
    """Test {{prompt_name}} with None options."""
    context = {"user_input": "test input"}
    result = prompt(context, None)
    assert isinstance(result, str)
    assert "test input" in result
