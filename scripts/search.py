#!/usr/bin/env python3
"""
Search across research notes.

Usage:
    python3 search.py <query> [--scope <scope>]
"""

import sys
import re
from pathlib import Path


def slugify(text):
    """Convert text to slug."""
    return text.lower().replace(' ', '-').replace('_', '-')


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
    except:
        return []


def main():
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

    # Get paths
    workspace = Path(__file__).parent.parent.parent.parent.parent
    research_root = workspace / "research-notes"
    projects_dir = research_root / "projects"

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
            if project_md.exists():
                project_content = project_md.read_text(encoding="utf-8")
                for line in project_content.split('\n'):
                    if line.startswith("title:"):
                        project_name = line.split(':', 1)[1].strip().strip('"\'')
                        break

            for idea_dir in ideas_dir.iterdir():
                if not idea_dir.is_dir():
                    continue

                idea_md = idea_dir / "idea.md"
                if idea_md.exists():
                    matches = search_in_file(idea_md, query)
                    if matches:
                        # Get idea title
                        idea_content = idea_md.read_text(encoding="utf-8")
                        for line in idea_content.split('\n'):
                            if line.startswith("title:"):
                                idea_title = line.split(':', 1)[1].strip().strip('"\'')
                                break

                        print(f"\n  Project: {project_name}")
                        print(f"  Idea: {idea_title}")
                        print(f"  Location: {idea_dir.relative_to(workspace)}")

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
            if project_md.exists():
                project_content = project_md.read_text(encoding="utf-8")
                for line in project_content.split('\n'):
                    if line.startswith("title:"):
                        project_name = line.split(':', 1)[1].strip().strip('"\'')
                        break

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
                            experiment_content = experiment_md.read_text(encoding="utf-8")
                            for line in experiment_content.split('\n'):
                                if line.startswith("title:"):
                                    experiment_title = line.split(':', 1)[1].strip().strip('"\'')
                                    break
                                if line.startswith("idea:"):
                                    idea_title = line.split(':', 1)[1].strip().strip('"\'')
                                    break

                            print(f"\n  Project: {project_name}")
                            print(f"  Idea: {idea_title}")
                            print(f"  Experiment: {experiment_title}")
                            print(f"  Location: {experiment_dir.relative_to(workspace)}")

                            for line_num, line in matches[:3]:
                                print(f"    L{line_num}: {line[:80]}...")

                            if len(matches) > 3:
                                print(f"    ... ({len(matches)} total matches)")

                            total_matches += len(matches)

    print("\n" + "=" * 70)
    print(f"\n✓ Found {total_matches} matches total")


if __name__ == "__main__":
    main()
