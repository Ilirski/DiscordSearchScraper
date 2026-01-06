# Use uv for fast dependency installation
FROM python:3.13-slim-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies using uv (faster than pip)
RUN uv sync --frozen --no-dev

# Create non-root user
RUN useradd -m -u 1000 dss

# Copy application code
COPY scraper.py ./

# Create output directory
RUN mkdir -p /out && chown -R dss:dss /out /app

USER dss
WORKDIR /out

# Run the application using uv run
ENTRYPOINT ["uv", "run", "--no-dev", "python", "/app/scraper.py"]

