#!/usr/bin/env python3
"""Find source files without corresponding test files.

Usage:
    python find_coverage_gaps.py [src_dir] [test_dir] [--limit N]

Examples:
    python find_coverage_gaps.py
    python find_coverage_gaps.py api/src api/test --limit 10
"""

import argparse
import sys
from pathlib import Path

# Default directories follow ABP Framework conventions
DEFAULT_SRC_DIR = "api/src"
DEFAULT_TEST_DIR = "api/test"

# Maximum files to report (balances usefulness vs. overwhelming output)
DEFAULT_LIMIT = 5

# Patterns to skip (generated code, infrastructure)
SKIP_PATTERNS = {
    ".Designer.cs",
    ".generated.cs",
    "AssemblyInfo.cs",
    "GlobalUsings.cs",
}

# Directories to skip
SKIP_DIRS = {"obj", "bin", "Migrations", "Properties"}


def find_source_files(src_dir: Path) -> list[Path]:
    """Find all C# source files, excluding generated code."""
    if not src_dir.exists():
        print(f"Error: Source directory not found: {src_dir}")
        print(f"Hint: Check the directory path or run from project root.")
        return []

    files = []
    for file in src_dir.rglob("*.cs"):
        # Skip generated files
        if any(pattern in file.name for pattern in SKIP_PATTERNS):
            continue
        # Skip certain directories
        if any(skip in file.parts for skip in SKIP_DIRS):
            continue
        files.append(file)

    return files


def find_test_files(test_dir: Path) -> set[str]:
    """Find all test file names (without path) for quick lookup."""
    if not test_dir.exists():
        print(f"Warning: Test directory not found: {test_dir}")
        return set()

    test_names = set()
    for file in test_dir.rglob("*Tests.cs"):
        # Extract the class name being tested
        # e.g., "UserAppServiceTests.cs" -> "UserAppService"
        base_name = file.stem.replace("Tests", "").replace("IntegrationTests", "")
        test_names.add(base_name)

    return test_names


def extract_class_name(file_path: Path) -> str:
    """Extract primary class name from file (assumes file name matches class)."""
    return file_path.stem


def find_gaps(
    src_dir: Path,
    test_dir: Path,
    limit: int
) -> list[tuple[Path, str]]:
    """Find source files without corresponding test files."""
    source_files = find_source_files(src_dir)
    if not source_files:
        return []

    test_names = find_test_files(test_dir)

    gaps = []
    for src_file in source_files:
        class_name = extract_class_name(src_file)

        # Check if any test exists for this class
        if class_name not in test_names:
            # Determine class type for prioritization
            if "AppService" in class_name:
                priority = 1  # High priority
            elif "Validator" in class_name:
                priority = 2
            elif "Controller" in class_name:
                priority = 3
            else:
                priority = 4  # Lower priority

            gaps.append((src_file, class_name, priority))

    # Sort by priority, then alphabetically
    gaps.sort(key=lambda x: (x[2], x[1]))

    return [(path, name) for path, name, _ in gaps[:limit]]


def main():
    parser = argparse.ArgumentParser(
        description="Find source files without test coverage"
    )
    parser.add_argument(
        "src_dir",
        nargs="?",
        default=DEFAULT_SRC_DIR,
        help=f"Source directory (default: {DEFAULT_SRC_DIR})"
    )
    parser.add_argument(
        "test_dir",
        nargs="?",
        default=DEFAULT_TEST_DIR,
        help=f"Test directory (default: {DEFAULT_TEST_DIR})"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Maximum files to report (default: {DEFAULT_LIMIT})"
    )
    args = parser.parse_args()

    gaps = find_gaps(
        Path(args.src_dir),
        Path(args.test_dir),
        args.limit
    )

    if not gaps:
        print("No coverage gaps found (or source directory is empty).")
        sys.exit(0)

    print(f"Found {len(gaps)} files without tests:\n")
    for file_path, class_name in gaps:
        print(f"  {file_path}")

    print(f"\nRun: python scripts/generate_tests.py <file> to generate tests")


if __name__ == "__main__":
    main()
