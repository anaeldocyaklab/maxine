# Contributing to MAXINE

Thank you for your interest in contributing to MAXINE! This document provides guidelines and instructions for contributing to the project.

## 📝 Development Setup

### Prerequisites

- Python 3.13 or higher
- Poetry for dependency management
- Git for version control

### Getting Started

1. **Fork the repository**

   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**

   ```bash
   git clone https://github.com/your-username/maxine.git
   cd maxine
   ```

3. **Install dependencies**

   ```bash
   poetry install
   ```

4. **Install pre-commit hooks**

   ```bash
   poetry run pre-commit install
   ```

5. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🧪 Development Workflow

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test file
poetry run pytest tests/test_agent.py
```

### Code Quality

```bash
# Format code
poetry run black src/
poetry run ruff format src/

# Lint code
poetry run ruff check src/
poetry run mypy src/
```

### Pre-commit Hooks

Pre-commit hooks are automatically run when you commit. To run them manually:

```bash
# Run hooks manually on all files
poetry run pre-commit run --all-files

# Run hooks on staged files only
poetry run pre-commit run
```

## 📏 Code Standards

### Python Code Style

- **Formatting**: Use `black` for code formatting
- **Linting**: Use `ruff` for linting
- **Type Checking**: Use `mypy` for type checking
- **Line Length**: Maximum 88 characters (black default)
- **Import Sorting**: Use `ruff` for import sorting

### Documentation

- **Docstrings**: Use Google-style docstrings
- **Type Hints**: All functions should have proper type hints
- **Comments**: Write clear, concise comments for complex logic

### Testing

- **Test Coverage**: Aim for >90% test coverage
- **Test Structure**: Use pytest fixtures and parametrization
- **Test Naming**: Use descriptive test function names

## 📝 Commit Message Guidelines

To maintain consistency and clarity in our project history, please follow this commit message template:

### Commit Message Template

To maintain consistency and clarity in our project history, please follow this commit message template:

```text
<type>            (required, one of: feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)
(<scope>)         (optional, single word, lowercase, no spaces or punctuation)
:                 (required, colon and single space)
<short summary>   (required, imperative, <= 50 chars, first word capitalized, no period at end)
\n                (required, single blank line after the header)
<body>            (optional, lines <= 72 chars, explains what and why)
\n                (required, single blank line before footer if footer is present)
<footer>          (optional, for metadata: BREAKING CHANGE: <desc>, Closes #123)
```

### Commit Message Fields

#### Type

Must be one of the following:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to our CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

#### Scope

Optional, single word, lowercase, no spaces or punctuation. Examples:

- `api`
- `agent`
- `tools`
- `server`
- `streaming`

#### Short Summary

- Required, imperative mood (e.g., "Add" not "Added" or "Adds")
- Maximum 50 characters
- First word capitalized
- No period at the end

#### Body

- Optional, but recommended for non-trivial changes
- Lines should be ≤ 72 characters
- Explain what and why, not how
- Separate from summary with a blank line

#### Footer

- Optional
- Used for metadata like breaking changes and issue references
- Format: `BREAKING CHANGE: <description>` or `Closes #123`

### Example Commit Messages

#### Simple feature

```text
feat(api): Add new endpoint for fetching user data
```

#### Bug fix with details

```text
fix(agent): Resolve memory leak in tool caching

The tool cache was not properly releasing references to large objects,
causing memory usage to grow over time. Updated cache implementation
to use weak references for better garbage collection.

Closes #42
```

#### Breaking change

```text
feat(api): Update response format for agent endpoints

BREAKING CHANGE: Agent responses now return structured data instead of plain strings.
Update your client code to handle the new format: {"output": "...", "metadata": {...}}
```

## 🔄 Pull Request Process

### Before Submitting

1. **Ensure all tests pass**: `poetry run pytest`
2. **Check code quality**: `poetry run pre-commit run --all-files`
3. **Update documentation**: If you've changed APIs or behavior
4. **Add tests**: For new features and bug fixes
5. **Update CHANGELOG**: If your change affects users

### Pull Request Template

When submitting a pull request, please include:

- **Description**: What does this PR do?
- **Motivation**: Why is this change needed?
- **Testing**: How was this tested?
- **Breaking Changes**: Are there any breaking changes?
- **Screenshots**: If applicable (for UI changes)

### Review Process

1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one maintainer review required
3. **Testing**: Ensure all tests pass and coverage is maintained
4. **Documentation**: Verify documentation is updated if needed

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Environment**: OS, Python version, Poetry version
- **Steps to Reproduce**: Clear, numbered steps
- **Expected Behavior**: What should happen?
- **Actual Behavior**: What actually happens?
- **Error Messages**: Full error messages and stack traces
- **Additional Context**: Any other relevant information

### Feature Requests

For feature requests, please provide:

- **Use Case**: Why do you need this feature?
- **Proposed Solution**: How should it work?
- **Alternative Solutions**: Other approaches you've considered
- **Additional Context**: Any relevant examples or references

## 🔧 Development Environment

### Environment Variables

Create a `.env` file for local development:

```env
OLLAMA_MODEL=llama3:8b
OLLAMA_BASE_URL=http://localhost:11434
SEARXNG_BASE_URL=http://localhost:8080
LOG_LEVEL=DEBUG
HOST=127.0.0.1
PORT=8000
```

### Docker Development

For consistency, you can use Docker for development:

```bash
# Start dependencies
docker-compose up -d ollama searxng

# Run in development mode
poetry run maxine
```

## 📚 Documentation Guidelines

### Code Documentation

- Use Google-style docstrings for all public functions and classes
- Include type hints for all parameters and return values
- Document complex algorithms and business logic
- Keep comments up-to-date with code changes

### API Documentation

- Update OpenAPI schemas when changing API endpoints
- Include examples in docstrings
- Document error responses and status codes
- Keep README examples current

## 🚀 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

### Release Checklist

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Ensure all tests pass
4. Create release PR
5. Tag release after merge
6. Publish to PyPI (if applicable)

## ❓ Getting Help

- **Documentation**: Check the README and API docs first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Community**: Join our community channels (if available)

## 🙏 Recognition

Contributors will be recognized in our:

- GitHub contributors list
- Release notes (for significant contributions)
- CHANGELOG.md
- README acknowledgments (for major features)

Thank you for contributing to MAXINE! 🚀
