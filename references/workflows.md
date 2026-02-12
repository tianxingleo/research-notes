# Research Workflows

This document provides common workflows for research projects using research-notes.

## Paper Reading Workflow

1. **Create project for paper**
   ```bash
   python3 scripts/create_project.py "Paper Title" --type academic
   ```

2. **Read and annotate**
   - Open `projects/paper-title/papers/` (create if needed)
   - Add paper PDF
   - Create `notes.md` with key insights

3. **Extract ideas**
   ```bash
   python3 scripts/create_idea.py "Paper Title" "Idea from paper" --priority high
   ```

4. **Plan experiments**
   ```bash
   python3 scripts/create_experiment.py "Paper Title" "Idea from paper" "Experiment Name"
   ```

5. **Run experiments and validate**
   - Fill in `results.md`
   - Update validation status
   ```bash
   python3 scripts/update_validation.py "Paper Title" "Idea from paper" --status validated
   ```

## Engineering Research Workflow

1. **Create project**
   ```bash
   python3 scripts/create_project.py "Component Name" --type engineering
   ```

2. **Design phase**
   - Edit `engineering/component-name/design.md`
   - Document architecture and algorithms

3. **Implementation**
   - Edit `engineering/component-name/implementation.md`
   - Track code and progress

4. **Testing**
   - Edit `engineering/component-name/tests.md`
   - Document test cases and results

5. **Iterate**
   - Create ideas for improvements
   - Run experiments to validate
   - Update validation status

## Literature Review Workflow

1. **Create direction project**
   ```bash
   python3 scripts/create_project.py "3D Reconstruction" --type direction
   ```

2. **Add papers**
   - Create `papers/paper-1/`, `papers/paper-2/`, etc.
   - Add reading notes for each

3. **Extract common ideas**
   - Identify recurring themes across papers
   - Create ideas linking to multiple papers

4. **Identify research gaps**
   - Create ideas for future work
   - Mark as `planned` status

5. **Track progress**
   - Use `list_projects.py` to review all projects
   - Use `search.py` to find related work

## Idea Validation Workflow

1. **Create idea**
   ```bash
   python3 scripts/create_idea.py "Project Name" "Idea Title" --priority high
   ```

2. **Design experiment**
   ```bash
   python3 scripts/create_experiment.py "Project Name" "Idea Title" "Experiment Name"
   ```
   - Fill in setup, hypothesis, procedure
   - Define expected results

3. **Run experiment**
   - Execute the experiment
   - Collect data and metrics
   - Fill in `results.md`

4. **Analyze results**
   - Compare to expectations
   - Document conclusions in `experiment.md`

5. **Update validation**
   ```bash
   python3 scripts/update_validation.py "Project Name" "Idea Title" --status validated
   ```
   - Or: `--status rejected` if hypothesis wrong
   - Update `validation.md` with key findings

6. **Iterate**
   - Create new ideas based on findings
   - Continue experimentation cycle

## Quick Reference

### Command Summary

```bash
# Initialize research notes
python3 scripts/init.py

# Create project
python3 scripts/create_project.py <title> [--type <type>] [--tags <tags>]

# Create idea
python3 scripts/create_idea.py <project> <title> [--priority <priority>] [--tags <tags>]

# Create experiment
python3 scripts/create_experiment.py <project> <idea> <title>

# Update validation
python3 scripts/update_validation.py <project> <idea> --status <status>

# List projects
python3 scripts/list_projects.py

# Search
python3 scripts/search.py <query> [--scope <scope>]
```

### Status Values

**Projects:** active, on-hold, completed

**Ideas:** unverified, planned, in-progress, validated, rejected, on-hold

**Experiments:** planned, in-progress, completed, failed

### Project Types

- `academic` - Academic research (papers, theses)
- `engineering` - Engineering projects (prototypes, implementations)
- `direction` - Broad research areas
