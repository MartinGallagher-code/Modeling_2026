#!/usr/bin/env python3
"""
Simple Fix for Pipelined Models
================================

The pipelined models have one broken line:
    base_cpi = self.pipeline_stages[bottleneck_stage]

This should be:
    base_cpi = sum(w * self.instruction_categories[c].base_cycles 
                   for c, w in profile.category_weights.items() 
                   if c in self.instruction_categories)

This script makes just that one-line fix.

Usage:
    1. First restore files: sh restore_pipelined.sh
    2. Then run: python fix_pipelined_simple.py .

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import sys
import re
import argparse
from pathlib import Path


PIPELINED_PROCESSORS = {
    'i80286': 'intel',
    'm68000': 'motorola', 
    'm68008': 'motorola',
    'm68010': 'motorola',
    'm68020': 'motorola',
    'ns32016': 'other',
}

# The broken line pattern
OLD_LINE_PATTERN = r'base_cpi\s*=\s*self\.pipeline_stages\[bottleneck_stage\]'

# The fixed line - calculates weighted CPI from instruction categories
NEW_LINE = '''# Calculate weighted CPI from instruction categories (FIXED)
        base_cpi = 0.0
        for cat_name, weight in profile.category_weights.items():
            if cat_name in self.instruction_categories:
                base_cpi += weight * self.instruction_categories[cat_name].base_cycles'''


def fix_file(file_path: Path, dry_run: bool = False) -> tuple:
    """Apply the one-line fix"""
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        return False, f"Read error: {e}"
    
    # Check if already fixed
    if 'Calculate weighted CPI from instruction categories' in content:
        return False, "Already fixed"
    
    # Check if has the broken pattern
    if not re.search(OLD_LINE_PATTERN, content):
        return False, "Pattern not found - may have different structure"
    
    # Replace the broken line
    # Match the line with its indentation
    pattern = r'(\s*)' + OLD_LINE_PATTERN
    replacement = r'\1' + NEW_LINE.replace('\n', '\n\\1').lstrip()
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content == content:
        return False, "Replacement failed"
    
    # Verify syntax
    try:
        compile(new_content, str(file_path), 'exec')
    except SyntaxError as e:
        return False, f"Syntax error after fix: {e}"
    
    if not dry_run:
        with open(file_path, 'w') as f:
            f.write(new_content)
    
    return True, "Fixed base_cpi calculation"


def main():
    parser = argparse.ArgumentParser(description='Simple one-line fix for pipelined models')
    parser.add_argument('repo_path', nargs='?', default='.', help='Repository path')
    parser.add_argument('--dry-run', action='store_true', help='Preview only')
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    print("=" * 60)
    print("SIMPLE PIPELINED MODEL FIX")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY'}")
    print()
    print("This fixes the line:")
    print("  OLD: base_cpi = self.pipeline_stages[bottleneck_stage]")
    print("  NEW: base_cpi = sum(weight * category.base_cycles)")
    print()
    
    fixed = 0
    
    for proc_name, family in PIPELINED_PROCESSORS.items():
        file_path = repo_path / family / proc_name / 'current' / f'{proc_name}_validated.py'
        
        if not file_path.exists():
            print(f"⚠️  {proc_name}: File not found")
            continue
        
        success, message = fix_file(file_path, args.dry_run)
        
        if success:
            print(f"✅ {proc_name}: {message}")
            fixed += 1
        else:
            print(f"⏭️  {proc_name}: {message}")
    
    print()
    print("=" * 60)
    print(f"Fixed: {fixed}/{len(PIPELINED_PROCESSORS)}")
    
    if args.dry_run and fixed > 0:
        print("\nRun without --dry-run to apply")
    elif fixed > 0:
        print("\nNow run: python advanced_calibrator.py . --calibrate-all")


if __name__ == '__main__':
    main()
