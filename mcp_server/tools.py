"""Tool definitions for the preferences MCP server.

Tools provide executable functions that can search, analyze, and compare preferences.
"""

from pathlib import Path
from fastmcp import FastMCP

from .utils import search_in_file, list_directory_files


def register_tools(mcp: FastMCP, repo_root: Path):
    """Register all tools with the MCP server.

    Args:
        mcp: FastMCP server instance
        repo_root: Path to the repository root
    """

    @mcp.tool()
    def search_preferences(query: str, category: str = "all") -> list[dict]:
        """Searches for preferences matching a query.

        Searches through preference files and returns matches with context.

        Args:
            query: Search term to look for
            category: Filter by category - "all", "devcontainer", or "guide"

        Returns:
            List of dictionaries containing match information:
            - type: Category type (devcontainer or guide)
            - name: Name of the item
            - file: Filename (for devcontainers)
            - path: Relative path to the file
        """
        results = []
        query_lower = query.lower()

        # Search devcontainers
        if category in ["all", "devcontainer"]:
            devcontainer_dir = repo_root / "templates" / "devcontainers"
            if devcontainer_dir.exists():
                for dc_dir in devcontainer_dir.iterdir():
                    if dc_dir.is_dir() and not dc_dir.name.startswith("."):
                        for file_path in dc_dir.rglob("*"):
                            if file_path.is_file():
                                if search_in_file(file_path, query):
                                    results.append({
                                        "type": "devcontainer",
                                        "name": dc_dir.name,
                                        "file": file_path.name,
                                        "path": str(file_path.relative_to(repo_root))
                                    })

        # Search guides
        if category in ["all", "guide"]:
            for guide in ["CLAUDE.md", "README.md"]:
                guide_path = repo_root / guide
                if guide_path.exists():
                    if search_in_file(guide_path, query):
                        results.append({
                            "type": "guide",
                            "name": guide,
                            "path": guide
                        })

        return results

    @mcp.tool()
    def list_devcontainer_files(name: str) -> list[str]:
        """Lists all files in a specific devcontainer configuration.

        Args:
            name: Name of the devcontainer

        Returns:
            List of relative file paths within the devcontainer
        """
        dc_path = repo_root / "templates" / "devcontainers" / name

        if not dc_path.exists() or not dc_path.is_dir():
            return []

        return list_directory_files(dc_path)

    @mcp.tool()
    def compare_devcontainers(name1: str, name2: str) -> dict:
        """Compares two devcontainer configurations.

        Analyzes the files present in each devcontainer and identifies
        common files and unique files in each.

        Args:
            name1: First devcontainer name
            name2: Second devcontainer name

        Returns:
            Dictionary containing:
            - name1, name2: Names of the devcontainers
            - files1, files2: Lists of files in each
            - common_files: Files present in both
            - unique_to_1: Files only in the first
            - unique_to_2: Files only in the second
        """
        dc1_path = repo_root / "templates" / "devcontainers" / name1
        dc2_path = repo_root / "templates" / "devcontainers" / name2

        comparison = {
            "name1": name1,
            "name2": name2,
            "files1": [],
            "files2": [],
            "common_files": [],
            "unique_to_1": [],
            "unique_to_2": []
        }

        # Get file lists
        if dc1_path.exists() and dc1_path.is_dir():
            comparison["files1"] = [
                f.name for f in dc1_path.iterdir() if f.is_file()
            ]

        if dc2_path.exists() and dc2_path.is_dir():
            comparison["files2"] = [
                f.name for f in dc2_path.iterdir() if f.is_file()
            ]

        # Compare
        set1 = set(comparison["files1"])
        set2 = set(comparison["files2"])

        comparison["common_files"] = sorted(list(set1 & set2))
        comparison["unique_to_1"] = sorted(list(set1 - set2))
        comparison["unique_to_2"] = sorted(list(set2 - set1))

        return comparison

    @mcp.tool()
    def list_all_preferences() -> dict:
        """Lists all available preferences organized by category.

        Returns:
            Dictionary with categories and their items:
            - devcontainers: List of devcontainer configurations
            - Each devcontainer includes name and file list
        """
        result = {
            "devcontainers": []
        }

        devcontainer_dir = repo_root / ".devcontainer"
        if devcontainer_dir.exists():
            for dc_dir in devcontainer_dir.iterdir():
                if dc_dir.is_dir() and not dc_dir.name.startswith("."):
                    files = [f.name for f in dc_dir.iterdir() if f.is_file()]
                    result["devcontainers"].append({
                        "name": dc_dir.name,
                        "files": sorted(files)
                    })

        # Sort by name
        result["devcontainers"].sort(key=lambda x: x["name"])

        return result
