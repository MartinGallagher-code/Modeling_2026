#!/usr/bin/env python3
"""
Fix Dataclass Default Values in Modeling_2026
==============================================

This script fixes the "unhashable type: 'dict'" error that occurs when
dataclasses use mutable default values like {} or [] directly.

The fix: Replace `= {}` with `= field(default_factory=dict)`
         Replace `= []` with `= field(default_factory=list)`

Usage:
    python fix_dataclass_defaults.py [repo_path] [--dry-run]

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import List, Tuple


# Patterns to find and fix
PATTERNS = [
    # Dict defaults in dataclasses
    (
        r'(\s+\w+:\s*Dict\[[\w\s,\[\]]+\])\s*=\s*\{\}',
        r'\1 = field(default_factory=dict)'
    ),
    (
        r'(\s+\w+:\s*dict)\s*=\s*\{\}',
        r'\1 = field(default_factory=dict)'
    ),
    # List defaults in dataclasses  
    (
        r'(\s+\w+:\s*List\[[\w\s,\[\]]+\])\s*=\s*\[\]',
        r'\1 = field(default_factory=list)'
    ),
    (
        r'(\s+\w+:\s*list)\s*=\s*\[\]',
        r'\1 = field(default_factory=list)'
    ),
    # Set defaults in dataclasses
    (
        r'(\s+\w+:\s*Set\[[\w\s,\[\]]+\])\s*=\s*set\(\)',
        r'\1 = field(default_factory=set)'
    ),
]


def check_has_field_import(content: str) -> bool:
    """Check if 'field' is imported from dataclasses"""
    return bool(re.search(r'from dataclasses import.*\bfield\b', content))


def add_field_import(content: str) -> str:
    """Add 'field' to dataclasses import if not present"""
    if check_has_field_import(content):
        return content
    
    # Try to add to existing dataclasses import
    pattern = r'(from dataclasses import )([^;\n]+)'
    match = re.search(pattern, content)
    if match:
        existing_imports = match.group(2).strip()
        if 'field' not in existing_imports:
            new_imports = existing_imports.rstrip(')').rstrip() + ', field'
            if existing_imports.endswith(')'):
                new_imports += ')'
            content = re.sub(pattern, r'\1' + new_imports, content, count=1)
    else:
        # Add new import after other imports
        import_section_end = 0
        for match in re.finditer(r'^(import |from )[^\n]+\n', content, re.MULTILINE):
            import_section_end = match.end()
        
        if import_section_end > 0:
            content = content[:import_section_end] + 'from dataclasses import field\n' + content[import_section_end:]
        else:
            content = 'from dataclasses import field\n' + content
    
    return content


def fix_file(file_path: Path, dry_run: bool = False) -> Tuple[bool, List[str]]:
    """Fix dataclass defaults in a single file"""
    changes = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return False, [f"Error reading file: {e}"]
    
    content = original_content
    needs_field_import = False
    
    # Apply each pattern
    for pattern, replacement in PATTERNS:
        matches = list(re.finditer(pattern, content))
        if matches:
            for match in matches:
                changes.append(f"  Fixed: {match.group(0).strip()} -> {re.sub(pattern, replacement, match.group(0)).strip()}")
            content = re.sub(pattern, replacement, content)
            needs_field_import = True
    
    # Add field import if needed
    if needs_field_import and not check_has_field_import(content):
        content = add_field_import(content)
        changes.append("  Added 'field' to dataclasses import")
    
    # Write changes if any
    if content != original_content:
        if not dry_run:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                return False, [f"Error writing file: {e}"]
        return True, changes
    
    return False, []


def fix_repository(repo_path: Path, dry_run: bool = False) -> dict:
    """Fix all Python files in the repository"""
    results = {
        'files_checked': 0,
        'files_fixed': 0,
        'changes': []
    }
    
    # Files to check
    patterns = [
        'common/**/*.py',
        'intel/**/*.py',
        'motorola/**/*.py',
        'mos_wdc/**/*.py',
        'zilog/**/*.py',
        'other/**/*.py',
    ]
    
    for pattern in patterns:
        for file_path in repo_path.glob(pattern):
            if file_path.is_file() and not file_path.name.startswith('.'):
                results['files_checked'] += 1
                fixed, changes = fix_file(file_path, dry_run)
                if fixed:
                    results['files_fixed'] += 1
                    results['changes'].append({
                        'file': str(file_path.relative_to(repo_path)),
                        'changes': changes
                    })
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Fix dataclass mutable default values in Modeling_2026'
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Path to repository'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would change without making changes'
    )
    parser.add_argument(
        '--file',
        help='Fix a specific file only'
    )
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Path does not exist: {repo_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("DATACLASS DEFAULT VALUE FIXER")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY FIXES'}")
    print()
    
    if args.file:
        # Fix single file
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = repo_path / file_path
        
        print(f"Fixing: {file_path}")
        fixed, changes = fix_file(file_path, args.dry_run)
        if fixed:
            print("Changes:")
            for change in changes:
                print(change)
        else:
            print("No changes needed")
    else:
        # Fix entire repository
        results = fix_repository(repo_path, args.dry_run)
        
        print(f"Files checked: {results['files_checked']}")
        print(f"Files fixed: {results['files_fixed']}")
        print()
        
        if results['changes']:
            print("CHANGES:")
            print("-" * 40)
            for item in results['changes']:
                print(f"\n📄 {item['file']}")
                for change in item['changes']:
                    print(change)
        else:
            print("No changes needed - all files OK")
    
    print()
    print("=" * 60)
    if args.dry_run:
        print("DRY RUN - No files were modified")
        print("Run without --dry-run to apply fixes")
    else:
        print("DONE")
    print("=" * 60)


if __name__ == '__main__':
    main()
