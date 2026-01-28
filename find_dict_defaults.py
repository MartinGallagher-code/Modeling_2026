#!/usr/bin/env python3
"""
Find all instances of mutable defaults in Python files.
Shows exactly what lines need to be fixed.
"""

import sys
import re
from pathlib import Path

def find_issues(file_path):
    """Find problematic lines in a file"""
    issues = []
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        in_dataclass = False
        for i, line in enumerate(lines, 1):
            # Track if we're in a dataclass
            if '@dataclass' in line:
                in_dataclass = True
            elif line.strip().startswith('class ') and in_dataclass:
                pass  # Still in dataclass
            elif line.strip().startswith('class '):
                in_dataclass = False
            elif line.strip().startswith('def '):
                in_dataclass = False
            
            # Look for problematic patterns
            if in_dataclass or ':' in line:
                # Dict default
                if re.search(r':\s*(Dict\[|dict).*=\s*\{\}', line):
                    issues.append((i, line.rstrip(), 'Dict = {}'))
                # List default
                if re.search(r':\s*(List\[|list).*=\s*\[\]', line):
                    issues.append((i, line.rstrip(), 'List = []'))
                # Any with {}
                if re.search(r':\s*Any\s*=\s*\{\}', line):
                    issues.append((i, line.rstrip(), 'Any = {}'))
                    
    except Exception as e:
        return [(0, f"Error: {e}", 'error')]
    
    return issues

def main():
    repo_path = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    
    print("Searching for mutable default values...")
    print("=" * 70)
    
    total_issues = 0
    for py_file in repo_path.glob('**/*.py'):
        if '__pycache__' in str(py_file):
            continue
        issues = find_issues(py_file)
        if issues:
            rel_path = py_file.relative_to(repo_path)
            print(f"\n📄 {rel_path}")
            for line_num, line, issue_type in issues:
                print(f"   Line {line_num}: {line}")
                print(f"   ⚠️  Issue: {issue_type} -> needs field(default_factory=...)")
                total_issues += 1
    
    print()
    print("=" * 70)
    print(f"Total issues found: {total_issues}")
    
    if total_issues > 0:
        print("\nTo fix, run: python fix_all_dict_defaults.py .")

if __name__ == '__main__':
    main()
