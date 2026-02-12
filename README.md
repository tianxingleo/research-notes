# Research Notes Skill

Hierarchical research and idea management system for academic papers, engineering projects, and research workflows.

## Features

- **Project-based organization** - Papers, engineering projects, research directions
- **Idea tracking** - With validation states (unverified, planned, in-progress, validated, rejected)
- **Experiment management** - Track hypotheses, procedures, results
- **Markdown-based** - Human-readable, version-controlled
- **Searchable** - Full-text search across all notes
- **Notion integration** - Optional sync for collaboration
- **Git-friendly** - Version control for your research

## Quick Start

```bash
# Initialize research notes structure
python3 scripts/init.py

# Create a project
python3 scripts/create_project.py "3D Neural Rendering" --type academic --tags "3d-vision,nerf"

# Add an idea
python3 scripts/create_idea.py "3D Neural Rendering" "Sparse-view Reconstruction" --priority high

# Create an experiment
python3 scripts/create_experiment.py "3D Neural Rendering" "Sparse-view Reconstruction" "View Ablation Study"

# Update validation
python3 scripts/update_validation.py "3D Neural Rendering" "Sparse-view Reconstruction" --status validated

# Search
python3 scripts/search.py "neural rendering"
```

## Project Structure

```
research-notes/
├── projects/              # All research projects
│   └── project-name/
│       ├── project.md     # Project metadata
│       ├── ideas/         # Ideas within project
│       │   └── idea-name/
│       │       ├── idea.md
│       │       ├── validation.md
│       │       └── experiments/
│       ├── papers/        # Papers
│       └── engineering/  # Engineering work
├── scripts/              # Management scripts
├── references/           # Documentation
└── config.yaml           # Configuration
```

## Documentation

See [SKILL.md](SKILL.md) for complete documentation.

## License

MIT License
