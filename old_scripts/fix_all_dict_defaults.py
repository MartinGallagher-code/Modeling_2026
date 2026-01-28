#!/usr/bin/env python3
"""
Comprehensive Fix for Dict/List Defaults in Modeling_2026
==========================================================

Fixes ALL instances of mutable default arguments in dataclasses and class definitions.

Usage:
    python fix_all_dict_defaults.py [repo_path] [--dry-run]
"""

import os
import sys
import re
import argparse
from pathlib import Path


def fix_file_comprehensive(file_path: Path, dry_run: bool = False) -> tuple:
    """Comprehensively fix all mutable default issues in a file"""
    changes = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, [f"Error reading: {e}"]
    
    original = content
    
    # Pattern 1: Dataclass field with Dict type and {} default
    # e.g., "    utilizations: Dict[str, float] = {}"
    pattern1 = r'(\n\s+)(\w+)(\s*:\s*Dict\[[^\]]+\])\s*=\s*\{\}'
    if re.search(pattern1, content):
        content = re.sub(pattern1, r'\1\2\3 = field(default_factory=dict)', content)
        changes.append("Fixed Dict[...] = {} patterns")
    
    # Pattern 2: Dataclass field with List type and [] default
    pattern2 = r'(\n\s+)(\w+)(\s*:\s*List\[[^\]]+\])\s*=\s*\[\]'
    if re.search(pattern2, content):
        content = re.sub(pattern2, r'\1\2\3 = field(default_factory=list)', content)
        changes.append("Fixed List[...] = [] patterns")
    
    # Pattern 3: Simple dict type hint
    pattern3 = r'(\n\s+)(\w+)(\s*:\s*dict)\s*=\s*\{\}'
    if re.search(pattern3, content):
        content = re.sub(pattern3, r'\1\2\3 = field(default_factory=dict)', content)
        changes.append("Fixed dict = {} patterns")
    
    # Pattern 4: Simple list type hint  
    pattern4 = r'(\n\s+)(\w+)(\s*:\s*list)\s*=\s*\[\]'
    if re.search(pattern4, content):
        content = re.sub(pattern4, r'\1\2\3 = field(default_factory=list)', content)
        changes.append("Fixed list = [] patterns")
    
    # Pattern 5: Optional Dict with {} default
    pattern5 = r'(\n\s+)(\w+)(\s*:\s*Optional\[Dict\[[^\]]+\]\])\s*=\s*\{\}'
    if re.search(pattern5, content):
        content = re.sub(pattern5, r'\1\2\3 = field(default_factory=dict)', content)
        changes.append("Fixed Optional[Dict] = {} patterns")
    
    # Pattern 6: Any type with {} or [] (in dataclass context)
    pattern6 = r'(\n\s+)(\w+)(\s*:\s*Any)\s*=\s*\{\}'
    if re.search(pattern6, content):
        content = re.sub(pattern6, r'\1\2\3 = field(default_factory=dict)', content)
        changes.append("Fixed Any = {} patterns")
    
    pattern7 = r'(\n\s+)(\w+)(\s*:\s*Any)\s*=\s*\[\]'
    if re.search(pattern7, content):
        content = re.sub(pattern7, r'\1\2\3 = field(default_factory=list)', content)
        changes.append("Fixed Any = [] patterns")
    
    # Ensure 'field' is imported if we made changes
    if changes and 'field' not in content:
        # Add field to dataclasses import
        if 'from dataclasses import' in content:
            content = re.sub(
                r'(from dataclasses import )([^\n]+)',
                lambda m: m.group(1) + m.group(2).rstrip() + (', field' if 'field' not in m.group(2) else ''),
                content,
                count=1
            )
            changes.append("Added 'field' to dataclasses import")
        else:
            # Add new import
            content = "from dataclasses import field\n" + content
            changes.append("Added dataclasses field import")
    
    if content != original:
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return True, changes
    
    return False, []


def main():
    parser = argparse.ArgumentParser(description='Fix all mutable default issues')
    parser.add_argument('repo_path', nargs='?', default='.', help='Repository path')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes only')
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    print("=" * 60)
    print("COMPREHENSIVE DICT/LIST DEFAULT FIXER")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY FIXES'}")
    print()
    
    # Find all Python files
    patterns = ['**/*.py']
    files_checked = 0
    files_fixed = 0
    all_changes = []
    
    for pattern in patterns:
        for file_path in repo_path.glob(pattern):
            if file_path.is_file() and '__pycache__' not in str(file_path):
                files_checked += 1
                fixed, changes = fix_file_comprehensive(file_path, args.dry_run)
                if fixed:
                    files_fixed += 1
                    rel_path = file_path.relative_to(repo_path)
                    all_changes.append((rel_path, changes))
                    print(f"{'Would fix' if args.dry_run else 'Fixed'}: {rel_path}")
                    for c in changes:
                        print(f"  - {c}")
    
    print()
    print("=" * 60)
    print(f"Files checked: {files_checked}")
    print(f"Files {'to fix' if args.dry_run else 'fixed'}: {files_fixed}")
    print("=" * 60)
    
    if args.dry_run and files_fixed > 0:
        print("\nRun without --dry-run to apply fixes")


if __name__ == '__main__':
    main()
