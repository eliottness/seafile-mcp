# Contributing to Seafile MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/setugk/seafile-mcp/issues)
2. If not, open a new issue with:
   - A clear, descriptive title
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - Your environment (OS, Python version, Seafile server version)

### Suggesting Features

1. Open an issue with the `enhancement` label
2. Describe the feature and its use case
3. Explain why it would be useful to other users

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear, descriptive messages
6. Push to your fork
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/setugk/seafile-mcp.git
cd seafile-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up your .env file
cp .env.example .env
# Edit .env with your test Seafile server credentials
```

## Code Guidelines

### Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions (see existing code for format)

### Security

- Never log or print API tokens or credentials
- Never commit `.env` files or hardcoded credentials
- Validate all user inputs before using in API calls
- Use parameterized API calls, never string concatenation for URLs with user input

### Tool Design

When adding new MCP tools:

1. Use the `@mcp.tool()` decorator
2. Add a clear docstring explaining what the tool does
3. Document all parameters with type hints and descriptions
4. Handle errors gracefully and return meaningful error messages
5. Follow the existing patterns in `server.py`

Example:

```python
@mcp.tool()
async def your_new_tool(param1: str, param2: int = 10) -> dict:
    """Brief description of what this tool does.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
    """
    # Implementation here
```

## Testing

Before submitting a PR:

1. Test all existing tools still work
2. Test your new functionality
3. Test error cases (invalid inputs, network errors, etc.)
4. Verify no credentials are exposed in logs or errors

## Commit Messages

Use clear, descriptive commit messages:

```
Add library sharing tools

- Add share_library tool for creating share links
- Add list_shares tool for viewing existing shares
- Update README with new tool documentation
```

## Questions?

Open an issue with the `question` label if you have questions about contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
