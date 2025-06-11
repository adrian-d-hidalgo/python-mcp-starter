#!/usr/bin/env python3
"""
🛠️ MCP Tool Generator - Super Easy!

Script to automatically create new MCP tools.
Usage:
    python scripts/create_tool.py <name>

Example:
    python scripts/create_tool.py calculator
"""

import re
import sys
from datetime import datetime
from pathlib import Path

# Constants
MIN_ARGS = 2


def to_snake_case(name):
    """Convert to snake_case for file names."""
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    name = re.sub(r"([A-Z])", r"_\1", name).lower()
    return re.sub(r"^_+|_+$", "", name)


def to_title_case(name):
    """Convert to Title Case for documentation."""
    return name.replace("_", " ").title()


def create_tool(tool_name: str) -> bool:
    """
    Create a new MCP tool.

    Args:
        tool_name: Tool name in snake_case format.

    Returns:
        bool: True if the tool was created successfully.
    """
    # Validate name
    if not re.match(r"^[a-z][a-z0-9_]*$", tool_name):
        print(f"❌ Error: Name '{tool_name}' is invalid")
        print("   Must be snake_case and start with a letter")
        return False

    # Convert to snake_case if needed
    snake_name = re.sub(r"(?<!^)(?=[A-Z])", "_", tool_name).lower()

    # Create directories if they don't exist
    tools_dir = Path("src/tools")
    tests_dir = Path("tests/unit/tools")
    tools_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)

    # File paths
    new_file_path = tools_dir / f"{snake_name}.py"
    new_test_path = tests_dir / f"test_{snake_name}.py"
    template_path = Path("templates/tool_template.py")
    test_template_path = Path("templates/test_tool_template.py")

    # Check if already exists
    if new_file_path.exists():
        print(f"❌ Error: Tool '{snake_name}' already exists")
        return False

    # Read and process template
    with open(template_path, encoding="utf-8") as f:
        content = f.read()

    # Replace placeholders
    content = content.replace("{{tool_name}}", snake_name)
    content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))

    # Write file
    with open(new_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Create test if template exists
    if test_template_path.exists():
        with open(test_template_path, encoding="utf-8") as f:
            test_content = f.read()

        # Replace placeholders in test
        test_content = test_content.replace("{{tool_name}}", snake_name)
        test_content = test_content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))

        # Write test
        with open(new_test_path, "w", encoding="utf-8") as f:
            f.write(test_content)

    print(f"✅ Tool '{snake_name}' created successfully")
    print(f"📁 File: {new_file_path}")
    if test_template_path.exists():
        print(f"📁 Test: {new_test_path}")

    print("\n📋 Next steps:")
    print(f"1. Edit {new_file_path} to implement your logic")
    print("2. The tool will be automatically loaded when the server restarts")
    print("3. Run: pdm run start to test your server")
    print("4. Run: pdm run test to verify it works")

    return True


def show_help():
    """Show script help."""
    print(
        """
🛠️  MCP Tool Generator

Usage:
    python scripts/create_tool.py <name>

Example:
    python scripts/create_tool.py calculator

Features:
✅ Ready-to-use functional templates
✅ Dynamic auto-loading in server
✅ Automatic tests
✅ Included documentation
"""
    )


if __name__ == "__main__":
    if len(sys.argv) < MIN_ARGS:
        print("❌ Error: You must specify the tool name")
        print("   Usage: python create_tool.py <tool_name>")
        sys.exit(1)

    tool_name = sys.argv[1].strip()
    if not create_tool(tool_name):
        sys.exit(1)
