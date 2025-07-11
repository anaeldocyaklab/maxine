#!/usr/bin/env python3
"""
Setup script for MAXINE development environment.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔧 {description}...")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {' '.join(cmd)}")
        print(f"   Error: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up MAXINE development environment")
    print()

    project_root = Path(__file__).parent.parent

    # Check if poetry is available
    if not run_command(["poetry", "--version"], "Checking Poetry installation"):
        print("❌ Poetry is not installed. Please install Poetry first:")
        print("   https://python-poetry.org/docs/#installation")
        return 1

    # Install dependencies
    if not run_command(["poetry", "install"], "Installing dependencies"):
        return 1

    # Install pre-commit hooks
    if not run_command(
        ["poetry", "run", "pre-commit", "install"], "Installing pre-commit hooks"
    ):
        return 1

    # Run pre-commit on all files to ensure everything works
    print("🔍 Running initial pre-commit check...")
    try:
        subprocess.run(
            ["poetry", "run", "pre-commit", "run", "--all-files"],
            check=False,  # Don't fail if there are issues, just report
            cwd=project_root,
        )
        print("✅ Pre-commit setup completed")
    except subprocess.CalledProcessError:
        print(
            "⚠️  Pre-commit found issues. Run 'poetry run pre-commit run --all-files' to see details."
        )

    print()
    print("🎉 Development environment setup complete!")
    print()
    print("📝 Next steps:")
    print("   1. Create a feature branch: git checkout -b feature/your-feature")
    print("   2. Make your changes")
    print("   3. Commit your changes (pre-commit hooks will run automatically)")
    print("   4. Push and create a pull request")
    print()
    print("💡 Useful commands:")
    print("   - Run tests: poetry run pytest")
    print("   - Format code: poetry run black src/")
    print("   - Check linting: poetry run ruff check src/")
    print("   - Run pre-commit: poetry run pre-commit run --all-files")
    print("   - Start server: poetry run maxine")

    return 0


if __name__ == "__main__":
    sys.exit(main())
