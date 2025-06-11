"""
Tests for MCP server implementation.
"""

import pytest
from src.server import MCPServer


@pytest.fixture
def server():
    return MCPServer()


def test_server_initializes(server):
    """Test that server initializes correctly."""
    assert server.mcp is not None


def test_tool_registration(server):
    @server.mcp.tool()
    def test_tool():
        return "test"

    assert "test_tool" in server.mcp._tool_manager._tools


def test_duplicate_tool_registration(server):
    @server.mcp.tool()
    def test_tool1():
        return "test1"

    @server.mcp.tool()
    def test_tool2():
        return "test2"

    assert "test_tool2" in server.mcp._tool_manager._tools


def test_module_setup(server):
    # Test that modules can be set up
    server.set_modules("src.tools", "set_tools", server.mcp)
    assert "hello" in server.mcp._tool_manager._tools
    assert "echo" in server.mcp._tool_manager._tools
    assert "status" in server.mcp._tool_manager._tools


@pytest.mark.parametrize("module_path", ["nonexistent_module", "src.tools.nonexistent"])
def test_invalid_module_setup(server, module_path):
    with pytest.raises(ImportError):
        server.set_modules(module_path, "set_tools", server.mcp)


def run_manual_tests():
    """Run basic tests without pytest."""
    server = MCPServer()
    print("Server initialized successfully")

    @server.mcp.tool()
    def test_tool():
        return "test"

    print("Tool registered successfully")
    assert "test_tool" in server.mcp._tool_manager._tools
    print("Tool found in registered tools")

    server.set_modules("src.tools", "set_tools", server.mcp)
    print("Tools module set up successfully")
    assert "hello" in server.mcp._tool_manager._tools
    print("Basic tools found in registered tools")

    print("All tests passed!")


if __name__ == "__main__":
    run_manual_tests()
