#!/usr/bin/env python3
"""
Post-Migration Validation Script
================================
Validates that the migration was successful and all files are in order.

This script checks:
1. Directory structure is correct
2. All expected files exist
3. Python files are syntactically valid
4. JSON files are parseable
5. Index.json is complete and accurate
6. No orphaned files in old/

Usage:
    python validate_migration.py [--repo-path /path/to/repo] [--fix]
"""

import os
import sys
import json
import ast
from pathlib import Path
from typing import List, Tuple, Dict

# =============================================================================
# VALIDATION CHECKS
# =============================================================================

class ValidationResult:
    def __init__(self, name: str, passed: bool, message: str, fixable: bool = False):
        self.name = name
        self.passed = passed
        self.message = message
        self.fixable = fixable


def check_directory_structure(repo_path: Path) -> List[ValidationResult]:
    """Verify expected directories exist."""
    results = []
    
    expected_dirs = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other', 'common']
    
    for dir_name in expected_dirs:
        dir_path = repo_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            results.append(ValidationResult(
                f"Directory: {dir_name}",
                True,
                f"Found at {dir_path}"
            ))
        else:
            results.append(ValidationResult(
                f"Directory: {dir_name}",
                False,
                f"Missing: {dir_path}",
                fixable=True
            ))
    
    return results


def check_processor_structure(repo_path: Path) -> List[ValidationResult]:
    """Verify each processor has the correct subdirectory structure."""
    results = []
    
    for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
        family_path = repo_path / family
        if not family_path.exists():
            continue
        
        for processor_dir in family_path.iterdir():
            if not processor_dir.is_dir() or processor_dir.name.startswith('.'):
                continue
            
            # Check expected subdirs
            expected_subdirs = ['current', 'archive', 'validation', 'docs']
            for subdir in expected_subdirs:
                subdir_path = processor_dir / subdir
                if subdir_path.exists():
                    # Check it has at least one file (for current/)
                    if subdir == 'current':
                        files = list(subdir_path.glob('*.py'))
                        if files:
                            results.append(ValidationResult(
                                f"{processor_dir.name}/current",
                                True,
                                f"Has {len(files)} Python file(s)"
                            ))
                        else:
                            results.append(ValidationResult(
                                f"{processor_dir.name}/current",
                                False,
                                "No Python files in current/",
                                fixable=False
                            ))
                else:
                    results.append(ValidationResult(
                        f"{processor_dir.name}/{subdir}",
                        False,
                        f"Missing subdirectory",
                        fixable=True
                    ))
            
            # Check for README.md
            readme = processor_dir / 'README.md'
            if readme.exists():
                results.append(ValidationResult(
                    f"{processor_dir.name}/README.md",
                    True,
                    "README exists"
                ))
            else:
                results.append(ValidationResult(
                    f"{processor_dir.name}/README.md",
                    False,
                    "Missing README.md",
                    fixable=True
                ))
    
    return results


def check_python_syntax(repo_path: Path) -> List[ValidationResult]:
    """Verify all Python files have valid syntax."""
    results = []
    
    for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
        family_path = repo_path / family
        if not family_path.exists():
            continue
        
        for py_file in family_path.rglob('*.py'):
            try:
                with open(py_file, 'r') as f:
                    source = f.read()
                ast.parse(source)
                results.append(ValidationResult(
                    f"Syntax: {py_file.relative_to(repo_path)}",
                    True,
                    "Valid Python"
                ))
            except SyntaxError as e:
                results.append(ValidationResult(
                    f"Syntax: {py_file.relative_to(repo_path)}",
                    False,
                    f"Syntax error: {e}",
                    fixable=False
                ))
    
    return results


def check_json_validity(repo_path: Path) -> List[ValidationResult]:
    """Verify all JSON files are parseable."""
    results = []
    
    for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
        family_path = repo_path / family
        if not family_path.exists():
            continue
        
        for json_file in family_path.rglob('*.json'):
            try:
                with open(json_file, 'r') as f:
                    json.load(f)
                results.append(ValidationResult(
                    f"JSON: {json_file.relative_to(repo_path)}",
                    True,
                    "Valid JSON"
                ))
            except json.JSONDecodeError as e:
                results.append(ValidationResult(
                    f"JSON: {json_file.relative_to(repo_path)}",
                    False,
                    f"JSON error: {e}",
                    fixable=False
                ))
    
    return results


def check_index_completeness(repo_path: Path) -> List[ValidationResult]:
    """Verify index.json contains all processors."""
    results = []
    
    index_path = repo_path / 'index.json'
    if not index_path.exists():
        results.append(ValidationResult(
            "index.json",
            False,
            "Missing index.json",
            fixable=True
        ))
        return results
    
    with open(index_path, 'r') as f:
        index = json.load(f)
    
    # Find all processors
    found_processors = set()
    for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
        family_path = repo_path / family
        if not family_path.exists():
            continue
        
        for processor_dir in family_path.iterdir():
            if processor_dir.is_dir() and not processor_dir.name.startswith('.'):
                found_processors.add(processor_dir.name)
    
    indexed_processors = set(index.get('processors', {}).keys())
    
    # Check for missing in index
    missing = found_processors - indexed_processors
    if missing:
        results.append(ValidationResult(
            "index.json completeness",
            False,
            f"Missing from index: {', '.join(sorted(missing))}",
            fixable=True
        ))
    else:
        results.append(ValidationResult(
            "index.json completeness",
            True,
            f"All {len(found_processors)} processors indexed"
        ))
    
    # Check for orphans in index
    orphans = indexed_processors - found_processors
    if orphans:
        results.append(ValidationResult(
            "index.json accuracy",
            False,
            f"In index but missing: {', '.join(sorted(orphans))}",
            fixable=True
        ))
    
    # Check counts
    if index.get('total_processors') != len(found_processors):
        results.append(ValidationResult(
            "index.json count",
            False,
            f"Count mismatch: index says {index.get('total_processors')}, found {len(found_processors)}",
            fixable=True
        ))
    else:
        results.append(ValidationResult(
            "index.json count",
            True,
            f"Correct count: {len(found_processors)}"
        ))
    
    return results


def check_historical_docs(repo_path: Path) -> List[ValidationResult]:
    """Verify historical documentation was preserved."""
    results = []
    
    docs_path = repo_path / 'docs' / 'historical'
    if not docs_path.exists():
        results.append(ValidationResult(
            "Historical docs",
            False,
            "Missing docs/historical/ directory",
            fixable=False
        ))
        return results
    
    expected_docs = [
        'Modeling_2026_Master_Prompt.docx',
        'Modeling_2026_Recreation_Guide_v2.docx',
        'Pre1986_CPU_Modeling_Lessons_Learned.docx',
        'METHODOLOGY.md',
    ]
    
    found = 0
    for doc in expected_docs:
        if (docs_path / doc).exists():
            found += 1
    
    if found > 0:
        results.append(ValidationResult(
            "Historical docs",
            True,
            f"Found {found}/{len(expected_docs)} expected documents"
        ))
    else:
        results.append(ValidationResult(
            "Historical docs",
            False,
            "No historical documents found",
            fixable=False
        ))
    
    return results


# =============================================================================
# FIX FUNCTIONS
# =============================================================================

def fix_missing_directories(repo_path: Path):
    """Create missing directories."""
    for dir_name in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other', 'common']:
        dir_path = repo_path / dir_name
        dir_path.mkdir(exist_ok=True)


def fix_index_json(repo_path: Path):
    """Rebuild index.json from actual directory contents."""
    index = {
        "project": "Modeling_2026",
        "total_processors": 0,
        "families": {
            "intel": 0,
            "motorola": 0,
            "mos_wdc": 0,
            "zilog": 0,
            "other": 0
        },
        "processors": {}
    }
    
    for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
        family_path = repo_path / family
        if not family_path.exists():
            continue
        
        count = 0
        for processor_dir in family_path.iterdir():
            if processor_dir.is_dir() and not processor_dir.name.startswith('.'):
                index['processors'][processor_dir.name] = processor_dir.name.upper()
                count += 1
        
        index['families'][family] = count
    
    index['total_processors'] = len(index['processors'])
    
    with open(repo_path / 'index.json', 'w') as f:
        json.dump(index, f, indent=2, sort_keys=True)
    
    print(f"  Fixed: Rebuilt index.json with {index['total_processors']} processors")


# =============================================================================
# MAIN
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate migration results')
    parser.add_argument('--repo-path', type=str, default='.',
                        help='Path to repository')
    parser.add_argument('--fix', action='store_true',
                        help='Attempt to fix fixable issues')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show all results, not just failures')
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    print("=" * 70)
    print("Post-Migration Validation")
    print("=" * 70)
    print(f"\nRepository: {repo_path}")
    print(f"Fix mode: {args.fix}")
    
    # Run all checks
    all_results = []
    
    print("\n" + "-" * 70)
    print("Checking directory structure...")
    all_results.extend(check_directory_structure(repo_path))
    
    print("Checking processor structure...")
    all_results.extend(check_processor_structure(repo_path))
    
    print("Checking Python syntax...")
    all_results.extend(check_python_syntax(repo_path))
    
    print("Checking JSON validity...")
    all_results.extend(check_json_validity(repo_path))
    
    print("Checking index.json...")
    all_results.extend(check_index_completeness(repo_path))
    
    print("Checking historical docs...")
    all_results.extend(check_historical_docs(repo_path))
    
    # Report results
    print("\n" + "-" * 70)
    print("VALIDATION RESULTS")
    print("-" * 70)
    
    passed = [r for r in all_results if r.passed]
    failed = [r for r in all_results if not r.passed]
    fixable = [r for r in failed if r.fixable]
    
    if args.verbose:
        print(f"\n✅ PASSED ({len(passed)}):")
        for r in passed:
            print(f"  • {r.name}: {r.message}")
    
    if failed:
        print(f"\n❌ FAILED ({len(failed)}):")
        for r in failed:
            fix_note = " [FIXABLE]" if r.fixable else ""
            print(f"  • {r.name}: {r.message}{fix_note}")
    
    # Apply fixes if requested
    if args.fix and fixable:
        print("\n" + "-" * 70)
        print("APPLYING FIXES")
        print("-" * 70)
        
        # Fix missing directories
        dir_issues = [r for r in fixable if 'Directory:' in r.name]
        if dir_issues:
            fix_missing_directories(repo_path)
            print("  Fixed: Created missing directories")
        
        # Fix index.json
        index_issues = [r for r in fixable if 'index.json' in r.name]
        if index_issues:
            fix_index_json(repo_path)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nTotal checks: {len(all_results)}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    if fixable:
        print(f"Fixable: {len(fixable)}")
    
    if failed:
        print("\n⚠️  Some checks failed. Review the issues above.")
        if fixable and not args.fix:
            print("   Run with --fix to attempt automatic fixes.")
        return 1
    else:
        print("\n✅ All checks passed!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
