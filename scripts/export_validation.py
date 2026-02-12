#!/usr/bin/env python3
"""
Export validation report.

Usage:
    python3 export_validation.py <project>
"""

import sys
from utils import *
from pathlib import Path
from datetime import datetime


def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python3 export_validation.py <project>")
            print("Exports validation report to Markdown")
            sys.exit(1)

        project_name = sys.argv[1]

        # Get research root directory
        research_root = get_research_root()
        projects_dir = research_root / "projects"

        if not projects_dir.exists():
            print(format_error_with_suggestions(
                "No projects directory found",
                [
                    "Run init.py to initialize the research notes directory",
                    "Create a project first"
                ]
            ))
            sys.exit(1)

        # Find project directory using utils function
        project_dir = find_project_by_title(projects_dir, project_name)

        if project_dir is None:
            print(format_error_with_suggestions(
                f"Project '{project_name}' not found",
                [
                    "Check the project name spelling",
                    "Use list_projects.py to see all projects"
                ]
            ))
            sys.exit(1)

        # Generate report
        project_md = project_dir / "project.md"
        project_content = project_md.read_text(encoding="utf-8")

        # Parse project metadata
        project_data = parse_frontmatter(project_content)
        project_title = project_data.get('title', 'Unknown')
        project_type = project_data.get('type', 'Unknown')

        # Collect all ideas
        ideas_dir = project_dir / "ideas"
        if not ideas_dir.exists():
            print(format_error_with_suggestions(
                f"No ideas found in project '{project_name}'",
                [
                    "Create ideas using scripts/create_idea.py",
                    "The project may be empty"
                ]
            ))
            sys.exit(1)

        report_lines = []

        # Header
        report_lines.append("# Validation Report")
        report_lines.append(f"**Project:** {project_title}")
        report_lines.append(f"**Type:** {project_type}")
        report_lines.append(f"**Generated:** {datetime.now().isoformat()}")
        report_lines.append("---")

        # Statistics
        total_ideas = 0
        validated_count = 0
        rejected_count = 0
        in_progress_count = 0
        planned_count = 0

        # Process each idea
        for idea_dir in ideas_dir.iterdir():
            if not idea_dir.is_dir():
                continue

            idea_md = idea_dir / "idea.md"
            if not idea_md.exists():
                continue

            try:
                idea_content = idea_md.read_text(encoding="utf-8")
                idea_data = parse_frontmatter(idea_content)
                idea_title = idea_data.get('title')
                idea_status = idea_data.get('status')
            except Exception as e:
                print(f"Warning: Failed to read {idea_md}: {e}")
                continue

            if idea_title is None:
                continue

            total_ideas += 1

            if idea_status == "validated":
                validated_count += 1
            elif idea_status == "rejected":
                rejected_count += 1
            elif idea_status == "in-progress":
                in_progress_count += 1
            elif idea_status == "planned":
                planned_count += 1

        # Statistics section
        report_lines.append("## Summary")
        report_lines.append("| Metric | Count |")
        report_lines.append("|--------|-------|")
        report_lines.append(f"| Total Ideas | {total_ideas} |")
        report_lines.append(f"| Validated | {validated_count} |")
        report_lines.append(f"| Rejected | {rejected_count} |")
        report_lines.append(f"| In Progress | {in_progress_count} |")
        report_lines.append(f"| Planned | {planned_count} |")

        # Validation rate
        if total_ideas > 0:
            validation_rate = (validated_count / total_ideas) * 100
            report_lines.append(f"| Validation Rate | {validation_rate:.1f}% |")

        report_lines.append("---")

        # Detailed sections
        for idea_dir in sorted(ideas_dir.iterdir()):
            if not idea_dir.is_dir():
                continue

            idea_md = idea_dir / "idea.md"
            validation_md = idea_dir / "validation.md"

            if not idea_md.exists() or not validation_md.exists():
                continue

            try:
                idea_content = idea_md.read_text(encoding="utf-8")
                validation_content = validation_md.read_text(encoding="utf-8")
            except Exception as e:
                print(f"Warning: Failed to read idea files: {e}")
                continue

            # Parse idea metadata
            idea_data = parse_frontmatter(idea_content)
            idea_title = idea_data.get('title')
            idea_status = idea_data.get('status')

            if idea_title is None:
                continue

            # Add to report
            report_lines.append(f"## {idea_title}")
            report_lines.append(f"**Status:** {idea_status}")
            report_lines.append(f"**Location:** `ideas/{idea_dir.name}/`")

            # Count experiments
            experiments_dir = idea_dir / "experiments"
            if experiments_dir.exists():
                exp_count = sum(1 for e in experiments_dir.iterdir() if e.is_dir())
                report_lines.append(f"**Experiments:** {exp_count}")

            report_lines.append("### Validation Summary")

            # Extract validation summary
            in_summary = False
            for line in validation_content.split('\n'):
                if line.startswith("## Validation Summary"):
                    in_summary = True
                    continue
                if in_summary:
                    if line.startswith("##"):
                        break
                    report_lines.append(line)

            report_lines.append("---")

        # Write report
        report_text = "\n".join(report_lines)
        output_file = research_root / f"validation-report-{slugify(project_name)}.md"
        output_file.write_text(report_text, encoding="utf-8")

        print(f"✓ Validation report exported to Markdown")
        print(f"Output: {output_file}")

    except RuntimeError as e:
        print(format_error_with_suggestions(
            str(e),
            [
                "Set RESEARCH_NOTES_ROOT environment variable",
                "Run init.py from the research-notes directory"
            ]
        ))
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
