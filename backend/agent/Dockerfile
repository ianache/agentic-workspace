FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY .env.example .env

# Install dependencies
RUN uv sync --frozen

# Copy source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "main.py"]
