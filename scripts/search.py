#!/usr/bin/env python3
"""
Search across research notes.

Usage:
    python3 search.py <query> [--scope <scope>]
"""

import sys
from utils import *
from pathlib import Path


def search_in_file(filepath, query):
    """Search for query in a file."""
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.split('\n')
        matches = []

        for i, line in enumerate(lines, 1):
            if query.lower() in line.lower():
                matches.append((i, line.strip()))

        return matches
    except Exception as e:
        print(f"Warning: Failed to read {filepath}: {e}")
        return []


def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python3 search.py <query> [--scope <scope>]")
            print("\nScopes: ideas, experiments, papers, all")
            sys.exit(1)

        query = sys.argv[1]

        # Parse optional arguments
        scope = "all"  # default
        for i, arg in enumerate(sys.argv):
            if arg == "--scope" and i + 1 < len(sys.argv):
                scope = sys.argv[i + 1]

        # Get research root directory
        research_root = get_research_root()
        projects_dir = research_root / "projects"

        if not projects_dir.exists():
            print(format_error_with_suggestions(
                "No projects directory found",
                [
                    "Run init.py to initialize the research notes directory",
                    "Create a project first to search"
                ]
            ))
            return

        print(f"\n🔍 Searching for: '{query}' (scope: {scope})\n")
        print("=" * 70)

        total_matches = 0

        # Search in projects
        if scope in ["all", "ideas"]:
            print("\n📝 IDEAS")
            print("-" * 70)

            for project_dir in projects_dir.iterdir():
                if not project_dir.is_dir():
                    continue

                ideas_dir = project_dir / "ideas"
                if not ideas_dir.exists():
                    continue

                # Get project name
                project_md = project_dir / "project.md"
                project_name = "Unknown"
                if project_md.exists():
                    try:
                        project_content = project_md.read_text(encoding="utf-8")
                        project_data = parse_frontmatter(project_content)
                        project_name = project_data.get('title', 'Unknown')
                    except Exception as e:
                        print(f"Warning: Failed to read project metadata: {e}")

                for idea_dir in ideas_dir.iterdir():
                    if not idea_dir.is_dir():
                        continue

                    idea_md = idea_dir / "idea.md"
                    if idea_md.exists():
                        matches = search_in_file(idea_md, query)
                        if matches:
                            # Get idea title
                            try:
                                idea_content = idea_md.read_text(encoding="utf-8")
                                idea_data = parse_frontmatter(idea_content)
                                idea_title = idea_data.get('title', 'Unknown')
                            except Exception as e:
                                idea_title = "Unknown"

                            print(f"\n  Project: {project_name}")
                            print(f"  Idea: {idea_title}")
                            print(f"  Location: {idea_dir.relative_to(research_root)}")

                            for line_num, line in matches[:3]:  # Show first 3 matches
                                print(f"    L{line_num}: {line[:80]}...")

                            if len(matches) > 3:
                                print(f"    ... ({len(matches)} total matches)")

                            total_matches += len(matches)

        # Search in experiments
        if scope in ["all", "experiments"]:
            print("\n\n🧪 EXPERIMENTS")
            print("-" * 70)

            for project_dir in projects_dir.iterdir():
                if not project_dir.is_dir():
                    continue

                ideas_dir = project_dir / "ideas"
                if not ideas_dir.exists():
                    continue

                # Get project name
                project_md = project_dir / "project.md"
                project_name = "Unknown"
                if project_md.exists():
                    try:
                        project_content = project_md.read_text(encoding="utf-8")
                        project_data = parse_frontmatter(project_content)
                        project_name = project_data.get('title', 'Unknown')
                    except Exception as e:
                        print(f"Warning: Failed to read project metadata: {e}")

                for idea_dir in ideas_dir.iterdir():
                    if not idea_dir.is_dir():
                        continue

                    experiments_dir = idea_dir / "experiments"
                    if not experiments_dir.exists():
                        continue

                    for experiment_dir in experiments_dir.iterdir():
                        if not experiment_dir.is_dir():
                            continue

                        experiment_md = experiment_dir / "experiment.md"
                        if experiment_md.exists():
                            matches = search_in_file(experiment_md, query)
                            if matches:
                                # Get experiment title
                                try:
                                    experiment_content = experiment_md.read_text(encoding="utf-8")
                                    experiment_data = parse_frontmatter(experiment_content)
                                    experiment_title = experiment_data.get('title', 'Unknown')
                                    idea_title = experiment_data.get('idea', 'Unknown')
                                except Exception as e:
                                    experiment_title = "Unknown"
                                    idea_title = "Unknown"

                                print(f"\n  Project: {project_name}")
                                print(f"  Idea: {idea_title}")
                                print(f"  Experiment: {experiment_title}")
                                print(f"  Location: {experiment_dir.relative_to(research_root)}")

                                for line_num, line in matches[:3]:
                                    print(f"    L{line_num}: {line[:80]}...")

                                if len(matches) > 3:
                                    print(f"    ... ({len(matches)} total matches)")

                                total_matches += len(matches)

        print("\n" + "=" * 70)
        print(f"\n✓ Found {total_matches} matches total")

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
