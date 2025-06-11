# DevContainer Dockerfile - OPTIMIZED for development
# Optimized for junior teams with everything pre-configured

FROM python:3.12-slim

# OPTIMIZED: Development-specific dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    htop \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# OPTIMIZED: Common environment variables
ENV PDM_USE_VENV=false
ENV PDM_PYTHON=/usr/local/bin/python
ENV PYTHONPATH=/workspaces
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install PDM globally
RUN pip install --no-cache-dir pdm

# Create non-root user for secure development
RUN groupadd --gid 1000 devuser \
    && useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home devuser

# OPTIMIZED: Devcontainer-specific configuration
RUN echo 'alias ll="ls -la"' >> ~/.bashrc \
    && echo 'alias pdm-shell="eval \$(pdm venv activate)"' >> ~/.bashrc \
    && echo 'alias python=python3' >> ~/.bashrc \
    && echo 'alias pip=pip3' >> ~/.bashrc

# Set the working directory
WORKDIR /app

# Install all project dependencies
COPY pyproject.toml ./pyproject.toml
COPY pdm.lock ./pdm.lock
RUN touch README.md

# Install dependencies
RUN pdm install --no-lock --no-editable

COPY . .

# Give ownership to devuser
RUN chown -R devuser:devuser /app

# Switch to devuser
USER devuser

# Keep container running for testing
CMD ["sleep", "infinity"]
