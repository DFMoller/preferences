"""Prompt definitions for the preferences MCP server.

Prompts provide automatic context injection to guide AI assistants
in following preferred coding styles and patterns. Be carefult not
to flood prompts with too much information.
"""

from pathlib import Path
from fastmcp import FastMCP

from .utils import read_file_safe


def register_prompts(mcp: FastMCP, repo_root: Path):
    """Register all prompts with the MCP server.

    These prompts are automatically available to AI assistants and provide
    context about coding preferences, style guidelines, and best practices.

    Args:
        mcp: FastMCP server instance.
        repo_root: Path to the repository root.
    """

    @mcp.prompt(
        description="Provides coding style guidelines that should be followed for all code",
        tags={"style", "guidelines", "formatting"}
    )
    def coding_style_guidelines() -> str:
        """Coding style guidelines for this user's projects.

        This prompt provides comprehensive style guidelines including:
        - Line length limits (120 characters).
        - Comment formatting requirements.
        - Language-specific conventions (Python, JavaScript, Go, etc.).
        - Docstring format preferences (NumPy style for Python).

        These guidelines should be automatically applied to all code written
        without needing explicit user reminders.
        """
        style_path = repo_root / "STYLE.md"
        try:
            style_content = read_file_safe(style_path, repo_root)
            return f"""You must follow these coding style guidelines for all code you write:

{style_content}

IMPORTANT: Apply these guidelines automatically to all code without being prompted."""
        except FileNotFoundError:
            return "Style guidelines not found. Use sensible defaults: 120 char lines, complete sentences in comments."

    @mcp.prompt(
        description="Information about available devcontainer templates and configuration preferences",
        tags={"devcontainer", "docker", "development"}
    )
    def devcontainer_preferences() -> str:
        """Available devcontainer templates and configuration patterns.

        Provides information about the user's preferred devcontainer setups.

        Use this when setting up development environments or when asked about
        container configurations.
        """
        devcontainer_dir = repo_root / "templates" / "devcontainers"
        available = []

        if devcontainer_dir.exists():
            for dc_dir in devcontainer_dir.iterdir():
                if dc_dir.is_dir() and not dc_dir.name.startswith("."):
                    available.append(dc_dir.name)

        if not available:
            return "No devcontainer templates found."

        template_list = "\n".join(f"- {name}" for name in sorted(available))

        return f"""Available devcontainer templates:

{template_list}

These templates represent the user's preferred development environment configurations.
When setting up a new project or configuring a devcontainer, consider using one of these
as a starting point.

To access a specific template's configuration files, use the MCP tools:
- list_devcontainer_files(name) to see all files in a template.
- Use resources like preferences://devcontainer/{{name}}/config for specific files.
"""

    @mcp.prompt(
        description="General project guidance and how to use this preferences repository",
        tags={"guide", "documentation", "preferences"}
    )
    def repository_guide() -> str:
        """Guidance on using the preferences repository.

        Explains the purpose of this preferences repository and how to apply
        these patterns to other projects.
        """
        claude_md_path = repo_root / "CLAUDE.md"
        try:
            claude_content = read_file_safe(claude_md_path, repo_root)
            return f"""Repository Usage Guide:

{claude_content}

This repository serves as a reference for preferred patterns and configurations.
When working on other projects, consult these preferences to understand the user's
preferred approaches to common development tasks."""
        except FileNotFoundError:
            return "Repository guide not found."
