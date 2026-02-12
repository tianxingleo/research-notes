#!/usr/bin/env python3
"""
Initialize Git repository for research notes.

Usage:
    python3 init_git.py
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run shell command."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def main():
    workspace = Path(__file__).parent.parent.parent.parent.parent
    research_root = workspace / "research-notes"

    if not research_root.exists():
        print("Error: Research notes directory not found")
        print("Run init.py first to create the structure")
        sys.exit(1)

    # Check if already initialized
    git_dir = research_root / ".git"
    if git_dir.exists():
        print("✓ Git repository already initialized")
        print(f"  Location: {research_root}")
        print("\nTo add remote:")
        print(f"  cd {research_root}")
        print("  git remote add origin <repository-url>")
        print("  git push -u origin main")
        return

    print("Initializing Git repository...")
    print(f"Location: {research_root}\n")

    # Initialize git
    success, stdout, stderr = run_command("git init", cwd=research_root)
    if not success:
        print(f"Error initializing git: {stderr}")
        sys.exit(1)

    print("✓ Git initialized")

    # Set default branch to main
    success, stdout, stderr = run_command("git checkout -b main", cwd=research_root)
    if not success:
        print(f"Error creating main branch: {stderr}")
        sys.exit(1)

    print("✓ Created 'main' branch")

    # Add all files
    success, stdout, stderr = run_command("git add -A", cwd=research_root)
    if not success:
        print(f"Error adding files: {stderr}")
        sys.exit(1)

    print("✓ Staged all files")

    # Initial commit
    success, stdout, stderr = run_command(
        'git commit -m "Initial commit: Research Notes"',
        cwd=research_root
    )
    if not success:
        print(f"Error committing: {stderr}")
        sys.exit(1)

    print("✓ Created initial commit")

    print("\n✓ Git repository initialized successfully!")
    print("\nNext steps:")
    print("1. Create a remote repository on GitHub")
    print("2. Add remote: git remote add origin <repository-url>")
    print("3. Push: git push -u origin main")


if __name__ == "__main__":
    main()
