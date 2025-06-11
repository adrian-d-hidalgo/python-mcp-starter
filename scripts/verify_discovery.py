#!/usr/bin/env python3
"""
Discovery Verification Script

Tests the MCP server's component discovery functionality.
"""

import sys
from pathlib import Path

# Add root directory to path
sys.path.append(str(Path(__file__).parent.parent))


def verify_discovery():
    """Verify that all components are discovered correctly."""
    try:
        # Test 1: Import server
        print("🧪 Test 1: Importing server...")
        from src.server import MCPServer

        print("✅ Server imported successfully")

        # Test 2: Create server
        print("\n🧪 Test 2: Creating server...")
        server = MCPServer()
        print("✅ Server created successfully")

        # Test 3: Verify components
        print("\n🧪 Test 3: Verifying components...")

        # Verify tools
        tools = server.mcp._tool_manager.list_tools()
        print(f"✅ Found {len(tools)} tools")
        for tool in tools[:5]:  # Show first 5 tools
            print(f"  - {tool.name}: {tool.description[:50]}...")

        # Verify resources
        resources = server.mcp._resource_manager.list_resources()
        print(f"\n✅ Found {len(resources)} resources")
        for resource in resources[:5]:  # Show first 5 resources
            print(f"  - {resource.uri}: {resource.name}")

        # Verify prompts
        prompts = server.mcp._prompt_manager.list_prompts()
        print(f"\n✅ Found {len(prompts)} prompts")
        for prompt in prompts[:5]:  # Show first 5 prompts
            print(
                f"  - {prompt.name}: {prompt.description[:50] if prompt.description else 'No description'}..."
            )

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    if not verify_discovery():
        sys.exit(1)
