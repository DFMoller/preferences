# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository serves as a preferences and examples collection for AI assistants working on the user's other projects. It contains code templates, configuration examples, and preferred patterns that should inform how AI assistants approach development tasks in the user's other repositories.

## Structure

The repository is organized by topic, with each folder containing multiple example implementations:

- `templates/devcontainers/` - Development container configurations
  - `ubuntu-python-poetry/` - Ubuntu 24.04 + Python + Poetry devcontainer setup
  - `ubuntu-python-uv/` - Ubuntu 24.04 + Python + uv devcontainer setup
  - `node-caddy/` - Node.js with Caddy web server devcontainer setup

Each folder contains alternative approaches or examples for the same concept. Only one example from each topic would typically be used in any given project.

## Using This Repository in Your Projects

Access these preferences through the MCP (Model Context Protocol) server. This provides system-wide access to all preferences and examples without needing per-project configuration.

### MCP Server Installation

This repository includes a FastMCP server that can be installed to Claude Desktop or Claude Code, or deployed remotely. Once installed, all these preferences become automatically available to Claude through the Model Context Protocol.

**Installation**: See `README.md` for complete installation instructions including:
- Local installation for Claude Desktop using `fastmcp install`
- Remote deployment using Docker and Cloudflare Tunnel
- Connecting Claude Code to local or remote MCP servers

**Benefits**:
- Automatic access to all preferences without per-project setup
- Search and comparison tools for exploring preferences
- Works across all Claude Desktop and Claude Code sessions
- Can be deployed remotely for access from anywhere

## Important Notes

- This repository contains examples and templates, not production code
- When applying these patterns to other projects, adapt the specific versions and configurations as needed
- Read the relevant example files to understand the user's preferred patterns and configurations
