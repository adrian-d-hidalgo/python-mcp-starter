# Stage 1: Builder
FROM python:3.12-slim AS builder

# Essential build dependencies only
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# PDM environment variables
ENV PDM_USE_VENV=false
ENV PDM_PYTHON=/usr/local/bin/python
ENV PYTHONPATH=/app:/app/__pypackages__/3.12/lib
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install PDM
RUN pip install --no-cache-dir pdm

WORKDIR /app

# Copy configuration files
COPY pyproject.toml pdm.lock* ./
RUN touch README.md

# Install production dependencies
RUN pdm install --prod --frozen-lockfile --no-editable --no-self

# Stage 2: Runtime
FROM python:3.12-slim

# Environment variables
ENV PYTHONPATH=/app:/app/__pypackages__/3.12/lib
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app:${PATH}"

# Create non-root user
RUN groupadd --gid 1000 mcpuser \
    && useradd --uid 1000 --gid mcpuser --shell /bin/bash --create-home mcpuser

# Minimal runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy everything from builder
COPY --from=builder /app /app

# Copy source code
COPY --chown=mcpuser:mcpuser . /app/

# Switch to non-root user
USER mcpuser

# Application environment variables
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000
ENV MCP_DEBUG=false
ENV MCP_SERVER_NAME="mcp-server"
ENV MCP_SERVER_INSTRUCTIONS="MCP Server Template with modular tools, prompts, and resources"
ENV MCP_JSON_RESPONSE=false
ENV MCP_STATELESS_HTTP=false

CMD ["python", "-m", "src.main"]
