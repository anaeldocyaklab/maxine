#!/usr/bin/env python3
"""
MAXINE Pre-commit Script

This script enforces project-specific coding standards and guidelines
for the MAXINE project before commits are allowed.
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional


class PreCommitChecker:
    """Pre-commit checker for MAXINE project standards."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def run_checks(self) -> bool:
        """Run all pre-commit checks and return True if all pass."""
        print("🔍 Running MAXINE pre-commit checks...")

        # Get list of staged files
        staged_files = self._get_staged_files()

        if not staged_files:
            print("ℹ️  No staged files to check")
            return True

        # Run checks
        self._check_commit_message()
        self._check_python_files(staged_files)
        self._check_imports(staged_files)
        self._check_docstrings(staged_files)
        self._check_test_coverage(staged_files)
        self._check_file_structure()
        self._check_environment_variables()

        # Report results
        self._report_results()

        return len(self.errors) == 0

    def _get_staged_files(self) -> List[str]:
        """Get list of staged files."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            return result.stdout.strip().split("\n") if result.stdout.strip() else []
        except subprocess.CalledProcessError:
            return []

    def _check_commit_message(self) -> None:
        """Check if commit message follows the template."""
        try:
            # Get the commit message
            result = subprocess.run(
                ["git", "log", "--format=%B", "-n", "1", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode != 0:
                # No commits yet or git error - skip this check
                return

            commit_msg = result.stdout.strip()
            if not commit_msg:
                return  # Empty commit message will be caught by git hooks

            # Check commit message format
            self._validate_commit_message(commit_msg)

        except subprocess.CalledProcessError:
            # Skip if we can't get commit message
            pass

    def _validate_commit_message(self, message: str) -> None:
        """Validate commit message format."""
        lines = message.split("\n")
        if not lines:
            return

        header = lines[0]

        # Check header format: type(scope): description
        pattern = r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z]+\))?: .{1,50}$"

        if not re.match(pattern, header):
            self.errors.append(
                f"❌ Commit message header doesn't follow format: "
                f"'type(scope): description'\n"
                f"   Current: '{header}'\n"
                f"   Example: 'feat(api): Add new endpoint for user data'\n"
                f"   See CONTRIBUTING.md for full guidelines"
            )

        # Check that header doesn't end with period
        if header.endswith("."):
            self.errors.append("❌ Commit message header should not end with a period")

        # Check body format if present
        if len(lines) > 1 and lines[1].strip():  # Second line should be empty
            self.warnings.append(
                "⚠️  Commit message should have a blank line after the header"
            )

    def _check_python_files(self, staged_files: List[str]) -> None:
        """Check Python files for standards compliance."""
        python_files = [f for f in staged_files if f.endswith(".py")]

        for file_path in python_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                continue

            self._check_python_file_standards(full_path, file_path)

    def _check_python_file_standards(self, full_path: Path, relative_path: str) -> None:
        """Check individual Python file for standards."""
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")

            self._check_shebang_line(content, relative_path)
            self._check_todo_comments(lines, relative_path)
            self._check_print_statements(lines, relative_path)
            self._check_long_lines(lines, relative_path)

        except Exception as e:
            self.warnings.append(f"⚠️  Could not check {relative_path}: {e}")

    def _check_shebang_line(self, content: str, relative_path: str) -> None:
        if not content.startswith("#!/usr/bin/env python3") and "src/" in relative_path:
            self.warnings.append(f"⚠️  {relative_path}: Consider adding shebang line")

    def _check_todo_comments(self, lines: List[str], relative_path: str) -> None:
        todo_pattern = r"#\s*(TODO|FIXME|XXX|HACK)"
        for i, line in enumerate(lines, 1):
            if re.search(todo_pattern, line, re.IGNORECASE):
                self.warnings.append(
                    f"⚠️  {relative_path}:{i}: Found TODO/FIXME comment: {line.strip()}"
                )

    def _check_print_statements(self, lines: List[str], relative_path: str) -> None:
        if "src/" in relative_path and "test" not in relative_path:
            print_pattern = r"\bprint\s*\("
            for i, line in enumerate(lines, 1):
                if re.search(print_pattern, line) and not line.strip().startswith("#"):
                    self.warnings.append(
                        f"⚠️  {relative_path}:{i}: Use logging instead of print() in source code"
                    )

    def _check_long_lines(self, lines: List[str], relative_path: str) -> None:
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                self.warnings.append(
                    f"⚠️  {relative_path}:{i}: Very long line ({len(line)} chars), consider breaking"
                )

    def _check_imports(self, staged_files: List[str]) -> None:
        """Check import statements in Python files."""
        python_files = [f for f in staged_files if f.endswith(".py")]

        for file_path in python_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                continue

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for relative imports in src/
                if "src/" in file_path:
                    if re.search(r"from\s+\.\.?\s+import", content):
                        # This is actually OK for internal imports, just flag for review
                        self.warnings.append(
                            f"⚠️  {file_path}: Uses relative imports - ensure they're appropriate"
                        )

                # Check for wildcard imports
                if re.search(r"from\s+\w+\s+import\s+\*", content):
                    self.errors.append(
                        f"❌ {file_path}: Avoid wildcard imports (from module import *)"
                    )

            except Exception as e:
                self.warnings.append(f"⚠️  Could not check imports in {file_path}: {e}")

    def _check_docstrings(self, staged_files: List[str]) -> None:
        """Check for proper docstrings in Python files."""
        python_files = [f for f in staged_files if f.endswith(".py") and "src/" in f]

        for file_path in python_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                continue

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                self._check_module_docstring(file_path, content)
                self._check_function_docstrings(file_path, content)

            except Exception as e:
                self.warnings.append(
                    f"⚠️  Could not check docstrings in {file_path}: {e}"
                )

    def _check_module_docstring(self, file_path: str, content: str) -> None:
        """Check if the module has a docstring."""
        stripped = content.strip()
        if not (stripped.startswith('"""') or stripped.startswith("'''")):
            lines = content.split("\n")
            found_docstring = False
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith('"""') or line.startswith("'''"):
                    found_docstring = True
                break

            if not found_docstring:
                self.warnings.append(f"⚠️  {file_path}: Missing module docstring")

    def _check_function_docstrings(self, file_path: str, content: str) -> None:
        """Check if public functions have docstrings."""
        func_pattern = r"def\s+([a-zA-Z_][\w]*)\s*\("
        functions = re.finditer(func_pattern, content)

        for match in functions:
            func_name = match.group(1)
            if not func_name.startswith("_"):  # Public functions
                start_pos = match.end()
                remaining = content[start_pos:]

                if '"""' not in remaining[:200] and "'''" not in remaining[:200]:
                    self.warnings.append(
                        f"⚠️  {file_path}: Function '{func_name}' missing docstring"
                    )

    def _check_test_coverage(self, staged_files: List[str]) -> None:
        """Check if changes to source files have corresponding tests."""
        src_files = [
            f for f in staged_files if f.startswith("src/") and f.endswith(".py")
        ]
        test_files = [f for f in staged_files if "test" in f and f.endswith(".py")]

        if src_files and not test_files:
            self.warnings.append(
                "⚠️  Modified source files but no test files. Consider adding/updating tests."
            )

        # Check if tests directory exists
        tests_dir = self.project_root / "tests"
        if src_files and not tests_dir.exists():
            self.warnings.append(
                "⚠️  No tests directory found. Consider creating tests for your code."
            )

    def _check_file_structure(self) -> None:
        """Check project file structure."""
        required_files = [
            "pyproject.toml",
            "README.md",
            "CONTRIBUTING.md",
            ".pre-commit-config.yaml",
        ]

        for file_name in required_files:
            if not (self.project_root / file_name).exists():
                self.errors.append(f"❌ Missing required file: {file_name}")

        # Check src directory structure
        src_dir = self.project_root / "src"
        if src_dir.exists():
            init_file = src_dir / "__init__.py"
            if not init_file.exists():
                self.warnings.append("⚠️  src/__init__.py missing")

    def _check_environment_variables(self) -> None:
        """Check for hardcoded secrets or sensitive information."""
        # This is a basic check - in a real project you might want more sophisticated checks
        env_file = self.project_root / ".env"
        if env_file.exists():
            try:
                with open(env_file, "r") as f:
                    content = f.read()

                # Check for potential secrets in .env file
                sensitive_patterns = [
                    r'password\s*=\s*["\']?[^"\'\s]+',
                    r'secret\s*=\s*["\']?[^"\'\s]+',
                    r'token\s*=\s*["\']?[^"\'\s]+',
                    r'key\s*=\s*["\']?[^"\'\s]+',
                ]

                for pattern in sensitive_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        self.warnings.append(
                            "⚠️  .env file may contain sensitive information. "
                            "Ensure it's in .gitignore and not committed."
                        )
                        break

            except Exception:
                pass

    def _report_results(self) -> None:
        """Report the results of all checks."""
        print()

        if self.errors:
            print("❌ PRE-COMMIT ERRORS (must fix):")
            for error in self.errors:
                print(f"  {error}")
            print()

        if self.warnings:
            print("⚠️  PRE-COMMIT WARNINGS (recommended to fix):")
            for warning in self.warnings:
                print(f"  {warning}")
            print()

        if not self.errors and not self.warnings:
            print("✅ All MAXINE pre-commit checks passed!")
        elif not self.errors:
            print("✅ No blocking errors found. Warnings can be addressed later.")
        else:
            print("❌ Pre-commit checks failed. Please fix the errors above.")
            print("\n💡 Tips:")
            print("  - See CONTRIBUTING.md for detailed guidelines")
            print("  - Run 'poetry run black src/' to format code")
            print("  - Run 'poetry run ruff check src/' to check linting")
            print("  - Run 'poetry run mypy src/' to check types")


def main() -> int:
    """Main entry point for pre-commit script."""
    checker = PreCommitChecker()

    try:
        success = checker.run_checks()
        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n❌ Pre-commit checks interrupted")
        return 1

    except Exception as e:
        print(f"\n❌ Error running pre-commit checks: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
