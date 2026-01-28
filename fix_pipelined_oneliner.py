#!/usr/bin/env python3
"""
One-Liner Fix for Pipelined Models
===================================

Replaces the broken line with a working one-liner.

Usage:
    python fix_pipelined_oneliner.py .
"""

import sys
from pathlib import Path

PIPELINED_PROCESSORS = {
    'i80286': 'intel',
    'm68000': 'motorola', 
    'm68008': 'motorola',
    'm68010': 'motorola',
    'm68020': 'motorola',
    'ns32016': 'other',
}

# Exact strings to find and replace
OLD_LINE = "        base_cpi = self.pipeline_stages[bottleneck_stage]"
NEW_LINE = "        base_cpi = sum(w * self.instruction_categories[c].base_cycles for c, w in profile.category_weights.items() if c in self.instruction_categories)"


def main():
    repo_path = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    dry_run = '--dry-run' in sys.argv
    
    print("=" * 60)
    print("ONE-LINER FIX FOR PIPELINED MODELS")
    print("=" * 60)
    print(f"Mode: {'DRY-RUN' if dry_run else 'APPLY'}")
    print()
    
    fixed = 0
    
    for proc_name, family in PIPELINED_PROCESSORS.items():
        file_path = repo_path / family / proc_name / 'current' / f'{proc_name}_validated.py'
        
        if not file_path.exists():
            print(f"⚠️  {proc_name}: Not found")
            continue
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        if OLD_LINE not in content:
            print(f"⏭️  {proc_name}: Pattern not found (may already be fixed or different)")
            continue
        
        new_content = content.replace(OLD_LINE, NEW_LINE)
        
        # Verify syntax
        try:
            compile(new_content, str(file_path), 'exec')
        except SyntaxError as e:
            print(f"❌ {proc_name}: Syntax error - {e}")
            continue
        
        if not dry_run:
            with open(file_path, 'w') as f:
                f.write(new_content)
        
        print(f"✅ {proc_name}: Fixed")
        fixed += 1
    
    print()
    print(f"Fixed: {fixed}/6")
    
    if fixed > 0 and not dry_run:
        print("\nNow run: python advanced_calibrator.py . --calibrate-all")


if __name__ == '__main__':
    main()
