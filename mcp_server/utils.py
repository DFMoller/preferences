"""Utility functions for the preferences MCP server."""

from pathlib import Path
from typing import Optional


def get_repo_root() -> Path:
    """Get the repository root directory.

    Returns the path from the REPO_PATH environment variable if set,
    otherwise assumes the parent directory of the mcp package.
    """
    import os

    repo_path = os.getenv("REPO_PATH")
    if repo_path:
        return Path(repo_path).resolve()

    # Default: parent directory of mcp package
    return Path(__file__).parent.parent.resolve()


def ensure_path_in_repo(file_path: Path, repo_root: Path) -> Path:
    """Ensure a file path is within the repository.

    Args:
        file_path: The file path to check
        repo_root: The repository root directory

    Returns:
        The resolved file path

    Raises:
        ValueError: If the path is outside the repository
    """
    resolved_path = file_path.resolve()
    try:
        resolved_path.relative_to(repo_root.resolve())
        return resolved_path
    except ValueError:
        raise ValueError(f"Access denied: path '{file_path}' is outside repository")


def list_directory_files(directory: Path, pattern: str = "*") -> list[str]:
    """List all files in a directory matching a pattern.

    Args:
        directory: Directory to search
        pattern: Glob pattern to match (default: all files)

    Returns:
        List of relative file paths
    """
    if not directory.exists() or not directory.is_dir():
        return []

    files = []
    for file_path in directory.rglob(pattern):
        if file_path.is_file():
            files.append(str(file_path.relative_to(directory)))

    return sorted(files)


def read_file_safe(file_path: Path, repo_root: Path) -> str:
    """Safely read a file within the repository.

    Args:
        file_path: Path to the file to read
        repo_root: Repository root directory

    Returns:
        File contents as string

    Raises:
        ValueError: If path is outside repository
        FileNotFoundError: If file doesn't exist
    """
    # Security check
    resolved_path = ensure_path_in_repo(file_path, repo_root)

    if not resolved_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not resolved_path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    return resolved_path.read_text()


def search_in_file(file_path: Path, query: str, case_sensitive: bool = False) -> bool:
    """Check if a query string appears in a file.

    Args:
        file_path: Path to the file
        query: Search query
        case_sensitive: Whether to perform case-sensitive search

    Returns:
        True if query is found, False otherwise
    """
    try:
        content = file_path.read_text()
        if case_sensitive:
            return query in content
        else:
            return query.lower() in content.lower()
    except Exception:
        return False
