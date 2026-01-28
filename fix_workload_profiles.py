#!/usr/bin/env python3
"""
Fix Workload Profile String Issue in Modeling_2026
===================================================

Fixes the issue where category_weights in WorkloadProfile is a string
representation of a dict instead of an actual dict.

Usage:
    python fix_workload_profiles.py [repo_path] [--dry-run]
"""

import os
import sys
import re
import argparse
from pathlib import Path


def fix_file(file_path: Path, dry_run: bool = False) -> tuple:
    """Fix workload profile string issues in a file"""
    changes = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, [f"Error reading: {e}"]
    
    original = content
    
    # Pattern 1: category_weights="{'key': value, ...}"
    # Should be: category_weights={'key': value, ...}
    pattern1 = r"category_weights\s*=\s*\"(\{[^\"]+\})\""
    matches1 = re.findall(pattern1, content)
    if matches1:
        content = re.sub(pattern1, r'category_weights=\1', content)
        changes.append(f"Fixed {len(matches1)} double-quoted category_weights")
    
    # Pattern 2: category_weights='{'key': value, ...}'
    # This is trickier because of nested quotes
    pattern2 = r"category_weights\s*=\s*'(\{[^']+\})'"
    matches2 = re.findall(pattern2, content)
    if matches2:
        content = re.sub(pattern2, r'category_weights=\1', content)
        changes.append(f"Fixed {len(matches2)} single-quoted category_weights")
    
    # Pattern 3: String dict with escaped quotes
    # category_weights="{\'key\': value}"
    pattern3 = r'category_weights\s*=\s*"(\{[^"]*\\\'[^"]*\})"'
    if re.search(pattern3, content):
        def fix_escaped(m):
            inner = m.group(1).replace("\\'", "'")
            return f'category_weights={inner}'
        content = re.sub(pattern3, fix_escaped, content)
        changes.append("Fixed escaped quote category_weights")
    
    # Pattern 4: Fix any remaining string-wrapped dicts in WorkloadProfile
    # Look for WorkloadProfile(...category_weights="..." or '...')
    pattern4 = r"(WorkloadProfile\([^)]*category_weights\s*=\s*)(['\"])(\{[^'\"]+\})\2"
    matches4 = re.findall(pattern4, content)
    if matches4:
        content = re.sub(pattern4, r'\1\3', content)
        changes.append(f"Fixed {len(matches4)} WorkloadProfile category_weights")
    
    if content != original:
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return True, changes
    
    return False, []


def main():
    parser = argparse.ArgumentParser(description='Fix workload profile string issues')
    parser.add_argument('repo_path', nargs='?', default='.', help='Repository path')
    parser.add_argument('--dry-run', action='store_true', help='Preview only')
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    print("=" * 60)
    print("WORKLOAD PROFILE STRING FIXER")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY FIXES'}")
    print()
    
    files_fixed = 0
    
    for py_file in repo_path.glob('**/*_validated.py'):
        if '__pycache__' in str(py_file):
            continue
        
        fixed, changes = fix_file(py_file, args.dry_run)
        
        if fixed:
            files_fixed += 1
            rel_path = py_file.relative_to(repo_path)
            print(f"{'Would fix' if args.dry_run else 'Fixed'}: {rel_path}")
            for c in changes:
                print(f"  - {c}")
    
    print()
    print("=" * 60)
    print(f"Files fixed: {files_fixed}")
    
    if args.dry_run and files_fixed > 0:
        print("\nRun without --dry-run to apply fixes")
    print("=" * 60)


if __name__ == '__main__':
    main()


def show_problematic_lines(repo_path: Path):
    """Show actual problematic lines for debugging"""
    print("\nSearching for problematic patterns...")
    print("-" * 50)
    
    for py_file in repo_path.glob('**/*_validated.py'):
        if '__pycache__' in str(py_file):
            continue
        
        try:
            with open(py_file, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                if 'category_weights' in line and ('="' in line or "='" in line):
                    rel_path = py_file.relative_to(repo_path)
                    print(f"\n{rel_path}:{i}")
                    print(f"  {line.strip()}")
        except:
            pass


if __name__ == '__main__':
    import sys
    if '--show' in sys.argv:
        repo_path = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else '.').resolve()
        show_problematic_lines(repo_path)
    else:
        main()
