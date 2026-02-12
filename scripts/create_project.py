#!/usr/bin/env python3
"""
Create a new research project.

Usage:
    python3 create_project.py <title> [--type <type>] [--tags <tags>]
"""

import sys
import os
import json
import yaml
from datetime import datetime
from pathlib import Path


def slugify(text):
    """Convert text to slug."""
    return text.lower().replace(' ', '-').replace('_', '-')


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 create_project.py <title> [--type <type>] [--tags <tags>]")
        print("\nTypes: academic, engineering, direction")
        print("Tags: Comma-separated, e.g., '3d-vision,nerf,optimization'")
        sys.exit(1)

    title = sys.argv[1]

    # Parse optional arguments
    project_type = "academic"  # default
    tags = []

    for i, arg in enumerate(sys.argv):
        if arg == "--type" and i + 1 < len(sys.argv):
            project_type = sys.argv[i + 1]
        elif arg == "--tags" and i + 1 < len(sys.argv):
            tags = [t.strip() for t in sys.argv[i + 1].split(",")]

    # Validate type
    valid_types = ["academic", "engineering", "direction"]
    if project_type not in valid_types:
        print(f"Error: Invalid type '{project_type}'. Valid types: {', '.join(valid_types)}")
        sys.exit(1)

    # Get paths
    workspace = Path(__file__).parent.parent.parent.parent.parent
    research_root = workspace / "research-notes"
    projects_dir = research_root / "projects"

    # Create project directory
    project_slug = slugify(title)
    project_dir = projects_dir / project_slug

    if project_dir.exists():
        print(f"Error: Project '{title}' already exists")
        sys.exit(1)

    project_dir.mkdir()

    # Create subdirectories
    (project_dir / "ideas").mkdir()
    (project_dir / "papers").mkdir()
    (project_dir / "engineering").mkdir()

    # Create project.md
    now = datetime.now().isoformat()

    project_content = f"""---
title: {title}
type: {project_type}
created: {now}
updated: {now}
status: active
tags: {json.dumps(tags)}
priority: medium
---

## Project Overview

[Brief description of this project]

## Goals

1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

## Related Papers

- [Paper Title]
- [Paper Title]

## Timeline

- [ ] [Milestone 1]
- [ ] [Milestone 2]
- [ ] [Milestone 3]
"""

    (project_dir / "project.md").write_text(project_content, encoding="utf-8")

    # Update index.md
    index_path = research_root / "index.md"
    index_content = index_path.read_text(encoding="utf-8")

    # Find projects section and add new project
    if "## Projects" in index_content:
        projects_section = "## Projects\n\n"
        new_entry = f"- [{title}](projects/{project_slug}/project.md) - {project_type} - {now}\n"
        index_content = index_content.replace(projects_section, projects_section + new_entry)

    index_path.write_text(index_content, encoding="utf-8")

    print(f"\n✓ Project created successfully!")
    print(f"\nTitle: {title}")
    print(f"Type: {project_type}")
    print(f"Tags: {', '.join(tags) if tags else 'None'}")
    print(f"\nLocation: {project_dir}")
    print("\nNext steps:")
    print(f"1. Edit project.md to add details")
    print(f"2. Add ideas: python3 scripts/create_idea.py '{title}' '<idea title>'")


if __name__ == "__main__":
    main()
