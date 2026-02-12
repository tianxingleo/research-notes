#!/usr/bin/env python3
"""
Initialize Research Notes structure.

Creates base directory structure, index files, and config.
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path


def main():
    # Get workspace root
    workspace = Path(__file__).parent.parent.parent.parent.parent
    research_root = workspace / "research-notes"

    if research_root.exists():
        print(f"✓ Research notes already exists at {research_root}")
        overwrite = input("Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("Aborted.")
            return

    # Create base structure
    print("Creating research notes structure...")
    research_root.mkdir(exist_ok=True)

    # Create projects directory
    projects_dir = research_root / "projects"
    projects_dir.mkdir(exist_ok=True)

    # Create index.md
    index_content = """# Research Notes Index

Last updated: {date}

## Projects

[Projects will be listed here automatically]

## Tags

[Tags will be listed here automatically]

## Quick Stats

- Total Projects: 0
- Total Ideas: 0
- Total Experiments: 0
""".format(date=datetime.now().isoformat())

    (research_root / "index.md").write_text(index_content, encoding="utf-8")

    # Create tags.md
    tags_content = """# Research Notes Tags

Use tags to organize your research across projects.

## Common Tags

- #3d-vision - 3D computer vision
- #deep-learning - Deep learning techniques
- #optimization - Performance optimization
- #reconstruction - 3D reconstruction
- #neural-rendering - Neural rendering
- #real-time - Real-time systems

## Tag Usage

Add tags to any project, idea, or experiment:

```yaml
tags: [3d-vision, nerf, optimization]
```
"""

    (research_root / "tags.md").write_text(tags_content, encoding="utf-8")

    # Create config.yaml
    config = {
        "notion": {
            "enabled": False,
            "token": "",
            "database_id": "",
            "sync_on_change": False,
            "projects_page_id": ""
        },
        "database": {
            "enabled": False,
            "path": ".research-notes.db",
            "auto_backup": True,
            "backup_interval": 3600
        },
        "storage": {
            "symlink_large_files": False,
            "symlink_threshold": 10,  # MB
            "external_storage": ""
        },
        "git": {
            "auto_commit": False,
            "auto_push": False,
            "commit_message_prefix": "[Research Notes]"
        }
    }

    with open(research_root / "config.yaml", 'w', encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

    # Create templates directory
    templates_dir = research_root / "templates"
    templates_dir.mkdir(exist_ok=True)

    # Create experiment template
    experiment_template = """---
title: {title}
idea: {idea}
project: {project}
created: {created}
updated: {updated}
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

    (templates_dir / "experiment-template.md").write_text(experiment_template, encoding="utf-8")

    # Create idea template
    idea_template = """---
title: {title}
project: {project}
created: {created}
updated: {updated}
status: unverified
tags: []
priority: medium
---

## Idea Description

[Describe your idea]

## Hypothesis

[What do you think will happen?]

## Approach

[How will you test this idea?]

## Related Work

[Papers, projects, or previous experiments]

## Next Steps

- [ ] [Next action item]
"""

    (templates_dir / "idea-template.md").write_text(idea_template, encoding="utf-8")

    # Create project template
    project_template = """---
title: {title}
type: {type}
created: {created}
updated: {updated}
status: active
tags: []
priority: medium
---

## Project Overview

[Brief description of this project]

## Goals

1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

## Related Papers

- [Paper Title]
- [Paper Title]

## Timeline

- [ ] [Milestone 1]
- [ ] [Milestone 2]
- [ ] [Milestone 3]
"""

    (templates_dir / "project-template.md").write_text(project_template, encoding="utf-8")

    print("\n✓ Research notes structure created successfully!")
    print(f"\nLocation: {research_root}")
    print("\nNext steps:")
    print("1. Create a project: python3 scripts/create_project.py <title>")
    print("2. Add ideas: python3 scripts/create_idea.py <project> <title>")
    print("3. Create experiments: python3 scripts/create_experiment.py <project> <idea> <title>")
    print("\nOptional:")
    print("- Configure Notion sync: Edit config.yaml")
    print("- Enable database: Edit config.yaml")
    print("- Initialize git: python3 scripts/init_git.py")


if __name__ == "__main__":
    main()
