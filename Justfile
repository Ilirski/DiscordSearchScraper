# Justfile for Discord Search API Scraper
# See https://github.com/casey/just

default:
    @just --list

# Install dependencies
install:
    uv sync

# Install dev dependencies
install-dev:
    uv sync --all-extras

# Run the scraper
run *args:
    uv run python scraper.py {{args}}

# Run the JSONL to CSV converter
convert *args:
    uv run python jsonl-to-csv.py {{args}}

# Lint code with ruff
lint:
    uv run ruff check .

# Fix linting issues automatically
lint-fix:
    uv run ruff check --fix .

# Format code with ruff
format:
    uv run ruff format .

# Format and lint in one go
fmt: format lint

# Run tests
test:
    uv run pytest

# Run tests with coverage
test-cov:
    uv run pytest --cov=scraper --cov-report=html --cov-report=term

# Run tests in watch mode
test-watch:
    uv run pytest -f

# Clean generated files
clean:
    rm -rf .venv
    rm -rf .pytest_cache
    rm -rf .ruff_cache
    rm -rf htmlcov
    rm -rf *.egg-info
    rm -rf build
    rm -rf dist
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Build Docker image
docker-build:
    docker build -t discord-scraper .

# Run Docker container
docker-run *args:
    docker run --rm -v $(pwd)/output:/out discord-scraper {{args}}

# Update all dependencies
update:
    uv sync --upgrade

# Lock dependencies
lock:
    uv lock

# Show dependency tree
deptree:
    uv pip show requests

# Check for security vulnerabilities
check-security:
    uv pip check

# Pre-commit: run all checks before committing
pre-commit: lint-fix format test

# Install pre-commit hooks (if using pre-commit framework)
hooks-install:
    uv run pre-commit install

# Run pre-commit hooks manually
hooks-run:
    uv run pre-commit run --all-files

# Development setup (run after cloning)
setup: install-dev hooks-install
    @echo "Development environment ready!"
    @echo "Run 'just run' to start the scraper"

# Release checklist
release-check: lint test
    @echo "Ready for release!"
