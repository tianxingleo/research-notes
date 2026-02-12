#!/usr/bin/env python3
"""Create a new experiment for an idea."""

import sys
from pathlib import Path
from datetime import datetime

# Import utils
sys.path.insert(0, str(Path(__file__).parent))
from utils import slugify, get_research_root, parse_frontmatter, validate_title


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 create_experiment.py <project> <idea> <title>")
        sys.exit(1)

    project_name = sys.argv[1]
    idea_title = sys.argv[2]
    experiment_title = sys.argv[3]

    # Validate title
    is_valid, error_msg = validate_title(experiment_title)
    if not is_valid:
        print(f"Error: {error_msg}")
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
        print(f"Available ideas in project '{project_name}':")
        ideas_dir = project_dir / "ideas"
        if ideas_dir.exists():
            for i in ideas_dir.iterdir():
                if i.is_dir():
                    idea_md = i / "idea.md"
                    if idea_md.exists():
                        metadata = parse_frontmatter(idea_md.read_text(encoding='utf-8'))
                        if 'title' in metadata:
                            print(f"  - {metadata['title']}")
        sys.exit(1)

    # Create experiment directory with safe slug
    experiments_dir = idea_dir / "experiments"
    experiment_slug = slugify(experiment_title)
    experiment_dir = experiments_dir / experiment_slug

    if experiment_dir.exists():
        print(f"Error: Experiment '{experiment_title}' already exists")
        sys.exit(1)

    experiment_dir.mkdir()

    # Get current time
    now = datetime.now().isoformat()

    # Create experiment.md
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

    # Update idea.md timestamp
    idea_md = idea_dir / "idea.md"
    idea_content = idea_md.read_text(encoding="utf-8")

    # Update timestamp
    idea_content = idea_content.replace(
        f"updated: {now[:10]}",
        f"updated: {now}"
    )
    idea_md.write_text(idea_content, encoding="utf-8")

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
