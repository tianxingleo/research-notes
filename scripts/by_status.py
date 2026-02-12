#!/usr/bin/env python3
"""
List items by status.

Usage:
    python3 by_status.py <status> [--scope <scope>]
"""

import sys
from utils import *
from pathlib import Path


def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python3 by_status.py <status> [--scope <scope>]")
            print("\nStatus options:")
            print("  Projects: active, on-hold, completed")
            print("  Ideas: unverified, planned, in-progress, validated, rejected, on-hold")
            print("  Experiments: planned, in-progress, completed, failed")
            print("\nScopes: projects, ideas, experiments, all")
            sys.exit(1)

        status = sys.argv[1]

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
                    "Create a project first"
                ]
            ))
            return

        print(f"\n📊 Items with status: '{status}' (scope: {scope})\n")
        print("=" * 70)

        total_matches = 0

        # Search in projects
        if scope in ["all", "projects"]:
            print("\n📁 PROJECTS")
            print("-" * 70)

            valid_project_statuses = ["active", "on-hold", "completed"]
            if status not in valid_project_statuses:
                print(f"  (Skipping projects - '{status}' is not a valid project status)")
            else:
                projects_found = 0
                for project_dir in projects_dir.iterdir():
                    if not project_dir.is_dir():
                        continue

                    project_md = project_dir / "project.md"
                    if not project_md.exists():
                        continue

                    try:
                        content = project_md.read_text(encoding="utf-8")
                        project_data = parse_frontmatter(content)

                        project_status = project_data.get('status', '').lower()

                        if project_status == status.lower() and project_data.get('title'):
                            print(f"\n  {project_data['title']}")
                            print(f"  Type: {project_data.get('type', 'N/A')}")
                            print(f"  Location: {project_dir.relative_to(research_root)}")
                            projects_found += 1
                            total_matches += 1

                    except Exception as e:
                        print(f"Warning: Failed to read {project_md}: {e}")
                        continue

                if projects_found == 0:
                    print("  No projects found with this status.")

        # Search in ideas
        if scope in ["all", "ideas"]:
            print("\n\n📝 IDEAS")
            print("-" * 70)

            valid_idea_statuses = ["unverified", "planned", "in-progress", "validated", "rejected", "on-hold"]
            if status not in valid_idea_statuses:
                print(f"  (Skipping ideas - '{status}' is not a valid idea status)")
            else:
                ideas_found = 0
                for project_dir in projects_dir.iterdir():
                    if not project_dir.is_dir():
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

                    ideas_dir = project_dir / "ideas"
                    if not ideas_dir.exists():
                        continue

                    for idea_dir in ideas_dir.iterdir():
                        if not idea_dir.is_dir():
                            continue

                        idea_md = idea_dir / "idea.md"
                        if not idea_md.exists():
                            continue

                        try:
                            content = idea_md.read_text(encoding="utf-8")
                            idea_data = parse_frontmatter(content)

                            idea_status = idea_data.get('status', '').lower()

                            if idea_status == status.lower() and idea_data.get('title'):
                                print(f"\n  Project: {project_name}")
                                print(f"  Idea: {idea_data['title']}")
                                print(f"  Priority: {idea_data.get('priority', 'N/A')}")
                                print(f"  Location: {idea_dir.relative_to(research_root)}")
                                ideas_found += 1
                                total_matches += 1

                        except Exception as e:
                            print(f"Warning: Failed to read {idea_md}: {e}")
                            continue

                if ideas_found == 0:
                    print("  No ideas found with this status.")

        # Search in experiments
        if scope in ["all", "experiments"]:
            print("\n\n🧪 EXPERIMENTS")
            print("-" * 70)

            valid_experiment_statuses = ["planned", "in-progress", "completed", "failed"]
            if status not in valid_experiment_statuses:
                print(f"  (Skipping experiments - '{status}' is not a valid experiment status)")
            else:
                experiments_found = 0
                for project_dir in projects_dir.iterdir():
                    if not project_dir.is_dir():
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

                    ideas_dir = project_dir / "ideas"
                    if not ideas_dir.exists():
                        continue

                    for idea_dir in ideas_dir.iterdir():
                        if not idea_dir.is_dir():
                            continue

                        # Get idea title
                        idea_md = idea_dir / "idea.md"
                        idea_title = "Unknown"
                        if idea_md.exists():
                            try:
                                idea_content = idea_md.read_text(encoding="utf-8")
                                idea_data = parse_frontmatter(idea_content)
                                idea_title = idea_data.get('title', 'Unknown')
                            except Exception as e:
                                print(f"Warning: Failed to read idea metadata: {e}")

                        experiments_dir = idea_dir / "experiments"
                        if not experiments_dir.exists():
                            continue

                        for experiment_dir in experiments_dir.iterdir():
                            if not experiment_dir.is_dir():
                                continue

                            experiment_md = experiment_dir / "experiment.md"
                            if not experiment_md.exists():
                                continue

                            try:
                                content = experiment_md.read_text(encoding="utf-8")
                                experiment_data = parse_frontmatter(content)

                                experiment_status = experiment_data.get('status', '').lower()

                                if experiment_status == status.lower() and experiment_data.get('title'):
                                    print(f"\n  Project: {project_name}")
                                    print(f"  Idea: {idea_title}")
                                    print(f"  Experiment: {experiment_data['title']}")
                                    print(f"  Location: {experiment_dir.relative_to(research_root)}")
                                    experiments_found += 1
                                    total_matches += 1

                            except Exception as e:
                                print(f"Warning: Failed to read {experiment_md}: {e}")
                                continue

                if experiments_found == 0:
                    print("  No experiments found with this status.")

        print("\n" + "=" * 70)
        print(f"\n✓ Found {total_matches} items with status '{status}'")

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
