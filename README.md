# Python MCP Server Starter

A production-ready template for building MCP (Model Context Protocol) servers in Python. This template provides a clean, maintainable architecture with automatic component discovery and optimized performance settings.

## Table of Contents

- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Development](#development)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Key Features

- **Production Ready**: Optimized settings with uvloop and httptools for high performance
- **Auto Component Discovery**: Automatically loads tools, prompts, and resources from modules
- **Type Safety**: Full type hints and mypy configuration
- **Testing Framework**: Unit and E2E tests with pytest
- **Modern Tooling**: PDM for dependency management and packaging
- **Clean Architecture**: Modular structure with core utilities and component separation
- **Development Tools**: Code generators, linting, formatting, and hot-reload support

## Project Structure

```
python-mcp-starter/
├── src/
│   ├── core/              # Core functionality and utilities
│   │   ├── logger.py      # Logging configuration
│   │   └── module_loader.py # Dynamic module loading
│   ├── config/            # Configuration management
│   ├── tools/             # MCP tools implementation
│   │   └── basic_tools.py # Example tools (hello, echo, status)
│   ├── prompts/           # Prompt templates
│   │   └── basic_prompts.py # Example prompts
│   ├── resources/         # External resources
│   │   └── basic_resources.py # Example resources
│   ├── server.py          # MCP server implementation
│   └── main.py            # Main entry point
├── tests/
│   ├── unit/              # Unit tests
│   │   └── test_server.py # Server tests
│   └── e2e/               # End-to-end tests
│       └── test_server_e2e.py # E2E server tests
├── templates/             # Component templates for generators
│   ├── new_tool_template.py
│   ├── new_prompt_template.py
│   ├── new_resource_template.py
│   ├── test_tool_template.py
│   ├── test_prompt_template.py
│   └── test_resource_template.py
├── scripts/               # Utility scripts
│   ├── create_tool.py     # Tool generator
│   ├── create_prompt.py   # Prompt generator
│   ├── create_resource.py # Resource generator
│   ├── verify_project.py  # Project verification
│   └── verify_discovery.py # Component discovery verification
├── Dockerfile            # Production Docker configuration
├── Makefile             # Build and development commands
└── pyproject.toml       # Project configuration and dependencies
```

## Getting Started

### Prerequisites

- Python 3.12+
- PDM (Python Dependency Manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/adrian-d-hidalgo/python-mcp-starter.git
   cd python-mcp-starter
   ```

2. Install dependencies:
   ```bash
   pdm install
   ```

3. Verify installation:
   ```bash
   pdm run python scripts/verify_project.py
   ```

## Usage

### Running the Server

Start the MCP server in development mode:
```bash
pdm run dev
```

Or run directly with Python:
```bash
pdm run start
```

The server supports various options:
```bash
# Custom host and port
python -m src.main --host 127.0.0.1 --port 3000

# Debug mode with verbose logging
python -m src.main --debug

# Production mode with multiple workers
python -m src.main --workers 4

# Development with hot-reload
python -m src.main --reload
```

### Creating Components

The project includes scripts to generate new components:

1. **Create a Tool**:
   ```bash
   python scripts/create_tool.py calculator
   ```
   Creates `src/tools/calculator.py` with template structure.

2. **Create a Prompt**:
   ```bash
   python scripts/create_prompt.py code_review
   ```
   Creates `src/prompts/code_review.py` with template structure.

3. **Create a Resource**:
   ```bash
   python scripts/create_resource.py api_docs
   ```
   Creates `src/resources/api_docs.py` with template structure.

All components are automatically discovered and loaded by the `ModuleLoader` when the server starts.

### Component Structure

Each component module should implement one of these functions:

- `set_tools(mcp: FastMCP)` - Register tools with decorators
- `set_prompts(mcp: FastMCP)` - Register prompts with decorators
- `set_resources(mcp: FastMCP)` - Register resources with decorators

Example tool implementation:
```python
from mcp.server.fastmcp import FastMCP

def set_tools(mcp: FastMCP) -> None:
    @mcp.tool(name="my_tool")
    def my_tool(input_text: str) -> str:
        """Process the input text."""
        return f"Processed: {input_text}"
```

## Development

### Available Commands

- `pdm run start`: Start the MCP server
- `pdm run dev`: Start with hot-reload enabled
- `pdm run test`: Run unit tests
- `pdm run test-e2e`: Run end-to-end tests
- `pdm run lint`: Run ruff linter
- `pdm run format`: Format code with ruff
- `pdm run type-check`: Run mypy type checking
- `pdm run clean`: Clean temporary files

### Architecture

The project follows a modular architecture:

- **Core Layer** (`src/core/`): Shared utilities and infrastructure
  - `logger.py`: Centralized logging configuration
  - `module_loader.py`: Dynamic component discovery and loading

- **Component Layer** (`src/tools/`, `src/prompts/`, `src/resources/`): MCP components
  - Each module implements `set_*` functions for registration
  - Components are automatically discovered by the module loader

- **Server Layer** (`src/server.py`, `src/main.py`): MCP server implementation
  - `MCPServer`: Main server class with optimized settings
  - `main.py`: CLI entry point with argument parsing

### Performance Optimizations

- **uvloop**: Fast event loop implementation
- **httptools**: Optimized HTTP parsing
- **Worker processes**: Automatic CPU-based scaling
- **Module caching**: Cached module imports for faster startup
- **Concurrent loading**: Parallel component registration

## Configuration

### Environment Variables

- `MCP_HOST`: Server host address (default: "0.0.0.0")
- `MCP_PORT`: Server port number (default: 8000)
- `MCP_DEBUG`: Enable debug mode (default: false)
- `MCP_WORKERS`: Number of worker processes (default: 0, auto-detect)
- `MCP_RELOAD`: Enable hot-reload in development (default: false)
- `MCP_LOG_LEVEL`: Logging level (default: "INFO")

### Configuration Files

- `pyproject.toml`: Project metadata and dependencies
- `.env`: Local environment variables (not tracked in git)
- `.env.example`: Example environment variables template

### Development Tools

- **PDM**: Package and dependency management
  - Configure in `pyproject.toml`
  - Use `pdm add` to add dependencies
  - Use `pdm run` to run commands

- **Ruff**: Code linting and formatting
  - Configure in `pyproject.toml` under `[tool.ruff]`
  - Use `pdm run lint` to run linter
  - Use `pdm run format` to format code

- **Mypy**: Type checking
  - Configure in `pyproject.toml` under `[tool.mypy]`
  - Use `pdm run type-check` to run type checker

- **Pytest**: Testing framework
  - Configure in `pyproject.toml` under `[tool.pytest]`
  - Use `pdm run test` to run tests

### Docker Support

Build and run with Docker:
```bash
# Build production image
docker build -t python-mcp-starter \
  --build-arg MCP_HOST=0.0.0.0 \
  --build-arg MCP_PORT=8000 \
  --build-arg MCP_DEBUG=false \
  --build-arg MCP_WORKERS=0 \
  .

# Run container
docker run -p 8000:8000 python-mcp-starter
```

#### Docker Compose Example

```yaml
version: "3.8"

services:
  mcp-server:
    build:
      context: .
      args:
        MCP_HOST: 0.0.0.0
        MCP_PORT: 8000
        MCP_DEBUG: false
        MCP_WORKERS: 0
    ports:
      - "8000:8000"
    environment:
      - MCP_HOST=0.0.0.0
      - MCP_PORT=8000
      - MCP_DEBUG=false
      - MCP_WORKERS=0
```

### Development Container

The project includes a VS Code devcontainer configuration:

- Located in `.devcontainer/`
- Includes all development tools
- Supports hot-reload
- Mounts local directory for live development

To use:

1. Install VS Code and Docker
2. Install "Remote - Containers" extension
3. Open project in VS Code
4. Click "Reopen in Container"

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details
