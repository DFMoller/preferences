"""Preferences MCP Server

A FastMCP server that exposes development preferences, examples,
and configuration templates to AI assistants via the Model Context Protocol.

This server provides:
- Resources: Read-only access to preference files and configurations
- Tools: Functions to search, compare, and analyze preferences

Usage:
    # Local (stdio) - for Claude Desktop
    python -m mcp_server.server

    # Remote (HTTP) - for network access
    python -m mcp_server.server --transport http --port 8000

    # Install to Claude Desktop
    fastmcp install claude-desktop mcp_server/server.py --project .
"""

import argparse
from pathlib import Path

from fastmcp import FastMCP

from .utils import get_repo_root
from .resources import register_resources
from .tools import register_tools


# Get repository root
REPO_ROOT = get_repo_root()

# Create FastMCP server
mcp = FastMCP(
    name="preferences-server"
)

# Register resources (read-only data)
register_resources(mcp, REPO_ROOT)

# Register tools (executable functions)
register_tools(mcp, REPO_ROOT)


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(
        description="Preferences MCP Server - Serve development preferences to AI assistants"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport type (default: stdio for local use)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP transport (default: 8000)"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host for HTTP transport (default: localhost)"
    )

    args = parser.parse_args()

    if args.transport == "stdio":
        # Local transport for Claude Desktop
        print(f"Starting MCP server with stdio transport", flush=True)
        print(f"Repository: {REPO_ROOT}", flush=True)
        mcp.run()
    else:
        # HTTP transport for remote access
        print(f"Starting MCP server with HTTP transport on {args.host}:{args.port}", flush=True)
        print(f"Repository: {REPO_ROOT}", flush=True)
        mcp.run(transport="http", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
