FROM python:3.12-slim

WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project files
COPY pyproject.toml README.md uv.lock ./
COPY src/ ./src/

# Sync dependencies
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# Run as non-root user
RUN addgroup --system pocketrelay && adduser --system --ingroup pocketrelay pocketrelay
RUN chown -R pocketrelay:pocketrelay /app
USER pocketrelay

ENTRYPOINT ["pocketrelay"]
CMD ["run"]
