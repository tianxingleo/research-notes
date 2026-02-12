---
name: research-notes
description: Hierarchical research and idea management system for academic papers, engineering projects, and research workflows. Organize projects, track ideas with validation status, manage experiments, and synchronize with Notion. Use when creating research projects, tracking experiment results, managing paper notes, or organizing engineering research efforts.
---

# Research Notes

## Overview

Research Notes provides a hierarchical organization system for managing research projects, papers, ideas, and experiments. Perfect for academic research (theses, papers), engineering research (prototypes, POCs), and idea tracking with validation states.

## Project Structure

```
research-notes/
├── projects/              # All research projects
│   ├── project-name/      # Project folder (can be paper title, direction, or project name)
│   │   ├── project.md     # Project metadata (created, updated, status, tags)
│   │   ├── ideas/         # Ideas within this project
│   │   │   └── idea-name/
│   │   │       ├── idea.md              # Idea details
│   │   │       ├── validation.md        # Validation status & results
│   │   │       └── experiments/         # Experiments testing this idea
│   │   │           └── experiment-name/
│   │   │               ├── experiment.md
│   │   │               ├── results.md
│   │   │               └── artifacts/   # Code, data, outputs
│   │   ├── papers/      # Papers related to this project
│   │   │   └── paper-title/
│   │   │       ├── paper.md
│   │   │       └── notes.md
│   │   └── engineering/ # Engineering/prototyping work
│   │       └── component-name/
│   │           ├── design.md
│   │           ├── implementation.md
│   │           └── tests.md
├── index.md              # Global project index
├── tags.md              # Tag-based navigation
└── config.yaml           # Configuration (Notion sync, backup options)
```

## Core Concepts

### Project Types

1. **Academic Research** - Papers, theses, conference submissions
2. **Engineering Research** - Prototypes, POCs, experimental features
3. **Direction/Topic** - Broad research areas (e.g., "3D Reconstruction")

### Idea Validation States

- `unverified` - New idea, not yet tested
- `planned` - Planned for validation
- `in-progress` - Currently being tested
- `validated` - Confirmed through experiments
- `rejected` - Proven incorrect or unfeasible
- `on-hold` - Paused, may revisit later

### Metadata

Every file includes front matter with:
- `created`: ISO 8601 timestamp
- `updated`: ISO 8601 timestamp
- `status`: Current state
- `tags`: Array of tags for categorization
- `priority`: Optional priority level (low/medium/high)

## Quick Start

### 1. Initialize Research Notes

```bash
# Run initialization script
python3 scripts/init.py
```

Creates base structure with `index.md` and `config.yaml`.

### 2. Create a New Project

```bash
# Create project with type (academic|engineering|direction)
python3 scripts/create_project.py "3D Neural Rendering" --type academic

# Or create manually in chat:
# "Create a new research project titled 'NeRF Optimization' with type academic"
```

Generated `project.md`:

```markdown
---
title: NeRF Optimization
type: academic
created: 2026-02-12T12:00:00Z
updated: 2026-02-12T12:00:00Z
status: active
tags: [neural-rendering, 3d-vision, deep-learning]
priority: high
---

## Project Overview

[Your project description]

## Goals

1. Optimize NeRF rendering speed by 2x
2. Reduce memory usage to < 4GB
3. Support real-time rendering on consumer hardware

## Related Papers

- Original NeRF paper
- Instant-NGP
- ...
```

### 3. Add an Idea

```bash
# Add idea to project
python3 scripts/create_idea.py "3D Neural Rendering" "Sparse-view reconstruction" --priority high
```

Generated `ideas/sparse-view-reconstruction/idea.md`:

```markdown
---
title: Sparse-view Reconstruction
project: 3D Neural Rendering
created: 2026-02-12T12:05:00Z
updated: 2026-02-12T12:05:00Z
status: planned
tags: [sparse-view, reconstruction, optimization]
priority: high
---

## Idea Description

Use neural networks to reconstruct 3D scenes from sparse camera views.

## Hypothesis

Neural priors can fill in missing information from limited viewpoints.

## Approach

1. Train on synthetic data with varying view counts
2. Evaluate reconstruction quality vs. view count
3. Compare to traditional MVS methods

## Related Work

- [Paper Title]
- [Paper Title]

## Next Steps

- [ ] Create experiment plan
- [ ] Implement baseline
```

### 4. Create Experiment

```bash
# Create experiment for idea
python3 scripts/create_experiment.py "3D Neural Rendering" "Sparse-view Reconstruction" "View Ablation Study"
```

Generated `experiments/view-ablation-study/experiment.md`:

```markdown
---
title: View Ablation Study
idea: Sparse-view Reconstruction
project: 3D Neural Rendering
created: 2026-02-12T12:10:00Z
updated: 2026-02-12T12:10:00Z
status: in-progress
tags: [ablation, evaluation]
---

## Experiment Setup

- Dataset: DTU
- View counts: [3, 5, 10, 20]
- Metrics: PSNR, SSIM, LPIPS
- Baseline: Original NeRF

## Hypothesis

Minimum 5 views needed for acceptable quality (>30dB PSNR).

## Procedure

1. Train models with different view counts
2. Evaluate on test set
3. Compare metrics

## Expected Results

| Views | PSNR (expected) | SSIM (expected) |
|-------|-----------------|-----------------|
| 3     | 25.5            | 0.75            |
| 5     | 30.2            | 0.85            |
| 10    | 32.5            | 0.89            |
| 20    | 33.8            | 0.91            |
```

### 5. Update Validation Status

After experiment completes:

```bash
# Update idea validation status
python3 scripts/update_validation.py "3D Neural Rendering" "Sparse-view Reconstruction" --status validated
```

Updates `validation.md`:

```markdown
---
idea: Sparse-view Reconstruction
status: validated
validated: 2026-02-12T18:00:00Z
---

## Validation Summary

Idea validated through view ablation study.

## Experiments Conducted

1. View Ablation Study (2026-02-12)
   - Result: Minimum 5 views achieved 30.2 dB PSNR
   - Conclusion: Hypothesis confirmed

## Key Findings

- 5 views sufficient for >30 dB quality
- Diminishing returns beyond 10 views
- Suggested threshold: 7-8 views for deployment

## Next Steps

- [ ] Test on real-world data
- [ ] Optimize for 7-view deployment
```

## Commands Reference

### Project Management

```bash
# Create new project
python3 scripts/create_project.py <title> [--type <type>] [--tags <tags>]

# List all projects
python3 scripts/list_projects.py

# Update project metadata
python3 scripts/update_project.py <project-name> [--status <status>]

# Delete project (with confirmation)
python3 scripts/delete_project.py <project-name>
```

### Idea Management

```bash
# Create new idea
python3 scripts/create_idea.py <project> <title> [--priority <priority>] [--tags <tags>]

# List ideas in project
python3 scripts/list_ideas.py <project>

# Update idea status
python3 scripts/update_idea.py <project> <idea> [--status <status>]

# Search ideas by tag
python3 scripts/search_ideas.py --tag <tag>
```

### Experiment Management

```bash
# Create experiment
python3 scripts/create_experiment.py <project> <idea> <title>

# List experiments for idea
python3 scripts/list_experiments.py <project> <idea>

# Update experiment status
python3 scripts/update_experiment.py <project> <idea> <experiment> [--status <status>]

# Record experiment results
python3 scripts/record_results.py <project> <idea> <experiment> <results-file>
```

### Validation Management

```bash
# Update validation status
python3 scripts/update_validation.py <project> <idea> --status <status>

# Get validation summary
python3/scripts/validation_summary.py <project>

# Export validation report
python3/scripts/export_validation.py <project> --format markdown|pdf
```

### Search & Navigation

```bash
# Search across all projects
python3 scripts/search.py <query>

# List by tag
python3 scripts/by_tag.py <tag>

# List by status
python3 scripts/by_status.py <status>  # unverified|planned|in-progress|validated|rejected

# Recent changes (last N days)
python3/scripts/recent.py --days 7
```

## Advanced Features

### Notion Integration

Sync research notes to Notion for team collaboration:

**Setup:**

Edit `config.yaml`:

```yaml
notion:
  enabled: true
  token: "your_notion_integration_token"
  database_id: "your_database_id"
  sync_on_change: true
  projects_page_id: "optional_parent_page"
```

**Sync commands:**

```bash
# Sync all projects to Notion
python3 scripts/notion_sync.py --all

# Sync specific project
python3 scripts/notion_sync.py --project "3D Neural Rendering"

# Sync only changes
python3 scripts/notion_sync.py --incremental
```

**Notion Database Schema:**

Create a database with properties:
- Name (Title)
- Type (Select: Academic/Engineering/Direction)
- Status (Select: Active/On Hold/Completed)
- Tags (Multi-select)
- Created (Date)
- Updated (Date)
- Priority (Select: Low/Medium/High)
- Project Link (Relation to experiments)

### Database Backup

For large datasets, enable SQLite backup:

```yaml
database:
  enabled: true
  path: .research-notes.db
  auto_backup: true
  backup_interval: 3600  # seconds
```

**Query database:**

```bash
# Query with SQL
python3 scripts/query_db.py "SELECT * FROM ideas WHERE status='validated'"

# Export to CSV
python3 scripts/export_db.py --format csv --output ideas.csv
```

### Templates

Use templates for faster creation:

```bash
# List available templates
python3 scripts/templates.py --list

# Create from template
python3 scripts/create_from_template.py --template experiment-template --output my-experiment.md
```

Templates are stored in `templates/`:
- `experiment-template.md` - Standard experiment structure
- `paper-notes-template.md` - Paper reading notes
- `idea-validation-template.md` - Validation checklist

## Data Management

### Large Data Handling

For experiments with large datasets/results:

```yaml
storage:
  # Use symlinks for large files
  symlink_large_files: true
  # Threshold in MB
  symlink_threshold: 10
  # External storage path
  external_storage: /mnt/data/research
```

### Backup & Version Control

**Git integration:**

```bash
# Initialize git repo
python3 scripts/init_git.py

# Auto-commit on changes
python3 scripts/commit_changes.py --message "Update validation results"

# Create release tag
python3 scripts/tag_release.py --tag v1.0 --message "First stable release"
```

**Backup to external location:**

```bash
# Full backup
python3 scripts/backup.py --output /backup/research-notes-$(date +%Y%m%d).tar.gz

# Incremental backup
python3 scripts/backup.py --incremental --output /backup/
```

## Search & Retrieval

### Full-Text Search

```bash
# Search in ideas
python3 scripts/search.py --scope ideas "neural rendering"

# Search in experiments
python3 scripts/search.py --scope experiments "ablation study"

# Search by date range
python3/scripts/search.py --after "2026-02-01" --before "2026-02-15"
```

### Advanced Queries

```bash
# Validated ideas with high priority
python3/scripts/query.py --status validated --priority high

# Experiments in last 30 days
python3/scripts/query.py --type experiment --days 30

# Papers tagged "3d-vision" in academic projects
python3/scripts/query.py --type paper --tag 3d-vision --project-type academic
```

## Collaboration

### Sharing Projects

```bash
# Export project as shareable archive
python3/scripts/export_project.py "3D Neural Rendering" --output shared/

# Import shared project
python3/scripts/import_project.py --from shared/3d-Neural-Rendering.tar.gz
```

### Team Workflows

For shared research projects:

1. **Git repo for collaboration:**
```bash
# Remote setup
python3/scripts/setup_remote.py --origin https://github.com/tianxingleo/research-notes

# Pull changes from team
python3/scripts/pull_changes.py

# Push changes
python3/scripts/push_changes.py --message "Update experiment results"
```

2. **Notion sync for non-technical team:**
   - Enable Notion integration in `config.yaml`
   - Team members can view/edit in Notion
   - Changes sync back to local repo

## Resources

### scripts/

All management scripts are in the `scripts/` directory:

- `init.py` - Initialize research notes structure
- `create_project.py` - Create new project
- `create_idea.py` - Create new idea
- `create_experiment.py` - Create new experiment
- `update_validation.py` - Update validation status
- `search.py` - Full-text search
- `notion_sync.py` - Notion integration
- `query_db.py` - Database queries
- `backup.py` - Backup management
- `templates.py` - Template management

### references/

Additional documentation:
- `workflows.md` - Common research workflows
- `best-practices.md` - Research note best practices
- `notion-setup.md` - Notion integration guide

### templates/

Reusable templates:
- `experiment-template.md`
- `paper-notes-template.md`
- `idea-validation-template.md`

## Best Practices

1. **Consistent Naming:** Use kebab-case for folders/files
2. **Timestamps:** Always update `updated` field on modifications
3. **Tag Strategy:** Use hierarchical tags (e.g., `3d-vision:nerf`)
4. **Validation:** Always update validation status after experiments
5. **Documentation:** Document null results and failed experiments
6. **Regular Sync:** Commit/push changes regularly, especially after validations
7. **Backup:** Enable database backup for large-scale research

## Common Workflows

### Paper Reading Workflow

1. Create project for paper: `create_project.py "Paper Title" --type academic`
2. Read paper: `papers/paper-title/notes.md`
3. Extract ideas: `create_idea.py "Paper Title" "Idea from paper"`
4. Plan experiments: `create_experiment.py ...`
5. Validate and update: `update_validation.py ...`

### Engineering Research Workflow

1. Create project: `create_project.py "Component Name" --type engineering`
2. Design phase: `engineering/component/design.md`
3. Implementation: `engineering/component/implementation.md`
4. Testing: `engineering/component/tests.md`
5. Iterate: Create ideas for improvements

### Literature Review Workflow

1. Create direction project: `create_project.py "3D Reconstruction" --type direction`
2. Add papers: `papers/paper-1/`, `papers/paper-2/`, etc.
3. Extract common ideas: Link ideas across papers
4. Identify research gaps: Create ideas for future work
