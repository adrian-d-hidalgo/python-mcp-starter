#!/usr/bin/env python3
"""
💬 MCP Prompt Generator - Super Easy!

Script to automatically create new MCP prompt modules.
Usage:
    python scripts/create_prompt.py <name>

Example:
    python scripts/create_prompt.py math
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


def create_prompt(prompt_name: str) -> bool:
    """
    Create a new MCP prompt.

    Args:
        prompt_name: Prompt name in snake_case format.

    Returns:
        bool: True if the prompt was created successfully.
    """
    # Validate name
    if not re.match(r"^[a-z][a-z0-9_]*$", prompt_name):
        print(f"❌ Error: Name '{prompt_name}' is invalid")
        print("   Must be snake_case and start with a letter")
        return False

    # Convert to snake_case if needed
    snake_name = re.sub(r"(?<!^)(?=[A-Z])", "_", prompt_name).lower()

    # Create directories if they don't exist
    prompts_dir = Path("src/prompts")
    tests_dir = Path("tests/unit/prompts")
    prompts_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)

    # File paths
    new_file_path = prompts_dir / f"{snake_name}.py"
    new_test_path = tests_dir / f"test_{snake_name}_prompts.py"
    template_path = Path("templates/prompt_template.py")
    test_template_path = Path("templates/test_prompt_template.py")

    # Check if already exists
    if new_file_path.exists():
        print(f"❌ Error: Prompt '{snake_name}' already exists")
        return False

    # Read and process template
    with open(template_path, encoding="utf-8") as f:
        content = f.read()

    # Replace placeholders
    content = content.replace("{{prompt_name}}", snake_name)
    content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))

    # Write file
    with open(new_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Create test if template exists
    if test_template_path.exists():
        with open(test_template_path, encoding="utf-8") as f:
            test_content = f.read()

        # Replace placeholders in test
        test_content = test_content.replace("{{prompt_name}}", snake_name)
        test_content = test_content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))

        # Write test
        with open(new_test_path, "w", encoding="utf-8") as f:
            f.write(test_content)

    print(f"✅ Prompt '{snake_name}' created successfully")
    print(f"📁 File: {new_file_path}")
    if test_template_path.exists():
        print(f"📁 Test: {new_test_path}")

    print("\n📋 Next steps:")
    print(f"1. Edit {new_file_path} to implement your prompts")
    print("2. Prompts will be automatically loaded when the server restarts")
    print("3. Run: pdm run start to test your server")
    print("4. Run: pdm run test to verify it works")

    return True


def show_help():
    """Show script help."""
    print(
        """
💬 MCP Prompt Generator

Usage:
    python scripts/create_prompt.py <name>

Example:
    python scripts/create_prompt.py math

Features:
✅ Ready-to-use functional templates
✅ Dynamic auto-loading in server
✅ Automatic tests
✅ Included documentation
"""
    )


if __name__ == "__main__":
    if len(sys.argv) < MIN_ARGS:
        print("❌ Error: You must specify the prompt name")
        print("   Usage: python create_prompt.py <prompt_name>")
        sys.exit(1)

    prompt_name = sys.argv[1].strip()
    if not create_prompt(prompt_name):
        sys.exit(1)
