#!/usr/bin/env python3
"""
Export validation report.

Usage:
    python3 export_validation.py <project> [--format <format>]
"""

import sys
from pathlib import Path
from datetime import datetime


def parse_iso_date(date_str):
    """Parse ISO 8601 date string."""
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 export_validation.py <project> [--format <format>]")
        print("\nFormats: markdown (default), pdf")
        sys.exit(1)

    project_name = sys.argv[1]

    # Parse optional arguments
    format_type = "markdown"  # default
    for i, arg in enumerate(sys.argv):
        if arg == "--format" and i + 1 < len(sys.argv):
            format_type = sys.argv[i + 1].lower()

    if format_type not in ["markdown", "pdf"]:
        print(f"Error: Invalid format '{format_type}'. Valid formats: markdown, pdf")
        sys.exit(1)

    # Get paths
    workspace = Path(__file__).parent.parent.parent.parent.parent
    research_root = workspace / "research-notes"
    projects_dir = research_root / "projects"

    # Find project directory
    project_dir = None
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
            break

    if not project_dir:
        print(f"Error: Project '{project_name}' not found")
        sys.exit(1)

    # Generate report
    project_md = project_dir / "project.md"
    project_content = project_md.read_text(encoding="utf-8")

    # Parse project metadata
    project_title = None
    project_type = None

    for line in project_content.split('\n'):
        if line.startswith("title:"):
            project_title = line.split(':', 1)[1].strip().strip('"\'')
        elif line.startswith("type:"):
            project_type = line.split(':', 1)[1].strip().strip('"\'')

    # Collect all ideas
    ideas_dir = project_dir / "ideas"
    if not ideas_dir.exists():
        print(f"Error: No ideas found in project '{project_name}'")
        sys.exit(1)

    report_lines = []

    # Header
    report_lines.append(f"# Validation Report")
    report_lines.append(f"\n**Project:** {project_title}")
    report_lines.append(f"**Type:** {project_type}")
    report_lines.append(f"**Generated:** {datetime.now().isoformat()}")
    report_lines.append("\n---\n")

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

        idea_content = idea_md.read_text(encoding="utf-8")

        # Parse idea metadata
        idea_title = None
        idea_status = None
        idea_priority = None
        idea_updated = None

        for line in idea_content.split('\n'):
            if line.startswith("title:"):
                idea_title = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("status:"):
                idea_status = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("priority:"):
                idea_priority = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("updated:"):
                idea_updated = parse_iso_date(line.split(':', 1)[1].strip().strip('"\'')

        if not idea_title:
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
    report_lines.append(f"\n| Metric | Count |")
    report_lines.append(f"|--------|-------|")
    report_lines.append(f"| Total Ideas | {total_ideas} |")
    report_lines.append(f"| Validated | {validated_count} |")
    report_lines.append(f"| Rejected | {rejected_count} |")
    report_lines.append(f"| In Progress | {in_progress_count} |")
    report_lines.append(f"| Planned | {planned_count} |")

    # Validation rate
    if total_ideas > 0:
        validation_rate = (validated_count / total_ideas) * 100
        report_lines.append(f"| Validation Rate | {validation_rate:.1f}% |")

    report_lines.append("\n---\n")

    # Detailed sections by status
    for idea_dir in sorted(ideas_dir.iterdir()):
        if not idea_dir.is_dir():
            continue

        idea_md = idea_dir / "idea.md"
        validation_md = idea_dir / "validation.md"

        if not idea_md.exists() or not validation_md.exists():
            continue

        idea_content = idea_md.read_text(encoding="utf-8")
        validation_content = validation_md.read_text(encoding="utf-8")

        # Parse idea metadata
        idea_title = None
        idea_status = None
        idea_priority = None
        idea_updated = None

        for line in idea_content.split('\n'):
            if line.startswith("title:"):
                idea_title = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("status:"):
                idea_status = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("priority:"):
                idea_priority = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith("updated:"):
                idea_updated = parse_iso_date(line.split(':', 1)[1].strip().strip('"\'')

        if not idea_title:
            continue

        # Add to report
        report_lines.append(f"## {idea_title}")
        report_lines.append(f"\n**Status:** {idea_status}")
        report_lines.append(f"**Priority:** {idea_priority}")
        if idea_updated:
            report_lines.append(f"**Last Updated:** {idea_updated.strftime('%Y-%m-%d')}")
        report_lines.append(f"**Location:** `ideas/{idea_dir.name}/`")

        # Count experiments
        experiments_dir = idea_dir / "experiments"
        if experiments_dir.exists():
            exp_count = sum(1 for e in experiments_dir.iterdir() if e.is_dir())
            report_lines.append(f"**Experiments:** {exp_count}")

        report_lines.append("\n### Validation Summary")

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

        report_lines.append("\n---\n")

    # Write report
    report_text = "\n".join(report_lines)

    if format_type == "markdown":
        output_file = research_root / f"validation-report-{project_name.lower().replace(' ', '-')}.md"
        output_file.write_text(report_text, encoding="utf-8")
        print(f"\n✓ Validation report exported to Markdown")
        print(f"  Output: {output_file}")
    elif format_type == "pdf":
        # For PDF, we'd need a library like markdown2pdf or similar
        # For now, export as markdown with instructions
        output_file = research_root / f"validation-report-{project_name.lower().replace(' ', '-')}.md"
        output_file.write_text(report_text, encoding="utf-8")
        print(f"\n⚠️  PDF export requires additional dependencies")
        print(f"  Markdown report exported: {output_file}")
        print(f"\n  To convert to PDF, use:")
        print(f"    1. pandoc: pandoc {output_file} -o output.pdf")
        print(f"    2. Markdown-to-PDF tools (browser extension, etc.)")
        print(f"    3. Install markdown2pdf: pip install markdown2pdf")


if __name__ == "__main__":
    main()
