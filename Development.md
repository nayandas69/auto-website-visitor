# Local Development Guide

This guide explains how to set up and use the Auto Website Visitor project locally for development and testing.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (recommended: Python 3.10 or 3.11)
- **Git** for version control
- **Web browsers** (Chrome, Firefox, or Edge) for testing
- **Virtual environment** tool (venv, virtualenv, or conda)

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/nayandas69/auto-website-visitor.git
cd auto-website-visitor
```

### 2. Create Virtual Environment

```bash
# Using venv (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install package in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov pytest-mock black flake8 mypy types-PyYAML types-requests
```

### 4. Verify Installation

```bash
# Check if the CLI works
awv --version
awv --help
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=auto_website_visitor --cov-report=html

# Run specific test file
pytest tests/test_config.py

# Run tests with verbose output
pytest -v

# Run tests and stop on first failure
pytest -x
```

### Code Quality Checks

```bash
# Format code with Black
black auto_website_visitor/ tests/

# Lint with flake8
flake8 auto_website_visitor/ tests/

# Type checking with mypy
mypy auto_website_visitor --ignore-missing-imports
```

### Testing the CLI

```bash
# Basic website visit
awv --url https://httpbin.org/html --count 1 --headless

# Test with different browsers
awv --url https://httpbin.org/html --browser firefox --headless --count 1
awv --url https://httpbin.org/html --browser edge --headless --count 1

# Test auto-scroll feature
awv --url https://httpbin.org/html --auto-scroll --headless --count 1

# Test with proxy (if you have one)
awv --url https://httpbin.org/html --proxy 127.0.0.1:8080 --headless --count 1

# Test interactive mode
awv --interactive

# Create and test config file
awv create-config --config-path test-config.yaml
awv --config test-config.yaml --url https://httpbin.org/html --headless
```

### Testing Configuration Files

```bash
# Create sample YAML config
awv create-config --config-path config.yaml

# Edit the config file and test
awv --config config.yaml

# Test JSON config
cat > config.json << EOF
{
  "url": "https://httpbin.org/html",
  "visit_count": 2,
  "browser": "chrome",
  "headless": true,
  "auto_scroll": true,
  "log_level": "DEBUG"
}
EOF

awv --config config.json
```

### Testing Scheduled Execution

```bash
# Test interval scheduling (runs every 30 seconds)
awv --url https://httpbin.org/html --schedule "30s" --headless

# Test cron scheduling (runs every minute)
awv --url https://httpbin.org/html --schedule "*/1 * * * *" --headless

# Stop with Ctrl+C
```

## Environment Variables

Set up environment variables for testing:

```bash
# For proxy authentication
export PROXY_USER="your_username"
export PROXY_PASS="your_password"

# For custom headers
export CUSTOM_HEADERS='{"Authorization": "Bearer token123", "X-Custom": "value"}'
```

## Project Structure

```
auto-website-visitor/
├── auto_website_visitor/          # Main package
│   ├── __init__.py               # Package initialization
│   ├── cli.py                    # Command-line interface
│   ├── config.py                 # Configuration management
│   ├── core.py                   # Core visitor functionality
│   ├── browser.py                # Browser management
│   ├── logger.py                 # Logging utilities
│   ├── scheduler.py              # Scheduling functionality
│   ├── updater.py                # Auto-update mechanism
│   └── templates/                # Configuration templates
├── tests/                        # Test suite
│   ├── test_config.py           # Configuration tests
│   ├── test_logger.py           # Logging tests
│   └── test_scheduler.py        # Scheduler tests
├── .github/workflows/            # GitHub Actions
├── requirements.txt              # Dependencies
├── pyproject.toml               # Project configuration
├── setup.py                     # Setup script
└── README.md                    # Documentation
```

## Adding New Features

### 1. Create Feature Branch

```bash
git checkout -b feature/new-feature-name
```

### 2. Implement Feature

- Add code to appropriate module in `auto_website_visitor/`
- Follow existing code style and patterns
- Add type hints and docstrings

### 3. Add Tests

```bash
# Create test file if needed
touch tests/test_new_feature.py

# Write comprehensive tests
# - Unit tests for individual functions
# - Integration tests for complete workflows
# - Edge cases and error conditions
```

### 4. Update Documentation

- Update docstrings
- Add CLI help text if applicable
- Update README.md if needed

### 5. Test Everything

```bash
# Run full test suite
pytest

# Test CLI functionality
awv --help

# Test with real websites
awv --url https://httpbin.org/html --headless --count 1
```

## Debugging

### Enable Debug Logging

```bash
# CLI with debug logging
awv --url https://httpbin.org/html --log-level DEBUG --headless

# Check log file
tail -f auto_visitor.log
```

### Browser Debugging

```bash
# Run without headless mode to see browser
awv --url https://httpbin.org/html --count 1

# Use different browsers for comparison
awv --url https://httpbin.org/html --browser firefox
awv --url https://httpbin.org/html --browser edge
```

### Python Debugging

```python
# Add breakpoints in code
import pdb; pdb.set_trace()

# Or use your IDE's debugger
```

## Common Issues and Solutions

### WebDriver Issues

```bash
# Update webdriver-manager
pip install --upgrade webdriver-manager

# Clear webdriver cache
rm -rf ~/.wdm/
```

### Permission Issues

```bash
# On Linux/macOS, ensure execute permissions
chmod +x venv/bin/awv

# Check browser installations
google-chrome --version
firefox --version
```

### Import Issues

```bash
# Reinstall in development mode
pip uninstall auto-website-visitor
pip install -e .
```

## Performance Testing

```bash
# Test with multiple visits
awv --url https://httpbin.org/html --count 10 --interval 1 --headless

# Test with auto-scroll
awv --url https://httpbin.org/html --auto-scroll --max-scroll 10 --headless

# Monitor resource usage
top -p $(pgrep -f awv)
```

## Building and Distribution

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Install from local build
pip install dist/auto_website_visitor-*.whl
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Ensure all tests pass
6. Submit a pull request

## Getting Help

- Check the main README.md for usage examples
- Run `awv --help` for CLI options
- Check the test files for usage patterns
- Open an issue on GitHub for bugs or feature requests

## Useful Commands Summary

```bash
# Development setup
python -m venv venv && source venv/bin/activate
pip install -e .

# Testing
pytest --cov=auto_website_visitor
black auto_website_visitor/ tests/
flake8 auto_website_visitor/ tests/

# Quick functionality test
awv --url https://httpbin.org/html --headless --count 1

# Interactive testing
awv --interactive

# Config file testing
awv create-config && awv --config config.yaml
```