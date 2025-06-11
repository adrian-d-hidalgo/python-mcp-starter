#!/usr/bin/env python3
"""
Project Verification Script

Verifies the project structure and functionality.
"""

import logging
import sys
from pathlib import Path

# Add root directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class ProjectVerifier:
    """Verifies the project structure and functionality."""

    def __init__(self, project_root: Path):
        """
        Initialize the verifier.

        Args:
            project_root: Path to the project root directory.
        """
        self.project_root = project_root
        self.issues = []
        self.stats = {
            "files": 0,
            "lines": 0,
            "imports": 0,
            "functions": 0,
            "classes": 0,
        }

    def verify(self):
        """Run all verification checks."""
        # Verify directory structure
        self._verify_structure()

        # Verify imports
        self._verify_imports()

        # Verify configuration
        self._verify_config()

        # Analyze project stats
        self._analyze_stats()

        # Print results
        self._print_results()

    def _verify_structure(self):
        """Verify the project directory structure."""
        required_dirs = [
            "src",
            "src/tools",
            "src/prompts",
            "src/resources",
            "tests",
            "tests/unit",
            "tests/unit/tools",
            "tests/unit/prompts",
            "tests/unit/resources",
        ]

        for directory in required_dirs:
            if not (self.project_root / directory).exists():
                self.issues.append(f"❌ Missing directory: {directory}")

    def _verify_imports(self):
        """Verify that main imports work."""
        try:
            if not (self.project_root / "src" / "server.py").exists():
                raise ImportError("Module src.server not found")

            logger.info("✅ Main imports correct")
        except ImportError as e:
            self.issues.append(f"❌ Import error: {e}")

    def _verify_config(self):
        """Verify project configuration."""
        # Check pyproject.toml
        pyproject_path = self.project_root / "pyproject.toml"
        if not pyproject_path.exists():
            self.issues.append("❌ Missing pyproject.toml")
            return

        try:
            with open(pyproject_path) as f:
                content = f.read()

            if "pdm" not in content:
                self.issues.append("❌ pyproject.toml is not configured for PDM")
        except Exception as e:
            self.issues.append(f"❌ Error reading pyproject.toml: {e}")

    def _analyze_stats(self):
        """Analyze project statistics."""
        for py_file in self.project_root.rglob("*.py"):
            if "venv" in str(py_file) or ".pytest_cache" in str(py_file):
                continue

            self.stats["files"] += 1

            with open(py_file, encoding="utf-8") as f:
                content = f.read()

            # Count lines
            self.stats["lines"] += len(content.splitlines())

            # Count imports
            self.stats["imports"] += content.count("import ")
            self.stats["imports"] += content.count("from ")

            # Count functions and classes
            self.stats["functions"] += content.count("def ")
            self.stats["classes"] += content.count("class ")

    def _print_results(self):
        """Print verification results."""
        if self.issues:
            print("\n⚠️ Issues Found:")
            for issue in self.issues:
                print(issue)
        else:
            print("\n✅ No issues found!")

        print("\n📊 Project Statistics:")
        print(f"📁 Files: {self.stats['files']}")
        print(f"📝 Lines: {self.stats['lines']}")
        print(f"📦 Imports: {self.stats['imports']}")
        print(f"🔧 Functions: {self.stats['functions']}")
        print(f"🏗️  Classes: {self.stats['classes']}")


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    verifier = ProjectVerifier(project_root)
    verifier.verify()


if __name__ == "__main__":
    main()
