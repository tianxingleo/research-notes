#!/usr/bin/env python3
"""
List all research projects.

Usage:
    python3 list_projects.py
"""

from utils import *
from pathlib import Path
from datetime import datetime


def main():
    try:
        # Get research root directory
        research_root = get_research_root()
        projects_dir = research_root / "projects"

        if not projects_dir.exists():
            print(format_error_with_suggestions(
                "No projects directory found",
                [
                    "Run init.py to initialize the research notes directory",
                    "Set RESEARCH_NOTES_ROOT environment variable if using custom path"
                ]
            ))
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

            # Read project metadata using parse_frontmatter
            try:
                content = project_md.read_text(encoding="utf-8")
                project_data = parse_frontmatter(content)
            except Exception as e:
                print(f"Warning: Failed to read {project_md}: {e}")
                continue

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

            tags = project_data.get('tags', [])
            if tags:
                tags_str = ', '.join(tags) if isinstance(tags, list) else str(tags)
                print(f"   Tags: {tags_str}")

            print(f"   Location: {project_dir.relative_to(research_root)}")

        print("\n" + "=" * 70)

    except RuntimeError as e:
        print(format_error_with_suggestions(
            str(e),
            [
                "Set RESEARCH_NOTES_ROOT environment variable",
                "Run init.py from the research-notes directory"
            ]
        ))
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
