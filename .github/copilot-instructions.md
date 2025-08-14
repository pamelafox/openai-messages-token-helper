# OpenAI Messages Token Helper

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

OpenAI Messages Token Helper is a Python library for estimating tokens used by messages and building messages lists that fit within the token limits of OpenAI GPT models. It uses the tiktoken library for tokenizing text and the Pillow library for image-related calculations.

## Working Effectively

### Environment Setup and Dependencies

Bootstrap, build, and test the repository:

```bash
# CRITICAL: Install dependencies - May fail due to network connectivity issues
python3 -m pip install -e '.[dev]'
pre-commit install
```

**KNOWN ISSUE**: `python3 -m pip install` frequently fails due to PyPI connectivity timeouts. If you encounter ReadTimeoutError or connection timeouts:
- Try increasing pip timeout: `pip3 install --timeout 600 -e '.[dev]'`
- Some system packages may be available: `sudo apt install python3-pil` for Pillow

### Testing and Validation

```bash
# Run tests - NEVER CANCEL: Test suite takes approximately 1-2 minutes. Set timeout to 5+ minutes.
python3 -m pytest

# Run with coverage (as used in CI)
python3 -m pytest -s -vv --cov --cov-fail-under=97
```

### Code Quality Checks

```bash
# NEVER CANCEL: Each command takes 10-30 seconds. Set timeout to 2+ minutes for safety.

# Lint with ruff (required for CI)
ruff check .

# Check formatting with black (required for CI)
black . --check --verbose

# Run type checks with mypy (required for CI)
python3 -m mypy .
```

### Pre-commit Hooks

```bash
# Install and run pre-commit hooks
pre-commit install
pre-commit run --all-files
```

## Validation Requirements

**CRITICAL**: Always test at least one complete functional scenario after making changes:

### CI Compliance Validation
Always run all CI checks before completing work:

```bash
# All checks that must pass for CI - NEVER CANCEL: Total time ~2-3 minutes
ruff check .
black . --check --verbose  
python3 -m mypy .
python3 -m pytest -s -vv --cov --cov-fail-under=97
```

## Project Structure and Key Files

### Repository Root
```
.github/                 # GitHub Actions workflows and configuration
├── workflows/
│   └── python.yaml     # CI workflow (linting, testing, type checking)
src/openai_messages_token_helper/  # Main source code
├── __init__.py         # Package exports
├── function_format.py  # Function formatting utilities  
├── images_helper.py    # Image token calculation
├── message_builder.py  # Core message building logic
└── model_helper.py     # Model-specific token limits and counting
tests/                  # Test suite
├── test_*.py          # Unit tests
├── verify_*.py        # Integration tests (require OpenAI API access)
├── messages.py        # Test message fixtures
├── functions.py       # Test function fixtures
└── image_messages.py  # Test image message fixtures
pyproject.toml         # Project configuration and dependencies
.pre-commit-config.yaml # Pre-commit hook configuration
```

### Core Library Functions
The package exports these main functions:
- `build_messages()` - Build message lists within token limits
- `count_tokens_for_message()` - Count tokens for a single message
- `count_tokens_for_image()` - Count tokens for image content
- `get_token_limit()` - Get token limits for models
- `count_tokens_for_system_and_tools()` - Count tokens for system messages and tools

### Development Workflow Commands Summary
```bash
# Install dependencies (may fail due to network issues)
python3 -m pip install -e '.[dev]'

# Code quality (run all before committing)
ruff check .
black . --check --verbose
python3 -m mypy .

# Testing (NEVER CANCEL - set 5+ minute timeout)
python3 -m pytest -s -vv --cov --cov-fail-under=97
```

## Common Issues and Workarounds

### Network Connectivity Issues
- **Problem**: PyPI timeouts during `pip install`
- **Workaround**: Use system packages where available
- **Command**: `sudo apt install python3-pil` for Pillow dependency

### Dependency Import Errors
- **Problem**: Missing `openai`, `tiktoken`, or `pillow` packages
- **Solution**: Ensure dependencies are installed; if not possible due to network issues, continue with available tools
- **Validation**: Basic imports will fail but code structure analysis can continue

### CI/GitHub Actions Timing
- **Install dependencies**: ~30-60 seconds (when successful)
- **Linting (ruff)**: ~10-15 seconds
- **Formatting (black)**: ~5-10 seconds  
- **Type checking (mypy)**: ~10-20 seconds
- **Testing (pytest)**: ~30-45 seconds
- **Total CI time**: ~1.5-2.5 minutes per Python version (tests 3.9, 3.10, 3.11, 3.12)

## CRITICAL Reminders

- **NEVER CANCEL** commands that appear to hang - testing and dependency installation can take several minutes
- **ALWAYS** set appropriate timeouts: 5+ minutes for tests, 2+ minutes for linting
- **ALWAYS** validate functionality after changes using pytest tests
- **ALWAYS** run all CI checks before submitting: ruff, black, mypy, pytest
- **EXPECT** potential PyPI connectivity issues and plan accordingly