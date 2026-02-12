#!/usr/bin/env python3
"""
List items by tag.

Usage:
    python3 by_tag.py <tag> [--scope <scope>]
"""

import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 by_tag.py <tag> [--scope <scope>]")
        print("\nScopes: projects, ideas, experiments, all")
        sys.exit(1)

    tag = sys.argv[1]

    # Parse optional arguments
    scope = "all"  # default
    for i, arg in enumerate(sys.argv):
        if arg == "--scope" and i + 1 < len(sys.argv):
            scope = sys.argv[i + 1]

    # Get paths
    workspace = Path(__file__).parent.parent.parent.parent.parent
    research_root = workspace / "research-notes"
    projects_dir = research_root / "projects"

    print(f"\n🏷️  Items tagged with: '{tag}' (scope: {scope})\n")
    print("=" * 70)

    total_matches = 0

    # Search in projects
    if scope in ["all", "projects"]:
        print("\n📁 PROJECTS")
        print("-" * 70)

        for project_dir in projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            project_md = project_dir / "project.md"
            if not project_md.exists():
                continue

            content = project_md.read_text(encoding="utf-8")

            # Check if tag is in tags list
            tags_match = False
            project_title = None
            project_type = None

            for line in content.split('\n'):
                if line.startswith("title:"):
                    project_title = line.split(':', 1)[1].strip().strip('"\'')
                elif line.startswith("type:"):
                    project_type = line.split(':', 1)[1].strip().strip('"\'')
                elif line.startswith("tags:"):
                    tags_str = line.split(':', 1)[1].strip().strip('"\'[]')
                    if tags_str:
                        tags = [t.strip() for t in tags_str.split(',')]
                        if tag.lower() in [t.lower() for t in tags]:
                            tags_match = True

            if tags_match and project_title:
                print(f"\n  {project_title}")
                print(f"  Type: {project_type}")
                print(f"  Location: {project_dir.relative_to(workspace)}")
                total_matches += 1

    # Search in ideas
    if scope in ["all", "ideas"]:
        print("\n\n📝 IDEAS")
        print("-" * 70)

        for project_dir in projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            project_md = project_dir / "project.md"
            if not project_md.exists():
                continue

            project_content = project_md.read_text(encoding="utf-8")
            for line in project_content.split('\n'):
                if line.startswith("title:"):
                    project_title = line.split(':', 1)[1].strip().strip('"\'')
                    break

            ideas_dir = project_dir / "ideas"
            if not ideas_dir.exists():
                continue

            for idea_dir in ideas_dir.iterdir():
                if not idea_dir.is_dir():
                    continue

                idea_md = idea_dir / "idea.md"
                if not idea_md.exists():
                    continue

                content = idea_md.read_text(encoding="utf-8")

                # Check if tag is in tags list
                tags_match = False
                idea_title = None
                idea_status = None

                for line in content.split('\n'):
                    if line.startswith("title:"):
                        idea_title = line.split(':', 1)[1].strip().strip('"\'')
                    elif line.startswith("status:"):
                        idea_status = line.split(':', 1)[1].strip().strip('"\'')
                    elif line.startswith("tags:"):
                        tags_str = line.split(':', 1)[1].strip().strip('"\'[]')
                        if tags_str:
                            tags = [t.strip() for t in tags_str.split(',')]
                            if tag.lower() in [t.lower() for t in tags]:
                                tags_match = True

                if tags_match and idea_title:
                    print(f"\n  Project: {project_title}")
                    print(f"  Idea: {idea_title}")
                    print(f"  Status: {idea_status}")
                    print(f"  Location: {idea_dir.relative_to(workspace)}")
                    total_matches += 1

    # Search in experiments
    if scope in ["all", "experiments"]:
        print("\n\n🧪 EXPERIMENTS")
        print("-" * 70)

        for project_dir in projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            project_md = project_dir / "project.md"
            if not project_md.exists():
                continue

            project_content = project_md.read_text(encoding="utf-8")
            for line in project_content.split('\n'):
                if line.startswith("title:"):
                    project_title = line.split(':', 1)[1].strip().strip('"\'')
                    break

            ideas_dir = project_dir / "ideas"
            if not ideas_dir.exists():
                continue

            for idea_dir in ideas_dir.iterdir():
                if not idea_dir.is_dir():
                    continue

                idea_md = idea_dir / "idea.md"
                if not idea_md.exists():
                    continue

                idea_content = idea_md.read_text(encoding="utf-8")
                for line in idea_content.split('\n'):
                    if line.startswith("title:"):
                        idea_title = line.split(':', 1)[1].strip().strip('"\'')
                        break

                experiments_dir = idea_dir / "experiments"
                if not experiments_dir.exists():
                    continue

                for experiment_dir in experiments_dir.iterdir():
                    if not experiment_dir.is_dir():
                        continue

                    experiment_md = experiment_dir / "experiment.md"
                    if not experiment_md.exists():
                        continue

                    content = experiment_md.read_text(encoding="utf-8")

                    # Check if tag is in tags list
                    tags_match = False
                    experiment_title = None
                    experiment_status = None

                    for line in content.split('\n'):
                        if line.startswith("title:"):
                            experiment_title = line.split(':', 1)[1].strip().strip('"\'')
                        elif line.startswith("status:"):
                            experiment_status = line.split(':', 1)[1].strip().strip('"\'')
                        elif line.startswith("tags:"):
                            tags_str = line.split(':', 1)[1].strip().strip('"\'[]')
                            if tags_str:
                                tags = [t.strip() for t in tags_str.split(',')]
                                if tag.lower() in [t.lower() for t in tags]:
                                    tags_match = True

                    if tags_match and experiment_title:
                        print(f"\n  Project: {project_title}")
                        print(f"  Idea: {idea_title}")
                        print(f"  Experiment: {experiment_title}")
                        print(f"  Status: {experiment_status}")
                        print(f"  Location: {experiment_dir.relative_to(workspace)}")
                        total_matches += 1

    print("\n" + "=" * 70)
    print(f"\n✓ Found {total_matches} items with tag '{tag}'")


if __name__ == "__main__":
    main()
