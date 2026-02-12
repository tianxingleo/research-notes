# Skill Review: Research Notes

## Review Date
2026-02-12

## Executive Summary

The Research Notes skill is a well-designed hierarchical research and idea management system for academic and engineering projects. The skill demonstrates **solid architecture** with clear organization and good documentation. However, there are several areas where improvements would enhance usability, robustness, and maintainability.

**Overall Rating: 7.5/10**

## Strengths

### 1. Excellent Documentation (9/10)
- **Comprehensive README**: Clear, well-structured with examples
- **Detailed SKILL.md**: 580 lines of thorough documentation covering all features
- **Workflow Guide**: Practical workflows for different use cases
- **Consistent Formatting**: Good use of code blocks, examples, and organization

### 2. Well-Designed Architecture (8/10)
- **Clear Hierarchy**: Project → Ideas → Experiments structure is logical
- **Markdown-Based**: Human-readable, version-control friendly
- **Metadata-Driven**: Consistent YAML front matter across all documents
- **Validation States**: Well-defined idea validation lifecycle (unverified → planned → in-progress → validated/rejected)
- **Template System**: Pre-built templates for rapid creation

### 3. Feature-Rich (8/10)
- Project management with types (academic, engineering, direction)
- Idea tracking with priority levels
- Experiment management with artifacts
- Search functionality across all content
- Notion integration (basic)
- Git-friendly design

### 4. Consistent Code Style (7/10)
- All scripts follow similar patterns
- Good use of helper functions (slugify)
- Reasonable error handling
- UTF-8 encoding consistently specified

## Weaknesses & Issues

### 1. Critical Issues (Must Fix)

#### 1.1 Hardcoded Path Assumptions (CRITICAL)
**Severity: HIGH**

All scripts use this problematic path calculation:
```python
workspace = Path(__file__).parent.parent.parent.parent.parent
research_root = workspace / "research-notes"
```

**Problems:**
- Assumes scripts are always 5 levels deep in directory structure
- Breaks if script location changes
- Not portable across different installations
- Assumes `research-notes` directory exists in a specific location

**Impact:** Scripts will fail if:
- Cloned to different directory name
- Scripts are run from different locations
- Used as a library or installed package

**Recommended Fix:**
```python
# Option 1: Environment variable
research_root = Path(os.getenv('RESEARCH_NOTES_ROOT', Path.home() / 'research-notes'))

# Option 2: Config file
config_file = Path(__file__).parent.parent / 'config.yaml'
# Store research_root in config

# Option 3: Search upward for marker file
def find_research_root():
    current = Path(__file__).parent
    while current != current.parent:
        if (current / 'config.yaml').exists():
            return current
        current = current.parent
    raise RuntimeError("Research notes root not found")
```

#### 1.2 Poor Error Messages (HIGH)
**Examples:**
- `"Error: Project 'X' not found"` - doesn't list available projects
- No indication of what went wrong when parsing fails
- Silent failures in search functionality (`except: return []`)

**Recommended Fix:**
- Always suggest next actions in error messages
- List available options when selection fails
- Use proper exception handling with meaningful messages

#### 1.3 Inefficient File Searching (MEDIUM)
**Problem:**
- Linear search through all directories
- Re-reads project titles multiple times
- No caching or indexing

**Impact:**
- Slow with many projects (>50)
- Redundant I/O operations

**Recommended Fix:**
- Build an index on initialization
- Cache project/idea mappings
- Use SQLite as mentioned in docs (currently not implemented)

### 2. Code Quality Issues

#### 2.1 Repeated Code (Medium Priority)
**Problem:** Project/idea lookup code is duplicated in:
- `create_idea.py`
- `create_experiment.py`
- `update_validation.py`

**Lines of duplication:** ~40 lines per file

**Recommended Fix:**
```python
# Create shared module: scripts/utils.py
def find_project(projects_dir, project_name):
    """Find project directory by name."""
    # Shared implementation
    
def find_idea(project_dir, idea_title):
    """Find idea directory by title."""
    # Shared implementation
```

#### 2.2 Inconsistent Front Matter Parsing (Medium)
**Problem:** Manual line-by-line parsing instead of using YAML parser

Current approach:
```python
for line in content.split('\n'):
    if line.startswith("title:"):
        project_title = line.split(':', 1)[1].strip().strip('"\'')
```

**Issues:**
- Fragile (breaks with multi-line values)
- Inconsistent with YAML spec
- Already imports `yaml` module but doesn't use it

**Recommended Fix:**
```python
import yaml

def parse_frontmatter(content):
    """Extract YAML front matter from markdown."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1])
    return {}
```

#### 2.3 No Input Validation (Medium)
**Missing validations:**
- Title length limits
- Special character handling in slugify
- Tag format validation
- Date format validation

**Potential issues:**
- Very long titles create filesystem issues
- Special characters break file paths
- Invalid dates cause parsing errors

#### 2.4 Incomplete Features (Medium)
**Documented but not implemented:**
1. Database backup (config exists, no implementation)
2. Git integration scripts (`init_git.py`, `commit_changes.py` not found)
3. Most advanced features in SKILL.md:
   - `query_db.py`
   - `export_validation.py`
   - `templates.py`
   - `backup.py`
   - Advanced search features

**Impact:** User expects features that don't work

### 3. Design Issues

#### 3.1 Notion Integration Incomplete (Low Priority)
- Script exists but only prints instructions
- No actual sync implementation
- Config structure exists but unused

#### 3.2 No Tests (Medium Priority)
- No unit tests
- No integration tests
- No CI/CD setup
- High risk of regressions

#### 3.3 Limited Search (Medium Priority)
**Current limitations:**
- Case-insensitive only
- No regex support
- No fuzzy matching
- Only shows first 3 matches
- Doesn't search in papers or engineering sections

### 4. Security Considerations

#### 4.1 Path Traversal Risk (LOW-MEDIUM)
**Issue:** User input used directly in file paths
```python
project_slug = slugify(title)
project_dir = projects_dir / project_slug
```

If `slugify()` doesn't properly sanitize, could create files outside intended directory.

**Current `slugify()`:**
```python
def slugify(text):
    return text.lower().replace(' ', '-').replace('_', '-')
```

**Missing sanitization:**
- Doesn't handle `..`
- Doesn't handle `/` or `\`
- Doesn't handle absolute paths

**Recommended Fix:**
```python
import re

def slugify(text):
    """Convert text to safe slug."""
    # Remove or replace dangerous characters
    text = re.sub(r'[^\w\s-]', '', text)
    text = text.strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    # Prevent path traversal
    text = text.replace('..', '')
    return text[:100]  # Limit length
```

#### 4.2 YAML Injection Risk (LOW)
Using `yaml.safe_load()` is good, but `yaml.dump()` without proper escaping could be problematic with user input containing YAML special characters.

## Detailed Recommendations

### Priority 1: Fix Critical Path Issue
1. Remove hardcoded path assumptions
2. Use environment variable or config file
3. Add path discovery logic
4. Update all 8 scripts

### Priority 2: Code Quality Improvements
1. Extract common functions to `utils.py`
2. Use proper YAML parsing for front matter
3. Add input validation
4. Improve error messages

### Priority 3: Implement Missing Features OR Update Documentation
Either:
- Implement the documented features, OR
- Remove documentation for unimplemented features
- Mark features as "planned" if not yet implemented

### Priority 4: Add Tests
1. Create `tests/` directory
2. Add unit tests for core functions
3. Add integration tests for workflows
4. Add CI with GitHub Actions

### Priority 5: Enhance Security
1. Improve `slugify()` function
2. Add path validation
3. Limit input lengths
4. Sanitize all user inputs

## Specific Code Improvements

### Example 1: Better Error Handling in `create_idea.py`

**Before:**
```python
if not project_dir:
    print(f"Error: Project '{project_name}' not found")
    print(f"Available projects: {[p.name for p in projects_dir.iterdir() if p.is_dir()]}")
    sys.exit(1)
```

**After:**
```python
if not project_dir:
    available = []
    for p in projects_dir.iterdir():
        if p.is_dir() and (p / "project.md").exists():
            meta = parse_frontmatter((p / "project.md").read_text())
            available.append(meta.get('title', p.name))
    
    print(f"Error: Project '{project_name}' not found\n")
    if available:
        print("Available projects:")
        for proj in available:
            print(f"  - {proj}")
    else:
        print("No projects found. Create one with:")
        print(f"  python3 scripts/create_project.py 'My Project'")
    sys.exit(1)
```

### Example 2: Shared Utilities

**Create `scripts/utils.py`:**
```python
"""Shared utilities for research notes."""

import re
import yaml
from pathlib import Path


def slugify(text, max_length=100):
    """Convert text to filesystem-safe slug."""
    # Remove dangerous characters
    text = re.sub(r'[^\w\s-]', '', text)
    text = text.strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    # Prevent path traversal
    text = text.replace('..', '')
    return text[:max_length]


def parse_frontmatter(content):
    """Extract YAML front matter from markdown."""
    if not content.startswith('---'):
        return {}
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}
    
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def find_project_by_title(projects_dir, title):
    """Find project directory by title."""
    title_lower = title.lower()
    
    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue
            
        project_md = project_dir / "project.md"
        if not project_md.exists():
            continue
        
        meta = parse_frontmatter(project_md.read_text(encoding='utf-8'))
        if meta.get('title', '').lower() == title_lower:
            return project_dir
    
    return None


def find_idea_by_title(project_dir, title):
    """Find idea directory by title."""
    ideas_dir = project_dir / "ideas"
    if not ideas_dir.exists():
        return None
    
    title_lower = title.lower()
    
    for idea_dir in ideas_dir.iterdir():
        if not idea_dir.is_dir():
            continue
        
        idea_md = idea_dir / "idea.md"
        if not idea_md.exists():
            continue
        
        meta = parse_frontmatter(idea_md.read_text(encoding='utf-8'))
        if meta.get('title', '').lower() == title_lower:
            return idea_dir
    
    return None
```

## Testing Recommendations

### Unit Tests Structure
```
tests/
├── test_utils.py           # Test utility functions
├── test_create_project.py  # Test project creation
├── test_create_idea.py     # Test idea creation
├── test_search.py          # Test search functionality
└── fixtures/               # Test data
    └── sample_project/
```

### Example Test
```python
# tests/test_utils.py
import pytest
from scripts.utils import slugify, parse_frontmatter

def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"

def test_slugify_special_chars():
    assert slugify("Test/Project: V1.0") == "testproject-v10"

def test_slugify_path_traversal():
    assert ".." not in slugify("../../../etc/passwd")

def test_parse_frontmatter():
    content = """---
title: Test
status: active
---
# Content here"""
    meta = parse_frontmatter(content)
    assert meta['title'] == 'Test'
    assert meta['status'] == 'active'
```

## Documentation Improvements

### 1. Add Troubleshooting Section
```markdown
## Troubleshooting

### "Project not found" error
- Run `python3 scripts/list_projects.py` to see available projects
- Check that project name matches exactly (case-insensitive)

### "Permission denied" error
- Check file permissions on research-notes directory
- Ensure you have write access

### Scripts not working
- Ensure you're running from the repository root
- Check that Python 3.6+ is installed
- Install dependencies: pip install pyyaml
```

### 2. Add Installation Section
```markdown
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tianxingleo/research-notes.git
   cd research-notes
   ```

2. Install dependencies:
   ```bash
   pip install pyyaml
   # Optional: pip install notion-client
   ```

3. Initialize research notes:
   ```bash
   python3 scripts/init.py
   ```
```

### 3. Add Requirements File
Create `requirements.txt`:
```
pyyaml>=6.0
notion-client>=2.0.0  # optional
```

## Performance Recommendations

### 1. Add Caching
```python
# scripts/cache.py
import json
from pathlib import Path
from datetime import datetime

class ProjectCache:
    def __init__(self, cache_file='.research-notes-cache.json'):
        self.cache_file = Path(cache_file)
        self.cache = self._load()
    
    def _load(self):
        if self.cache_file.exists():
            return json.loads(self.cache_file.read_text())
        return {}
    
    def _save(self):
        self.cache_file.write_text(json.dumps(self.cache, indent=2))
    
    def invalidate(self):
        self.cache = {}
        self._save()
    
    def get_projects(self):
        # Return cached project list
        pass
```

### 2. Use Database (As Documented)
Implement the SQLite backend mentioned in documentation:
```python
# scripts/db.py
import sqlite3

class ResearchDB:
    def __init__(self, db_path='.research-notes.db'):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()
    
    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                type TEXT,
                status TEXT,
                created TEXT,
                updated TEXT
            )
        """)
        # Add more tables...
```

## Conclusion

### What's Good
The Research Notes skill has a **solid foundation** with:
- Clear, logical structure
- Excellent documentation
- Good feature design
- Practical workflows

### What Needs Work
Main issues to address:
1. **Portability**: Fix hardcoded paths (CRITICAL)
2. **Code Quality**: Reduce duplication, improve parsing
3. **Completeness**: Implement or document missing features
4. **Robustness**: Add tests and validation
5. **Security**: Improve input sanitization

### Recommended Action Plan

**Phase 1 (1-2 days):**
- Fix path assumptions
- Extract common utilities
- Improve error messages

**Phase 2 (2-3 days):**
- Add input validation
- Improve security
- Add basic tests

**Phase 3 (3-5 days):**
- Implement missing features OR clean up documentation
- Add comprehensive tests
- Performance optimizations

**Total Estimated Effort:** 1-2 weeks for comprehensive improvements

### Final Rating Breakdown
- Documentation: 9/10
- Architecture: 8/10
- Code Quality: 6/10
- Features: 7/10
- Security: 6/10
- Tests: 2/10 (minimal)
- **Overall: 7.5/10**

With the recommended improvements, this could easily become a **9/10** skill suitable for production use in research environments.
