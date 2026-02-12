#!/usr/bin/env python3
"""
Shared utilities for research notes.
"""

import re
import os
from pathlib import Path
from typing import Optional, Dict, Any


def get_research_root() -> Path:
    """
    Get research notes root directory.

    Priority:
    1. RESEARCH_NOTES_ROOT environment variable
    2. Search upward for config.yaml
    3. Default to ~/research-notes

    Returns:
        Path to research notes root directory

    Raises:
        RuntimeError: If root cannot be determined and doesn't exist
    """
    # Try environment variable first
    env_root = os.getenv('RESEARCH_NOTES_ROOT')
    if env_root:
        root = Path(env_root)
        if root.exists():
            return root

    # Try to find config.yaml by searching upward
    current = Path.cwd()
    for _ in range(10):  # Limit search depth
        config_file = current / 'config.yaml'
        if config_file.exists():
            # Verify it's a research notes config
            with open(config_file) as f:
                content = f.read()
                if 'notion' in content or 'database' in content:
                    return current

        if current == current.parent:
            break
        current = current.parent

    # Default to home directory
    default_root = Path.home() / 'research-notes'
    if not default_root.exists():
        raise RuntimeError(
            "Research notes root not found. "
            "Set RESEARCH_NOTES_ROOT environment variable or run init.py first."
        )

    return default_root


def slugify(text: str, max_length: int = 100) -> str:
    """
    Convert text to filesystem-safe slug.

    This improved version:
    - Removes all dangerous characters
    - Prevents path traversal
    - Collapses multiple spaces/dashes
    - Limits length
    - Handles Unicode properly

    Args:
        text: Input text to slugify
        max_length: Maximum length of output (default: 100)

    Returns:
        Safe filesystem slug

    Examples:
        >>> slugify('Hello World')
        'hello-world'
        >>> slugify('Test/Project: V1.0')
        'test-project-v10'
        >>> slugify('../../../etc/passwd')
        'etc-passwd'
    """
    if not text:
        return 'untitled'

    # Convert to lowercase
    text = text.lower()

    # Remove any non-word characters (except spaces and dashes)
    text = re.sub(r'[^\w\s-]', '', text)

    # Replace whitespace with dashes
    text = re.sub(r'[-\s]+', '-', text)

    # Remove leading/trailing dashes
    text = text.strip('-')

    # Ensure no path traversal
    text = text.replace('..', '')
    text = text.replace('/', '')
    text = text.replace('\\', '')

    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
        # Try to break at a dash
        if '-' in text:
            text = text.rsplit('-', 1)[0]

    # Ensure result is not empty
    return text if text else 'untitled'


def parse_frontmatter(content: str) -> Dict[str, Any]:
    """
    Extract YAML front matter from markdown content.

    This properly parses YAML instead of manual line parsing.

    Args:
        content: Markdown content with YAML front matter

    Returns:
        Dictionary of front matter fields, empty dict if no front matter

    Examples:
        >>> content = '''---
        ... title: Test
        ... tags: [a, b, c]
        ... ---
        ... # Content'''
        >>> meta = parse_frontmatter(content)
        >>> meta['title']
        'Test'
        >>> meta['tags']
        ['a', 'b', 'c']
    """
    if not content or not content.startswith('---'):
        return {}

    # Split on triple dashes
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    try:
        import yaml
        metadata = yaml.safe_load(parts[1]) or {}
        return metadata if isinstance(metadata, dict) else {}
    except Exception as e:
        # If yaml import fails, return empty dict
        return {}


def find_project_by_title(projects_dir: Path, title: str) -> Optional[Path]:
    """
    Find project directory by title (case-insensitive).

    Args:
        projects_dir: Path to projects directory
        title: Project title to search for

    Returns:
        Path to project directory, or None if not found
    """
    if not projects_dir.exists():
        return None

    title_lower = title.lower().strip()

    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue

        project_md = project_dir / "project.md"
        if not project_md.exists():
            continue

        try:
            content = project_md.read_text(encoding='utf-8')
            metadata = parse_frontmatter(content)

            project_title = metadata.get('title', '')
            if project_title.lower().strip() == title_lower:
                return project_dir
        except Exception as e:
            print(f"Warning: Failed to read {project_md}: {e}")
            continue

    return None


def find_idea_by_title(project_dir: Path, title: str) -> Optional[Path]:
    """
    Find idea directory by title (case-insensitive).

    Args:
        project_dir: Path to project directory
        title: Idea title to search for

    Returns:
        Path to idea directory, or None if not found
    """
    ideas_dir = project_dir / "ideas"
    if not ideas_dir.exists():
        return None

    title_lower = title.lower().strip()

    for idea_dir in ideas_dir.iterdir():
        if not idea_dir.is_dir():
            continue

        idea_md = idea_dir / "idea.md"
        if not idea_md.exists():
            continue

        try:
            content = idea_md.read_text(encoding='utf-8')
            metadata = parse_frontmatter(content)

            idea_title = metadata.get('title', '')
            if idea_title.lower().strip() == title_lower:
                return idea_dir
        except Exception as e:
            print(f"Warning: Failed to read {idea_md}: {e}")
            continue

    return None


def validate_title(title: str, max_length: int = 200) -> tuple[bool, str]:
    """
    Validate a title for use in research notes.

    Args:
        title: Title to validate
        max_length: Maximum allowed length

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Title cannot be empty"

    if len(title) > max_length:
        return False, f"Title too long (max {max_length} characters)"

    # Check for path traversal attempts
    if '..' in title or '/' in title or '\\' in title:
        return False, "Title cannot contain path separators or '..'"

    # Check if slugified version would be valid
    slug = slugify(title)
    if not slug or slug == 'untitled':
        return False, "Title must contain at least some alphanumeric characters"

    return True, ""


def format_error_with_suggestions(error_msg: str, suggestions: list) -> str:
    """
    Format an error message with helpful suggestions.

    Args:
        error_msg: The error message
        suggestions: List of suggestion strings

    Returns:
        Formatted error message
    """
    output = [f"\n❌ Error: {error_msg}\n"]

    if suggestions:
        output.append("💡 Suggestions:")
        for suggestion in suggestions:
            output.append(f"   • {suggestion}")

    return '\n'.join(output)
