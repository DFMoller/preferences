# Dockerfile for Preferences MCP Server
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml .
COPY uv.lock .
COPY mcp_server/ mcp_server/
COPY templates/ templates/
COPY CLAUDE.md CLAUDE.md
COPY README.md README.md
COPY STYLE.md STYLE.md

# Install dependencies
RUN uv sync --frozen

# Expose port for HTTP transport
EXPOSE 8000

# Set environment variable for repo path
ENV REPO_PATH=/app

# Run the MCP server with HTTP transport
CMD ["uv", "run", "python", "-m", "mcp_server.server", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
