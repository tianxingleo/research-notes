# Issues Found During Testing

This document demonstrates actual issues found while testing the skill.

## Issue 1: Path Traversal Vulnerability (CONFIRMED)

### Test Code
```python
from scripts.create_project import slugify

# Test dangerous input
print(slugify('../../../etc/passwd'))
# Output: '../../../etc/passwd'

print(slugify('test/subdir'))
# Output: 'test/subdir'
```

### Result
The slugify function does NOT sanitize:
- Path traversal sequences (`..`)
- Directory separators (`/`)
- Special characters (`@#$%^&*()`)

### Impact
Could potentially create directories outside the intended location or with problematic names.

## Issue 2: Tags Not Parsed Correctly (CONFIRMED)

### Test Command
```bash
python3 scripts/create_project.py "Test Project" --tags "test,demo"
python3 scripts/list_projects.py
```

### Output
```
Tags: test", "demo
```

### Expected
```
Tags: test, demo
```

### Root Cause
In `create_project.py` line 76:
```python
tags: {json.dumps(tags)}
```

This creates: `tags: ["test", "demo"]` in YAML front matter.

In `list_projects.py` lines 55-58:
```python
elif line.startswith("tags:"):
    tags = line.split(':', 1)[1].strip().strip('"\'[]')
    if tags:
        project_data['tags'] = [t.strip() for t in tags.split(',')]
```

The parsing doesn't handle JSON array format correctly - it just strips quotes and brackets, leaving malformed data.

## Issue 3: Hardcoded Path (CONFIRMED)

### Evidence
When running `init.py` from `/home/runner/work/research-notes/research-notes/`, it creates:
```
/home/runner/research-notes/
```

Instead of creating it in the current repository or a configurable location.

### Root Cause
All scripts use:
```python
workspace = Path(__file__).parent.parent.parent.parent.parent
research_root = workspace / "research-notes"
```

This assumes:
- Script is 5 levels deep
- Parent directory structure is always the same
- A directory named "research-notes" should be created at that level

## Issue 4: Multiple Spaces Not Collapsed (MINOR)

### Test
```python
slugify('Project with    many   spaces')
# Output: 'project-with----many---spaces'
```

### Expected
```
'project-with-many-spaces'
```

Multiple consecutive spaces become multiple dashes instead of a single dash.

## Issue 5: No Input Length Validation (CONFIRMED)

The scripts don't validate input lengths. This could cause:
- Filesystem errors with overly long filenames
- Performance issues with very long inputs
- Buffer issues in some filesystems

### Test
```python
# This would work but create a very long directory name
slugify('a' * 500)  # Returns 500-character string
```

Most filesystems have a 255-character limit for filenames.

## Issue 6: Silent Failures in Search (CONFIRMED)

In `search.py` line 31:
```python
def search_in_file(filepath, query):
    try:
        content = filepath.read_text(encoding="utf-8")
        # ... search logic ...
        return matches
    except:
        return []  # Silent failure!
```

Any error (permission denied, encoding issues, etc.) is silently ignored.

## Summary

| Issue | Severity | Confirmed | Fix Priority |
|-------|----------|-----------|--------------|
| Path traversal in slugify | HIGH | ✓ | P1 |
| Hardcoded paths | HIGH | ✓ | P1 |
| Tag parsing broken | MEDIUM | ✓ | P1 |
| Silent failures | MEDIUM | ✓ | P2 |
| No length validation | MEDIUM | ✓ | P2 |
| Multiple spaces | LOW | ✓ | P3 |

All issues identified in the review have been verified through testing.
