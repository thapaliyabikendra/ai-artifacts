#!/usr/bin/env python3
"""
Enhanced validation script for skills with quality checks.

Usage:
    python quick_validate.py <skill_directory>
    python quick_validate.py <skill_directory> --strict    # Include quality warnings
    python quick_validate.py <skill_directory> --verbose   # Show all checks
"""

import sys
import re
from pathlib import Path

# Handle yaml import gracefully
try:
    import yaml
except ImportError:
    yaml = None

# Quality thresholds
MAX_SKILL_MD_LINES = 500
MIN_DESCRIPTION_LENGTH = 50
TRIGGER_KEYWORDS = ['use when', 'triggers', 'use for', 'use this', 'invoke when', 'activate when']


def count_lines(file_path):
    """Count lines in a file."""
    return len(file_path.read_text().splitlines())


def check_todo_placeholders(content):
    """Check for remaining TODO placeholders."""
    todo_patterns = [
        r'\[TODO:',
        r'\[TODO\]',
        r'TODO:',
        r'\[Replace with',
        r'\[Add content',
    ]
    for pattern in todo_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False


def check_referenced_files_exist(skill_path, content):
    """Check that files referenced in SKILL.md actually exist."""
    missing = []
    # Match markdown links like [text](path) and references like `path/file.md`
    link_pattern = r'\]\(([^)]+\.(?:md|py|sh|txt|json))\)'
    ref_pattern = r'`((?:scripts|references|assets)/[^`]+)`'

    for pattern in [link_pattern, ref_pattern]:
        matches = re.findall(pattern, content)
        for match in matches:
            # Handle relative paths
            ref_path = skill_path / match
            if not ref_path.exists():
                missing.append(match)

    return missing


def validate_skill(skill_path, strict=False, verbose=False):
    """
    Validate a skill with optional strict quality checks.

    Returns:
        (valid: bool, message: str, warnings: list)
    """
    skill_path = Path(skill_path)
    warnings = []

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found", warnings

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found", warnings

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format", warnings

    frontmatter_text = match.group(1)
    body_content = content[match.end():]

    # Parse YAML frontmatter
    if yaml is None:
        # Fallback: basic parsing without yaml library
        frontmatter = {}
        for line in frontmatter_text.strip().split('\n'):
            if ':' in line:
                key, _, value = line.partition(':')
                key = key.strip()
                value = value.strip()
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                frontmatter[key] = value
    else:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return False, "Frontmatter must be a YAML dictionary", warnings
        except yaml.YAMLError as e:
            return False, f"Invalid YAML in frontmatter: {e}", warnings

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        ), warnings

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter", warnings
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter", warnings

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}", warnings
    name = name.strip()
    if name:
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)", warnings
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens", warnings
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters.", warnings

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}", warnings
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)", warnings
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters.", warnings

    # ==================== QUALITY CHECKS (warnings) ====================

    # Check 1: SKILL.md line count
    line_count = count_lines(skill_md)
    if line_count > MAX_SKILL_MD_LINES:
        warnings.append(
            f"SKILL.md has {line_count} lines (recommended max: {MAX_SKILL_MD_LINES}). "
            "Consider moving details to references/."
        )

    # Check 2: Description length and triggers
    if len(description) < MIN_DESCRIPTION_LENGTH:
        warnings.append(
            f"Description is short ({len(description)} chars). "
            "Consider adding specific trigger scenarios."
        )

    # Check 3: Trigger keywords in description
    desc_lower = description.lower()
    has_trigger = any(keyword in desc_lower for keyword in TRIGGER_KEYWORDS)
    if not has_trigger:
        warnings.append(
            "Description lacks explicit trigger scenarios. "
            "Consider adding 'Use when...' or 'Triggers include...' phrases."
        )

    # Check 4: TODO placeholders
    if check_todo_placeholders(content):
        warnings.append(
            "SKILL.md contains TODO placeholders that should be completed."
        )

    # Check 5: Referenced files exist
    missing_refs = check_referenced_files_exist(skill_path, content)
    if missing_refs:
        warnings.append(
            f"Referenced files not found: {', '.join(missing_refs)}"
        )

    # Check 6: Empty resource directories
    for dir_name in ['scripts', 'references', 'assets']:
        dir_path = skill_path / dir_name
        if dir_path.exists():
            files = list(dir_path.glob('*'))
            # Filter out example files
            non_example_files = [f for f in files if 'example' not in f.name.lower()]
            if not non_example_files and files:
                warnings.append(
                    f"{dir_name}/ contains only example files. "
                    "Consider adding real content or removing the directory."
                )

    # Check 7: No code examples in body (suggests abstract-only)
    if '```' not in body_content and len(body_content) > 500:
        warnings.append(
            "SKILL.md body has no code examples. "
            "Consider adding concrete examples to improve clarity."
        )

    # Check 8: Directory name matches skill name
    if name and skill_path.name != name:
        warnings.append(
            f"Directory name '{skill_path.name}' doesn't match skill name '{name}'. "
            "These should be identical."
        )

    return True, "Skill is valid!", warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <skill_directory> [--strict] [--verbose]")
        print("\nOptions:")
        print("  --strict   Treat quality warnings as errors")
        print("  --verbose  Show all checks performed")
        sys.exit(1)

    skill_path = sys.argv[1]
    strict = '--strict' in sys.argv
    verbose = '--verbose' in sys.argv

    if verbose:
        print(f"🔍 Validating skill: {skill_path}")
        print(f"   Mode: {'strict' if strict else 'standard'}")
        print()

    valid, message, warnings = validate_skill(skill_path, strict, verbose)

    # Print result
    if valid:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

    # Print warnings
    if warnings:
        print(f"\n⚠️  Quality warnings ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")

        if strict and warnings:
            print("\n❌ Strict mode: warnings treated as errors")
            sys.exit(1)
    elif verbose:
        print("\n✅ No quality warnings")

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()