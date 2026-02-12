#!/usr/bin/env python3
"""
List all research projects.

Usage:
    python3 list_projects.py
"""

import yaml
from pathlib import Path
from datetime import datetime


def main():
    # Get paths
    workspace = Path(__file__).parent.parent.parent.parent.parent
    research_root = workspace / "research-notes"
    projects_dir = research_root / "projects"

    if not projects_dir.exists():
        print("No projects directory found. Run init.py first.")
        return

    print("\n📚 Research Projects\n")
    print("=" * 70)

    if not any(projects_dir.iterdir()):
        print("No projects found.")
        print("\nCreate a project: python3 scripts/create_project.py <title>")
        return

    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue

        project_md = project_dir / "project.md"
        if not project_md.exists():
            continue

        # Read project metadata
        content = project_md.read_text(encoding="utf-8")

        project_data = {}
        for line in content.split('\n'):
            if line.startswith("title:"):
                project_data['title'] = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("type:"):
                project_data['type'] = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("status:"):
                project_data['status'] = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("updated:"):
                project_data['updated'] = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("priority:"):
                project_data['priority'] = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("tags:"):
                tags = line.split(':', 1)[1].strip().strip('"\'[]')
                if tags:
                    project_data['tags'] = [t.strip() for t in tags.split(',')]

        if 'title' not in project_data:
            continue

        # Count ideas and experiments
        ideas_count = 0
        experiments_count = 0

        ideas_dir = project_dir / "ideas"
        if ideas_dir.exists():
            ideas_count = sum(1 for i in ideas_dir.iterdir() if i.is_dir())
            for idea_dir in ideas_dir.iterdir():
                if idea_dir.is_dir():
                    exp_dir = idea_dir / "experiments"
                    if exp_dir.exists():
                        experiments_count += sum(1 for e in exp_dir.iterdir() if e.is_dir())

        # Print project info
        print(f"\n📁 {project_data['title']}")
        print(f"   Type: {project_data.get('type', 'N/A')}")
        print(f"   Status: {project_data.get('status', 'N/A')}")
        print(f"   Priority: {project_data.get('priority', 'N/A')}")
        print(f"   Ideas: {ideas_count}")
        print(f"   Experiments: {experiments_count}")
        print(f"   Updated: {project_data.get('updated', 'N/A')}")

        if 'tags' in project_data:
            tags_str = ', '.join(project_data['tags'])
            print(f"   Tags: {tags_str}")

        print(f"   Location: {project_dir.relative_to(workspace)}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
