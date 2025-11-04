# Coding Style Guide

This document defines preferred coding styles and conventions for projects.

## General Formatting

### Line Length
- Maximum line length: **120 characters**
- Applies to all languages unless otherwise specified.
- Break long lines at logical points for readability.

### Comments
- All comments should end with a full stop.
- Use complete sentences when possible.
- Example: `# This function processes user input.`

## Python

### Docstrings
- Use **NumPy docstring format** for all functions, classes, and modules.
- The summary line must start on the same line as the opening `"""`.
- Follow the summary with a blank line before the Parameters section.
- Include sections: Parameters, Returns, Raises, Examples as appropriate.

#### NumPy Docstring Example

```python
def calculate_mean(values, weights=None):
    """Calculate the weighted mean of an array of values.

    Parameters
    ----------
    values : array-like
        Input array of numeric values.
    weights : array-like, optional
        Array of weights corresponding to values. If None, uses equal weights.

    Returns
    -------
    float
        The weighted mean of the input values.

    Raises
    ------
    ValueError
        If values and weights have different lengths.

    Examples
    --------
    >>> calculate_mean([1, 2, 3, 4, 5])
    3.0
    >>> calculate_mean([1, 2, 3], weights=[0.2, 0.3, 0.5])
    2.3
    """
    # Implementation here.
    pass
```

### Line Length
- Maximum line length: 120 characters.
- Use implicit line continuation inside parentheses, brackets, and braces.
- Use backslash continuation only when necessary.

### Import Style
- Group imports in the following order:
  1. Standard library imports.
  2. Related third-party imports.
  3. Local application imports.
- Use absolute imports when possible.
- One import per line for clarity.

### Type Hints
- Use type hints for function parameters and return values.
- Import types from `typing` module as needed.
- Example: `def process_data(items: list[str]) -> dict[str, int]:`

## Additional Language Guidelines

### JavaScript/TypeScript
- Line length: 120 characters.
- Use JSDoc comments for documentation.
- All comments end with full stops.

### Go
- Follow standard Go formatting (`gofmt`).
- Line length: 120 characters.
- Comments end with full stops.

### Markdown
- Line length: Soft limit at 120 characters, but can exceed for URLs and code blocks.
- Use consistent heading styles.

## Configuration Files

For consistent enforcement across editors, consider using:

### .editorconfig
```ini
[*]
max_line_length = 120
```

### pyproject.toml (for Python projects)
```toml
[tool.black]
line-length = 120

[tool.ruff]
line-length = 120
```

## Notes

- These are guidelines, not strict rules. Prioritize readability and maintainability.
- When working on existing projects, match the existing style for consistency.
- Use automated formatters when available (e.g., black, prettier) configured to these preferences.
