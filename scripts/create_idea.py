#!/usr/bin/env python3
"""Create a new idea for a project."""

import sys
import json
from pathlib import Path
from datetime import datetime

# Import utils
sys.path.insert(0, str(Path(__file__).parent))
from utils import slugify, get_research_root, parse_frontmatter, validate_title


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 create_idea.py <project> <title> [--priority <priority>] [--tags <tags>]")
        print("\nPriorities: low, medium, high")
        print("Tags: Comma-separated, e.g., '3d-vision,nerf,optimization'")
        sys.exit(1)

    project_name = sys.argv[1]
    title = sys.argv[2]

    # Parse optional arguments
    priority = "medium"  # default
    tags = []

    for i, arg in enumerate(sys.argv):
        if arg == "--priority" and i + 1 < len(sys.argv):
            priority = sys.argv[i + 1]
        elif arg == "--tags" and i + 1 < len(sys.argv):
            tags = [t.strip() for t in sys.argv[i + 1].split(",")]

    # Validate priority
    valid_priorities = ["low", "medium", "high"]
    if priority not in valid_priorities:
        print(f"Error: Invalid priority '{priority}'. Valid priorities: {', '.join(valid_priorities)}")
        sys.exit(1)

    # Validate title
    is_valid, error_msg = validate_title(title)
    if not is_valid:
        print(f"Error: {error_msg}")
        sys.exit(1)

    # Get paths using new utility
    research_root = get_research_root()
    projects_dir = research_root / "projects"

    # Find project directory
    project_dir = None
    for p in projects_dir.iterdir():
        if not p.is_dir():
            continue

        project_md = p / "project.md"
        if not project_md.exists():
            continue

        content = project_md.read_text(encoding="utf-8")

        # Check if project title matches
        metadata = parse_frontmatter(content)
        project_title = metadata.get('title', '').strip()

        if project_title.lower() == project_name.lower():
            project_dir = p
            break

    if not project_dir:
        # List available projects
        available = []
        for p in projects_dir.iterdir():
            if not p.is_dir():
                continue
            project_md = p / "project.md"
            if not project_md.exists():
                continue
            metadata = parse_frontmatter(project_md.read_text(encoding='utf-8'))
            if 'title' in metadata:
                available.append(metadata['title'])

        print(f"Error: Project '{project_name}' not found\n")
        if available:
            print("Available projects:")
            for proj in available:
                print(f"  - {proj}")
        else:
            print("No projects found. Create one with:")
            print(f"  python3 scripts/create_project.py 'My Project'")
        sys.exit(1)

    # Create idea directory with safe slug
    ideas_dir = project_dir / "ideas"
    idea_slug = slugify(title)
    idea_dir = ideas_dir / idea_slug

    if idea_dir.exists():
        print(f"Error: Idea '{title}' already exists in this project")
        sys.exit(1)

    idea_dir.mkdir()

    # Get current time
    now = datetime.now().isoformat()

    # Create idea.md with proper YAML front matter
    idea_content = f"""---
title: {title}
project: {project_name}
created: {now}
updated: {now}
status: unverified
tags: {json.dumps(tags)}
priority: {priority}
---

## Idea Description

[Describe your idea]

## Hypothesis

[What do you think will happen?]

## Approach

[How will you test this idea?]

## Related Work

[Papers, projects, or previous experiments]

## Next Steps

- [ ] [Next action item]
"""

    (idea_dir / "idea.md").write_text(idea_content, encoding="utf-8")

    # Create validation.md
    validation_content = f"""---
idea: {title}
status: unverified
validated: null
---

## Validation Summary

[Idea not yet validated]

## Experiments Conducted

[No experiments yet]

## Key Findings

[Fill in after validation]

## Next Steps

- [ ] Create experiment plan
- [ ] Run experiment
"""

    (idea_dir / "validation.md").write_text(validation_content, encoding="utf-8")

    # Create experiments directory
    (idea_dir / "experiments").mkdir()

    # Update project.md timestamp
    project_md = project_dir / "project.md"
    project_content = project_md.read_text(encoding="utf-8")

    # Update timestamp
    project_content = project_content.replace(
        f"updated: {now[:10]}",
        f"updated: {now}"
    )
    project_md.write_text(project_content, encoding="utf-8")

    print(f"\n✓ Idea created successfully!")
    print(f"\nTitle: {title}")
    print(f"Project: {project_name}")
    print(f"Priority: {priority}")
    print(f"Tags: {', '.join(tags) if tags else 'None'}")
    print(f"\nLocation: {idea_dir}")
    print("\nNext steps:")
    print(f"1. Edit idea.md to add details")
    print(f"2. Create experiment: python3 scripts/create_experiment.py '{project_name}' '{title}' '<experiment title>'")


if __name__ == "__main__":
    main()
