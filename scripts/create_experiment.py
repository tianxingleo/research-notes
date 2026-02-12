#!/usr/bin/env python3
"""
Create a new experiment for an idea.

Usage:
    python3 create_experiment.py <project> <idea> <title>
"""

import sys
from datetime import datetime
from pathlib import Path


def slugify(text):
    """Convert text to slug."""
    return text.lower().replace(' ', '-').replace('_', '-')


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 create_experiment.py <project> <idea> <title>")
        sys.exit(1)

    project_name = sys.argv[1]
    idea_title = sys.argv[2]
    experiment_title = sys.argv[3]

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

    # Create experiment directory
    experiments_dir = idea_dir / "experiments"
    experiment_slug = slugify(experiment_title)
    experiment_dir = experiments_dir / experiment_slug

    if experiment_dir.exists():
        print(f"Error: Experiment '{experiment_title}' already exists")
        sys.exit(1)

    experiment_dir.mkdir()

    # Create experiment.md
    now = datetime.now().isoformat()

    experiment_content = f"""---
title: {experiment_title}
idea: {idea_title}
project: {project_name}
created: {now}
updated: {now}
status: planned
tags: []
---

## Experiment Setup

[Describe your experimental setup]

- Dataset:
- Parameters:
- Metrics:
- Baseline:

## Hypothesis

[Your hypothesis about what will happen]

## Procedure

[Step-by-step procedure]

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Results

[What you expect to happen]

## Actual Results

[Fill in after experiment completes]

## Conclusion

[Your conclusion from the experiment]
"""

    (experiment_dir / "experiment.md").write_text(experiment_content, encoding="utf-8")

    # Create results.md
    results_content = """# Experiment Results

[Fill in after experiment completes]

## Metrics

| Metric | Value |
|--------|-------|
|        |       |

## Visualizations

[Add plots, charts, or images]

## Raw Data

[Add links to raw data files]
"""

    (experiment_dir / "results.md").write_text(results_content, encoding="utf-8")

    # Create artifacts directory
    (experiment_dir / "artifacts").mkdir()

    print(f"\n✓ Experiment created successfully!")
    print(f"\nTitle: {experiment_title}")
    print(f"Idea: {idea_title}")
    print(f"Project: {project_name}")
    print(f"\nLocation: {experiment_dir}")
    print("\nNext steps:")
    print(f"1. Edit experiment.md to add setup and procedure")
    print(f"2. Run experiment")
    print(f"3. Fill in results.md")
    print(f"4. Update validation: python3 scripts/update_validation.py '{project_name}' '{idea_title}'")


if __name__ == "__main__":
    main()
