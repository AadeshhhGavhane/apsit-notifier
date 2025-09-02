# Use uv image with Python 3.12 (Debian slim)
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Optional optimizations
ENV UV_LINK_MODE=copy \
    UV_PYTHON=3.12 \
    UV_COMPILE_BYTECODE=1

# Layers for better caching
COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-cache

# Project files
COPY . .

# Run
CMD ["uv", "run", "main.py"]