#!/usr/bin/env python3
"""
Fix Double Curly Braces in Modeling_2026
=========================================

Fixes template escaping issue where { and } were not converted to { and }

Usage:
    python fix_double_braces.py [repo_path] [--dry-run]
"""

import sys
import argparse
from pathlib import Path


def fix_file(file_path: Path, dry_run: bool = False) -> tuple:
    """Fix double braces in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, 0, str(e)
    
    original = content
    
    # Count replacements
    double_open = content.count('{')
    double_close = content.count('}')
    
    # Replace { with { and } with }
    content = content.replace('{', '{')
    content = content.replace('}', '}')
    
    total_replaced = double_open + double_close
    
    if content != original:
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return True, total_replaced, None
    
    return False, 0, None


def main():
    parser = argparse.ArgumentParser(description='Fix double curly braces')
    parser.add_argument('repo_path', nargs='?', default='.', help='Repository path')
    parser.add_argument('--dry-run', action='store_true', help='Preview only')
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    print("=" * 60)
    print("DOUBLE CURLY BRACE FIXER")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY FIXES'}")
    print()
    
    files_fixed = 0
    total_replacements = 0
    
    # Find all Python files
    for py_file in repo_path.glob('**/*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        fixed, count, error = fix_file(py_file, args.dry_run)
        
        if error:
            print(f"❌ Error in {py_file}: {error}")
        elif fixed:
            files_fixed += 1
            total_replacements += count
            rel_path = py_file.relative_to(repo_path)
            print(f"{'Would fix' if args.dry_run else 'Fixed'}: {rel_path} ({count} replacements)")
    
    print()
    print("=" * 60)
    print(f"Files fixed: {files_fixed}")
    print(f"Total brace replacements: {total_replacements}")
    print("=" * 60)
    
    if args.dry_run and files_fixed > 0:
        print("\nRun without --dry-run to apply fixes")


if __name__ == '__main__':
    main()
