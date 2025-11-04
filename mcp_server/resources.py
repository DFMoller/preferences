"""Resource definitions for the preferences MCP server.

Resources provide read-only access to preference files and configurations.
"""

from pathlib import Path
from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError

from .utils import get_repo_root, read_file_safe, list_directory_files


def register_resources(mcp: FastMCP, repo_root: Path):
    """Register all resources with the MCP server.

    Args:
        mcp: FastMCP server instance
        repo_root: Path to the repository root
    """

    @mcp.resource("preferences://catalog")
    def list_preferences() -> dict:
        """Lists all available preference categories and examples.

        Returns a dictionary with:
        - devcontainers: List of available devcontainer configurations
        - guides: List of available documentation files
        - repository: Path to the repository root
        """
        devcontainer_dir = repo_root / "templates" / "devcontainers"
        devcontainers = []

        if devcontainer_dir.exists():
            devcontainers = [
                d.name for d in devcontainer_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ]

        return {
            "devcontainers": sorted(devcontainers),
            "guides": ["CLAUDE.md", "README.md", "STYLE.md"],
            "repository": str(repo_root)
        }

    @mcp.resource("preferences://devcontainer/{name}/{file}")
    def get_devcontainer_file(name: str, file: str) -> str:
        """Retrieves a specific file from a devcontainer configuration.

        Args:
            name: Name of the devcontainer (e.g., "ubuntu-python-uv")
            file: File type to retrieve (config, dockerfile, compose, caddyfile)

        Returns:
            File contents as string

        Raises:
            ResourceError: If the file type is invalid or file not found
        """
        valid_files = {
            "config": "devcontainer.json",
            "dockerfile": "Dockerfile",
            "compose": "docker-compose.yml",
            "caddyfile": "Caddyfile"
        }

        if file not in valid_files:
            raise ResourceError(
                f"Invalid file type '{file}'. "
                f"Valid types: {', '.join(valid_files.keys())}"
            )

        file_path = repo_root / "templates" / "devcontainers" / name / valid_files[file]

        try:
            return read_file_safe(file_path, repo_root)
        except FileNotFoundError:
            raise ResourceError(
                f"File '{valid_files[file]}' not found in devcontainer '{name}'"
            )

    @mcp.resource("preferences://guide/{name}")
    def get_guide(name: str) -> str:
        """Retrieves guide documentation.

        Args:
            name: Guide name (claude, readme, style)

        Returns:
            Guide contents as string

        Raises:
            ResourceError: If the guide doesn't exist
        """
        valid_guides = {
            "claude": "CLAUDE.md",
            "readme": "README.md",
            "style": "STYLE.md"
        }

        if name not in valid_guides:
            raise ResourceError(
                f"Invalid guide '{name}'. "
                f"Valid guides: {', '.join(valid_guides.keys())}"
            )

        guide_path = repo_root / valid_guides[name]

        try:
            return read_file_safe(guide_path, repo_root)
        except FileNotFoundError:
            raise ResourceError(f"Guide '{name}' not found")

    @mcp.resource("preferences://devcontainer/{name}/list")
    def list_devcontainer_files(name: str) -> dict:
        """Lists all files in a devcontainer configuration.

        Args:
            name: Name of the devcontainer

        Returns:
            Dictionary with list of files

        Raises:
            ResourceError: If devcontainer doesn't exist
        """
        dc_path = repo_root / "templates" / "devcontainers" / name

        if not dc_path.exists():
            raise ResourceError(f"Devcontainer '{name}' not found")

        files = list_directory_files(dc_path)

        return {
            "devcontainer": name,
            "files": files,
            "count": len(files)
        }

    @mcp.resource("preferences://files/{filepath*}")
    def get_file_content(filepath: str) -> str:
        """Retrieves content from any file in the preferences repository.

        This is a wildcard resource that allows access to any file within
        the repository. Path traversal is prevented by security checks.

        Args:
            filepath: Relative path to the file

        Returns:
            File contents as string

        Raises:
            ResourceError: If file not found or access denied
        """
        file_path = repo_root / filepath

        try:
            return read_file_safe(file_path, repo_root)
        except ValueError as e:
            raise ResourceError(str(e))
        except FileNotFoundError:
            raise ResourceError(f"File '{filepath}' not found")
