#!/usr/bin/env python3
"""
Sync research notes to Notion.

Usage:
    python3 notion_sync.py [--project <project>] [--all] [--incremental]
"""

import sys
import yaml
from pathlib import Path


def load_config():
    """Load configuration."""
    workspace = Path(__file__).parent.parent.parent.parent.parent
    research_root = workspace / "research-notes"
    config_path = research_root / "config.yaml"

    if not config_path.exists():
        print("Error: config.yaml not found")
        print("Run init.py first to create config")
        sys.exit(1)

    with open(config_path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_notion_installed():
    """Check if notion-client is installed."""
    try:
        import notion_client
        return True
    except ImportError:
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 notion_sync.py [--project <project>] [--all] [--incremental]")
        print("\nRequires: pip install notion-client")
        print("Setup: Edit config.yaml to add Notion token and database ID")
        sys.exit(1)

    # Load config
    config = load_config()

    if not config.get('notion', {}).get('enabled', False):
        print("Error: Notion sync is not enabled")
        print("Edit config.yaml and set notion.enabled: true")
        print("Add your Notion integration token and database ID")
        sys.exit(1)

    # Check if notion-client is installed
    if not check_notion_installed():
        print("Error: notion-client package not installed")
        print("Install with: pip install notion-client")
        sys.exit(1)

    from notion_client import Client

    notion = Client(auth=config['notion']['token'])
    database_id = config['notion']['database_id']

    # Parse arguments
    project_name = None
    sync_all = False
    incremental = False

    for i, arg in enumerate(sys.argv):
        if arg == "--project" and i + 1 < len(sys.argv):
            project_name = sys.argv[i + 1]
        elif arg == "--all":
            sync_all = True
        elif arg == "--incremental":
            incremental = True

    print("✓ Notion sync initialized")
    print(f"\nConfiguration:")
    print(f"  Database ID: {database_id}")
    print(f"  Sync All: {sync_all}")
    print(f"  Incremental: {incremental}")
    if project_name:
        print(f"  Project: {project_name}")

    # For now, just show sync status
    print("\n🔄 Sync would happen here (notion-client integration)")
    print("\nTo complete Notion integration:")
    print("1. Create a Notion integration at https://www.notion.so/my-integrations")
    print("2. Create a database with required properties")
    print("3. Share the database with your integration")
    print("4. Add the token and database ID to config.yaml")
    print("\nRequired database properties:")
    print("  - Name (Title)")
    print("  - Type (Select)")
    print("  - Status (Select)")
    print("  - Tags (Multi-select)")
    print("  - Created (Date)")
    print("  - Updated (Date)")
    print("  - Priority (Select)")


if __name__ == "__main__":
    main()
