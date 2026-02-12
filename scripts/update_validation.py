#!/usr/bin/env python3
"""
Update validation status for an idea.

Usage:
    python3 update_validation.py <project> <idea> --status <status>
"""

import sys
from datetime import datetime
from pathlib import Path

# Import utils
sys.path.insert(0, str(Path(__file__).parent))
from utils import get_research_root, parse_frontmatter


def main():
    if len(sys.argv) < 5:
        print("Usage: python3 update_validation.py <project> <idea> --status <status>")
        print("\nStatus: unverified, planned, in-progress, validated, rejected, on-hold")
        sys.exit(1)

    project_name = sys.argv[1]
    idea_title = sys.argv[2]

    # Parse status
    if sys.argv[3] != "--status" or len(sys.argv) < 5:
        print("Error: --status required")
        sys.exit(1)

    status = sys.argv[4]

    # Validate status
    valid_statuses = ["unverified", "planned", "in-progress", "validated", "rejected", "on-hold"]
    if status not in valid_statuses:
        print(f"Error: Invalid status '{status}'. Valid statuses: {', '.join(valid_statuses)}")
        sys.exit(1)

    # Get paths using new utility
    research_root = get_research_root()
    projects_dir = research_root / "projects"

    # Find project and idea directories
    project_dir = None
    idea_dir = None

    for p in projects_dir.iterdir():
        if not p.is_dir():
            continue

        project_md = p / "project.md"
        if not project_md.exists():
            continue

        content = project_md.read_text(encoding="utf-8")

        # Check if project title matches
        metadata = parse_frontmatter(content)
        p_title = metadata.get('title', '').strip()

        if p_title.lower() == project_name.lower():
            project_dir = p

            # Find idea
            ideas_dir = project_dir / "ideas"
            if ideas_dir.exists():
                for i in ideas_dir.iterdir():
                    if not i.is_dir():
                        continue

                    idea_md = i / "idea.md"
                    if not idea_md.exists():
                        continue

                    content = idea_md.read_text(encoding="utf-8")

                    # Check if idea title matches
                    metadata = parse_frontmatter(content)
                    i_title = metadata.get('title', '').strip()

                    if i_title.lower() == idea_title.lower():
                        idea_dir = i
                        break
            if idea_dir:
                break

    if not project_dir:
        print(f"Error: Project '{project_name}' not found")
        sys.exit(1)

    if not idea_dir:
        print(f"Error: Idea '{idea_title}' not found in project '{project_name}'")
        sys.exit(1)

    now = datetime.now().isoformat()

    # Update idea.md status
    idea_md = idea_dir / "idea.md"
    idea_content = idea_md.read_text(encoding="utf-8")

    # Replace status using YAML-safe approach
    # Find the status line and replace it
    lines = idea_content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith("status:"):
            lines[i] = f"status: {status}"
            break

    # Also update timestamp
    for i, line in enumerate(lines):
        if line.startswith("updated:"):
            lines[i] = f"updated: {now}"
            break

    idea_md.write_text('\n'.join(lines), encoding="utf-8")

    # Update validation.md
    validation_md = idea_dir / "validation.md"
    validation_content = validation_md.read_text(encoding="utf-8")

    # Replace status in validation.md
    lines = validation_content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith("status:"):
            lines[i] = f"status: {status}"
            break

    # Update validated date if status is validated or rejected
    if status in ["validated", "rejected"]:
        for i, line in enumerate(lines):
            if line.startswith("validated:"):
                lines[i] = f"validated: {now}"
                break
    else:
        # Remove validated date if not validated
        for i, line in enumerate(lines):
            if line.startswith("validated:"):
                lines[i] = f"validated: null"
                break

    validation_md.write_text('\n'.join(lines), encoding="utf-8")

    print(f"\n✓ Validation status updated successfully!")
    print(f"\nIdea: {idea_title}")
    print(f"Project: {project_name}")
    print(f"New status: {status}")
    if status in ["validated", "rejected"]:
        print(f"Validated: {now}")


if __name__ == "__main__":
    main()
