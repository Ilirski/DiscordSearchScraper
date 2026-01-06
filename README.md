# Discord Search API Scraper

A Discord search scraper that uses the Discord API to search for and extract messages from guilds.

## Features

- Search Discord messages across guilds
- Filter messages by date ranges
- Export results to JSONL/CSV format
- Docker support for containerized deployment
- Comprehensive test suite (66% coverage)
- Pre-commit hooks for code quality
- Fast development tooling with Justfile

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

### Using uv

```bash
# Install dependencies
uv sync

# Install dev dependencies
uv sync --all-extras
```

## Usage

### Running the Scraper

```bash
# Run with uv
uv run python scraper.py

# Or activate the virtual environment first
source .venv/bin/activate  # On Linux/macOS
python scraper.py
```

### Docker

```bash
# Build the image
docker build -t discord-scraper .

# Run the container
docker run --rm -v $(pwd)/output:/out discord-scraper
```

## Development

### Available Commands

The project includes a `Justfile` for convenient command execution:

```bash
just install-dev       # Install all dependencies
just run               # Run the scraper
just lint              # Lint code
just format            # Format code
just test              # Run tests
just test-cov          # Run tests with coverage
just clean             # Clean generated files
just docker-build      # Build Docker image
just pre-commit        # Run all pre-commit checks
just setup             # Full development setup

# Or use uv directly
uv run python scraper.py
uv run ruff check .
uv run pytest
```

Run `just` (with no arguments) to see all available commands.

### Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Fix linting issues automatically
uv run ruff check --fix .
```

### Pre-commit Hooks

Pre-commit hooks are configured to automatically run linting and formatting before commits:

```bash
# Install pre-commit hooks (one-time setup)
just hooks-install
# or: uv run pre-commit install

# Run hooks manually
just hooks-run
# or: uv run pre-commit run --all-files
```

The pre-commit hooks will:
- Check and fix code style with Ruff
- Detect merge conflicts
- Check for trailing whitespace
- Validate JSON, YAML, and TOML syntax
- Detect accidentally committed private keys

### Testing

The project has a comprehensive test suite with 66% code coverage:

```bash
# Run tests
just test
# or: uv run pytest

# Run tests with coverage report
just test-cov
# or: uv run pytest --cov=scraper --cov-report=html

# Run tests in watch mode
just test-watch
```

Tests cover:
- Discord snowflake conversion utilities
- DiscordSearcher class initialization and configuration
- Query formation with various parameters
- File output handling
- Message appending

## Project Structure

```
discord-search-api-scraper/
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_discord_searcher.py
│   └── test_snowflake_utils.py
├── scraper.py                 # Main scraper script
├── jsonl-to-csv.py            # Utility for converting JSONL to CSV
├── pyproject.toml             # Project configuration
├── uv.lock                    # Dependency lock file
├── Justfile                   # Just commands
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── .dockerignore              # Docker build exclusions
└── Dockerfile                 # Container configuration
```
