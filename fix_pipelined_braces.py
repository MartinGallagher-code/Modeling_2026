#!/usr/bin/env python3
"""Fix double braces in pipelined model files"""
import sys
from pathlib import Path

PIPELINED = {
    'i80286': 'intel',
    'm68000': 'motorola', 
    'm68008': 'motorola',
    'm68010': 'motorola',
    'm68020': 'motorola',
    'ns32016': 'other',
}

repo = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()

print("Fixing double braces in pipelined models...")

for proc, family in PIPELINED.items():
    path = repo / family / proc / 'current' / f'{proc}_validated.py'
    if not path.exists():
        print(f"  {proc}: not found")
        continue
    
    with open(path, 'r') as f:
        content = f.read()
    
    if '{{' not in content and '}}' not in content:
        print(f"  {proc}: no double braces")
        continue
    
    # Replace double braces with single
    new_content = content.replace('{{', '{').replace('}}', '}')
    
    with open(path, 'w') as f:
        f.write(new_content)
    
    count = content.count('{{') + content.count('}}')
    print(f"  ✅ {proc}: fixed {count} double braces")

print("\nDone! Run: python check_fixed_models.py .")
