FROM python:3.11-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install the application dependencies.
COPY uv.lock pyproject.toml README.md ./
RUN uv sync --frozen --no-cache

# Copy application code
COPY . .


# Run FastAPI backend
CMD ["uv", "run", "uvicorn", "src.infrastructure.api:app", "--host", "0.0.0.0", "--port", "8000"]
