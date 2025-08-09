FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UV_SYSTEM_PYTHON=1

# Set work directory
WORKDIR /app

# Install PostgreSQL client for pg_isready
#RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY ../pyproject.toml ../uv.lock /app/
RUN uv sync

# Copy project
COPY ../. /app/

# Expose the port Gunicorn will run on
EXPOSE 8000

# Command to run the application
CMD ["sh", "/app/deployment/entrypoint.sh"]
