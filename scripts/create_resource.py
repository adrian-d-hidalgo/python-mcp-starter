#!/usr/bin/env python3
"""
🔄 MCP Resource Generator - Super Easy!

Script to automatically create new MCP resources.
Usage:
    python scripts/create_resource.py <name>

Example:
    python scripts/create_resource.py math
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


def create_resource(resource_name: str) -> bool:
    """
    Create a new MCP resource.

    Args:
        resource_name: Resource name in snake_case format.

    Returns:
        bool: True if the resource was created successfully.
    """
    # Validate name
    if not re.match(r"^[a-z][a-z0-9_]*$", resource_name):
        print(f"❌ Error: Name '{resource_name}' is invalid")
        print("   Must be snake_case and start with a letter")
        return False

    # Convert to snake_case if needed
    snake_name = re.sub(r"(?<!^)(?=[A-Z])", "_", resource_name).lower()

    # Create directories if they don't exist
    resources_dir = Path("src/resources")
    tests_dir = Path("tests/unit/resources")
    resources_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)

    # File paths
    new_file_path = resources_dir / f"{snake_name}.py"
    new_test_path = tests_dir / f"test_{snake_name}_resources.py"
    template_path = Path("templates/resource_template.py")
    test_template_path = Path("templates/test_resource_template.py")

    # Check if already exists
    if new_file_path.exists():
        print(f"❌ Error: Resource '{snake_name}' already exists")
        return False

    # Read and process template
    with open(template_path, encoding="utf-8") as f:
        content = f.read()

    # Replace placeholders
    content = content.replace("{{resource_name}}", snake_name)
    content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))

    # Write file
    with open(new_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Create test if template exists
    if test_template_path.exists():
        with open(test_template_path, encoding="utf-8") as f:
            test_content = f.read()

        # Replace placeholders in test
        test_content = test_content.replace("{{resource_name}}", snake_name)
        test_content = test_content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))

        # Write test
        with open(new_test_path, "w", encoding="utf-8") as f:
            f.write(test_content)

    print(f"✅ Resource '{snake_name}' created successfully")
    print(f"📁 File: {new_file_path}")
    if test_template_path.exists():
        print(f"📁 Test: {new_test_path}")

    print("\n📋 Next steps:")
    print(f"1. Edit {new_file_path} to implement your resources")
    print("2. Resources will be automatically loaded when the server restarts")
    print("3. Run: pdm run start to test your server")
    print("4. Run: pdm run test to verify it works")

    return True


def show_help():
    """Show script help."""
    print(
        """
🔄 MCP Resource Generator

Usage:
    python scripts/create_resource.py <name>

Example:
    python scripts/create_resource.py math

Features:
✅ Ready-to-use functional templates
✅ Dynamic auto-loading in server
✅ Automatic tests
✅ Included documentation
"""
    )


if __name__ == "__main__":
    if len(sys.argv) < MIN_ARGS:
        print("❌ Error: You must specify the resource name")
        print("   Usage: python create_resource.py <resource_name>")
        sys.exit(1)

    resource_name = sys.argv[1].strip()
    if not create_resource(resource_name):
        sys.exit(1)
