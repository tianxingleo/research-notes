#!/usr/bin/env python3
"""Show recent changes."""

import sys
from datetime import datetime, timedelta
from pathlib import Path


def parse_iso_date(date_str):
    """Parse ISO 8601 date string."""
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        return None


def parse_frontmatter(content):
    """Extract YAML front matter from markdown."""
    if not content or not content.startswith('---'):
        return {}

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    try:
        import yaml
        metadata = yaml.safe_load(parts[1]) or {}
        return metadata if isinstance(metadata, dict) else {}
    except:
        return {}


def main():
    days = 7

    for i, arg in enumerate(sys.argv):
        if arg == "--days" and i + 1 < len(sys.argv):
            try:
                days = int(sys.argv[i + 1])
            except ValueError:
                print("Error: --days must be a number")
                sys.exit(1)

    # Get paths - try multiple locations
    workspace = Path(__file__).parent.parent.parent.parent
    research_root = workspace / "research-notes"

    if not research_root.exists():
        # Try home directory
        research_root = Path.home() / "research-notes"

    if not research_root.exists():
        print("Error: Research notes directory not found.")
        print("Please run init.py first to create the structure.")
        sys.exit(1)

    projects_dir = research_root / "projects"
    cutoff_date = datetime.now() - timedelta(days=days)

    print(f"\n📅 Recent changes (last {days} days)")
    print(f"Since: {cutoff_date.isoformat()}\n")
    print("=" * 70)

    recent_items = []

    # Search in projects
    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue

        project_md = project_dir / "project.md"
        if not project_md.exists():
            continue

        content = project_md.read_text(encoding="utf-8")

        # Parse metadata
        metadata = parse_frontmatter(content)
        project_title = metadata.get('title')
        project_type = metadata.get('type')
        updated_str = metadata.get('updated')

        if updated_str:
            updated = parse_iso_date(updated_str)
        else:
            updated = None

        if updated and updated > cutoff_date and project_title:
            recent_items.append({
                'type': 'project',
                'title': project_title,
                'project_type': project_type,
                'updated': updated,
                'location': project_dir.relative_to(research_root)
            })

        # Search in ideas
        ideas_dir = project_dir / "ideas"
        if ideas_dir.exists():
            for idea_dir in ideas_dir.iterdir():
                if not idea_dir.is_dir():
                    continue

                idea_md = idea_dir / "idea.md"
                if not idea_md.exists():
                    continue

                content = idea_md.read_text(encoding="utf-8")

                # Parse metadata
                metadata = parse_frontmatter(content)
                idea_title = metadata.get('title')
                idea_status = metadata.get('status')
                updated_str = metadata.get('updated')

                if updated_str:
                    updated = parse_iso_date(updated_str)
                else:
                    updated = None

                if updated and updated > cutoff_date and idea_title:
                    recent_items.append({
                        'type': 'idea',
                        'title': idea_title,
                        'project': project_title,
                        'status': idea_status,
                        'updated': updated,
                        'location': idea_dir.relative_to(research_root)
                    })

                # Search in experiments
                experiments_dir = idea_dir / "experiments"
                if experiments_dir.exists():
                    for experiment_dir in experiments_dir.iterdir():
                        if not experiment_dir.is_dir():
                            continue

                        experiment_md = experiment_dir / "experiment.md"
                        if not experiment_md.exists():
                            continue

                        content = experiment_md.read_text(encoding="utf-8")

                        # Parse metadata
                        metadata = parse_frontmatter(content)
                        experiment_title = metadata.get('title')
                        experiment_status = metadata.get('status')
                        updated_str = metadata.get('updated')

                        if updated_str:
                            updated = parse_iso_date(updated_str)
                        else:
                            updated = None

                        if updated and updated > cutoff_date and experiment_title:
                            recent_items.append({
                                'type': 'experiment',
                                'title': experiment_title,
                                'project': project_title,
                                'idea': idea_title,
                                'status': experiment_status,
                                'updated': updated,
                                'location': experiment_dir.relative_to(research_root)
                            })

    # Sort by updated date (newest first)
    recent_items.sort(key=lambda x: x['updated'], reverse=True)

    # Display results
    if not recent_items:
        print(f"No changes found in the last {days} days.")
        print("\nTips:")
        print("- Increase --days to see older changes")
        print("- Create a new project or idea to get started")
        return

    for item in recent_items:
        type_icons = {
            'project': '📁',
            'idea': '💡',
            'experiment': '🧪'
        }

        print(f"\n{type_icons[item['type']]} {item['type'].upper()}")

        if item['type'] == 'project':
            print(f"  Title: {item['title']}")
            print(f"  Type: {item['project_type']}")
        elif item['type'] == 'idea':
            print(f"  Project: {item['project']}")
            print(f"  Idea: {item['title']}")
            print(f"  Status: {item['status']}")
        elif item['type'] == 'experiment':
            print(f"  Project: {item['project']}")
            print(f"  Idea: {item['idea']}")
            print(f"  Experiment: {item['title']}")
            print(f"  Status: {item['status']}")

        print(f"  Updated: {item['updated'].isoformat()}")
        print(f"  Location: {item['location']}")

    print("\n" + "=" * 70)
    print(f"\n✓ Found {len(recent_items)} items changed in the last {days} days")


if __name__ == "__main__":
    main()
