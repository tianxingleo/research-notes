#!/usr/bin/env python3
"""
Update validation status for an idea.

Usage:
    python3 update_validation.py <project> <idea> --status <status>
"""

import sys
import re
from datetime import datetime
from pathlib import Path


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

    # Get paths
    workspace = Path(__file__).parent.parent.parent.parent.parent
    research_root = workspace / "research-notes"
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
        for line in content.split('\n'):
            if line.startswith("title:"):
                project_title = line.split(':', 1)[1].strip().strip('"\'')
                if project_title.lower() == project_name.lower():
                    project_dir = p
                    break

        if project_dir:
            # Find idea
            ideas_dir = project_dir / "ideas"
            if ideas_dir.exists():
                for i in ideas_dir.iterdir():
                    if i.is_dir():
                        idea_md = i / "idea.md"
                        if idea_md.exists():
                            idea_content = idea_md.read_text(encoding="utf-8")
                            for line in idea_content.split('\n'):
                                if line.startswith("title:"):
                                    it = line.split(':', 1)[1].strip().strip('"\'')
                                    if it.lower() == idea_title.lower():
                                        idea_dir = i
                                        break
                            if idea_dir:
                                break
            break

    if not project_dir:
        print(f"Error: Project '{project_name}' not found")
        sys.exit(1)

    if not idea_dir:
        print(f"Error: Idea '{idea_title}' not found in project '{project_name}'")
        sys.exit(1)

    # Update idea.md status
    idea_md = idea_dir / "idea.md"
    idea_content = idea_md.read_text(encoding="utf-8")

    # Update status in idea.md
    idea_content = re.sub(
        r'^status: .*$',
        f'status: {status}',
        idea_content,
        flags=re.MULTILINE
    )

    now = datetime.now().isoformat()
    idea_content = re.sub(
        r'^updated: .*$',
        f'updated: {now}',
        idea_content,
        flags=re.MULTILINE
    )

    idea_md.write_text(idea_content, encoding="utf-8")

    # Update validation.md
    validation_md = idea_dir / "validation.md"
    validation_content = validation_md.read_text(encoding="utf-8")

    # Update status in validation.md
    validation_content = re.sub(
        r'^status: .*$',
        f'status: {status}',
        validation_content,
        flags=re.MULTILINE
    )

    if status in ["validated", "rejected"]:
        validation_content = re.sub(
            r'^validated: null$',
            f'validated: {now}',
            validation_content,
            flags=re.MULTILINE
        )
    else:
        validation_content = re.sub(
            r'^validated: .*$',
            'validated: null',
            validation_content,
            flags=re.MULTILINE
        )

    validation_md.write_text(validation_content, encoding="utf-8")

    print(f"\n✓ Validation status updated successfully!")
    print(f"\nIdea: {idea_title}")
    print(f"Project: {project_name}")
    print(f"New status: {status}")
    if status in ["validated", "rejected"]:
        print(f"Validated: {now}")


if __name__ == "__main__":
    main()
